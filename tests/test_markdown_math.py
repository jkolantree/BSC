from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.check_markdown_math import scan_markdown


class MarkdownMathTests(unittest.TestCase):
    def test_github_math_delimiters_pass(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "README.md").write_text(
                "Inline $x^2$ and display:\n\n$$\nx^2 + y^2\n$$\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_markdown(root), [])

    def test_every_legacy_delimiter_is_rejected(self) -> None:
        tokens = [r"\(", r"\)", r"\[", r"\]"]
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "legacy.md").write_text(
                " ".join(tokens) + "\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual([finding.token for finding in findings], tokens)

    def test_generated_directories_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "README.md").write_text("$x$\n", encoding="utf-8")
            for directory in ("build", "dist"):
                path = root / directory
                path.mkdir()
                (path / "generated.md").write_text(
                    r"\(legacy\)" + "\n",
                    encoding="utf-8",
                )
            self.assertEqual(scan_markdown(root), [])


if __name__ == "__main__":
    unittest.main()
