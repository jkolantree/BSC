#!/usr/bin/env python3
"""Verify that a release manifest names exactly the release payload.

The manifest intentionally omits itself. Generated work directories are not
release payload and are excluded explicitly below; every other regular file
must appear exactly once, with a safe normalized path and a matching SHA-256.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


MANIFEST_NAME = "MANIFEST.sha256"
MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})  (\./[^\r\n]+)$")
EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "build",
    "dist",
}
EXCLUDED_FILE_SUFFIXES = {".pyc", ".pyo"}
FORBIDDEN_PAYLOAD_ROOTS = {"tmp"}


class ManifestError(ValueError):
    """Raised for an invalid or incomplete release manifest."""


@dataclass(frozen=True)
class ManifestEntry:
    digest: str
    path: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_manifest_path(raw_path: str) -> str:
    if "\x00" in raw_path or "\\" in raw_path:
        raise ManifestError(f"unsafe manifest path: {raw_path!r}")
    if not raw_path.startswith("./"):
        raise ManifestError(f"manifest path must start with './': {raw_path!r}")

    path = raw_path[2:]
    pure = PurePosixPath(path)
    if not path or pure.is_absolute():
        raise ManifestError(f"unsafe manifest path: {raw_path!r}")
    if any(part in {"", ".", ".."} for part in pure.parts):
        raise ManifestError(f"unsafe manifest path: {raw_path!r}")
    if str(pure) != path:
        raise ManifestError(f"manifest path is not normalized: {raw_path!r}")
    if pure.name == MANIFEST_NAME and len(pure.parts) == 1:
        raise ManifestError(f"{MANIFEST_NAME} must not hash itself")
    return path


def parse_manifest(manifest_path: Path) -> dict[str, ManifestEntry]:
    try:
        text = manifest_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ManifestError(f"cannot read manifest: {exc}") from exc

    if not text.endswith("\n"):
        raise ManifestError("manifest must end with a newline")

    entries: dict[str, ManifestEntry] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = MANIFEST_LINE.fullmatch(line)
        if match is None:
            raise ManifestError(
                f"malformed manifest line {line_number}: {line!r}"
            )
        digest, raw_path = match.groups()
        path = normalize_manifest_path(raw_path)
        if path in entries:
            raise ManifestError(
                f"duplicate manifest path on line {line_number}: {path}"
            )
        entries[path] = ManifestEntry(digest=digest, path=path)

    if not entries:
        raise ManifestError("manifest contains no entries")
    return entries


def inventory_release_files(root: Path) -> dict[str, Path]:
    root = root.resolve()
    if not root.is_dir():
        raise ManifestError(f"release root is not a directory: {root}")

    inventory: dict[str, Path] = {}
    for directory, directory_names, file_names in os.walk(
        root, topdown=True, followlinks=False
    ):
        current = Path(directory)

        retained_directories: list[str] = []
        for name in sorted(directory_names):
            candidate = current / name
            if name in EXCLUDED_DIRECTORY_NAMES:
                continue
            mode = candidate.lstat().st_mode
            if stat.S_ISLNK(mode):
                relative = candidate.relative_to(root).as_posix()
                raise ManifestError(
                    f"release payload contains a directory symlink: {relative}"
                )
            if not stat.S_ISDIR(mode):
                relative = candidate.relative_to(root).as_posix()
                raise ManifestError(
                    f"release payload contains a special directory entry: "
                    f"{relative}"
                )
            retained_directories.append(name)
        directory_names[:] = retained_directories

        for name in sorted(file_names):
            candidate = current / name
            relative = candidate.relative_to(root).as_posix()
            if relative == MANIFEST_NAME:
                continue
            if candidate.suffix in EXCLUDED_FILE_SUFFIXES:
                continue

            mode = candidate.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise ManifestError(
                    f"release payload contains a file symlink: {relative}"
                )
            if not stat.S_ISREG(mode):
                raise ManifestError(
                    f"release payload contains a special file: {relative}"
                )
            normalized = normalize_manifest_path(f"./{relative}")
            inventory[normalized] = candidate
    return inventory


def verify_manifest(root: Path, manifest_path: Path) -> list[str]:
    entries = parse_manifest(manifest_path)
    inventory = inventory_release_files(root)

    manifest_paths = set(entries)
    inventory_paths = set(inventory)
    missing = sorted(manifest_paths - inventory_paths)
    extras = sorted(inventory_paths - manifest_paths)
    forbidden = sorted(
        path
        for path in inventory
        if PurePosixPath(path).parts[0] in FORBIDDEN_PAYLOAD_ROOTS
    )
    errors: list[str] = []
    if forbidden:
        errors.append("forbidden payload paths: " + ", ".join(forbidden))
    if missing:
        errors.append("manifest entries missing from payload: " + ", ".join(missing))
    if extras:
        errors.append("payload files missing from manifest: " + ", ".join(extras))

    for path in sorted(manifest_paths & inventory_paths):
        actual = sha256_file(inventory[path])
        expected = entries[path].digest
        if actual != expected:
            errors.append(
                f"hash mismatch for {path}: expected {expected}, got {actual}"
            )
    return errors


def build_parser() -> argparse.ArgumentParser:
    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Verify completeness and SHA-256 integrity of a release tree."
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    manifest = (
        args.manifest.resolve()
        if args.manifest is not None
        else root / MANIFEST_NAME
    )
    try:
        errors = verify_manifest(root, manifest)
    except ManifestError as exc:
        print(f"MANIFEST: FAIL: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"MANIFEST: FAIL: {error}", file=sys.stderr)
        return 1

    entries = parse_manifest(manifest)
    print(f"MANIFEST: PASS: {len(entries)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
