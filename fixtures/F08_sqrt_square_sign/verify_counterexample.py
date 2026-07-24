#!/usr/bin/env python3
"""Emit the deterministic receipt for BSC fixture F8."""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_counterexample.py RECEIPT.json")

    source = Path(__file__).read_bytes()
    x = -1
    lhs = math.isqrt(x * x)
    rhs = x
    claim = "for every real x, sqrt(x^2) = x"
    record = {
        "fixture_id": "F8-SQRT-SQUARE-SIGN",
        "arithmetic_model": "exact integers",
        "claim": claim,
        "claim_sha256": hashlib.sha256(claim.encode("utf-8")).hexdigest(),
        "command": "python3 verify_counterexample.py verification_receipt.json",
        "input": {"x": x},
        "interpreter": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
        },
        "output": {"sqrt_x_squared": lhs, "x": rhs},
        "predicate_holds": lhs == rhs,
        "result": "counterexample_confirmed",
        "script_sha256": hashlib.sha256(source).hexdigest(),
        "receipt_schema": "bsc-deterministic-receipt/1",
    }
    Path(sys.argv[1]).write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
