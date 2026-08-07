#!/usr/bin/env python3
"""Verify C13-COV-01 and the finite arithmetic in C13-RIG-01."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import Counter
from functools import lru_cache
from math import comb
from pathlib import Path
from typing import Any, Iterable, Sequence


HERE = Path(__file__).resolve().parent
DEFAULT_CONSTRUCTION = HERE / "construction.json"
DEFAULT_PROVENANCE = HERE / "provenance.json"
DEFAULT_RECEIPT = HERE / "verification_receipt.json"

EXPECTED_SOURCE_TEXT_SHA256 = (
    "76f4ce2b6b42391f49bd83708d820ae38eb67939d7a7a5c3427a2cbbed4a2e7d"
)
EXPECTED_CONSTRUCTION_TEXT_SHA256 = (
    "7306ee18f5181f2ff3afb7054ceec9bded0fc4424a1f842644c1afbf64f83582"
)
EXPECTED_LEAVE = ((2, 5, 7), (5, 7, 10))
EXPECTED_REMOVED = (
    (1, 2, 7, 8, 10, 11),
    (1, 3, 4, 7, 8, 12),
    (2, 3, 5, 7, 10, 12),
)
EXPECTED_ADDED = (
    (1, 3, 4, 7, 8, 11),
    (2, 3, 7, 8, 10, 12),
)
EXPECTED_BLOCKED_PROMOTIONS = (
    "C(13,6,3)=21",
    "284 is an optimal 20-block partial coverage value",
    "284 is a best-known 20-block partial coverage value",
    "absolute historical priority",
    "kernel-verified proof",
    "formal proof",
)


class C13VerificationError(ValueError):
    """Raised when tracked evidence fails closed."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise C13VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    try:
        value = json.loads(
            raw.decode("utf-8", errors="strict"),
            object_pairs_hook=_strict_object,
        )
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise C13VerificationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise C13VerificationError(f"top-level JSON in {path} must be an object")
    return value, raw


def require_exact_keys(value: dict[str, Any], expected: Iterable[str], label: str) -> None:
    expected_set = set(expected)
    observed = set(value)
    if observed != expected_set:
        raise C13VerificationError(
            f"{label} keys differ: missing={sorted(expected_set - observed)}, "
            f"extra={sorted(observed - expected_set)}"
        )


def require_plain_int(value: Any, label: str) -> int:
    if type(value) is not int:
        raise C13VerificationError(f"{label} must be an integer")
    return value


def validate_sha256(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise C13VerificationError(f"{label} must be 64 lowercase hexadecimal digits")
    return value


def validate_blocks(
    raw_blocks: Any,
    *,
    expected_count: int,
    label: str,
    require_lexicographic_inventory: bool,
) -> tuple[tuple[int, ...], ...]:
    if not isinstance(raw_blocks, list) or len(raw_blocks) != expected_count:
        raise C13VerificationError(
            f"{label} must contain exactly {expected_count} blocks"
        )
    blocks: list[tuple[int, ...]] = []
    for index, raw_block in enumerate(raw_blocks):
        if not isinstance(raw_block, list) or len(raw_block) != 6:
            raise C13VerificationError(f"{label}[{index}] must be a six-element list")
        if any(type(point) is not int for point in raw_block):
            raise C13VerificationError(f"{label}[{index}] contains a non-integer")
        block = tuple(raw_block)
        if block != tuple(sorted(block)):
            raise C13VerificationError(f"{label}[{index}] is not strictly ordered")
        if len(set(block)) != 6 or not all(1 <= point <= 13 for point in block):
            raise C13VerificationError(f"{label}[{index}] is not a 6-subset of [13]")
        blocks.append(block)
    if len(set(blocks)) != expected_count:
        raise C13VerificationError(f"{label} contains a duplicate block")
    result = tuple(blocks)
    if require_lexicographic_inventory and result != tuple(sorted(result)):
        raise C13VerificationError(f"{label} is not in canonical lexicographic order")
    return result


def normalized_block_bytes(blocks: Sequence[Sequence[int]]) -> bytes:
    return (
        "".join(" ".join(str(point) for point in block) + "\n" for block in blocks)
    ).encode("ascii")


def subset_multiplicities(
    point_set: Sequence[int],
    blocks: Sequence[Sequence[int]],
    subset_size: int,
) -> dict[tuple[int, ...], int]:
    result = {
        subset: 0 for subset in itertools.combinations(point_set, subset_size)
    }
    for block in blocks:
        for subset in itertools.combinations(block, subset_size):
            result[subset] += 1
    return result


def value_histogram(values: Iterable[int]) -> dict[int, int]:
    return dict(sorted(Counter(values).items()))


def block_intersection_histogram(
    blocks: Sequence[Sequence[int]],
) -> dict[int, int]:
    counts = Counter(
        len(set(left).intersection(right))
        for left, right in itertools.combinations(blocks, 2)
    )
    return {intersection: counts[intersection] for intersection in range(6)}


def covered_triple_count(
    point_set: Sequence[int], blocks: Sequence[Sequence[int]]
) -> int:
    return sum(
        multiplicity > 0
        for multiplicity in subset_multiplicities(point_set, blocks, 3).values()
    )


def verify_construction(document: dict[str, Any]) -> dict[str, Any]:
    require_exact_keys(
        document,
        {"artifact_id", "construction", "parameters", "schema", "source_cover"},
        "construction document",
    )
    if document["schema"] != "c13-covering-construction-v1":
        raise C13VerificationError("unexpected construction schema")
    if document["artifact_id"] != "C13-COV-01":
        raise C13VerificationError("unexpected construction artifact identifier")

    parameters = document["parameters"]
    if not isinstance(parameters, dict):
        raise C13VerificationError("parameters must be an object")
    require_exact_keys(parameters, {"block_count", "k", "point_set", "t", "v"}, "parameters")
    expected_parameters = {
        "block_count": 20,
        "k": 6,
        "point_set": list(range(1, 14)),
        "t": 3,
        "v": 13,
    }
    if parameters != expected_parameters:
        raise C13VerificationError("construction parameters differ from (13,6,3;20)")
    point_set = tuple(parameters["point_set"])

    source = document["source_cover"]
    if not isinstance(source, dict):
        raise C13VerificationError("source_cover must be an object")
    require_exact_keys(source, {"blocks", "record_id"}, "source_cover")
    if source["record_id"] != "LJCR-C(13,6,3)-21":
        raise C13VerificationError("unexpected source-cover record identifier")
    source_blocks = validate_blocks(
        source["blocks"],
        expected_count=21,
        label="source_cover.blocks",
        require_lexicographic_inventory=False,
    )

    construction = document["construction"]
    if not isinstance(construction, dict):
        raise C13VerificationError("construction must be an object")
    require_exact_keys(
        construction,
        {"blocks", "claimed_covered_triples", "claimed_leave", "relation_to_source"},
        "construction",
    )
    blocks = validate_blocks(
        construction["blocks"],
        expected_count=20,
        label="construction.blocks",
        require_lexicographic_inventory=True,
    )

    source_bytes = normalized_block_bytes(source_blocks)
    construction_bytes = normalized_block_bytes(blocks)
    if hashlib.sha256(source_bytes).hexdigest() != EXPECTED_SOURCE_TEXT_SHA256:
        raise C13VerificationError("normalized source-cover identity mismatch")
    if (
        hashlib.sha256(construction_bytes).hexdigest()
        != EXPECTED_CONSTRUCTION_TEXT_SHA256
    ):
        raise C13VerificationError("normalized construction identity mismatch")

    source_triples = subset_multiplicities(point_set, source_blocks, 3)
    if sum(value > 0 for value in source_triples.values()) != 286:
        raise C13VerificationError("source inventory does not cover all 286 triples")

    triples = subset_multiplicities(point_set, blocks, 3)
    leave = tuple(triple for triple, multiplicity in triples.items() if multiplicity == 0)
    covered = 286 - len(leave)
    claimed_leave_raw = construction["claimed_leave"]
    if not isinstance(claimed_leave_raw, list):
        raise C13VerificationError("claimed_leave must be a list")
    claimed_leave = tuple(tuple(item) for item in claimed_leave_raw)
    if claimed_leave != EXPECTED_LEAVE or leave != EXPECTED_LEAVE:
        raise C13VerificationError("the exact two-triple leave does not match")
    if require_plain_int(
        construction["claimed_covered_triples"], "claimed_covered_triples"
    ) != 284 or covered != 284:
        raise C13VerificationError("covered-triple count does not equal 284")

    relation = construction["relation_to_source"]
    if not isinstance(relation, dict):
        raise C13VerificationError("relation_to_source must be an object")
    require_exact_keys(
        relation,
        {"added_blocks", "common_block_count", "removed_blocks"},
        "relation_to_source",
    )
    removed = tuple(tuple(block) for block in relation["removed_blocks"])
    added = tuple(tuple(block) for block in relation["added_blocks"])
    source_set = set(source_blocks)
    construction_set = set(blocks)
    observed_removed = tuple(sorted(source_set - construction_set))
    observed_added = tuple(sorted(construction_set - source_set))
    if removed != EXPECTED_REMOVED or observed_removed != EXPECTED_REMOVED:
        raise C13VerificationError("removed-block inventory mismatch")
    if added != EXPECTED_ADDED or observed_added != EXPECTED_ADDED:
        raise C13VerificationError("added-block inventory mismatch")
    common = len(source_set.intersection(construction_set))
    if require_plain_int(relation["common_block_count"], "common_block_count") != 18:
        raise C13VerificationError("claimed common-block count differs from 18")
    if common != 18:
        raise C13VerificationError("observed common-block count differs from 18")

    point_degrees = {
        point: sum(point in block for block in blocks) for point in point_set
    }
    pairs = subset_multiplicities(point_set, blocks, 2)
    intersections = block_intersection_histogram(blocks)
    triple_histogram = value_histogram(triples.values())
    pair_histogram = value_histogram(pairs.values())
    point_degree_histogram = value_histogram(point_degrees.values())
    expected_intersections = {0: 0, 1: 6, 2: 75, 3: 103, 4: 0, 5: 6}
    if point_degree_histogram != {9: 10, 10: 3}:
        raise C13VerificationError("point-degree histogram mismatch")
    if pair_histogram != {3: 24, 4: 42, 5: 12}:
        raise C13VerificationError("pair-multiplicity histogram mismatch")
    if triple_histogram != {0: 2, 1: 203, 2: 58, 3: 11, 4: 12}:
        raise C13VerificationError("triple-multiplicity histogram mismatch")
    if intersections != expected_intersections:
        raise C13VerificationError("block-intersection histogram mismatch")

    e2 = sum((multiplicity - 3) ** 2 for multiplicity in pairs.values())
    q_value = sum(
        comb(multiplicity - 1, 2)
        for multiplicity in triples.values()
        if multiplicity >= 1
    )
    h_value = sum(max(multiplicity - 2, 0) for multiplicity in triples.values())
    uncovered = triple_histogram[0]
    singly_covered = triple_histogram[1]
    d_value = intersections[1] + 4 * intersections[4] + 15 * intersections[5]
    j_value = 4 * intersections[4] + 15 * intersections[5]
    s1 = sum(index * count for index, count in intersections.items())
    s2 = sum(comb(index, 2) * count for index, count in intersections.items())
    s3 = sum(comb(index, 3) * count for index, count in intersections.items())
    observed = {
        "D": d_value,
        "E2": e2,
        "H": h_value,
        "J": j_value,
        "Q": q_value,
        "S1": s1,
        "S2": s2,
        "S3": s3,
        "U": uncovered,
        "singly_covered": singly_covered,
    }
    expected = {
        "D": 96,
        "E2": 90,
        "H": 35,
        "J": 90,
        "Q": 47,
        "S1": 495,
        "S2": 444,
        "S3": 163,
        "U": 2,
        "singly_covered": 203,
    }
    if observed != expected:
        raise C13VerificationError(f"near-cover moment record mismatch: {observed}")

    c_value = s1 - 456
    if 3 * (q_value + uncovered) != e2 + d_value - c_value:
        raise C13VerificationError("corrected partial-cover moment identity failed")
    if singly_covered != 172 + h_value - 2 * uncovered:
        raise C13VerificationError("corrected partial-cover singleton identity failed")
    if 3 * q_value == e2 + d_value - c_value:
        raise C13VerificationError("complete-cover identity was accepted for a partial cover")
    if singly_covered == 172 + h_value:
        raise C13VerificationError("complete-cover singleton identity was accepted")

    deletion_counts = Counter(
        covered_triple_count(
            point_set, source_blocks[:index] + source_blocks[index + 1 :]
        )
        for index in range(len(source_blocks))
    )
    expected_deletions = {
        271: 1,
        272: 3,
        273: 2,
        274: 3,
        276: 2,
        280: 4,
        281: 3,
        282: 1,
        283: 2,
    }
    if dict(sorted(deletion_counts.items())) != expected_deletions:
        raise C13VerificationError("source one-block-deletion histogram mismatch")

    return {
        "added_blocks": [list(block) for block in observed_added],
        "block_count": len(blocks),
        "block_intersection_histogram": {
            str(key): value for key, value in intersections.items()
        },
        "common_blocks": common,
        "covered_triples": covered,
        "deletion_coverage_histogram": {
            str(key): value for key, value in expected_deletions.items()
        },
        "leave": [list(triple) for triple in leave],
        "moments": observed,
        "normalized_blocks_sha256": hashlib.sha256(construction_bytes).hexdigest(),
        "pair_multiplicity_histogram": {
            str(key): value for key, value in pair_histogram.items()
        },
        "point_degree_histogram": {
            str(key): value for key, value in point_degree_histogram.items()
        },
        "removed_blocks": [list(block) for block in observed_removed],
        "source_covers_all_triples": True,
        "source_normalized_blocks_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "triple_multiplicity_histogram": {
            str(key): value for key, value in triple_histogram.items()
        },
    }


def balanced_square_minimum(total: int, slots: int) -> int:
    if type(total) is not int or type(slots) is not int or total < 0 or slots <= 0:
        raise C13VerificationError("balanced-square arguments are invalid")
    quotient, remainder = divmod(total, slots)
    return (slots - remainder) * quotient**2 + remainder * (quotient + 1) ** 2


def e2_lower_bounds() -> dict[str, int]:
    # Type A: x is the total excess on the three high-high pairs.
    type_a = min(
        balanced_square_minimum(x, 3)
        + balanced_square_minimum(42 - 2 * x, 30)
        + balanced_square_minimum(24 + x, 45)
        for x in range(22)
        if 42 - 2 * x >= 0
    )
    # Type B: x is the excess on the unique high-medium pair.
    type_b = min(
        x**2
        + balanced_square_minimum(19 - x, 11)
        + balanced_square_minimum(14 - x, 11)
        + balanced_square_minimum(33 + x, 55)
        for x in range(15)
    )
    # Type C: high-low excess totals 24; low-low excess totals 42.
    type_c = balanced_square_minimum(24, 12) + balanced_square_minimum(42, 66)
    result = {"A": type_a, "B": type_b, "C": type_c}
    if result != {"A": 72, "B": 82, "C": 90}:
        raise C13VerificationError(f"unexpected E2 lower bounds: {result}")
    return result


def packing_minimum(multiplicity: int) -> int:
    quotient, remainder = divmod(3 * multiplicity, 10)
    return (10 - remainder) * comb(quotient, 2) + remainder * comb(
        quotient + 1, 2
    )


def max_triangles_for_edges(edge_count: int) -> int:
    """Kruskal-Katona/colex maximum number of triangles for this many edges."""
    if edge_count < 0:
        raise C13VerificationError("edge count cannot be negative")
    clique_size = 0
    while comb(clique_size + 1, 2) <= edge_count:
        clique_size += 1
    remainder = edge_count - comb(clique_size, 2)
    return comb(clique_size, 3) + comb(remainder, 2)


def _high_multiplicity_histograms(
    h_total: int, maximum_multiplicity: int, exceptional_above_six: int
) -> tuple[tuple[int, ...], ...]:
    # Entry i records z_(i+3); each contributes i+1 to H.
    width = maximum_multiplicity - 2
    results: list[tuple[int, ...]] = []

    def visit(index: int, remaining: int, counts: list[int], exceptional: int) -> None:
        if index == width:
            if remaining == 0:
                results.append(tuple(counts))
            return
        contribution = index + 1
        limit = remaining // contribution
        multiplicity = contribution + 2
        if multiplicity > 6:
            limit = min(limit, exceptional_above_six - exceptional)
        for count in range(limit + 1):
            visit(
                index + 1,
                remaining - count * contribution,
                counts + [count],
                exceptional + (count if multiplicity > 6 else 0),
            )

    visit(0, h_total, [], 0)
    return tuple(results)


def _z(counts: Sequence[int], multiplicity: int) -> int:
    index = multiplicity - 3
    return counts[index] if 0 <= index < len(counts) else 0


@lru_cache(maxsize=None)
def _intersection_solutions(
    s1: int, e2: int, q_value: int, minimum_j: int
) -> tuple[tuple[int, int, int, int, int, int], ...]:
    s2 = 399 + e2 // 2
    s3 = 114 + q_value
    results: list[tuple[int, int, int, int, int, int]] = []
    for n5 in range(s3 // 10 + 1):
        for n4 in range((s3 - 10 * n5) // 4 + 1):
            if 4 * n4 + 15 * n5 < minimum_j:
                continue
            n3 = s3 - 4 * n4 - 10 * n5
            n2 = s2 - 3 * s3 + 6 * n4 + 20 * n5
            n1 = s1 - 2 * s2 + 3 * s3 - 4 * n4 - 15 * n5
            n0 = 190 - n1 - n2 - n3 - n4 - n5
            values = (n0, n1, n2, n3, n4, n5)
            if min(values) >= 0:
                results.append(values)
    return tuple(results)


def _boundary_obstruction(
    type_label: str,
    e2: int,
    multiplicities: Sequence[int],
    intersections: Sequence[int],
) -> str | None:
    pair_collision_budget = (e2 - 66) // 2

    # A multiplicity-5 triple is a triangle of edges e_ij >= 2. Each such
    # edge spends at least one unit of sum C(e_ij,2).
    if _z(multiplicities, 5) > max_triangles_for_edges(pair_collision_budget):
        return "multiplicity-5 pair-excess triangle budget"

    # A multiplicity-6 triple is a triangle of edges e_ij >= 3. Each such
    # edge spends at least three collision units.
    if _z(multiplicities, 6) > max_triangles_for_edges(
        pair_collision_budget // 3
    ):
        return "multiplicity-6 pair-excess triangle budget"

    n4, n5 = intersections[4], intersections[5]
    if type_label == "A" and n5 == 0:
        z4 = _z(multiplicities, 4)
        # Each multiplicity-4 triple needs at least two x=4 block pairs. Two
        # such pairs cannot support four distinct triples; three cannot support
        # five. Equal 4-point intersections only have four constituent triples.
        if (z4 == 4 and n4 == 2) or (z4 >= 5 and n4 <= 3):
            return "multiplicity-4 intersection-support lemma"

    if (
        type_label == "B"
        and _z(multiplicities, 5) >= 3
        and n5 == 0
        and n4 == 5
    ):
        # Equality would put all three triples in all five 4-point
        # intersections. Those intersections are one common 4-set, whose
        # endpoint blocks create at least six x>=4 block pairs.
        return "type-B equality intersection-support lemma"

    if type_label == "C" and _z(multiplicities, 5):
        # E2=90 is the class-balanced minimum: twelve high-low edges have
        # weight 2 and the low-low energy is 42. Every extra low-low collision
        # costs two in E2. A multiplicity-5 triangle either uses the high point
        # and one such low-low edge, or is a triangle of low-low heavy edges.
        low_low_heavy_budget = (e2 - 90) // 2
        capacity = low_low_heavy_budget + max_triangles_for_edges(
            low_low_heavy_budget
        )
        if _z(multiplicities, 5) > capacity:
            return "type-C low-low pair-excess budget"

    return None


def verify_rigidity_arithmetic() -> dict[str, Any]:
    degree_types = {
        "A": {
            "c": 39,
            "degrees": (10, 10, 10) + (9,) * 10,
            "exceptional_above_six": 1,
            "h_lower": 11,
            "maximum_multiplicity": 10,
            "s1": 495,
        },
        "B": {
            "c": 40,
            "degrees": (11, 10) + (9,) * 11,
            "exceptional_above_six": 0,
            "h_lower": 12,
            "maximum_multiplicity": 6,
            "s1": 496,
        },
        "C": {
            "c": 42,
            "degrees": (12,) + (9,) * 12,
            "exceptional_above_six": 0,
            "h_lower": 13,
            "maximum_multiplicity": 6,
            "s1": 498,
        },
    }
    if {sum(entry["degrees"]) for entry in degree_types.values()} != {120}:
        raise C13VerificationError("degree-type total differs from 120")
    if any(min(entry["degrees"]) != 9 for entry in degree_types.values()):
        raise C13VerificationError("degree-type minimum differs from nine")

    polynomial = tuple(
        3 * comb(x, 3) - 2 * comb(x, 2) + x for x in range(6)
    )
    if polynomial != (0, 1, 0, 0, 4, 15):
        raise C13VerificationError("intersection polynomial mismatch")
    packing_values = {m: packing_minimum(m) for m in range(4, 11)}
    if packing_values != {4: 2, 5: 5, 6: 8, 7: 12, 8: 18, 9: 24, 10: 30}:
        raise C13VerificationError("residual packing table mismatch")
    # The link-excess argument gives 7m-21 <= 24 through a degree-9 point.
    if max(m for m in range(1, 10) if 7 * m - 21 <= 24) != 6:
        raise C13VerificationError("degree-nine multiplicity cap mismatch")

    e2_minima = e2_lower_bounds()
    raw_state_count = 0
    boundary_profiles: dict[tuple[str, int, tuple[int, ...]], set[str]] = {}
    survivors: list[dict[str, Any]] = []

    for type_label, entry in degree_types.items():
        h_lower = entry["h_lower"]
        for h_value in range(h_lower):
            histograms = _high_multiplicity_histograms(
                h_value,
                entry["maximum_multiplicity"],
                entry["exceptional_above_six"],
            )
            for multiplicities in histograms:
                q_value = sum(
                    count * contribution * (contribution + 1) // 2
                    for contribution, count in enumerate(multiplicities, start=1)
                )
                maximum = max(
                    (
                        multiplicity
                        for multiplicity in range(3, len(multiplicities) + 3)
                        if _z(multiplicities, multiplicity)
                    ),
                    default=2,
                )
                triple_e2_bound = (
                    66 + 3 * (maximum - 3) * (maximum - 4)
                    if maximum >= 4
                    else 66
                )
                e2_lower = max(e2_minima[type_label], triple_e2_bound)
                if e2_lower % 2:
                    e2_lower += 1
                minimum_j = 4 * packing_minimum(maximum) if maximum >= 4 else 0
                e2_upper = 3 * q_value + entry["c"]
                for e2 in range(e2_lower, e2_upper + 1, 2):
                    solutions = _intersection_solutions(
                        entry["s1"], e2, q_value, minimum_j
                    )
                    for intersections in solutions:
                        raw_state_count += 1
                        reason = _boundary_obstruction(
                            type_label, e2, multiplicities, intersections
                        )
                        profile = (type_label, h_value, tuple(multiplicities))
                        if reason is None:
                            survivors.append(
                                {
                                    "E2": e2,
                                    "H": h_value,
                                    "Q": q_value,
                                    "intersections": list(intersections),
                                    "multiplicities": list(multiplicities),
                                    "type": type_label,
                                }
                            )
                        else:
                            boundary_profiles.setdefault(profile, set()).add(reason)

    if survivors:
        raise C13VerificationError(
            f"low-H boundary enumeration retained {len(survivors)} survivor(s)"
        )
    per_type_profiles = Counter(profile[0] for profile in boundary_profiles)
    if raw_state_count != 49:
        raise C13VerificationError(
            f"boundary arithmetic state count differs from 49: {raw_state_count}"
        )
    if dict(per_type_profiles) != {"A": 5, "B": 2, "C": 3}:
        raise C13VerificationError(
            f"boundary profile roster differs from 5/2/3: {dict(per_type_profiles)}"
        )

    result_types: dict[str, Any] = {}
    for label, entry in degree_types.items():
        result_types[label] = {
            "E2_lower": e2_minima[label],
            "H_lower": entry["h_lower"],
            "S1": entry["s1"],
            "c": entry["c"],
            "degrees": list(entry["degrees"]),
            "singly_covered_lower": 172 + entry["h_lower"],
        }
    if [result_types[label]["singly_covered_lower"] for label in "ABC"] != [
        183,
        184,
        185,
    ]:
        raise C13VerificationError("singly-covered lower bounds mismatch")
    if any(
        (result_types[label]["singly_covered_lower"] + 19) // 20 < 10
        for label in "ABC"
    ):
        raise C13VerificationError("private-triple block conclusion mismatch")

    return {
        "arithmetic_state_count": raw_state_count,
        "boundary_profile_count": len(boundary_profiles),
        "boundary_profiles_by_type": dict(sorted(per_type_profiles.items())),
        "degree_nine_multiplicity_cap": 6,
        "intersection_polynomial": list(polynomial),
        "packing_minima": {str(key): value for key, value in packing_values.items()},
        "private_triples_in_some_block_lower": 10,
        "survivors": 0,
        "types": result_types,
    }


def verify_provenance(
    document: dict[str, Any], construction_report: dict[str, Any]
) -> dict[str, Any]:
    require_exact_keys(
        document,
        {
            "artifact_id",
            "blocked_promotions",
            "construction_identity",
            "evidence_status",
            "novelty_search",
            "schema",
            "source",
        },
        "provenance document",
    )
    if document["schema"] != "c13-covering-provenance-v1":
        raise C13VerificationError("unexpected provenance schema")
    if document["artifact_id"] != "C13-COV-01":
        raise C13VerificationError("provenance artifact identifier mismatch")
    blocked = document["blocked_promotions"]
    if not isinstance(blocked, list) or tuple(blocked) != EXPECTED_BLOCKED_PROMOTIONS:
        raise C13VerificationError("blocked-promotion roster mismatch")

    construction_identity = document["construction_identity"]
    if not isinstance(construction_identity, dict):
        raise C13VerificationError("construction_identity must be an object")
    require_exact_keys(
        construction_identity, {"bytes", "serialization", "sha256"}, "construction_identity"
    )
    if require_plain_int(construction_identity["bytes"], "construction bytes") != 277:
        raise C13VerificationError("normalized construction byte count mismatch")
    if (
        validate_sha256(construction_identity["sha256"], "construction sha256")
        != construction_report["normalized_blocks_sha256"]
    ):
        raise C13VerificationError("provenance construction hash mismatch")

    source = document["source"]
    if not isinstance(source, dict):
        raise C13VerificationError("source provenance must be an object")
    require_exact_keys(
        source,
        {
            "database",
            "method",
            "normalized_block_inventory",
            "reported_bound",
            "retrieved_on",
            "retrieved_page_observation",
            "url",
            "zenodo_index",
        },
        "source provenance",
    )
    if source["reported_bound"] != "20 <= C(13,6,3) <= 21":
        raise C13VerificationError("source bound was altered")
    if source["url"] != (
        "https://ljcr.dmgordon.org/cover/show_cover.php?k=6&t=3&v=13"
    ):
        raise C13VerificationError("source URL was altered")
    source_identity = source["normalized_block_inventory"]
    if not isinstance(source_identity, dict):
        raise C13VerificationError("normalized_block_inventory must be an object")
    require_exact_keys(
        source_identity, {"bytes", "serialization", "sha256"}, "normalized source identity"
    )
    if require_plain_int(source_identity["bytes"], "source bytes") != 291:
        raise C13VerificationError("normalized source byte count mismatch")
    if (
        validate_sha256(source_identity["sha256"], "source sha256")
        != construction_report["source_normalized_blocks_sha256"]
    ):
        raise C13VerificationError("provenance source hash mismatch")

    page = source["retrieved_page_observation"]
    if not isinstance(page, dict):
        raise C13VerificationError("retrieved_page_observation must be an object")
    require_exact_keys(page, {"bytes", "sha256", "warning"}, "page observation")
    if require_plain_int(page["bytes"], "retrieved page bytes") != 588:
        raise C13VerificationError("retrieved page byte count mismatch")
    validate_sha256(page["sha256"], "retrieved page sha256")

    zenodo = source["zenodo_index"]
    if not isinstance(zenodo, dict):
        raise C13VerificationError("zenodo_index must be an object")
    require_exact_keys(
        zenodo,
        {
            "coverdata_bytes",
            "coverdata_md5_from_record",
            "coverdata_sha256_observed",
            "entry",
            "record_id",
            "version",
        },
        "zenodo_index",
    )
    if zenodo["record_id"] != 19735294 or zenodo["version"] != "1.2":
        raise C13VerificationError("Zenodo index identity mismatch")
    if zenodo["coverdata_bytes"] != 8319503:
        raise C13VerificationError("Zenodo coverdata byte count mismatch")
    validate_sha256(zenodo["coverdata_sha256_observed"], "coverdata sha256")
    if zenodo["entry"] != {"key": "C(13,6,3)", "low_bd": 20, "size": 21}:
        raise C13VerificationError("Zenodo C(13,6,3) entry mismatch")

    evidence = document["evidence_status"]
    expected_evidence = {
        "construction": "independently_reproduced",
        "rigidity_arithmetic": "mechanically_replayed",
        "rigidity_proof": "hand_checked",
        "unresolved_covering_number": "open_in_checked_public_record",
    }
    if evidence != expected_evidence:
        raise C13VerificationError("evidence-status vocabulary mismatch")
    novelty = document["novelty_search"]
    if not isinstance(novelty, dict):
        raise C13VerificationError("novelty_search must be an object")
    require_exact_keys(
        novelty, {"checked_through", "result", "scope", "warning"}, "novelty_search"
    )
    if novelty["result"] != "no matching public record located":
        raise C13VerificationError("novelty result was promoted or altered")

    return {
        "blocked_promotions": len(blocked),
        "construction_status": evidence["construction"],
        "novelty_status": novelty["result"],
        "rigidity_arithmetic_status": evidence["rigidity_arithmetic"],
        "rigidity_proof_status": evidence["rigidity_proof"],
        "source_record": "Zenodo 19735294 v1.2 / LJCR-C(13,6,3)-21",
    }


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def verify_all(construction_path: Path, provenance_path: Path) -> dict[str, Any]:
    construction, construction_raw = load_json(construction_path)
    provenance, provenance_raw = load_json(provenance_path)
    construction_report = verify_construction(construction)
    rigidity_report = verify_rigidity_arithmetic()
    provenance_report = verify_provenance(provenance, construction_report)
    return {
        "artifact_id": "C13-COV-01",
        "construction": construction_report,
        "input_sha256": {
            "construction_json": hashlib.sha256(construction_raw).hexdigest(),
            "provenance_json": hashlib.sha256(provenance_raw).hexdigest(),
        },
        "provenance": provenance_report,
        "rigidity": rigidity_report,
        "status": "PASS",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--construction", type=Path, default=DEFAULT_CONSTRUCTION)
    parser.add_argument("--provenance", type=Path, default=DEFAULT_PROVENANCE)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = verify_all(args.construction, args.provenance)
        expected_receipt = args.receipt.read_bytes()
        observed_receipt = canonical_json(report)
        if observed_receipt != expected_receipt:
            raise C13VerificationError("tracked verification receipt mismatch")
    except (OSError, C13VerificationError) as exc:
        print(f"C13-COVERING-VERIFY: FAIL: {exc}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write(observed_receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
