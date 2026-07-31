from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest import mock

from tools.archive_validation import SOURCE_ARCHIVE_MEMBERS
from tools.build_archives import create_release_artifacts
from tools.release_identity import (
    IdentityError,
    canonical_manifest_path,
    canonical_json_bytes,
    resolve_build_plan,
    sha256_file,
    verify_identity_file,
    write_identity_file,
)
from tools.update_manifest import update_manifest


class GitRepositoryTestCase(unittest.TestCase):
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
        self, workspace: Path, version: str | None = None, epoch: int | None = None
    ) -> Path:
        root = workspace / "repository"
        root.mkdir()
        self.git(root, "init", "--initial-branch=main")
        self.git(root, "config", "core.autocrlf", "false")
        self.git(root, "config", "user.name", "BSC Test")
        self.git(root, "config", "user.email", "bsc-test@example.invalid")
        (root / "release").mkdir()
        self.write_spec(root, version, epoch)
        for relative in SOURCE_ARCHIVE_MEMBERS:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"fixture for {relative}\n", encoding="utf-8")
        self.write_release_surfaces(root, version, epoch)
        update_manifest(root, root / "MANIFEST.sha256")
        self.git(root, "add", "--all")
        self.git(root, "commit", "-m", "release fixture")
        return root

    def write_spec(
        self, root: Path, version: str | None, epoch: int | None
    ) -> None:
        (root / "release" / "release-spec.json").write_text(
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

    def spec(self, root: Path) -> Path:
        return root / "release" / "release-spec.json"

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
        paper = root / "paper/source/On_Boundaries_of_Evidence.tex"
        paper.write_text(
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

    def git_without_replacements(self, root: Path, *args: str) -> str:
        environment = os.environ.copy()
        environment["GIT_CONFIG_NOSYSTEM"] = "1"
        environment["GIT_NO_REPLACE_OBJECTS"] = "1"
        result = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=environment,
        )
        return result.stdout.strip()


class ReleaseAuthorityTests(GitRepositoryTestCase):
    def test_development_name_contains_source_commit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            root = self.make_repository(Path(temporary))
            plan = resolve_build_plan(root, self.spec(root), "development")
            self.assertIn(plan.git.commit[:12], plan.outer_label)
            self.assertEqual(plan.version, None)
            self.assertEqual(plan.tag_object, None)

    def test_candidate_requires_matching_spec_and_contains_commit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            root = self.make_repository(Path(temporary), "1.5.0", 1785542400)
            plan = resolve_build_plan(root, self.spec(root), "candidate", "1.5.0")
            self.assertIn(plan.git.commit[:12], plan.outer_label)
            self.assertEqual(plan.archive_label, "v1.5.0")
            with self.assertRaisesRegex(IdentityError, "does not match"):
                resolve_build_plan(root, self.spec(root), "candidate", "1.5.1")

    def test_candidate_rejects_an_existing_tag(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            root = self.make_repository(Path(temporary), "1.5.0", 1785542400)
            self.git(root, "tag", "-a", "v1.5.0", "-m", "release")
            with self.assertRaisesRegex(IdentityError, "tag already exists"):
                resolve_build_plan(root, self.spec(root), "candidate", "1.5.0")

    def test_candidate_rejects_stale_release_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            root = self.make_repository(Path(temporary), "1.5.0", 1785542400)
            (root / "README.md").write_text(
                "**Latest released version:** v1.4.0\n", encoding="utf-8"
            )
            update_manifest(root, root / "MANIFEST.sha256")
            self.git(root, "add", "README.md", "MANIFEST.sha256")
            self.git(root, "commit", "-m", "stale metadata fixture")
            with self.assertRaisesRegex(IdentityError, "release metadata"):
                resolve_build_plan(root, self.spec(root), "candidate", "1.5.0")

    def test_release_requires_annotated_tag_at_head(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            root = self.make_repository(Path(temporary), "1.5.0", 1785542400)
            with self.assertRaises(IdentityError):
                resolve_build_plan(root, self.spec(root), "release", "1.5.0")
            self.git(root, "tag", "v1.5.0")
            with self.assertRaisesRegex(IdentityError, "annotated tag"):
                resolve_build_plan(root, self.spec(root), "release", "1.5.0")
            self.git(root, "tag", "-d", "v1.5.0")
            self.git(root, "tag", "-a", "v1.5.0", "-m", "release")
            plan = resolve_build_plan(root, self.spec(root), "release", "1.5.0")
            self.assertEqual(plan.tag_name, "v1.5.0")
            self.assertEqual(plan.tag_object, self.git(root, "rev-parse", "v1.5.0"))
            self.assertNotEqual(plan.tag_object, plan.git.commit)

    def test_release_rejects_tag_to_tag_chain(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            root = self.make_repository(Path(temporary), "1.5.0", 1785542400)
            self.git(root, "tag", "-a", "base", "-m", "base")
            self.git(root, "tag", "-a", "v1.5.0", "base", "-m", "release")
            with self.assertRaisesRegex(IdentityError, "directly tag a commit"):
                resolve_build_plan(root, self.spec(root), "release", "1.5.0")

    def test_release_rejects_mismatched_internal_tag_name(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            root = self.make_repository(Path(temporary), "1.5.0", 1785542400)
            self.git(root, "tag", "-a", "other", "-m", "other")
            other_object = self.git(root, "rev-parse", "refs/tags/other")
            self.git(root, "update-ref", "refs/tags/v1.5.0", other_object)
            with self.assertRaisesRegex(IdentityError, "object name"):
                resolve_build_plan(root, self.spec(root), "release", "1.5.0")

    def test_release_rejects_same_tree_at_a_different_commit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            root = self.make_repository(Path(temporary), "1.5.0", 1785542400)
            self.git(root, "tag", "-a", "v1.5.0", "-m", "release")
            tagged_tree = self.git(root, "rev-parse", "v1.5.0^{tree}")
            self.git(root, "commit", "--allow-empty", "-m", "same tree new commit")
            self.assertEqual(tagged_tree, self.git(root, "rev-parse", "HEAD^{tree}"))
            with self.assertRaisesRegex(IdentityError, "does not directly tag HEAD"):
                resolve_build_plan(root, self.spec(root), "release", "1.5.0")

    def test_dirty_staged_unstaged_and_untracked_inputs_fail_closed(self) -> None:
        mutations = ("unstaged", "staged", "untracked")
        for mutation in mutations:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory(
                prefix="bsc-identity-test-"
            ) as temporary:
                root = self.make_repository(Path(temporary))
                if mutation == "unstaged":
                    (root / "README.md").write_bytes(b"changed\n")
                elif mutation == "staged":
                    (root / "README.md").write_bytes(b"changed\n")
                    self.git(root, "add", "README.md")
                else:
                    (root / "UNTRACKED").write_bytes(b"extra\n")
                with self.assertRaisesRegex(IdentityError, "clean Git worktree"):
                    resolve_build_plan(root, self.spec(root), "development")

    def test_malformed_version_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            root = self.make_repository(Path(temporary), "1.5.0", 1785542400)
            for version in ("v1.5.0", "01.5.0", "1.5", "1.5.0+local"):
                with self.subTest(version=version), self.assertRaises(IdentityError):
                    resolve_build_plan(root, self.spec(root), "candidate", version)

    def test_git_replacement_objects_do_not_change_recorded_identity(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            root = self.make_repository(Path(temporary))
            prior = self.git(root, "rev-parse", "HEAD")
            (root / "README.md").write_text("second tree\n", encoding="utf-8")
            update_manifest(root, root / "MANIFEST.sha256")
            self.git(root, "add", "README.md", "MANIFEST.sha256")
            self.git(root, "commit", "-m", "second tree")
            head = self.git(root, "rev-parse", "HEAD")
            self.git(root, "replace", head, prior)
            raw_tree = self.git_without_replacements(root, "rev-parse", "HEAD^{tree}")
            plan = resolve_build_plan(root, self.spec(root), "development")
            self.assertEqual(plan.git.commit, head)
            self.assertEqual(plan.git.tree, raw_tree)

    def test_redirecting_git_environment_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            workspace = Path(temporary)
            root = self.make_repository(workspace)
            with mock.patch.dict(
                os.environ,
                {
                    "GIT_DIR": str(workspace / "not-a-repository"),
                    "GIT_WORK_TREE": str(workspace / "wrong-worktree"),
                    "GIT_INDEX_FILE": str(workspace / "wrong-index"),
                },
                clear=False,
            ):
                plan = resolve_build_plan(root, self.spec(root), "development")
            self.assertEqual(plan.git.commit, self.git(root, "rev-parse", "HEAD"))


class DetachedIdentityTests(GitRepositoryTestCase):
    def test_serialization_is_deterministic_and_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            workspace = Path(temporary)
            root = self.make_repository(workspace)
            first = create_release_artifacts(
                root,
                root / "MANIFEST.sha256",
                workspace / "first",
                self.spec(root),
                "development",
            )
            second = create_release_artifacts(
                root,
                root / "MANIFEST.sha256",
                workspace / "second",
                self.spec(root),
                "development",
            )
            identity = first[2]
            document = json.loads(identity.read_text(encoding="utf-8"))
            self.assertEqual(identity.read_bytes(), canonical_json_bytes(document))
            self.assertEqual(identity.read_bytes(), second[2].read_bytes())
            self.assertNotIn(str(root), identity.read_text(encoding="utf-8"))
            verify_identity_file(
                root, self.spec(root), root / "MANIFEST.sha256", identity
            )
            first[0].write_bytes(b"mutated")
            with self.assertRaises(IdentityError):
                verify_identity_file(
                    root, self.spec(root), root / "MANIFEST.sha256", identity
                )

    def test_identity_writer_never_removes_an_existing_record(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            identity = Path(temporary) / "identity.json"
            identity.write_bytes(b"preserve me\n")
            with self.assertRaises(FileExistsError):
                write_identity_file(identity, {"schema": "test"})
            self.assertEqual(identity.read_bytes(), b"preserve me\n")

    def test_appended_zip_trailer_fails_even_if_identity_is_rehashed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            workspace = Path(temporary)
            root = self.make_repository(workspace)
            outputs = create_release_artifacts(
                root,
                root / "MANIFEST.sha256",
                workspace / "output",
                self.spec(root),
                "development",
            )
            complete, _, identity = outputs
            with complete.open("ab") as stream:
                stream.write(b"UNMANIFESTED-TRAILER")
            document = json.loads(identity.read_text(encoding="utf-8"))
            complete_record = next(
                item
                for item in document["artifacts"]
                if item["role"] == "complete-release"
            )
            complete_record["sha256"] = sha256_file(complete)
            complete_record["size"] = complete.stat().st_size
            identity.write_bytes(canonical_json_bytes(document))
            with self.assertRaisesRegex(IdentityError, "not canonical"):
                verify_identity_file(
                    root, self.spec(root), root / "MANIFEST.sha256", identity
                )

    def test_canonical_manifest_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-identity-test-") as temporary:
            root = Path(temporary) / "root"
            root.mkdir()
            outside = Path(temporary) / "outside-manifest"
            outside.write_text("outside\n", encoding="utf-8")
            try:
                (root / "MANIFEST.sha256").symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            with self.assertRaisesRegex(IdentityError, "regular file"):
                canonical_manifest_path(root, root / "MANIFEST.sha256")


if __name__ == "__main__":
    unittest.main()
