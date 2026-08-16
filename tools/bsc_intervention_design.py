#!/usr/bin/env python3
"""Check finite deterministic intervention-identifiability problems exactly.

The executable accepts only a closed, canonical JSON dialect.  It verifies
identifiability twice: once by grouping states into joint-report fibers and
once by covering every target-separated state pair.  It then enumerates every
intervention family, finds all minimum-cost identifying families over Q, and
computes declared tolerance-based target oscillations over exact finite
metrics.

This is a bounded finite-model checker.  It does not establish causal-model
validity, empirical adequacy, novelty, or claims outside the supplied model.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Any, Iterable


INPUT_SCHEMA = "bsc-intervention-design-input/1"
REPORT_SCHEMA = "bsc-intervention-design-report/1"
MODEL_KIND = "finite_deterministic"
ARITHMETIC = "exact_rational"
SERIALIZATION = "UTF-8 JSON, two-space indentation, sorted keys, LF terminator"
MAX_STATES = 256
MAX_INTERVENTIONS = 16
MAX_METRIC_POINTS = 32
MAX_OSCILLATION_QUERIES = 256
MAX_EXHAUSTIVE_OPERATIONS = 10_000_000
MAX_METRIC_VALIDATION_OPERATIONS = 1_000_000
MAX_REPORTED_MINIMIZERS = 4_096
MAX_INPUT_BYTES = 2_000_000
MAX_REPORT_BYTES = 4_000_000
MAX_CHECKER_BYTES = 1_000_000
MAX_JSON_DEPTH = 32
MAX_JSON_ITEMS = 200_000
MAX_STRING_CHARS = 4_096
MAX_IDENTIFIER_CHARS = 128
MAX_INTEGER_DIGITS = 18
MAX_RATIONAL_COMPONENT = 1_000_000_000_000
MAX_DERIVED_RATIONAL_BITS = 1_024
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")


class DesignError(ValueError):
    """Raised when an input or a derived exact obligation is invalid."""


@dataclass(frozen=True)
class FiniteMetric:
    points: tuple[str, ...]
    distances: dict[tuple[str, str], Fraction]

    def distance(self, left: str, right: str) -> Fraction:
        return self.distances[(left, right)]


@dataclass(frozen=True)
class Intervention:
    identifier: str
    cost: Fraction
    tolerance: Fraction
    reports: dict[str, str]
    metric: FiniteMetric


@dataclass(frozen=True)
class Problem:
    problem_id: str
    states: tuple[str, ...]
    target_values: dict[str, str]
    target_metric: FiniteMetric
    interventions: tuple[Intervention, ...]
    oscillation_queries: tuple[tuple[str, ...], ...]

    @property
    def intervention_by_id(self) -> dict[str, Intervention]:
        return {item.identifier: item for item in self.interventions}


def canonical_json_bytes(value: Any) -> bytes:
    """Return the single admitted byte encoding for an input or report."""

    try:
        return (
            json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
    except (RecursionError, UnicodeError, ValueError, OverflowError):
        raise DesignError("value cannot be serialized within fixed limits") from None


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reject_float(token: str) -> None:
    raise DesignError("floating-point JSON numbers are forbidden")


def reject_constant(token: str) -> None:
    raise DesignError(f"nonfinite JSON constant is forbidden: {token}")


def bounded_integer(token: str) -> int:
    if len(token.removeprefix("-")) > MAX_INTEGER_DIGITS:
        raise DesignError(
            f"JSON integer exceeds the {MAX_INTEGER_DIGITS}-digit bound"
        )
    return int(token)


def unique_mapping(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DesignError("duplicate JSON key")
        result[key] = value
    return result


def has_surrogate(value: str) -> bool:
    return any(0xD800 <= ord(character) <= 0xDFFF for character in value)


def validate_json_shape(value: Any, label: str) -> None:
    pending: list[tuple[Any, int]] = [(value, 0)]
    item_count = 0
    while pending:
        item, depth = pending.pop()
        item_count += 1
        if item_count > MAX_JSON_ITEMS:
            raise DesignError(
                f"{label} exceeds the {MAX_JSON_ITEMS}-item structural bound"
            )
        if depth > MAX_JSON_DEPTH:
            raise DesignError(
                f"{label} exceeds the nesting-depth bound of {MAX_JSON_DEPTH}"
            )
        if isinstance(item, str):
            if len(item) > MAX_STRING_CHARS:
                raise DesignError(
                    f"{label} contains a string longer than {MAX_STRING_CHARS} characters"
                )
            if has_surrogate(item):
                raise DesignError(f"{label} contains a forbidden Unicode surrogate")
        elif isinstance(item, dict):
            for key, child in item.items():
                pending.append((key, depth + 1))
                pending.append((child, depth + 1))
        elif isinstance(item, list):
            pending.extend((child, depth + 1) for child in item)


def read_bounded(path: Path, maximum: int, label: str) -> bytes:
    try:
        with path.open("rb") as stream:
            data = stream.read(maximum + 1)
    except OSError:
        raise DesignError(f"cannot read {label}") from None
    if len(data) > maximum:
        raise DesignError(f"{label} exceeds the {maximum}-byte bound")
    return data


def load_canonical_json_bytes(data: bytes, label: str = "input") -> Any:
    if len(data) > MAX_INPUT_BYTES:
        raise DesignError(f"{label} exceeds the {MAX_INPUT_BYTES}-byte bound")
    if data.startswith(b"\xef\xbb\xbf"):
        raise DesignError(f"{label} contains a forbidden UTF-8 BOM")
    if b"\r" in data:
        raise DesignError(f"{label} must use LF line endings")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise DesignError(f"{label} is not strict UTF-8") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=unique_mapping,
            parse_int=bounded_integer,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except DesignError:
        raise
    except json.JSONDecodeError as exc:
        raise DesignError(
            f"{label} is invalid JSON at line {exc.lineno}, column {exc.colno}"
        ) from None
    except (RecursionError, ValueError, OverflowError):
        raise DesignError(f"{label} exceeds the JSON parser limits") from None
    validate_json_shape(value, label)
    if data != canonical_json_bytes(value):
        raise DesignError(f"{label} is not canonical JSON")
    return value


def load_canonical_json(path: Path, label: str = "input") -> tuple[bytes, Any]:
    data = read_bounded(path, MAX_INPUT_BYTES, label)
    return data, load_canonical_json_bytes(data, label)


def closed_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise DesignError(f"{label} must be an object")
    actual = set(value)
    if actual != keys:
        raise DesignError(
            f"{label} keys mismatch: missing_count={len(keys - actual)}, "
            f"extra_count={len(actual - keys)}"
        )
    return value


def identifier(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) > MAX_IDENTIFIER_CHARS
        or not IDENTIFIER.fullmatch(value)
    ):
        raise DesignError(f"{label} must be a nonempty portable identifier")
    return value


def string_list(
    value: Any,
    label: str,
    *,
    require_sorted: bool = True,
    maximum: int | None = None,
) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise DesignError(f"{label} must be a nonempty array")
    result = tuple(identifier(item, f"{label}[{index}]") for index, item in enumerate(value))
    if len(set(result)) != len(result):
        raise DesignError(f"{label} contains a duplicate identifier")
    if require_sorted and result != tuple(sorted(result)):
        raise DesignError(f"{label} must be strictly lexicographically sorted")
    if maximum is not None and len(result) > maximum:
        raise DesignError(f"{label} exceeds the exact-checker bound of {maximum}")
    return result


def integer(value: Any, label: str) -> int:
    if type(value) is not int:
        raise DesignError(f"{label} must be an integer")
    if abs(value) > MAX_RATIONAL_COMPONENT:
        raise DesignError(
            f"{label} exceeds the absolute bound of {MAX_RATIONAL_COMPONENT}"
        )
    return value


def rational(value: Any, label: str) -> Fraction:
    item = closed_object(value, {"denominator", "numerator"}, label)
    numerator = integer(item["numerator"], f"{label}.numerator")
    denominator = integer(item["denominator"], f"{label}.denominator")
    if denominator <= 0:
        raise DesignError(f"{label} denominator must be positive")
    if math.gcd(abs(numerator), denominator) != 1:
        raise DesignError(f"{label} must be reduced")
    if numerator == 0 and denominator != 1:
        raise DesignError(f"{label} has a noncanonical zero")
    return Fraction(numerator, denominator)


def rational_json(value: Fraction) -> dict[str, int]:
    return {"denominator": value.denominator, "numerator": value.numerator}


def exact_state_map(
    value: Any,
    states: tuple[str, ...],
    codomain: set[str],
    label: str,
) -> dict[str, str]:
    if not isinstance(value, dict):
        raise DesignError(f"{label} must be an object")
    if set(value) != set(states):
        raise DesignError(
            f"{label} state coverage mismatch: "
            f"missing_count={len(set(states) - set(value))}, "
            f"extra_count={len(set(value) - set(states))}"
        )
    result: dict[str, str] = {}
    for state in states:
        point = value[state]
        if not isinstance(point, str) or point not in codomain:
            raise DesignError(f"{label}.{state} is outside the declared metric space")
        result[state] = point
    return result


def parse_metric(value: Any, label: str) -> FiniteMetric:
    item = closed_object(value, {"distances", "points"}, label)
    points = string_list(
        item["points"],
        f"{label}.points",
        maximum=MAX_METRIC_POINTS,
    )
    entries = item["distances"]
    expected_pairs = tuple(product(points, repeat=2))
    if not isinstance(entries, list) or len(entries) != len(expected_pairs):
        raise DesignError(
            f"{label}.distances must cover all {len(expected_pairs)} ordered pairs"
        )
    distances: dict[tuple[str, str], Fraction] = {}
    for index, (entry, expected_pair) in enumerate(zip(entries, expected_pairs)):
        record = closed_object(
            entry,
            {"distance", "left", "right"},
            f"{label}.distances[{index}]",
        )
        pair = (record["left"], record["right"])
        if pair != expected_pair:
            raise DesignError(
                f"{label}.distances[{index}] must be ordered pair {expected_pair}"
            )
        distance = rational(record["distance"], f"{label}.distances[{index}].distance")
        if distance < 0:
            raise DesignError(f"{label} contains a negative distance")
        distances[pair] = distance

    for left in points:
        for right in points:
            distance = distances[(left, right)]
            if left == right and distance != 0:
                raise DesignError(f"{label} has a nonzero diagonal distance")
            if left != right and distance <= 0:
                raise DesignError(f"{label} does not separate {left} and {right}")
            if distance != distances[(right, left)]:
                raise DesignError(f"{label} is not symmetric at {left}, {right}")
    for left in points:
        for middle in points:
            for right in points:
                if distances[(left, right)] > (
                    distances[(left, middle)] + distances[(middle, right)]
                ):
                    raise DesignError(
                        f"{label} violates the triangle inequality at "
                        f"{left}, {middle}, {right}"
                    )
    return FiniteMetric(points=points, distances=distances)


def family_order_key(family: tuple[str, ...]) -> tuple[int, tuple[str, ...]]:
    return len(family), family


def metric_validation_cost(value: Any) -> int:
    if not isinstance(value, dict):
        return 0
    points = value.get("points")
    if not isinstance(points, list):
        return 0
    count = len(points)
    return count * count + count * count * count


def ensure_metric_validation_budget(
    target: dict[str, Any], interventions: list[Any]
) -> None:
    metrics: list[Any] = [target.get("metric")]
    metrics.extend(
        item.get("metric") for item in interventions if isinstance(item, dict)
    )
    estimate = sum(metric_validation_cost(metric) for metric in metrics)
    if estimate > MAX_METRIC_VALIDATION_OPERATIONS:
        raise DesignError(
            "metric validation exceeds the fixed operation bound: "
            f"estimate={estimate}, bound={MAX_METRIC_VALIDATION_OPERATIONS}"
        )


def parse_problem(value: Any) -> Problem:
    validate_json_shape(value, "input")
    root = closed_object(
        value,
        {
            "arithmetic",
            "interventions",
            "model_kind",
            "oscillation_queries",
            "problem_id",
            "schema",
            "states",
            "target",
        },
        "input",
    )
    if root["schema"] != INPUT_SCHEMA:
        raise DesignError("input.schema mismatch")
    if root["model_kind"] != MODEL_KIND:
        raise DesignError("input.model_kind must be finite_deterministic")
    if root["arithmetic"] != ARITHMETIC:
        raise DesignError("input.arithmetic must be exact_rational")
    problem_id = identifier(root["problem_id"], "input.problem_id")
    states = string_list(root["states"], "input.states", maximum=MAX_STATES)

    target = closed_object(root["target"], {"metric", "values"}, "input.target")
    raw_interventions = root["interventions"]
    if not isinstance(raw_interventions, list) or not raw_interventions:
        raise DesignError("input.interventions must be a nonempty array")
    if len(raw_interventions) > MAX_INTERVENTIONS:
        raise DesignError(
            f"input.interventions exceeds the exhaustive bound of {MAX_INTERVENTIONS}"
        )
    ensure_metric_validation_budget(target, raw_interventions)

    target_metric = parse_metric(target["metric"], "input.target.metric")
    target_values = exact_state_map(
        target["values"], states, set(target_metric.points), "input.target.values"
    )

    interventions: list[Intervention] = []
    for index, raw in enumerate(raw_interventions):
        label = f"input.interventions[{index}]"
        item = closed_object(
            raw,
            {"cost", "id", "metric", "reports", "tolerance"},
            label,
        )
        intervention_id = identifier(item["id"], f"{label}.id")
        metric = parse_metric(item["metric"], f"{label}.metric")
        cost = rational(item["cost"], f"{label}.cost")
        tolerance = rational(item["tolerance"], f"{label}.tolerance")
        if cost < 0:
            raise DesignError(f"{label}.cost must be nonnegative")
        if tolerance < 0:
            raise DesignError(f"{label}.tolerance must be nonnegative")
        reports = exact_state_map(
            item["reports"], states, set(metric.points), f"{label}.reports"
        )
        interventions.append(
            Intervention(
                identifier=intervention_id,
                cost=cost,
                tolerance=tolerance,
                reports=reports,
                metric=metric,
            )
        )
    intervention_ids = tuple(item.identifier for item in interventions)
    if len(set(intervention_ids)) != len(intervention_ids):
        raise DesignError("input.interventions contains a duplicate id")
    if intervention_ids != tuple(sorted(intervention_ids)):
        raise DesignError("input.interventions must be sorted by id")

    raw_queries = root["oscillation_queries"]
    if not isinstance(raw_queries, list) or not raw_queries:
        raise DesignError("input.oscillation_queries must be a nonempty array")
    if len(raw_queries) > MAX_OSCILLATION_QUERIES:
        raise DesignError(
            "input.oscillation_queries exceeds the fixed bound of "
            f"{MAX_OSCILLATION_QUERIES}"
        )
    queries: list[tuple[str, ...]] = []
    known = set(intervention_ids)
    for index, raw_family in enumerate(raw_queries):
        if not isinstance(raw_family, list):
            raise DesignError(f"input.oscillation_queries[{index}] must be an array")
        family = tuple(
            identifier(item, f"input.oscillation_queries[{index}][{position}]")
            for position, item in enumerate(raw_family)
        )
        if len(set(family)) != len(family):
            raise DesignError(f"input.oscillation_queries[{index}] has a duplicate id")
        if family != tuple(sorted(family)):
            raise DesignError(f"input.oscillation_queries[{index}] must be sorted")
        unknown = sorted(set(family) - known)
        if unknown:
            raise DesignError(
                f"input.oscillation_queries[{index}] has unknown ids: {unknown}"
            )
        queries.append(family)
    if len(set(queries)) != len(queries):
        raise DesignError("input.oscillation_queries contains a duplicate family")
    if tuple(queries) != tuple(sorted(queries, key=family_order_key)):
        raise DesignError(
            "input.oscillation_queries must be ordered by cardinality then lexicographically"
        )

    problem = Problem(
        problem_id=problem_id,
        states=states,
        target_values=target_values,
        target_metric=target_metric,
        interventions=tuple(interventions),
        oscillation_queries=tuple(queries),
    )
    ensure_exhaustive_budget(problem)
    ensure_full_intervention_coverage(problem)
    return problem


def unordered_state_pairs(states: tuple[str, ...]) -> Iterable[tuple[str, str]]:
    return combinations(states, 2)


def target_separated_pairs(problem: Problem) -> tuple[tuple[str, str], ...]:
    return tuple(
        (left, right)
        for left, right in unordered_state_pairs(problem.states)
        if problem.target_values[left] != problem.target_values[right]
    )


def fiber_identifies(problem: Problem, family: tuple[str, ...]) -> bool:
    """Test whether the target is constant on every joint-report fiber."""

    by_id = problem.intervention_by_id
    fibers: dict[tuple[str, ...], str] = {}
    for state in problem.states:
        signature = tuple(by_id[item].reports[state] for item in family)
        target = problem.target_values[state]
        if signature in fibers and fibers[signature] != target:
            return False
        fibers[signature] = target
    return True


def pair_cover_identifies(problem: Problem, family: tuple[str, ...]) -> bool:
    """Test whether reports cover every target-separated state pair."""

    by_id = problem.intervention_by_id
    required = target_separated_pairs(problem)
    for left, right in required:
        if not any(
            by_id[item].reports[left] != by_id[item].reports[right] for item in family
        ):
            return False
    return True


def all_families(problem: Problem) -> tuple[tuple[str, ...], ...]:
    identifiers = tuple(item.identifier for item in problem.interventions)
    return tuple(
        family
        for size in range(len(identifiers) + 1)
        for family in combinations(identifiers, size)
    )


def ensure_exhaustive_budget(problem: Problem) -> None:
    """Reject inputs whose mandatory all-subset audit exceeds the fixed bound."""

    intervention_count = len(problem.interventions)
    family_count = 1 << intervention_count
    per_family = max(1, intervention_count) * (
        len(problem.states) + len(target_separated_pairs(problem))
    )
    estimate = family_count * max(1, per_family)
    if estimate > MAX_EXHAUSTIVE_OPERATIONS:
        raise DesignError(
            "exhaustive audit exceeds the fixed operation bound: "
            f"estimate={estimate}, bound={MAX_EXHAUSTIVE_OPERATIONS}"
        )


def ensure_full_intervention_coverage(problem: Problem) -> None:
    full = tuple(item.identifier for item in problem.interventions)
    uncovered = []
    by_id = problem.intervention_by_id
    for left, right in target_separated_pairs(problem):
        if not any(
            by_id[item].reports[left] != by_id[item].reports[right] for item in full
        ):
            uncovered.append((left, right))
    if uncovered:
        raise DesignError(
            f"target-separated pairs are uncovered: count={len(uncovered)}"
        )


def family_cost(problem: Problem, family: tuple[str, ...]) -> Fraction:
    by_id = problem.intervention_by_id
    total = Fraction(0)
    for item in family:
        total += by_id[item].cost
        if (
            total.numerator.bit_length() > MAX_DERIVED_RATIONAL_BITS
            or total.denominator.bit_length() > MAX_DERIVED_RATIONAL_BITS
        ):
            raise DesignError(
                "derived family cost exceeds the exact-arithmetic operand bound"
            )
    return total


def exact_minimum_families(
    problem: Problem,
) -> tuple[Fraction, tuple[tuple[str, ...], ...], int]:
    minimum: Fraction | None = None
    minimizers: list[tuple[str, ...]] = []
    minimizer_overflow = False
    agreement_count = 0
    for family in all_families(problem):
        by_fiber = fiber_identifies(problem, family)
        by_cover = pair_cover_identifies(problem, family)
        if by_fiber != by_cover:
            raise DesignError(
                f"identifiability cross-checks disagree for family {family}"
            )
        agreement_count += 1
        if not by_fiber:
            continue
        cost = family_cost(problem, family)
        if minimum is None or cost < minimum:
            minimum = cost
            minimizers = [family]
            minimizer_overflow = False
        elif cost == minimum:
            if len(minimizers) < MAX_REPORTED_MINIMIZERS:
                minimizers.append(family)
            else:
                minimizer_overflow = True
    if minimum is None:
        raise DesignError("no identifying intervention family exists")
    if minimizer_overflow:
        raise DesignError(
            "minimum-family report exceeds the fixed bound of "
            f"{MAX_REPORTED_MINIMIZERS} families"
        )
    ordered = tuple(sorted(minimizers, key=family_order_key))
    return minimum, ordered, agreement_count


def approximate_oscillation(
    problem: Problem, family: tuple[str, ...]
) -> tuple[Fraction, tuple[tuple[str, str], ...], int]:
    by_id = problem.intervention_by_id
    maximum = Fraction(0)
    witnesses: list[tuple[str, str]] = []
    admissible_pair_count = 0
    for left, right in unordered_state_pairs(problem.states):
        close = all(
            by_id[item].metric.distance(
                by_id[item].reports[left], by_id[item].reports[right]
            )
            <= by_id[item].tolerance
            for item in family
        )
        if not close:
            continue
        admissible_pair_count += 1
        distance = problem.target_metric.distance(
            problem.target_values[left], problem.target_values[right]
        )
        if distance > maximum:
            maximum = distance
            witnesses = [(left, right)]
        elif distance == maximum and distance > 0:
            witnesses.append((left, right))
    return maximum, tuple(witnesses), admissible_pair_count


def build_report(input_bytes: bytes, value: Any, checker_path: Path | None = None) -> dict[str, Any]:
    if len(input_bytes) > MAX_INPUT_BYTES:
        raise DesignError(f"input exceeds the {MAX_INPUT_BYTES}-byte bound")
    problem = parse_problem(value)
    minimum, minimizers, checked = exact_minimum_families(problem)
    checker = checker_path or Path(__file__)
    oscillations = []
    for family in problem.oscillation_queries:
        value_q, witnesses, admissible_count = approximate_oscillation(problem, family)
        oscillations.append(
            {
                "admissible_nonidentical_pair_count": admissible_count,
                "family": list(family),
                "maximum_target_oscillation": rational_json(value_q),
                "zero_target_ambiguity": value_q == 0,
                "witness_pairs": [list(pair) for pair in witnesses],
            }
        )
    target_pairs = target_separated_pairs(problem)
    report = {
        "authority": {
            "does_not_establish": [
                "causal-model validity",
                "empirical adequacy",
                "external or counterfactual identification",
                "novelty or priority",
                "stochastic or continuous-model identification",
            ],
            "establishes": [
                "exact finite deterministic identifiability for the supplied model",
                "exact minimum rational intervention cost within the supplied family",
                "exact tolerance-based oscillation for the declared queries",
            ],
            "status": "exact_finite_conditional_result",
        },
        "exact_identifiability": {
            "all_minimum_cost_families": [list(family) for family in minimizers],
            "full_family_covers_every_target_separated_pair": True,
            "cross_check_methods": [
                "joint_report_fiber_constancy",
                "target_separated_pair_cover",
            ],
            "cross_check_methods_agree": True,
            "intervention_family_count_checked": checked,
            "minimum_cost": rational_json(minimum),
            "selected_family": list(minimizers[0]),
            "selection_rule": (
                "minimum exact rational cost; enumerate all ties; select minimum "
                "cardinality then lexicographic identifiers"
            ),
            "target_separated_pair_count": len(target_pairs),
            "target_separated_pairs": [list(pair) for pair in target_pairs],
        },
        "finite_problem": {
            "intervention_count": len(problem.interventions),
            "model_kind": MODEL_KIND,
            "problem_id": problem.problem_id,
            "state_count": len(problem.states),
        },
        "oscillation_queries": oscillations,
        "schema": REPORT_SCHEMA,
        "source_binding": {
            "checker_sha256": sha256(
                read_bounded(checker, MAX_CHECKER_BYTES, "checker source")
            ),
            "input_sha256": sha256(input_bytes),
            "serialization": SERIALIZATION,
        },
    }
    if len(canonical_json_bytes(report)) > MAX_REPORT_BYTES:
        raise DesignError(f"report exceeds the {MAX_REPORT_BYTES}-byte bound")
    return report


def analyze_path(path: Path, checker_path: Path | None = None) -> dict[str, Any]:
    input_bytes, value = load_canonical_json(path, "input")
    return build_report(input_bytes, value, checker_path)


def format_fraction(value: dict[str, int]) -> str:
    if value["denominator"] == 1:
        return str(value["numerator"])
    return f"{value['numerator']}/{value['denominator']}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="canonical finite design JSON")
    parser.add_argument(
        "--json", action="store_true", help="write the canonical exact report to stdout"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = analyze_path(args.input)
    except DesignError as exc:
        print(f"BSC-INTERVENTION-DESIGN: FAIL: {exc}", file=sys.stderr)
        return 1
    except OSError:
        print(
            "BSC-INTERVENTION-DESIGN: FAIL: cannot access a required file",
            file=sys.stderr,
        )
        return 1
    if args.json:
        sys.stdout.buffer.write(canonical_json_bytes(report))
    else:
        exact = report["exact_identifiability"]
        selected = ",".join(exact["selected_family"]) or "<empty>"
        print(
            "BSC-INTERVENTION-DESIGN: PASS: "
            f"states={report['finite_problem']['state_count']} "
            f"interventions={report['finite_problem']['intervention_count']} "
            f"minimum_cost={format_fraction(exact['minimum_cost'])} "
            f"minimum_families={len(exact['all_minimum_cost_families'])} "
            f"selected={selected}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
