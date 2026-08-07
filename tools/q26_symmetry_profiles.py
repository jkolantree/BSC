#!/usr/bin/env python3
"""Generate the exact Q26 symmetry/parity shell roster.

This module reconstructs a structural over-cover for a hypothetical
thirteen-queen dominating set on the 26 by 26 board.  It does not enumerate
queen placements and it does not call a SAT solver.
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import product
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "bsc.q26-symmetry-parity-profiles.v1"
EXPECTED_COARSE_COUNTS = (16, 91, 49)
EXPECTED_TIGHTENED_COUNTS = (15, 78, 49)
EXPECTED_TIGHTENED_W0 = (
    (1, 6),
    (1, 8),
    (2, 5),
    (2, 7),
    (2, 9),
    (3, 4),
    (3, 6),
    (3, 8),
    (3, 10),
    (4, 5),
    (4, 7),
    (4, 9),
    (5, 6),
    (5, 8),
    (6, 7),
)


class ProfileError(ValueError):
    """Raised when a profile roster violates the frozen reconstruction."""


Pair = tuple[int, int]


def w0_raw_pairs() -> frozenset[Pair]:
    """Return all feasible parity margins for the 13-row/13-column type."""

    pairs: set[Pair] = set()
    for a, b in product(range(14), repeat=2):
        numerator = a + b - 7
        if numerator % 2:
            continue
        x = numerator // 2
        cells = (x, a - x, b - x, 13 - a - b + x)
        if min(cells) >= 0:
            pairs.add((a, b))
    return frozenset(pairs)


def w1_raw_pairs() -> frozenset[Pair]:
    """Return the coarse rectangle for the 12-row/13-column type."""

    return frozenset(product(range(13), range(14)))


def w2_raw_pairs() -> frozenset[Pair]:
    """Return the coarse square for the 12-row/12-column type."""

    return frozenset(product(range(13), repeat=2))


def orbit_w0(pair: Pair) -> frozenset[Pair]:
    """Orbit under transpose and half-turn for the W0 inventory."""

    a, b = pair
    return frozenset(
        ((a, b), (b, a), (13 - a, 13 - b), (13 - b, 13 - a))
    )


def orbit_w1(pair: Pair) -> frozenset[Pair]:
    """Orbit under the residual half-turn for normalized W1 inventories."""

    a, b = pair
    return frozenset(((a, b), (12 - a, 13 - b)))


def orbit_w2(pair: Pair) -> frozenset[Pair]:
    """Orbit under transpose and half-turn for the W2 inventory."""

    a, b = pair
    return frozenset(
        ((a, b), (b, a), (12 - a, 12 - b), (12 - b, 12 - a))
    )


def representatives(
    pairs: Iterable[Pair], orbit_function: Any
) -> tuple[Pair, ...]:
    """Return the sorted lexicographically least representatives."""

    pair_set = frozenset(pairs)
    result: set[Pair] = set()
    for pair in pair_set:
        orbit = orbit_function(pair)
        if not orbit <= pair_set:
            raise ProfileError(f"orbit leaves its declared domain at {pair}")
        result.add(min(orbit))
    return tuple(sorted(result))


def _json_pairs(pairs: Iterable[Pair]) -> list[list[int]]:
    return [[a, b] for a, b in pairs]


def _assert_counts(
    coarse: tuple[tuple[Pair, ...], ...],
    tightened: tuple[tuple[Pair, ...], ...],
) -> None:
    coarse_counts = tuple(map(len, coarse))
    tightened_counts = tuple(map(len, tightened))
    if coarse_counts != EXPECTED_COARSE_COUNTS:
        raise ProfileError(
            f"coarse shell counts changed: {coarse_counts} != {EXPECTED_COARSE_COUNTS}"
        )
    if tightened_counts != EXPECTED_TIGHTENED_COUNTS:
        raise ProfileError(
            "tightened shell counts changed: "
            f"{tightened_counts} != {EXPECTED_TIGHTENED_COUNTS}"
        )
    if tightened[0] != EXPECTED_TIGHTENED_W0:
        raise ProfileError("tightened W0 representative roster changed")


def build_report() -> dict[str, Any]:
    """Build the canonical structural-profile report."""

    raw0 = w0_raw_pairs()
    raw1 = w1_raw_pairs()
    raw2 = w2_raw_pairs()

    tightened0 = frozenset(
        pair for pair in raw0 if 1 <= pair[0] <= 12 and 1 <= pair[1] <= 12
    )
    tightened1 = frozenset(pair for pair in raw1 if 1 <= pair[1] <= 12)
    tightened2 = raw2

    coarse = (
        representatives(raw0, orbit_w0),
        representatives(raw1, orbit_w1),
        representatives(raw2, orbit_w2),
    )
    tightened = (
        representatives(tightened0, orbit_w0),
        representatives(tightened1, orbit_w1),
        representatives(tightened2, orbit_w2),
    )
    _assert_counts(coarse, tightened)

    raw_domains = (raw0, raw1, raw2)
    tightened_domains = (tightened0, tightened1, tightened2)
    inventory = ((13, 13), (12, 13), (12, 12))
    labels = ("W0", "W1", "W2")
    types: dict[str, Any] = {}
    for index, label in enumerate(labels):
        occupied_rows, occupied_columns = inventory[index]
        types[label] = {
            "occupied_rows": occupied_rows,
            "occupied_columns": occupied_columns,
            "coarse": {
                "raw_pairs": len(raw_domains[index]),
                "shells": len(coarse[index]),
                "representatives": _json_pairs(coarse[index]),
            },
            "after_weakley_lemma_6": {
                "raw_pairs": len(tightened_domains[index]),
                "shells": len(tightened[index]),
                "representatives": _json_pairs(tightened[index]),
            },
        }

    return {
        "schema": SCHEMA,
        "board_size": 26,
        "queen_count": 13,
        "normalized_checkerboard_color_split": [6, 7],
        "classification": "independent_reconstruction",
        "result_type": "exhaustive_structural_over_cover",
        "shell_definition": (
            "occupied-line-count type plus occupied even-indexed row and "
            "column counts"
        ),
        "theorem_dependencies": [
            "Weakley general lower bound",
            "Weakley Proposition 11 and its equality-case proof",
            "Weakley Proposition 13, Definition 14, and Theorem 18",
            "Weakley Lemma 6",
        ],
        "source_records": [
            {
                "author": "William D. Weakley",
                "title": "Queen Domination of Even Square Boards",
                "doi": "10.37236/10617",
                "role": "theorem bridge",
            },
            {
                "author": "Dmitry Kamenetsky",
                "title": "A075458: Best known solutions for n<=26",
                "url": "https://oeis.org/A075458/a075458.txt",
                "role": "fourteen-queen upper-bound witness",
            },
        ],
        "types": types,
        "totals": {
            "coarse_shells": sum(map(len, coarse)),
            "after_weakley_lemma_6_shells": sum(map(len, tightened)),
        },
        "does_not_establish": [
            "that any shell admits a queen placement",
            "that every placement inside any shell was searched",
            "that any Q26 SAT instance is unsatisfiable",
            "that thirteen queens cannot dominate Q26",
            "that gamma(Q26) equals 14",
        ],
        "historical_solver_replay": False,
    }


def canonical_bytes(report: dict[str, Any] | None = None) -> bytes:
    """Serialize a report in its deterministic repository form."""

    if report is None:
        report = build_report()
    return (
        json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def verify_report(report: dict[str, Any]) -> None:
    """Reject any report that differs from the reconstructed roster."""

    if report != build_report():
        raise ProfileError("profile report does not match the canonical reconstruction")


def _summary(report: dict[str, Any]) -> str:
    types = report["types"]
    coarse = tuple(types[label]["coarse"]["shells"] for label in ("W0", "W1", "W2"))
    tightened = tuple(
        types[label]["after_weakley_lemma_6"]["shells"]
        for label in ("W0", "W1", "W2")
    )
    return "\n".join(
        (
            "Q26 SYMMETRY-PARITY PROFILES: PASS",
            f"coarse: {coarse} total={sum(coarse)}",
            f"after Weakley Lemma 6: {tightened} total={sum(tightened)}",
            "scope: structural over-cover only; no placement or UNSAT conclusion",
        )
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--json", action="store_true", help="print canonical JSON")
    actions.add_argument("--write", type=Path, help="write canonical JSON to PATH")
    actions.add_argument("--check", type=Path, help="verify canonical JSON at PATH")
    arguments = parser.parse_args(argv)

    report = build_report()
    encoded = canonical_bytes(report)
    if arguments.json:
        sys.stdout.buffer.write(encoded)
        return 0
    if arguments.write is not None:
        with arguments.write.open("xb") as output:
            output.write(encoded)
        print(f"Q26 SYMMETRY-PARITY PROFILES: WROTE {arguments.write}")
        return 0
    if arguments.check is not None:
        if arguments.check.read_bytes() != encoded:
            raise ProfileError(
                f"{arguments.check} does not match the canonical reconstruction"
            )
        print(f"Q26 SYMMETRY-PARITY PROFILES: PASS: {arguments.check}")
        return 0

    print(_summary(report))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ProfileError) as exc:
        print(f"Q26 SYMMETRY-PARITY PROFILES: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
