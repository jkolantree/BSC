from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.verify_manifest import (
    ManifestError,
    inventory_release_files,
    parse_manifest,
    verify_manifest,
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class ManifestValidatorTests(unittest.TestCase):
    def make_release(
        self, files: dict[str, bytes]
    ) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="bsc-manifest-test-")
        root = Path(temporary.name)
        lines: list[str] = []
        for relative, content in sorted(files.items()):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            lines.append(f"{digest(content)}  ./{relative}\n")
        (root / "MANIFEST.sha256").write_text("".join(lines), encoding="utf-8")
        return temporary, root

    def test_complete_manifest_passes(self) -> None:
        temporary, root = self.make_release(
            {"README.md": b"release\n", "nested/data.json": b"{}\n"}
        )
        self.addCleanup(temporary.cleanup)
        self.assertEqual(
            verify_manifest(root, root / "MANIFEST.sha256"),
            [],
        )

    def test_extra_file_is_rejected(self) -> None:
        temporary, root = self.make_release({"README.md": b"release\n"})
        self.addCleanup(temporary.cleanup)
        (root / "UNMANIFESTED.md").write_text("extra\n", encoding="utf-8")
        errors = verify_manifest(root, root / "MANIFEST.sha256")
        self.assertTrue(
            any(
                "payload files missing from manifest: UNMANIFESTED.md" in error
                for error in errors
            )
        )

    def test_duplicate_manifest_path_is_rejected(self) -> None:
        temporary, root = self.make_release({"README.md": b"release\n"})
        self.addCleanup(temporary.cleanup)
        manifest = root / "MANIFEST.sha256"
        release_digest = digest(b"release\n")
        manifest.write_text(
            manifest.read_text(encoding="utf-8")
            + f"{release_digest}  ./README.md\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ManifestError, "duplicate manifest path"):
            parse_manifest(manifest)

    def test_unsafe_manifest_paths_are_rejected(self) -> None:
        unsafe_paths = [
            "../escape",
            "/absolute",
            "nested/../escape",
            "nested\\escape",
            "nested//escape",
        ]
        for unsafe in unsafe_paths:
            with self.subTest(path=unsafe):
                with tempfile.TemporaryDirectory(
                    prefix="bsc-manifest-unsafe-"
                ) as temporary:
                    manifest = Path(temporary) / "MANIFEST.sha256"
                    manifest.write_text(
                        f"{'0' * 64}  ./{unsafe}\n", encoding="utf-8"
                    )
                    with self.assertRaises(ManifestError):
                        parse_manifest(manifest)

    def test_hash_mismatch_is_rejected(self) -> None:
        temporary, root = self.make_release({"README.md": b"release\n"})
        self.addCleanup(temporary.cleanup)
        (root / "README.md").write_bytes(b"changed\n")
        errors = verify_manifest(root, root / "MANIFEST.sha256")
        self.assertTrue(any("hash mismatch for README.md" in e for e in errors))

    def test_build_directories_are_not_release_payload(self) -> None:
        temporary, root = self.make_release({"README.md": b"release\n"})
        self.addCleanup(temporary.cleanup)
        (root / "build").mkdir()
        (root / "build" / "paper.pdf").write_bytes(b"%PDF-generated")
        (root / "dist").mkdir()
        (root / "dist" / "release.zip").write_bytes(b"generated archive")
        self.assertEqual(
            verify_manifest(root, root / "MANIFEST.sha256"),
            [],
        )

    def test_root_git_directory_is_excluded(self) -> None:
        temporary, root = self.make_release({"README.md": b"release\n"})
        self.addCleanup(temporary.cleanup)
        (root / ".git").mkdir()
        (root / ".git" / "HEAD").write_text("ref: refs/heads/main\n")
        self.assertEqual(verify_manifest(root, root / "MANIFEST.sha256"), [])
        self.assertEqual(set(inventory_release_files(root)), {"README.md"})

    def test_root_git_indirection_file_is_excluded(self) -> None:
        temporary, root = self.make_release({"README.md": b"release\n"})
        self.addCleanup(temporary.cleanup)
        (root / ".git").write_text("gitdir: ../repo/.git/worktrees/linked\n")
        self.assertEqual(verify_manifest(root, root / "MANIFEST.sha256"), [])
        self.assertEqual(set(inventory_release_files(root)), {"README.md"})

    def test_manifest_cannot_admit_root_git_metadata(self) -> None:
        temporary, root = self.make_release({"README.md": b"release\n"})
        self.addCleanup(temporary.cleanup)
        manifest = root / "MANIFEST.sha256"
        manifest.write_text(
            manifest.read_text(encoding="utf-8")
            + f"{digest(b'gitdir: elsewhere\n')}  ./.git\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ManifestError, "root .git metadata"):
            parse_manifest(manifest)

    def test_nested_git_file_is_not_root_metadata(self) -> None:
        temporary, root = self.make_release({"README.md": b"release\n"})
        self.addCleanup(temporary.cleanup)
        (root / "nested").mkdir()
        (root / "nested" / ".git").write_text("payload\n")
        errors = verify_manifest(root, root / "MANIFEST.sha256")
        self.assertTrue(
            any("payload files missing from manifest: nested/.git" in e for e in errors)
        )

    def test_nested_git_directory_is_not_silently_excluded(self) -> None:
        temporary, root = self.make_release({"README.md": b"release\n"})
        self.addCleanup(temporary.cleanup)
        (root / "nested" / ".git").mkdir(parents=True)
        (root / "nested" / ".git" / "data").write_text("payload\n")
        errors = verify_manifest(root, root / "MANIFEST.sha256")
        self.assertTrue(
            any(
                "payload files missing from manifest: nested/.git/data" in e
                for e in errors
            )
        )

    def test_directory_scan_errors_fail_closed(self) -> None:
        temporary, root = self.make_release({"README.md": b"release\n"})
        self.addCleanup(temporary.cleanup)

        def denied_walk(*args: object, **kwargs: object):
            onerror = kwargs["onerror"]
            assert callable(onerror)
            onerror(PermissionError("denied fixture"))
            yield  # pragma: no cover

        with mock.patch("tools.verify_manifest.os.walk", side_effect=denied_walk):
            with self.assertRaisesRegex(ManifestError, "cannot scan release payload"):
                inventory_release_files(root)

    def test_directory_junctions_fail_closed(self) -> None:
        temporary, root = self.make_release({"README.md": b"release\n"})
        self.addCleanup(temporary.cleanup)
        (root / "linked").mkdir()
        with mock.patch.object(Path, "is_junction", return_value=True):
            with self.assertRaisesRegex(ManifestError, "directory junction"):
                inventory_release_files(root)

    def test_tmp_staging_directory_is_rejected(self) -> None:
        temporary, root = self.make_release({"README.md": b"release\n"})
        self.addCleanup(temporary.cleanup)
        (root / "tmp").mkdir()
        (root / "tmp" / "staging.bin").write_bytes(b"staging")
        errors = verify_manifest(root, root / "MANIFEST.sha256")
        self.assertTrue(
            any(
                "forbidden payload paths: tmp/staging.bin" in error
                for error in errors
            )
        )

    def test_manifest_cannot_admit_tmp_payload(self) -> None:
        temporary, root = self.make_release(
            {
                "README.md": b"release\n",
                "tmp/staging.bin": b"staging",
            }
        )
        self.addCleanup(temporary.cleanup)
        errors = verify_manifest(root, root / "MANIFEST.sha256")
        self.assertTrue(
            any(
                "forbidden payload paths: tmp/staging.bin" in error
                for error in errors
            )
        )


if __name__ == "__main__":
    unittest.main()
