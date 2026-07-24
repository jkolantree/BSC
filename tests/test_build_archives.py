from __future__ import annotations

import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.build_archives import (
    ArchiveError,
    sha256_file,
    write_deterministic_zip,
)


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


if __name__ == "__main__":
    unittest.main()
