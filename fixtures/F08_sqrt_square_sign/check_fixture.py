#!/usr/bin/env python3
"""Fail-closed verification gate for the retained F8 receipt."""

from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


FIXTURE_DIR = Path(__file__).resolve().parent
SCRIPT = FIXTURE_DIR / "verify_counterexample.py"
SCHEMA = FIXTURE_DIR / "receipt.schema.json"
EXPECTED = FIXTURE_DIR / "verification_receipt.json"
FIXTURE_ID = "F8-SQRT-SQUARE-SIGN"
CLAIM = "for every real x, sqrt(x^2) = x"
RECEIPT_SCHEMA = "bsc-deterministic-receipt/2"
SAFE_COMMAND = (
    "python3 fixtures/F08_sqrt_square_sign/verify_counterexample.py "
    "build/F08_actual_receipt.json"
)
SUPPORTED_SCHEMA_KEYWORDS = {
    "$schema",
    "additionalProperties",
    "const",
    "description",
    "pattern",
    "properties",
    "required",
    "title",
    "type",
}
SUPPORTED_JSON_TYPES = {
    "array",
    "boolean",
    "integer",
    "null",
    "number",
    "object",
    "string",
}


class SchemaValidationError(ValueError):
    """Raised when the schema or receipt violates the supported contract."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fail(message: str) -> int:
    print(f"{FIXTURE_ID}: FAIL: {message}", file=sys.stderr)
    return 1


def json_equal(left: Any, right: Any) -> bool:
    """JSON equality that does not conflate booleans and integers."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(
            json_equal(left[key], right[key]) for key in left
        )
    if isinstance(left, list):
        return len(left) == len(right) and all(
            json_equal(a, b) for a, b in zip(left, right, strict=True)
        )
    return bool(left == right)


def validate_schema_definition(schema: Any, location: str = "$") -> None:
    if not isinstance(schema, dict):
        raise SchemaValidationError(f"{location}: schema node must be an object")
    unknown = set(schema) - SUPPORTED_SCHEMA_KEYWORDS
    if unknown:
        raise SchemaValidationError(
            f"{location}: unsupported schema keywords: {sorted(unknown)}"
        )

    declared_type = schema.get("type")
    if declared_type is not None:
        if (
            not isinstance(declared_type, str)
            or declared_type not in SUPPORTED_JSON_TYPES
        ):
            raise SchemaValidationError(
                f"{location}: unsupported type declaration: {declared_type!r}"
            )

    required = schema.get("required")
    if required is not None:
        if (
            not isinstance(required, list)
            or not all(isinstance(item, str) for item in required)
            or len(required) != len(set(required))
        ):
            raise SchemaValidationError(
                f"{location}: required must contain unique strings"
            )

    properties = schema.get("properties")
    if properties is not None:
        if not isinstance(properties, dict) or not all(
            isinstance(key, str) for key in properties
        ):
            raise SchemaValidationError(
                f"{location}: properties must be an object"
            )
        for key, subschema in properties.items():
            validate_schema_definition(subschema, f"{location}.{key}")

    additional = schema.get("additionalProperties")
    if additional is not None and not isinstance(additional, bool):
        raise SchemaValidationError(
            f"{location}: additionalProperties must be Boolean"
        )

    pattern = schema.get("pattern")
    if pattern is not None:
        if not isinstance(pattern, str):
            raise SchemaValidationError(f"{location}: pattern must be a string")
        try:
            re.compile(pattern)
        except re.error as exc:
            raise SchemaValidationError(
                f"{location}: invalid regular expression: {exc}"
            ) from exc


def instance_has_type(instance: Any, declared_type: str) -> bool:
    return {
        "array": lambda value: isinstance(value, list),
        "boolean": lambda value: type(value) is bool,
        "integer": lambda value: type(value) is int,
        "null": lambda value: value is None,
        "number": lambda value: type(value) in {int, float},
        "object": lambda value: isinstance(value, dict),
        "string": lambda value: isinstance(value, str),
    }[declared_type](instance)


def validate_instance(
    instance: Any, schema: dict[str, Any], location: str = "$"
) -> None:
    declared_type = schema.get("type")
    if declared_type is not None and not instance_has_type(instance, declared_type):
        raise SchemaValidationError(
            f"{location}: expected {declared_type}, got "
            f"{type(instance).__name__}"
        )

    if "const" in schema and not json_equal(instance, schema["const"]):
        raise SchemaValidationError(
            f"{location}: value does not match declared constant"
        )

    pattern = schema.get("pattern")
    if pattern is not None:
        if not isinstance(instance, str) or re.search(pattern, instance) is None:
            raise SchemaValidationError(
                f"{location}: string does not match {pattern!r}"
            )

    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        missing = sorted(set(required) - set(instance))
        if missing:
            raise SchemaValidationError(
                f"{location}: missing required properties: {missing}"
            )
        if schema.get("additionalProperties") is False:
            extras = sorted(set(instance) - set(properties))
            if extras:
                raise SchemaValidationError(
                    f"{location}: unexpected properties: {extras}"
                )
        for key, subschema in properties.items():
            if key in instance:
                validate_instance(instance[key], subschema, f"{location}.{key}")


def load_json(path: Path, description: str) -> tuple[bytes, Any]:
    try:
        data = path.read_bytes()
        return data, json.loads(data)
    except (OSError, json.JSONDecodeError) as exc:
        raise SchemaValidationError(f"cannot read {description}: {exc}") from exc


def verify_receipt_semantics(
    expected: dict[str, Any], script_bytes: bytes, schema_bytes: bytes
) -> None:
    fixed_fields = {
        "arithmetic_model": "exact integers",
        "claim": CLAIM,
        "command": SAFE_COMMAND,
        "fixture_id": FIXTURE_ID,
        "receipt_schema": RECEIPT_SCHEMA,
        "working_directory": "repository root",
    }
    for field, value in fixed_fields.items():
        if not json_equal(expected.get(field), value):
            raise SchemaValidationError(f"{field} is not the required value")

    if sha256(CLAIM.encode("utf-8")) != expected["claim_sha256"]:
        raise SchemaValidationError("claim hash mismatch")
    if sha256(script_bytes) != expected["script_sha256"]:
        raise SchemaValidationError("verifier hash mismatch")
    if sha256(schema_bytes) != expected["schema_sha256"]:
        raise SchemaValidationError("schema hash mismatch")

    x = expected["input"]["x"]
    if type(x) is not int:
        raise SchemaValidationError("fixture input must be an integer")
    recorded_output = expected["output"]
    exact_sqrt = math.isqrt(x * x)
    if recorded_output["x"] != x:
        raise SchemaValidationError("recorded output x differs from the input")
    if recorded_output["sqrt_x_squared"] != exact_sqrt:
        raise SchemaValidationError(
            "recorded square root differs from independent exact arithmetic"
        )

    predicate = exact_sqrt == x
    result = "claim_holds_for_input" if predicate else "counterexample_confirmed"
    if expected["predicate_holds"] is not predicate:
        raise SchemaValidationError(
            "predicate field is inconsistent with independent arithmetic"
        )
    if predicate:
        raise SchemaValidationError("the retained input is not a counterexample")
    if expected["result"] != result:
        raise SchemaValidationError(
            "result label is inconsistent with independent arithmetic"
        )


def main() -> int:
    try:
        expected_bytes, expected = load_json(EXPECTED, "retained receipt")
        schema_bytes, schema = load_json(SCHEMA, "receipt schema")
        if not isinstance(schema, dict):
            raise SchemaValidationError("receipt schema must be an object")
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise SchemaValidationError("unexpected JSON Schema dialect")
        validate_schema_definition(schema)
        validate_instance(expected, schema)
        script_bytes = SCRIPT.read_bytes()
        verify_receipt_semantics(expected, script_bytes, schema_bytes)
    except (OSError, SchemaValidationError) as exc:
        return fail(str(exc))

    with tempfile.TemporaryDirectory(prefix="bsc-f8-") as temp_dir:
        isolated_fixture = Path(temp_dir)
        isolated_script = isolated_fixture / SCRIPT.name
        isolated_schema = isolated_fixture / SCHEMA.name
        shutil.copyfile(SCRIPT, isolated_script)
        shutil.copyfile(SCHEMA, isolated_schema)
        actual_path = isolated_fixture / "actual_receipt.json"
        completed = subprocess.run(
            [sys.executable, str(isolated_script), str(actual_path)],
            cwd=isolated_fixture,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip()
            return fail(f"verifier exited {completed.returncode}: {detail}")
        try:
            actual_bytes = actual_path.read_bytes()
            retained_after_execution = EXPECTED.read_bytes()
        except OSError as exc:
            return fail(f"verifier did not preserve both receipts: {exc}")

    if retained_after_execution != expected_bytes:
        return fail("verifier modified the retained receipt")
    if actual_bytes != expected_bytes:
        return fail(
            "generated receipt is not byte-identical to the retained receipt; "
            f"expected {sha256(expected_bytes)}, got {sha256(actual_bytes)}"
        )

    print(f"{FIXTURE_ID}: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
