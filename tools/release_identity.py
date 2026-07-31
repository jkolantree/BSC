#!/usr/bin/env python3
"""Resolve release authority and verify detached archive identity records."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

try:
    from tools.archive_validation import (
        SOURCE_ARCHIVE_MEMBERS,
        ArchiveValidationError,
        verify_archive_payload,
    )
    from tools.verify_manifest import (
        MANIFEST_NAME,
        is_excluded_release_file,
        parse_manifest,
        verify_manifest,
    )
except ModuleNotFoundError:
    from archive_validation import (  # type: ignore[no-redef]
        SOURCE_ARCHIVE_MEMBERS,
        ArchiveValidationError,
        verify_archive_payload,
    )
    from verify_manifest import (  # type: ignore[no-redef]
        MANIFEST_NAME,
        is_excluded_release_file,
        parse_manifest,
        verify_manifest,
    )


SPEC_RELATIVE_PATH = Path("release/release-spec.json")
SPEC_SCHEMA = "bsc.release-spec.v1"
IDENTITY_SCHEMA = "bsc.release-identity.v1"
GIT_OBJECT_PATTERN = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)"
    r"(?:-((?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*))*))?$"
)


class IdentityError(ValueError):
    """Raised when release identity cannot be established or reproduced."""


@dataclass(frozen=True)
class ReleaseSpec:
    intended_version: str | None
    build_epoch: int | None


@dataclass(frozen=True)
class GitIdentity:
    commit: str
    tree: str
    commit_epoch: int

    @property
    def short_commit(self) -> str:
        return self.commit[:12]


@dataclass(frozen=True)
class BuildPlan:
    mode: str
    version: str | None
    build_epoch: int
    outer_label: str
    archive_label: str
    git: GitIdentity
    tag_name: str | None
    tag_object: str | None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left.resolve())) == os.path.normcase(
        str(right.resolve())
    )


def canonical_spec_path(root: Path, supplied: Path | None = None) -> Path:
    root = root.resolve()
    expected = root / SPEC_RELATIVE_PATH
    actual = expected if supplied is None else supplied
    if not _same_path(actual, expected):
        raise IdentityError(
            f"release specification must be {SPEC_RELATIVE_PATH.as_posix()}"
        )
    try:
        mode = expected.lstat().st_mode
    except OSError as exc:
        raise IdentityError(f"cannot inspect release specification: {exc}") from exc
    if not stat.S_ISREG(mode):
        raise IdentityError("release specification must be a regular file")
    return expected


def canonical_manifest_path(root: Path, supplied: Path | None = None) -> Path:
    root = root.resolve()
    expected = root / MANIFEST_NAME
    actual = expected if supplied is None else supplied
    if not _same_path(actual, expected):
        raise IdentityError(f"manifest must be the canonical root {MANIFEST_NAME}")
    try:
        mode = expected.lstat().st_mode
    except OSError as exc:
        raise IdentityError(f"cannot inspect canonical manifest: {exc}") from exc
    if not stat.S_ISREG(mode):
        raise IdentityError("canonical manifest must be a regular file")
    return expected


def load_release_spec(path: Path) -> ReleaseSpec:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise IdentityError(f"cannot read release specification: {exc}") from exc
    if not isinstance(value, dict):
        raise IdentityError("release specification must be a JSON object")
    expected_keys = {"schema", "intended_version", "build_epoch"}
    if set(value) != expected_keys:
        raise IdentityError(
            "release specification keys must be exactly: "
            + ", ".join(sorted(expected_keys))
        )
    if value["schema"] != SPEC_SCHEMA:
        raise IdentityError(f"release specification schema must be {SPEC_SCHEMA}")

    version = value["intended_version"]
    epoch = value["build_epoch"]
    if version is not None and (
        not isinstance(version, str) or SEMVER_PATTERN.fullmatch(version) is None
    ):
        raise IdentityError("intended_version must be null or strict SemVer")
    if epoch is not None and (
        not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0
    ):
        raise IdentityError("build_epoch must be null or a non-negative integer")
    if (version is None) != (epoch is None):
        raise IdentityError(
            "intended_version and build_epoch must either both be null or both be set"
        )
    return ReleaseSpec(intended_version=version, build_epoch=epoch)


def _run_git(
    root: Path, args: Sequence[str], *, allow_failure: bool = False
) -> subprocess.CompletedProcess[str]:
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
    try:
        result = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(root), *args],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            env=environment,
        )
    except (OSError, UnicodeError) as exc:
        raise IdentityError(f"cannot execute Git: {exc}") from exc
    if result.returncode != 0 and not allow_failure:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
        raise IdentityError(f"Git {' '.join(args)} failed: {detail}")
    return result


def _run_git_bytes(root: Path, args: Sequence[str]) -> bytes:
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
    try:
        result = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(root), *args],
            check=False,
            capture_output=True,
            env=environment,
        )
    except OSError as exc:
        raise IdentityError(f"cannot execute Git: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise IdentityError(f"Git {' '.join(args)} failed: {detail or 'unknown error'}")
    return result.stdout


def _git_text(root: Path, *args: str) -> str:
    return _run_git(root, args).stdout.strip()


def _require_object_id(value: str, label: str) -> str:
    if GIT_OBJECT_PATTERN.fullmatch(value) is None:
        raise IdentityError(f"Git returned an invalid {label} object ID: {value!r}")
    return value


def require_tracked_file(root: Path, relative: Path) -> None:
    result = _run_git(
        root,
        ("ls-files", "--error-unmatch", "--", relative.as_posix()),
        allow_failure=True,
    )
    if result.returncode != 0:
        raise IdentityError(f"required release file is not tracked: {relative.as_posix()}")


def verify_head_payload(root: Path, manifest_path: Path) -> None:
    errors = verify_manifest(root, manifest_path)
    if errors:
        raise IdentityError("; ".join(errors))
    manifest_entries = set(parse_manifest(manifest_path))
    required = manifest_entries | {MANIFEST_NAME}
    tree_output = _run_git_bytes(
        root, ("ls-tree", "-r", "-z", "--full-tree", "HEAD")
    )
    tracked: dict[str, tuple[str, str, str]] = {}
    try:
        for raw_entry in tree_output.split(b"\0"):
            if not raw_entry:
                continue
            header, path_bytes = raw_entry.split(b"\t", 1)
            mode, object_type, object_id = header.decode("ascii").split(" ")
            path = path_bytes.decode("utf-8")
            tracked[path] = (mode, object_type, object_id)
    except (UnicodeError, ValueError) as exc:
        raise IdentityError("Git tree inventory is not valid normalized UTF-8") from exc

    eligible = {
        path: entry
        for path, entry in tracked.items()
        if not is_excluded_release_file(path)
    }
    for relative, (mode, object_type, _) in sorted(eligible.items()):
        if mode not in {"100644", "100755"} or object_type != "blob":
            raise IdentityError(f"release payload is not a regular HEAD blob: {relative}")
    head_paths = set(eligible)
    missing_from_head = sorted(manifest_entries - head_paths)
    missing_from_manifest = sorted(head_paths - manifest_entries)
    if missing_from_head:
        raise IdentityError(
            "manifest payload is absent from HEAD: " + ", ".join(missing_from_head)
        )
    if missing_from_manifest:
        raise IdentityError(
            "HEAD payload is missing from manifest: "
            + ", ".join(missing_from_manifest)
        )

    for relative in sorted(required):
        entry = tracked.get(relative)
        if entry is None:
            raise IdentityError(f"release payload is absent from HEAD: {relative}")
        mode, object_type, object_id = entry
        if mode not in {"100644", "100755"} or object_type != "blob":
            raise IdentityError(f"release payload is not a regular HEAD blob: {relative}")
        blob = _run_git_bytes(root, ("cat-file", "blob", object_id))
        try:
            worktree_bytes = (root / relative).read_bytes()
        except OSError as exc:
            raise IdentityError(f"cannot read release payload {relative}: {exc}") from exc
        if worktree_bytes != blob:
            raise IdentityError(f"release payload bytes differ from HEAD: {relative}")


def validate_release_surfaces(root: Path, version: str, build_epoch: int) -> None:
    release_url = f"https://github.com/jkolantree/BSC/releases/tag/v{version}"
    release_date = datetime.fromtimestamp(build_epoch, tz=UTC).date().isoformat()
    requirements = {
        "README.md": (f"Latest released version:** v{version}",),
        "CITATION.cff": (
            f'version: "{version}"',
            f"date-released: {release_date}",
            f'repository-artifact: "{release_url}"',
        ),
        ".zenodo.json": (
            f'"version": "{version}"',
            f'"publication_date": "{release_date}"',
            f'"identifier": "{release_url}"',
        ),
        "CHANGELOG.md": (f"## {version}",),
        "paper/source/On_Boundaries_of_Evidence.tex": (
            rf"\newcommand{{\BSCVersion}}{{{version}}}",
        ),
        "synopsis/Technical_Synopsis.md": (
            f"Repository state:** version {version} release",
        ),
        "synopsis/source/Technical_Synopsis.tex": (
            rf"\newcommand{{\BSCVersion}}{{{version}}}",
        ),
    }
    for relative, fragments in requirements.items():
        path = root / relative
        try:
            mode = path.lstat().st_mode
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise IdentityError(f"cannot inspect release metadata {relative}: {exc}") from exc
        if not stat.S_ISREG(mode):
            raise IdentityError(f"release metadata is not a regular file: {relative}")
        missing = [fragment for fragment in fragments if fragment not in text]
        if missing:
            raise IdentityError(
                f"release metadata does not match version {version}: {relative}"
            )


def resolve_git_identity(root: Path) -> GitIdentity:
    root = root.resolve()
    if not root.is_dir():
        raise IdentityError(f"repository root is not a directory: {root}")
    top_level = Path(_git_text(root, "rev-parse", "--show-toplevel"))
    if not _same_path(top_level, root):
        raise IdentityError("--root must be the exact Git worktree root")

    commit = _require_object_id(
        _git_text(root, "rev-parse", "--verify", "HEAD^{commit}"), "commit"
    )
    tree = _require_object_id(
        _git_text(root, "rev-parse", "--verify", "HEAD^{tree}"), "tree"
    )
    epoch_text = _git_text(root, "show", "-s", "--format=%ct", "HEAD")
    try:
        epoch = int(epoch_text)
    except ValueError as exc:
        raise IdentityError(f"Git returned an invalid commit epoch: {epoch_text!r}") from exc

    status = _git_text(root, "status", "--porcelain=v1", "--untracked-files=all")
    if status:
        raise IdentityError("release archive input must be a clean Git worktree")
    if _git_text(root, "ls-files", "--unmerged"):
        raise IdentityError("release archive input contains unresolved merges")
    staged = _git_text(root, "ls-files", "--stage")
    if any(line.startswith("160000 ") for line in staged.splitlines()):
        raise IdentityError("release archive input contains a Git submodule")

    return GitIdentity(commit=commit, tree=tree, commit_epoch=epoch)


def _tag_exists(root: Path, tag_name: str) -> bool:
    result = _run_git(
        root,
        ("show-ref", "--verify", "--quiet", f"refs/tags/{tag_name}"),
        allow_failure=True,
    )
    if result.returncode not in {0, 1}:
        detail = result.stderr.strip() or "unknown error"
        raise IdentityError(f"cannot inspect tag {tag_name}: {detail}")
    return result.returncode == 0


def resolve_annotated_tag(
    root: Path, tag_name: str, git: GitIdentity
) -> tuple[str, str]:
    ref = f"refs/tags/{tag_name}"
    tag_object = _require_object_id(_git_text(root, "rev-parse", ref), "tag")
    if _git_text(root, "cat-file", "-t", tag_object) != "tag":
        raise IdentityError(f"{tag_name} must be an annotated tag")

    headers: dict[str, str] = {}
    for line in _git_text(root, "cat-file", "-p", tag_object).splitlines():
        if not line:
            break
        key, separator, value = line.partition(" ")
        if separator:
            headers[key] = value
    if headers.get("type") != "commit":
        raise IdentityError(f"{tag_name} must directly tag a commit")
    if headers.get("tag") != tag_name:
        raise IdentityError(f"annotated tag object name does not match {tag_name}")
    direct_object = _require_object_id(headers.get("object", ""), "tag target")
    if direct_object != git.commit:
        raise IdentityError(f"{tag_name} does not directly tag HEAD")

    peeled_commit = _require_object_id(
        _git_text(root, "rev-parse", f"{ref}^{{commit}}"), "peeled commit"
    )
    peeled_tree = _require_object_id(
        _git_text(root, "rev-parse", f"{ref}^{{tree}}"), "peeled tree"
    )
    if peeled_commit != git.commit:
        raise IdentityError(f"{tag_name} peeled commit does not match HEAD")
    if peeled_tree != git.tree:
        raise IdentityError(f"{tag_name} tree does not match HEAD tree")
    return tag_object, direct_object


def resolve_build_plan(
    root: Path,
    spec_path: Path,
    mode: str,
    requested_version: str | None = None,
    *,
    candidate_requires_tag_absence: bool = True,
) -> BuildPlan:
    root = root.resolve()
    spec_path = canonical_spec_path(root, spec_path)
    require_tracked_file(root, SPEC_RELATIVE_PATH)
    spec = load_release_spec(spec_path)
    git = resolve_git_identity(root)

    if mode == "development":
        if requested_version is not None:
            raise IdentityError("development mode does not accept a release version")
        label = f"dev-g{git.short_commit}"
        return BuildPlan(
            mode=mode,
            version=None,
            build_epoch=git.commit_epoch,
            outer_label=label,
            archive_label=label,
            git=git,
            tag_name=None,
            tag_object=None,
        )

    if mode not in {"candidate", "release"}:
        raise IdentityError(f"unknown archive mode: {mode!r}")
    if requested_version is None or SEMVER_PATTERN.fullmatch(requested_version) is None:
        raise IdentityError(f"{mode} mode requires an explicit strict SemVer version")
    if spec.intended_version != requested_version:
        raise IdentityError(
            f"requested version {requested_version} does not match the tracked release specification"
        )
    if spec.build_epoch is None:
        raise IdentityError("candidate and release modes require a tracked build_epoch")
    validate_release_surfaces(root, requested_version, spec.build_epoch)

    tag_name = f"v{requested_version}"
    if mode == "candidate":
        if candidate_requires_tag_absence and _tag_exists(root, tag_name):
            raise IdentityError(f"candidate tag already exists: {tag_name}")
        return BuildPlan(
            mode=mode,
            version=requested_version,
            build_epoch=spec.build_epoch,
            outer_label=f"v{requested_version}-candidate-g{git.short_commit}",
            archive_label=f"v{requested_version}",
            git=git,
            tag_name=None,
            tag_object=None,
        )

    tag_object, _ = resolve_annotated_tag(root, tag_name, git)
    return BuildPlan(
        mode=mode,
        version=requested_version,
        build_epoch=spec.build_epoch,
        outer_label=f"v{requested_version}",
        archive_label=f"v{requested_version}",
        git=git,
        tag_name=tag_name,
        tag_object=tag_object,
    )


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def expected_artifact_names(plan: BuildPlan) -> dict[str, str]:
    prefix = f"On_Boundaries_of_Evidence_{plan.outer_label}"
    return {
        "complete-release": f"{prefix}_Complete_Release.zip",
        "manuscript-source": f"{prefix}_Source.zip",
    }


def expected_identity_name(plan: BuildPlan) -> str:
    return f"On_Boundaries_of_Evidence_{plan.outer_label}_Identity.json"


def build_identity_document(
    plan: BuildPlan,
    manifest_path: Path,
    artifacts: Sequence[tuple[str, Path]],
) -> dict[str, Any]:
    manifest_entries = parse_manifest(manifest_path)
    artifact_records = []
    for role, path in artifacts:
        if path.name in {"", ".", ".."}:
            raise IdentityError(f"invalid artifact filename: {path.name!r}")
        artifact_records.append(
            {
                "name": path.name,
                "role": role,
                "sha256": sha256_file(path),
                "size": path.stat().st_size,
            }
        )
    artifact_records.sort(key=lambda item: (item["role"], item["name"]))
    return {
        "schema": IDENTITY_SCHEMA,
        "mode": plan.mode,
        "version": plan.version,
        "build_epoch": plan.build_epoch,
        "git": {
            "commit": plan.git.commit,
            "tree": plan.git.tree,
            "tag": (
                None
                if plan.tag_name is None
                else {"name": plan.tag_name, "object": plan.tag_object}
            ),
        },
        "manifest": {
            "name": MANIFEST_NAME,
            "sha256": sha256_file(manifest_path),
            "entries": len(manifest_entries),
        },
        "artifacts": artifact_records,
    }


def write_identity_file(path: Path, document: dict[str, Any]) -> None:
    payload = canonical_json_bytes(document)
    created = False
    try:
        with path.open("xb") as stream:
            created = True
            stream.write(payload)
    except Exception:
        if created:
            path.unlink(missing_ok=True)
        raise


def verify_identity_file(
    root: Path,
    spec_path: Path,
    manifest_path: Path,
    identity_path: Path,
) -> None:
    root = root.resolve()
    spec_path = canonical_spec_path(root, spec_path)
    manifest_path = canonical_manifest_path(root, manifest_path)
    require_tracked_file(root, Path(MANIFEST_NAME))
    verify_head_payload(root, manifest_path)
    try:
        identity_mode = identity_path.lstat().st_mode
        raw = identity_path.read_bytes()
        document = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise IdentityError(f"cannot read detached identity: {exc}") from exc
    if not stat.S_ISREG(identity_mode):
        raise IdentityError("detached identity must be a regular file")
    if not isinstance(document, dict):
        raise IdentityError("detached identity must be a JSON object")
    if raw != canonical_json_bytes(document):
        raise IdentityError("detached identity is not deterministically serialized")

    mode = document.get("mode")
    version = document.get("version")
    if mode not in {"development", "candidate", "release"}:
        raise IdentityError("detached identity has an invalid mode")
    if version is not None and not isinstance(version, str):
        raise IdentityError("detached identity has an invalid version")
    plan = resolve_build_plan(
        root,
        spec_path,
        mode,
        version,
        candidate_requires_tag_absence=False,
    )
    if identity_path.name != expected_identity_name(plan):
        raise IdentityError("detached identity filename does not match its authority")

    artifact_values = document.get("artifacts")
    if not isinstance(artifact_values, list) or len(artifact_values) != 2:
        raise IdentityError("detached identity must name exactly two artifacts")
    artifacts: list[tuple[str, Path]] = []
    for value in artifact_values:
        if not isinstance(value, dict):
            raise IdentityError("detached identity artifact record is invalid")
        role = value.get("role")
        name = value.get("name")
        if role not in {"complete-release", "manuscript-source"}:
            raise IdentityError("detached identity artifact role is invalid")
        if (
            not isinstance(name, str)
            or Path(name).name != name
            or name in {"", ".", ".."}
        ):
            raise IdentityError("detached identity artifact name is unsafe")
        artifact_path = identity_path.parent / name
        try:
            artifact_mode = artifact_path.lstat().st_mode
        except OSError as exc:
            raise IdentityError(f"cannot inspect detached artifact {name}: {exc}") from exc
        if not stat.S_ISREG(artifact_mode):
            raise IdentityError(f"detached artifact must be a regular file: {name}")
        artifacts.append((role, artifact_path))
    if {role for role, _ in artifacts} != {"complete-release", "manuscript-source"}:
        raise IdentityError("detached identity artifact roles must be unique")
    expected_names = expected_artifact_names(plan)
    if {role: path.name for role, path in artifacts} != expected_names:
        raise IdentityError("detached identity artifact names do not match its authority")

    by_role = {role: path for role, path in artifacts}
    manifest_entries = parse_manifest(manifest_path)
    try:
        verify_archive_payload(
            by_role["complete-release"],
            f"On_Boundaries_of_Evidence_{plan.archive_label}",
            sorted([*manifest_entries, MANIFEST_NAME]),
            manifest_path,
            plan.build_epoch,
        )
        verify_archive_payload(
            by_role["manuscript-source"],
            f"On_Boundaries_of_Evidence_Source_{plan.archive_label}",
            SOURCE_ARCHIVE_MEMBERS,
            manifest_path,
            plan.build_epoch,
        )
    except ArchiveValidationError as exc:
        raise IdentityError(str(exc)) from exc

    expected = build_identity_document(plan, manifest_path, artifacts)
    if document != expected:
        raise IdentityError("detached identity does not match current inputs")


def build_parser() -> argparse.ArgumentParser:
    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Verify a detached release identity JSON.")
    parser.add_argument("--root", type=Path, default=repository_root)
    parser.add_argument("--spec", type=Path, default=None)
    parser.add_argument("--manifest", type=Path, default=None)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--identity", type=Path)
    action.add_argument(
        "--print-build-epoch",
        action="store_true",
        help="print tracked release epoch, or the clean HEAD epoch when unset",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    try:
        spec = canonical_spec_path(root, args.spec)
        if args.print_build_epoch:
            require_tracked_file(root, SPEC_RELATIVE_PATH)
            release_spec = load_release_spec(spec)
            if release_spec.build_epoch is not None:
                epoch = release_spec.build_epoch
            else:
                epoch_text = _git_text(root, "show", "-s", "--format=%ct", "HEAD")
                try:
                    epoch = int(epoch_text)
                except ValueError as exc:
                    raise IdentityError(
                        f"Git returned an invalid commit epoch: {epoch_text!r}"
                    ) from exc
            print(epoch)
            return 0
        manifest = canonical_manifest_path(root, args.manifest)
        if args.identity is None:
            raise IdentityError("detached identity path is required")
        verify_identity_file(root, spec, manifest, args.identity.resolve())
    except (IdentityError, OSError, ValueError) as exc:
        print(f"RELEASE IDENTITY: FAIL: {exc}", file=sys.stderr)
        return 1
    print("RELEASE IDENTITY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
