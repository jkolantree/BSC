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


if __name__ == "__main__":
    unittest.main()
