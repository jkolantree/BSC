#!/usr/bin/env python3
"""Independent fail-closed verifier for exact-Q derived-holonomy F12."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
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
GENERATOR = FIXTURE_DIR / "verify_derived_holonomy.py"
DEFAULT_INPUT = FIXTURE_DIR / "input.json"
DEFAULT_RECEIPT = FIXTURE_DIR / "verification_receipt.json"
PROVENANCE = FIXTURE_DIR / "provenance.json"
SCHEMA = FIXTURE_DIR / "receipt.schema.json"

INPUT_SCHEMA = "bsc-derived-holonomy-input/1"
CERTIFICATE_SCHEMA = "bsc-derived-holonomy-certificate/1"
CLAIM_ID = "BSC-DHC-01"
FIXTURE_CLAIM_ID = "BSC-FIX-12"
FIXTURE_ID = "F12-DERIVED-HOLONOMY-Q"
EVIDENCE_STATUS = "independent_reconstruction"
HISTORICAL_REPLAY_STATUS = "NOT_REPLAYED"
ARITHMETIC_MODEL = "fractions.Fraction exact rational arithmetic over Q"
SERIALIZATION = "UTF-8 JSON, two-space indentation, sorted keys, LF terminator"
SCHEMA_ID = "urn:bsc:fixture:f12:derived-holonomy-q:receipt:1"
SCHEMA_DRAFT = "https://json-schema.org/draft/2020-12/schema"
EXPECTED_SCHEMA_SHA256 = (
    "2a7c387033a3f94dcbaba18ff72ac9e72b04bfbfed74056dce68c6c022fc203e"
)
SUPPORTED_SCHEMA_KEYWORDS = {
    "$defs",
    "$id",
    "$ref",
    "$schema",
    "additionalProperties",
    "const",
    "enum",
    "items",
    "minimum",
    "minItems",
    "oneOf",
    "pattern",
    "properties",
    "required",
    "title",
    "type",
}
SUPPORTED_JSON_TYPES = {"array", "integer", "object", "string"}
EXPECTED_FIXTURE_ALLOCATIONS = {
    "F09": "fixtures/F09_zeta_dqpt_transfer/input.json",
    "F10-COUPLED-SURROGATE": "fixtures/F10_coupled_surrogate/input.json",
    "F11-COLLATZ-RECURSIVE-SIEVE": (
        "fixtures/F11_collatz_recursive_sieve/input.json"
    ),
    FIXTURE_ID: "fixtures/F12_derived_holonomy_q/input.json",
}
EXPECTED_PREFIX_DIRECTORIES = {
    "F09": "F09_zeta_dqpt_transfer",
    "F10": "F10_coupled_surrogate",
    "F11": "F11_collatz_recursive_sieve",
    "F12": "F12_derived_holonomy_q",
}


class VerificationError(ValueError):
    """Raised when an F12 artifact fails independent verification."""


@dataclass(frozen=True)
class Matrix:
    rows: int
    columns: int
    entries: tuple[tuple[Fraction, ...], ...]


@dataclass(frozen=True)
class Complex:
    minimum: int
    maximum: int
    dimensions: tuple[int, ...]
    differentials: tuple[Matrix, ...]

    def dimension(self, degree: int) -> int:
        if degree < self.minimum or degree > self.maximum:
            return 0
        return self.dimensions[degree - self.minimum]

    def differential(self, degree: int) -> Matrix:
        rows = self.dimension(degree - 1)
        columns = self.dimension(degree)
        if degree <= self.minimum or degree > self.maximum:
            return zeros(rows, columns)
        return self.differentials[degree - self.minimum - 1]


@dataclass(frozen=True)
class Problem:
    case_id: str
    source: Complex
    target: Complex
    f: tuple[Matrix, ...]
    g: tuple[Matrix, ...]
    document: dict[str, Any]


@dataclass(frozen=True)
class ReconstructedSystem:
    matrix: Matrix
    omega: tuple[Fraction, ...]
    rows: tuple[tuple[int, int, int], ...]
    columns: tuple[tuple[int, int, int], ...]


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reject_constant(value: str) -> None:
    raise VerificationError(f"non-finite JSON number is forbidden: {value}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def load_json(path: Path, label: str) -> tuple[bytes, Any]:
    try:
        data = path.read_bytes()
        value = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"cannot read {label}: {exc}") from exc
    if data != canonical_bytes(value):
        raise VerificationError(f"{label} is not canonical {SERIALIZATION}")
    return data, value


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


def resolve_schema_reference(
    reference: Any, root: dict[str, Any], location: str
) -> dict[str, Any]:
    prefix = "#/$defs/"
    if not isinstance(reference, str) or not reference.startswith(prefix):
        raise VerificationError(f"{location}: unsupported schema reference")
    name = reference[len(prefix):]
    definitions = root.get("$defs")
    if not name or "/" in name or not isinstance(definitions, dict):
        raise VerificationError(f"{location}: unsupported schema reference")
    target = definitions.get(name)
    if not isinstance(target, dict):
        raise VerificationError(f"{location}: unresolved schema reference")
    return target


def validate_schema_definition(
    schema: Any,
    root: dict[str, Any] | None = None,
    location: str = "$",
) -> None:
    if not isinstance(schema, dict):
        raise VerificationError(f"{location}: schema node must be an object")
    if root is None:
        root = schema
    unknown = set(schema) - SUPPORTED_SCHEMA_KEYWORDS
    if unknown:
        raise VerificationError(
            f"{location}: unsupported schema keywords: {sorted(unknown)}"
        )
    if "$ref" in schema:
        if set(schema) != {"$ref"}:
            raise VerificationError(
                f"{location}: schema reference must be the only keyword"
            )
        resolve_schema_reference(schema["$ref"], root, location)
        return
    definitions = schema.get("$defs")
    if definitions is not None:
        if location != "$" or not isinstance(definitions, dict) or not definitions:
            raise VerificationError(f"{location}: invalid schema definitions")
        for name, subschema in definitions.items():
            if not isinstance(name, str) or not name:
                raise VerificationError(
                    f"{location}: invalid schema definition name"
                )
            validate_schema_definition(subschema, root, f"{location}.$defs.{name}")
    declared_type = schema.get("type")
    if declared_type is not None and declared_type not in SUPPORTED_JSON_TYPES:
        raise VerificationError(
            f"{location}: unsupported type declaration: {declared_type!r}"
        )
    required = schema.get("required")
    if required is not None and (
        not isinstance(required, list)
        or not all(isinstance(item, str) for item in required)
        or len(required) != len(set(required))
    ):
        raise VerificationError(
            f"{location}: required must contain unique strings"
        )
    properties = schema.get("properties")
    if properties is not None:
        if not isinstance(properties, dict) or not all(
            isinstance(key, str) for key in properties
        ):
            raise VerificationError(f"{location}: properties must be an object")
        if required is not None and not set(required).issubset(properties):
            raise VerificationError(
                f"{location}: required names must have property schemas"
            )
        for key, subschema in properties.items():
            validate_schema_definition(subschema, root, f"{location}.{key}")
    additional = schema.get("additionalProperties")
    if additional is not None and not isinstance(additional, bool):
        raise VerificationError(
            f"{location}: additionalProperties must be Boolean"
        )
    items = schema.get("items")
    if items is not None:
        validate_schema_definition(items, root, f"{location}[]")
    branches = schema.get("oneOf")
    if branches is not None:
        if not isinstance(branches, list) or len(branches) < 2:
            raise VerificationError(
                f"{location}: oneOf needs at least two branches"
            )
        for index, branch in enumerate(branches):
            validate_schema_definition(branch, root, f"{location}.oneOf[{index}]")
    choices = schema.get("enum")
    if choices is not None and (not isinstance(choices, list) or not choices):
        raise VerificationError(f"{location}: enum must be a nonempty array")
    for key in ("minimum", "minItems"):
        if key in schema and (type(schema[key]) is not int or schema[key] < 0):
            raise VerificationError(
                f"{location}: {key} must be a nonnegative integer"
            )
    pattern = schema.get("pattern")
    if pattern is not None:
        if not isinstance(pattern, str):
            raise VerificationError(f"{location}: pattern must be a string")
        try:
            re.compile(pattern)
        except re.error as exc:
            raise VerificationError(f"{location}: invalid pattern: {exc}") from exc


def instance_has_type(instance: Any, declared_type: str) -> bool:
    return {
        "array": lambda value: isinstance(value, list),
        "integer": lambda value: type(value) is int,
        "object": lambda value: isinstance(value, dict),
        "string": lambda value: isinstance(value, str),
    }[declared_type](instance)


def validate_schema_instance(
    instance: Any,
    schema: dict[str, Any],
    root: dict[str, Any],
    location: str = "$",
) -> None:
    if "$ref" in schema:
        validate_schema_instance(
            instance,
            resolve_schema_reference(schema["$ref"], root, location),
            root,
            location,
        )
        return
    branches = schema.get("oneOf")
    if branches is not None:
        matches = 0
        for branch in branches:
            try:
                validate_schema_instance(instance, branch, root, location)
            except VerificationError:
                continue
            matches += 1
        if matches != 1:
            raise VerificationError(
                f"{location}: schema polarity/shape oneOf matched {matches} branches"
            )
    declared_type = schema.get("type")
    if declared_type is not None and not instance_has_type(instance, declared_type):
        raise VerificationError(
            f"{location}: expected {declared_type}, got {type(instance).__name__}"
        )
    if "const" in schema and not json_equal(instance, schema["const"]):
        raise VerificationError(
            f"{location}: value does not match declared constant"
        )
    choices = schema.get("enum")
    if choices is not None and not any(json_equal(instance, item) for item in choices):
        raise VerificationError(f"{location}: value is outside the declared enum")
    pattern = schema.get("pattern")
    if pattern is not None and (
        not isinstance(instance, str) or re.fullmatch(pattern, instance) is None
    ):
        raise VerificationError(f"{location}: string does not match {pattern!r}")
    minimum = schema.get("minimum")
    if minimum is not None and (type(instance) is not int or instance < minimum):
        raise VerificationError(f"{location}: value is below minimum {minimum}")
    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        missing = sorted(set(required) - set(instance))
        if missing:
            raise VerificationError(
                f"{location}: missing required properties: {missing}"
            )
        if schema.get("additionalProperties") is False:
            extras = sorted(set(instance) - set(properties))
            if extras:
                raise VerificationError(
                    f"{location}: unexpected properties: {extras}"
                )
        for key, subschema in properties.items():
            if key in instance:
                validate_schema_instance(
                    instance[key], subschema, root, f"{location}.{key}"
                )
    if isinstance(instance, list):
        minimum_items = schema.get("minItems")
        if minimum_items is not None and len(instance) < minimum_items:
            raise VerificationError(
                f"{location}: array has fewer than {minimum_items} items"
            )
        items = schema.get("items")
        if items is not None:
            for index, item in enumerate(instance):
                validate_schema_instance(item, items, root, f"{location}[{index}]")


def validate_schema_document(schema_bytes: bytes, schema: Any) -> dict[str, Any]:
    if digest(schema_bytes) != EXPECTED_SCHEMA_SHA256:
        raise VerificationError("receipt schema digest mismatch")
    if not isinstance(schema, dict):
        raise VerificationError("receipt schema must be an object")
    validate_schema_definition(schema)
    if schema.get("$id") != SCHEMA_ID or schema.get("$schema") != SCHEMA_DRAFT:
        raise VerificationError("receipt schema identity mismatch")
    return schema


def read_namespace_input(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise VerificationError(
            f"cannot inspect fixture namespace input {path}: {exc}"
        ) from exc


def verify_namespace_allocations(repository_root: Path = REPOSITORY_ROOT) -> None:
    ledger = repository_root / "ledgers" / "Claim_Status_Ledger.md"
    try:
        ledger_text = ledger.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise VerificationError(f"cannot inspect claim namespace ledger: {exc}") from exc
    definition_ids: list[str] = []
    for line in ledger_text.splitlines():
        if not line.startswith("| BSC-"):
            continue
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) >= 3:
            definition_ids.append(cells[1])
    for identifier in (
        CLAIM_ID,
        "BSC-FIX-09",
        "BSC-FIX-10",
        "BSC-FIX-11",
        FIXTURE_CLAIM_ID,
    ):
        count = definition_ids.count(identifier)
        if count != 1:
            raise VerificationError(
                f"namespace collision: {identifier} has {count} defining ledger rows"
            )

    fixtures_root = repository_root / "fixtures"
    allocations: dict[str, list[str]] = {}
    for input_path in sorted(fixtures_root.rglob("input.json")):
        value = read_namespace_input(input_path)
        if not isinstance(value, dict) or "fixture_id" not in value:
            continue
        fixture_id = value["fixture_id"]
        if not isinstance(fixture_id, str):
            raise VerificationError(
                f"fixture namespace identifier is not a string: {input_path}"
            )
        relative = input_path.relative_to(repository_root).as_posix()
        allocations.setdefault(fixture_id, []).append(relative)
    for fixture_id, expected_path in EXPECTED_FIXTURE_ALLOCATIONS.items():
        actual_paths = allocations.get(fixture_id, [])
        if actual_paths != [expected_path]:
            raise VerificationError(
                f"namespace collision: {fixture_id} allocations are {actual_paths}, "
                f"expected [{expected_path!r}]"
            )

    prefix_directories: dict[str, list[str]] = {}
    try:
        fixture_directories = sorted(
            path for path in fixtures_root.iterdir() if path.is_dir()
        )
    except OSError as exc:
        raise VerificationError(f"cannot inspect fixture directories: {exc}") from exc
    for directory in fixture_directories:
        match = re.match(r"^(F[0-9]+)(?:_|$)", directory.name)
        if match:
            prefix_directories.setdefault(match.group(1), []).append(directory.name)
    for prefix, expected_directory in EXPECTED_PREFIX_DIRECTORIES.items():
        actual_directories = prefix_directories.get(prefix, [])
        if actual_directories != [expected_directory]:
            raise VerificationError(
                f"namespace collision: {prefix} directories are {actual_directories}, "
                f"expected [{expected_directory!r}]"
            )


def exact_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VerificationError(f"{label} must be an object")
    if set(value) != keys:
        raise VerificationError(
            f"{label} keys are not exact; "
            f"missing={sorted(keys - set(value))}, extras={sorted(set(value) - keys)}"
        )
    return value


def integer(value: Any, label: str) -> int:
    if type(value) is not int:
        raise VerificationError(f"{label} must be a JSON integer")
    return value


def rational(value: Any, label: str) -> Fraction:
    obj = exact_object(value, {"denominator", "numerator"}, label)
    numerator = integer(obj["numerator"], f"{label}.numerator")
    denominator = integer(obj["denominator"], f"{label}.denominator")
    if denominator <= 0:
        raise VerificationError(f"{label}.denominator must be positive")
    if math.gcd(abs(numerator), denominator) != 1:
        raise VerificationError(f"{label} must be reduced")
    if numerator == 0 and denominator != 1:
        raise VerificationError(f"{label} zero must use denominator 1")
    return Fraction(numerator, denominator)


def rational_json(value: Fraction) -> dict[str, int]:
    return {"denominator": value.denominator, "numerator": value.numerator}


def zeros(rows: int, columns: int) -> Matrix:
    return Matrix(
        rows,
        columns,
        tuple(tuple(Fraction(0) for _ in range(columns)) for _ in range(rows)),
    )


def parse_matrix(value: Any, rows: int, columns: int, label: str) -> Matrix:
    obj = exact_object(value, {"columns", "entries", "rows"}, label)
    recorded_rows = integer(obj["rows"], f"{label}.rows")
    recorded_columns = integer(obj["columns"], f"{label}.columns")
    if (recorded_rows, recorded_columns) != (rows, columns):
        raise VerificationError(
            f"{label} shape must be {rows}x{columns}, "
            f"got {recorded_rows}x{recorded_columns}"
        )
    entries = obj["entries"]
    if not isinstance(entries, list) or len(entries) != rows:
        raise VerificationError(f"{label}.entries row count mismatch")
    parsed: list[tuple[Fraction, ...]] = []
    for row, raw_row in enumerate(entries):
        if not isinstance(raw_row, list) or len(raw_row) != columns:
            raise VerificationError(f"{label}.entries[{row}] column count mismatch")
        parsed.append(
            tuple(
                rational(entry, f"{label}.entries[{row}][{column}]")
                for column, entry in enumerate(raw_row)
            )
        )
    return Matrix(rows, columns, tuple(parsed))


def matrix_json(matrix: Matrix) -> dict[str, Any]:
    return {
        "columns": matrix.columns,
        "entries": [
            [rational_json(value) for value in row] for row in matrix.entries
        ],
        "rows": matrix.rows,
    }


def multiply(left: Matrix, right: Matrix) -> Matrix:
    if left.columns != right.rows:
        raise VerificationError("internal independent matrix shape mismatch")
    return Matrix(
        left.rows,
        right.columns,
        tuple(
            tuple(
                sum(
                    (left.entries[row][index] * right.entries[index][column]
                     for index in range(left.columns)),
                    Fraction(0),
                )
                for column in range(right.columns)
            )
            for row in range(left.rows)
        ),
    )


def add(left: Matrix, right: Matrix) -> Matrix:
    if (left.rows, left.columns) != (right.rows, right.columns):
        raise VerificationError("internal independent matrix-add shape mismatch")
    return Matrix(
        left.rows,
        left.columns,
        tuple(
            tuple(left.entries[row][column] + right.entries[row][column]
                  for column in range(left.columns))
            for row in range(left.rows)
        ),
    )


def subtract(left: Matrix, right: Matrix) -> Matrix:
    if (left.rows, left.columns) != (right.rows, right.columns):
        raise VerificationError("internal independent matrix-subtract shape mismatch")
    return Matrix(
        left.rows,
        left.columns,
        tuple(
            tuple(left.entries[row][column] - right.entries[row][column]
                  for column in range(left.columns))
            for row in range(left.rows)
        ),
    )


def vectorize(matrix: Matrix) -> tuple[Fraction, ...]:
    return tuple(
        matrix.entries[row][column]
        for column in range(matrix.columns)
        for row in range(matrix.rows)
    )


def parse_complex(value: Any, label: str) -> Complex:
    obj = exact_object(
        value,
        {"differentials", "dimensions", "maximum_degree", "minimum_degree"},
        label,
    )
    minimum = integer(obj["minimum_degree"], f"{label}.minimum_degree")
    maximum = integer(obj["maximum_degree"], f"{label}.maximum_degree")
    if maximum < minimum:
        raise VerificationError(f"{label} grading interval is empty")
    count = maximum - minimum + 1
    raw_dimensions = obj["dimensions"]
    if not isinstance(raw_dimensions, list) or len(raw_dimensions) != count:
        raise VerificationError(f"{label}.dimensions length mismatch")
    dimensions = tuple(
        integer(value, f"{label}.dimensions[{index}]")
        for index, value in enumerate(raw_dimensions)
    )
    if any(value < 0 for value in dimensions):
        raise VerificationError(f"{label}.dimensions must be nonnegative")
    raw_differentials = obj["differentials"]
    if not isinstance(raw_differentials, list) or len(raw_differentials) != count - 1:
        raise VerificationError(f"{label}.differentials length mismatch")
    differentials = tuple(
        parse_matrix(
            raw,
            dimensions[offset],
            dimensions[offset + 1],
            f"{label}.differentials[{offset}]",
        )
        for offset, raw in enumerate(raw_differentials)
    )
    result = Complex(minimum, maximum, dimensions, differentials)
    for degree in range(minimum + 2, maximum + 1):
        composite = multiply(
            result.differential(degree - 1), result.differential(degree)
        )
        if composite != zeros(composite.rows, composite.columns):
            raise VerificationError(f"{label} has nonzero d^2 at degree {degree}")
    return result


def parse_map(
    value: Any, source: Complex, target: Complex, label: str
) -> tuple[Matrix, ...]:
    obj = exact_object(value, {"components"}, label)
    raw_components = obj["components"]
    count = source.maximum - source.minimum + 1
    if not isinstance(raw_components, list) or len(raw_components) != count:
        raise VerificationError(f"{label}.components length mismatch")
    components = tuple(
        parse_matrix(
            raw,
            target.dimension(source.minimum + offset),
            source.dimension(source.minimum + offset),
            f"{label}.components[{offset}]",
        )
        for offset, raw in enumerate(raw_components)
    )
    for degree in range(source.minimum + 1, source.maximum + 1):
        offset = degree - source.minimum
        left = multiply(target.differential(degree), components[offset])
        right = multiply(components[offset - 1], source.differential(degree))
        if left != right:
            raise VerificationError(f"{label} is not a chain map at degree {degree}")
    return components


def parse_problem(value: Any, label: str) -> Problem:
    obj = exact_object(value, {"case_id", "f", "g", "source", "target"}, label)
    case_id = obj["case_id"]
    if not isinstance(case_id, str) or not case_id or any(
        character not in "abcdefghijklmnopqrstuvwxyz0123456789_" for character in case_id
    ):
        raise VerificationError(f"{label}.case_id must be lower snake case")
    source = parse_complex(obj["source"], f"{label}.source")
    target = parse_complex(obj["target"], f"{label}.target")
    if (source.minimum, source.maximum) != (target.minimum, target.maximum):
        raise VerificationError(f"{label} source and target grading must match")
    f = parse_map(obj["f"], source, target, f"{label}.f")
    g = parse_map(obj["g"], source, target, f"{label}.g")
    return Problem(case_id, source, target, f, g, obj)


def parse_input(value: Any) -> list[Problem]:
    obj = exact_object(
        value,
        {
            "cases",
            "claim_id",
            "evidence_status",
            "field",
            "fixture_claim_id",
            "fixture_id",
            "historical_replay_status",
            "schema",
        },
        "input",
    )
    fixed = {
        "claim_id": CLAIM_ID,
        "evidence_status": EVIDENCE_STATUS,
        "field": "Q",
        "fixture_claim_id": FIXTURE_CLAIM_ID,
        "fixture_id": FIXTURE_ID,
        "historical_replay_status": HISTORICAL_REPLAY_STATUS,
        "schema": INPUT_SCHEMA,
    }
    for key, expected in fixed.items():
        if obj[key] != expected:
            raise VerificationError(f"input.{key} must be {expected!r}")
    raw_cases = obj["cases"]
    if not isinstance(raw_cases, list) or not raw_cases:
        raise VerificationError("input.cases must be a nonempty array")
    cases = [
        parse_problem(case, f"input.cases[{index}]")
        for index, case in enumerate(raw_cases)
    ]
    identifiers = [case.case_id for case in cases]
    if identifiers != sorted(identifiers) or len(identifiers) != len(set(identifiers)):
        raise VerificationError("input case IDs must be unique and sorted")
    return cases


def verify_provenance(value: Any) -> None:
    obj = exact_object(
        value,
        {
            "classification",
            "historical_replay_status",
            "kernel_verification_status",
            "mechanical_replay_status",
            "source_documents",
            "source_redistribution",
        },
        "provenance",
    )
    expected = {
        "classification": EVIDENCE_STATUS,
        "historical_replay_status": HISTORICAL_REPLAY_STATUS,
        "kernel_verification_status": "not_kernel_verified",
        "mechanical_replay_status": "not_mechanically_replayed",
        "source_documents": [
            {
                "filename": "Derived_Witnessed_Descent_and_Atomic_Spectral_Complexity.md",
                "role": "provenance_only",
                "sha256": "a2bc92f94d3b53eecc379432c0eab9d7992797078ed1fb408b37ed3768795300",
            },
            {
                "filename": "Formal_Verification_and_Prime_Block_Obstruction.md",
                "role": "provenance_only",
                "sha256": "ba27ed31bc3c5c2f45a559acd2bbaaacfaf1968e61a63750943dfc1899953211",
            },
        ],
        "source_redistribution": "not_included; authorization not established",
    }
    if obj != expected:
        raise VerificationError("provenance contract mismatch")


def omega(problem: Problem) -> tuple[Matrix, ...]:
    return tuple(
        subtract(left, right)
        for left, right in zip(problem.f, problem.g, strict=True)
    )


def apply_homotopy(
    problem: Problem, homotopy: dict[int, Matrix]
) -> tuple[Matrix, ...]:
    components: list[Matrix] = []
    for degree in range(problem.source.minimum, problem.source.maximum + 1):
        high = homotopy.get(
            degree,
            zeros(
                problem.target.dimension(degree + 1),
                problem.source.dimension(degree),
            ),
        )
        low = homotopy.get(
            degree - 1,
            zeros(
                problem.target.dimension(degree),
                problem.source.dimension(degree - 1),
            ),
        )
        components.append(
            add(
                multiply(problem.target.differential(degree + 1), high),
                multiply(low, problem.source.differential(degree)),
            )
        )
    return tuple(components)


def reconstruct_system(problem: Problem) -> ReconstructedSystem:
    rows = tuple(
        (degree, row, column)
        for degree in range(problem.source.minimum, problem.source.maximum + 1)
        for column in range(problem.source.dimension(degree))
        for row in range(problem.target.dimension(degree))
    )
    columns = tuple(
        (degree, row, column)
        for degree in range(problem.source.minimum, problem.source.maximum)
        for column in range(problem.source.dimension(degree))
        for row in range(problem.target.dimension(degree + 1))
    )
    omega_vector = tuple(
        scalar for component in omega(problem) for scalar in vectorize(component)
    )

    coefficient_columns: list[tuple[Fraction, ...]] = []
    for selected_degree, selected_row, selected_column in columns:
        homotopy: dict[int, Matrix] = {}
        for degree in range(problem.source.minimum, problem.source.maximum):
            matrix = zeros(
                problem.target.dimension(degree + 1),
                problem.source.dimension(degree),
            )
            if degree == selected_degree:
                mutable = [list(row) for row in matrix.entries]
                mutable[selected_row][selected_column] = Fraction(1)
                matrix = Matrix(
                    matrix.rows,
                    matrix.columns,
                    tuple(tuple(row) for row in mutable),
                )
            homotopy[degree] = matrix
        coefficient_columns.append(
            tuple(
                scalar
                for component in apply_homotopy(problem, homotopy)
                for scalar in vectorize(component)
            )
        )
    matrix = Matrix(
        len(rows),
        len(columns),
        tuple(
            tuple(
                coefficient_columns[column][row]
                for column in range(len(columns))
            )
            for row in range(len(rows))
        ),
    )
    return ReconstructedSystem(matrix, omega_vector, rows, columns)


def coordinate_json(value: tuple[int, int, int]) -> dict[str, int]:
    degree, row, column = value
    return {"column": column, "degree": degree, "row": row}


def reconstructed_system_json(system: ReconstructedSystem) -> dict[str, Any]:
    return {
        "coefficient_matrix": matrix_json(system.matrix),
        "column_coordinates": [coordinate_json(value) for value in system.columns],
        "omega": [rational_json(value) for value in system.omega],
        "row_coordinates": [coordinate_json(value) for value in system.rows],
    }


def parse_homotopy(problem: Problem, value: Any) -> dict[int, Matrix]:
    obj = exact_object(value, {"homotopy"}, "certificate")
    raw = obj["homotopy"]
    expected_degrees = list(range(problem.source.minimum, problem.source.maximum))
    if not isinstance(raw, list) or len(raw) != len(expected_degrees):
        raise VerificationError("certificate.homotopy degree count mismatch")
    result: dict[int, Matrix] = {}
    for index, (item, expected_degree) in enumerate(zip(raw, expected_degrees, strict=True)):
        block = exact_object(item, {"degree", "matrix"}, f"homotopy[{index}]")
        degree = integer(block["degree"], f"homotopy[{index}].degree")
        if degree != expected_degree:
            raise VerificationError("certificate.homotopy degree ordering mismatch")
        result[degree] = parse_matrix(
            block["matrix"],
            problem.target.dimension(degree + 1),
            problem.source.dimension(degree),
            f"homotopy[{index}].matrix",
        )
    return result


def verify_pass(
    problem: Problem, system: ReconstructedSystem, certificate: Any
) -> None:
    homotopy = parse_homotopy(problem, certificate)
    if apply_homotopy(problem, homotopy) != omega(problem):
        raise VerificationError("homotopy certificate does not satisfy omega=dh+hd")
    vector = tuple(
        scalar
        for degree in range(problem.source.minimum, problem.source.maximum)
        for scalar in vectorize(homotopy[degree])
    )
    product = tuple(
        sum(
            (system.matrix.entries[row][column] * vector[column]
             for column in range(system.matrix.columns)),
            Fraction(0),
        )
        for row in range(system.matrix.rows)
    )
    if product != system.omega:
        raise VerificationError("homotopy vector does not satisfy A h = omega")


def verify_fail(
    system: ReconstructedSystem, certificate: Any
) -> None:
    obj = exact_object(
        certificate,
        {"left_null_pairing", "left_null_witness"},
        "certificate",
    )
    raw_witness = obj["left_null_witness"]
    if not isinstance(raw_witness, list) or len(raw_witness) != system.matrix.rows:
        raise VerificationError("left-null witness length mismatch")
    witness = tuple(
        rational(value, f"left_null_witness[{index}]")
        for index, value in enumerate(raw_witness)
    )
    pairing = rational(obj["left_null_pairing"], "left_null_pairing")
    if pairing != 1:
        raise VerificationError("left-null witness must be normalized to pairing 1")
    actual_pairing = sum(
        (left * right for left, right in zip(witness, system.omega, strict=True)),
        Fraction(0),
    )
    if actual_pairing != pairing:
        raise VerificationError("left-null witness has wrong omega pairing")
    for column in range(system.matrix.columns):
        column_pairing = sum(
            (
                witness[row] * system.matrix.entries[row][column]
                for row in range(system.matrix.rows)
            ),
            Fraction(0),
        )
        if column_pairing != 0:
            raise VerificationError(
                f"left-null witness is not null on A column {column}"
            )


def verify_result(problem: Problem, result: Any) -> None:
    obj = exact_object(
        result,
        {"case_id", "case_sha256", "certificate", "certificate_type", "status", "system"},
        f"result[{problem.case_id}]",
    )
    if obj["case_id"] != problem.case_id:
        raise VerificationError("result case ID mismatch")
    if obj["case_sha256"] != digest(canonical_bytes(problem.document)):
        raise VerificationError("result case digest mismatch")
    system = reconstruct_system(problem)
    if obj["system"] != reconstructed_system_json(system):
        raise VerificationError("recorded A, omega, or coordinate system mismatch")
    if obj["status"] == "pass" and obj["certificate_type"] == "homotopy":
        verify_pass(problem, system, obj["certificate"])
    elif obj["status"] == "fail" and obj["certificate_type"] == "left_null":
        verify_fail(system, obj["certificate"])
    else:
        raise VerificationError("certificate polarity and type do not match")


def verify_receipt(input_path: Path, receipt_path: Path) -> tuple[bytes, int]:
    input_bytes, input_value = load_json(input_path, "input")
    receipt_bytes, receipt_value = load_json(receipt_path, "receipt")
    provenance_bytes, provenance_value = load_json(PROVENANCE, "provenance")
    schema_bytes, schema_value = load_json(SCHEMA, "receipt schema")
    verify_provenance(provenance_value)
    schema = validate_schema_document(schema_bytes, schema_value)
    verify_namespace_allocations()
    problems = parse_input(input_value)
    receipt = exact_object(
        receipt_value,
        {
            "arithmetic_model",
            "certificate_schema",
            "claim_id",
            "evidence_status",
            "fixture_claim_id",
            "fixture_id",
            "generator_sha256",
            "historical_replay_status",
            "input_sha256",
            "provenance_sha256",
            "results",
            "schema_sha256",
            "serialization",
        },
        "receipt",
    )
    expected_scalars = {
        "arithmetic_model": ARITHMETIC_MODEL,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "claim_id": CLAIM_ID,
        "evidence_status": EVIDENCE_STATUS,
        "fixture_claim_id": FIXTURE_CLAIM_ID,
        "fixture_id": FIXTURE_ID,
        "generator_sha256": digest(GENERATOR.read_bytes()),
        "historical_replay_status": HISTORICAL_REPLAY_STATUS,
        "input_sha256": digest(input_bytes),
        "provenance_sha256": digest(provenance_bytes),
        "schema_sha256": digest(schema_bytes),
        "serialization": SERIALIZATION,
    }
    for key, expected in expected_scalars.items():
        if receipt[key] != expected:
            raise VerificationError(f"receipt.{key} mismatch")
    results = receipt["results"]
    if not isinstance(results, list) or len(results) != len(problems):
        raise VerificationError("receipt result count mismatch")
    for problem, result in zip(problems, results, strict=True):
        verify_result(problem, result)
    validate_schema_instance(receipt, schema, schema)
    return receipt_bytes, len(results)


def regenerate_and_compare(input_path: Path, expected_bytes: bytes) -> None:
    with tempfile.TemporaryDirectory(prefix="bsc-f12-derived-holonomy-") as temporary:
        output = Path(temporary) / "actual_receipt.json"
        completed = subprocess.run(
            [sys.executable, str(GENERATOR), str(input_path), str(output)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise VerificationError(
                f"isolated generator exited {completed.returncode}: {detail}"
            )
        actual = output.read_bytes()
    if actual != expected_bytes:
        raise VerificationError(
            "isolated generation is not byte-identical; "
            f"expected {digest(expected_bytes)}, got {digest(actual)}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Independently verify exact-Q derived-holonomy certificates."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        input_path = args.input.resolve()
        receipt_path = args.receipt.resolve()
        retained_before = (
            DEFAULT_RECEIPT.read_bytes() if DEFAULT_RECEIPT.exists() else None
        )
        receipt_bytes, case_count = verify_receipt(input_path, receipt_path)
        regenerate_and_compare(input_path, receipt_bytes)
        retained_after = (
            DEFAULT_RECEIPT.read_bytes() if DEFAULT_RECEIPT.exists() else None
        )
        if retained_before != retained_after:
            raise VerificationError("verification modified the retained receipt")
    except (VerificationError, OSError) as exc:
        print(f"{FIXTURE_ID}: FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"{FIXTURE_ID}: PASS: {case_count} exact certificates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
