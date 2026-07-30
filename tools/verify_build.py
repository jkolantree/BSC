#!/usr/bin/env python3
"""Fail CI on missing PDFs, page drift, or final LaTeX log warnings."""

from __future__ import annotations

import argparse
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path


OUTPUT_PATTERN = re.compile(
    r"Output written on[\s\S]{1,1000}?"
    r"\((?P<pages>[0-9]+) pages?, [0-9]+ bytes\)\.",
)
FORBIDDEN_LOG_PATTERNS = {
    "LaTeX warning": re.compile(r"^LaTeX Warning:", re.MULTILINE),
    "package warning": re.compile(r"^Package .+ Warning:", re.MULTILINE),
    "class warning": re.compile(r"^Class .+ Warning:", re.MULTILINE),
    "font warning": re.compile(r"^LaTeX Font Warning:", re.MULTILINE),
    "box overflow/underflow": re.compile(
        r"^(?:Over|Under)full \\[hv]box", re.MULTILINE
    ),
    "missing glyph": re.compile(r"^Missing character:", re.MULTILINE),
    "undefined reference/citation": re.compile(
        r"(?:There were undefined (?:references|citations)|"
        r"Citation .+ undefined|Reference .+ undefined)",
        re.IGNORECASE,
    ),
    "fatal TeX error": re.compile(
        r"(?:^! |Fatal error|Emergency stop|No pages of output)",
        re.MULTILINE,
    ),
}


@dataclass(frozen=True)
class Artifact:
    name: str
    pdf: Path
    log: Path
    expected_pages: int


def verify_artifact(artifact: Artifact) -> list[str]:
    errors: list[str] = []
    try:
        mode = artifact.pdf.lstat().st_mode
        if not stat.S_ISREG(mode):
            errors.append(f"{artifact.name}: PDF is not a regular file")
        elif not artifact.pdf.read_bytes().startswith(b"%PDF-"):
            errors.append(f"{artifact.name}: output does not have a PDF header")
    except OSError as exc:
        errors.append(f"{artifact.name}: cannot read PDF: {exc}")

    try:
        log = artifact.log.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        errors.append(f"{artifact.name}: cannot read LaTeX log: {exc}")
        return errors

    outputs = list(OUTPUT_PATTERN.finditer(log))
    if len(outputs) != 1:
        errors.append(
            f"{artifact.name}: expected one final output record, found {len(outputs)}"
        )
    else:
        pages = int(outputs[0].group("pages"))
        if pages != artifact.expected_pages:
            errors.append(
                f"{artifact.name}: expected {artifact.expected_pages} pages, "
                f"got {pages}"
            )

    for description, pattern in FORBIDDEN_LOG_PATTERNS.items():
        if pattern.search(log):
            errors.append(f"{artifact.name}: final log contains {description}")
    return errors


def build_parser() -> argparse.ArgumentParser:
    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Verify release PDF existence, page counts, and final logs."
    )
    parser.add_argument("--root", type=Path, default=repository_root)
    parser.add_argument("--paper-pages", type=int, default=50)
    parser.add_argument("--synopsis-pages", type=int, default=2)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    artifacts = [
        Artifact(
            name="paper",
            pdf=root / "build/paper/On_Boundaries_of_Evidence.pdf",
            log=root / "build/paper/On_Boundaries_of_Evidence.log",
            expected_pages=args.paper_pages,
        ),
        Artifact(
            name="synopsis",
            pdf=root / "build/synopsis/Technical_Synopsis.pdf",
            log=root / "build/synopsis/Technical_Synopsis.log",
            expected_pages=args.synopsis_pages,
        ),
    ]
    errors = [error for artifact in artifacts for error in verify_artifact(artifact)]
    if errors:
        for error in errors:
            print(f"BUILD: FAIL: {error}", file=sys.stderr)
        return 1

    print(
        "BUILD: PASS: "
        f"paper={args.paper_pages} pages; "
        f"synopsis={args.synopsis_pages} pages; final logs clean"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
