from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "fixtures" / "F11_collatz_recursive_sieve"


class F11FixtureTests(unittest.TestCase):
    def run_checker(self, fixture: Path = FIXTURE) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(fixture / "check_fixture.py")],
            cwd=ROOT,
            capture_output=True,
            check=False,
            text=True,
        )

    def make_mutant(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        destination = Path(temporary.name) / FIXTURE.name
        shutil.copytree(FIXTURE, destination)
        return temporary, destination

    def test_retained_fixture_passes_exact_replay(self) -> None:
        completed = self.run_checker()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("F11-COLLATZ-RECURSIVE-SIEVE: PASS", completed.stdout)

    def test_certificate_identity_and_summary_are_frozen(self) -> None:
        path = FIXTURE / "w_10b.tsv"
        self.assertEqual(path.stat().st_size, 4_826_862)
        self.assertEqual(
            hashlib.sha256(path.read_bytes()).hexdigest(),
            "88df1573d49511a4bc93fab35f85d3feb1cade2d40b5444ee"
            "88ae42699aa5250",
        )
        receipt = json.loads(
            (FIXTURE / "verification_receipt.json").read_text(encoding="utf-8")
        )
        self.assertTrue(receipt["completeness"]["full_scan"])
        self.assertEqual(
            receipt["completeness"]["enumerated_g_candidates"],
            1_388_888_889,
        )
        self.assertEqual(receipt["certificate"]["records"], 52_686)

    def test_changed_certificate_row_is_rejected(self) -> None:
        temporary, fixture = self.make_mutant()
        self.addCleanup(temporary.cleanup)
        path = fixture / "w_10b.tsv"
        data = path.read_bytes()
        path.write_bytes(data.replace(b"\t199\t", b"\t198\t", 1))
        completed = self.run_checker(fixture)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("certificate SHA-256 mismatch", completed.stderr)

    def test_false_completeness_count_is_rejected(self) -> None:
        temporary, fixture = self.make_mutant()
        self.addCleanup(temporary.cleanup)
        path = fixture / "verification_receipt.json"
        receipt = json.loads(path.read_text(encoding="utf-8"))
        receipt["completeness"]["enumerated_g_candidates"] -= 1
        path.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        completed = self.run_checker(fixture)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "$.completeness.enumerated_g_candidates: "
            "value does not match declared constant",
            completed.stderr,
        )

    def test_wrong_nested_type_is_rejected_by_schema(self) -> None:
        temporary, fixture = self.make_mutant()
        self.addCleanup(temporary.cleanup)
        path = fixture / "verification_receipt.json"
        receipt = json.loads(path.read_text(encoding="utf-8"))
        receipt["certificate"]["records"] = "52686"
        path.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        completed = self.run_checker(fixture)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "$.certificate.records: value does not match declared constant",
            completed.stderr,
        )

    def test_changed_self_hash_policy_is_rejected(self) -> None:
        temporary, fixture = self.make_mutant()
        self.addCleanup(temporary.cleanup)
        path = fixture / "verification_receipt.json"
        receipt = json.loads(path.read_text(encoding="utf-8"))
        receipt["self_hash_policy"] = 0
        path.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        completed = self.run_checker(fixture)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "$.self_hash_policy: value does not match declared constant",
            completed.stderr,
        )

    def test_generator_refuses_retained_receipt_overwrite(self) -> None:
        retained = FIXTURE / "verification_receipt.json"
        before = retained.read_bytes()
        completed = subprocess.run(
            [
                sys.executable,
                str(FIXTURE / "verify_collatz_repair.py"),
                str(retained),
                "--workers",
                "1",
            ],
            cwd=ROOT,
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "refusing to overwrite the retained verification receipt",
            completed.stderr,
        )
        self.assertEqual(retained.read_bytes(), before)

    def test_full_scan_mode_is_explicit_not_silently_claimed_by_quick_run(self) -> None:
        readme = (FIXTURE / "README.md").read_text(encoding="utf-8")
        checker = (FIXTURE / "check_fixture.py").read_text(encoding="utf-8")
        self.assertIn("--full-scan", readme)
        self.assertIn('parser.add_argument("--full-scan"', checker)
        self.assertIn(
            "does not repeat the ten-billion full enumeration",
            readme,
        )


if __name__ == "__main__":
    unittest.main()
