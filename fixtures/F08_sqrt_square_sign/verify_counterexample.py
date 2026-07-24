#!/usr/bin/env python3
"""Emit the deterministic receipt for BSC fixture F8."""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from pathlib import Path


FIXTURE_DIR = Path(__file__).resolve().parent
SCHEMA = FIXTURE_DIR / "receipt.schema.json"
RETAINED_RECEIPT = FIXTURE_DIR / "verification_receipt.json"
CLAIM = "for every real x, sqrt(x^2) = x"
SAFE_COMMAND = (
    "python3 fixtures/F08_sqrt_square_sign/verify_counterexample.py "
    "build/F08_actual_receipt.json"
)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_counterexample.py RECEIPT.json")

    destination = Path(sys.argv[1]).expanduser().resolve()
    if destination == RETAINED_RECEIPT.resolve():
        raise SystemExit("refusing to overwrite the retained verification receipt")

    source = Path(__file__).read_bytes()
    schema = SCHEMA.read_bytes()
    x = -1
    lhs = math.isqrt(x * x)
    rhs = x
    record = {
        "fixture_id": "F8-SQRT-SQUARE-SIGN",
        "arithmetic_model": "exact integers",
        "claim": CLAIM,
        "claim_sha256": hashlib.sha256(CLAIM.encode("utf-8")).hexdigest(),
        "command": SAFE_COMMAND,
        "working_directory": "repository root",
        "input": {"x": x},
        "interpreter": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
        },
        "output": {"sqrt_x_squared": lhs, "x": rhs},
        "predicate_holds": lhs == rhs,
        "result": "counterexample_confirmed",
        "script_sha256": hashlib.sha256(source).hexdigest(),
        "schema_sha256": hashlib.sha256(schema).hexdigest(),
        "receipt_schema": "bsc-deterministic-receipt/2",
    }
    try:
        with destination.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(record, indent=2, sort_keys=True) + "\n")
    except FileExistsError as exc:
        message = f"refusing to overwrite existing output: {destination}"
        raise SystemExit(message) from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
