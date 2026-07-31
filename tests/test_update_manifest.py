from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.update_manifest import render_manifest, update_manifest
from tools.verify_manifest import parse_manifest, verify_manifest


class ManifestUpdaterTests(unittest.TestCase):
    def test_render_is_sorted_complete_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-manifest-update-test-"
        ) as temporary:
            root = Path(temporary)
            (root / "nested").mkdir()
            (root / "nested" / "b.txt").write_bytes(b"bravo\n")
            (root / "a.txt").write_bytes(b"alpha\n")
            first = render_manifest(root)
            second = render_manifest(root)
            self.assertEqual(first, second)
            paths = [line.split("  ./", 1)[1] for line in first.splitlines()]
            self.assertEqual(paths, ["a.txt", "nested/b.txt"])

    def test_update_produces_a_verifiable_manifest(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-manifest-update-test-"
        ) as temporary:
            root = Path(temporary)
            (root / "README.md").write_bytes(b"release\n")
            manifest = root / "MANIFEST.sha256"
            self.assertEqual(update_manifest(root, manifest), 1)
            self.assertEqual(verify_manifest(root, manifest), [])
            self.assertEqual(set(parse_manifest(manifest)), {"README.md"})

    def test_generated_directories_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-manifest-update-test-"
        ) as temporary:
            root = Path(temporary)
            (root / "README.md").write_bytes(b"release\n")
            (root / "build").mkdir()
            (root / "build" / "artifact.pdf").write_bytes(b"%PDF")
            rendered = render_manifest(root)
            self.assertIn("./README.md", rendered)
            self.assertNotIn("artifact.pdf", rendered)

    def test_render_is_invariant_across_git_root_representations(self) -> None:
        rendered: list[str] = []
        for representation in ("directory", "file", "absent"):
            with self.subTest(representation=representation):
                with tempfile.TemporaryDirectory(
                    prefix="bsc-manifest-update-test-"
                ) as temporary:
                    root = Path(temporary)
                    (root / "README.md").write_bytes(b"release\n")
                    if representation == "directory":
                        (root / ".git").mkdir()
                        (root / ".git" / "HEAD").write_text(
                            "ref: refs/heads/main\n", encoding="utf-8"
                        )
                    elif representation == "file":
                        (root / ".git").write_text(
                            "gitdir: ../repo/.git/worktrees/linked\n",
                            encoding="utf-8",
                        )
                    rendered.append(render_manifest(root))
        self.assertEqual(rendered, [rendered[0]] * 3)
        self.assertNotIn(".git", rendered[0])

    def test_update_removes_a_stale_root_git_manifest_entry(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-manifest-update-test-"
        ) as temporary:
            root = Path(temporary)
            (root / "README.md").write_bytes(b"release\n")
            (root / ".git").write_text(
                "gitdir: ../repo/.git/worktrees/linked\n", encoding="utf-8"
            )
            manifest = root / "MANIFEST.sha256"
            manifest.write_text(
                f"{'0' * 64}  ./.git\n", encoding="utf-8", newline="\n"
            )
            self.assertEqual(update_manifest(root, manifest), 1)
            self.assertEqual(set(parse_manifest(manifest)), {"README.md"})
            self.assertEqual(verify_manifest(root, manifest), [])


if __name__ == "__main__":
    unittest.main()
