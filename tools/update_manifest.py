#!/usr/bin/env python3
"""Regenerate MANIFEST.sha256 from the fail-closed release inventory."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    from tools.verify_manifest import (
        MANIFEST_NAME,
        ManifestError,
        inventory_release_files,
        sha256_file,
    )
except ModuleNotFoundError:
    from verify_manifest import (  # type: ignore[no-redef]
        MANIFEST_NAME,
        ManifestError,
        inventory_release_files,
        sha256_file,
    )


def render_manifest(root: Path) -> str:
    inventory = inventory_release_files(root)
    if not inventory:
        raise ManifestError("release inventory contains no files")
    return "".join(
        f"{sha256_file(inventory[path])}  ./{path}\n"
        for path in sorted(inventory)
    )


def update_manifest(root: Path, manifest_path: Path) -> int:
    root = root.resolve()
    manifest_path = manifest_path.resolve()
    content = render_manifest(root)
    temporary = manifest_path.with_name(f".{manifest_path.name}.tmp")
    if temporary.exists():
        raise ManifestError(
            f"refusing to overwrite stale temporary manifest: {temporary}"
        )
    try:
        temporary.write_text(content, encoding="utf-8", newline="\n")
        os.replace(temporary, manifest_path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return len(content.splitlines())


def build_parser() -> argparse.ArgumentParser:
    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Regenerate the complete release manifest deterministically."
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
        entries = update_manifest(root, manifest)
    except (ManifestError, OSError) as exc:
        print(f"MANIFEST UPDATE: FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"MANIFEST UPDATE: PASS: {entries} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
