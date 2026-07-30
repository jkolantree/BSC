#!/usr/bin/env python3
"""Emit the deterministic receipt for BSC fixture F10."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


FIXTURE_DIR = Path(__file__).resolve().parent
INPUT = FIXTURE_DIR / "input.json"
SCHEMA = FIXTURE_DIR / "receipt.schema.json"
CHECKER = FIXTURE_DIR / "check_fixture.py"
RETAINED_RECEIPT = FIXTURE_DIR / "verification_receipt.json"
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


class FixtureInputError(ValueError):
    """Raised when the canonical fixture input is malformed."""


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


def fraction_from_record(value: Any, location: str) -> Fraction:
    if not isinstance(value, dict) or set(value) != {"denominator", "numerator"}:
        raise FixtureInputError(
            f"{location} must contain only numerator and denominator"
        )
    numerator = value["numerator"]
    denominator = value["denominator"]
    if type(numerator) is not int or type(denominator) is not int:
        raise FixtureInputError(f"{location} numerator and denominator must be integers")
    if denominator <= 0:
        raise FixtureInputError(f"{location} denominator must be positive")
    result = Fraction(numerator, denominator)
    if result.numerator != numerator or result.denominator != denominator:
        raise FixtureInputError(f"{location} must be in canonical reduced form")
    return result


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def load_input() -> tuple[bytes, dict[str, Any]]:
    try:
        input_bytes = INPUT.read_bytes()
        value = json.loads(input_bytes)
    except (OSError, json.JSONDecodeError) as exc:
        raise FixtureInputError(f"cannot read canonical input: {exc}") from exc
    if not isinstance(value, dict):
        raise FixtureInputError("canonical input must be an object")
    return input_bytes, value


def compute_host(
    host_spec: dict[str, Any],
    z: Fraction,
    zhat: Fraction,
    initial_reference_state: Fraction,
    initial_surrogate_state: Fraction,
    horizon: int,
    tolerance: Fraction,
) -> dict[str, Any]:
    host_id = host_spec.get("host_id")
    if not isinstance(host_id, str):
        raise FixtureInputError("host_id must be a string")
    a = fraction_from_record(host_spec.get("a"), f"{host_id}.a")
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
    maximum_error = max(
        (Fraction(value) for value in prefix_errors),
        default=Fraction(0),
    )
    within_tolerance = maximum_error <= tolerance
    effective_gain = maximum_error / interface_error
    return {
        "a": fraction_text(a),
        "effective_gain": fraction_text(effective_gain),
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


def build_receipt() -> dict[str, Any]:
    input_bytes, specification = load_input()
    if specification.get("claim_id") != CLAIM_ID:
        raise FixtureInputError("claim_id is not the required value")
    if specification.get("fixture_id") != FIXTURE_ID:
        raise FixtureInputError("fixture_id is not the required value")

    environment = specification.get("environment")
    if not isinstance(environment, dict):
        raise FixtureInputError("environment must be an object")
    actual_environment = {
        "arithmetic": "fractions.Fraction",
        "implementation": platform.python_implementation(),
        "version": platform.python_version(),
    }
    if environment != actual_environment:
        raise FixtureInputError(
            "runtime environment does not match the canonical input: "
            f"expected {environment!r}, got {actual_environment!r}"
        )

    horizon = specification.get("horizon")
    if type(horizon) is not int or horizon <= 0:
        raise FixtureInputError("horizon must be a positive integer")
    initial_reference_state = fraction_from_record(
        specification.get("initial_reference_state"),
        "initial_reference_state",
    )
    if initial_reference_state != 0:
        raise FixtureInputError("initial_reference_state must be exactly 0")
    initial_surrogate_state = fraction_from_record(
        specification.get("initial_surrogate_state"),
        "initial_surrogate_state",
    )
    if initial_surrogate_state != 0:
        raise FixtureInputError("initial_surrogate_state must be exactly 0")
    initial_error = abs(initial_surrogate_state - initial_reference_state)
    reference = specification.get("reference")
    surrogate = specification.get("surrogate")
    if not isinstance(reference, dict) or set(reference) != {"z"}:
        raise FixtureInputError("reference must contain only z")
    if not isinstance(surrogate, dict) or set(surrogate) != {"zhat"}:
        raise FixtureInputError("surrogate must contain only zhat")
    z = fraction_from_record(reference["z"], "reference.z")
    zhat = fraction_from_record(surrogate["zhat"], "surrogate.zhat")
    interface_error = abs(zhat - z)
    if interface_error == 0:
        raise FixtureInputError("interface error must be nonzero")
    tolerance = fraction_from_record(
        specification.get("tolerance"), "tolerance"
    )

    hosts = specification.get("hosts")
    if not isinstance(hosts, dict) or set(hosts) != {"HOST-A", "HOST-B"}:
        raise FixtureInputError("hosts must contain exactly HOST-A and HOST-B")
    host_results: dict[str, Any] = {}
    host_hashes: dict[str, str] = {}
    for host_id in ("HOST-A", "HOST-B"):
        host_spec = hosts[host_id]
        if not isinstance(host_spec, dict):
            raise FixtureInputError(f"{host_id} must be an object")
        if host_spec.get("host_id") != host_id:
            raise FixtureInputError(f"{host_id} has a stale host_id")
        host_hashes[host_id] = sha256(canonical_bytes(host_spec))
        host_results[host_id] = compute_host(
            host_spec,
            z,
            zhat,
            initial_reference_state,
            initial_surrogate_state,
            horizon,
            tolerance,
        )

    generator_bytes = Path(__file__).read_bytes()
    checker_bytes = CHECKER.read_bytes()
    schema_bytes = SCHEMA.read_bytes()
    candidate_material = {
        "hosts": hosts,
        "initial_reference_state": specification["initial_reference_state"],
        "initial_surrogate_state": specification["initial_surrogate_state"],
        "recurrence": specification["recurrence"],
        "reference": reference,
        "surrogate": surrogate,
    }
    data_material = {
        "reason": DATA_REASON,
        "status": DATA_STATUS,
    }
    analysis_material = {
        "checker_sha256": sha256(checker_bytes),
        "generator_sha256": sha256(generator_bytes),
        "schema_sha256": sha256(schema_bytes),
        "serialization": SERIALIZATION,
    }
    contract_material = {
        "claim": CLAIM,
        "claim_id": CLAIM_ID,
        "fixture_id": FIXTURE_ID,
        "input_sha256": sha256(input_bytes),
    }
    record = {
        "arithmetic_model": ARITHMETIC_MODEL,
        "claim": CLAIM,
        "claim_id": CLAIM_ID,
        "claim_sha256": sha256(CLAIM.encode("utf-8")),
        "command": SAFE_COMMAND,
        "environment": environment,
        "evidence_identity": {
            "analysis": {
                "analysis_sha256": sha256(canonical_bytes(analysis_material)),
                **analysis_material,
            },
            "candidate": {
                "candidate_sha256": sha256(
                    canonical_bytes(candidate_material)
                ),
                "host_sha256": host_hashes,
            },
            "contract": {
                "contract_sha256": sha256(
                    canonical_bytes(contract_material)
                ),
                **contract_material,
            },
            "data": {
                "data_sha256": sha256(canonical_bytes(data_material)),
                **data_material,
            },
            "environment": {
                "environment_sha256": sha256(
                    canonical_bytes(environment)
                ),
            },
        },
        "fixture_id": FIXTURE_ID,
        "hosts": host_results,
        "receipt_schema": RECEIPT_SCHEMA,
        "result": "host_relative_tolerance_disposition_confirmed",
        "self_hash_policy": SELF_HASH_POLICY,
        "specification": {
            "horizon": horizon,
            "initial_error": fraction_text(initial_error),
            "initial_reference_state": fraction_text(
                initial_reference_state
            ),
            "initial_surrogate_state": fraction_text(
                initial_surrogate_state
            ),
            "interface_error": fraction_text(interface_error),
            "reference_z": fraction_text(z),
            "surrogate_zhat": fraction_text(zhat),
            "tolerance": fraction_text(tolerance),
        },
        "working_directory": "repository root",
    }
    return record


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_coupled_surrogate.py RECEIPT.json")

    destination = Path(sys.argv[1]).expanduser().resolve()
    if destination == RETAINED_RECEIPT.resolve():
        raise SystemExit("refusing to overwrite the retained verification receipt")

    try:
        record = build_receipt()
    except (OSError, FixtureInputError) as exc:
        raise SystemExit(str(exc)) from exc

    serialized = json.dumps(
        record,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"
    try:
        with destination.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(serialized)
    except FileExistsError as exc:
        message = f"refusing to overwrite existing output: {destination}"
        raise SystemExit(message) from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
