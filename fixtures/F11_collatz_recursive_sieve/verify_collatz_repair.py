#!/usr/bin/env python3
"""Generate the deterministic full-scan receipt for BSC Fixture F11."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any


FIXTURE_DIR = Path(__file__).resolve().parent
GENERATOR = Path(__file__).resolve()
CHECKER = FIXTURE_DIR / "check_fixture.py"
INPUT = FIXTURE_DIR / "input.json"
SCHEMA = FIXTURE_DIR / "receipt.schema.json"
PROVENANCE = FIXTURE_DIR / "provenance.json"
RETAINED = FIXTURE_DIR / "verification_receipt.json"
CLAIM = (
    "conditional on the declared external 2^71 base, the exact W_173 "
    "enumeration and first-descent table extend convergence through "
    "2^71+10^10"
)
RECEIPT_SCHEMA = "bsc-deterministic-receipt/5"
ARITHMETIC_MODEL = "CPython arbitrary-precision integer arithmetic"
SELF_HASH_POLICY = (
    "the receipt does not hash itself; MANIFEST.sha256 binds the retained "
    "receipt externally"
)
SERIALIZATION = "UTF-8 JSON, two-space indentation, sorted keys, LF terminator"
NONCLAIMS = [
    "not a proof of the Collatz conjecture",
    "not an independent replay of the external n<2^71 verification",
    "not a proof that the original ternary F_n family is recursively sufficient",
    "not an official verification-frontier announcement",
]


class FixtureError(ValueError):
    """Raised when an F11 input or certificate violates the contract."""


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


def receipt_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def load_json(path: Path) -> tuple[bytes, Any]:
    data = path.read_bytes()
    return data, json.loads(data)


def validate_specification(spec: Any) -> dict[str, Any]:
    if not isinstance(spec, dict):
        raise FixtureError("input must be a JSON object")
    required = {
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
    if set(spec) != required:
        raise FixtureError("input keys are not exact")
    if spec["claim_id"] != "BSC-FIX-11":
        raise FixtureError("claim_id mismatch")
    if spec["fixture_id"] != "F11-COLLATZ-RECURSIVE-SIEVE":
        raise FixtureError("fixture_id mismatch")
    if spec["base"] != 1 << 71:
        raise FixtureError("base must be exactly 2^71")
    if spec["range_length"] != 10_000_000_000:
        raise FixtureError("range_length mismatch")
    if spec["depth"] != 173:
        raise FixtureError("depth mismatch")
    if spec["threshold"] != {
        "odd_count_coefficient": 485,
        "prefix_length_coefficient": 306,
    }:
        raise FixtureError("threshold mismatch")
    if spec["g_n_residues_mod_36"] != [3, 7, 15, 19, 27]:
        raise FixtureError("G residue list mismatch")
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


def is_v(n: int, depth: int, odd_coefficient: int, prefix_coefficient: int) -> bool:
    x = n
    odd_count = 0
    for step in range(1, depth + 1):
        if x & 1:
            odd_count += 1
            x = (3 * x + 1) // 2
        else:
            x //= 2
        if odd_coefficient * odd_count <= prefix_coefficient * step:
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


def parity_count(depth: int, odd_coefficient: int, prefix_coefficient: int) -> int:
    counts = [0] * (depth + 1)
    counts[0] = 1
    for step in range(1, depth + 1):
        next_counts = [0] * (depth + 1)
        for odd_count in range(step + 1):
            if odd_coefficient * odd_count <= prefix_coefficient * step:
                continue
            next_counts[odd_count] = counts[odd_count]
            if odd_count:
                next_counts[odd_count] += counts[odd_count - 1]
        counts = next_counts
    return sum(counts)


def first_defect_residues() -> list[int]:
    f1 = {
        (4 * a0 + 3 + 12 * lift) % 36
        for a0 in (0, 1)
        for lift in range(3)
    }
    f2 = {
        (4 * (a0 + 3 * a1) + 3) % 36
        for a0 in (0, 1)
        for a1 in (0, 1)
    }
    defect = sorted(f1 - f2)
    if f1 != {3, 7, 15, 19, 27, 31}:
        raise FixtureError("F1 residue expansion mismatch")
    if f2 != {3, 7, 15, 19} or defect != [27, 31]:
        raise FixtureError("first defect residue expansion mismatch")
    return defect


def verify_31_class_affine_path() -> None:
    # Affine pairs encode a*k+b for k >= 0.
    x = (36, 31)
    two_x = (72, 62)
    middle = (48, 41)
    lower = (32, 27)
    if tuple(2 * value for value in x) != two_x:
        raise FixtureError("31-class first affine edge mismatch")
    if (
        (3 * middle[0] // 2, (3 * middle[1] + 1) // 2)
        != two_x
        or middle[0] % 2
        or middle[1] % 2 != 1
    ):
        raise FixtureError("31-class second affine edge mismatch")
    if (
        (3 * lower[0] // 2, (3 * lower[1] + 1) // 2)
        != middle
        or lower[0] % 2
        or lower[1] % 2 != 1
    ):
        raise FixtureError("31-class third affine edge mismatch")
    if x[0] - lower[0] <= 0 or x[1] - lower[1] <= 0:
        raise FixtureError("31-class endpoint is not uniformly smaller")


def offset_bytes(offsets: list[int]) -> bytes:
    return "".join(f"{offset}\n" for offset in offsets).encode("ascii")


def replay_certificate(
    path: Path,
    spec: dict[str, Any],
) -> tuple[dict[str, Any], list[int]]:
    certificate = spec["certificate"]
    data = path.read_bytes()
    if len(data) != certificate["bytes"]:
        raise FixtureError("certificate byte length mismatch")
    if sha256_bytes(data) != certificate["sha256"]:
        raise FixtureError("certificate SHA-256 mismatch")
    base = spec["base"]
    depth = spec["depth"]
    odd_coefficient = spec["threshold"]["odd_count_coefficient"]
    prefix_coefficient = spec["threshold"]["prefix_length_coefficient"]
    residues = set(spec["g_n_residues_mod_36"])
    offsets: list[int] = []
    max_steps = 0
    max_peak = 0
    previous_offset = 0
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        expected_header = [
            "offset",
            "n",
            "G",
            "V173",
            "steps_to_descent",
            "descent_value",
            "peak",
        ]
        if reader.fieldnames != expected_header:
            raise FixtureError("certificate header mismatch")
        for line_number, row in enumerate(reader, start=2):
            try:
                offset = int(row["offset"])
                n = int(row["n"])
                steps = int(row["steps_to_descent"])
                descent = int(row["descent_value"])
                peak = int(row["peak"])
            except (TypeError, ValueError) as exc:
                raise FixtureError(
                    f"non-integer certificate field on line {line_number}"
                ) from exc
            if row["G"] != "1" or row["V173"] != "1":
                raise FixtureError(f"membership flag mismatch on line {line_number}")
            if not 0 < offset <= spec["range_length"]:
                raise FixtureError(f"offset out of range on line {line_number}")
            if offset <= previous_offset:
                raise FixtureError("certificate offsets are not strictly increasing")
            if n != base + offset:
                raise FixtureError(f"start value mismatch on line {line_number}")
            if n % 36 not in residues:
                raise FixtureError(f"G membership mismatch on line {line_number}")
            if not is_v(n, depth, odd_coefficient, prefix_coefficient):
                raise FixtureError(f"V173 membership mismatch on line {line_number}")
            expected = first_descent(n)
            if expected != (steps, descent, peak):
                raise FixtureError(f"first-descent replay mismatch on line {line_number}")
            offsets.append(offset)
            previous_offset = offset
            max_steps = max(max_steps, steps)
            max_peak = max(max_peak, peak)
    if len(offsets) != certificate["records"]:
        raise FixtureError("certificate record count mismatch")
    summary = {
        "bytes": len(data),
        "candidate_offsets_sha256": sha256_bytes(offset_bytes(offsets)),
        "first_offset": offsets[0],
        "last_offset": offsets[-1],
        "max_peak": max_peak,
        "max_steps_to_descent": max_steps,
        "records": len(offsets),
        "sha256": sha256_bytes(data),
    }
    return summary, offsets


def scan_task(task: tuple[int, int, int, int, int, int, tuple[int, ...]]) -> tuple[int, list[int]]:
    (
        first_block,
        final_block,
        base,
        length,
        depth,
        odd_coefficient,
        offset_residues,
    ) = task
    prefix_coefficient = 306
    scanned = 0
    found: list[int] = []
    for block in range(first_block, final_block):
        block_base = 36 * block
        for residue in offset_residues:
            offset = block_base + residue
            if not 0 < offset <= length:
                continue
            scanned += 1
            if is_v(
                base + offset,
                depth,
                odd_coefficient,
                prefix_coefficient,
            ):
                found.append(offset)
    return scanned, found


def enumerate_candidates(
    spec: dict[str, Any],
    workers: int,
) -> tuple[int, list[int]]:
    base = spec["base"]
    length = spec["range_length"]
    depth = spec["depth"]
    odd_coefficient = spec["threshold"]["odd_count_coefficient"]
    # B0 == 32 mod 36, so these offsets produce G residues
    # 3, 7, 15, 19, and 27 mod 36.
    offset_residues = (7, 11, 19, 23, 31)
    total_blocks = length // 36 + 1
    chunk_count = workers * 4
    tasks = []
    for index in range(chunk_count):
        first = total_blocks * index // chunk_count
        final = total_blocks * (index + 1) // chunk_count
        if first < final:
            tasks.append(
                (
                    first,
                    final,
                    base,
                    length,
                    depth,
                    odd_coefficient,
                    offset_residues,
                )
            )
    scanned = 0
    found: list[int] = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for task_scanned, task_found in pool.map(scan_task, tasks):
            scanned += task_scanned
            found.extend(task_found)
    found.sort()
    return scanned, found


def build_receipt(spec: dict[str, Any], workers: int) -> dict[str, Any]:
    certificate_path = FIXTURE_DIR / spec["certificate"]["path"]
    certificate_summary, certificate_offsets = replay_certificate(
        certificate_path,
        spec,
    )
    scanned, enumerated_offsets = enumerate_candidates(spec, workers)
    if enumerated_offsets != certificate_offsets:
        missing = sorted(set(certificate_offsets) - set(enumerated_offsets))[:20]
        extra = sorted(set(enumerated_offsets) - set(certificate_offsets))[:20]
        raise FixtureError(
            f"full enumeration mismatch: missing={missing}, extra={extra}"
        )
    depth = spec["depth"]
    odd_coefficient = spec["threshold"]["odd_count_coefficient"]
    prefix_coefficient = spec["threshold"]["prefix_length_coefficient"]
    v_count = parity_count(depth, odd_coefficient, prefix_coefficient)
    if v_count != spec["v173_residue_count"]:
        raise FixtureError("V173 dynamic-program count mismatch")
    base = spec["base"]
    if not (3 * base + 1) ** prefix_coefficient < (
        2**odd_coefficient * base**prefix_coefficient
    ):
        raise FixtureError("exact threshold inequality failed")
    defect_residues = first_defect_residues()
    verify_31_class_affine_path()
    input_bytes = INPUT.read_bytes()
    schema_bytes = SCHEMA.read_bytes()
    provenance_bytes = PROVENANCE.read_bytes()
    analysis_material = {
        "checker_sha256": sha256_file(CHECKER),
        "generator_sha256": sha256_file(GENERATOR),
        "schema_sha256": sha256_bytes(schema_bytes),
        "serialization": SERIALIZATION,
    }
    contract_material = {
        "claim": CLAIM,
        "claim_id": spec["claim_id"],
        "fixture_id": spec["fixture_id"],
        "input_sha256": sha256_bytes(input_bytes),
    }
    data_material = {
        "certificate_sha256": certificate_summary["sha256"],
        "provenance_sha256": sha256_bytes(provenance_bytes),
    }
    return {
        "arithmetic_model": ARITHMETIC_MODEL,
        "certificate": certificate_summary,
        "claim": CLAIM,
        "claim_id": spec["claim_id"],
        "completeness": {
            "candidate_offsets_sha256": sha256_bytes(
                offset_bytes(enumerated_offsets)
            ),
            "enumerated_g_candidates": scanned,
            "enumeration": (
                "all G-compatible offsets in (0,10000000000] were tested "
                "against the exact V173 prefix inequalities"
            ),
            "full_scan": True,
            "retained_candidates": len(enumerated_offsets),
        },
        "environment": spec["environment"],
        "evidence_identity": {
            "analysis": {
                **analysis_material,
                "analysis_sha256": sha256_bytes(
                    canonical_bytes(analysis_material)
                ),
            },
            "contract": {
                **contract_material,
                "contract_sha256": sha256_bytes(
                    canonical_bytes(contract_material)
                ),
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
        },
        "fixture_id": spec["fixture_id"],
        "mathematics": {
            "base": base,
            "conditional_prefix_end": base + spec["range_length"],
            "depth": depth,
            "first_defect_residues_mod_36": defect_residues,
            "g_residues_mod_36": spec["g_n_residues_mod_36"],
            "threshold_exact_inequality": True,
            "v173_residue_count": v_count,
            "w173_density_denominator": 9 * (1 << depth),
            "w173_density_numerator": 5 * v_count,
        },
        "nonclaims": NONCLAIMS,
        "receipt_schema": RECEIPT_SCHEMA,
        "result": "conditional_prefix_extension_certificate_verified",
        "self_hash_policy": SELF_HASH_POLICY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
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
        output = args.output.resolve()
        if output == RETAINED.resolve():
            raise FixtureError("refusing to overwrite the retained verification receipt")
        if output.exists():
            raise FixtureError(f"refusing to overwrite existing output: {output}")
        _, loaded = load_json(INPUT)
        spec = validate_specification(loaded)
        receipt = build_receipt(spec, args.workers)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(receipt_bytes(receipt))
    except (FixtureError, OSError, json.JSONDecodeError, csv.Error) as exc:
        print(f"F11-COLLATZ-RECURSIVE-SIEVE: FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"F11-COLLATZ-RECURSIVE-SIEVE: PASS: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
