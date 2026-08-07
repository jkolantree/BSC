#!/usr/bin/env python3
"""Generate the deterministic F13 Lorentz passivity receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


FIXTURE_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = FIXTURE_DIR.parents[1]
FRAMEWORK_PATH = REPOSITORY_ROOT / "framework" / "Lorentz_Auxiliary_State_Passivity.md"

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

SIGN_CONVENTION = {
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
UNIT_CONVENTION = {
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

VARIABLES = (
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
VARIABLE_INDEX = {name: index for index, name in enumerate(VARIABLES)}
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Fraction]


class CertificateError(ValueError):
    """Raised when an input cannot support the declared certificate."""


@dataclass(frozen=True)
class Case:
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
    em_energy_rate_integral: Fraction
    outward_flux_integral: Fraction
    declared_pump_rate: Fraction
    source_document: dict[str, Any]


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _reject_constant(value: str) -> None:
    raise CertificateError(f"nonfinite JSON constant is forbidden: {value}")


def _reject_float(value: str) -> None:
    raise CertificateError(f"floating-point JSON number is forbidden: {value}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CertificateError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_canonical_json(path: Path, label: str) -> tuple[bytes, Any]:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise CertificateError(f"{label} must not contain a UTF-8 BOM")
    if b"\r" in data:
        raise CertificateError(f"{label} must use LF line endings")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise CertificateError(f"{label} is not strict UTF-8") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as exc:
        raise CertificateError(f"{label} is not valid JSON: {exc}") from exc
    if data != canonical_bytes(value):
        raise CertificateError(f"{label} is not canonical JSON")
    return data, value


def exact_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CertificateError(f"{label} must be an object")
    actual = set(value)
    if actual != keys:
        missing = sorted(keys - actual)
        extra = sorted(actual - keys)
        raise CertificateError(f"{label} keys mismatch: missing={missing}, extra={extra}")
    return value


def exact_integer(value: Any, label: str) -> int:
    if type(value) is not int:
        raise CertificateError(f"{label} must be an integer, not {type(value).__name__}")
    return value


def parse_rational(value: Any, label: str) -> Fraction:
    record = exact_object(value, {"denominator", "numerator"}, label)
    numerator = exact_integer(record["numerator"], f"{label}.numerator")
    denominator = exact_integer(record["denominator"], f"{label}.denominator")
    if denominator <= 0:
        raise CertificateError(f"{label}.denominator must be positive")
    if math.gcd(abs(numerator), denominator) != 1:
        raise CertificateError(f"{label} must be reduced")
    if numerator == 0 and denominator != 1:
        raise CertificateError(f"{label} zero must have denominator 1")
    return Fraction(numerator, denominator)


def rational_document(value: Fraction) -> dict[str, int]:
    return {"denominator": value.denominator, "numerator": value.numerator}


def validate_schema(schema_bytes: bytes, value: Any) -> None:
    if sha256(schema_bytes) != EXPECTED_SCHEMA_SHA256:
        raise CertificateError("receipt schema hash does not match the pinned identity")
    schema = exact_object(
        value,
        {"$defs", "$id", "$schema", "additionalProperties", "properties", "required", "type"},
        "receipt schema",
    )
    if schema["$id"] != SCHEMA_ID or schema["$schema"] != SCHEMA_DRAFT:
        raise CertificateError("receipt schema identity mismatch")
    if schema["type"] != "object" or schema["additionalProperties"] is not False:
        raise CertificateError("receipt schema root must be a closed object")


def validate_provenance(value: Any) -> None:
    if value != EXPECTED_PROVENANCE:
        raise CertificateError("provenance boundary mismatch")


def parse_case(value: Any, index: int) -> Case:
    label = f"input.cases[{index}]"
    record = exact_object(
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
    case_id = record["case_id"]
    if not isinstance(case_id, str) or case_id != EXPECTED_CASE_IDS[index]:
        raise CertificateError(f"{label}.case_id mismatch")
    if record["case_scope"] != CASE_SCOPE:
        raise CertificateError(f"{label}.case_scope is not fail-closed")

    mode = record["parameter_mode"]
    if mode not in {"fixed", "time_varying"}:
        raise CertificateError(f"{label}.parameter_mode is invalid")

    a = parse_rational(record["a"], f"{label}.a")
    b = parse_rational(record["b"], f"{label}.b")
    gamma = parse_rational(record["gamma"], f"{label}.gamma")
    a_dot = parse_rational(record["a_dot"], f"{label}.a_dot")
    b_dot = parse_rational(record["b_dot"], f"{label}.b_dot")
    p = parse_rational(record["p"], f"{label}.p")
    v = parse_rational(record["v"], f"{label}.v")
    e = parse_rational(record["e"], f"{label}.e")
    j_free = parse_rational(record["j_free"], f"{label}.j_free")
    measure = parse_rational(record["spatial_measure"], f"{label}.spatial_measure")
    em_rate = parse_rational(
        record["em_energy_rate_integral"], f"{label}.em_energy_rate_integral"
    )
    outward = parse_rational(
        record["outward_flux_integral"], f"{label}.outward_flux_integral"
    )
    declared_pump = parse_rational(
        record["declared_pump_rate"], f"{label}.declared_pump_rate"
    )

    if a <= 0:
        raise CertificateError(f"{label}.a must be positive")
    if b <= 0:
        raise CertificateError(f"{label}.b must be positive")
    if gamma < 0:
        raise CertificateError(f"{label}.gamma cannot be passive when negative")
    if measure <= 0:
        raise CertificateError(f"{label}.spatial_measure must be positive")

    if mode == "fixed":
        if a_dot != 0 or b_dot != 0:
            raise CertificateError(f"{label} fixed parameters must have zero derivatives")
        expected_class = "passive_lossless" if gamma == 0 else "passive_dissipative"
    else:
        if a_dot == 0 and b_dot == 0:
            raise CertificateError(f"{label} time-varying mode needs a nonzero derivative")
        expected_class = (
            "pump_accounted_lossless" if gamma == 0 else "pump_accounted_dissipative"
        )
    if record["classification"] != expected_class:
        raise CertificateError(f"{label}.classification does not match its parameters")

    pump = b_dot * p * p / (2 * a) - a_dot * (v * v + b * p * p) / (2 * a * a)
    if declared_pump != pump:
        raise CertificateError(f"{label}.declared_pump_rate omits or mis-signs pump exchange")

    return Case(
        case_id=case_id,
        parameter_mode=mode,
        classification=expected_class,
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
        em_energy_rate_integral=em_rate,
        outward_flux_integral=outward,
        declared_pump_rate=declared_pump,
        source_document=record,
    )


def parse_input(value: Any) -> list[Case]:
    root = exact_object(
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
    expected_scalars = {
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
    for key, expected in expected_scalars.items():
        if root[key] != expected:
            raise CertificateError(f"input.{key} mismatch")
    if root["sign_convention"] != SIGN_CONVENTION:
        raise CertificateError("input.sign_convention mismatch")
    if root["unit_convention"] != UNIT_CONVENTION:
        raise CertificateError("input.unit_convention mismatch")
    cases_value = root["cases"]
    if not isinstance(cases_value, list) or len(cases_value) != len(EXPECTED_CASE_IDS):
        raise CertificateError("input.cases must contain the four retained cases")
    cases = [parse_case(case, index) for index, case in enumerate(cases_value)]
    if len({case.case_id for case in cases}) != len(cases):
        raise CertificateError("duplicate case identifiers")
    return cases


def poly_constant(value: Fraction | int) -> Polynomial:
    coefficient = Fraction(value)
    if coefficient == 0:
        return {}
    return {(0,) * len(VARIABLES): coefficient}


def poly_variable(name: str) -> Polynomial:
    powers = [0] * len(VARIABLES)
    powers[VARIABLE_INDEX[name]] = 1
    return {tuple(powers): Fraction(1)}


def poly_add(*values: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for value in values:
        for monomial, coefficient in value.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
            if result[monomial] == 0:
                del result[monomial]
    return result


def poly_scale(value: Polynomial, coefficient: Fraction | int) -> Polynomial:
    factor = Fraction(coefficient)
    if factor == 0:
        return {}
    return {monomial: factor * item for monomial, item in value.items()}


def poly_subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    return poly_add(left, poly_scale(right, -1))


def poly_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                left_power + right_power
                for left_power, right_power in zip(left_monomial, right_monomial)
            )
            result[monomial] = (
                result.get(monomial, Fraction(0))
                + left_coefficient * right_coefficient
            )
            if result[monomial] == 0:
                del result[monomial]
    return result


def product(*values: Polynomial) -> Polynomial:
    result = poly_constant(1)
    for value in values:
        result = poly_multiply(result, value)
    return result


def polynomial_document(value: Polynomial) -> list[dict[str, Any]]:
    document: list[dict[str, Any]] = []
    for monomial in sorted(value):
        factors = [
            {"exponent": exponent, "variable": variable}
            for variable, exponent in zip(VARIABLES, monomial)
            if exponent
        ]
        document.append(
            {
                "coefficient": rational_document(value[monomial]),
                "monomial": factors,
            }
        )
    return document


def symbolic_proof_document() -> dict[str, Any]:
    a = poly_variable("a")
    b = poly_variable("b")
    gamma = poly_variable("gamma")
    a_dot = poly_variable("a_dot")
    b_dot = poly_variable("b_dot")
    p = poly_variable("P")
    v = poly_variable("V")
    e = poly_variable("E")
    j_free = poly_variable("J_free")
    u_dot = poly_variable("u_dot")
    div_s = poly_variable("div_S")

    p_dot = v
    v_dot = poly_subtract(
        poly_subtract(product(a, e), product(gamma, v)),
        product(b, p),
    )
    maxwell_u_substitution = poly_scale(
        poly_add(div_s, product(e, j_free), product(e, v)), -1
    )
    maxwell_residual = poly_add(
        maxwell_u_substitution,
        div_s,
        product(e, j_free),
        product(e, v),
    )

    fixed_material = poly_add(
        product(v, v_dot),
        product(b, p, p_dot),
        poly_scale(product(a, e, v), -1),
        product(gamma, v, v),
    )
    fixed_coupled = poly_add(
        product(a, maxwell_u_substitution),
        product(a, div_s),
        product(a, e, j_free),
        product(v, v_dot),
        product(b, p, p_dot),
        product(gamma, v, v),
    )

    pump_numerator = poly_add(
        product(a, b_dot, p, p),
        poly_scale(product(a_dot, v, v), -1),
        poly_scale(product(a_dot, b, p, p), -1),
    )
    varying_w_dot_numerator = poly_add(
        poly_scale(product(a, v, v_dot), 2),
        poly_scale(product(a, b, p, p_dot), 2),
        pump_numerator,
    )
    varying_material = poly_add(
        varying_w_dot_numerator,
        poly_scale(product(a, a, e, v), -2),
        poly_scale(product(a, gamma, v, v), 2),
        poly_scale(pump_numerator, -1),
    )
    varying_coupled = poly_add(
        poly_scale(product(a, a, maxwell_u_substitution), 2),
        poly_scale(product(a, a, div_s), 2),
        poly_scale(product(a, a, e, j_free), 2),
        varying_w_dot_numerator,
        poly_scale(product(a, gamma, v, v), 2),
        poly_scale(pump_numerator, -1),
    )

    for label, residual in {
        "Maxwell premise": maxwell_residual,
        "fixed material": fixed_material,
        "fixed coupled": fixed_coupled,
        "varying material": varying_material,
        "varying coupled": varying_coupled,
    }.items():
        if residual:
            raise CertificateError(f"internal symbolic construction failed: {label}")

    return {
        "fixed_coupled_residual_terms": polynomial_document(fixed_coupled),
        "fixed_denominator_clear": "a",
        "fixed_material_residual_terms": polynomial_document(fixed_material),
        "maxwell_premise_residual_terms": polynomial_document(maxwell_residual),
        "ring": "Q[a,b,gamma,a_dot,b_dot,P,V,E,J_free,u_dot,div_S]",
        "sampling_used": False,
        "varying_coupled_residual_terms": polynomial_document(varying_coupled),
        "varying_denominator_clear": "2*a^2",
        "varying_material_residual_terms": polynomial_document(varying_material),
        "varying_pump_scaled_numerator_terms": polynomial_document(pump_numerator),
    }


def result_document(case: Case) -> dict[str, Any]:
    p_dot = case.v
    v_dot = case.a * case.e - case.gamma * case.v - case.b * case.p
    storage = (case.v * case.v + case.b * case.p * case.p) / (2 * case.a)
    polarization_power = case.e * case.v
    loss_rate = case.gamma * case.v * case.v / case.a
    pump_rate = (
        case.b_dot * case.p * case.p / (2 * case.a)
        - case.a_dot
        * (case.v * case.v + case.b * case.p * case.p)
        / (2 * case.a * case.a)
    )
    storage_rate_balance = polarization_power - loss_rate + pump_rate
    storage_rate = (
        (case.v * v_dot + case.b * case.p * p_dot) / case.a
        + case.b_dot * case.p * case.p / (2 * case.a)
        - case.a_dot
        * (case.v * case.v + case.b * case.p * case.p)
        / (2 * case.a * case.a)
    )
    material_residual = storage_rate - storage_rate_balance

    measure = case.spatial_measure
    material_energy = measure * storage
    material_energy_rate = measure * storage_rate
    free_current_work = measure * case.e * case.j_free
    polarization_work = measure * polarization_power
    loss = measure * loss_rate
    pump = measure * pump_rate
    maxwell_residual = (
        case.em_energy_rate_integral
        + case.outward_flux_integral
        + free_current_work
        + polarization_work
    )
    total_energy_rate = case.em_energy_rate_integral + material_energy_rate
    coupled_residual = (
        total_energy_rate
        + case.outward_flux_integral
        + free_current_work
        + loss
        - pump
    )
    inward_port_power = -case.outward_flux_integral
    inward_port_residual = (
        total_energy_rate - inward_port_power + free_current_work + loss - pump
    )

    if material_residual != 0:
        raise CertificateError(f"{case.case_id}: material identity failed")
    if maxwell_residual != 0:
        raise CertificateError(f"{case.case_id}: Maxwell energy ledger failed")
    if coupled_residual != 0 or inward_port_residual != 0:
        raise CertificateError(f"{case.case_id}: coupled energy ledger failed")
    if pump_rate != case.declared_pump_rate:
        raise CertificateError(f"{case.case_id}: declared pump mismatch")

    return {
        "case_id": case.case_id,
        "case_sha256": sha256(canonical_bytes(case.source_document)),
        "classification": case.classification,
        "integrated_balance": {
            "coupled_residual": rational_document(coupled_residual),
            "em_energy_rate": rational_document(case.em_energy_rate_integral),
            "free_current_work": rational_document(free_current_work),
            "inward_port_power": rational_document(inward_port_power),
            "inward_port_residual": rational_document(inward_port_residual),
            "loss": rational_document(loss),
            "material_energy": rational_document(material_energy),
            "material_energy_rate": rational_document(material_energy_rate),
            "maxwell_residual": rational_document(maxwell_residual),
            "outward_flux": rational_document(case.outward_flux_integral),
            "polarization_work": rational_document(polarization_work),
            "pump": rational_document(pump),
            "spatial_measure": rational_document(measure),
            "total_energy_rate": rational_document(total_energy_rate),
        },
        "material": {
            "loss_rate": rational_document(loss_rate),
            "material_residual": rational_document(material_residual),
            "polarization_power": rational_document(polarization_power),
            "pump_rate": rational_document(pump_rate),
            "storage": rational_document(storage),
            "storage_rate": rational_document(storage_rate),
            "storage_rate_balance": rational_document(storage_rate_balance),
        },
        "parameter_mode": case.parameter_mode,
        "parameters": {
            "a": rational_document(case.a),
            "a_dot": rational_document(case.a_dot),
            "b": rational_document(case.b),
            "b_dot": rational_document(case.b_dot),
            "gamma": rational_document(case.gamma),
        },
        "state": {
            "e": rational_document(case.e),
            "j_free": rational_document(case.j_free),
            "p": rational_document(case.p),
            "p_dot": rational_document(p_dot),
            "v": rational_document(case.v),
            "v_dot": rational_document(v_dot),
        },
    }


def generate_receipt(
    input_path: Path,
    fixture_dir: Path = FIXTURE_DIR,
    framework_path: Path = FRAMEWORK_PATH,
) -> dict[str, Any]:
    input_bytes, input_value = load_canonical_json(input_path, "input")
    provenance_path = fixture_dir / "provenance.json"
    schema_path = fixture_dir / "receipt.schema.json"
    generator_path = fixture_dir / "verify_lorentz_passivity.py"
    checker_path = fixture_dir / "check_fixture.py"
    provenance_bytes, provenance_value = load_canonical_json(provenance_path, "provenance")
    schema_bytes, schema_value = load_canonical_json(schema_path, "receipt schema")
    validate_provenance(provenance_value)
    validate_schema(schema_bytes, schema_value)
    cases = parse_input(input_value)

    for required in (framework_path, generator_path, checker_path):
        if not required.is_file():
            raise CertificateError(f"bound artifact is missing: {required}")

    return {
        "arithmetic_model": "fractions.Fraction and sparse polynomial arithmetic over Q",
        "checker_sha256": sha256(checker_path.read_bytes()),
        "claim_id": CLAIM_ID,
        "evidence_status": EVIDENCE_STATUS,
        "fixture_claim_id": FIXTURE_CLAIM_ID,
        "fixture_id": FIXTURE_ID,
        "fixture_scope": FIXTURE_SCOPE,
        "framework_sha256": sha256(framework_path.read_bytes()),
        "generator_sha256": sha256(generator_path.read_bytes()),
        "historical_replay_status": REPLAY_STATUS,
        "input_sha256": sha256(input_bytes),
        "provenance_sha256": sha256(provenance_bytes),
        "results": [result_document(case) for case in cases],
        "schema": RECEIPT_SCHEMA,
        "schema_sha256": sha256(schema_bytes),
        "serialization": SERIALIZATION,
        "spatial_profile": SPATIAL_PROFILE,
        "symbolic_proof": symbolic_proof_document(),
        "theorem_scope": THEOREM_SCOPE,
    }


def write_exclusive(path: Path, data: bytes) -> None:
    try:
        with path.open("xb") as stream:
            stream.write(data)
    except FileExistsError as exc:
        raise CertificateError(f"refusing to overwrite existing output: {path}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=FIXTURE_DIR / "input.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fixture-dir", type=Path, default=FIXTURE_DIR)
    parser.add_argument("--framework", type=Path, default=FRAMEWORK_PATH)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        input_path = args.input.resolve(strict=True)
        fixture_dir = args.fixture_dir.resolve(strict=True)
        framework_path = args.framework.resolve(strict=True)
        output_path = args.output.resolve(strict=False)
        bound_inputs = {
            input_path,
            framework_path,
            *(path.resolve(strict=True) for path in (
                fixture_dir / "provenance.json",
                fixture_dir / "receipt.schema.json",
                fixture_dir / "verify_lorentz_passivity.py",
                fixture_dir / "check_fixture.py",
            )),
        }
        if output_path in bound_inputs:
            raise CertificateError("output path aliases a bound input artifact")
        receipt = generate_receipt(input_path, fixture_dir, framework_path)
        write_exclusive(output_path, canonical_bytes(receipt))
    except (CertificateError, OSError) as exc:
        print(f"{FIXTURE_ID}: FAIL: {exc}")
        return 1
    print(f"{FIXTURE_ID}: GENERATED: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
