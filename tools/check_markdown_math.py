#!/usr/bin/env python3
"""Reject legacy LaTeX delimiters that GitHub Markdown does not render."""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


LEGACY_DELIMITER = re.compile(r"\\(?:\(|\)|\[|\])")
EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "build",
    "dist",
}


class MarkdownScanError(ValueError):
    """Raised when a Markdown file cannot be inspected safely."""


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    column: int
    token: str


def markdown_files(root: Path) -> list[Path]:
    root = root.resolve()
    if not root.is_dir():
        raise MarkdownScanError(f"scan root is not a directory: {root}")

    paths: list[Path] = []
    for directory, directory_names, file_names in os.walk(
        root, topdown=True, followlinks=False
    ):
        directory_names[:] = sorted(
            name
            for name in directory_names
            if name not in EXCLUDED_DIRECTORY_NAMES
        )
        current = Path(directory)
        paths.extend(
            current / name
            for name in sorted(file_names)
            if Path(name).suffix.lower() == ".md"
        )
    return paths


def scan_markdown(root: Path) -> list[Finding]:
    resolved_root = root.resolve()
    findings: list[Finding] = []
    for path in markdown_files(resolved_root):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            relative = path.relative_to(resolved_root).as_posix()
            raise MarkdownScanError(f"cannot read {relative}: {exc}") from exc
        relative = path.relative_to(resolved_root).as_posix()
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in LEGACY_DELIMITER.finditer(line):
                findings.append(
                    Finding(
                        path=relative,
                        line=line_number,
                        column=match.start() + 1,
                        token=match.group(),
                    )
                )
    return findings


def build_parser() -> argparse.ArgumentParser:
    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description=(
            "Reject legacy LaTeX delimiters in Markdown; use $...$ and "
            "$$...$$ instead."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=repository_root,
        help="Markdown tree root (default: repository root)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        findings = scan_markdown(args.root)
    except MarkdownScanError as exc:
        print(f"MARKDOWN-MATH: FAIL: {exc}", file=sys.stderr)
        return 1

    if findings:
        for finding in findings:
            print(
                f"MARKDOWN-MATH: FAIL: {finding.path}:{finding.line}:"
                f"{finding.column}: legacy delimiter {finding.token!r}",
                file=sys.stderr,
            )
        return 1

    print("MARKDOWN-MATH: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
