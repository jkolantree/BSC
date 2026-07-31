#!/usr/bin/env python3
"""Build deterministic complete-release and manuscript-source ZIP archives."""

from __future__ import annotations

import argparse
import hashlib
import stat
import sys
import zipfile
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence

try:
    from tools.archive_validation import (
        SOURCE_ARCHIVE_MEMBERS,
        ArchiveValidationError,
        verify_archive_payload,
    )
    from tools.release_identity import (
        BuildPlan,
        IdentityError,
        build_identity_document,
        canonical_manifest_path,
        canonical_spec_path,
        expected_artifact_names,
        expected_identity_name,
        require_tracked_file,
        resolve_build_plan,
        verify_head_payload,
        verify_identity_file,
        write_identity_file,
    )
    from tools.verify_manifest import (
        MANIFEST_NAME,
        ManifestError,
        parse_manifest,
        verify_manifest,
    )
except ModuleNotFoundError:
    from archive_validation import (  # type: ignore[no-redef]
        SOURCE_ARCHIVE_MEMBERS,
        ArchiveValidationError,
        verify_archive_payload,
    )
    from release_identity import (  # type: ignore[no-redef]
        BuildPlan,
        IdentityError,
        build_identity_document,
        canonical_manifest_path,
        canonical_spec_path,
        expected_artifact_names,
        expected_identity_name,
        require_tracked_file,
        resolve_build_plan,
        verify_head_payload,
        verify_identity_file,
        write_identity_file,
    )
    from verify_manifest import (  # type: ignore[no-redef]
        MANIFEST_NAME,
        ManifestError,
        parse_manifest,
        verify_manifest,
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
    plan: BuildPlan,
) -> tuple[Path, Path]:
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
        / f"On_Boundaries_of_Evidence_{plan.outer_label}_Complete_Release.zip"
    )
    source_output = (
        output_directory / f"On_Boundaries_of_Evidence_{plan.outer_label}_Source.zip"
    )
    write_deterministic_zip(
        complete_output,
        root,
        f"On_Boundaries_of_Evidence_{plan.archive_label}",
        complete_members,
        plan.build_epoch,
    )
    try:
        write_deterministic_zip(
            source_output,
            root,
            f"On_Boundaries_of_Evidence_Source_{plan.archive_label}",
            SOURCE_ARCHIVE_MEMBERS,
            plan.build_epoch,
        )
    except Exception:
        complete_output.unlink(missing_ok=True)
        raise
    return complete_output, source_output


def validate_output_directory(root: Path, output_directory: Path) -> Path:
    root = root.resolve()
    output = output_directory.resolve()
    try:
        relative = output.relative_to(root)
    except ValueError:
        return output
    if not relative.parts or relative.parts[0] not in {"build", "dist"}:
        raise ArchiveError(
            "output directory inside the release root must be under build/ or dist/"
        )
    return output


def create_release_artifacts(
    root: Path,
    manifest_path: Path,
    output_directory: Path,
    spec_path: Path,
    mode: str,
    requested_version: str | None = None,
) -> tuple[Path, Path, Path]:
    root = root.resolve()
    try:
        manifest = canonical_manifest_path(root, manifest_path)
        spec = canonical_spec_path(root, spec_path)
        require_tracked_file(root, Path(MANIFEST_NAME))
        plan = resolve_build_plan(root, spec, mode, requested_version)
        verify_head_payload(root, manifest)
    except IdentityError as exc:
        raise ArchiveError(str(exc)) from exc
    output = validate_output_directory(root, output_directory)
    artifact_names = expected_artifact_names(plan)
    complete = output / artifact_names["complete-release"]
    source = output / artifact_names["manuscript-source"]
    identity = output / expected_identity_name(plan)
    outputs = (complete, source, identity)
    existing = [path for path in outputs if path.exists()]
    if existing:
        raise ArchiveError(
            "refusing to overwrite existing output: "
            + ", ".join(path.name for path in existing)
        )
    output.mkdir(parents=True, exist_ok=True)

    created_outputs: list[Path] = []
    try:
        built_complete, built_source = build_release_archives(
            root, manifest, output, plan
        )
        created_outputs.extend((built_complete, built_source))
        manifest_entries = parse_manifest(manifest)
        verify_archive_payload(
            built_complete,
            f"On_Boundaries_of_Evidence_{plan.archive_label}",
            sorted([*manifest_entries, MANIFEST_NAME]),
            manifest,
            plan.build_epoch,
        )
        verify_archive_payload(
            built_source,
            f"On_Boundaries_of_Evidence_Source_{plan.archive_label}",
            SOURCE_ARCHIVE_MEMBERS,
            manifest,
            plan.build_epoch,
        )
        repeated_manifest_errors = verify_manifest(root, manifest)
        if repeated_manifest_errors:
            raise ArchiveError("; ".join(repeated_manifest_errors))

        try:
            final_plan = resolve_build_plan(root, spec, mode, requested_version)
        except IdentityError as exc:
            raise ArchiveError(str(exc)) from exc
        if final_plan != plan:
            raise ArchiveError("Git or release identity changed during archive construction")

        document = build_identity_document(
            plan,
            manifest,
            (
                ("complete-release", built_complete),
                ("manuscript-source", built_source),
            ),
        )
        write_identity_file(identity, document)
        created_outputs.append(identity)
        verify_identity_file(root, spec, manifest, identity)
        try:
            closing_plan = resolve_build_plan(root, spec, mode, requested_version)
        except IdentityError as exc:
            raise ArchiveError(str(exc)) from exc
        if closing_plan != plan:
            raise ArchiveError("Git or release identity changed before build completion")
    except ArchiveValidationError as exc:
        for path in created_outputs:
            path.unlink(missing_ok=True)
        raise ArchiveError(str(exc)) from exc
    except Exception:
        for path in created_outputs:
            path.unlink(missing_ok=True)
        raise
    return complete, source, identity


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
        help="manifest path; must resolve to ROOT/MANIFEST.sha256",
    )
    parser.add_argument(
        "--spec",
        type=Path,
        default=None,
        help="release specification; must resolve to ROOT/release/release-spec.json",
    )
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=None,
        help="archive directory (default: ROOT/dist)",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--development",
        action="store_true",
        help="build commit-named development artifacts",
    )
    mode.add_argument(
        "--candidate-version",
        metavar="VERSION",
        help="build commit-named candidate artifacts for strict SemVer VERSION",
    )
    mode.add_argument(
        "--release-version",
        metavar="VERSION",
        help="build final artifacts only from the matching annotated tag",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    manifest = (
        args.manifest
        if args.manifest is not None
        else root / MANIFEST_NAME
    )
    spec = args.spec if args.spec is not None else root / "release/release-spec.json"
    output_directory = (
        args.output_directory.resolve()
        if args.output_directory is not None
        else root / "dist"
    )
    if args.development:
        mode = "development"
        version = None
    elif args.candidate_version is not None:
        mode = "candidate"
        version = args.candidate_version
    else:
        mode = "release"
        version = args.release_version
    try:
        complete, source, identity = create_release_artifacts(
            root,
            manifest,
            output_directory,
            spec,
            mode,
            version,
        )
    except (ArchiveError, IdentityError, ManifestError, OSError) as exc:
        print(f"ARCHIVE: FAIL: {exc}", file=sys.stderr)
        return 1

    for path in (complete, source):
        print(f"ARCHIVE: {path.name}: {sha256_file(path)}")
    print(f"ARCHIVE IDENTITY: {identity.name}: {sha256_file(identity)}")
    print("ARCHIVE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
