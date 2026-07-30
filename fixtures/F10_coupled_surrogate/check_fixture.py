#!/usr/bin/env python3
"""Fail-closed verification gate for the retained F10 receipt."""

from __future__ import annotations

import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Any


FIXTURE_DIR = Path(__file__).resolve().parent
GENERATOR = FIXTURE_DIR / "verify_coupled_surrogate.py"
CHECKER = Path(__file__).resolve()
INPUT = FIXTURE_DIR / "input.json"
SCHEMA = FIXTURE_DIR / "receipt.schema.json"
EXPECTED = FIXTURE_DIR / "verification_receipt.json"
CLAIM_ID = "BSC-FIX-10"
FIXTURE_ID = "F10-COUPLED-SURROGATE"
CLAIM = (
    "the same exact standalone surrogate interface error stays within the "
    "declared host-state tolerance in HOST-A and produces an exact tolerance "
    "violation in HOST-B"
)
ARITHMETIC_MODEL = "fractions.Fraction exact rational arithmetic"
RECEIPT_SCHEMA = "bsc-deterministic-receipt/4"
SERIALIZATION = "UTF-8 JSON, two-space indentation, sorted keys, LF terminator"
SELF_HASH_POLICY = (
    "no recursive self-hash is embedded; bind verification_receipt.json "
    "externally in MANIFEST.sha256"
)
DATA_STATUS = "not_applicable"
DATA_REASON = (
    "exact rational fixture; no training, calibration, validation, "
    "or empirical data"
)
SAFE_COMMAND = (
    "python3 fixtures/F10_coupled_surrogate/verify_coupled_surrogate.py "
    "build/F10_actual_receipt.json"
)
RECURRENCE = "error[k] = a * error[k-1] + abs(zhat - z)"
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


class FixtureValidationError(ValueError):
    """Raised when an F10 artifact violates the fixture contract."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def fail(message: str) -> int:
    print(f"{FIXTURE_ID}: FAIL: {message}", file=sys.stderr)
    return 1


def json_equal(left: Any, right: Any) -> bool:
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
        raise FixtureValidationError(f"{location}: schema node must be an object")
    unknown = set(schema) - SUPPORTED_SCHEMA_KEYWORDS
    if unknown:
        raise FixtureValidationError(
            f"{location}: unsupported schema keywords: {sorted(unknown)}"
        )
    declared_type = schema.get("type")
    if declared_type is not None and (
        not isinstance(declared_type, str)
        or declared_type not in SUPPORTED_JSON_TYPES
    ):
        raise FixtureValidationError(
            f"{location}: unsupported type declaration: {declared_type!r}"
        )
    required = schema.get("required")
    if required is not None and (
        not isinstance(required, list)
        or not all(isinstance(item, str) for item in required)
        or len(required) != len(set(required))
    ):
        raise FixtureValidationError(
            f"{location}: required must contain unique strings"
        )
    properties = schema.get("properties")
    if properties is not None:
        if not isinstance(properties, dict) or not all(
            isinstance(key, str) for key in properties
        ):
            raise FixtureValidationError(
                f"{location}: properties must be an object"
            )
        for key, subschema in properties.items():
            validate_schema_definition(subschema, f"{location}.{key}")
    additional = schema.get("additionalProperties")
    if additional is not None and not isinstance(additional, bool):
        raise FixtureValidationError(
            f"{location}: additionalProperties must be Boolean"
        )
    pattern = schema.get("pattern")
    if pattern is not None:
        if not isinstance(pattern, str):
            raise FixtureValidationError(f"{location}: pattern must be a string")
        try:
            re.compile(pattern)
        except re.error as exc:
            raise FixtureValidationError(
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
        raise FixtureValidationError(
            f"{location}: expected {declared_type}, got "
            f"{type(instance).__name__}"
        )
    if "const" in schema and not json_equal(instance, schema["const"]):
        raise FixtureValidationError(
            f"{location}: value does not match declared constant"
        )
    pattern = schema.get("pattern")
    if pattern is not None and (
        not isinstance(instance, str) or re.search(pattern, instance) is None
    ):
        raise FixtureValidationError(
            f"{location}: string does not match {pattern!r}"
        )
    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        missing = sorted(set(required) - set(instance))
        if missing:
            raise FixtureValidationError(
                f"{location}: missing required properties: {missing}"
            )
        if schema.get("additionalProperties") is False:
            extras = sorted(set(instance) - set(properties))
            if extras:
                raise FixtureValidationError(
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
        raise FixtureValidationError(
            f"cannot read {description}: {exc}"
        ) from exc


def fraction_from_record(value: Any, location: str) -> Fraction:
    if not isinstance(value, dict) or set(value) != {"denominator", "numerator"}:
        raise FixtureValidationError(
            f"{location} must contain only numerator and denominator"
        )
    numerator = value["numerator"]
    denominator = value["denominator"]
    if type(numerator) is not int or type(denominator) is not int:
        raise FixtureValidationError(
            f"{location} numerator and denominator must be integers"
        )
    if denominator <= 0:
        raise FixtureValidationError(f"{location} denominator must be positive")
    result = Fraction(numerator, denominator)
    if result.numerator != numerator or result.denominator != denominator:
        raise FixtureValidationError(
            f"{location} must be in canonical reduced form"
        )
    return result


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def validate_input(specification: Any) -> dict[str, Any]:
    if not isinstance(specification, dict):
        raise FixtureValidationError("canonical input must be an object")
    required_keys = {
        "claim_id",
        "environment",
        "fixture_id",
        "horizon",
        "hosts",
        "initial_reference_state",
        "initial_surrogate_state",
        "recurrence",
        "reference",
        "surrogate",
        "tolerance",
    }
    if set(specification) != required_keys:
        raise FixtureValidationError("canonical input keys are not exact")
    if specification["claim_id"] != CLAIM_ID:
        raise FixtureValidationError("claim_id is not the required value")
    if specification["fixture_id"] != FIXTURE_ID:
        raise FixtureValidationError("fixture_id is not the required value")
    if specification["horizon"] != 10:
        raise FixtureValidationError("horizon must be exactly 10")
    if specification["recurrence"] != RECURRENCE:
        raise FixtureValidationError("recurrence is not the required value")

    expected_environment = {
        "arithmetic": "fractions.Fraction",
        "implementation": "CPython",
        "version": "3.12.13",
    }
    if not json_equal(specification["environment"], expected_environment):
        raise FixtureValidationError("environment contract is not exact")
    actual_environment = {
        "arithmetic": "fractions.Fraction",
        "implementation": platform.python_implementation(),
        "version": platform.python_version(),
    }
    if actual_environment != expected_environment:
        raise FixtureValidationError(
            "current runtime does not match the fixture environment"
        )

    reference = specification["reference"]
    surrogate = specification["surrogate"]
    if not isinstance(reference, dict) or set(reference) != {"z"}:
        raise FixtureValidationError("reference must contain only z")
    if not isinstance(surrogate, dict) or set(surrogate) != {"zhat"}:
        raise FixtureValidationError("surrogate must contain only zhat")
    if fraction_from_record(reference["z"], "reference.z") != 0:
        raise FixtureValidationError("reference z must be exactly 0")
    if fraction_from_record(surrogate["zhat"], "surrogate.zhat") != Fraction(
        1, 100
    ):
        raise FixtureValidationError("surrogate zhat must be exactly 1/100")
    if fraction_from_record(
        specification["initial_reference_state"],
        "initial_reference_state",
    ) != 0:
        raise FixtureValidationError(
            "initial_reference_state must be exactly 0"
        )
    if fraction_from_record(
        specification["initial_surrogate_state"],
        "initial_surrogate_state",
    ) != 0:
        raise FixtureValidationError(
            "initial_surrogate_state must be exactly 0"
        )
    if fraction_from_record(specification["tolerance"], "tolerance") != Fraction(
        1, 20
    ):
        raise FixtureValidationError("tolerance must be exactly 1/20")

    hosts = specification["hosts"]
    if not isinstance(hosts, dict) or set(hosts) != {"HOST-A", "HOST-B"}:
        raise FixtureValidationError(
            "hosts must contain exactly HOST-A and HOST-B"
        )
    expected_a = {"HOST-A": Fraction(1, 2), "HOST-B": Fraction(9, 10)}
    for host_id, required_a in expected_a.items():
        host = hosts[host_id]
        if not isinstance(host, dict) or set(host) != {"a", "host_id"}:
            raise FixtureValidationError(f"{host_id} keys are not exact")
        if host["host_id"] != host_id:
            raise FixtureValidationError(f"{host_id} has a stale host_id")
        if fraction_from_record(host["a"], f"{host_id}.a") != required_a:
            raise FixtureValidationError(f"{host_id} a is not the required value")
        if abs(required_a) >= 1:
            raise FixtureValidationError(f"{host_id} must be stable")
    return specification


def compute_expected_host(
    host_spec: dict[str, Any],
    z: Fraction,
    zhat: Fraction,
    initial_reference_state: Fraction,
    initial_surrogate_state: Fraction,
    horizon: int,
    tolerance: Fraction,
) -> dict[str, Any]:
    host_id = host_spec["host_id"]
    a = fraction_from_record(host_spec["a"], f"{host_id}.a")
    interface_error = abs(zhat - z)
    reference_state = initial_reference_state
    surrogate_state = initial_surrogate_state
    reference_state_path = [fraction_text(reference_state)]
    surrogate_state_path = [fraction_text(surrogate_state)]
    prefix_errors: list[str] = []
    first_violation_step: int | None = None
    for step in range(1, horizon + 1):
        reference_state = a * reference_state + z
        surrogate_state = a * surrogate_state + zhat
        error = abs(surrogate_state - reference_state)
        reference_state_path.append(fraction_text(reference_state))
        surrogate_state_path.append(fraction_text(surrogate_state))
        prefix_errors.append(fraction_text(error))
        if first_violation_step is None and error > tolerance:
            first_violation_step = step
    maximum_error = max(Fraction(value) for value in prefix_errors)
    within_tolerance = maximum_error <= tolerance
    return {
        "a": fraction_text(a),
        "effective_gain": fraction_text(maximum_error / interface_error),
        "first_violation_step": first_violation_step,
        "host_id": host_id,
        "maximum_error": fraction_text(maximum_error),
        "prefix_errors": prefix_errors,
        "reference_state_path": reference_state_path,
        "stable": abs(a) < 1,
        "surrogate_state_path": surrogate_state_path,
        "tolerance_disposition": (
            "within_tolerance" if within_tolerance else "tolerance_violated"
        ),
        "violation_basis": (
            "none"
            if within_tolerance
            else "exact_actual_error_above_tolerance"
        ),
        "within_tolerance": within_tolerance,
    }


def verify_receipt_semantics(
    receipt: dict[str, Any],
    specification: dict[str, Any],
    input_bytes: bytes,
    schema_bytes: bytes,
) -> None:
    fixed_fields = {
        "arithmetic_model": ARITHMETIC_MODEL,
        "claim": CLAIM,
        "claim_id": CLAIM_ID,
        "command": SAFE_COMMAND,
        "fixture_id": FIXTURE_ID,
        "receipt_schema": RECEIPT_SCHEMA,
        "result": "host_relative_tolerance_disposition_confirmed",
        "self_hash_policy": SELF_HASH_POLICY,
        "working_directory": "repository root",
    }
    for field, value in fixed_fields.items():
        if not json_equal(receipt.get(field), value):
            raise FixtureValidationError(f"{field} is not the required value")
    if receipt.get("claim_sha256") != sha256(CLAIM.encode("utf-8")):
        raise FixtureValidationError("claim hash mismatch")
    if not json_equal(receipt.get("environment"), specification["environment"]):
        raise FixtureValidationError("receipt environment differs from input")

    host_hashes = {
        host_id: sha256(canonical_bytes(specification["hosts"][host_id]))
        for host_id in ("HOST-A", "HOST-B")
    }
    candidate_material = {
        "hosts": specification["hosts"],
        "initial_reference_state": specification[
            "initial_reference_state"
        ],
        "initial_surrogate_state": specification[
            "initial_surrogate_state"
        ],
        "recurrence": specification["recurrence"],
        "reference": specification["reference"],
        "surrogate": specification["surrogate"],
    }
    data_material = {
        "reason": DATA_REASON,
        "status": DATA_STATUS,
    }
    analysis_material = {
        "checker_sha256": sha256(CHECKER.read_bytes()),
        "generator_sha256": sha256(GENERATOR.read_bytes()),
        "schema_sha256": sha256(schema_bytes),
        "serialization": SERIALIZATION,
    }
    contract_material = {
        "claim": CLAIM,
        "claim_id": CLAIM_ID,
        "fixture_id": FIXTURE_ID,
        "input_sha256": sha256(input_bytes),
    }
    expected_identity = {
        "analysis": {
            "analysis_sha256": sha256(canonical_bytes(analysis_material)),
            **analysis_material,
        },
        "candidate": {
            "candidate_sha256": sha256(canonical_bytes(candidate_material)),
            "host_sha256": host_hashes,
        },
        "contract": {
            "contract_sha256": sha256(canonical_bytes(contract_material)),
            **contract_material,
        },
        "data": {
            "data_sha256": sha256(canonical_bytes(data_material)),
            **data_material,
        },
        "environment": {
            "environment_sha256": sha256(
                canonical_bytes(specification["environment"])
            ),
        },
    }
    evidence_identity = receipt.get("evidence_identity")
    if not isinstance(evidence_identity, dict):
        raise FixtureValidationError("evidence_identity must be an object")
    candidate_identity = evidence_identity.get("candidate")
    if not isinstance(candidate_identity, dict):
        raise FixtureValidationError(
            "evidence_identity.candidate must be an object"
        )
    recorded_host_hashes = candidate_identity.get("host_sha256")
    if not isinstance(recorded_host_hashes, dict):
        raise FixtureValidationError("host_sha256 must be an object")
    for host_id in ("HOST-A", "HOST-B"):
        if recorded_host_hashes.get(host_id) != host_hashes[host_id]:
            raise FixtureValidationError(
                f"{host_id} host identity hash mismatch"
            )
    if not json_equal(evidence_identity, expected_identity):
        raise FixtureValidationError(
            "evidence_identity differs from the five-factor identity"
        )

    initial_reference_state = fraction_from_record(
        specification["initial_reference_state"],
        "initial_reference_state",
    )
    initial_surrogate_state = fraction_from_record(
        specification["initial_surrogate_state"],
        "initial_surrogate_state",
    )
    initial_error = abs(initial_surrogate_state - initial_reference_state)
    expected_specification = {
        "horizon": 10,
        "initial_error": fraction_text(initial_error),
        "initial_reference_state": fraction_text(initial_reference_state),
        "initial_surrogate_state": fraction_text(initial_surrogate_state),
        "interface_error": "1/100",
        "reference_z": "0",
        "surrogate_zhat": "1/100",
        "tolerance": "1/20",
    }
    if not json_equal(receipt.get("specification"), expected_specification):
        raise FixtureValidationError(
            "receipt specification is inconsistent with canonical input"
        )

    hosts = receipt.get("hosts")
    if not isinstance(hosts, dict) or set(hosts) != {"HOST-A", "HOST-B"}:
        raise FixtureValidationError("receipt hosts are not exact")
    for host_id in ("HOST-A", "HOST-B"):
        expected_host = compute_expected_host(
            specification["hosts"][host_id],
            Fraction(0),
            Fraction(1, 100),
            initial_reference_state,
            initial_surrogate_state,
            10,
            Fraction(1, 20),
        )
        recorded_host = hosts[host_id]
        if not isinstance(recorded_host, dict):
            raise FixtureValidationError(f"{host_id} receipt must be an object")
        if (
            recorded_host.get("within_tolerance")
            is not expected_host["within_tolerance"]
        ):
            raise FixtureValidationError(
                f"{host_id} within_tolerance is inconsistent with exact arithmetic"
            )
        if (
            recorded_host.get("tolerance_disposition")
            != expected_host["tolerance_disposition"]
        ):
            raise FixtureValidationError(
                f"{host_id} tolerance disposition is inconsistent with exact arithmetic"
            )
        if not json_equal(recorded_host, expected_host):
            raise FixtureValidationError(
                f"{host_id} receipt differs from independent exact arithmetic"
            )

    if hosts["HOST-A"]["maximum_error"] != "1023/51200":
        raise FixtureValidationError("HOST-A exact endpoint changed")
    if hosts["HOST-A"]["within_tolerance"] is not True:
        raise FixtureValidationError("HOST-A must be within tolerance")
    if hosts["HOST-B"]["maximum_error"] != "6513215599/100000000000":
        raise FixtureValidationError("HOST-B exact endpoint changed")
    if hosts["HOST-B"]["first_violation_step"] != 7:
        raise FixtureValidationError("HOST-B first actual violation must be step 7")
    if hosts["HOST-B"]["within_tolerance"] is not False:
        raise FixtureValidationError("HOST-B must violate tolerance")


def main() -> int:
    try:
        input_bytes, specification = load_json(INPUT, "canonical input")
        specification = validate_input(specification)
        schema_bytes, schema = load_json(SCHEMA, "receipt schema")
        if not isinstance(schema, dict):
            raise FixtureValidationError("receipt schema must be an object")
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise FixtureValidationError("unexpected JSON Schema dialect")
        validate_schema_definition(schema)
        expected_bytes, receipt = load_json(EXPECTED, "retained receipt")
        validate_instance(receipt, schema)
        if not isinstance(receipt, dict):
            raise FixtureValidationError("retained receipt must be an object")
        verify_receipt_semantics(
            receipt,
            specification,
            input_bytes,
            schema_bytes,
        )
    except (OSError, FixtureValidationError) as exc:
        return fail(str(exc))

    with tempfile.TemporaryDirectory(prefix="bsc-f10-") as temporary:
        isolated = Path(temporary)
        for source in (GENERATOR, CHECKER, INPUT, SCHEMA):
            shutil.copyfile(source, isolated / source.name)
        actual = isolated / "actual_receipt.json"
        completed = subprocess.run(
            [sys.executable, str(isolated / GENERATOR.name), str(actual)],
            cwd=isolated,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip()
            return fail(f"generator exited {completed.returncode}: {detail}")
        try:
            actual_bytes = actual.read_bytes()
            retained_after_execution = EXPECTED.read_bytes()
        except OSError as exc:
            return fail(f"generator did not preserve both receipts: {exc}")

    if retained_after_execution != expected_bytes:
        return fail("generator modified the retained receipt")
    if actual_bytes != expected_bytes:
        return fail(
            "generated receipt is not byte-identical to the retained receipt; "
            f"expected {sha256(expected_bytes)}, got {sha256(actual_bytes)}"
        )

    print(f"{FIXTURE_ID}: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
