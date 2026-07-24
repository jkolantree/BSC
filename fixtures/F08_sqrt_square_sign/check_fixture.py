#!/usr/bin/env python3
"""Fail-closed verification gate for the retained F8 receipt."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


FIXTURE_DIR = Path(__file__).resolve().parent
SCRIPT = FIXTURE_DIR / "verify_counterexample.py"
EXPECTED = FIXTURE_DIR / "verification_receipt.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fail(message: str) -> int:
    print(f"F8-SQRT-SQUARE-SIGN: FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    try:
        expected_bytes = EXPECTED.read_bytes()
        expected = json.loads(expected_bytes)
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"cannot read retained receipt: {exc}")

    required = {
        "arithmetic_model",
        "claim",
        "claim_sha256",
        "command",
        "fixture_id",
        "input",
        "interpreter",
        "output",
        "predicate_holds",
        "receipt_schema",
        "result",
        "script_sha256",
    }
    if set(expected) != required:
        return fail("retained receipt fields do not match the declared schema")

    claim = expected["claim"]
    if sha256(claim.encode("utf-8")) != expected["claim_sha256"]:
        return fail("claim hash mismatch")

    try:
        script_bytes = SCRIPT.read_bytes()
    except OSError as exc:
        return fail(f"cannot read verifier: {exc}")
    if sha256(script_bytes) != expected["script_sha256"]:
        return fail("verifier hash mismatch")

    predicate = (
        expected["output"]["sqrt_x_squared"] == expected["output"]["x"]
    )
    derived_result = (
        "claim_holds_for_input" if predicate else "counterexample_confirmed"
    )
    if expected["predicate_holds"] is not predicate:
        return fail("predicate field is inconsistent with the recorded output")
    if predicate:
        return fail("the retained input is not a counterexample")
    if expected["result"] != derived_result:
        return fail("result label is inconsistent with the predicate")

    with tempfile.TemporaryDirectory(prefix="bsc-f8-") as temp_dir:
        actual_path = Path(temp_dir) / "actual_receipt.json"
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(actual_path)],
            cwd=FIXTURE_DIR,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip()
            return fail(f"verifier exited {completed.returncode}: {detail}")
        try:
            actual_bytes = actual_path.read_bytes()
        except OSError as exc:
            return fail(f"verifier did not produce a receipt: {exc}")

    if actual_bytes != expected_bytes:
        return fail(
            "generated receipt is not byte-identical to the retained receipt; "
            f"expected {sha256(expected_bytes)}, got {sha256(actual_bytes)}"
        )

    print("F8-SQRT-SQUARE-SIGN: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
