#!/usr/bin/env python3
"""Build deterministic complete-release and manuscript-source ZIP archives."""

from __future__ import annotations

import argparse
import hashlib
import re
import stat
import sys
import zipfile
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence

try:
    from tools.verify_manifest import (
        MANIFEST_NAME,
        ManifestError,
        parse_manifest,
        verify_manifest,
    )
except ModuleNotFoundError:
    from verify_manifest import (  # type: ignore[no-redef]
        MANIFEST_NAME,
        ManifestError,
        parse_manifest,
        verify_manifest,
    )


DEFAULT_VERSION = "1.3.0"
DEFAULT_SOURCE_DATE_EPOCH = 1785369600
VERSION_PATTERN = re.compile(r"^[0-9A-Za-z][0-9A-Za-z._-]*$")
SOURCE_ARCHIVE_MEMBERS = (
    "CITATION.cff",
    "LICENSES/paper-and-documentation.txt",
    "REPRODUCING.md",
    "SOURCE_AVAILABILITY.md",
    "paper/source/On_Boundaries_of_Evidence.bib",
    "paper/source/On_Boundaries_of_Evidence.tex",
)


class ArchiveError(ValueError):
    """Raised when deterministic archive construction cannot proceed."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_relative_path(path: str) -> str:
    if "\x00" in path or "\\" in path:
        raise ArchiveError(f"unsafe archive member path: {path!r}")
    pure = PurePosixPath(path)
    if not path or pure.is_absolute():
        raise ArchiveError(f"unsafe archive member path: {path!r}")
    if any(part in {"", ".", ".."} for part in pure.parts):
        raise ArchiveError(f"unsafe archive member path: {path!r}")
    if str(pure) != path:
        raise ArchiveError(f"non-normalized archive member path: {path!r}")
    return path


def normalized_zip_time(source_date_epoch: int) -> tuple[int, ...]:
    try:
        instant = datetime.fromtimestamp(source_date_epoch, tz=UTC)
    except (OverflowError, OSError, ValueError) as exc:
        raise ArchiveError(f"invalid SOURCE_DATE_EPOCH: {source_date_epoch}") from exc
    if not 1980 <= instant.year <= 2107:
        raise ArchiveError("ZIP timestamp must fall between 1980 and 2107")
    second = instant.second - (instant.second % 2)
    return (
        instant.year,
        instant.month,
        instant.day,
        instant.hour,
        instant.minute,
        second,
    )


def archive_info(
    name: str, *, is_directory: bool, timestamp: tuple[int, ...]
) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=timestamp)
    info.create_system = 3
    info.compress_type = zipfile.ZIP_STORED
    info.comment = b""
    info.extra = b""
    if is_directory:
        info.external_attr = (stat.S_IFDIR | 0o755) << 16 | 0x10
    else:
        info.external_attr = (stat.S_IFREG | 0o644) << 16
    return info


def directory_entries(root_prefix: str, members: Iterable[str]) -> set[str]:
    directories = {f"{root_prefix}/"}
    for member in members:
        parts = PurePosixPath(member).parts[:-1]
        for length in range(1, len(parts) + 1):
            partial = "/".join(parts[:length])
            directories.add(f"{root_prefix}/{partial}/")
    return directories


def write_deterministic_zip(
    output: Path,
    root: Path,
    root_prefix: str,
    members: Sequence[str],
    source_date_epoch: int,
) -> None:
    resolved_root = root.resolve()
    prefix = validate_relative_path(root_prefix)
    normalized_members = sorted(validate_relative_path(path) for path in members)
    if len(normalized_members) != len(set(normalized_members)):
        raise ArchiveError("archive member list contains duplicate paths")

    payload: dict[str, bytes] = {}
    for relative in normalized_members:
        path = resolved_root / relative
        try:
            mode = path.lstat().st_mode
        except OSError as exc:
            raise ArchiveError(f"cannot inspect archive member {relative}: {exc}") from exc
        if not stat.S_ISREG(mode):
            raise ArchiveError(f"archive member is not a regular file: {relative}")
        try:
            payload[f"{prefix}/{relative}"] = path.read_bytes()
        except OSError as exc:
            raise ArchiveError(f"cannot read archive member {relative}: {exc}") from exc

    names = sorted(
        directory_entries(prefix, normalized_members) | set(payload)
    )
    timestamp = normalized_zip_time(source_date_epoch)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        stream = output.open("xb")
    except FileExistsError as exc:
        raise ArchiveError(f"refusing to overwrite existing archive: {output}") from exc

    try:
        with stream, zipfile.ZipFile(
            stream,
            mode="w",
            compression=zipfile.ZIP_STORED,
            allowZip64=True,
            strict_timestamps=True,
        ) as archive:
            for name in names:
                is_directory = name.endswith("/")
                info = archive_info(
                    name,
                    is_directory=is_directory,
                    timestamp=timestamp,
                )
                archive.writestr(info, b"" if is_directory else payload[name])
    except Exception:
        output.unlink(missing_ok=True)
        raise


def build_release_archives(
    root: Path,
    manifest_path: Path,
    output_directory: Path,
    version: str,
    source_date_epoch: int,
) -> tuple[Path, Path]:
    if VERSION_PATTERN.fullmatch(version) is None:
        raise ArchiveError(f"unsafe release version: {version!r}")
    try:
        errors = verify_manifest(root, manifest_path)
    except ManifestError as exc:
        raise ArchiveError(str(exc)) from exc
    if errors:
        raise ArchiveError("; ".join(errors))

    manifest_entries = parse_manifest(manifest_path)
    complete_members = sorted([*manifest_entries, MANIFEST_NAME])
    missing_sources = sorted(set(SOURCE_ARCHIVE_MEMBERS) - set(manifest_entries))
    if missing_sources:
        raise ArchiveError(
            "source archive members missing from manifest: "
            + ", ".join(missing_sources)
        )

    complete_output = (
        output_directory
        / f"On_Boundaries_of_Evidence_v{version}_Complete_Release.zip"
    )
    source_output = (
        output_directory / f"On_Boundaries_of_Evidence_v{version}_Source.zip"
    )
    write_deterministic_zip(
        complete_output,
        root,
        f"On_Boundaries_of_Evidence_v{version}",
        complete_members,
        source_date_epoch,
    )
    try:
        write_deterministic_zip(
            source_output,
            root,
            f"On_Boundaries_of_Evidence_Source_v{version}",
            SOURCE_ARCHIVE_MEMBERS,
            source_date_epoch,
        )
    except Exception:
        complete_output.unlink(missing_ok=True)
        raise
    return complete_output, source_output


def build_parser() -> argparse.ArgumentParser:
    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description=(
            "Build byte-reproducible ZIP archives from a complete verified "
            "release manifest."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=repository_root,
        help="release tree root (default: repository root)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="manifest path (default: ROOT/MANIFEST.sha256)",
    )
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=None,
        help="archive directory (default: ROOT/dist)",
    )
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument(
        "--source-date-epoch",
        type=int,
        default=DEFAULT_SOURCE_DATE_EPOCH,
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    manifest = (
        args.manifest.resolve()
        if args.manifest is not None
        else root / MANIFEST_NAME
    )
    output_directory = (
        args.output_directory.resolve()
        if args.output_directory is not None
        else root / "dist"
    )
    try:
        complete, source = build_release_archives(
            root,
            manifest,
            output_directory,
            args.version,
            args.source_date_epoch,
        )
    except (ArchiveError, ManifestError) as exc:
        print(f"ARCHIVE: FAIL: {exc}", file=sys.stderr)
        return 1

    for path in (complete, source):
        print(f"ARCHIVE: {path.name}: {sha256_file(path)}")
    print("ARCHIVE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
