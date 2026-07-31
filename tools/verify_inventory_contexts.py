#!/usr/bin/env python3
"""Compare release inventory across checkout, linked worktree, and Git archive."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

try:
    from tools.release_identity import IdentityError, resolve_git_identity
    from tools.verify_manifest import (
        MANIFEST_NAME,
        ManifestError,
        inventory_release_files,
        sha256_file,
        verify_manifest,
    )
except ModuleNotFoundError:
    from release_identity import (  # type: ignore[no-redef]
        IdentityError,
        resolve_git_identity,
    )
    from verify_manifest import (  # type: ignore[no-redef]
        MANIFEST_NAME,
        ManifestError,
        inventory_release_files,
        sha256_file,
        verify_manifest,
    )


class ContextError(ValueError):
    """Raised when release inventories differ between Git materializations."""


def _run_git(root: Path, *args: str) -> str:
    environment = os.environ.copy()
    for name in (
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_COMMON_DIR",
        "GIT_DIR",
        "GIT_INDEX_FILE",
        "GIT_NAMESPACE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_PREFIX",
        "GIT_QUARANTINE_PATH",
        "GIT_REPLACE_REF_BASE",
        "GIT_WORK_TREE",
    ):
        environment.pop(name, None)
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    result = subprocess.run(
        ["git", "--no-replace-objects", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        env=environment,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
        raise ContextError(f"Git {' '.join(args)} failed: {detail}")
    return result.stdout.strip()


def _extract_git_archive(archive_path: Path, destination: Path) -> None:
    with tarfile.open(archive_path, mode="r:") as archive:
        for member in archive.getmembers():
            name = member.name
            pure = PurePosixPath(name)
            if (
                not name
                or "\\" in name
                or pure.is_absolute()
                or any(part in {"", ".", ".."} for part in pure.parts)
                or str(pure) != name
            ):
                raise ContextError(f"unsafe Git archive member: {name!r}")
            target = destination.joinpath(*pure.parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            if not member.isfile():
                raise ContextError(f"unsupported Git archive member type: {name}")
            target.parent.mkdir(parents=True, exist_ok=True)
            source = archive.extractfile(member)
            if source is None:
                raise ContextError(f"cannot read Git archive member: {name}")
            with source, target.open("xb") as stream:
                while block := source.read(1024 * 1024):
                    stream.write(block)


def inventory_digests(root: Path) -> dict[str, str]:
    manifest = root / MANIFEST_NAME
    try:
        errors = verify_manifest(root, manifest)
    except ManifestError as exc:
        raise ContextError(f"{root.name} manifest is invalid: {exc}") from exc
    if errors:
        raise ContextError(f"{root.name} manifest failed: {'; '.join(errors)}")
    inventory = inventory_release_files(root)
    return {path: sha256_file(file_path) for path, file_path in inventory.items()}


def verify_inventory_contexts(root: Path) -> tuple[str, int]:
    root = root.resolve()
    try:
        git = resolve_git_identity(root)
    except IdentityError as exc:
        raise ContextError(str(exc)) from exc
    source_inventory = inventory_digests(root)
    with tempfile.TemporaryDirectory(prefix="bsc-inventory-contexts-") as temporary:
        temporary_root = Path(temporary)
        normal = temporary_root / "normal"
        linked = temporary_root / "linked"
        extracted = temporary_root / "archive"
        extracted.mkdir()
        archive_path = temporary_root / "tree.tar"
        linked_added = False
        try:
            _run_git(
                root,
                "clone",
                "--no-local",
                "--no-checkout",
                "--no-tags",
                str(root),
                str(normal),
            )
            _run_git(normal, "config", "core.autocrlf", "false")
            _run_git(normal, "checkout", "--detach", git.commit)
            if not (normal / ".git").is_dir():
                raise ContextError("temporary normal checkout lacks a root .git directory")
            normal_git = resolve_git_identity(normal)
            if normal_git.commit != git.commit or normal_git.tree != git.tree:
                raise ContextError("temporary checkout Git identity differs from source")

            _run_git(normal, "worktree", "add", "--detach", str(linked), git.commit)
            linked_added = True
            if not (linked / ".git").is_file():
                raise ContextError("linked worktree does not have a root .git file")
            _run_git(
                normal,
                "archive",
                "--format=tar",
                f"--output={archive_path}",
                git.commit,
            )
            _extract_git_archive(archive_path, extracted)
            if (extracted / ".git").exists():
                raise ContextError("Git archive unexpectedly contains root .git metadata")

            normal_inventory = inventory_digests(normal)
            linked_inventory = inventory_digests(linked)
            archive_inventory = inventory_digests(extracted)
            if normal_inventory != source_inventory:
                raise ContextError("temporary checkout release inventory differs from source")
            if linked_inventory != source_inventory:
                raise ContextError("linked worktree release inventory differs from checkout")
            if archive_inventory != source_inventory:
                raise ContextError("Git archive release inventory differs from checkout")
        finally:
            if linked_added:
                _run_git(normal, "worktree", "remove", "--force", str(linked))
    return git.commit, len(source_inventory)


def build_parser() -> argparse.ArgumentParser:
    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Verify identical release inventory in three Git contexts."
    )
    parser.add_argument("--root", type=Path, default=repository_root)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        commit, count = verify_inventory_contexts(args.root)
    except (ContextError, OSError, UnicodeError, tarfile.TarError) as exc:
        print(f"INVENTORY CONTEXTS: FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"INVENTORY CONTEXTS: PASS: {count} files at {commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
