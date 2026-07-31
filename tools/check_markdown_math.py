#!/usr/bin/env python3
"""Reject Markdown math constructs that render incorrectly on GitHub."""

from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path


LEGACY_DELIMITER = re.compile(r"\\(?:\(|\)|\[|\])")
# GitHub's deployed client rejects these TeX control words.
GITHUB_FORBIDDEN_COMMANDS = (
    "DeclareMathOperator",
    "DeclarePairedDelimiters",
    "Newextarrow",
    "colorbox",
    "definecolor",
    "fcolorbox",
    "hphantom",
    "mathchoice",
    "mmlToken",
    "newtagform",
    "operatorname",
    "phantom",
    "renewtagform",
    "unicode",
    "vphantom",
)
FORBIDDEN_MATH_TOKEN = re.compile(
    r"\\(?:"
    + "|".join(re.escape(command) for command in GITHUB_FORBIDDEN_COMMANDS)
    + r")(?![A-Za-z])"
)
# CommonMark consumes these backslash escapes before ordinary dollar-delimited
# math reaches MathJax. A double backslash is deliberately absent: TeX row
# breaks survive GitHub's preprocessing.
GFM_ESCAPED_CONTROL_SYMBOL = re.compile(
    r'''(?<!\\)\\[!"#$%&'()*+,\-./:;<=>?@\[\]^_`{|}~]'''
)
MALFORMED_BRACE_MACRO = re.compile(r"\\(?:lbrace|rbrace)[A-Za-z]+")
ENVIRONMENT_TOKEN = re.compile(r"\\(begin|end)\{([A-Za-z*]+)\}")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
# GitHub can leave indented dollar displays literal inside list items. The
# repository therefore accepts display syntax only at column zero. GitHub
# renders list-indented ``math`` fences as literal code blocks rather than
# equations, so list-adjacent displays must also use column-zero fences.
DISPLAY_DELIMITER = re.compile(r"^\$\$\s*$")
INDENTED_DISPLAY_DELIMITER = re.compile(r"^(?: +|\t+)\$\$\s*$")
INDENTED_MATH_FENCE = re.compile(
    r"^[ \t]+(?:`{3,}|~{3,})[ \t]*math(?:[ \t]|$)",
    re.IGNORECASE,
)
MARKDOWN_LINK_IN_MATH = re.compile(r"\[[^\]\n]+\]\([^\)\n]+\)")
MATH_IN_MARKDOWN_LINK_LABEL = re.compile(
    r"\[[^\]]*\$[^\]]*\]\([^\)]+\)", re.DOTALL
)
DISPLAY_SETEXT_HEADING = re.compile(r"^ {0,3}(?:=+|-+)\s*$")
DISPLAY_ATX_HEADING = re.compile(r"^ {0,3}#{1,6}(?:[ \t]+|$)")
DISPLAY_BLOCKQUOTE = re.compile(r"^ {0,3}>")
DISPLAY_LIST_ITEM = re.compile(
    r"^ {0,3}(?:[-+*]|1[.)])[ \t]+\S"
)
DISPLAY_THEMATIC_BREAK = re.compile(
    r"^ {0,3}(?:(?:\*[ \t]*){3,}|(?:_[ \t]*){3,}|(?:-[ \t]*){3,})$"
)
DISPLAY_HTML_RAW_BLOCK = re.compile(
    r"^ {0,3}</?(?:script|pre|style|textarea)(?:[ \t]|>|$)",
    re.IGNORECASE,
)
DISPLAY_HTML_BLOCK_TAG = re.compile(
    r"^ {0,3}</?(?:address|article|aside|base|basefont|blockquote|body|"
    r"caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|"
    r"fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|"
    r"header|hr|html|iframe|legend|li|link|main|menu|menuitem|nav|"
    r"noframes|ol|optgroup|option|p|param|search|section|summary|table|"
    r"tbody|td|tfoot|th|thead|title|tr|track|ul)(?:[ \t]|/?>|$)",
    re.IGNORECASE,
)
TABLE_DELIMITER_CELL = re.compile(r"^:?-{3,}:?$")
BLOCKQUOTE_PREFIX = re.compile(r"^ {0,3}>")
LIST_ITEM = re.compile(r"^( {0,3})([-+*]|\d{1,9}[.)])([ \t]+)")
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


def _is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def _fence_match(line: str) -> re.Match[str] | None:
    """Return only syntactically valid GFM fence markers."""

    match = FENCE.match(line)
    if (
        match is not None
        and match.group(1).startswith("`")
        and "`" in match.group(2)
    ):
        return None
    return match


def _block_protected_lines(
    lines: list[str],
) -> list[bool]:
    """Mark block syntax that must not participate in inline parsing."""

    protected = [False] * len(lines)
    fence_marker: str | None = None
    display_open = False
    for index, line in enumerate(lines):
        fence_match = _fence_match(line)
        if fence_marker is not None:
            protected[index] = True
            if (
                fence_match
                and fence_match.group(1)[0] == fence_marker[0]
                and len(fence_match.group(1)) >= len(fence_marker)
                and not fence_match.group(2).strip()
            ):
                fence_marker = None
            continue

        if display_open:
            protected[index] = True
            if DISPLAY_DELIMITER.fullmatch(line):
                display_open = False
            continue

        if fence_match:
            protected[index] = True
            fence_marker = fence_match.group(1)
            continue

        if DISPLAY_DELIMITER.fullmatch(line):
            protected[index] = True
            display_open = True
    return protected


def _indent_width(text: str) -> int:
    return len(text.expandtabs(4))


def _indented_code_lines(
    lines: list[str],
    block_protected: list[bool],
) -> list[bool]:
    """Identify top-level and list-relative indented code blocks."""

    indented_code = [False] * len(lines)
    continuation_indent: int | None = None
    indented_block_open = False
    previous_blank = True
    for index, line in enumerate(lines):
        if block_protected[index]:
            indented_block_open = False
            previous_blank = False
            continue
        list_match = LIST_ITEM.match(line)
        if list_match:
            continuation_indent = _indent_width(
                "".join(list_match.groups())
            )
            indented_block_open = False
            previous_blank = False
            continue
        if not line.strip():
            previous_blank = True
            continue
        leading = line[: len(line) - len(line.lstrip(" \t"))]
        leading_width = _indent_width(leading)
        if continuation_indent is not None:
            if leading_width >= continuation_indent + 4:
                if indented_block_open or previous_blank:
                    indented_code[index] = True
                    indented_block_open = True
                else:
                    indented_block_open = False
                previous_blank = False
                continue
            elif leading_width >= continuation_indent:
                indented_block_open = False
                previous_blank = False
                continue
            else:
                continuation_indent = None
                indented_block_open = False
        if (
            continuation_indent is None
            and leading_width >= 4
            and (indented_block_open or previous_blank)
        ):
            indented_code[index] = True
            indented_block_open = True
        else:
            indented_block_open = False
        previous_blank = False
    return indented_code


def _parts_from_segment(
    segment: str,
    start: int,
    end: int,
    first_line: int,
) -> list[tuple[int, int, str]]:
    prefix = segment[:start]
    line_number = first_line + prefix.count("\n")
    column = start - prefix.rfind("\n")
    parts: list[tuple[int, int, str]] = []
    for offset, content in enumerate(segment[start:end].split("\n")):
        parts.append(
            (
                line_number + offset,
                column if offset == 0 else 1,
                content,
            )
        )
    return parts


def _find_exact_backtick_run(text: str, marker: str, start: int) -> int:
    position = start
    while True:
        position = text.find(marker, position)
        if position < 0:
            return -1
        before_is_tick = position > 0 and text[position - 1] == "`"
        after = position + len(marker)
        after_is_tick = after < len(text) and text[after] == "`"
        if not before_is_tick and not after_is_tick:
            return position
        position += 1


def _mask_code_spans_and_scan_backtick_math(
    path: str,
    lines: list[str],
) -> tuple[list[str], list[Finding]]:
    """Mask CommonMark code spans and scan GitHub's protected inline math."""

    block_protected = _block_protected_lines(lines)
    indented_code = _indented_code_lines(lines, block_protected)
    protected_lines = [
        block or indented
        for block, indented in zip(block_protected, indented_code)
    ]
    masked_lines = list(lines)
    for index, is_indented_code in enumerate(indented_code):
        if is_indented_code:
            masked_lines[index] = ""
    findings: list[Finding] = []
    line_index = 0

    while line_index < len(lines):
        if protected_lines[line_index] or not lines[line_index].strip():
            line_index += 1
            continue
        segment_start = line_index
        while (
            line_index < len(lines)
            and not protected_lines[line_index]
            and lines[line_index].strip()
        ):
            line_index += 1
        segment = "\n".join(lines[segment_start:line_index])
        masked = list(segment)
        index = 0

        while index < len(segment):
            if (
                segment.startswith("$`", index)
                and not _is_escaped(segment, index)
            ):
                close = segment.find("`$", index + 2)
                if close >= 0:
                    findings.extend(
                        _scan_math_region(
                            path,
                            _parts_from_segment(
                                segment,
                                index + 2,
                                close,
                                segment_start + 1,
                            ),
                            gfm_preprocessed=False,
                        )
                    )
                    for position in range(index, close + 2):
                        if masked[position] != "\n":
                            masked[position] = " "
                    index = close + 2
                    continue

            if segment[index] != "`" or _is_escaped(segment, index):
                index += 1
                continue
            run_end = index
            while run_end < len(segment) and segment[run_end] == "`":
                run_end += 1
            marker = segment[index:run_end]
            line_start = segment.rfind("\n", 0, index) + 1
            prefix = segment[line_start:index]
            if (
                len(marker) >= 3
                and not prefix.strip()
            ):
                # A fence-like line rejected by the block parser must not be
                # reinterpreted as a multiline code span that hides content.
                index = run_end
                continue
            close = _find_exact_backtick_run(segment, marker, run_end)
            if close < 0:
                index = run_end
                continue
            span_end = close + len(marker)
            for position in range(index, span_end):
                if masked[position] != "\n":
                    masked[position] = " "
            index = span_end

        masked_segment = "".join(masked)
        findings.extend(
            _scan_gfm_inline_syntax(
                path,
                masked_segment,
                segment_start + 1,
            )
        )
        replacement = masked_segment.split("\n")
        masked_lines[segment_start:line_index] = replacement

    return masked_lines, findings


def _find_delimiter(text: str, delimiter: str, start: int) -> int:
    index = start
    while True:
        index = text.find(delimiter, index)
        if index < 0:
            return -1
        if _is_escaped(text, index):
            index += len(delimiter)
            continue
        if delimiter == "$" and (
            (index > 0 and text[index - 1] == "$")
            or (index + 1 < len(text) and text[index + 1] == "$")
        ):
            index += 1
            continue
        return index


def _ordinary_math_ranges(text: str) -> list[tuple[int, int]]:
    """Locate ordinary dollar-math contents without crossing source lines."""

    ranges: list[tuple[int, int]] = []
    offset = 0
    for line_with_ending in text.splitlines(keepends=True):
        line = line_with_ending.rstrip("\r\n")
        index = 0
        while index < len(line):
            opener = _find_delimiter(line, "$", index)
            display_opener = _find_delimiter(line, "$$", index)
            if display_opener >= 0 and (
                opener < 0 or display_opener <= opener
            ):
                opener = display_opener
                delimiter = "$$"
            elif opener >= 0:
                delimiter = "$"
            else:
                break

            content_start = opener + len(delimiter)
            closer = _find_delimiter(line, delimiter, content_start)
            if closer < 0:
                break
            ranges.append(
                (offset + content_start, offset + closer)
            )
            index = closer + len(delimiter)
        offset += len(line_with_ending)
    return ranges


def _is_markdown_punctuation(character: str | None) -> bool:
    return bool(
        character
        and unicodedata.category(character).startswith(("P", "S"))
    )


def _delimiter_capabilities(
    text: str, start: int, end: int, character: str
) -> tuple[bool, bool]:
    """Return CommonMark-style capabilities for one emphasis run."""

    before = text[start - 1] if start > 0 else None
    after = text[end] if end < len(text) else None
    before_space = before is None or before.isspace()
    after_space = after is None or after.isspace()
    before_punctuation = _is_markdown_punctuation(before)
    after_punctuation = _is_markdown_punctuation(after)
    left_flanking = not after_space and (
        not after_punctuation or before_space or before_punctuation
    )
    right_flanking = not before_space and (
        not before_punctuation or after_space or after_punctuation
    )
    if character == "_":
        can_open = left_flanking and (
            not right_flanking or before_punctuation
        )
        can_close = right_flanking and (
            not left_flanking or after_punctuation
        )
    else:
        can_open = left_flanking
        can_close = right_flanking
    return can_open, can_close


def _underscore_runs_can_pair(
    opener: tuple[int, int, str, bool, bool, bool],
    closer: tuple[int, int, str, bool, bool, bool],
) -> bool:
    opener_length = opener[1] - opener[0]
    closer_length = closer[1] - closer[0]
    if (opener[4] or closer[3]) and (
        opener_length + closer_length
    ) % 3 == 0 and (
        opener_length % 3 != 0 or closer_length % 3 != 0
    ):
        return False
    return True


def _inline_syntax_containers(
    text: str,
) -> list[tuple[str, int]]:
    """Split one blank-delimited segment at GFM table/list boundaries."""

    lines = text.splitlines(keepends=True)
    table_segment = False
    for line_with_ending in lines:
        cells = _split_table_row(line_with_ending.rstrip("\r\n"))
        if cells and all(
            TABLE_DELIMITER_CELL.fullmatch(cell) for cell in cells
        ):
            table_segment = True
            break
    if table_segment:
        containers: list[tuple[str, int]] = []
        for line_offset, line_with_ending in enumerate(lines):
            line = line_with_ending.rstrip("\r\n")
            pipes = [
                index
                for index, character in enumerate(line)
                if character == "|" and not _is_escaped(line, index)
            ]
            if not pipes:
                if line.strip():
                    containers.append((line, line_offset))
                continue
            boundaries = [-1, *pipes, len(line)]
            for left, right in zip(boundaries, boundaries[1:]):
                start = left + 1
                cell = line[start:right]
                if cell.strip():
                    containers.append((" " * start + cell, line_offset))
        return containers

    containers = []
    container_start = 0
    container_line = 0
    position = 0
    for line_offset, line_with_ending in enumerate(lines):
        line = line_with_ending.rstrip("\r\n")
        if LIST_ITEM.match(line):
            if text[container_start:position].strip():
                containers.append(
                    (
                        text[container_start:position],
                        container_line,
                    )
                )
            container_start = position
            container_line = line_offset
        elif DISPLAY_ATX_HEADING.match(line):
            if text[container_start:position].strip():
                containers.append(
                    (
                        text[container_start:position],
                        container_line,
                    )
                )
            containers.append((line, line_offset))
            container_start = position + len(line_with_ending)
            container_line = line_offset + 1
        position += len(line_with_ending)
    if text[container_start:].strip():
        containers.append((text[container_start:], container_line))
    return containers


def _scan_gfm_inline_syntax(
    path: str, text: str, first_line: int
) -> list[Finding]:
    """Reject GFM emphasis that can consume ordinary dollar math first."""

    findings: list[Finding] = []
    for match in MATH_IN_MARKDOWN_LINK_LABEL.finditer(text):
        position = match.start()
        prefix = text[:position]
        findings.append(
            Finding(
                path,
                first_line + prefix.count("\n"),
                position - prefix.rfind("\n"),
                "math syntax inside Markdown link label",
            )
        )
    for container, line_offset in _inline_syntax_containers(text):
        math_ranges = _ordinary_math_ranges(container)
        if not math_ranges:
            continue

        def inside_math(position: int) -> bool:
            return any(start <= position < end for start, end in math_ranges)

        runs: list[tuple[int, int, str, bool, bool, bool]] = []
        index = 0
        while index < len(container):
            character = container[index]
            if character not in "_*" or _is_escaped(container, index):
                index += 1
                continue
            run_end = index + 1
            while (
                run_end < len(container)
                and container[run_end] == character
            ):
                run_end += 1
            can_open, can_close = _delimiter_capabilities(
                container, index, run_end, character
            )
            if can_open or can_close:
                runs.append(
                    (
                        index,
                        run_end,
                        character,
                        can_open,
                        can_close,
                        inside_math(index),
                    )
                )
            index = run_end

        openers: list[tuple[int, int, str, bool, bool, bool]] = []
        for run in runs:
            if run[4]:
                match_index = next(
                    (
                        candidate
                        for candidate in range(len(openers) - 1, -1, -1)
                        if openers[candidate][2] == run[2]
                        and _underscore_runs_can_pair(
                            openers[candidate], run
                        )
                    ),
                    None,
                )
                if match_index is not None:
                    opener = openers[match_index]
                    if opener[5] or run[5]:
                        position = run[0]
                        prefix = container[:position]
                        line_number = (
                            first_line
                            + line_offset
                            + prefix.count("\n")
                        )
                        column = position - prefix.rfind("\n")
                        findings.append(
                            Finding(
                                path,
                                line_number,
                                column,
                                "Markdown emphasis syntax inside math",
                            )
                        )
                        break
                    del openers[match_index]
            if run[3]:
                openers.append(run)
    return findings


def _scan_math_region(
    path: str,
    parts: list[tuple[int, int, str]],
    *,
    gfm_preprocessed: bool,
) -> list[Finding]:
    """Check one inline, display, or fenced math region."""

    findings: list[Finding] = []
    braces: list[tuple[int, int]] = []
    environments: list[tuple[str, int, int]] = []

    for line_number, column_offset, content in parts:
        for match in FORBIDDEN_MATH_TOKEN.finditer(content):
            findings.append(
                Finding(
                    path=path,
                    line=line_number,
                    column=column_offset + match.start(),
                    token=match.group(),
                )
            )
        if gfm_preprocessed:
            for match in GFM_ESCAPED_CONTROL_SYMBOL.finditer(content):
                findings.append(
                    Finding(
                        path=path,
                        line=line_number,
                        column=column_offset + match.start(),
                        token=match.group(),
                    )
                )
            for match in MARKDOWN_LINK_IN_MATH.finditer(content):
                findings.append(
                    Finding(
                        path=path,
                        line=line_number,
                        column=column_offset + match.start(),
                        token="Markdown link syntax inside math",
                    )
                )
        for match in MALFORMED_BRACE_MACRO.finditer(content):
            findings.append(
                Finding(
                    path=path,
                    line=line_number,
                    column=column_offset + match.start(),
                    token=match.group(),
                )
            )

        for index, character in enumerate(content):
            if character not in "{}" or _is_escaped(content, index):
                continue
            column = column_offset + index
            if character == "{":
                braces.append((line_number, column))
            elif braces:
                braces.pop()
            else:
                findings.append(
                    Finding(path, line_number, column, "}")
                )

        for match in ENVIRONMENT_TOKEN.finditer(content):
            kind, name = match.groups()
            column = column_offset + match.start()
            if kind == "begin":
                environments.append((name, line_number, column))
            elif environments and environments[-1][0] == name:
                environments.pop()
            else:
                findings.append(
                    Finding(
                        path,
                        line_number,
                        column,
                        match.group(),
                    )
                )

    findings.extend(
        Finding(path, line, column, "{") for line, column in braces
    )
    findings.extend(
        Finding(path, line, column, rf"\begin{{{name}}}")
        for name, line, column in environments
    )
    return findings


def _scan_inline_math(
    path: str,
    line_number: int,
    line: str,
) -> list[Finding]:
    """Check inline math, which GitHub requires to close on this line."""

    findings: list[Finding] = []
    index = 0
    while index < len(line):
        opener = _find_delimiter(line, "$", index)
        display_opener = _find_delimiter(line, "$$", index)
        if display_opener >= 0 and (
            opener < 0 or display_opener <= opener
        ):
            opener = display_opener
            delimiter = "$$"
        elif opener >= 0:
            delimiter = "$"
        else:
            break

        content_start = opener + len(delimiter)
        closer = _find_delimiter(line, delimiter, content_start)
        if closer < 0:
            findings.append(
                Finding(path, line_number, opener + 1, delimiter)
            )
            break
        content = line[content_start:closer]
        if delimiter in {"$", "$$"}:
            if (
                (content and content[0].isspace())
                or (content and content[-1].isspace())
            ):
                findings.append(
                    Finding(
                        path,
                        line_number,
                        opener + 1,
                        "inline math boundary whitespace",
                    )
                )
            if opener > 0 and not (
                line[opener - 1].isspace()
                or line[opener - 1] == "("
            ):
                findings.append(
                    Finding(
                        path,
                        line_number,
                        opener + 1,
                        "inline math opening context",
                    )
                )
            after = closer + len(delimiter)
            if after < len(line) and (
                line[after].isalnum() or line[after] == "_"
            ):
                findings.append(
                    Finding(
                        path,
                        line_number,
                        closer + 1,
                        "inline math closing context",
                    )
                )
        findings.extend(
            _scan_math_region(
                path,
                [
                    (
                        line_number,
                        content_start + 1,
                        content,
                    )
                ],
                gfm_preprocessed=True,
            )
        )
        index = closer + len(delimiter)
    return findings


def _split_table_row(line: str) -> list[str] | None:
    cells: list[str] = []
    current: list[str] = []
    saw_separator = False
    for index, character in enumerate(line):
        if character == "|" and not _is_escaped(line, index):
            cells.append("".join(current).strip())
            current = []
            saw_separator = True
        else:
            current.append(character)
    if not saw_separator:
        return None
    cells.append("".join(current).strip())
    stripped = line.strip()
    if stripped.startswith("|"):
        cells = cells[1:]
    if stripped.endswith("|"):
        cells = cells[:-1]
    return cells


def _is_display_block_hazard(
    line: str, previous_line: str | None
) -> bool:
    """Return whether GFM can reinterpret a line inside a ``$$`` block."""

    if not line.strip():
        return True

    if any(
        pattern.match(line)
        for pattern in (
            DISPLAY_SETEXT_HEADING,
            DISPLAY_ATX_HEADING,
            DISPLAY_BLOCKQUOTE,
            DISPLAY_LIST_ITEM,
            DISPLAY_THEMATIC_BREAK,
            DISPLAY_HTML_RAW_BLOCK,
            DISPLAY_HTML_BLOCK_TAG,
        )
    ):
        return True

    stripped = (
        line.lstrip(" ")
        if len(line) - len(line.lstrip(" ")) <= 3
        else line
    )
    if stripped.startswith(("<!--", "<?", "<![CDATA[")):
        return True
    if re.match(r"<![A-Z]", stripped):
        return True
    if _fence_match(line):
        return True

    cells = _split_table_row(line)
    previous_cells = (
        _split_table_row(previous_line)
        if previous_line is not None
        else None
    )
    return bool(
        cells
        and previous_cells
        and len(cells) == len(previous_cells)
        and all(TABLE_DELIMITER_CELL.fullmatch(cell) for cell in cells)
    )


def _scan_table_shapes(path: str, lines: list[str]) -> list[Finding]:
    block_protected = _block_protected_lines(lines)
    indented_code = _indented_code_lines(lines, block_protected)
    protected_lines = [
        block or indented
        for block, indented in zip(block_protected, indented_code)
    ]
    visible_lines = [
        "" if protected else line
        for line, protected in zip(lines, protected_lines)
    ]

    findings: list[Finding] = []
    for index in range(1, len(visible_lines)):
        delimiter_cells = _split_table_row(visible_lines[index])
        if not delimiter_cells or not all(
            TABLE_DELIMITER_CELL.fullmatch(cell)
            for cell in delimiter_cells
        ):
            continue

        expected = len(delimiter_cells)
        header_cells = _split_table_row(visible_lines[index - 1])
        if header_cells is None or len(header_cells) != expected:
            findings.append(
                Finding(
                    path,
                    index,
                    1,
                    (
                        "table columns: expected "
                        f"{expected}, found "
                        f"{0 if header_cells is None else len(header_cells)}"
                    ),
                )
            )

        row = index + 1
        while row < len(visible_lines) and visible_lines[row].strip():
            cells = _split_table_row(visible_lines[row])
            if cells is None:
                break
            if len(cells) != expected:
                first_pipe = visible_lines[row].find("|")
                findings.append(
                    Finding(
                        path,
                        row + 1,
                        first_pipe + 1 if first_pipe >= 0 else 1,
                        (
                            "table columns: expected "
                            f"{expected}, found {len(cells)}"
                        ),
                    )
                )
            row += 1
    return findings


def _scan_document(path: str, text: str) -> list[Finding]:
    lines = text.splitlines()
    masked_lines, protected_findings = (
        _mask_code_spans_and_scan_backtick_math(path, lines)
    )
    findings = _scan_table_shapes(path, lines)
    findings.extend(protected_findings)
    for line_number, line in enumerate(lines, start=1):
        if BLOCKQUOTE_PREFIX.match(line) and any(
            token in line for token in ("$", "|", "```", "~~~")
        ):
            findings.append(
                Finding(
                    path,
                    line_number,
                    1,
                    "math/table syntax in blockquote",
                )
            )
    fence_marker: str | None = None
    math_fence = False
    fence_open_line = 0
    math_parts: list[tuple[int, int, str]] = []
    display_open_line: int | None = None
    display_parts: list[tuple[int, int, str]] = []

    for line_number, (raw_line, masked) in enumerate(
        zip(lines, masked_lines), start=1
    ):
        fence_match = _fence_match(raw_line)
        if fence_marker is not None:
            if (
                fence_match
                and fence_match.group(1)[0] == fence_marker[0]
                and len(fence_match.group(1)) >= len(fence_marker)
                and not fence_match.group(2).strip()
            ):
                if math_fence:
                    findings.extend(
                        _scan_math_region(
                            path,
                            math_parts,
                            gfm_preprocessed=False,
                        )
                    )
                fence_marker = None
                math_fence = False
                math_parts = []
            elif math_fence:
                math_parts.append((line_number, 1, raw_line))
            continue

        if (
            display_open_line is None
            and INDENTED_MATH_FENCE.match(raw_line)
        ):
            findings.append(
                Finding(
                    path,
                    line_number,
                    1,
                    "math fence indentation",
                )
            )

        if fence_match and display_open_line is None:
            fence_marker = fence_match.group(1)
            fence_open_line = line_number
            info = fence_match.group(2).strip().split()
            math_fence = bool(info and info[0].lower() == "math")
            continue

        for match in LEGACY_DELIMITER.finditer(masked):
            findings.append(
                Finding(
                    path,
                    line_number,
                    match.start() + 1,
                    match.group(),
                )
            )

        if INDENTED_DISPLAY_DELIMITER.fullmatch(masked):
            findings.append(
                Finding(
                    path,
                    line_number,
                    len(masked) - len(masked.lstrip()) + 1,
                    "display math indentation",
                )
            )
            continue

        if DISPLAY_DELIMITER.fullmatch(masked):
            if display_open_line is None:
                if line_number > 1 and lines[line_number - 2].strip():
                    findings.append(
                        Finding(
                            path,
                            line_number,
                            1,
                            "display math block separation",
                        )
                    )
                display_open_line = line_number
                display_parts = []
            else:
                findings.extend(
                    _scan_math_region(
                        path,
                        display_parts,
                        gfm_preprocessed=True,
                    )
                )
                if line_number < len(lines) and lines[line_number].strip():
                    findings.append(
                        Finding(
                            path,
                            line_number,
                            1,
                            "display math block separation",
                        )
                    )
                display_open_line = None
                display_parts = []
            continue

        if display_open_line is not None:
            previous_display_line = (
                display_parts[-1][2] if display_parts else None
            )
            if _is_display_block_hazard(raw_line, previous_display_line):
                findings.append(
                    Finding(
                        path,
                        line_number,
                        1,
                        "Markdown block syntax inside display math",
                    )
                )
            display_parts.append((line_number, 1, raw_line))
            continue

        findings.extend(_scan_inline_math(path, line_number, masked))

    if fence_marker is not None:
        findings.append(
            Finding(path, fence_open_line, 1, fence_marker)
        )
    if display_open_line is not None:
        findings.append(
            Finding(path, display_open_line, 1, "$$")
        )
    return findings


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
        findings.extend(_scan_document(relative, text))
    return findings


def build_parser() -> argparse.ArgumentParser:
    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description=(
            "Reject Markdown math and table syntax known to render "
            "incorrectly on GitHub."
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
                f"{finding.column}: incompatible token {finding.token!r}",
                file=sys.stderr,
            )
        return 1

    print("MARKDOWN-MATH: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
