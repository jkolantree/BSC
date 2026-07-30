from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
FIXTURE = REPOSITORY_ROOT / "fixtures" / "F10_coupled_surrogate"


def serialized_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


class F10FixtureTests(unittest.TestCase):
    def run_program(self, program: Path, *arguments: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(program), *(str(argument) for argument in arguments)],
            cwd=program.parent,
            check=False,
            capture_output=True,
            text=True,
        )

    def make_mutant(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="bsc-f10-mutant-")
        fixture = Path(temporary.name) / "fixture"
        shutil.copytree(FIXTURE, fixture)
        return temporary, fixture

    def read_json(self, path: Path) -> Any:
        return json.loads(path.read_text(encoding="utf-8"))

    def write_json(self, path: Path, value: Any) -> None:
        path.write_text(serialized_json(value), encoding="utf-8", newline="\n")

    def test_development_fixture_passes(self) -> None:
        completed = self.run_program(FIXTURE / "check_fixture.py")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("F10-COUPLED-SURROGATE: PASS", completed.stdout)

    def test_stale_host_identity_hash_is_rejected(self) -> None:
        temporary, fixture = self.make_mutant()
        self.addCleanup(temporary.cleanup)
        receipt_path = fixture / "verification_receipt.json"
        receipt = self.read_json(receipt_path)
        candidate = receipt["evidence_identity"]["candidate"]
        candidate["host_sha256"]["HOST-B"] = candidate["host_sha256"][
            "HOST-A"
        ]
        self.write_json(receipt_path, receipt)

        completed = self.run_program(fixture / "check_fixture.py")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "HOST-B host identity hash mismatch",
            completed.stderr,
        )

    def test_altered_horizon_is_rejected_even_with_refreshed_input_hash(self) -> None:
        temporary, fixture = self.make_mutant()
        self.addCleanup(temporary.cleanup)
        input_path = fixture / "input.json"
        specification = self.read_json(input_path)
        specification["horizon"] = 9
        self.write_json(input_path, specification)

        receipt_path = fixture / "verification_receipt.json"
        receipt = self.read_json(receipt_path)
        contract = receipt["evidence_identity"]["contract"]
        contract["input_sha256"] = hashlib.sha256(
            input_path.read_bytes()
        ).hexdigest()
        contract_material = {
            "claim": contract["claim"],
            "claim_id": contract["claim_id"],
            "fixture_id": contract["fixture_id"],
            "input_sha256": contract["input_sha256"],
        }
        contract["contract_sha256"] = hashlib.sha256(
            canonical_json_bytes(contract_material)
        ).hexdigest()
        self.write_json(receipt_path, receipt)

        completed = self.run_program(fixture / "check_fixture.py")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("horizon must be exactly 10", completed.stderr)

    def test_false_within_tolerance_host_b_is_rejected_beyond_schema(
        self,
    ) -> None:
        temporary, fixture = self.make_mutant()
        self.addCleanup(temporary.cleanup)

        schema_path = fixture / "receipt.schema.json"
        schema = self.read_json(schema_path)
        host_b_schema = schema["properties"]["hosts"]["properties"]["HOST-B"][
            "properties"
        ]
        host_b_schema["within_tolerance"]["const"] = True
        host_b_schema["tolerance_disposition"]["const"] = "within_tolerance"
        self.write_json(schema_path, schema)

        receipt_path = fixture / "verification_receipt.json"
        receipt = self.read_json(receipt_path)
        receipt["hosts"]["HOST-B"]["within_tolerance"] = True
        receipt["hosts"]["HOST-B"][
            "tolerance_disposition"
        ] = "within_tolerance"
        analysis = receipt["evidence_identity"]["analysis"]
        analysis["schema_sha256"] = hashlib.sha256(
            schema_path.read_bytes()
        ).hexdigest()
        analysis_material = {
            "checker_sha256": analysis["checker_sha256"],
            "generator_sha256": analysis["generator_sha256"],
            "schema_sha256": analysis["schema_sha256"],
            "serialization": analysis["serialization"],
        }
        analysis["analysis_sha256"] = hashlib.sha256(
            canonical_json_bytes(analysis_material)
        ).hexdigest()
        self.write_json(receipt_path, receipt)

        completed = self.run_program(fixture / "check_fixture.py")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "HOST-B within_tolerance is inconsistent with exact arithmetic",
            completed.stderr,
        )

    def test_receipt_binds_claim_state_paths_and_five_identity_factors(
        self,
    ) -> None:
        receipt = self.read_json(FIXTURE / "verification_receipt.json")
        self.assertEqual(receipt["claim_id"], "BSC-FIX-10")
        self.assertEqual(receipt["specification"]["initial_error"], "0")
        self.assertEqual(
            receipt["specification"]["initial_reference_state"], "0"
        )
        self.assertEqual(
            receipt["specification"]["initial_surrogate_state"], "0"
        )
        canonical_input = self.read_json(FIXTURE / "input.json")
        self.assertNotIn("initial_error", canonical_input)
        self.assertEqual(
            canonical_input["initial_reference_state"],
            {"denominator": 1, "numerator": 0},
        )
        self.assertEqual(
            canonical_input["initial_surrogate_state"],
            {"denominator": 1, "numerator": 0},
        )
        identity = receipt["evidence_identity"]
        self.assertEqual(
            set(identity),
            {"analysis", "candidate", "contract", "data", "environment"},
        )
        self.assertEqual(identity["data"]["status"], "not_applicable")
        for host in receipt["hosts"].values():
            self.assertEqual(len(host["reference_state_path"]), 11)
            self.assertEqual(len(host["surrogate_state_path"]), 11)
            self.assertEqual(host["reference_state_path"], ["0"] * 11)
            self.assertEqual(host["surrogate_state_path"][0], "0")
            self.assertEqual(
                host["surrogate_state_path"][1:],
                host["prefix_errors"],
            )

    def test_changed_initial_states_are_rejected(self) -> None:
        for field in (
            "initial_reference_state",
            "initial_surrogate_state",
        ):
            with self.subTest(field=field):
                temporary, fixture = self.make_mutant()
                self.addCleanup(temporary.cleanup)
                input_path = fixture / "input.json"
                specification = self.read_json(input_path)
                specification[field] = {
                    "denominator": 100,
                    "numerator": 1,
                }
                self.write_json(input_path, specification)

                completed = self.run_program(fixture / "check_fixture.py")
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(
                    f"{field} must be exactly 0",
                    completed.stderr,
                )

    def test_surrogate_state_path_mutant_is_rejected_beyond_schema(self) -> None:
        temporary, fixture = self.make_mutant()
        self.addCleanup(temporary.cleanup)
        receipt_path = fixture / "verification_receipt.json"
        receipt = self.read_json(receipt_path)
        receipt["hosts"]["HOST-A"]["surrogate_state_path"][-1] = "0"
        self.write_json(receipt_path, receipt)

        completed = self.run_program(fixture / "check_fixture.py")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "HOST-A receipt differs from independent exact arithmetic",
            completed.stderr,
        )

    def test_decimal_substitution_for_exact_rational_is_rejected(self) -> None:
        temporary, fixture = self.make_mutant()
        self.addCleanup(temporary.cleanup)
        input_path = fixture / "input.json"
        specification = self.read_json(input_path)
        specification["surrogate"]["zhat"] = 0.01
        self.write_json(input_path, specification)

        completed = self.run_program(fixture / "check_fixture.py")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "surrogate.zhat must contain only numerator and denominator",
            completed.stderr,
        )

    def test_generator_cannot_overwrite_retained_receipt(self) -> None:
        retained = FIXTURE / "verification_receipt.json"
        before = retained.read_bytes()
        completed = self.run_program(
            FIXTURE / "verify_coupled_surrogate.py",
            retained,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "refusing to overwrite the retained verification receipt",
            completed.stderr,
        )
        self.assertEqual(retained.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
