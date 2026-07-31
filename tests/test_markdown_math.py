from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.check_markdown_math import (
    GITHUB_FORBIDDEN_COMMANDS,
    scan_markdown,
)


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

    def test_renderer_safe_macros_and_math_fence_pass(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "safe.md").write_text(
                "Set $\\Omega=\\lbrace x\\in\\mathbb{R}^{3}:"
                "a<\\lVert x\\rVert<b\\rbrace$ and "
                "$\\mathrm{Tr}(A)$.\n\n"
                "```math\n"
                "\\begin{aligned}\n"
                "x &= y,\\\\\n"
                "z &= 1\n"
                "\\end{aligned}\n"
                "```\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_markdown(root), [])

    def test_renderer_neutral_replacements_pass(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "safe.md").write_text(
                r"$x\mkern3mu y+x\mkern-3mu y+x\mkern5mu y$"
                "\n"
                r"$\lVert u\rVert+f_{\sharp}\mu$ and $50$%."
                "\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_markdown(root), [])

    def test_single_dollar_math_cannot_cross_a_source_line(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "Before $x +\ny$ after\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(
                [(finding.line, finding.token) for finding in findings],
                [(1, "$"), (2, "$")],
            )

    def test_inline_math_rejects_boundary_whitespace(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "Before $ x$ after\n"
                "Before $x $ after\n"
                "Before $ x $ after\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(
                [finding.token for finding in findings],
                ["inline math boundary whitespace"] * 3,
            )

    def test_inline_math_rejects_github_boundary_contexts(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "fixed-$s$ slash/$t$ attached$x$ close $y$B "
                "colon:$z$ bracket[$w$ dot.$q$\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(
                [finding.token for finding in findings],
                [
                    "inline math opening context",
                    "inline math opening context",
                    "inline math opening context",
                    "inline math closing context",
                    "inline math opening context",
                    "inline math opening context",
                    "inline math opening context",
                ],
            )

    def test_inline_math_after_parenthesis_is_supported(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "safe.md").write_text("Value ($s$).\n", encoding="utf-8")
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

    def test_exact_screenshot_failures_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "$\\operatorname{ord}_{137}(2)=68$\n"
                "$\\Omega=\\{x\\in\\mathbb R^3:a<|x|<b\\}$\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(
                [finding.token for finding in findings],
                [r"\operatorname", r"\{", r"\}"],
            )

    def test_complete_github_command_denylist_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "commands.md").write_text(
                "\n".join(
                    f"$\\{command}{{x}}$"
                    for command in GITHUB_FORBIDDEN_COMMANDS
                )
                + "\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(
                [finding.token for finding in findings],
                [f"\\{command}" for command in GITHUB_FORBIDDEN_COMMANDS],
            )

    def test_brace_control_words_require_a_separator(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "$\\lbracex\\rbrace$\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(
                [finding.token for finding in findings],
                [r"\lbracex"],
            )

    def test_unclosed_math_delimiters_are_rejected(self) -> None:
        cases = {
            "inline.md": ("Broken $x + y\n", "$"),
            "display.md": ("$$\nx + y\n", "$$"),
        }
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            for name, (source, _) in cases.items():
                (root / name).write_text(source, encoding="utf-8")
            findings = scan_markdown(root)
            self.assertEqual(
                {(finding.path, finding.token) for finding in findings},
                {(name, token) for name, (_, token) in cases.items()},
            )

    def test_unbalanced_braces_and_environments_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "structure.md").write_text(
                "$x_{1}}$\n"
                "$x_{1$\n"
                "```math\n"
                "\\begin{aligned}\n"
                "x = 1\n"
                "\\end{gathered}\n"
                "```\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(
                [finding.token for finding in findings],
                ["}", "{", r"\end{gathered}", r"\begin{aligned}"],
            )

    def test_code_spans_and_fences_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "code.md").write_text(
                "`$\\operatorname{x}$`\n\n"
                "```text\n"
                "$\\operatorname{x}$ | not | a | table\n"
                "```\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_markdown(root), [])

    def test_multiline_code_spans_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "code.md").write_text(
                "``code $\\operatorname{x}$\ncontinued``\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_markdown(root), [])

    def test_indented_code_blocks_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "code.md").write_text(
                "    $\\operatorname{x}$\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_markdown(root), [])

    def test_indented_paragraph_continuations_are_scanned(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "Paragraph\n    $\\operatorname{x}$\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [finding.token for finding in scan_markdown(root)],
                [r"\operatorname"],
            )

    def test_github_backtick_math_is_scanned_before_markdown_escaping(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "safe.md").write_text(
                "$`x\\,y+\\{z\\}+50\\%`$\n"
                "$`x +\ny`$\n",
                encoding="utf-8",
            )
            (root / "broken.md").write_text(
                "$`\\operatorname{Tr}(A)`$\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(
                [(finding.path, finding.token) for finding in findings],
                [("broken.md", r"\operatorname")],
            )

    def test_github_backtick_math_cannot_cross_blank_blocks(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "$`x\n\ny`$\n",
                encoding="utf-8",
            )
            self.assertNotEqual(scan_markdown(root), [])

    def test_gfm_inline_syntax_cannot_consume_math(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "$\\ell^{\\rm dep}_{c,j}\\le\\ell^0_{c,j}$\n\n"
                "$(\\mathsf S_i,\\mathsf{Cert}_i)$ is certified and\n"
                "$\\mathfrak M_{ij}$ is its comparison.\n\n"
                "$[\\mathcal K_Fg](x)=g(F(x))$\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [finding.token for finding in scan_markdown(root)],
                [
                    "Markdown emphasis syntax inside math",
                    "Markdown emphasis syntax inside math",
                    "Markdown link syntax inside math",
                ],
            )

            (root / "protected.md").write_text(
                "$`\\ell^{\\rm dep}_{c,j}\\le\\ell^0_{c,j}`$\n"
                "$`(\\mathsf S_i,\\mathsf{Cert}_i)`$ and "
                "$`\\mathfrak M_{ij}`$\n"
                "$`[\\mathcal K_Fg](x)=g(F(x))`$\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [
                    finding
                    for finding in scan_markdown(root)
                    if finding.path == "protected.md"
                ],
                [],
            )

    def test_gfm_inline_containers_do_not_cross_block_boundaries(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "safe.md").write_text(
                "$(\\mathsf S_i,\\mathsf{Cert}_i)$\n\n"
                "$\\mathfrak M_{ij}$\n\n"
                "| First | Second |\n"
                "| --- | --- |\n"
                "| $(\\mathsf S_i,\\mathsf{Cert}_i)$ | "
                "$\\mathfrak M_{ij}$ |\n\n"
                "- $(\\mathsf S_i,\\mathsf{Cert}_i)$\n"
                "- $\\mathfrak M_{ij}$\n\n"
                "*ordinary emphasis* and $x_i$\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_markdown(root), [])

    def test_link_labels_require_protected_math(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "[On $H(\\mathrm{curl},\\Omega)$](https://example.test/a)\n"
                "[Contractivity under\n"
                "$L_p$ norms](https://example.test/b)\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [finding.token for finding in scan_markdown(root)],
                [
                    "math syntax inside Markdown link label",
                    "math syntax inside Markdown link label",
                ],
            )

            (root / "safe.md").write_text(
                "[On $`H(\\mathrm{curl},\\Omega)`$]"
                "(https://example.test/a)\n"
                "[Contractivity under\n"
                "$`L_p`$ norms](https://example.test/b)\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [
                    finding
                    for finding in scan_markdown(root)
                    if finding.path == "safe.md"
                ],
                [],
            )

    def test_list_displays_require_column_zero_math_fences(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "- A list equation:\n\n"
                "  $$\n"
                "  x+y\n"
                "  $$\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [finding.token for finding in scan_markdown(root)],
                ["display math indentation", "display math indentation"],
            )

            (root / "broken-fence.md").write_text(
                "- A list equation:\n\n"
                "  ```math\n"
                "  x+y\n"
                "  ```\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [
                    finding.token
                    for finding in scan_markdown(root)
                    if finding.path == "broken-fence.md"
                ],
                ["math fence indentation"],
            )

            (root / "four-space-fence.md").write_text(
                "- A list equation:\n\n"
                "    ```math\n"
                "    x+y\n"
                "    ```\n",
                encoding="utf-8",
            )
            (root / "tab-fence.md").write_text(
                "- A list equation:\n\n"
                "\t```math\n"
                "\tx+y\n"
                "\t```\n",
                encoding="utf-8",
            )
            self.assertEqual(
                {
                    (finding.path, finding.token)
                    for finding in scan_markdown(root)
                    if finding.path
                    in {"four-space-fence.md", "tab-fence.md"}
                },
                {
                    (
                        "four-space-fence.md",
                        "math fence indentation",
                    ),
                    ("tab-fence.md", "math fence indentation"),
                },
            )

            (root / "safe.md").write_text(
                "- A list equation:\n\n"
                "```math\n"
                "x+y\n"
                "```\n\n"
                "- The next item.\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [
                    finding
                    for finding in scan_markdown(root)
                    if finding.path == "safe.md"
                ],
                [],
            )

    def test_gfm_escaped_control_symbols_are_rejected_in_ordinary_math(self) -> None:
        symbols = [r"\,", r"\!", r"\;", r"\|", r"\#", r"\%", r"\{", r"\}"]
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "\n".join(f"$x{symbol}y$" for symbol in symbols) + "\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(
                [finding.token for finding in findings], symbols
            )

    def test_gfm_escaped_control_symbols_are_rejected_in_display_math(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "$$\nx\\,y+f_\\#\\mu\n$$\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(
                [finding.token for finding in findings], [r"\,", r"\#"]
            )

    def test_repeated_backslashes_preserve_control_symbols(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "safe.md").write_text(
                r"$x\\,y+\\{z\\}$" + "\n"
                r"$x\\\,y+\\\{z\\\}$" + "\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_markdown(root), [])

    def test_same_line_double_dollars_require_safe_context(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "foo$$x$$bar\n"
                "x/$$y$$\n"
                "A$$z$$\n"
                "$$q$$B\n",
                encoding="utf-8",
            )
            tokens = [finding.token for finding in scan_markdown(root)]
            self.assertEqual(
                tokens,
                [
                    "inline math opening context",
                    "inline math closing context",
                    "inline math opening context",
                    "inline math opening context",
                    "inline math closing context",
                ],
            )

    def test_fences_allow_at_most_three_leading_spaces(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "valid.md").write_text(
                "```text\n$\\operatorname{x}$\n```\n\n"
                "   ~~~text\n$\\operatorname{x}$\n   ~~~\n",
                encoding="utf-8",
            )
            (root / "broken.md").write_text(
                "    ```text\n$\\operatorname{x}$\n    ```\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(
                [(finding.path, finding.token) for finding in findings],
                [("broken.md", r"\operatorname")],
            )

    def test_invalid_backtick_fence_info_cannot_hide_math(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "```foo`bar\n$\\operatorname{x}$\n```\n",
                encoding="utf-8",
            )
            self.assertIn(
                r"\operatorname",
                [finding.token for finding in scan_markdown(root)],
            )

    def test_code_spans_cannot_hide_math_across_blank_lines(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "`start\n\n$\\operatorname{x}$\n\nend`\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [finding.token for finding in scan_markdown(root)],
                [r"\operatorname"],
            )

    def test_blockquote_math_and_tables_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "> ```math\n"
                "> \\operatorname{Tr}(A)\n"
                "> ```\n\n"
                "> | Symbol | Meaning |\n"
                "> | --- | --- |\n"
                "> | $|x|$ | norm |\n",
                encoding="utf-8",
            )
            tokens = [finding.token for finding in scan_markdown(root)]
            self.assertIn("math/table syntax in blockquote", tokens)

    def test_display_math_requires_paragraph_separation(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "Before\n$$\nx+y\n$$\nAfter\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [finding.token for finding in scan_markdown(root)],
                [
                    "display math block separation",
                    "display math block separation",
                ],
            )

    def test_markdown_block_syntax_cannot_split_display_math(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            broken_blocks = [
                "$$\nx\n=\ny\n$$",
                "$$\nx\n# heading\ny\n$$",
                "$$\nx\n> quote\ny\n$$",
                "$$\nx\n- item\ny\n$$",
                "$$\nx\n+ item\ny\n$$",
                "$$\nx\n* item\ny\n$$",
                "$$\nx\n1. item\ny\n$$",
                "$$\nx\n***\ny\n$$",
                "$$\nx\n___\ny\n$$",
                "$$\nx\n<div>\ny\n$$",
                "$$\nx\n```text\ny\n$$",
                "$$\nh1 | h2\n--- | ---\n$$",
                "$$\nx\n\ny\n$$",
            ]
            (root / "broken.md").write_text(
                "\n\n".join(broken_blocks) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [finding.token for finding in scan_markdown(root)],
                ["Markdown block syntax inside display math"] * 13,
            )

            (root / "safe.md").write_text(
                "```math\nx\n=\ny\n```\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [
                    finding
                    for finding in scan_markdown(root)
                    if finding.path == "safe.md"
                ],
                [],
            )

            (root / "safe-dollar-display.md").write_text(
                "$$\n"
                "    x + y\n"
                "[x]: /url\n"
                "+\n"
                "*\n"
                "2. item\n"
                "|x|\n"
                "<m_\\Omega\n"
                "$$\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [
                    finding
                    for finding in scan_markdown(root)
                    if finding.path == "safe-dollar-display.md"
                ],
                [],
            )

    def test_ordered_list_continuations_are_scanned(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "broken.md").write_text(
                "10. A list item introduces a formula:\n\n"
                "   $$\n"
                "   \\operatorname{Tr}(A)\n"
                "   $$\n"
                "11. A list continuation has live "
                "\n    $\\operatorname{Tr}(B)$ math.\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(
                [finding.token for finding in findings],
                [
                    "display math indentation",
                    "display math indentation",
                    r"\operatorname",
                ],
            )

    def test_table_width_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "table.md").write_text(
                "| Symbol | Meaning |\n"
                "| --- | --- |\n"
                "| $|x|$ | broken |\n",
                encoding="utf-8",
            )
            findings = scan_markdown(root)
            self.assertEqual(len(findings), 1)
            self.assertEqual(
                findings[0].token,
                "table columns: expected 2, found 4",
            )

    def test_renderer_safe_table_bars_pass(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="bsc-markdown-math-"
        ) as temporary:
            root = Path(temporary)
            (root / "table.md").write_text(
                "| Symbol | Meaning |\n"
                "| --- | --- |\n"
                "| $\\lvert x\\rvert$ | valid |\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_markdown(root), [])


if __name__ == "__main__":
    unittest.main()
