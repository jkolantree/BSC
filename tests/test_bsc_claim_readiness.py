from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.bsc_claim_readiness import (
    MAX_INPUT_BYTES,
    MAX_RECEIPT_BYTES,
    ReadinessError,
    canonical_json,
    evaluate,
    evaluate_path,
    validate_graph,
)


INPUT = ROOT / "fixtures" / "F15_cyclic_readiness" / "input.json"
RECEIPT = (
    ROOT / "fixtures" / "F15_cyclic_readiness" / "verification_receipt.json"
)
TOOL = ROOT / "tools" / "bsc_claim_readiness.py"


def input_document() -> dict:
    return json.loads(INPUT.read_text(encoding="utf-8"))


class ClaimReadinessTests(unittest.TestCase):
    def test_retained_receipt_matches_exact_input(self) -> None:
        expected = canonical_json(evaluate_path(INPUT))
        self.assertEqual(RECEIPT.read_bytes(), expected)
        receipt = json.loads(expected)
        self.assertEqual(receipt["status"], "PASS")
        self.assertGreaterEqual(receipt["iterations"], 2)
        self.assertEqual(
            receipt["result"]["BSC-F15-SOURCE"]["verdict"], "true"
        )
        self.assertEqual(
            receipt["result"]["BSC-F15-DECISION"]["verdict"], "open"
        )

    def test_inapplicable_axis_is_absent(self) -> None:
        receipt = evaluate_path(INPUT)
        source = receipt["result"]["BSC-F15-SOURCE"]
        self.assertEqual(source["applicable_axes"], ["IDENTITY", "REVIEW"])
        self.assertNotIn("FORMAL", source["readiness"])

    def test_cycle_propagates_identity_without_changing_verdict(self) -> None:
        receipt = evaluate_path(INPUT)
        model = receipt["result"]["BSC-F15-MODEL"]
        decision = receipt["result"]["BSC-F15-DECISION"]
        self.assertEqual(model["readiness"]["IDENTITY"], "claim-bound")
        self.assertEqual(decision["readiness"]["IDENTITY"], "claim-bound")
        self.assertEqual(model["readiness"]["FORMAL"], "kernel-checked")
        self.assertEqual(decision["readiness"]["FORMAL"], "kernel-checked")

    def test_nonmonotone_cap_is_rejected(self) -> None:
        document = input_document()
        document["edges"][0]["caps"]["REVIEW"] = [
            "internal",
            "unreviewed",
            "external",
        ]
        with self.assertRaisesRegex(ReadinessError, "not monotone"):
            validate_graph(document)

    def test_cap_on_inapplicable_axis_is_rejected(self) -> None:
        document = input_document()
        document["edges"][0]["caps"]["FORMAL"] = [
            "proof-present",
            "kernel-checked",
            "independently-checked",
        ]
        with self.assertRaisesRegex(ReadinessError, "not applicable to source"):
            validate_graph(document)

    def test_duplicate_json_key_is_rejected_by_cli(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-readiness-test-") as temporary:
            graph = Path(temporary) / "duplicate.json"
            graph.write_text(
                '{"schema":"bsc.claim-readiness-graph.v1",'
                '"schema":"bsc.claim-readiness-graph.v1",'
                '"axes":{},"nodes":[],"edges":[]}',
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, "-B", str(TOOL), "evaluate", str(graph)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("duplicate JSON key", result.stderr)

    def test_receipt_identity_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-readiness-test-") as temporary:
            receipt = Path(temporary) / "receipt.json"
            mutated = json.loads(RECEIPT.read_text(encoding="utf-8"))
            mutated["input_sha256"] = "0" * 64
            receipt.write_bytes(canonical_json(mutated))
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(TOOL),
                    "check",
                    str(INPUT),
                    str(receipt),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("identity-mismatched", result.stderr)

    def test_write_new_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-readiness-test-") as temporary:
            receipt = Path(temporary) / "receipt.json"
            receipt.write_text("preserve me\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(TOOL),
                    "write-new",
                    str(INPUT),
                    str(receipt),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(receipt.read_text(encoding="utf-8"), "preserve me\n")

    def test_unknown_extra_field_is_rejected(self) -> None:
        document = copy.deepcopy(input_document())
        document["unexpected"] = True
        with self.assertRaisesRegex(ReadinessError, "keys differ"):
            evaluate(canonical_json(document), document)

    def test_oversized_graph_and_receipt_fail_closed_on_stderr(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-readiness-test-") as temporary:
            graph = Path(temporary) / "oversized-graph.json"
            graph.write_bytes(b" " * (MAX_INPUT_BYTES + 1))
            graph_result = subprocess.run(
                [sys.executable, "-B", str(TOOL), "evaluate", str(graph)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(graph_result.returncode, 2)
            self.assertEqual(graph_result.stdout, "")
            self.assertIn("byte bound", graph_result.stderr)
            self.assertNotIn(str(graph), graph_result.stderr)
            self.assertNotIn("Traceback", graph_result.stderr)

            receipt = Path(temporary) / "oversized-receipt.json"
            receipt.write_bytes(b" " * (MAX_RECEIPT_BYTES + 1))
            receipt_result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(TOOL),
                    "check",
                    str(INPUT),
                    str(receipt),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(receipt_result.returncode, 2)
            self.assertEqual(receipt_result.stdout, "")
            self.assertIn("byte bound", receipt_result.stderr)
            self.assertNotIn(str(receipt), receipt_result.stderr)

    def test_deep_json_oversized_integer_and_surrogate_fail_typed(self) -> None:
        hostile_inputs = (
            b"[" * 100 + b"0" + b"]" * 100,
            b'{"unexpected":999999999999999999999999999999999999}\n',
            b'{"schema":"bsc.claim-readiness-graph.v1","axes":{},'
            b'"nodes":[],"edges":[],"note":"\\ud800"}\n',
        )
        for payload in hostile_inputs:
            with self.subTest(payload=payload[:32]):
                with tempfile.TemporaryDirectory(
                    prefix="bsc-readiness-test-"
                ) as temporary:
                    graph = Path(temporary) / "hostile.json"
                    graph.write_bytes(payload)
                    result = subprocess.run(
                        [sys.executable, "-B", str(TOOL), "evaluate", str(graph)],
                        cwd=ROOT,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("BSC READINESS: FAIL:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_explicit_fixed_point_work_bound_fails_closed(self) -> None:
        document = input_document()
        with mock.patch(
            "tools.bsc_claim_readiness.MAX_FIXED_POINT_OPERATIONS", 1
        ):
            with self.assertRaisesRegex(ReadinessError, "fixed-point work"):
                validate_graph(document)


if __name__ == "__main__":
    unittest.main()
