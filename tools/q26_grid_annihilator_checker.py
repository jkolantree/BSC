#!/usr/bin/env python3
"""Replay the exact finite arithmetic in the Q26 grid-annihilator proof.

This checker is deliberately independent of the existing Q26 shell tools and
reports only a conditional arithmetic closure.  It does not run a SAT solver,
check an LRAT proof, or promote the retained root-CNF status from UNKNOWN.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from itertools import product
from typing import Any, Iterable


SCHEMA = "bsc.q26-grid-annihilator-check.v1"
BOARD_SIZE = 26
QUEEN_COUNT = 13
COLOR_COUNTS = (6, 7)
INVENTORIES = {
    "W0": (13, 13),
    "W1": (12, 13),
    "W2": (12, 12),
}
EXPECTED_COARSE = {
    "W0": (56, 16),
    "W1": (182, 91),
    "W2": (169, 49),
}
EXPECTED_RAW_SURVIVORS = {
    "W0": ((5, 8), (6, 7), (7, 6), (8, 5)),
    "W1": ((5, 7), (5, 8), (7, 5), (7, 6)),
    "W2": ((5, 7), (7, 5)),
}
EXPECTED_REPRESENTATIVES = {
    "W0": ((5, 8), (6, 7)),
    "W1": ((5, 7), (5, 8)),
    "W2": ((5, 7),),
}
EXPECTED_CANONICAL_LIFTS = {
    ("W0", (5, 8)): ((0, 0, (3, 2, 5, 3)),),
    ("W0", (6, 7)): ((0, 0, (3, 3, 4, 3)),),
    ("W1", (5, 7)): ((1, 0, (3, 3, 4, 3)),),
    ("W1", (5, 8)): ((0, 0, (3, 2, 5, 3)),),
    ("W2", (5, 7)): (
        (0, 1, (3, 2, 5, 3)),
        (1, 0, (3, 3, 4, 3)),
    ),
}


class GridCheckError(ValueError):
    """Raised when an exact invariant in the arithmetic replay fails."""


Pair = tuple[int, int]
Table = tuple[int, int, int, int]
Lift = tuple[int, int, Table]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GridCheckError(message)


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("ascii")


def parity_table(even_row_incidence: int, even_column_incidence: int) -> Table | None:
    """Return q00,q01,q10,q11 for the normalized 6/7 color split."""

    if type(even_row_incidence) is not int or type(even_column_incidence) is not int:
        raise GridCheckError("parity margins must be integers")
    numerators = (
        even_row_incidence + even_column_incidence - 7,
        even_row_incidence - even_column_incidence + 7,
        even_column_incidence - even_row_incidence + 7,
        19 - even_row_incidence - even_column_incidence,
    )
    if any(value < 0 or value % 2 for value in numerators):
        return None
    table = tuple(value // 2 for value in numerators)
    q00, q01, q10, q11 = table
    require(sum(table) == QUEEN_COUNT, "parity table has the wrong queen total")
    require(q00 + q11 == COLOR_COUNTS[0], "even-color table total changed")
    require(q01 + q10 == COLOR_COUNTS[1], "odd-color table total changed")
    require(q00 + q01 == even_row_incidence, "even-row margin changed")
    require(q00 + q10 == even_column_incidence, "even-column margin changed")
    return table  # type: ignore[return-value]


def duplicate_choices(occupied_lines: int, occupied_even_lines: int) -> tuple[int, ...]:
    if occupied_lines == 13:
        return (0,)
    if occupied_lines == 12:
        choices: list[int] = []
        if occupied_lines - occupied_even_lines > 0:
            choices.append(0)
        if occupied_even_lines > 0:
            choices.append(1)
        return tuple(choices)
    raise GridCheckError(f"unsupported occupied-line count: {occupied_lines}")


def feasible_lifts(kind: str, pair: Pair) -> tuple[Lift, ...]:
    occupied_rows, occupied_columns = INVENTORIES[kind]
    a, b = pair
    result: list[Lift] = []
    for duplicate_row_even in duplicate_choices(occupied_rows, a):
        for duplicate_column_even in duplicate_choices(occupied_columns, b):
            table = parity_table(
                a + duplicate_row_even,
                b + duplicate_column_even,
            )
            if table is not None:
                result.append((duplicate_row_even, duplicate_column_even, table))
    return tuple(result)


def coarse_domain(kind: str) -> tuple[Pair, ...]:
    occupied_rows, occupied_columns = INVENTORIES[kind]
    pairs = tuple(product(range(occupied_rows + 1), range(occupied_columns + 1)))
    if kind == "W0":
        pairs = tuple(pair for pair in pairs if parity_table(*pair) is not None)
    return tuple(sorted(pairs))


def empty_counts(kind: str, pair: Pair) -> tuple[int, int, int, int]:
    occupied_rows, occupied_columns = INVENTORIES[kind]
    a, b = pair
    counts = (
        13 - a,
        13 - occupied_rows + a,
        13 - b,
        13 - occupied_columns + b,
    )
    require(min(counts) >= 0, f"negative empty-line count for {kind}{pair}")
    require(counts[0] + counts[1] == BOARD_SIZE - occupied_rows, "row empties changed")
    require(counts[2] + counts[3] == BOARD_SIZE - occupied_columns, "column empties changed")
    return counts


def cn_grid_ok(row_count: int, column_count: int, queen_count: int) -> bool:
    """Check every exact top-coefficient Nullstellensatz alternative."""

    if min(row_count, column_count, queen_count) < 0:
        raise GridCheckError("CN cardinalities must be nonnegative")
    return all(
        row_count <= 2 * (queen_count - j) or column_count <= 2 * j
        for j in range(queen_count + 1)
    )


def cn_profile_ok(kind: str, pair: Pair) -> bool:
    x0, x1, y0, y1 = empty_counts(kind, pair)
    # Weakley's Lemma 6 supplies an empty line of each index parity in both
    # directions.  Keep this published bridge condition separate from CN.
    if min(x0, x1, y0, y1) <= 0:
        return False
    return all(
        cn_grid_ok(rows, columns, queens)
        for rows, columns, queens in (
            (x0, y0, 6),
            (x1, y1, 6),
            (x0, y1, 7),
            (x1, y0, 7),
        )
    )


def orbit(kind: str, pair: Pair) -> frozenset[Pair]:
    a, b = pair
    if kind == "W0":
        values = ((a, b), (b, a), (13 - a, 13 - b), (13 - b, 13 - a))
    elif kind == "W1":
        values = ((a, b), (12 - a, 13 - b))
    elif kind == "W2":
        values = ((a, b), (b, a), (12 - a, 12 - b), (12 - b, 12 - a))
    else:
        raise GridCheckError(f"unknown inventory kind: {kind}")
    return frozenset(values)


def representatives(kind: str, pairs: Iterable[Pair]) -> tuple[Pair, ...]:
    domain = frozenset(pairs)
    result: set[Pair] = set()
    for pair in domain:
        item_orbit = orbit(kind, pair)
        require(item_orbit <= domain, f"{kind} domain is not orbit-closed at {pair}")
        result.add(min(item_orbit))
    return tuple(sorted(result))


def survivor_domain(kind: str) -> tuple[Pair, ...]:
    return tuple(
        pair
        for pair in coarse_domain(kind)
        if cn_profile_ok(kind, pair) and feasible_lifts(kind, pair)
    )


def normalize_equation(left: int, right: int) -> tuple[int, int]:
    require(left > 0 and right > 0, "moment coefficients must be positive")
    divisor = math.gcd(left, right)
    return left // divisor, right // divisor


def row_moment(row_count: int, column_count: int, queen_count: int) -> dict[str, int] | None:
    """Derive m*R=n*A from the exact degree-(2k-1) binomial ratio."""

    if row_count <= 0 or row_count % 2:
        return None
    if column_count % 2 == 0 and row_count + column_count == 2 * queen_count + 2:
        j = column_count // 2 - 1
        equality_case = 0  # even/even
    elif column_count % 2 == 1 and row_count + column_count == 2 * queen_count + 1:
        j = (column_count - 1) // 2
        equality_case = 1  # even/odd
    else:
        return None
    require(0 <= j <= queen_count - 1, "moment coefficient index is out of range")
    coefficient_a = math.comb(queen_count, j)
    coefficient_r = 2 * math.comb(queen_count - 1, j)
    normalized = normalize_equation(coefficient_r, coefficient_a)
    expected = normalize_equation(row_count, queen_count)
    require(normalized == expected, "binomial ratio does not give a*R=k*A")
    return {
        "a_coefficient": normalized[1],
        "binomial_a": coefficient_a,
        "binomial_r": coefficient_r,
        "column_count": column_count,
        "equality_case": equality_case,
        "j": j,
        "queen_count": queen_count,
        "r_coefficient": normalized[0],
        "row_count": row_count,
    }


def v2(value: int) -> int:
    require(value > 0, "2-adic valuation requires a positive integer")
    result = 0
    while value % 2 == 0:
        value //= 2
        result += 1
    return result


def moment_records(kind: str, pair: Pair) -> tuple[dict[str, Any], ...]:
    x0, x1, y0, y1 = empty_counts(kind, pair)
    candidates = (
        ("row", 0, 0, x0, y0, 6, "R0", "A0"),
        ("row", 0, 1, x1, y1, 6, "R0", "A1"),
        ("row", 1, 0, x0, y1, 7, "R1", "A0"),
        ("row", 1, 1, x1, y0, 7, "R1", "A1"),
        ("column", 0, 0, y0, x0, 6, "C0", "B0"),
        ("column", 0, 1, y1, x1, 6, "C0", "B1"),
        ("column", 1, 1, y1, x0, 7, "C1", "B1"),
        ("column", 1, 0, y0, x1, 7, "C1", "B0"),
    )
    result: list[dict[str, Any]] = []
    for axis, color, line_parity, lines, other_lines, queens, sum_name, line_sum_name in candidates:
        relation = row_moment(lines, other_lines, queens)
        if relation is None:
            continue
        result.append(
            {
                **relation,
                "axis": axis,
                "color": color,
                "line_parity": line_parity,
                "line_sum_name": line_sum_name,
                "queen_sum_name": sum_name,
            }
        )
    return tuple(result)


def valuation_closure(kind: str, pair: Pair, lift: Lift) -> dict[str, Any]:
    """Close one lift using only exact coefficient equations and parity."""

    _, _, table = lift
    _, q01, q10, q11 = table
    x0, x1, y0, y1 = empty_counts(kind, pair)
    exact_queen_sums = {
        "R0": 0 if q11 % 2 else None,
        "R1": 0 if q10 % 2 else None,
        "C0": 0 if q11 % 2 else None,
        "C1": 0 if q01 % 2 else None,
    }
    line_constraints = {
        "A0": {"exact": None, "lower": 1},
        "A1": {"exact": 0 if x1 % 2 else None, "lower": 0 if x1 % 2 else 1},
        "B0": {"exact": None, "lower": 1},
        "B1": {"exact": 0 if y1 % 2 else None, "lower": 0 if y1 % 2 else 1},
    }

    inferences: list[dict[str, Any]] = []
    for relation in moment_records(kind, pair):
        known_sum = exact_queen_sums[relation["queen_sum_name"]]
        if known_sum is None:
            continue
        inferred = (
            v2(relation["r_coefficient"])
            + known_sum
            - v2(relation["a_coefficient"])
        )
        inferences.append(
            {
                "line_sum_name": relation["line_sum_name"],
                "inferred_v2": inferred,
                "queen_sum_name": relation["queen_sum_name"],
                "source": [
                    relation["r_coefficient"],
                    relation["a_coefficient"],
                ],
            }
        )

    conflicts: list[dict[str, Any]] = []
    by_line_sum: dict[str, list[int]] = {"A0": [], "A1": [], "B0": [], "B1": []}
    for inference in inferences:
        by_line_sum[inference["line_sum_name"]].append(inference["inferred_v2"])
    for line_sum_name, inferred_values in by_line_sum.items():
        direct = line_constraints[line_sum_name]
        for inferred in inferred_values:
            if inferred < 0:
                conflicts.append(
                    {"code": "NEGATIVE_V2", "line_sum_name": line_sum_name, "values": [inferred]}
                )
            if direct["exact"] is not None and inferred != direct["exact"]:
                conflicts.append(
                    {
                        "code": "DIRECT_EXACT_CONFLICT",
                        "line_sum_name": line_sum_name,
                        "values": [direct["exact"], inferred],
                    }
                )
            if inferred < direct["lower"]:
                conflicts.append(
                    {
                        "code": "PARITY_LOWER_BOUND_CONFLICT",
                        "line_sum_name": line_sum_name,
                        "values": [direct["lower"], inferred],
                    }
                )
        if len(set(inferred_values)) > 1:
            conflicts.append(
                {
                    "code": "INCOMPATIBLE_MOMENTS",
                    "line_sum_name": line_sum_name,
                    "values": sorted(set(inferred_values)),
                }
            )
    require(conflicts, f"no valuation contradiction found for {kind}{pair} lift {lift[:2]}")
    return {
        "closed": True,
        "conflicts": conflicts,
        "exact_queen_sum_v2": exact_queen_sums,
        "inferences": inferences,
        "line_sum_constraints": line_constraints,
    }


def lift_record(kind: str, pair: Pair, lift: Lift) -> dict[str, Any]:
    duplicate_row_even, duplicate_column_even, table = lift
    require(table[3] == 3, f"q11 changed for {kind}{pair} lift {lift[:2]}")
    return {
        "closure": valuation_closure(kind, pair, lift),
        "duplicate_column_even": duplicate_column_even,
        "duplicate_row_even": duplicate_row_even,
        "q_table": list(table),
    }


def case_record(kind: str, pair: Pair) -> dict[str, Any]:
    lifts = feasible_lifts(kind, pair)
    require(lifts, f"survivor {kind}{pair} has no parity lift")
    return {
        "empty_counts": list(empty_counts(kind, pair)),
        "kind": kind,
        "lifts": [lift_record(kind, pair, lift) for lift in lifts],
        "moments": list(moment_records(kind, pair)),
        "pair": list(pair),
    }


def build_report() -> dict[str, Any]:
    coarse: dict[str, Any] = {}
    survivors: dict[str, Any] = {}
    canonical_cases: list[dict[str, Any]] = []
    raw_cases: list[dict[str, Any]] = []
    for kind in INVENTORIES:
        domain = coarse_domain(kind)
        coarse_representatives = representatives(kind, domain)
        require(
            (len(domain), len(coarse_representatives)) == EXPECTED_COARSE[kind],
            f"{kind} coarse domain changed",
        )
        raw_survivors = survivor_domain(kind)
        require(raw_survivors == EXPECTED_RAW_SURVIVORS[kind], f"{kind} raw survivors changed")
        survivor_representatives = representatives(kind, raw_survivors)
        require(
            survivor_representatives == EXPECTED_REPRESENTATIVES[kind],
            f"{kind} representative roster changed",
        )
        coarse[kind] = {
            "orbits": len(coarse_representatives),
            "raw_pairs": len(domain),
        }
        survivors[kind] = {
            "raw_pairs": [list(pair) for pair in raw_survivors],
            "representatives": [list(pair) for pair in survivor_representatives],
        }
        raw_cases.extend(case_record(kind, pair) for pair in raw_survivors)
        for pair in survivor_representatives:
            actual_lifts = feasible_lifts(kind, pair)
            require(
                actual_lifts == EXPECTED_CANONICAL_LIFTS[(kind, pair)],
                f"{kind}{pair} canonical lift roster changed",
            )
            canonical_cases.append(case_record(kind, pair))

    canonical_lift_count = sum(len(case["lifts"]) for case in canonical_cases)
    raw_lift_count = sum(len(case["lifts"]) for case in raw_cases)
    require(canonical_lift_count == 6, "canonical lift count changed")
    require(raw_lift_count == 12, "raw lift count changed")
    require(
        all(lift["closure"]["closed"] for case in raw_cases for lift in case["lifts"]),
        "an orbit partner did not close",
    )
    return {
        "authority": {
            "assumed_published_bridge": [
                "a hypothetical at-most-13 dominator has exactly 13 queens",
                "it is bichromatic with normalized color counts 6 and 7",
                "it has at most one excess row and at most one excess column",
                "its empty rows and columns each contain both index parities",
            ],
            "candidate_conclusion": (
                "NO_13_QUEEN_DOMINATOR_IF_THE_DOCUMENTED_PUBLISHED_BRIDGE_"
                "AND_POLYNOMIAL_LEMMAS_ARE_ACCEPTED"
            ),
            "does_not_assert": [
                "root-CNF UNSAT",
                "LRAT or DRAT proof replay",
                "solver-certified global Q26 status",
                "all difference or sum labels are distinct",
            ],
            "root_cnf_status": "UNKNOWN_UNCHANGED",
            "scope": "CONDITIONAL_EXACT_FINITE_ARITHMETIC",
        },
        "canonical_cases": canonical_cases,
        "cn_survivors": survivors,
        "coarse": coarse,
        "parameters": {
            "board_size": BOARD_SIZE,
            "color_counts": list(COLOR_COUNTS),
            "queen_count": QUEEN_COUNT,
        },
        "schema": SCHEMA,
        "status": "PASS",
        "totals": {
            "canonical_closed_lifts": canonical_lift_count,
            "coarse_orbits": sum(item["orbits"] for item in coarse.values()),
            "raw_closed_lifts": raw_lift_count,
            "raw_survivor_pairs": sum(len(item["raw_pairs"]) for item in survivors.values()),
            "survivor_orbits": sum(len(item["representatives"]) for item in survivors.values()),
        },
    }


def verify_report(report: dict[str, Any]) -> None:
    require(type(report) is dict, "report must be an object")
    require(report == build_report(), "report differs from the exact arithmetic replay")


def _summary(report: dict[str, Any]) -> str:
    totals = report["totals"]
    return (
        "PASS "
        f"coarse={totals['coarse_orbits']} "
        f"survivors={totals['survivor_orbits']} "
        f"lifts={totals['canonical_closed_lifts']} "
        "authority=CONDITIONAL_EXACT_FINITE_ARITHMETIC "
        "root_cnf=UNKNOWN_UNCHANGED"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--check", action="store_true", help="recompute and summarize every exact check")
    actions.add_argument("--json", action="store_true", help="write the canonical report to stdout")
    arguments = parser.parse_args(argv)
    try:
        report = build_report()
        verify_report(report)
        if arguments.json:
            sys.stdout.buffer.write(canonical_json_bytes(report))
        else:
            print(_summary(report))
        return 0
    except GridCheckError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    except Exception as error:  # pragma: no cover - fail-closed CLI boundary
        print(f"INTERNAL ERROR: {type(error).__name__}: {error}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
