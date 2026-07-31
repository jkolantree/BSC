#!/usr/bin/env python3
"""Fail-closed exact checker for BSC Fixture F11."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any


FIXTURE_DIR = Path(__file__).resolve().parent
CHECKER = Path(__file__).resolve()
GENERATOR = FIXTURE_DIR / "verify_collatz_repair.py"
INPUT = FIXTURE_DIR / "input.json"
SCHEMA = FIXTURE_DIR / "receipt.schema.json"
PROVENANCE = FIXTURE_DIR / "provenance.json"
RECEIPT = FIXTURE_DIR / "verification_receipt.json"
CLAIM = (
    "conditional on the declared external 2^71 base, the exact W_173 "
    "enumeration and first-descent table extend convergence through "
    "2^71+10^10"
)
NONCLAIMS = [
    "not a proof of the Collatz conjecture",
    "not an independent replay of the external n<2^71 verification",
    "not a proof that the original ternary F_n family is recursively sufficient",
    "not an official verification-frontier announcement",
]
SELF_HASH_POLICY = (
    "the receipt does not hash itself; MANIFEST.sha256 binds the retained "
    "receipt externally"
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


class FixtureError(ValueError):
    """Raised when an F11 artifact violates the fixture contract."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def load_json(path: Path, label: str) -> tuple[bytes, Any]:
    try:
        data = path.read_bytes()
        return data, json.loads(data)
    except (OSError, json.JSONDecodeError) as exc:
        raise FixtureError(f"cannot load {label}: {exc}") from exc


def validate_spec(spec: Any) -> dict[str, Any]:
    if not isinstance(spec, dict):
        raise FixtureError("input must be an object")
    expected_keys = {
        "base",
        "certificate",
        "claim_id",
        "depth",
        "environment",
        "fixture_id",
        "g_n_residues_mod_36",
        "range_length",
        "shortcut_map",
        "threshold",
        "v173_residue_count",
    }
    if set(spec) != expected_keys:
        raise FixtureError("input keys are not exact")
    fixed = {
        "base": 1 << 71,
        "claim_id": "BSC-FIX-11",
        "depth": 173,
        "fixture_id": "F11-COLLATZ-RECURSIVE-SIEVE",
        "g_n_residues_mod_36": [3, 7, 15, 19, 27],
        "range_length": 10_000_000_000,
        "shortcut_map": (
            "T(n)=n/2 for even n; T(n)=(3n+1)/2 for odd n"
        ),
        "threshold": {
            "odd_count_coefficient": 485,
            "prefix_length_coefficient": 306,
        },
        "v173_residue_count": (
            113556863454847668033678912559844765797703296469
        ),
    }
    for key, value in fixed.items():
        if spec.get(key) != value:
            raise FixtureError(f"{key} mismatch")
    expected_certificate = {
        "bytes": 4_826_862,
        "path": "w_10b.tsv",
        "records": 52_686,
        "sha256": (
            "88df1573d49511a4bc93fab35f85d3feb1cade2d40b5444ee"
            "88ae42699aa5250"
        ),
    }
    if spec["certificate"] != expected_certificate:
        raise FixtureError("certificate contract mismatch")
    expected_environment = {
        "arithmetic": "CPython arbitrary-precision integers",
        "implementation": "CPython",
        "version": "3.12.13",
    }
    if spec["environment"] != expected_environment:
        raise FixtureError("environment contract mismatch")
    actual_environment = {
        "arithmetic": "CPython arbitrary-precision integers",
        "implementation": platform.python_implementation(),
        "version": platform.python_version(),
    }
    if actual_environment != expected_environment:
        raise FixtureError(
            f"runtime mismatch: expected {expected_environment}, got {actual_environment}"
        )
    return spec


def is_v173(n: int) -> bool:
    x = n
    odd_count = 0
    for step in range(1, 174):
        if x & 1:
            odd_count += 1
            x = (3 * x + 1) // 2
        else:
            x //= 2
        if 485 * odd_count <= 306 * step:
            return False
    return True


def first_descent(n: int) -> tuple[int, int, int]:
    x = n
    peak = n
    for step in range(1, 1_000_001):
        x = (3 * x + 1) // 2 if x & 1 else x // 2
        peak = max(peak, x)
        if x < n:
            return step, x, peak
    raise FixtureError(f"first-descent cap exceeded for {n}")


def independent_v173_count() -> int:
    paths: dict[int, int] = {0: 1}
    for step in range(1, 174):
        next_paths: dict[int, int] = {}
        for prior_odd_count, ways in paths.items():
            for next_odd_count in (prior_odd_count, prior_odd_count + 1):
                if 485 * next_odd_count > 306 * step:
                    next_paths[next_odd_count] = (
                        next_paths.get(next_odd_count, 0) + ways
                    )
        paths = next_paths
    return sum(paths.values())


def verify_first_defect_and_merge() -> list[int]:
    f1 = {
        residue
        for residue in range(36)
        if residue % 12 in {3, 7}
    }
    f2 = {
        (4 * (low_bit + 3 * high_bit) + 3) % 36
        for low_bit in (0, 1)
        for high_bit in (0, 1)
    }
    defect = sorted(f1.difference(f2))
    if defect != [27, 31]:
        raise FixtureError("independent first-defect derivation mismatch")

    # Direct coefficient identities for
    # 36k+31 <- 72k+62 <- 48k+41 <- 32k+27.
    if (72 // 2, 62 // 2) != (36, 31):
        raise FixtureError("independent first merge edge mismatch")
    if ((3 * 48) // 2, (3 * 41 + 1) // 2) != (72, 62):
        raise FixtureError("independent second merge edge mismatch")
    if ((3 * 32) // 2, (3 * 27 + 1) // 2) != (48, 41):
        raise FixtureError("independent third merge edge mismatch")
    if not (32 < 36 and 27 < 31):
        raise FixtureError("independent smaller-endpoint check failed")
    return defect


def offset_bytes(offsets: list[int]) -> bytes:
    return "".join(f"{offset}\n" for offset in offsets).encode("ascii")


def replay_rows(spec: dict[str, Any]) -> tuple[dict[str, Any], list[int]]:
    path = FIXTURE_DIR / spec["certificate"]["path"]
    data = path.read_bytes()
    if len(data) != spec["certificate"]["bytes"]:
        raise FixtureError("certificate byte length mismatch")
    if sha256_bytes(data) != spec["certificate"]["sha256"]:
        raise FixtureError("certificate SHA-256 mismatch")
    offsets: list[int] = []
    previous = 0
    max_steps = 0
    max_peak = 0
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream, delimiter="\t")
        header = next(reader, None)
        if header != [
            "offset",
            "n",
            "G",
            "V173",
            "steps_to_descent",
            "descent_value",
            "peak",
        ]:
            raise FixtureError("certificate header mismatch")
        for line_number, fields in enumerate(reader, start=2):
            if len(fields) != 7:
                raise FixtureError(f"field count mismatch on line {line_number}")
            try:
                offset, n, g, v, steps, descent, peak = map(int, fields)
            except ValueError as exc:
                raise FixtureError(
                    f"non-integer field on line {line_number}"
                ) from exc
            if (g, v) != (1, 1):
                raise FixtureError(f"membership flag mismatch on line {line_number}")
            if not 0 < offset <= 10_000_000_000 or offset <= previous:
                raise FixtureError(f"offset order/range mismatch on line {line_number}")
            if n != (1 << 71) + offset:
                raise FixtureError(f"start mismatch on line {line_number}")
            if n % 36 not in {3, 7, 15, 19, 27}:
                raise FixtureError(f"G mismatch on line {line_number}")
            if not is_v173(n):
                raise FixtureError(f"V173 mismatch on line {line_number}")
            if first_descent(n) != (steps, descent, peak):
                raise FixtureError(f"descent replay mismatch on line {line_number}")
            offsets.append(offset)
            previous = offset
            max_steps = max(max_steps, steps)
            max_peak = max(max_peak, peak)
    if len(offsets) != 52_686:
        raise FixtureError("record count mismatch")
    return {
        "bytes": len(data),
        "candidate_offsets_sha256": sha256_bytes(offset_bytes(offsets)),
        "first_offset": offsets[0],
        "last_offset": offsets[-1],
        "max_peak": max_peak,
        "max_steps_to_descent": max_steps,
        "records": len(offsets),
        "sha256": sha256_bytes(data),
    }, offsets


def scan_partition(task: tuple[int, int]) -> tuple[int, list[int]]:
    first_block, final_block = task
    base = 1 << 71
    length = 10_000_000_000
    residues = (7, 11, 19, 23, 31)
    scanned = 0
    found: list[int] = []
    for block in range(first_block, final_block):
        block_base = 36 * block
        for residue in residues:
            offset = block_base + residue
            if not 0 < offset <= length:
                continue
            scanned += 1
            if is_v173(base + offset):
                found.append(offset)
    return scanned, found


def independent_full_scan(workers: int) -> tuple[int, list[int]]:
    blocks = 10_000_000_000 // 36 + 1
    partitions = []
    for index in range(workers * 5):
        first = blocks * index // (workers * 5)
        final = blocks * (index + 1) // (workers * 5)
        if first < final:
            partitions.append((first, final))
    scanned = 0
    found: list[int] = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for part_scanned, part_found in pool.map(scan_partition, partitions):
            scanned += part_scanned
            found.extend(part_found)
    found.sort()
    return scanned, found


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
        raise FixtureError(f"{location}: schema node must be an object")
    unknown = set(schema) - SUPPORTED_SCHEMA_KEYWORDS
    if unknown:
        raise FixtureError(
            f"{location}: unsupported schema keywords: {sorted(unknown)}"
        )
    declared_type = schema.get("type")
    if declared_type is not None and (
        not isinstance(declared_type, str)
        or declared_type not in SUPPORTED_JSON_TYPES
    ):
        raise FixtureError(
            f"{location}: unsupported type declaration: {declared_type!r}"
        )
    required = schema.get("required")
    if required is not None and (
        not isinstance(required, list)
        or not all(isinstance(item, str) for item in required)
        or len(required) != len(set(required))
    ):
        raise FixtureError(
            f"{location}: required must contain unique strings"
        )
    properties = schema.get("properties")
    if properties is not None:
        if not isinstance(properties, dict) or not all(
            isinstance(key, str) for key in properties
        ):
            raise FixtureError(f"{location}: properties must be an object")
        for key, subschema in properties.items():
            validate_schema_definition(subschema, f"{location}.{key}")
    additional = schema.get("additionalProperties")
    if additional is not None and not isinstance(additional, bool):
        raise FixtureError(
            f"{location}: additionalProperties must be Boolean"
        )
    pattern = schema.get("pattern")
    if pattern is not None:
        if not isinstance(pattern, str):
            raise FixtureError(f"{location}: pattern must be a string")
        try:
            re.compile(pattern)
        except re.error as exc:
            raise FixtureError(
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
        raise FixtureError(
            f"{location}: expected {declared_type}, got "
            f"{type(instance).__name__}"
        )
    if "const" in schema and not json_equal(instance, schema["const"]):
        raise FixtureError(
            f"{location}: value does not match declared constant"
        )
    pattern = schema.get("pattern")
    if pattern is not None and (
        not isinstance(instance, str) or re.search(pattern, instance) is None
    ):
        raise FixtureError(
            f"{location}: string does not match {pattern!r}"
        )
    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        missing = sorted(set(required) - set(instance))
        if missing:
            raise FixtureError(
                f"{location}: missing required properties: {missing}"
            )
        if schema.get("additionalProperties") is False:
            extras = sorted(set(instance) - set(properties))
            if extras:
                raise FixtureError(
                    f"{location}: unexpected properties: {extras}"
                )
        for key, subschema in properties.items():
            if key in instance:
                validate_instance(instance[key], subschema, f"{location}.{key}")


def verify_receipt(
    spec: dict[str, Any],
    receipt: dict[str, Any],
    certificate_summary: dict[str, Any],
) -> None:
    if receipt["claim"] != CLAIM:
        raise FixtureError("receipt claim mismatch")
    if receipt["environment"] != spec["environment"]:
        raise FixtureError("receipt environment mismatch")
    if receipt["certificate"] != certificate_summary:
        raise FixtureError("receipt certificate summary mismatch")
    if receipt["nonclaims"] != NONCLAIMS:
        raise FixtureError("receipt nonclaims mismatch")
    if receipt["self_hash_policy"] != SELF_HASH_POLICY:
        raise FixtureError("receipt self-hash policy mismatch")
    v_count = independent_v173_count()
    if v_count != spec["v173_residue_count"]:
        raise FixtureError("independent V173 count mismatch")
    base = 1 << 71
    if not (3 * base + 1) ** 306 < 2**485 * base**306:
        raise FixtureError("threshold inequality mismatch")
    defect_residues = verify_first_defect_and_merge()
    if receipt["mathematics"] != {
        "base": base,
        "conditional_prefix_end": base + 10_000_000_000,
        "depth": 173,
        "first_defect_residues_mod_36": defect_residues,
        "g_residues_mod_36": [3, 7, 15, 19, 27],
        "threshold_exact_inequality": True,
        "v173_residue_count": v_count,
        "w173_density_denominator": 9 * (1 << 173),
        "w173_density_numerator": 5 * v_count,
    }:
        raise FixtureError("receipt mathematics mismatch")
    completeness = receipt["completeness"]
    if completeness != {
        "candidate_offsets_sha256": certificate_summary[
            "candidate_offsets_sha256"
        ],
        "enumerated_g_candidates": 1_388_888_889,
        "enumeration": (
            "all G-compatible offsets in (0,10000000000] were tested "
            "against the exact V173 prefix inequalities"
        ),
        "full_scan": True,
        "retained_candidates": 52_686,
    }:
        raise FixtureError("receipt completeness mismatch")
    input_bytes = INPUT.read_bytes()
    schema_bytes = SCHEMA.read_bytes()
    provenance_bytes = PROVENANCE.read_bytes()
    analysis_material = {
        "checker_sha256": sha256_file(CHECKER),
        "generator_sha256": sha256_file(GENERATOR),
        "schema_sha256": sha256_bytes(schema_bytes),
        "serialization": (
            "UTF-8 JSON, two-space indentation, sorted keys, LF terminator"
        ),
    }
    contract_material = {
        "claim": CLAIM,
        "claim_id": "BSC-FIX-11",
        "fixture_id": "F11-COLLATZ-RECURSIVE-SIEVE",
        "input_sha256": sha256_bytes(input_bytes),
    }
    data_material = {
        "certificate_sha256": certificate_summary["sha256"],
        "provenance_sha256": sha256_bytes(provenance_bytes),
    }
    expected_identity = {
        "analysis": {
            **analysis_material,
            "analysis_sha256": sha256_bytes(canonical_bytes(analysis_material)),
        },
        "contract": {
            **contract_material,
            "contract_sha256": sha256_bytes(canonical_bytes(contract_material)),
        },
        "data": {
            **data_material,
            "data_sha256": sha256_bytes(canonical_bytes(data_material)),
        },
        "environment": {
            **spec["environment"],
            "environment_sha256": sha256_bytes(
                canonical_bytes(spec["environment"])
            ),
        },
    }
    if receipt["evidence_identity"] != expected_identity:
        raise FixtureError("receipt evidence identity mismatch")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-scan", action="store_true")
    parser.add_argument(
        "--workers",
        type=int,
        default=min(16, os.cpu_count() or 1),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.workers < 1:
            raise FixtureError("workers must be positive")
        _, loaded_spec = load_json(INPUT, "input")
        spec = validate_spec(loaded_spec)
        _, schema = load_json(SCHEMA, "schema")
        _, receipt = load_json(RECEIPT, "receipt")
        if not isinstance(schema, dict):
            raise FixtureError("receipt schema must be an object")
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise FixtureError("unexpected JSON Schema dialect")
        validate_schema_definition(schema)
        validate_instance(receipt, schema)
        certificate_summary, offsets = replay_rows(spec)
        verify_receipt(spec, receipt, certificate_summary)
        if args.full_scan:
            scanned, found = independent_full_scan(args.workers)
            if scanned != 1_388_888_889:
                raise FixtureError("full-scan candidate count mismatch")
            if found != offsets:
                missing = sorted(set(offsets) - set(found))[:20]
                extra = sorted(set(found) - set(offsets))[:20]
                raise FixtureError(
                    f"full-scan set mismatch: missing={missing}, extra={extra}"
                )
    except (FixtureError, OSError, json.JSONDecodeError, csv.Error) as exc:
        print(f"F11-COLLATZ-RECURSIVE-SIEVE: FAIL: {exc}", file=sys.stderr)
        return 1
    mode = "FULL-SCAN PASS" if args.full_scan else "PASS"
    print(f"F11-COLLATZ-RECURSIVE-SIEVE: {mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
