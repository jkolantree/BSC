from __future__ import annotations

import copy
import hashlib
import inspect
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import q26_grid_annihilator_checker as GRID  # noqa: E402


class Q26GridAnnihilatorCheckerTests(unittest.TestCase):
    def test_patched_lean_validation_receipt_binds_full_project_projection(self) -> None:
        source_manifest = ROOT / "applications" / "Q26_lean_4_32_2_source_sha256.txt"
        receipt_path = ROOT / "applications" / "Q26_lean_4_32_2_validation.json"
        project = ROOT / "formal" / "q26_grid_annihilator"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        manifest_bytes = source_manifest.read_bytes()
        self.assertEqual(
            hashlib.sha256(manifest_bytes).hexdigest(),
            receipt["subject"]["source_manifest_sha256"],
        )
        lines = manifest_bytes.decode("utf-8").splitlines()
        self.assertEqual(len(lines), receipt["subject"]["source_file_count"])
        seen: set[str] = set()
        for line in lines:
            digest, separator, relative = line.partition("  ")
            self.assertEqual(separator, "  ")
            self.assertEqual(len(digest), 64)
            self.assertNotIn(relative, seen)
            seen.add(relative)
            target = (project / relative).resolve()
            self.assertTrue(target.is_relative_to(project.resolve()))
            self.assertTrue(target.is_file())
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), digest)
        expected = {
            "Q26GridAnnihilator.lean",
            "lake-manifest.json",
            "lakefile.toml",
            "lean-toolchain",
        }
        expected.update(
            path.relative_to(project).as_posix()
            for path in (project / "Q26GridAnnihilator").rglob("*.lean")
        )
        self.assertEqual(seen, expected)
        self.assertEqual(
            receipt["authority"],
            {
                "exact_cardinality_thirteen": "EXTERNALLY_CHECKED",
                "gamma_q26_equals_fourteen": (
                    "COMPOSITE_CONSEQUENCE_WITH_CITED_LOWER_BOUND_AND_CHECKED_WITNESS"
                ),
                "root_cnf_status": "UNKNOWN_UNCHANGED",
            },
        )
        checks = {item["id"]: item for item in receipt["checks"]}
        self.assertEqual(checks["linux_comparator_nanoda"]["status"], "PASS")
        self.assertTrue(checks["linux_comparator_nanoda"]["nanoda_enabled"])
        self.assertEqual(
            checks["linux_comparator_nanoda"]["permitted_axioms"],
            ["propext", "Quot.sound", "Classical.choice"],
        )
        self.assertEqual(checks["windows_leanchecker_fresh"]["status"], "NOT_CHECKED")
        self.assertEqual(checks["windows_leanchecker_fresh"]["termination"], "TIMEOUT")
        self.assertEqual(
            checks["windows_leanchecker_fresh"]["timeout_limit_seconds"], 900
        )
        external = checks["linux_comparator_nanoda"]
        comparator_receipt_path = ROOT / external["receipt_path"]
        comparator_receipt = json.loads(
            comparator_receipt_path.read_text(encoding="utf-8")
        )
        transcript = ROOT / external["transcript_path"]
        self.assertEqual(
            hashlib.sha256(transcript.read_bytes()).hexdigest(),
            comparator_receipt["comparator_log_sha256"],
        )
        validation_dir = comparator_receipt_path.parent
        for filename, key in (
            ("TrustedChallenge.lean", "challenge_sha256"),
            ("comparator-config.json", "config_sha256"),
        ):
            self.assertEqual(
                hashlib.sha256((validation_dir / filename).read_bytes()).hexdigest(),
                comparator_receipt[key],
            )
        projection = validation_dir / "evidence" / "lean-source-projection-sha256.txt"
        self.assertEqual(
            hashlib.sha256(projection.read_bytes()).hexdigest(),
            comparator_receipt["source_projection_manifest_sha256"],
        )
        self.assertEqual(comparator_receipt["status"], "DUAL_KERNEL_ACCEPTED")
        self.assertEqual(
            comparator_receipt["checks"]["wsl_leanchecker_fresh"],
            "TIMEOUT_10_MINUTES_NO_DIAGNOSTIC",
        )
        self.assertEqual(
            comparator_receipt["checks"]["challenge_build"],
            "PASS_1595_JOBS_TRANSCRIPT",
        )
        self.assertEqual(
            comparator_receipt["checks"]["solution_build"],
            "PASS_8675_JOBS_TRANSCRIPT",
        )
        self.assertEqual(comparator_receipt["root_cnf_status"], "UNKNOWN_UNCHANGED")

    def test_checker_is_independent_of_existing_profile_tools(self) -> None:
        source = inspect.getsource(GRID)
        self.assertNotIn("q26_symmetry_profiles", source)
        self.assertNotIn("Q26_symmetry_parity_profiles.json", source)

    def test_full_coarse_domains_and_orbits_are_reconstructed(self) -> None:
        for kind, expected in GRID.EXPECTED_COARSE.items():
            domain = GRID.coarse_domain(kind)
            self.assertEqual((len(domain), len(GRID.representatives(kind, domain))), expected)

    def test_exact_cn_filter_leaves_only_the_five_orbits(self) -> None:
        for kind in GRID.INVENTORIES:
            raw = GRID.survivor_domain(kind)
            self.assertEqual(raw, GRID.EXPECTED_RAW_SURVIVORS[kind])
            self.assertEqual(
                GRID.representatives(kind, raw),
                GRID.EXPECTED_REPRESENTATIVES[kind],
            )
        self.assertFalse(GRID.cn_profile_ok("W0", (0, 7)))

    def test_cn_boundaries_use_every_exact_top_coefficient(self) -> None:
        for rows, columns, queens in ((6, 7, 6), (6, 8, 6), (8, 5, 6), (8, 8, 7)):
            self.assertTrue(GRID.cn_grid_ok(rows, columns, queens))
        self.assertFalse(GRID.cn_grid_ok(8, 7, 6))
        self.assertFalse(GRID.cn_grid_ok(7, 7, 6))
        self.assertTrue(GRID.cn_grid_ok(0, 100, 6))
        self.assertTrue(GRID.cn_grid_ok(100, 0, 6))

    def test_duplicate_parity_lifts_and_q_tables_are_exact(self) -> None:
        for key, expected in GRID.EXPECTED_CANONICAL_LIFTS.items():
            kind, pair = key
            actual = GRID.feasible_lifts(kind, pair)
            self.assertEqual(actual, expected)
            for _, _, table in actual:
                self.assertEqual(table[3], 3)
                self.assertEqual(table[0] + table[3], 6)
                self.assertEqual(table[1] + table[2], 7)
        self.assertIsNone(GRID.parity_table(0, 0))
        self.assertEqual(
            GRID.feasible_lifts("W2", (0, 7)),
            ((0, 0, (0, 0, 7, 6)),),
        )

    def test_binomial_ratios_derive_the_four_used_moments(self) -> None:
        expected = {
            (6, 7, 6): (1, 1),
            (6, 8, 6): (1, 1),
            (8, 5, 6): (4, 3),
            (8, 8, 7): (8, 7),
        }
        for arguments, coefficients in expected.items():
            relation = GRID.row_moment(*arguments)
            self.assertIsNotNone(relation)
            self.assertEqual(
                (relation["r_coefficient"], relation["a_coefficient"]),
                coefficients,
            )
        self.assertIsNone(GRID.row_moment(7, 7, 7))
        self.assertIsNone(GRID.row_moment(8, 6, 7))

    def test_every_raw_symmetry_partner_and_lift_closes(self) -> None:
        raw_lifts = 0
        for kind in GRID.INVENTORIES:
            raw = GRID.survivor_domain(kind)
            self.assertEqual(set().union(*(GRID.orbit(kind, pair) for pair in raw)), set(raw))
            for pair in raw:
                for lift in GRID.feasible_lifts(kind, pair):
                    raw_lifts += 1
                    closure = GRID.valuation_closure(kind, pair, lift)
                    self.assertTrue(closure["closed"])
                    self.assertTrue(closure["conflicts"])
        self.assertEqual(raw_lifts, 12)

    def test_w0_5_8_requires_incompatible_even_color_and_odd_color_moments(self) -> None:
        lift = GRID.feasible_lifts("W0", (5, 8))[0]
        closure = GRID.valuation_closure("W0", (5, 8), lift)
        a0_values = {
            item["inferred_v2"]
            for item in closure["inferences"]
            if item["line_sum_name"] == "A0"
        }
        self.assertEqual(a0_values, {2, 3})
        self.assertIn(
            "INCOMPATIBLE_MOMENTS",
            {item["code"] for item in closure["conflicts"]},
        )

    def test_report_is_deterministic_scoped_and_fail_closed_on_mutation(self) -> None:
        first = GRID.build_report()
        second = GRID.build_report()
        self.assertEqual(GRID.canonical_json_bytes(first), GRID.canonical_json_bytes(second))
        self.assertEqual(first["totals"]["coarse_orbits"], 156)
        self.assertEqual(first["totals"]["survivor_orbits"], 5)
        self.assertEqual(first["totals"]["canonical_closed_lifts"], 6)
        self.assertEqual(first["authority"]["root_cnf_status"], "UNKNOWN_UNCHANGED")
        self.assertIn(
            "all difference or sum labels are distinct",
            first["authority"]["does_not_assert"],
        )
        mutation = copy.deepcopy(first)
        mutation["canonical_cases"][0]["lifts"][0]["q_table"][3] = 2
        with self.assertRaises(GRID.GridCheckError):
            GRID.verify_report(mutation)

    def test_known_q6_w0_dominator_refutes_the_unused_independence_overclaim(self) -> None:
        queens = ((1, 1), (3, 5), (5, 3))
        for row in range(1, 7):
            for column in range(1, 7):
                self.assertTrue(
                    any(
                        row == qr
                        or column == qc
                        or row - column == qr - qc
                        or row + column == qr + qc
                        for qr, qc in queens
                    )
                )
        self.assertEqual(len({row for row, _ in queens}), 3)
        self.assertEqual(len({column for _, column in queens}), 3)
        self.assertLess(len({row + column for row, column in queens}), 3)


if __name__ == "__main__":
    unittest.main()
