#!/usr/bin/env python3
"""Same-implementation replay of the retained F14 intervention report."""

from __future__ import annotations

import sys
from pathlib import Path


FIXTURE = Path(__file__).resolve().parent
ROOT = FIXTURE.parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import bsc_intervention_design as DESIGN  # noqa: E402


def main() -> int:
    input_path = FIXTURE / "input.json"
    report_path = FIXTURE / "expected_report.json"
    checker_path = TOOLS / "bsc_intervention_design.py"
    try:
        input_bytes, input_value = DESIGN.load_canonical_json(input_path, "input")
        retained_bytes, retained_value = DESIGN.load_canonical_json(
            report_path, "report"
        )
        reconstructed = DESIGN.build_report(input_bytes, input_value, checker_path)
        if retained_value != reconstructed:
            raise DESIGN.DesignError("retained report differs from exact reconstruction")
        if retained_bytes != DESIGN.canonical_json_bytes(reconstructed):
            raise DESIGN.DesignError("retained report bytes are not canonical")
    except DESIGN.DesignError as exc:
        print(f"F14-INTERVENTION-IDENTIFIABILITY: FAIL: {exc}", file=sys.stderr)
        return 1
    except OSError:
        print(
            "F14-INTERVENTION-IDENTIFIABILITY: FAIL: cannot access a required file",
            file=sys.stderr,
        )
        return 1
    exact = reconstructed["exact_identifiability"]
    print(
        "F14-INTERVENTION-IDENTIFIABILITY: PASS: "
        f"families={exact['intervention_family_count_checked']} "
        f"minimum_cost={DESIGN.format_fraction(exact['minimum_cost'])} "
        f"minimizers={len(exact['all_minimum_cost_families'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
