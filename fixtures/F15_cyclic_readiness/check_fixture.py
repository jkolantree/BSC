#!/usr/bin/env python3
"""Cross-check the retained F15 receipt using same-implementation parsing."""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from tools.bsc_claim_readiness import (  # noqa: E402
    MAX_RECEIPT_BYTES,
    ReadinessError,
    assignment_is_feasible,
    canonical_json,
    evaluate_path,
    load_json_bytes,
    validate_graph,
)


def assignments_below_initial(graph):
    coordinates: list[tuple[str, str, range]] = []
    for identifier in sorted(graph.nodes):
        node = graph.nodes[identifier]
        for axis in node.applicable_axes:
            coordinates.append((identifier, axis, range(node.initial[axis] + 1)))
    for values in itertools.product(*(coordinate[2] for coordinate in coordinates)):
        assignment = {
            identifier: {} for identifier in sorted(graph.nodes)
        }
        for (identifier, axis, _), value in zip(coordinates, values):
            assignment[identifier][axis] = value
        yield assignment


def validate_receipt_schema(document):
    expected_keys = {
        "axis_count",
        "checks",
        "edge_count",
        "generator_sha256",
        "input_sha256",
        "iterations",
        "node_count",
        "result",
        "schema",
        "status",
    }
    if not isinstance(document, dict) or set(document) != {
        "$schema",
        "$id",
        "title",
        "type",
        "additionalProperties",
        "required",
        "properties",
    }:
        raise ReadinessError("receipt schema has an unexpected root shape")
    if document["$schema"] != "https://json-schema.org/draft/2020-12/schema":
        raise ReadinessError("receipt schema draft differs")
    if document["$id"] != "urn:bsc:fixture:f15:cyclic-readiness-receipt:v1":
        raise ReadinessError("receipt schema identifier differs")
    if document["type"] != "object" or document["additionalProperties"] is not False:
        raise ReadinessError("receipt schema is not a closed object")
    if document["required"] != sorted(expected_keys):
        raise ReadinessError("receipt schema required keys differ")
    properties = document["properties"]
    if not isinstance(properties, dict) or set(properties) != expected_keys:
        raise ReadinessError("receipt schema properties differ")
    expected_constants = {
        "axis_count": 3,
        "edge_count": 3,
        "node_count": 3,
        "schema": "bsc.claim-readiness-receipt.v1",
        "status": "PASS",
    }
    for key, value in expected_constants.items():
        if properties[key] != {"const": value}:
            raise ReadinessError(f"receipt schema constant differs for {key}")


def parse_receipt_result(graph, receipt):
    result = receipt.get("result")
    if not isinstance(result, dict) or set(result) != set(graph.nodes):
        raise ReadinessError("receipt result node set differs from graph")
    assignment = {}
    for identifier in sorted(graph.nodes):
        record = result[identifier]
        if not isinstance(record, dict) or set(record) != {
            "applicable_axes",
            "readiness",
            "verdict",
        }:
            raise ReadinessError(f"invalid receipt record for {identifier}")
        node = graph.nodes[identifier]
        if record["applicable_axes"] != list(node.applicable_axes):
            raise ReadinessError(f"applicability mismatch for {identifier}")
        if record["verdict"] != node.verdict:
            raise ReadinessError(f"verdict changed for {identifier}")
        readiness = record["readiness"]
        if not isinstance(readiness, dict) or set(readiness) != set(
            node.applicable_axes
        ):
            raise ReadinessError(f"readiness axes differ for {identifier}")
        assignment[identifier] = {}
        for axis in node.applicable_axes:
            try:
                assignment[identifier][axis] = graph.axes[axis].index(
                    readiness[axis]
                )
            except (TypeError, ValueError) as exc:
                raise ReadinessError(
                    f"unknown receipt level for {identifier}.{axis}"
                ) from exc
    return assignment


def main() -> int:
    input_path = FIXTURE / "input.json"
    receipt_path = FIXTURE / "verification_receipt.json"
    schema_path = FIXTURE / "receipt.schema.json"
    try:
        _, schema_document = load_json_bytes(schema_path, label="receipt schema")
        validate_receipt_schema(schema_document)
        _, document = load_json_bytes(input_path)
        graph = validate_graph(document)
        receipt_bytes, receipt = load_json_bytes(
            receipt_path, maximum=MAX_RECEIPT_BYTES, label="receipt"
        )
        expected = evaluate_path(input_path)
        if receipt_bytes != canonical_json(receipt):
            raise ReadinessError("retained receipt is not canonical JSON")
        if receipt != expected:
            raise ReadinessError("retained receipt does not match the generator")
        retained = parse_receipt_result(graph, receipt)
        if not assignment_is_feasible(graph, retained):
            raise ReadinessError("retained assignment is not feasible")
        feasible_count = 0
        for candidate in assignments_below_initial(graph):
            if not assignment_is_feasible(graph, candidate):
                continue
            feasible_count += 1
            for identifier in retained:
                for axis in retained[identifier]:
                    if candidate[identifier][axis] > retained[identifier][axis]:
                        raise ReadinessError(
                            "retained assignment is not the greatest feasible one"
                        )
        if feasible_count == 0:
            raise ReadinessError("no feasible assignments were enumerated")
    except (ReadinessError, OSError, json.JSONDecodeError) as exc:
        print(f"F15 CHECK: FAIL: {exc}", file=sys.stderr)
        return 1
    print(
        "F15 CHECK: PASS: canonical receipt; "
        f"{feasible_count} feasible assignments; greatest fixed point confirmed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
