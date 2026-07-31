from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.update_manifest import update_manifest
from tools.verify_inventory_contexts import verify_inventory_contexts


@unittest.skipUnless(shutil.which("git"), "Git is required")
class InventoryContextTests(unittest.TestCase):
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

    def test_checkout_linked_worktree_and_archive_inventories_match(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-inventory-context-test-"
        ) as temporary:
            root = Path(temporary) / "repository"
            root.mkdir()
            self.git(root, "init", "--initial-branch=main")
            self.git(root, "config", "core.autocrlf", "false")
            self.git(root, "config", "user.name", "BSC Test")
            self.git(root, "config", "user.email", "bsc-test@example.invalid")
            (root / "README.md").write_bytes(b"release\n")
            (root / "nested").mkdir()
            (root / "nested" / "payload.txt").write_bytes(b"payload\n")
            update_manifest(root, root / "MANIFEST.sha256")
            self.git(root, "add", "--all")
            self.git(root, "commit", "-m", "inventory fixture")

            commit, count = verify_inventory_contexts(root)
            self.assertEqual(commit, self.git(root, "rev-parse", "HEAD"))
            self.assertEqual(count, 2)

    def test_linked_source_worktree_can_run_the_three_context_gate(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-inventory-context-test-"
        ) as temporary:
            workspace = Path(temporary)
            root = workspace / "repository"
            linked = workspace / "source-linked"
            root.mkdir()
            self.git(root, "init", "--initial-branch=main")
            self.git(root, "config", "core.autocrlf", "false")
            self.git(root, "config", "user.name", "BSC Test")
            self.git(root, "config", "user.email", "bsc-test@example.invalid")
            (root / "README.md").write_bytes(b"release\n")
            update_manifest(root, root / "MANIFEST.sha256")
            self.git(root, "add", "--all")
            self.git(root, "commit", "-m", "inventory fixture")
            self.git(root, "worktree", "add", "--detach", str(linked), "HEAD")
            try:
                self.assertTrue((linked / ".git").is_file())
                commit, count = verify_inventory_contexts(linked)
                self.assertEqual(commit, self.git(root, "rev-parse", "HEAD"))
                self.assertEqual(count, 1)
            finally:
                self.git(root, "worktree", "remove", "--force", str(linked))


if __name__ == "__main__":
    unittest.main()
