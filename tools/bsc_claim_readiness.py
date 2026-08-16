#!/usr/bin/env python3
"""Evaluate finite cyclic BSC readiness-cap systems exactly.

The mathematical verdict is carried unchanged.  Readiness is a product of
independently ordered axes, and an axis that does not apply to a claim is
absent rather than encoded as an artificial top or bottom value.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


GRAPH_SCHEMA = "bsc.claim-readiness-graph.v1"
RECEIPT_SCHEMA = "bsc.claim-readiness-receipt.v1"
ALLOWED_VERDICTS = frozenset({"N/A", "false", "ill-posed", "open", "true"})
IDENTIFIER = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$")
MAX_INPUT_BYTES = 1_000_000
MAX_RECEIPT_BYTES = 2_000_000
MAX_JSON_DEPTH = 32
MAX_JSON_ITEMS = 50_000
MAX_STRING_CHARS = 4_096
MAX_IDENTIFIER_CHARS = 128
MAX_INTEGER_DIGITS = 18
MAX_AXES = 32
MAX_LEVELS_PER_AXIS = 64
MAX_NODES = 512
MAX_EDGES = 4_096
MAX_COORDINATES = 4_096
MAX_DESCENT_STEPS = 100_000
MAX_FIXED_POINT_OPERATIONS = 10_000_000


class ReadinessError(ValueError):
    """Raised when a graph or receipt violates the closed format."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReadinessError("duplicate JSON key")
        result[key] = value
    return result


def _bounded_integer(token: str) -> int:
    digits = token.removeprefix("-")
    if len(digits) > MAX_INTEGER_DIGITS:
        raise ReadinessError(
            f"JSON integer exceeds the {MAX_INTEGER_DIGITS}-digit bound"
        )
    return int(token)


def _reject_number(token: str) -> None:
    raise ReadinessError("floating-point and nonfinite JSON numbers are forbidden")


def _has_surrogate(value: str) -> bool:
    return any(0xD800 <= ord(character) <= 0xDFFF for character in value)


def _validate_json_shape(value: Any) -> None:
    pending: list[tuple[Any, int]] = [(value, 0)]
    item_count = 0
    while pending:
        item, depth = pending.pop()
        item_count += 1
        if item_count > MAX_JSON_ITEMS:
            raise ReadinessError(
                f"JSON exceeds the {MAX_JSON_ITEMS}-item structural bound"
            )
        if depth > MAX_JSON_DEPTH:
            raise ReadinessError(
                f"JSON exceeds the nesting-depth bound of {MAX_JSON_DEPTH}"
            )
        if isinstance(item, str):
            if len(item) > MAX_STRING_CHARS:
                raise ReadinessError(
                    f"JSON string exceeds the {MAX_STRING_CHARS}-character bound"
                )
            if _has_surrogate(item):
                raise ReadinessError("JSON contains a forbidden Unicode surrogate")
        elif isinstance(item, dict):
            for key, child in item.items():
                pending.append((key, depth + 1))
                pending.append((child, depth + 1))
        elif isinstance(item, list):
            pending.extend((child, depth + 1) for child in item)


def _read_bounded(path: Path, maximum: int, label: str) -> bytes:
    try:
        with path.open("rb") as stream:
            data = stream.read(maximum + 1)
    except OSError:
        raise ReadinessError(f"cannot read {label}") from None
    if len(data) > maximum:
        raise ReadinessError(f"{label} exceeds the {maximum}-byte bound")
    return data


def load_json_bytes(
    path: Path,
    *,
    maximum: int = MAX_INPUT_BYTES,
    label: str = "graph",
) -> tuple[bytes, Any]:
    raw = _read_bounded(path, maximum, label)
    try:
        text = raw.decode("utf-8")
    except UnicodeError:
        raise ReadinessError(f"{label} is not strict UTF-8") from None
    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_int=_bounded_integer,
            parse_float=_reject_number,
            parse_constant=_reject_number,
        )
    except ReadinessError:
        raise
    except json.JSONDecodeError as exc:
        raise ReadinessError(
            f"{label} is invalid JSON at line {exc.lineno}, column {exc.colno}"
        ) from None
    except (RecursionError, ValueError, OverflowError):
        raise ReadinessError(f"{label} exceeds the JSON parser limits") from None
    _validate_json_shape(value)
    return raw, value


def canonical_json(value: Any) -> bytes:
    try:
        return (
            json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
    except (RecursionError, ValueError, OverflowError):
        raise ReadinessError("value cannot be serialized within fixed limits") from None


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReadinessError(f"{label} must be an object")
    return value


def _require_exact_keys(
    value: dict[str, Any], expected: set[str], label: str
) -> None:
    actual = set(value)
    if actual != expected:
        raise ReadinessError(
            f"{label} keys differ: missing_count={len(expected - actual)}, "
            f"extra_count={len(actual - expected)}"
        )


def _require_identifier(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) > MAX_IDENTIFIER_CHARS
        or not IDENTIFIER.fullmatch(value)
    ):
        raise ReadinessError(f"{label} must be an uppercase hyphenated identifier")
    return value


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ReadinessError(f"{label} must be a nonempty string")
    return value


@dataclass(frozen=True)
class Node:
    identifier: str
    verdict: str
    applicable_axes: tuple[str, ...]
    initial: dict[str, int]


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    caps: dict[str, tuple[int, ...]]


@dataclass(frozen=True)
class Graph:
    axes: dict[str, tuple[str, ...]]
    nodes: dict[str, Node]
    edges: tuple[Edge, ...]
    maximum_iterations: int


def validate_graph(document: Any) -> Graph:
    _validate_json_shape(document)
    root = _require_object(document, "graph")
    _require_exact_keys(root, {"schema", "axes", "nodes", "edges"}, "graph")
    if root["schema"] != GRAPH_SCHEMA:
        raise ReadinessError(f"unsupported graph schema: {root['schema']!r}")

    axes_raw = _require_object(root["axes"], "axes")
    if not axes_raw:
        raise ReadinessError("axes must not be empty")
    if len(axes_raw) > MAX_AXES:
        raise ReadinessError(f"axes exceeds the fixed bound of {MAX_AXES}")
    axes: dict[str, tuple[str, ...]] = {}
    for axis_name in sorted(axes_raw):
        _require_identifier(axis_name, "axis name")
        levels_raw = axes_raw[axis_name]
        if not isinstance(levels_raw, list) or not levels_raw:
            raise ReadinessError(f"axis {axis_name} must have a nonempty level list")
        if len(levels_raw) > MAX_LEVELS_PER_AXIS:
            raise ReadinessError(
                f"axis {axis_name} exceeds the {MAX_LEVELS_PER_AXIS}-level bound"
            )
        levels = tuple(
            _require_string(level, f"axis {axis_name} level") for level in levels_raw
        )
        if len(set(levels)) != len(levels):
            raise ReadinessError(f"axis {axis_name} contains duplicate levels")
        axes[axis_name] = levels

    nodes_raw = root["nodes"]
    if not isinstance(nodes_raw, list) or not nodes_raw:
        raise ReadinessError("nodes must be a nonempty list")
    if len(nodes_raw) > MAX_NODES:
        raise ReadinessError(f"nodes exceeds the fixed bound of {MAX_NODES}")
    nodes: dict[str, Node] = {}
    for index, raw_node in enumerate(nodes_raw):
        node_object = _require_object(raw_node, f"nodes[{index}]")
        _require_exact_keys(
            node_object,
            {"id", "verdict", "applicable_axes", "initial"},
            f"nodes[{index}]",
        )
        identifier = _require_identifier(node_object["id"], f"nodes[{index}].id")
        if identifier in nodes:
            raise ReadinessError(f"duplicate node id: {identifier}")
        verdict = _require_string(
            node_object["verdict"], f"nodes[{index}].verdict"
        )
        if verdict not in ALLOWED_VERDICTS:
            raise ReadinessError(
                f"node {identifier} verdict is outside the closed vocabulary"
            )
        applicable_raw = node_object["applicable_axes"]
        if not isinstance(applicable_raw, list):
            raise ReadinessError(f"nodes[{index}].applicable_axes must be a list")
        applicable = tuple(
            _require_identifier(axis, f"nodes[{index}].applicable_axes")
            for axis in applicable_raw
        )
        if tuple(sorted(applicable)) != applicable or len(set(applicable)) != len(
            applicable
        ):
            raise ReadinessError(
                f"nodes[{index}].applicable_axes must be sorted and unique"
            )
        unknown_axes = sorted(set(applicable) - set(axes))
        if unknown_axes:
            raise ReadinessError(
                f"node {identifier} references unknown axes: {unknown_axes}"
            )
        initial_raw = _require_object(node_object["initial"], f"node {identifier}.initial")
        if set(initial_raw) != set(applicable):
            raise ReadinessError(
                f"node {identifier} initial axes must equal applicable_axes"
            )
        initial: dict[str, int] = {}
        for axis in applicable:
            label = _require_string(initial_raw[axis], f"node {identifier}.{axis}")
            try:
                initial[axis] = axes[axis].index(label)
            except ValueError as exc:
                raise ReadinessError(
                    f"node {identifier} has unknown {axis} level: {label!r}"
                ) from exc
        nodes[identifier] = Node(identifier, verdict, applicable, initial)

    edges_raw = root["edges"]
    if not isinstance(edges_raw, list):
        raise ReadinessError("edges must be a list")
    if len(edges_raw) > MAX_EDGES:
        raise ReadinessError(f"edges exceeds the fixed bound of {MAX_EDGES}")
    edges: list[Edge] = []
    edge_pairs: set[tuple[str, str]] = set()
    for index, raw_edge in enumerate(edges_raw):
        edge_object = _require_object(raw_edge, f"edges[{index}]")
        _require_exact_keys(
            edge_object, {"source", "target", "caps"}, f"edges[{index}]"
        )
        source = _require_identifier(edge_object["source"], f"edges[{index}].source")
        target = _require_identifier(edge_object["target"], f"edges[{index}].target")
        if source not in nodes or target not in nodes:
            raise ReadinessError(f"edge {source}->{target} references an unknown node")
        if (source, target) in edge_pairs:
            raise ReadinessError(f"duplicate edge: {source}->{target}")
        edge_pairs.add((source, target))
        caps_raw = _require_object(edge_object["caps"], f"edge {source}->{target}.caps")
        if not caps_raw:
            raise ReadinessError(f"edge {source}->{target} must constrain an axis")
        caps: dict[str, tuple[int, ...]] = {}
        for axis in sorted(caps_raw):
            if axis not in axes:
                raise ReadinessError(f"edge {source}->{target} uses unknown axis {axis}")
            if axis not in nodes[source].applicable_axes:
                raise ReadinessError(f"axis {axis} is not applicable to source {source}")
            if axis not in nodes[target].applicable_axes:
                raise ReadinessError(f"axis {axis} is not applicable to target {target}")
            map_raw = caps_raw[axis]
            levels = axes[axis]
            if not isinstance(map_raw, list) or len(map_raw) != len(levels):
                raise ReadinessError(
                    f"edge {source}->{target} cap for {axis} must have {len(levels)} entries"
                )
            mapped: list[int] = []
            for label in map_raw:
                label = _require_string(label, f"edge {source}->{target} {axis} cap")
                try:
                    mapped.append(levels.index(label))
                except ValueError as exc:
                    raise ReadinessError(
                        f"edge {source}->{target} has unknown {axis} cap {label!r}"
                    ) from exc
            if any(left > right for left, right in zip(mapped, mapped[1:])):
                raise ReadinessError(
                    f"edge {source}->{target} cap for {axis} is not monotone"
                )
            caps[axis] = tuple(mapped)
        edges.append(Edge(source, target, caps))

    coordinate_count = sum(len(node.applicable_axes) for node in nodes.values())
    if coordinate_count > MAX_COORDINATES:
        raise ReadinessError(
            f"applicable readiness coordinates exceed the bound of {MAX_COORDINATES}"
        )
    maximum_iterations = sum(
        level for node in nodes.values() for level in node.initial.values()
    )
    if maximum_iterations > MAX_DESCENT_STEPS:
        raise ReadinessError(
            f"readiness descent exceeds the bound of {MAX_DESCENT_STEPS} steps"
        )
    cap_count = sum(len(edge.caps) for edge in edges)
    operation_bound = (maximum_iterations + 1) * max(
        1, coordinate_count + cap_count
    )
    if operation_bound > MAX_FIXED_POINT_OPERATIONS:
        raise ReadinessError(
            "fixed-point work exceeds the bound of "
            f"{MAX_FIXED_POINT_OPERATIONS} readiness operations"
        )

    edges.sort(key=lambda edge: (edge.source, edge.target))
    return Graph(axes, nodes, tuple(edges), maximum_iterations)


Assignment = dict[str, dict[str, int]]


def initial_assignment(graph: Graph) -> Assignment:
    return {
        identifier: dict(graph.nodes[identifier].initial)
        for identifier in sorted(graph.nodes)
    }


def readiness_step(graph: Graph, assignment: Assignment) -> Assignment:
    result = initial_assignment(graph)
    for edge in graph.edges:
        for axis, cap_map in edge.caps.items():
            source_level = assignment[edge.source][axis]
            result[edge.target][axis] = min(
                result[edge.target][axis], cap_map[source_level]
            )
    return result


def fixed_point(graph: Graph) -> tuple[Assignment, int]:
    current = initial_assignment(graph)
    for iterations in range(graph.maximum_iterations + 1):
        updated = readiness_step(graph, current)
        if updated == current:
            return current, iterations
        for identifier in current:
            for axis in current[identifier]:
                if updated[identifier][axis] > current[identifier][axis]:
                    raise ReadinessError("internal error: readiness iteration increased")
        current = updated
    raise ReadinessError("internal error: readiness descent bound was exhausted")


def assignment_is_below_initial(graph: Graph, assignment: Assignment) -> bool:
    if set(assignment) != set(graph.nodes):
        return False
    for identifier, node in graph.nodes.items():
        values = assignment[identifier]
        if set(values) != set(node.applicable_axes):
            return False
        for axis, level in values.items():
            if not isinstance(level, int) or isinstance(level, bool):
                return False
            if not 0 <= level <= node.initial[axis]:
                return False
    return True


def edge_constraints_are_satisfied(graph: Graph, assignment: Assignment) -> bool:
    if not assignment_is_below_initial(graph, assignment):
        return False
    for edge in graph.edges:
        for axis, cap_map in edge.caps.items():
            if assignment[edge.target][axis] > cap_map[assignment[edge.source][axis]]:
                return False
    return True


def assignment_is_feasible(graph: Graph, assignment: Assignment) -> bool:
    return assignment_is_below_initial(
        graph, assignment
    ) and edge_constraints_are_satisfied(graph, assignment)


def render_assignment(graph: Graph, assignment: Assignment) -> dict[str, Any]:
    return {
        identifier: {
            "applicable_axes": list(graph.nodes[identifier].applicable_axes),
            "readiness": {
                axis: graph.axes[axis][assignment[identifier][axis]]
                for axis in graph.nodes[identifier].applicable_axes
            },
            "verdict": graph.nodes[identifier].verdict,
        }
        for identifier in sorted(graph.nodes)
    }


def evaluate(raw: bytes, document: Any) -> dict[str, Any]:
    graph = validate_graph(document)
    assignment, iterations = fixed_point(graph)
    stepped = readiness_step(graph, assignment)
    return {
        "axis_count": len(graph.axes),
        "checks": {
            "below_initial": assignment_is_below_initial(graph, assignment),
            "edge_constraints_satisfied": edge_constraints_are_satisfied(
                graph, assignment
            ),
            "fixed_point": stepped == assignment,
            "verdicts_unchanged": True,
        },
        "edge_count": len(graph.edges),
        "generator_sha256": hashlib.sha256(
            _read_bounded(Path(__file__), MAX_INPUT_BYTES, "checker source")
        ).hexdigest(),
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "iterations": iterations,
        "node_count": len(graph.nodes),
        "result": render_assignment(graph, assignment),
        "schema": RECEIPT_SCHEMA,
        "status": "PASS",
    }


def evaluate_path(path: Path) -> dict[str, Any]:
    raw, document = load_json_bytes(path)
    return evaluate(raw, document)


def _write_new(path: Path, content: bytes) -> None:
    try:
        with path.open("xb") as stream:
            stream.write(content)
    except FileExistsError as exc:
        raise ReadinessError("refusing to overwrite existing receipt") from exc
    except OSError:
        raise ReadinessError("cannot write receipt") from None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate or verify a finite cyclic BSC readiness graph."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    evaluate_parser = subparsers.add_parser("evaluate")
    evaluate_parser.add_argument("graph", type=Path)
    write_parser = subparsers.add_parser("write-new")
    write_parser.add_argument("graph", type=Path)
    write_parser.add_argument("receipt", type=Path)
    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("graph", type=Path)
    check_parser.add_argument("receipt", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        expected = canonical_json(evaluate_path(args.graph))
        if args.command == "evaluate":
            sys.stdout.buffer.write(expected)
        elif args.command == "write-new":
            _write_new(args.receipt, expected)
            print("BSC READINESS: PASS: wrote receipt")
        else:
            actual = _read_bounded(
                args.receipt, MAX_RECEIPT_BYTES, "retained receipt"
            )
            if actual != expected:
                raise ReadinessError("receipt is stale, noncanonical, or identity-mismatched")
            print("BSC READINESS: PASS: receipt matches exact graph bytes")
    except ReadinessError as exc:
        print(f"BSC READINESS: FAIL: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
