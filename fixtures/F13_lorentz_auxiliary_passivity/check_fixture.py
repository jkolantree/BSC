#!/usr/bin/env python3
"""Independently verify the retained F13 Lorentz passivity receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


FIXTURE_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = FIXTURE_DIR.parents[1]
FRAMEWORK_PATH = REPOSITORY_ROOT / "framework" / "Lorentz_Auxiliary_State_Passivity.md"
INPUT_PATH = FIXTURE_DIR / "input.json"
RECEIPT_PATH = FIXTURE_DIR / "verification_receipt.json"

INPUT_SCHEMA = "bsc-lorentz-passivity-input/1"
RECEIPT_SCHEMA = "bsc-lorentz-passivity-receipt/1"
CLAIM_ID = "BSC-EM-12"
FIXTURE_CLAIM_ID = "BSC-FIX-13"
FIXTURE_ID = "F13-LORENTZ-AUXILIARY-PASSIVITY"
EVIDENCE_STATUS = "independent_reconstruction"
REPLAY_STATUS = "NOT_REPLAYED"
THEOREM_SCOPE = "real_scalar_isotropic_fixed_domain_conditional_identity"
FIXTURE_SCOPE = (
    "exact_symbolic_identity_and_finite_energy_ledgers_not_continuous_pde_execution"
)
CASE_SCOPE = "exact_finite_energy_ledger_not_pde_execution"
SPATIAL_PROFILE = "uniform_normalized_cell"
SCHEMA_ID = "urn:bsc:fixture:f13:lorentz-auxiliary-passivity:receipt:1"
SCHEMA_DRAFT = "https://json-schema.org/draft/2020-12/schema"
EXPECTED_SCHEMA_SHA256 = (
    "d986b17cb09d763deb7c566a14b663d59d67f1e9392aaaeefaf88734900da2bc"
)
EXPECTED_CASE_IDS = (
    "fixed_dissipative",
    "fixed_lossless",
    "varying_b_pump",
    "varying_a_pump",
)
SERIALIZATION = "UTF-8 JSON, two-space indentation, sorted keys, LF terminator"

EXPECTED_SIGN_CONVENTION = {
    "background_storage_excludes_polarization": True,
    "coupled_pointwise_fixed": (
        "d_t(u_EM + W) + div S = -E J_free - gamma V^2/a"
    ),
    "coupled_pointwise_varying": (
        "d_t(u_EM + W) + div S = -E J_free - gamma V^2/a + q_pump"
    ),
    "inward_port_power": "negative_outward_flux",
    "maxwell_pointwise": "d_t u_EM + div S = -E J_free - E V",
    "outward_flux": "positive_outward",
}
EXPECTED_UNIT_CONVENTION = {
    "absolute_physical_energy_claim": False,
    "kind": "normalized_symbolic_and_exact_rational_ledger",
    "physical_parameter_bridge": "not_supplied",
}
EXPECTED_PROVENANCE = {
    "blocked_promotions": [
        "absolute_physical_energy",
        "device_efficiency",
        "empirical_validation",
        "historical_replay",
        "kernel_verification",
        "magnetic_switching",
        "mechanical_replay",
        "memory_performance",
        "novelty",
        "priority",
    ],
    "classification": "independent_reconstruction",
    "external_code_or_data_reuse": "none",
    "external_source_dependency": "none",
    "historical_replay_status": "NOT_REPLAYED",
    "kernel_verification_status": "not_kernel_verified",
    "mechanical_replay_status": "not_mechanically_replayed",
    "roadmap_scope": "item_9_auxiliary_state_storage_bullet_only",
    "source_redistribution": "none",
}

SYMBOLS = (
    "a",
    "b",
    "gamma",
    "a_dot",
    "b_dot",
    "P",
    "V",
    "E",
    "J_free",
    "u_dot",
    "div_S",
)
SYMBOL_POSITION = {symbol: position for position, symbol in enumerate(SYMBOLS)}
PowerProduct = tuple[int, ...]
SparsePolynomial = dict[PowerProduct, Fraction]


class VerificationError(ValueError):
    """Raised when retained evidence fails a verification obligation."""


@dataclass(frozen=True)
class LedgerCase:
    case_id: str
    parameter_mode: str
    classification: str
    a: Fraction
    b: Fraction
    gamma: Fraction
    a_dot: Fraction
    b_dot: Fraction
    p: Fraction
    v: Fraction
    e: Fraction
    j_free: Fraction
    spatial_measure: Fraction
    em_energy_rate: Fraction
    outward_flux: Fraction
    declared_pump: Fraction
    document: dict[str, Any]


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reject_float(token: str) -> None:
    raise VerificationError(f"floating-point JSON number is forbidden: {token}")


def reject_constant(token: str) -> None:
    raise VerificationError(f"nonfinite JSON constant is forbidden: {token}")


def unique_mapping(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key, value in pairs:
        if key in mapping:
            raise VerificationError(f"duplicate JSON key: {key}")
        mapping[key] = value
    return mapping


def load_json(path: Path, label: str) -> tuple[bytes, Any]:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise VerificationError(f"{label} contains a forbidden BOM")
    if b"\r" in data:
        raise VerificationError(f"{label} must use LF line endings")
    try:
        source = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"{label} is not strict UTF-8") from exc
    try:
        value = json.loads(
            source,
            object_pairs_hook=unique_mapping,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as exc:
        raise VerificationError(f"{label} is invalid JSON: {exc}") from exc
    if data != canonical_bytes(value):
        raise VerificationError(f"{label} is not canonical JSON")
    return data, value


def load_namespace_json(path: Path) -> Any:
    """Parse existing fixture inputs strictly without imposing F13 formatting."""
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise VerificationError(f"fixture namespace input {path} contains a forbidden BOM")
    try:
        source = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"fixture namespace input {path} is not strict UTF-8") from exc
    try:
        return json.loads(
            source,
            object_pairs_hook=unique_mapping,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as exc:
        raise VerificationError(f"fixture namespace input {path} is invalid JSON: {exc}") from exc


def closed_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VerificationError(f"{label} must be an object")
    actual = set(value)
    if actual != keys:
        raise VerificationError(
            f"{label} keys mismatch: missing={sorted(keys - actual)}, "
            f"extra={sorted(actual - keys)}"
        )
    return value


def integer(value: Any, label: str) -> int:
    if type(value) is not int:
        raise VerificationError(f"{label} must be an integer")
    return value


def rational(value: Any, label: str) -> Fraction:
    item = closed_object(value, {"denominator", "numerator"}, label)
    numerator = integer(item["numerator"], f"{label}.numerator")
    denominator = integer(item["denominator"], f"{label}.denominator")
    if denominator <= 0:
        raise VerificationError(f"{label} denominator must be positive")
    if math.gcd(abs(numerator), denominator) != 1:
        raise VerificationError(f"{label} is not reduced")
    if numerator == 0 and denominator != 1:
        raise VerificationError(f"{label} has a noncanonical zero")
    return Fraction(numerator, denominator)


def rational_json(value: Fraction) -> dict[str, int]:
    return {"denominator": value.denominator, "numerator": value.numerator}


def resolve_reference(root: dict[str, Any], reference: str) -> Any:
    if not reference.startswith("#/"):
        raise VerificationError(f"unsupported schema reference: {reference}")
    node: Any = root
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or part not in node:
            raise VerificationError(f"unresolved schema reference: {reference}")
        node = node[part]
    return node


def schema_type_matches(value: Any, declared: str) -> bool:
    if declared == "object":
        return isinstance(value, dict)
    if declared == "array":
        return isinstance(value, list)
    if declared == "string":
        return isinstance(value, str)
    if declared == "integer":
        return type(value) is int
    if declared == "boolean":
        return type(value) is bool
    return False


def validate_instance(value: Any, schema: Any, root: dict[str, Any], label: str) -> None:
    if not isinstance(schema, dict):
        raise VerificationError(f"{label}: schema node must be an object")
    if "$ref" in schema:
        if set(schema) != {"$ref"}:
            raise VerificationError(f"{label}: sibling keywords beside $ref are unsupported")
        validate_instance(value, resolve_reference(root, schema["$ref"]), root, label)
        return
    declared_type = schema.get("type")
    if declared_type is not None:
        if not isinstance(declared_type, str) or not schema_type_matches(value, declared_type):
            raise VerificationError(f"{label}: expected schema type {declared_type}")
    if "const" in schema and value != schema["const"]:
        raise VerificationError(f"{label}: const mismatch")
    if "enum" in schema and value not in schema["enum"]:
        raise VerificationError(f"{label}: enum mismatch")
    if "minimum" in schema:
        if type(value) is not int or value < schema["minimum"]:
            raise VerificationError(f"{label}: minimum violated")

    if declared_type == "object":
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        if not isinstance(properties, dict) or not isinstance(required, list):
            raise VerificationError(f"{label}: malformed object schema")
        for key in required:
            if key not in value:
                raise VerificationError(f"{label}: missing required key {key}")
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                raise VerificationError(f"{label}: additional keys {sorted(extra)}")
        for key, child in value.items():
            if key in properties:
                validate_instance(child, properties[key], root, f"{label}.{key}")
    elif declared_type == "array":
        if "minItems" in schema and len(value) < schema["minItems"]:
            raise VerificationError(f"{label}: too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise VerificationError(f"{label}: too many items")
        if "items" in schema:
            for index, item in enumerate(value):
                validate_instance(item, schema["items"], root, f"{label}[{index}]")


def validate_schema_document(schema_bytes: bytes, value: Any) -> dict[str, Any]:
    if digest(schema_bytes) != EXPECTED_SCHEMA_SHA256:
        raise VerificationError("schema hash differs from the pinned identity")
    schema = closed_object(
        value,
        {"$defs", "$id", "$schema", "additionalProperties", "properties", "required", "type"},
        "schema",
    )
    if schema["$id"] != SCHEMA_ID or schema["$schema"] != SCHEMA_DRAFT:
        raise VerificationError("schema identity mismatch")
    if schema["type"] != "object" or schema["additionalProperties"] is not False:
        raise VerificationError("schema root is not a closed object")
    return schema


def parse_case(value: Any, index: int) -> LedgerCase:
    label = f"input.cases[{index}]"
    record = closed_object(
        value,
        {
            "a",
            "a_dot",
            "b",
            "b_dot",
            "case_id",
            "case_scope",
            "classification",
            "declared_pump_rate",
            "e",
            "em_energy_rate_integral",
            "gamma",
            "j_free",
            "outward_flux_integral",
            "p",
            "parameter_mode",
            "spatial_measure",
            "v",
        },
        label,
    )
    if record["case_id"] != EXPECTED_CASE_IDS[index]:
        raise VerificationError(f"{label}.case_id mismatch")
    if record["case_scope"] != CASE_SCOPE:
        raise VerificationError(f"{label}.case_scope promotes finite evidence")

    mode = record["parameter_mode"]
    if mode not in {"fixed", "time_varying"}:
        raise VerificationError(f"{label}.parameter_mode invalid")
    a = rational(record["a"], f"{label}.a")
    b = rational(record["b"], f"{label}.b")
    gamma = rational(record["gamma"], f"{label}.gamma")
    a_dot = rational(record["a_dot"], f"{label}.a_dot")
    b_dot = rational(record["b_dot"], f"{label}.b_dot")
    p = rational(record["p"], f"{label}.p")
    v = rational(record["v"], f"{label}.v")
    e = rational(record["e"], f"{label}.e")
    j_free = rational(record["j_free"], f"{label}.j_free")
    measure = rational(record["spatial_measure"], f"{label}.spatial_measure")
    em_rate = rational(
        record["em_energy_rate_integral"], f"{label}.em_energy_rate_integral"
    )
    outward = rational(
        record["outward_flux_integral"], f"{label}.outward_flux_integral"
    )
    declared_pump = rational(
        record["declared_pump_rate"], f"{label}.declared_pump_rate"
    )
    if a <= 0 or b <= 0:
        raise VerificationError(f"{label}: storage coefficients must be positive")
    if gamma < 0:
        raise VerificationError(f"{label}: negative gamma is active, not passive")
    if measure <= 0:
        raise VerificationError(f"{label}: spatial measure must be positive")

    if mode == "fixed":
        if a_dot != 0 or b_dot != 0:
            raise VerificationError(f"{label}: fixed coefficients have nonzero derivative")
        classification = "passive_lossless" if gamma == 0 else "passive_dissipative"
    else:
        if a_dot == 0 and b_dot == 0:
            raise VerificationError(f"{label}: time-varying case has no modulation")
        classification = (
            "pump_accounted_lossless" if gamma == 0 else "pump_accounted_dissipative"
        )
    if record["classification"] != classification:
        raise VerificationError(f"{label}: classification mismatch")

    computed_pump = (
        b_dot * p * p / (2 * a)
        - a_dot * (v * v + b * p * p) / (2 * a * a)
    )
    if computed_pump != declared_pump:
        raise VerificationError(f"{label}: omitted or sign-flipped pump term")

    return LedgerCase(
        case_id=record["case_id"],
        parameter_mode=mode,
        classification=classification,
        a=a,
        b=b,
        gamma=gamma,
        a_dot=a_dot,
        b_dot=b_dot,
        p=p,
        v=v,
        e=e,
        j_free=j_free,
        spatial_measure=measure,
        em_energy_rate=em_rate,
        outward_flux=outward,
        declared_pump=declared_pump,
        document=record,
    )


def parse_input(value: Any) -> list[LedgerCase]:
    root = closed_object(
        value,
        {
            "arithmetic_field",
            "cases",
            "claim_id",
            "evidence_status",
            "fixture_claim_id",
            "fixture_id",
            "fixture_scope",
            "historical_replay_status",
            "schema",
            "sign_convention",
            "spatial_profile",
            "theorem_scope",
            "unit_convention",
        },
        "input",
    )
    expectations = {
        "arithmetic_field": "Q",
        "claim_id": CLAIM_ID,
        "evidence_status": EVIDENCE_STATUS,
        "fixture_claim_id": FIXTURE_CLAIM_ID,
        "fixture_id": FIXTURE_ID,
        "fixture_scope": FIXTURE_SCOPE,
        "historical_replay_status": REPLAY_STATUS,
        "schema": INPUT_SCHEMA,
        "spatial_profile": SPATIAL_PROFILE,
        "theorem_scope": THEOREM_SCOPE,
    }
    for key, expected in expectations.items():
        if root[key] != expected:
            raise VerificationError(f"input.{key} mismatch")
    if root["sign_convention"] != EXPECTED_SIGN_CONVENTION:
        raise VerificationError("input sign convention mismatch")
    if root["unit_convention"] != EXPECTED_UNIT_CONVENTION:
        raise VerificationError("input unit convention mismatch")
    raw_cases = root["cases"]
    if not isinstance(raw_cases, list) or len(raw_cases) != 4:
        raise VerificationError("input must contain four retained cases")
    cases = [parse_case(item, index) for index, item in enumerate(raw_cases)]
    if len({case.case_id for case in cases}) != 4:
        raise VerificationError("duplicate case identifiers")
    return cases


def constant(value: int | Fraction) -> SparsePolynomial:
    coefficient = Fraction(value)
    return {} if coefficient == 0 else {(0,) * len(SYMBOLS): coefficient}


def symbol(name: str) -> SparsePolynomial:
    powers = [0] * len(SYMBOLS)
    powers[SYMBOL_POSITION[name]] = 1
    return {tuple(powers): Fraction(1)}


def sum_poly(*polynomials: SparsePolynomial) -> SparsePolynomial:
    total: SparsePolynomial = {}
    for polynomial in polynomials:
        for powers, coefficient in polynomial.items():
            updated = total.get(powers, Fraction(0)) + coefficient
            if updated:
                total[powers] = updated
            elif powers in total:
                del total[powers]
    return total


def scale_poly(polynomial: SparsePolynomial, factor: int | Fraction) -> SparsePolynomial:
    coefficient = Fraction(factor)
    if coefficient == 0:
        return {}
    return {powers: coefficient * value for powers, value in polynomial.items()}


def multiply_poly(*polynomials: SparsePolynomial) -> SparsePolynomial:
    total = constant(1)
    for polynomial in polynomials:
        product_value: SparsePolynomial = {}
        for left_powers, left_coefficient in total.items():
            for right_powers, right_coefficient in polynomial.items():
                powers = tuple(
                    left + right for left, right in zip(left_powers, right_powers)
                )
                product_value[powers] = (
                    product_value.get(powers, Fraction(0))
                    + left_coefficient * right_coefficient
                )
                if product_value[powers] == 0:
                    del product_value[powers]
        total = product_value
    return total


def subtract_poly(left: SparsePolynomial, right: SparsePolynomial) -> SparsePolynomial:
    return sum_poly(left, scale_poly(right, -1))


def polynomial_json(polynomial: SparsePolynomial) -> list[dict[str, Any]]:
    terms: list[dict[str, Any]] = []
    for powers in sorted(polynomial):
        terms.append(
            {
                "coefficient": rational_json(polynomial[powers]),
                "monomial": [
                    {"exponent": exponent, "variable": variable}
                    for variable, exponent in zip(SYMBOLS, powers)
                    if exponent > 0
                ],
            }
        )
    return terms


def reconstruct_symbolic_proof() -> dict[str, Any]:
    a = symbol("a")
    b = symbol("b")
    gamma = symbol("gamma")
    a_dot = symbol("a_dot")
    b_dot = symbol("b_dot")
    p = symbol("P")
    v = symbol("V")
    e = symbol("E")
    j = symbol("J_free")
    div_s = symbol("div_S")

    p_derivative = v
    v_derivative = sum_poly(
        multiply_poly(a, e),
        scale_poly(multiply_poly(gamma, v), -1),
        scale_poly(multiply_poly(b, p), -1),
    )
    assumed_u_derivative = scale_poly(
        sum_poly(div_s, multiply_poly(e, j), multiply_poly(e, v)), -1
    )
    maxwell = sum_poly(
        assumed_u_derivative,
        div_s,
        multiply_poly(e, j),
        multiply_poly(e, v),
    )

    fixed_material = sum_poly(
        multiply_poly(v, v_derivative),
        multiply_poly(b, p, p_derivative),
        scale_poly(multiply_poly(a, e, v), -1),
        multiply_poly(gamma, v, v),
    )
    fixed_total = sum_poly(
        multiply_poly(a, assumed_u_derivative),
        multiply_poly(a, div_s),
        multiply_poly(a, e, j),
        multiply_poly(v, v_derivative),
        multiply_poly(b, p, p_derivative),
        multiply_poly(gamma, v, v),
    )

    pump_numerator = sum_poly(
        multiply_poly(a, b_dot, p, p),
        scale_poly(multiply_poly(a_dot, v, v), -1),
        scale_poly(multiply_poly(a_dot, b, p, p), -1),
    )
    varying_storage_derivative_numerator = sum_poly(
        scale_poly(multiply_poly(a, v, v_derivative), 2),
        scale_poly(multiply_poly(a, b, p, p_derivative), 2),
        pump_numerator,
    )
    varying_material = sum_poly(
        varying_storage_derivative_numerator,
        scale_poly(multiply_poly(a, a, e, v), -2),
        scale_poly(multiply_poly(a, gamma, v, v), 2),
        scale_poly(pump_numerator, -1),
    )
    varying_total = sum_poly(
        scale_poly(multiply_poly(a, a, assumed_u_derivative), 2),
        scale_poly(multiply_poly(a, a, div_s), 2),
        scale_poly(multiply_poly(a, a, e, j), 2),
        varying_storage_derivative_numerator,
        scale_poly(multiply_poly(a, gamma, v, v), 2),
        scale_poly(pump_numerator, -1),
    )
    for name, residual in (
        ("Maxwell", maxwell),
        ("fixed material", fixed_material),
        ("fixed coupled", fixed_total),
        ("varying material", varying_material),
        ("varying coupled", varying_total),
    ):
        if residual:
            raise VerificationError(f"independent symbolic reconstruction failed: {name}")

    return {
        "fixed_coupled_residual_terms": polynomial_json(fixed_total),
        "fixed_denominator_clear": "a",
        "fixed_material_residual_terms": polynomial_json(fixed_material),
        "maxwell_premise_residual_terms": polynomial_json(maxwell),
        "ring": "Q[a,b,gamma,a_dot,b_dot,P,V,E,J_free,u_dot,div_S]",
        "sampling_used": False,
        "varying_coupled_residual_terms": polynomial_json(varying_total),
        "varying_denominator_clear": "2*a^2",
        "varying_material_residual_terms": polynomial_json(varying_material),
        "varying_pump_scaled_numerator_terms": polynomial_json(pump_numerator),
    }


def reconstruct_result(case: LedgerCase) -> dict[str, Any]:
    p_dot = case.v
    v_dot = case.a * case.e - case.gamma * case.v - case.b * case.p
    storage = (case.v**2 + case.b * case.p**2) / (2 * case.a)
    polarization_power = case.e * case.v
    loss_rate = case.gamma * case.v**2 / case.a
    pump_rate = (
        case.b_dot * case.p**2 / (2 * case.a)
        - case.a_dot * (case.v**2 + case.b * case.p**2) / (2 * case.a**2)
    )
    storage_rate_balance = polarization_power - loss_rate + pump_rate
    storage_rate = (
        (case.v * v_dot + case.b * case.p * p_dot) / case.a
        + case.b_dot * case.p**2 / (2 * case.a)
        - case.a_dot * (case.v**2 + case.b * case.p**2) / (2 * case.a**2)
    )
    material_residual = storage_rate - storage_rate_balance

    measure = case.spatial_measure
    material_energy = measure * storage
    material_rate = measure * storage_rate
    free_work = measure * case.e * case.j_free
    polarization_work = measure * polarization_power
    loss = measure * loss_rate
    pump = measure * pump_rate
    maxwell_residual = case.em_energy_rate + case.outward_flux + free_work + polarization_work
    total_rate = case.em_energy_rate + material_rate
    total_residual = total_rate + case.outward_flux + free_work + loss - pump
    inward_power = -case.outward_flux
    inward_residual = total_rate - inward_power + free_work + loss - pump

    if any(value != 0 for value in (material_residual, maxwell_residual, total_residual, inward_residual)):
        raise VerificationError(f"{case.case_id}: an exact ledger residual is nonzero")
    if pump_rate != case.declared_pump:
        raise VerificationError(f"{case.case_id}: pump mismatch")

    return {
        "case_id": case.case_id,
        "case_sha256": digest(canonical_bytes(case.document)),
        "classification": case.classification,
        "integrated_balance": {
            "coupled_residual": rational_json(total_residual),
            "em_energy_rate": rational_json(case.em_energy_rate),
            "free_current_work": rational_json(free_work),
            "inward_port_power": rational_json(inward_power),
            "inward_port_residual": rational_json(inward_residual),
            "loss": rational_json(loss),
            "material_energy": rational_json(material_energy),
            "material_energy_rate": rational_json(material_rate),
            "maxwell_residual": rational_json(maxwell_residual),
            "outward_flux": rational_json(case.outward_flux),
            "polarization_work": rational_json(polarization_work),
            "pump": rational_json(pump),
            "spatial_measure": rational_json(measure),
            "total_energy_rate": rational_json(total_rate),
        },
        "material": {
            "loss_rate": rational_json(loss_rate),
            "material_residual": rational_json(material_residual),
            "polarization_power": rational_json(polarization_power),
            "pump_rate": rational_json(pump_rate),
            "storage": rational_json(storage),
            "storage_rate": rational_json(storage_rate),
            "storage_rate_balance": rational_json(storage_rate_balance),
        },
        "parameter_mode": case.parameter_mode,
        "parameters": {
            "a": rational_json(case.a),
            "a_dot": rational_json(case.a_dot),
            "b": rational_json(case.b),
            "b_dot": rational_json(case.b_dot),
            "gamma": rational_json(case.gamma),
        },
        "state": {
            "e": rational_json(case.e),
            "j_free": rational_json(case.j_free),
            "p": rational_json(case.p),
            "p_dot": rational_json(p_dot),
            "v": rational_json(case.v),
            "v_dot": rational_json(v_dot),
        },
    }


def expected_receipt(
    input_bytes: bytes,
    input_value: Any,
    schema_bytes: bytes,
    provenance_bytes: bytes,
    fixture_dir: Path,
    framework_path: Path,
) -> dict[str, Any]:
    cases = parse_input(input_value)
    generator_path = fixture_dir / "verify_lorentz_passivity.py"
    checker_path = fixture_dir / "check_fixture.py"
    for required in (generator_path, checker_path, framework_path):
        if not required.is_file():
            raise VerificationError(f"missing bound artifact: {required}")
    return {
        "arithmetic_model": "fractions.Fraction and sparse polynomial arithmetic over Q",
        "checker_sha256": digest(checker_path.read_bytes()),
        "claim_id": CLAIM_ID,
        "evidence_status": EVIDENCE_STATUS,
        "fixture_claim_id": FIXTURE_CLAIM_ID,
        "fixture_id": FIXTURE_ID,
        "fixture_scope": FIXTURE_SCOPE,
        "framework_sha256": digest(framework_path.read_bytes()),
        "generator_sha256": digest(generator_path.read_bytes()),
        "historical_replay_status": REPLAY_STATUS,
        "input_sha256": digest(input_bytes),
        "provenance_sha256": digest(provenance_bytes),
        "results": [reconstruct_result(case) for case in cases],
        "schema": RECEIPT_SCHEMA,
        "schema_sha256": digest(schema_bytes),
        "serialization": SERIALIZATION,
        "spatial_profile": SPATIAL_PROFILE,
        "symbolic_proof": reconstruct_symbolic_proof(),
        "theorem_scope": THEOREM_SCOPE,
    }


def verify_namespace_allocations(repository_root: Path) -> None:
    ledger_path = repository_root / "ledgers" / "Claim_Status_Ledger.md"
    ledger = ledger_path.read_text(encoding="utf-8")
    claim_ids: list[str] = []
    claim_row = re.compile(r"^\s*\|\s*(BSC-[A-Z0-9]+(?:-[A-Z0-9]+)*)\s*\|")
    for line in ledger.splitlines():
        match = claim_row.match(line)
        if match:
            claim_ids.append(match.group(1))
    duplicates = sorted({item for item in claim_ids if claim_ids.count(item) > 1})
    if duplicates:
        raise VerificationError(f"duplicate ledger claim identifiers: {duplicates}")
    if claim_ids.count(CLAIM_ID) != 1 or claim_ids.count(FIXTURE_CLAIM_ID) != 1:
        raise VerificationError("F13 ledger allocations are missing or duplicated")

    fixture_root = repository_root / "fixtures"
    prefix_directories: dict[int, list[str]] = {}
    for path in fixture_root.iterdir():
        if not path.is_dir():
            continue
        match = re.match(r"^F(\d+)(?:_|$)", path.name)
        if match:
            prefix_directories.setdefault(int(match.group(1)), []).append(path.name)
    collisions = {number: names for number, names in prefix_directories.items() if len(names) > 1}
    if collisions:
        raise VerificationError(f"duplicate fixture-prefix directories: {collisions}")
    if prefix_directories.get(13) != ["F13_lorentz_auxiliary_passivity"]:
        raise VerificationError("F13 directory allocation mismatch")

    runtime_locations: list[Path] = []
    for path in fixture_root.rglob("input.json"):
        value = load_namespace_json(path)
        if isinstance(value, dict) and "fixture_id" in value and not isinstance(
            value["fixture_id"], str
        ):
            raise VerificationError(f"fixture namespace input {path} has a non-string fixture_id")
        if isinstance(value, dict) and value.get("fixture_id") == FIXTURE_ID:
            runtime_locations.append(path.resolve())
    expected_runtime = (fixture_root / "F13_lorentz_auxiliary_passivity" / "input.json").resolve()
    if runtime_locations != [expected_runtime]:
        raise VerificationError("runtime fixture identifier collision")


def regenerate_and_compare(
    input_path: Path,
    expected_bytes: bytes,
    fixture_dir: Path,
    framework_path: Path,
) -> None:
    generator = fixture_dir / "verify_lorentz_passivity.py"
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="bsc-f13-check-") as first_dir, tempfile.TemporaryDirectory(
        prefix="bsc-f13-check-"
    ) as second_dir:
        outputs = [Path(first_dir) / "receipt.json", Path(second_dir) / "receipt.json"]
        for output in outputs:
            command = [
                sys.executable,
                str(generator),
                "--input",
                str(input_path),
                "--output",
                str(output),
                "--fixture-dir",
                str(fixture_dir),
                "--framework",
                str(framework_path),
            ]
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                env=environment,
            )
            if completed.returncode != 0:
                raise VerificationError(
                    "generator failed during independent regeneration: "
                    + completed.stdout.strip()
                    + completed.stderr.strip()
                )
        first = outputs[0].read_bytes()
        second = outputs[1].read_bytes()
        if first != second or first != expected_bytes:
            raise VerificationError("generator output is not byte-identical to the retained receipt")

        retained_before = first
        overwrite = subprocess.run(
            [
                sys.executable,
                str(generator),
                "--input",
                str(input_path),
                "--output",
                str(outputs[0]),
                "--fixture-dir",
                str(fixture_dir),
                "--framework",
                str(framework_path),
            ],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
        if overwrite.returncode == 0:
            raise VerificationError("generator overwrote an existing receipt")
        if outputs[0].read_bytes() != retained_before:
            raise VerificationError("failed overwrite attempt changed retained bytes")


def verify_receipt(
    input_path: Path = INPUT_PATH,
    receipt_path: Path = RECEIPT_PATH,
    fixture_dir: Path = FIXTURE_DIR,
    framework_path: Path = FRAMEWORK_PATH,
    repository_root: Path = REPOSITORY_ROOT,
    *,
    regenerate: bool = True,
    verify_namespaces: bool = True,
) -> tuple[bytes, int]:
    input_bytes, input_value = load_json(input_path, "input")
    receipt_bytes, receipt_value = load_json(receipt_path, "receipt")
    schema_bytes, schema_value = load_json(fixture_dir / "receipt.schema.json", "schema")
    provenance_bytes, provenance_value = load_json(
        fixture_dir / "provenance.json", "provenance"
    )
    schema = validate_schema_document(schema_bytes, schema_value)
    validate_instance(receipt_value, schema, schema, "receipt")
    if provenance_value != EXPECTED_PROVENANCE:
        raise VerificationError("provenance boundary mismatch")
    expected = expected_receipt(
        input_bytes,
        input_value,
        schema_bytes,
        provenance_bytes,
        fixture_dir,
        framework_path,
    )
    if receipt_value != expected:
        raise VerificationError("receipt differs from independent exact reconstruction")
    if receipt_bytes != canonical_bytes(expected):
        raise VerificationError("receipt bytes differ from canonical reconstruction")
    if verify_namespaces:
        verify_namespace_allocations(repository_root)
    if regenerate:
        regenerate_and_compare(input_path, receipt_bytes, fixture_dir, framework_path)
    return receipt_bytes, len(expected["results"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT_PATH)
    parser.add_argument("--receipt", type=Path, default=RECEIPT_PATH)
    parser.add_argument("--fixture-dir", type=Path, default=FIXTURE_DIR)
    parser.add_argument("--framework", type=Path, default=FRAMEWORK_PATH)
    parser.add_argument("--repository-root", type=Path, default=REPOSITORY_ROOT)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        _, count = verify_receipt(
            args.input.resolve(strict=True),
            args.receipt.resolve(strict=True),
            args.fixture_dir.resolve(strict=True),
            args.framework.resolve(strict=True),
            args.repository_root.resolve(strict=True),
        )
    except (OSError, VerificationError) as exc:
        print(f"{FIXTURE_ID}: FAIL: {exc}")
        return 1
    print(f"{FIXTURE_ID}: PASS: {count} exact ledgers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
