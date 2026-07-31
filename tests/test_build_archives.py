from __future__ import annotations

import stat
import json
import os
import subprocess
import tempfile
import unittest
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from unittest import mock

from tools.build_archives import (
    ArchiveError,
    SOURCE_ARCHIVE_MEMBERS,
    create_release_artifacts,
    sha256_file,
    write_deterministic_zip,
)
from tools.release_identity import IdentityError, verify_identity_file
from tools.update_manifest import update_manifest


class DeterministicArchiveTests(unittest.TestCase):
    def make_tree(self, root: Path) -> None:
        (root / "nested").mkdir()
        (root / "nested" / "b.txt").write_bytes(b"bravo\n")
        (root / "a.txt").write_bytes(b"alpha\n")

    def test_repeated_builds_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-archive-test-"
        ) as temporary:
            workspace = Path(temporary)
            root = workspace / "payload"
            root.mkdir()
            self.make_tree(root)
            first = workspace / "first.zip"
            second = workspace / "second.zip"
            members = ["nested/b.txt", "a.txt"]
            for output in (first, second):
                write_deterministic_zip(
                    output,
                    root,
                    "release-v1.0.1",
                    members,
                    1784851200,
                )
            self.assertEqual(sha256_file(first), sha256_file(second))

    def test_order_timestamp_mode_and_storage_are_normalized(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-archive-test-"
        ) as temporary:
            workspace = Path(temporary)
            root = workspace / "payload"
            root.mkdir()
            self.make_tree(root)
            output = workspace / "release.zip"
            write_deterministic_zip(
                output,
                root,
                "release-v1.0.1",
                ["nested/b.txt", "a.txt"],
                1784851200,
            )

            with zipfile.ZipFile(output) as archive:
                infos = archive.infolist()
                names = [info.filename for info in infos]
                self.assertEqual(names, sorted(names))
                self.assertTrue(
                    all(info.date_time == (2026, 7, 24, 0, 0, 0) for info in infos)
                )
                self.assertTrue(
                    all(info.compress_type == zipfile.ZIP_STORED for info in infos)
                )
                for info in infos:
                    mode = info.external_attr >> 16
                    if info.is_dir():
                        self.assertTrue(stat.S_ISDIR(mode))
                        self.assertEqual(stat.S_IMODE(mode), 0o755)
                    else:
                        self.assertTrue(stat.S_ISREG(mode))
                        self.assertEqual(stat.S_IMODE(mode), 0o644)

    def test_existing_output_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-archive-test-"
        ) as temporary:
            workspace = Path(temporary)
            root = workspace / "payload"
            root.mkdir()
            (root / "a.txt").write_bytes(b"alpha\n")
            output = workspace / "release.zip"
            output.write_bytes(b"keep me")
            with self.assertRaisesRegex(ArchiveError, "refusing to overwrite"):
                write_deterministic_zip(
                    output,
                    root,
                    "release-v1.0.1",
                    ["a.txt"],
                    1784851200,
                )
            self.assertEqual(output.read_bytes(), b"keep me")

    def test_unsafe_member_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-archive-test-"
        ) as temporary:
            workspace = Path(temporary)
            root = workspace / "payload"
            root.mkdir()
            output = workspace / "release.zip"
            with self.assertRaisesRegex(ArchiveError, "unsafe archive member"):
                write_deterministic_zip(
                    output,
                    root,
                    "release-v1.0.1",
                    ["../escape"],
                    1784851200,
                )
            self.assertFalse(output.exists())


class ReleaseArchiveOrchestrationTests(unittest.TestCase):
    def git(self, root: Path, *args: str) -> str:
        environment = os.environ.copy()
        environment["GIT_CONFIG_NOSYSTEM"] = "1"
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=environment,
        )
        return result.stdout.strip()

    def make_repository(
        self,
        workspace: Path,
        version: str | None = None,
        epoch: int | None = None,
    ) -> Path:
        root = workspace / "repository"
        root.mkdir()
        self.git(root, "init", "--initial-branch=main")
        self.git(root, "config", "core.autocrlf", "false")
        self.git(root, "config", "user.name", "BSC Test")
        self.git(root, "config", "user.email", "bsc-test@example.invalid")
        for relative in SOURCE_ARCHIVE_MEMBERS:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"fixture for {relative}\n", encoding="utf-8")
        spec = root / "release" / "release-spec.json"
        spec.parent.mkdir(parents=True, exist_ok=True)
        spec.write_text(
            json.dumps(
                {
                    "schema": "bsc.release-spec.v1",
                    "intended_version": version,
                    "build_epoch": epoch,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        self.write_release_surfaces(root, version, epoch)
        update_manifest(root, root / "MANIFEST.sha256")
        self.git(root, "add", "--all")
        self.git(root, "commit", "-m", "release fixture")
        return root

    def write_release_surfaces(
        self, root: Path, version: str | None, epoch: int | None
    ) -> None:
        if version is None or epoch is None:
            (root / "README.md").write_text("release\n", encoding="utf-8")
            return
        date = datetime.fromtimestamp(epoch, tz=UTC).date().isoformat()
        url = f"https://github.com/jkolantree/BSC/releases/tag/v{version}"
        (root / "README.md").write_text(
            f"**Latest released version:** v{version}\n", encoding="utf-8"
        )
        (root / "CITATION.cff").write_text(
            f'version: "{version}"\n'
            f"date-released: {date}\n"
            f'repository-artifact: "{url}"\n',
            encoding="utf-8",
        )
        (root / ".zenodo.json").write_text(
            json.dumps(
                {
                    "version": version,
                    "publication_date": date,
                    "identifier": url,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (root / "CHANGELOG.md").write_text(f"## {version}\n", encoding="utf-8")
        (root / "paper/source/On_Boundaries_of_Evidence.tex").write_text(
            rf"\newcommand{{\BSCVersion}}{{{version}}}" + "\n", encoding="utf-8"
        )
        synopsis_markdown = root / "synopsis/Technical_Synopsis.md"
        synopsis_markdown.parent.mkdir(parents=True, exist_ok=True)
        synopsis_markdown.write_text(
            f"**Repository state:** version {version} release\n", encoding="utf-8"
        )
        synopsis_tex = root / "synopsis/source/Technical_Synopsis.tex"
        synopsis_tex.parent.mkdir(parents=True, exist_ok=True)
        synopsis_tex.write_text(
            rf"\newcommand{{\BSCVersion}}{{{version}}}" + "\n", encoding="utf-8"
        )

    def test_development_artifacts_and_identity_are_commit_named(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-archive-test-") as temporary:
            workspace = Path(temporary)
            root = self.make_repository(workspace)
            commit = self.git(root, "rev-parse", "HEAD")
            outputs = create_release_artifacts(
                root,
                root / "MANIFEST.sha256",
                workspace / "output",
                root / "release" / "release-spec.json",
                "development",
            )
            self.assertTrue(all(commit[:12] in path.name for path in outputs))
            with zipfile.ZipFile(outputs[0]) as archive:
                self.assertFalse(any(name.endswith("Identity.json") for name in archive.namelist()))
                self.assertFalse(any("/.git" in name for name in archive.namelist()))
            verify_identity_file(
                root,
                root / "release" / "release-spec.json",
                root / "MANIFEST.sha256",
                outputs[2],
            )

    def test_external_manifest_and_payload_output_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-archive-test-") as temporary:
            workspace = Path(temporary)
            root = self.make_repository(workspace)
            external = workspace / "MANIFEST.sha256"
            external.write_bytes((root / "MANIFEST.sha256").read_bytes())
            with self.assertRaisesRegex(ArchiveError, "canonical root"):
                create_release_artifacts(
                    root,
                    external,
                    workspace / "output",
                    root / "release" / "release-spec.json",
                    "development",
                )
            with self.assertRaisesRegex(ArchiveError, "under build/ or dist/"):
                create_release_artifacts(
                    root,
                    root / "MANIFEST.sha256",
                    root / "artifacts",
                    root / "release" / "release-spec.json",
                    "development",
                )

    def test_candidate_and_release_bytes_match_but_authority_names_differ(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-archive-test-") as temporary:
            workspace = Path(temporary)
            root = self.make_repository(workspace, "1.5.0", 1785542400)
            commit = self.git(root, "rev-parse", "HEAD")
            candidate = create_release_artifacts(
                root,
                root / "MANIFEST.sha256",
                workspace / "candidate",
                root / "release" / "release-spec.json",
                "candidate",
                "1.5.0",
            )
            self.assertTrue(all(commit[:12] in path.name for path in candidate))
            self.git(root, "tag", "-a", "v1.5.0", "-m", "release")
            release = create_release_artifacts(
                root,
                root / "MANIFEST.sha256",
                workspace / "release-output",
                root / "release" / "release-spec.json",
                "release",
                "1.5.0",
            )
            self.assertTrue(all("v1.5.0" in path.name for path in release))
            self.assertTrue(all(commit[:12] not in path.name for path in release))
            self.assertEqual(sha256_file(candidate[0]), sha256_file(release[0]))
            self.assertEqual(sha256_file(candidate[1]), sha256_file(release[1]))
            self.assertNotEqual(candidate[2].read_bytes(), release[2].read_bytes())

    def test_wrong_tree_cannot_create_a_published_version_filename(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-archive-test-") as temporary:
            workspace = Path(temporary)
            root = self.make_repository(workspace, "1.4.0", 1785456000)
            with self.assertRaises(ArchiveError):
                create_release_artifacts(
                    root,
                    root / "MANIFEST.sha256",
                    workspace / "output",
                    root / "release" / "release-spec.json",
                    "release",
                    "1.4.0",
                )
            self.assertEqual(list((workspace / "output").glob("*")), [])

    def test_identity_failure_removes_only_new_outputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-archive-test-") as temporary:
            workspace = Path(temporary)
            root = self.make_repository(workspace)
            output = workspace / "output"
            output.mkdir()
            preserved = output / "preserved.txt"
            preserved.write_text("keep\n", encoding="utf-8")
            with mock.patch(
                "tools.build_archives.write_identity_file",
                side_effect=IdentityError("simulated identity failure"),
            ):
                with self.assertRaisesRegex(IdentityError, "simulated"):
                    create_release_artifacts(
                        root,
                        root / "MANIFEST.sha256",
                        output,
                        root / "release" / "release-spec.json",
                        "development",
                    )
            self.assertEqual(preserved.read_text(encoding="utf-8"), "keep\n")
            self.assertEqual(list(output.glob("*.zip")), [])
            self.assertEqual(list(output.glob("*Identity.json")), [])

    def test_ignored_untracked_manifest_payload_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-archive-test-") as temporary:
            workspace = Path(temporary)
            root = self.make_repository(workspace)
            (root / ".gitignore").write_text("ambient.dat\n", encoding="utf-8")
            (root / "ambient.dat").write_bytes(b"ambient\n")
            update_manifest(root, root / "MANIFEST.sha256")
            self.git(root, "add", ".gitignore", "MANIFEST.sha256")
            self.git(root, "commit", "-m", "ignored ambient fixture")
            self.assertEqual(self.git(root, "status", "--porcelain=v1"), "")
            with self.assertRaisesRegex(ArchiveError, "absent from HEAD: ambient.dat"):
                create_release_artifacts(
                    root,
                    root / "MANIFEST.sha256",
                    workspace / "output",
                    root / "release" / "release-spec.json",
                    "development",
                )

    def test_skip_worktree_payload_difference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-archive-test-") as temporary:
            workspace = Path(temporary)
            root = self.make_repository(workspace)
            original = (root / "README.md").read_bytes()
            replacement = b"replacement\n"
            (root / "README.md").write_bytes(replacement)
            update_manifest(root, root / "MANIFEST.sha256")
            (root / "README.md").write_bytes(original)
            self.git(root, "add", "MANIFEST.sha256")
            self.git(root, "commit", "-m", "anticipatory manifest fixture")
            self.git(root, "update-index", "--skip-worktree", "README.md")
            (root / "README.md").write_bytes(replacement)
            self.assertEqual(self.git(root, "status", "--porcelain=v1"), "")
            with self.assertRaisesRegex(ArchiveError, "bytes differ from HEAD: README.md"):
                create_release_artifacts(
                    root,
                    root / "MANIFEST.sha256",
                    workspace / "output",
                    root / "release" / "release-spec.json",
                    "development",
                )

    def test_sparse_missing_head_payload_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-archive-test-") as temporary:
            workspace = Path(temporary)
            root = self.make_repository(workspace)
            sparse = root / "sparse-only.txt"
            sparse.write_bytes(b"tracked but intentionally unmanifested\n")
            self.git(root, "add", "sparse-only.txt")
            self.git(root, "commit", "-m", "sparse omission fixture")
            self.git(root, "update-index", "--skip-worktree", "sparse-only.txt")
            sparse.unlink()
            self.assertEqual(self.git(root, "status", "--porcelain=v1"), "")
            with self.assertRaisesRegex(
                ArchiveError, "HEAD payload is missing from manifest: sparse-only.txt"
            ):
                create_release_artifacts(
                    root,
                    root / "MANIFEST.sha256",
                    workspace / "output",
                    root / "release" / "release-spec.json",
                    "development",
                )


if __name__ == "__main__":
    unittest.main()
