#!/usr/bin/env python3
"""Validate deterministic BSC release ZIPs against the canonical manifest."""

from __future__ import annotations

import hashlib
import io
import stat
import zipfile
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence

try:
    from tools.verify_manifest import MANIFEST_NAME, parse_manifest
except ModuleNotFoundError:
    from verify_manifest import MANIFEST_NAME, parse_manifest  # type: ignore[no-redef]


SOURCE_ARCHIVE_MEMBERS = (
    "CITATION.cff",
    "LICENSES/paper-and-documentation.txt",
    "REPRODUCING.md",
    "SOURCE_AVAILABILITY.md",
    "paper/source/On_Boundaries_of_Evidence.bib",
    "paper/source/On_Boundaries_of_Evidence.tex",
)


class ArchiveValidationError(ValueError):
    """Raised when a release ZIP is not the declared deterministic payload."""


def _directory_entries(root_prefix: str, members: Iterable[str]) -> set[str]:
    directories = {f"{root_prefix}/"}
    for member in members:
        parts = PurePosixPath(member).parts[:-1]
        for length in range(1, len(parts) + 1):
            directories.add(f"{root_prefix}/{'/'.join(parts[:length])}/")
    return directories


def _zip_timestamp(epoch: int) -> tuple[int, ...]:
    try:
        instant = datetime.fromtimestamp(epoch, tz=UTC)
    except (OverflowError, OSError, ValueError) as exc:
        raise ArchiveValidationError(f"invalid build epoch: {epoch}") from exc
    if not 1980 <= instant.year <= 2107:
        raise ArchiveValidationError("ZIP timestamp must fall between 1980 and 2107")
    return (
        instant.year,
        instant.month,
        instant.day,
        instant.hour,
        instant.minute,
        instant.second - (instant.second % 2),
    )


def _archive_info(
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


def _canonical_zip_bytes(
    names: Sequence[str], payloads: dict[str, bytes], timestamp: tuple[int, ...]
) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(
        stream,
        mode="w",
        compression=zipfile.ZIP_STORED,
        allowZip64=True,
        strict_timestamps=True,
    ) as archive:
        for name in names:
            is_directory = name.endswith("/")
            archive.writestr(
                _archive_info(name, is_directory=is_directory, timestamp=timestamp),
                b"" if is_directory else payloads[name],
            )
    return stream.getvalue()


def verify_archive_payload(
    archive_path: Path,
    root_prefix: str,
    members: Sequence[str],
    manifest_path: Path,
    build_epoch: int,
) -> None:
    try:
        archive_mode = archive_path.lstat().st_mode
    except OSError as exc:
        raise ArchiveValidationError(f"cannot inspect archive: {exc}") from exc
    if not stat.S_ISREG(archive_mode):
        raise ArchiveValidationError("release artifact must be a regular file")

    manifest_entries = parse_manifest(manifest_path)
    expected_names = _directory_entries(root_prefix, members) | {
        f"{root_prefix}/{member}" for member in members
    }
    expected_timestamp = _zip_timestamp(build_epoch)
    payloads: dict[str, bytes] = {}
    try:
        with zipfile.ZipFile(archive_path) as archive:
            if archive.comment:
                raise ArchiveValidationError("archive comment must be empty")
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                raise ArchiveValidationError(
                    f"archive contains duplicate members: {archive_path.name}"
                )
            if names != sorted(names) or set(names) != expected_names:
                raise ArchiveValidationError(
                    f"archive inventory mismatch: {archive_path.name}"
                )
            for info in infos:
                mode = info.external_attr >> 16
                if info.date_time != expected_timestamp:
                    raise ArchiveValidationError(
                        f"archive timestamp mismatch: {info.filename}"
                    )
                if (
                    info.create_system != 3
                    or info.compress_type != zipfile.ZIP_STORED
                    or info.comment
                    or info.extra
                    or info.flag_bits & 0x1
                ):
                    raise ArchiveValidationError(
                        f"archive metadata mismatch: {info.filename}"
                    )
                if info.is_dir():
                    if not stat.S_ISDIR(mode) or stat.S_IMODE(mode) != 0o755:
                        raise ArchiveValidationError(
                            f"archive directory mode mismatch: {info.filename}"
                        )
                elif not stat.S_ISREG(mode) or stat.S_IMODE(mode) != 0o644:
                    raise ArchiveValidationError(
                        f"archive file mode mismatch: {info.filename}"
                    )

            canonical_manifest_bytes = manifest_path.read_bytes()
            for member in members:
                name = f"{root_prefix}/{member}"
                payload = archive.read(name)
                payloads[name] = payload
                if member == MANIFEST_NAME:
                    matches = payload == canonical_manifest_bytes
                else:
                    expected = manifest_entries.get(member)
                    matches = (
                        expected is not None
                        and hashlib.sha256(payload).hexdigest() == expected.digest
                    )
                if not matches:
                    raise ArchiveValidationError(
                        f"archive payload mismatch for {name}: {archive_path.name}"
                    )
        canonical = _canonical_zip_bytes(sorted(expected_names), payloads, expected_timestamp)
        if archive_path.read_bytes() != canonical:
            raise ArchiveValidationError(
                f"archive bytes are not canonical: {archive_path.name}"
            )
    except (OSError, zipfile.BadZipFile, KeyError) as exc:
        raise ArchiveValidationError(
            f"cannot verify archive {archive_path.name}: {exc}"
        ) from exc
