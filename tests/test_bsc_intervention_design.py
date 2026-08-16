from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import bsc_intervention_design as DESIGN  # noqa: E402


FIXTURE = ROOT / "fixtures" / "F14_intervention_identifiability"
INPUT = FIXTURE / "input.json"
EXPECTED = FIXTURE / "expected_report.json"
CHECKER = TOOLS / "bsc_intervention_design.py"


def rational(numerator: int, denominator: int = 1) -> dict[str, int]:
    return {"denominator": denominator, "numerator": numerator}


class BSCInterventionDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.input_bytes, cls.input_value = DESIGN.load_canonical_json(INPUT)
        cls.problem = DESIGN.parse_problem(cls.input_value)
        cls.report = DESIGN.build_report(cls.input_bytes, cls.input_value, CHECKER)

    def test_positive_fixture_has_two_exact_minimum_cost_designs(self) -> None:
        exact = self.report["exact_identifiability"]
        self.assertEqual(exact["minimum_cost"], rational(2))
        self.assertEqual(
            exact["all_minimum_cost_families"],
            [["direct"], ["column", "row"]],
        )
        self.assertEqual(exact["selected_family"], ["direct"])
        self.assertEqual(exact["intervention_family_count_checked"], 8)
        self.assertEqual(exact["target_separated_pair_count"], 6)
        self.assertTrue(exact["cross_check_methods_agree"])

    def test_fiber_and_pair_cover_algorithms_agree_on_every_subset(self) -> None:
        for family in DESIGN.all_families(self.problem):
            self.assertEqual(
                DESIGN.fiber_identifies(self.problem, family),
                DESIGN.pair_cover_identifies(self.problem, family),
                family,
            )
        self.assertFalse(DESIGN.fiber_identifies(self.problem, ("column",)))
        self.assertTrue(DESIGN.fiber_identifies(self.problem, ("direct",)))
        self.assertTrue(
            DESIGN.pair_cover_identifies(self.problem, ("column", "row"))
        )

    def test_exact_rational_oscillation_queries(self) -> None:
        observed = {
            tuple(item["family"]): Fraction(
                item["maximum_target_oscillation"]["numerator"],
                item["maximum_target_oscillation"]["denominator"],
            )
            for item in self.report["oscillation_queries"]
        }
        self.assertEqual(
            observed,
            {
                (): Fraction(7, 2),
                ("column",): Fraction(3),
                ("direct",): Fraction(3, 2),
                ("row",): Fraction(3, 2),
                ("column", "row"): Fraction(0),
                ("column", "direct", "row"): Fraction(0),
            },
        )

    def test_retained_report_is_canonical_and_source_bound(self) -> None:
        expected_bytes, expected_value = DESIGN.load_canonical_json(EXPECTED, "report")
        self.assertEqual(expected_value, self.report)
        self.assertEqual(expected_bytes, DESIGN.canonical_json_bytes(self.report))
        self.assertEqual(
            self.report["source_binding"]["input_sha256"],
            DESIGN.sha256(self.input_bytes),
        )
        self.assertEqual(
            self.report["source_binding"]["checker_sha256"],
            DESIGN.sha256(CHECKER.read_bytes()),
        )

    def test_cli_report_is_byte_deterministic(self) -> None:
        command = [sys.executable, str(CHECKER), str(INPUT), "--json"]
        first = subprocess.run(command, check=False, capture_output=True)
        second = subprocess.run(command, check=False, capture_output=True)
        self.assertEqual(first.returncode, 0, first.stderr.decode())
        self.assertEqual(second.returncode, 0, second.stderr.decode())
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first.stdout, EXPECTED.read_bytes())

    def test_duplicate_json_key_is_rejected_before_model_parsing(self) -> None:
        with self.assertRaisesRegex(DESIGN.DesignError, "duplicate JSON key"):
            DESIGN.load_canonical_json_bytes(b'{"x":1,"x":2}\n')

    def test_float_and_noncanonical_serialization_are_rejected(self) -> None:
        with self.assertRaisesRegex(DESIGN.DesignError, "floating-point"):
            DESIGN.load_canonical_json_bytes(b'{"x":1.0}\n')
        noncanonical = (json.dumps(self.input_value) + "\n").encode("utf-8")
        self.assertNotEqual(noncanonical, self.input_bytes)
        with self.assertRaisesRegex(DESIGN.DesignError, "not canonical JSON"):
            DESIGN.load_canonical_json_bytes(noncanonical)

    def test_duplicate_states_and_interventions_are_rejected(self) -> None:
        duplicate_state = copy.deepcopy(self.input_value)
        duplicate_state["states"].append("s3")
        with self.assertRaisesRegex(DESIGN.DesignError, "duplicate identifier"):
            DESIGN.parse_problem(duplicate_state)

        duplicate_intervention = copy.deepcopy(self.input_value)
        duplicate_intervention["interventions"][1]["id"] = "column"
        with self.assertRaisesRegex(DESIGN.DesignError, "duplicate id"):
            DESIGN.parse_problem(duplicate_intervention)

    def test_missing_and_extra_state_reports_are_rejected(self) -> None:
        missing = copy.deepcopy(self.input_value)
        missing["interventions"][0]["reports"].pop("s3")
        with self.assertRaisesRegex(DESIGN.DesignError, "state coverage mismatch"):
            DESIGN.parse_problem(missing)

        extra = copy.deepcopy(self.input_value)
        extra["target"]["values"]["s4"] = "q0"
        with self.assertRaisesRegex(DESIGN.DesignError, "state coverage mismatch"):
            DESIGN.parse_problem(extra)

    def test_unknown_report_point_is_rejected(self) -> None:
        mutation = copy.deepcopy(self.input_value)
        mutation["interventions"][0]["reports"]["s0"] = "undeclared"
        with self.assertRaisesRegex(DESIGN.DesignError, "outside the declared metric"):
            DESIGN.parse_problem(mutation)

    def test_incomplete_metric_is_rejected(self) -> None:
        mutation = copy.deepcopy(self.input_value)
        mutation["target"]["metric"]["distances"].pop()
        with self.assertRaisesRegex(DESIGN.DesignError, "must cover all 16 ordered pairs"):
            DESIGN.parse_problem(mutation)

    def test_nonmetric_distance_table_is_rejected(self) -> None:
        mutation = copy.deepcopy(self.input_value)
        distances = mutation["interventions"][1]["metric"]["distances"]
        for entry in distances:
            if (entry["left"], entry["right"]) in {("a", "d"), ("d", "a")}:
                entry["distance"] = rational(2)
        with self.assertRaisesRegex(DESIGN.DesignError, "triangle inequality"):
            DESIGN.parse_problem(mutation)

    def test_nonreduced_rational_and_negative_cost_are_rejected(self) -> None:
        nonreduced = copy.deepcopy(self.input_value)
        nonreduced["interventions"][0]["cost"] = rational(2, 2)
        with self.assertRaisesRegex(DESIGN.DesignError, "must be reduced"):
            DESIGN.parse_problem(nonreduced)

        negative = copy.deepcopy(self.input_value)
        negative["interventions"][0]["cost"] = rational(-1)
        with self.assertRaisesRegex(DESIGN.DesignError, "must be nonnegative"):
            DESIGN.parse_problem(negative)

    def test_uncovered_target_pair_fails_closed(self) -> None:
        mutation = copy.deepcopy(self.input_value)
        mutation["interventions"][0]["reports"]["s1"] = "0"
        mutation["interventions"][1]["reports"]["s1"] = "a"
        with self.assertRaisesRegex(DESIGN.DesignError, "pairs are uncovered"):
            DESIGN.parse_problem(mutation)

    def test_exhaustive_resource_ceiling_fails_closed(self) -> None:
        with mock.patch.object(DESIGN, "MAX_EXHAUSTIVE_OPERATIONS", 1):
            with self.assertRaisesRegex(DESIGN.DesignError, "operation bound"):
                DESIGN.parse_problem(copy.deepcopy(self.input_value))

    def test_duplicate_or_unknown_oscillation_query_fails_closed(self) -> None:
        duplicate = copy.deepcopy(self.input_value)
        duplicate["oscillation_queries"].append(["row"])
        with self.assertRaisesRegex(DESIGN.DesignError, "duplicate family"):
            DESIGN.parse_problem(duplicate)

        unknown = copy.deepcopy(self.input_value)
        unknown["oscillation_queries"][1] = ["missing"]
        with self.assertRaisesRegex(DESIGN.DesignError, "unknown ids"):
            DESIGN.parse_problem(unknown)

    def test_closed_top_level_and_source_mutation_binding(self) -> None:
        extra = copy.deepcopy(self.input_value)
        extra["undeclared"] = True
        with self.assertRaisesRegex(DESIGN.DesignError, "keys mismatch"):
            DESIGN.parse_problem(extra)

        mutation = copy.deepcopy(self.input_value)
        mutation["problem_id"] = "F14-INTERVENTION-IDENTIFIABILITY-MUTATION"
        mutation_bytes = DESIGN.canonical_json_bytes(mutation)
        mutated_report = DESIGN.build_report(mutation_bytes, mutation, CHECKER)
        self.assertNotEqual(
            mutated_report["source_binding"]["input_sha256"],
            self.report["source_binding"]["input_sha256"],
        )

    def test_cli_malformed_input_returns_failure_without_report(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-f14-test-") as temporary:
            path = Path(temporary) / "duplicate.json"
            path.write_bytes(b'{"x":1,"x":2}\n')
            completed = subprocess.run(
                [sys.executable, str(CHECKER), str(path), "--json"],
                check=False,
                capture_output=True,
            )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stdout, b"")
        self.assertIn(b"duplicate JSON key", completed.stderr)

    def test_oversized_input_deep_nesting_integer_and_surrogate_fail_typed(self) -> None:
        hostile_inputs = (
            b" " * (DESIGN.MAX_INPUT_BYTES + 1),
            b"[" * 100 + b"0" + b"]" * 100,
            b'{"x":999999999999999999999999999999999999}\n',
            b'{"x":"\\ud800"}\n',
        )
        for payload in hostile_inputs:
            with self.subTest(payload=payload[:32]):
                with self.assertRaises(DESIGN.DesignError) as raised:
                    DESIGN.load_canonical_json_bytes(payload)
                self.assertNotIn("Traceback", str(raised.exception))

    def test_cli_io_failure_does_not_disclose_private_path(self) -> None:
        private_name = "PRIVATE-ABSENT-F14-INPUT.json"
        private_path = ROOT / private_name
        completed = subprocess.run(
            [sys.executable, str(CHECKER), str(private_path), "--json"],
            check=False,
            capture_output=True,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stdout, b"")
        self.assertIn(b"cannot read input", completed.stderr)
        self.assertNotIn(private_name.encode(), completed.stderr)
        self.assertNotIn(b"Traceback", completed.stderr)

    def test_rational_operand_ceiling_fails_closed(self) -> None:
        mutation = copy.deepcopy(self.input_value)
        mutation["interventions"][0]["cost"] = rational(
            DESIGN.MAX_RATIONAL_COMPONENT + 1
        )
        with self.assertRaisesRegex(DESIGN.DesignError, "absolute bound"):
            DESIGN.parse_problem(mutation)

    def test_metric_and_query_work_ceilings_fail_closed(self) -> None:
        with mock.patch.object(DESIGN, "MAX_METRIC_VALIDATION_OPERATIONS", 1):
            with self.assertRaisesRegex(DESIGN.DesignError, "metric validation"):
                DESIGN.parse_problem(copy.deepcopy(self.input_value))
        with mock.patch.object(DESIGN, "MAX_OSCILLATION_QUERIES", 1):
            with self.assertRaisesRegex(DESIGN.DesignError, "oscillation_queries"):
                DESIGN.parse_problem(copy.deepcopy(self.input_value))

    def test_report_minimizer_ceiling_fails_closed(self) -> None:
        with mock.patch.object(DESIGN, "MAX_REPORTED_MINIMIZERS", 1):
            with self.assertRaisesRegex(DESIGN.DesignError, "minimum-family report"):
                DESIGN.build_report(self.input_bytes, self.input_value, CHECKER)


if __name__ == "__main__":
    unittest.main()
