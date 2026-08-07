from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "research" / "C13_6_3_covering"
TOOL = ARTIFACT / "verify_c13_covering.py"
CONSTRUCTION = ARTIFACT / "construction.json"
PROVENANCE = ARTIFACT / "provenance.json"
NOTE = ARTIFACT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
LICENSE_MAP = ROOT / "LICENSES" / "README.md"


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


C13 = load_module(TOOL, "bsc_c13_covering_tests")


class C13CoveringTests(unittest.TestCase):
    def setUp(self) -> None:
        self.construction = json.loads(CONSTRUCTION.read_text(encoding="utf-8"))
        self.provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))

    def write_json(self, directory: Path, name: str, value: object) -> Path:
        path = directory / name
        path.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        return path

    def verify_documents(self, construction: object, provenance: object) -> dict:
        with tempfile.TemporaryDirectory(prefix="bsc-c13-test-") as directory:
            root = Path(directory)
            construction_path = self.write_json(
                root, "construction.json", construction
            )
            provenance_path = self.write_json(root, "provenance.json", provenance)
            return C13.verify_all(construction_path, provenance_path)

    def test_exact_construction_and_source_exchange(self) -> None:
        report = C13.verify_all(CONSTRUCTION, PROVENANCE)
        construction = report["construction"]
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(construction["block_count"], 20)
        self.assertEqual(construction["covered_triples"], 284)
        self.assertEqual(construction["leave"], [[2, 5, 7], [5, 7, 10]])
        self.assertEqual(construction["common_blocks"], 18)
        self.assertTrue(construction["source_covers_all_triples"])
        self.assertEqual(
            construction["deletion_coverage_histogram"],
            {
                "271": 1,
                "272": 3,
                "273": 2,
                "274": 3,
                "276": 2,
                "280": 4,
                "281": 3,
                "282": 1,
                "283": 2,
            },
        )
        self.assertEqual(
            construction["normalized_blocks_sha256"],
            "7306ee18f5181f2ff3afb7054ceec9bded0fc4424a1f842644c1afbf64f83582",
        )

    def test_near_cover_moments_use_the_partial_identities(self) -> None:
        moments = C13.verify_all(CONSTRUCTION, PROVENANCE)["construction"][
            "moments"
        ]
        self.assertEqual(moments["E2"], 90)
        self.assertEqual(moments["Q"], 47)
        self.assertEqual(moments["H"], 35)
        self.assertEqual(moments["U"], 2)
        self.assertEqual(moments["D"], 96)
        self.assertEqual(moments["J"], 90)
        self.assertEqual(3 * (moments["Q"] + moments["U"]), 147)
        self.assertEqual(moments["E2"] + moments["D"] - 39, 147)
        self.assertEqual(
            moments["singly_covered"], 172 + moments["H"] - 2 * moments["U"]
        )
        self.assertNotEqual(3 * moments["Q"], 147)
        self.assertNotEqual(moments["singly_covered"], 172 + moments["H"])
        self.assertLess(moments["J"], moments["D"])

    def test_one_value_and_structural_block_mutations_fail_closed(self) -> None:
        mutations = []

        changed = copy.deepcopy(self.construction)
        changed["construction"]["blocks"][0][-1] = 7
        mutations.append(changed)

        duplicate = copy.deepcopy(self.construction)
        duplicate["construction"]["blocks"][1] = duplicate["construction"][
            "blocks"
        ][0]
        mutations.append(duplicate)

        unsorted = copy.deepcopy(self.construction)
        unsorted["construction"]["blocks"][0][0:2] = [2, 1]
        mutations.append(unsorted)

        outside = copy.deepcopy(self.construction)
        outside["construction"]["blocks"][0][-1] = 14
        mutations.append(outside)

        wrong_size = copy.deepcopy(self.construction)
        wrong_size["construction"]["blocks"][0].pop()
        mutations.append(wrong_size)

        for index, mutation in enumerate(mutations):
            with self.subTest(mutation=index):
                with self.assertRaises(C13.C13VerificationError):
                    self.verify_documents(mutation, self.provenance)

    def test_false_leave_counts_and_source_cover_fail_closed(self) -> None:
        false_leave = copy.deepcopy(self.construction)
        false_leave["construction"]["claimed_leave"][0] = [1, 2, 3]
        with self.assertRaises(C13.C13VerificationError):
            self.verify_documents(false_leave, self.provenance)

        false_count = copy.deepcopy(self.construction)
        false_count["construction"]["claimed_covered_triples"] = 285
        with self.assertRaises(C13.C13VerificationError):
            self.verify_documents(false_count, self.provenance)

        changed_source = copy.deepcopy(self.construction)
        changed_source["source_cover"]["blocks"][0][-1] = 13
        with self.assertRaises(C13.C13VerificationError):
            self.verify_documents(changed_source, self.provenance)

    def test_duplicate_json_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-c13-duplicate-") as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text(
                '{"schema":"c13-covering-construction-v1",'
                '"schema":"changed"}\n',
                encoding="utf-8",
                newline="\n",
            )
            with self.assertRaises(C13.C13VerificationError):
                C13.load_json(path)

    def test_provenance_hash_and_promotion_mutations_fail_closed(self) -> None:
        changed_hash = copy.deepcopy(self.provenance)
        changed_hash["construction_identity"]["sha256"] = "0" * 64
        with self.assertRaises(C13.C13VerificationError):
            self.verify_documents(self.construction, changed_hash)

        removed_gate = copy.deepcopy(self.provenance)
        removed_gate["blocked_promotions"].pop()
        with self.assertRaises(C13.C13VerificationError):
            self.verify_documents(self.construction, removed_gate)

        promoted = copy.deepcopy(self.provenance)
        promoted["novelty_search"]["result"] = "first ever"
        with self.assertRaises(C13.C13VerificationError):
            self.verify_documents(self.construction, promoted)

        formalized = copy.deepcopy(self.provenance)
        formalized["evidence_status"]["rigidity_proof"] = "kernel_verified"
        with self.assertRaises(C13.C13VerificationError):
            self.verify_documents(self.construction, formalized)

    def test_rigidity_boundary_enumeration_is_complete_and_closed(self) -> None:
        report = C13.verify_rigidity_arithmetic()
        self.assertEqual(report["arithmetic_state_count"], 49)
        self.assertEqual(report["boundary_profile_count"], 10)
        self.assertEqual(report["boundary_profiles_by_type"], {"A": 5, "B": 2, "C": 3})
        self.assertEqual(report["survivors"], 0)
        self.assertEqual(report["degree_nine_multiplicity_cap"], 6)
        self.assertEqual(report["private_triples_in_some_block_lower"], 10)
        self.assertEqual(
            [report["types"][label]["H_lower"] for label in "ABC"],
            [11, 12, 13],
        )
        self.assertEqual(
            [
                report["types"][label]["singly_covered_lower"]
                for label in "ABC"
            ],
            [183, 184, 185],
        )

    def test_finite_lemmas_and_packing_table(self) -> None:
        self.assertEqual(C13.e2_lower_bounds(), {"A": 72, "B": 82, "C": 90})
        self.assertEqual(
            {m: C13.packing_minimum(m) for m in range(4, 11)},
            {4: 2, 5: 5, 6: 8, 7: 12, 8: 18, 9: 24, 10: 30},
        )
        self.assertEqual(
            [C13.max_triangles_for_edges(edges) for edges in range(7)],
            [0, 0, 0, 1, 1, 2, 4],
        )
        self.assertTrue(7 * 6 - 21 <= 24)
        self.assertFalse(7 * 7 - 21 <= 24)

    def test_note_keeps_independent_namespace_and_claim_boundary(self) -> None:
        note = NOTE.read_text(encoding="utf-8")
        self.assertIn("C13-COV-01", note)
        self.assertIn("C13-RIG-01", note)
        self.assertIn("conditional on a 20-cover existing", note)
        self.assertIn("not a design trade", note)
        self.assertIn("not a proof-assistant kernel", note)
        self.assertIn("not a global", note)
        self.assertNotIn("BSC-C13", note)
        self.assertNotIn("F14", note)

    def test_public_surfaces_preserve_attribution_and_theorem_scope(self) -> None:
        note = NOTE.read_text(encoding="utf-8")
        changelog = CHANGELOG.read_text(encoding="utf-8")
        license_map = LICENSE_MAP.read_text(encoding="utf-8")

        for required in (
            "Daniel M. Gordon",
            "La Jolla Coverings Repository",
            "10.5281/zenodo.19735294",
            "CC BY",
        ):
            self.assertIn(required, note)
        self.assertIn("some block must contain at least 10 private", changelog)
        self.assertNotIn("every block must contain at least 10 private", changelog)

        json_license_rows = [
            line
            for line in license_map.splitlines()
            if "`research/**/*.json`" in line
        ]
        self.assertEqual(len(json_license_rows), 1)
        self.assertIn("CC BY 4.0", json_license_rows[0])
        self.assertNotIn("MIT", json_license_rows[0])

    def test_cli_output_is_deterministic_and_failure_is_nonzero(self) -> None:
        command = [sys.executable, str(TOOL)]
        first = subprocess.run(command, check=True, capture_output=True)
        second = subprocess.run(command, check=True, capture_output=True)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(json.loads(first.stdout)["status"], "PASS")

        with tempfile.TemporaryDirectory(prefix="bsc-c13-cli-") as directory:
            changed = copy.deepcopy(self.construction)
            changed["construction"]["claimed_covered_triples"] = 286
            changed_path = self.write_json(Path(directory), "changed.json", changed)
            failed = subprocess.run(
                command + ["--construction", str(changed_path)],
                check=False,
                capture_output=True,
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn(b"C13-COVERING-VERIFY: FAIL", failed.stderr)


if __name__ == "__main__":
    unittest.main()
