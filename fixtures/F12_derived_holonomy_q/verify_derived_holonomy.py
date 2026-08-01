#!/usr/bin/env python3
"""Generate deterministic exact-Q derived-holonomy certificates for F12."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


FIXTURE_DIR = Path(__file__).resolve().parent
PROVENANCE_PATH = FIXTURE_DIR / "provenance.json"
SCHEMA_PATH = FIXTURE_DIR / "receipt.schema.json"
RETAINED_RECEIPT = FIXTURE_DIR / "verification_receipt.json"

INPUT_SCHEMA = "bsc-derived-holonomy-input/1"
CERTIFICATE_SCHEMA = "bsc-derived-holonomy-certificate/1"
CLAIM_ID = "BSC-DHC-01"
FIXTURE_CLAIM_ID = "BSC-FIX-12"
FIXTURE_ID = "F12-DERIVED-HOLONOMY-Q"
FIELD = "Q"
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


class CertificateError(ValueError):
    """Raised when an input or exact certificate invariant fails."""


@dataclass(frozen=True)
class Matrix:
    rows: int
    columns: int
    entries: tuple[tuple[Fraction, ...], ...]


@dataclass(frozen=True)
class Complex:
    minimum_degree: int
    maximum_degree: int
    dimensions: tuple[int, ...]
    differentials: tuple[Matrix, ...]

    def dimension(self, degree: int) -> int:
        if degree < self.minimum_degree or degree > self.maximum_degree:
            return 0
        return self.dimensions[degree - self.minimum_degree]

    def differential(self, degree: int) -> Matrix:
        rows = self.dimension(degree - 1)
        columns = self.dimension(degree)
        if degree <= self.minimum_degree or degree > self.maximum_degree:
            return zero_matrix(rows, columns)
        return self.differentials[degree - self.minimum_degree - 1]


@dataclass(frozen=True)
class ChainMap:
    components: tuple[Matrix, ...]


@dataclass(frozen=True)
class Problem:
    case_id: str
    source: Complex
    target: Complex
    f: ChainMap
    g: ChainMap
    document: dict[str, Any]


@dataclass(frozen=True)
class LinearSystem:
    coefficient_matrix: Matrix
    omega: tuple[Fraction, ...]
    row_coordinates: tuple[tuple[int, int, int], ...]
    column_coordinates: tuple[tuple[int, int, int], ...]


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _reject_constant(value: str) -> None:
    raise CertificateError(f"non-finite JSON number is forbidden: {value}")


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CertificateError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def load_canonical_json(path: Path, description: str) -> tuple[bytes, Any]:
    try:
        data = path.read_bytes()
        text = data.decode("utf-8")
        value = json.loads(
            text,
            object_pairs_hook=_object_without_duplicates,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CertificateError(f"cannot read {description}: {exc}") from exc
    if data != canonical_bytes(value):
        raise CertificateError(
            f"{description} is not canonical {SERIALIZATION}"
        )
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
        raise CertificateError(f"{location}: unsupported schema reference")
    name = reference[len(prefix):]
    definitions = root.get("$defs")
    if not name or "/" in name or not isinstance(definitions, dict):
        raise CertificateError(f"{location}: unsupported schema reference")
    target = definitions.get(name)
    if not isinstance(target, dict):
        raise CertificateError(f"{location}: unresolved schema reference")
    return target


def validate_schema_definition(
    schema: Any,
    root: dict[str, Any] | None = None,
    location: str = "$",
) -> None:
    if not isinstance(schema, dict):
        raise CertificateError(f"{location}: schema node must be an object")
    if root is None:
        root = schema
    unknown = set(schema) - SUPPORTED_SCHEMA_KEYWORDS
    if unknown:
        raise CertificateError(
            f"{location}: unsupported schema keywords: {sorted(unknown)}"
        )
    if "$ref" in schema:
        if set(schema) != {"$ref"}:
            raise CertificateError(
                f"{location}: schema reference must be the only keyword"
            )
        resolve_schema_reference(schema["$ref"], root, location)
        return
    definitions = schema.get("$defs")
    if definitions is not None:
        if location != "$" or not isinstance(definitions, dict) or not definitions:
            raise CertificateError(f"{location}: invalid schema definitions")
        for name, subschema in definitions.items():
            if not isinstance(name, str) or not name:
                raise CertificateError(f"{location}: invalid schema definition name")
            validate_schema_definition(subschema, root, f"{location}.$defs.{name}")
    declared_type = schema.get("type")
    if declared_type is not None and declared_type not in SUPPORTED_JSON_TYPES:
        raise CertificateError(
            f"{location}: unsupported type declaration: {declared_type!r}"
        )
    required = schema.get("required")
    if required is not None and (
        not isinstance(required, list)
        or not all(isinstance(item, str) for item in required)
        or len(required) != len(set(required))
    ):
        raise CertificateError(f"{location}: required must contain unique strings")
    properties = schema.get("properties")
    if properties is not None:
        if not isinstance(properties, dict) or not all(
            isinstance(key, str) for key in properties
        ):
            raise CertificateError(f"{location}: properties must be an object")
        if required is not None and not set(required).issubset(properties):
            raise CertificateError(
                f"{location}: required names must have property schemas"
            )
        for key, subschema in properties.items():
            validate_schema_definition(subschema, root, f"{location}.{key}")
    additional = schema.get("additionalProperties")
    if additional is not None and not isinstance(additional, bool):
        raise CertificateError(
            f"{location}: additionalProperties must be Boolean"
        )
    items = schema.get("items")
    if items is not None:
        validate_schema_definition(items, root, f"{location}[]")
    branches = schema.get("oneOf")
    if branches is not None:
        if not isinstance(branches, list) or len(branches) < 2:
            raise CertificateError(f"{location}: oneOf needs at least two branches")
        for index, branch in enumerate(branches):
            validate_schema_definition(branch, root, f"{location}.oneOf[{index}]")
    choices = schema.get("enum")
    if choices is not None and (not isinstance(choices, list) or not choices):
        raise CertificateError(f"{location}: enum must be a nonempty array")
    for key in ("minimum", "minItems"):
        if key in schema and (type(schema[key]) is not int or schema[key] < 0):
            raise CertificateError(f"{location}: {key} must be a nonnegative integer")
    pattern = schema.get("pattern")
    if pattern is not None:
        if not isinstance(pattern, str):
            raise CertificateError(f"{location}: pattern must be a string")
        try:
            re.compile(pattern)
        except re.error as exc:
            raise CertificateError(f"{location}: invalid pattern: {exc}") from exc


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
            except CertificateError:
                continue
            matches += 1
        if matches != 1:
            raise CertificateError(
                f"{location}: schema polarity/shape oneOf matched {matches} branches"
            )
    declared_type = schema.get("type")
    if declared_type is not None and not instance_has_type(instance, declared_type):
        raise CertificateError(
            f"{location}: expected {declared_type}, got {type(instance).__name__}"
        )
    if "const" in schema and not json_equal(instance, schema["const"]):
        raise CertificateError(f"{location}: value does not match declared constant")
    choices = schema.get("enum")
    if choices is not None and not any(json_equal(instance, item) for item in choices):
        raise CertificateError(f"{location}: value is outside the declared enum")
    pattern = schema.get("pattern")
    if pattern is not None and (
        not isinstance(instance, str) or re.fullmatch(pattern, instance) is None
    ):
        raise CertificateError(f"{location}: string does not match {pattern!r}")
    minimum = schema.get("minimum")
    if minimum is not None and (type(instance) is not int or instance < minimum):
        raise CertificateError(f"{location}: value is below minimum {minimum}")
    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        missing = sorted(set(required) - set(instance))
        if missing:
            raise CertificateError(f"{location}: missing required properties: {missing}")
        if schema.get("additionalProperties") is False:
            extras = sorted(set(instance) - set(properties))
            if extras:
                raise CertificateError(f"{location}: unexpected properties: {extras}")
        for key, subschema in properties.items():
            if key in instance:
                validate_schema_instance(instance[key], subschema, root, f"{location}.{key}")
    if isinstance(instance, list):
        minimum_items = schema.get("minItems")
        if minimum_items is not None and len(instance) < minimum_items:
            raise CertificateError(
                f"{location}: array has fewer than {minimum_items} items"
            )
        items = schema.get("items")
        if items is not None:
            for index, item in enumerate(instance):
                validate_schema_instance(item, items, root, f"{location}[{index}]")


def validate_schema_document(schema_bytes: bytes, schema: Any) -> dict[str, Any]:
    if sha256(schema_bytes) != EXPECTED_SCHEMA_SHA256:
        raise CertificateError("receipt schema digest mismatch")
    if not isinstance(schema, dict):
        raise CertificateError("receipt schema must be an object")
    validate_schema_definition(schema)
    if schema.get("$id") != SCHEMA_ID or schema.get("$schema") != SCHEMA_DRAFT:
        raise CertificateError("receipt schema identity mismatch")
    return schema


def require_keys(value: Any, keys: set[str], location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CertificateError(f"{location} must be an object")
    actual = set(value)
    if actual != keys:
        missing = sorted(keys - actual)
        extras = sorted(actual - keys)
        raise CertificateError(
            f"{location} keys are not exact; missing={missing}, extras={extras}"
        )
    return value


def require_int(value: Any, location: str) -> int:
    if type(value) is not int:
        raise CertificateError(f"{location} must be a JSON integer")
    return value


def parse_rational(value: Any, location: str) -> Fraction:
    obj = require_keys(value, {"denominator", "numerator"}, location)
    numerator = require_int(obj["numerator"], f"{location}.numerator")
    denominator = require_int(obj["denominator"], f"{location}.denominator")
    if denominator <= 0:
        raise CertificateError(f"{location}.denominator must be positive")
    if math.gcd(abs(numerator), denominator) != 1:
        raise CertificateError(f"{location} must be reduced")
    if numerator == 0 and denominator != 1:
        raise CertificateError(f"{location} zero must use denominator 1")
    return Fraction(numerator, denominator)


def rational_document(value: Fraction) -> dict[str, int]:
    return {"denominator": value.denominator, "numerator": value.numerator}


def zero_matrix(rows: int, columns: int) -> Matrix:
    return Matrix(
        rows,
        columns,
        tuple(tuple(Fraction(0) for _ in range(columns)) for _ in range(rows)),
    )


def identity_matrix(size: int) -> Matrix:
    return Matrix(
        size,
        size,
        tuple(
            tuple(Fraction(int(row == column)) for column in range(size))
            for row in range(size)
        ),
    )


def matrix_document(matrix: Matrix) -> dict[str, Any]:
    return {
        "columns": matrix.columns,
        "entries": [
            [rational_document(entry) for entry in row] for row in matrix.entries
        ],
        "rows": matrix.rows,
    }


def parse_matrix(
    value: Any, expected_rows: int, expected_columns: int, location: str
) -> Matrix:
    obj = require_keys(value, {"columns", "entries", "rows"}, location)
    rows = require_int(obj["rows"], f"{location}.rows")
    columns = require_int(obj["columns"], f"{location}.columns")
    if rows != expected_rows or columns != expected_columns:
        raise CertificateError(
            f"{location} shape must be {expected_rows}x{expected_columns}, "
            f"got {rows}x{columns}"
        )
    raw_entries = obj["entries"]
    if not isinstance(raw_entries, list) or len(raw_entries) != rows:
        raise CertificateError(f"{location}.entries row count mismatch")
    parsed_rows: list[tuple[Fraction, ...]] = []
    for row_index, raw_row in enumerate(raw_entries):
        if not isinstance(raw_row, list) or len(raw_row) != columns:
            raise CertificateError(
                f"{location}.entries[{row_index}] column count mismatch"
            )
        parsed_rows.append(
            tuple(
                parse_rational(entry, f"{location}.entries[{row_index}][{column}]")
                for column, entry in enumerate(raw_row)
            )
        )
    return Matrix(rows, columns, tuple(parsed_rows))


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    if (left.rows, left.columns) != (right.rows, right.columns):
        raise CertificateError("internal matrix-addition shape mismatch")
    return Matrix(
        left.rows,
        left.columns,
        tuple(
            tuple(left.entries[row][column] + right.entries[row][column]
                  for column in range(left.columns))
            for row in range(left.rows)
        ),
    )


def matrix_subtract(left: Matrix, right: Matrix) -> Matrix:
    if (left.rows, left.columns) != (right.rows, right.columns):
        raise CertificateError("internal matrix-subtraction shape mismatch")
    return Matrix(
        left.rows,
        left.columns,
        tuple(
            tuple(left.entries[row][column] - right.entries[row][column]
                  for column in range(left.columns))
            for row in range(left.rows)
        ),
    )


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    if left.columns != right.rows:
        raise CertificateError("internal matrix-multiplication shape mismatch")
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


def flatten_column_major(matrix: Matrix) -> tuple[Fraction, ...]:
    return tuple(
        matrix.entries[row][column]
        for column in range(matrix.columns)
        for row in range(matrix.rows)
    )


def parse_complex(value: Any, location: str) -> Complex:
    obj = require_keys(
        value,
        {"differentials", "dimensions", "maximum_degree", "minimum_degree"},
        location,
    )
    minimum = require_int(obj["minimum_degree"], f"{location}.minimum_degree")
    maximum = require_int(obj["maximum_degree"], f"{location}.maximum_degree")
    if maximum < minimum:
        raise CertificateError(f"{location} grading interval is empty")
    raw_dimensions = obj["dimensions"]
    expected_count = maximum - minimum + 1
    if not isinstance(raw_dimensions, list) or len(raw_dimensions) != expected_count:
        raise CertificateError(f"{location}.dimensions length mismatch")
    dimensions = tuple(
        require_int(item, f"{location}.dimensions[{index}]")
        for index, item in enumerate(raw_dimensions)
    )
    if any(dimension < 0 for dimension in dimensions):
        raise CertificateError(f"{location}.dimensions must be nonnegative")

    raw_differentials = obj["differentials"]
    if not isinstance(raw_differentials, list) or len(raw_differentials) != (
        expected_count - 1
    ):
        raise CertificateError(f"{location}.differentials length mismatch")
    differentials: list[Matrix] = []
    for offset, raw_matrix in enumerate(raw_differentials, start=1):
        degree = minimum + offset
        differentials.append(
            parse_matrix(
                raw_matrix,
                dimensions[offset - 1],
                dimensions[offset],
                f"{location}.differentials[{offset - 1}]",
            )
        )
    complex_value = Complex(minimum, maximum, dimensions, tuple(differentials))
    for degree in range(minimum + 2, maximum + 1):
        composite = matrix_multiply(
            complex_value.differential(degree - 1),
            complex_value.differential(degree),
        )
        if composite != zero_matrix(composite.rows, composite.columns):
            raise CertificateError(f"{location} has nonzero d^2 at degree {degree}")
    return complex_value


def parse_chain_map(
    value: Any,
    source: Complex,
    target: Complex,
    location: str,
) -> ChainMap:
    obj = require_keys(value, {"components"}, location)
    raw_components = obj["components"]
    count = source.maximum_degree - source.minimum_degree + 1
    if not isinstance(raw_components, list) or len(raw_components) != count:
        raise CertificateError(f"{location}.components length mismatch")
    components = tuple(
        parse_matrix(
            raw_matrix,
            target.dimension(source.minimum_degree + offset),
            source.dimension(source.minimum_degree + offset),
            f"{location}.components[{offset}]",
        )
        for offset, raw_matrix in enumerate(raw_components)
    )
    result = ChainMap(components)
    for degree in range(source.minimum_degree + 1, source.maximum_degree + 1):
        offset = degree - source.minimum_degree
        left = matrix_multiply(target.differential(degree), components[offset])
        right = matrix_multiply(components[offset - 1], source.differential(degree))
        if left != right:
            raise CertificateError(f"{location} is not a chain map at degree {degree}")
    return result


def parse_problem(value: Any, location: str) -> Problem:
    obj = require_keys(value, {"case_id", "f", "g", "source", "target"}, location)
    case_id = obj["case_id"]
    if not isinstance(case_id, str) or not case_id or any(
        character not in "abcdefghijklmnopqrstuvwxyz0123456789_" for character in case_id
    ):
        raise CertificateError(f"{location}.case_id must be lower snake case")
    source = parse_complex(obj["source"], f"{location}.source")
    target = parse_complex(obj["target"], f"{location}.target")
    if (
        source.minimum_degree,
        source.maximum_degree,
    ) != (target.minimum_degree, target.maximum_degree):
        raise CertificateError(f"{location} source and target grading must match")
    f = parse_chain_map(obj["f"], source, target, f"{location}.f")
    g = parse_chain_map(obj["g"], source, target, f"{location}.g")
    return Problem(case_id, source, target, f, g, obj)


def validate_provenance(value: Any) -> None:
    obj = require_keys(
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
    fixed = {
        "classification": EVIDENCE_STATUS,
        "historical_replay_status": HISTORICAL_REPLAY_STATUS,
        "kernel_verification_status": "not_kernel_verified",
        "mechanical_replay_status": "not_mechanically_replayed",
        "source_redistribution": "not_included; authorization not established",
    }
    for key, expected in fixed.items():
        if obj[key] != expected:
            raise CertificateError(f"provenance.{key} mismatch")
    expected_sources = [
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
    ]
    if obj["source_documents"] != expected_sources:
        raise CertificateError("provenance.source_documents mismatch")


def parse_input(value: Any) -> list[Problem]:
    obj = require_keys(
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
        "field": FIELD,
        "fixture_claim_id": FIXTURE_CLAIM_ID,
        "fixture_id": FIXTURE_ID,
        "historical_replay_status": HISTORICAL_REPLAY_STATUS,
        "schema": INPUT_SCHEMA,
    }
    for key, expected in fixed.items():
        if obj[key] != expected:
            raise CertificateError(f"input.{key} must be {expected!r}")
    raw_cases = obj["cases"]
    if not isinstance(raw_cases, list) or not raw_cases:
        raise CertificateError("input.cases must be a nonempty array")
    problems = [
        parse_problem(case, f"input.cases[{index}]")
        for index, case in enumerate(raw_cases)
    ]
    case_ids = [problem.case_id for problem in problems]
    if case_ids != sorted(case_ids) or len(case_ids) != len(set(case_ids)):
        raise CertificateError("input case IDs must be unique and sorted")
    return problems


def omega_components(problem: Problem) -> tuple[Matrix, ...]:
    return tuple(
        matrix_subtract(f_component, g_component)
        for f_component, g_component in zip(
            problem.f.components, problem.g.components, strict=True
        )
    )


def boundary_components(
    problem: Problem, homotopy: dict[int, Matrix]
) -> tuple[Matrix, ...]:
    source = problem.source
    target = problem.target
    components: list[Matrix] = []
    for degree in range(source.minimum_degree, source.maximum_degree + 1):
        rows = target.dimension(degree)
        columns = source.dimension(degree)
        high = homotopy.get(
            degree,
            zero_matrix(target.dimension(degree + 1), source.dimension(degree)),
        )
        low = homotopy.get(
            degree - 1,
            zero_matrix(target.dimension(degree), source.dimension(degree - 1)),
        )
        first = matrix_multiply(target.differential(degree + 1), high)
        second = matrix_multiply(low, source.differential(degree))
        component = matrix_add(first, second)
        if (component.rows, component.columns) != (rows, columns):
            raise CertificateError("internal boundary component shape mismatch")
        components.append(component)
    return tuple(components)


def build_system(problem: Problem) -> LinearSystem:
    source = problem.source
    target = problem.target
    row_coordinates = tuple(
        (degree, row, column)
        for degree in range(source.minimum_degree, source.maximum_degree + 1)
        for column in range(source.dimension(degree))
        for row in range(target.dimension(degree))
    )
    column_coordinates = tuple(
        (degree, row, column)
        for degree in range(source.minimum_degree, source.maximum_degree)
        for column in range(source.dimension(degree))
        for row in range(target.dimension(degree + 1))
    )
    omega = tuple(
        value
        for component in omega_components(problem)
        for value in flatten_column_major(component)
    )

    columns: list[tuple[Fraction, ...]] = []
    for basis_degree, basis_row, basis_column in column_coordinates:
        homotopy = {
            degree: zero_matrix(
                target.dimension(degree + 1), source.dimension(degree)
            )
            for degree in range(source.minimum_degree, source.maximum_degree)
        }
        selected = homotopy[basis_degree]
        mutable = [list(row) for row in selected.entries]
        mutable[basis_row][basis_column] = Fraction(1)
        homotopy[basis_degree] = Matrix(
            selected.rows,
            selected.columns,
            tuple(tuple(row) for row in mutable),
        )
        columns.append(
            tuple(
                value
                for component in boundary_components(problem, homotopy)
                for value in flatten_column_major(component)
            )
        )
    coefficient_rows = tuple(
        tuple(columns[column][row] for column in range(len(columns)))
        for row in range(len(row_coordinates))
    )
    return LinearSystem(
        Matrix(len(row_coordinates), len(column_coordinates), coefficient_rows),
        omega,
        row_coordinates,
        column_coordinates,
    )


def solve_system(
    system: LinearSystem,
) -> tuple[str, tuple[Fraction, ...]]:
    matrix = system.coefficient_matrix
    row_count = matrix.rows
    column_count = matrix.columns
    augmented = [
        list(matrix.entries[row]) + [system.omega[row]] for row in range(row_count)
    ]
    transform = [list(row) for row in identity_matrix(row_count).entries]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, row_count)
                if augmented[row][column] != 0
            ),
            None,
        )
        if selected is None:
            continue
        if selected != pivot_row:
            augmented[pivot_row], augmented[selected] = (
                augmented[selected],
                augmented[pivot_row],
            )
            transform[pivot_row], transform[selected] = (
                transform[selected],
                transform[pivot_row],
            )
        pivot = augmented[pivot_row][column]
        augmented[pivot_row] = [value / pivot for value in augmented[pivot_row]]
        transform[pivot_row] = [value / pivot for value in transform[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = augmented[row][column]
            if factor == 0:
                continue
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    augmented[row], augmented[pivot_row], strict=True
                )
            ]
            transform[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    transform[row], transform[pivot_row], strict=True
                )
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    for row in range(row_count):
        if all(augmented[row][column] == 0 for column in range(column_count)):
            pairing = augmented[row][column_count]
            if pairing != 0:
                witness = tuple(value / pairing for value in transform[row])
                return "fail", witness

    solution = [Fraction(0) for _ in range(column_count)]
    for row, column in enumerate(pivot_columns):
        solution[column] = augmented[row][column_count]
    return "pass", tuple(solution)


def homotopy_from_solution(
    problem: Problem,
    system: LinearSystem,
    solution: tuple[Fraction, ...],
) -> list[dict[str, Any]]:
    source = problem.source
    target = problem.target
    values: dict[int, list[list[Fraction]]] = {}
    for degree in range(source.minimum_degree, source.maximum_degree):
        values[degree] = [
            [Fraction(0) for _ in range(source.dimension(degree))]
            for _ in range(target.dimension(degree + 1))
        ]
    for coordinate, scalar in zip(
        system.column_coordinates, solution, strict=True
    ):
        degree, row, column = coordinate
        values[degree][row][column] = scalar
    return [
        {
            "degree": degree,
            "matrix": matrix_document(
                Matrix(
                    target.dimension(degree + 1),
                    source.dimension(degree),
                    tuple(tuple(row) for row in values[degree]),
                )
            ),
        }
        for degree in range(source.minimum_degree, source.maximum_degree)
    ]


def coordinate_document(coordinate: tuple[int, int, int]) -> dict[str, int]:
    degree, row, column = coordinate
    return {"column": column, "degree": degree, "row": row}


def system_document(system: LinearSystem) -> dict[str, Any]:
    return {
        "coefficient_matrix": matrix_document(system.coefficient_matrix),
        "column_coordinates": [
            coordinate_document(coordinate)
            for coordinate in system.column_coordinates
        ],
        "omega": [rational_document(value) for value in system.omega],
        "row_coordinates": [
            coordinate_document(coordinate) for coordinate in system.row_coordinates
        ],
    }


def result_document(problem: Problem) -> dict[str, Any]:
    system = build_system(problem)
    status, witness = solve_system(system)
    if status == "pass":
        certificate_type = "homotopy"
        certificate: dict[str, Any] = {
            "homotopy": homotopy_from_solution(problem, system, witness)
        }
    else:
        certificate_type = "left_null"
        pairing = sum(
            (left * right for left, right in zip(witness, system.omega, strict=True)),
            Fraction(0),
        )
        if pairing != 1:
            raise CertificateError("internal left-null normalization failure")
        certificate = {
            "left_null_pairing": rational_document(pairing),
            "left_null_witness": [rational_document(value) for value in witness],
        }
    return {
        "case_id": problem.case_id,
        "case_sha256": sha256(canonical_bytes(problem.document)),
        "certificate": certificate,
        "certificate_type": certificate_type,
        "status": status,
        "system": system_document(system),
    }


def generate_receipt(
    input_bytes: bytes,
    input_value: Any,
    provenance_bytes: bytes,
    provenance_value: Any,
    schema_bytes: bytes,
    schema_value: Any,
) -> dict[str, Any]:
    problems = parse_input(input_value)
    validate_provenance(provenance_value)
    schema = validate_schema_document(schema_bytes, schema_value)
    receipt = {
        "arithmetic_model": ARITHMETIC_MODEL,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "claim_id": CLAIM_ID,
        "evidence_status": EVIDENCE_STATUS,
        "fixture_claim_id": FIXTURE_CLAIM_ID,
        "fixture_id": FIXTURE_ID,
        "generator_sha256": sha256(Path(__file__).read_bytes()),
        "historical_replay_status": HISTORICAL_REPLAY_STATUS,
        "input_sha256": sha256(input_bytes),
        "provenance_sha256": sha256(provenance_bytes),
        "results": [result_document(problem) for problem in problems],
        "schema_sha256": sha256(schema_bytes),
        "serialization": SERIALIZATION,
    }
    validate_schema_instance(receipt, schema, schema)
    return receipt


def write_exclusive(path: Path, data: bytes) -> None:
    try:
        with path.open("xb") as stream:
            stream.write(data)
    except FileExistsError as exc:
        raise CertificateError(f"refusing to overwrite existing output: {path}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate exact-Q derived-holonomy pass/fail certificates."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        input_path = args.input.resolve()
        output_path = args.output.resolve()
        if output_path == RETAINED_RECEIPT.resolve():
            raise CertificateError("refusing to overwrite the retained receipt")
        if output_path == input_path:
            raise CertificateError("input and output paths must differ")
        input_bytes, input_value = load_canonical_json(input_path, "input")
        provenance_bytes, provenance_value = load_canonical_json(
            PROVENANCE_PATH, "provenance"
        )
        schema_bytes, schema_value = load_canonical_json(
            SCHEMA_PATH, "receipt schema"
        )
        receipt = generate_receipt(
            input_bytes,
            input_value,
            provenance_bytes,
            provenance_value,
            schema_bytes,
            schema_value,
        )
        write_exclusive(output_path, canonical_bytes(receipt))
    except (CertificateError, OSError) as exc:
        print(f"{FIXTURE_ID}: FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
