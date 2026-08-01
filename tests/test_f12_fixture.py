from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "F12_derived_holonomy_q"
GENERATOR = FIXTURE / "verify_derived_holonomy.py"
CHECKER = FIXTURE / "check_fixture.py"
INPUT = FIXTURE / "input.json"
RECEIPT = FIXTURE / "verification_receipt.json"
PROVENANCE = FIXTURE / "provenance.json"
SCHEMA = FIXTURE / "receipt.schema.json"


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def q(numerator: int, denominator: int = 1) -> dict[str, int]:
    return {"denominator": denominator, "numerator": numerator}


def matrix(
    rows: int, columns: int, entries: list[list[int | dict[str, int]]]
) -> dict[str, Any]:
    encoded = [
        [q(value) if type(value) is int else value for value in row]
        for row in entries
    ]
    return {"columns": columns, "entries": encoded, "rows": rows}


def zero_matrix(rows: int, columns: int) -> dict[str, Any]:
    return matrix(rows, columns, [[0 for _ in range(columns)] for _ in range(rows)])


def fixture_input(cases: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "cases": cases,
        "claim_id": "BSC-DHC-01",
        "evidence_status": "independent_reconstruction",
        "field": "Q",
        "fixture_claim_id": "BSC-FIX-12",
        "fixture_id": "F12-DERIVED-HOLONOMY-Q",
        "historical_replay_status": "NOT_REPLAYED",
        "schema": "bsc-derived-holonomy-input/1",
    }


def scalar_case(
    source_d: int,
    target_d: int,
    f1: int,
    f0: int,
    g1: int,
    g0: int,
    case_id: str = "scalar_case",
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "f": {"components": [matrix(1, 1, [[f0]]), matrix(1, 1, [[f1]])]},
        "g": {"components": [matrix(1, 1, [[g0]]), matrix(1, 1, [[g1]])]},
        "source": {
            "differentials": [matrix(1, 1, [[source_d]])],
            "dimensions": [1, 1],
            "maximum_degree": 1,
            "minimum_degree": 0,
        },
        "target": {
            "differentials": [matrix(1, 1, [[target_d]])],
            "dimensions": [1, 1],
            "maximum_degree": 1,
            "minimum_degree": 0,
        },
    }


def nontrivial_obstruction_case() -> dict[str, Any]:
    differential = matrix(2, 1, [[1], [0]])
    return {
        "case_id": "nontrivial_obstruction",
        "f": {
            "components": [
                matrix(2, 2, [[0, 0], [0, 1]]),
                zero_matrix(1, 1),
            ]
        },
        "g": {
            "components": [zero_matrix(2, 2), zero_matrix(1, 1)]
        },
        "source": {
            "differentials": [differential],
            "dimensions": [2, 1],
            "maximum_degree": 1,
            "minimum_degree": 0,
        },
        "target": {
            "differentials": [differential],
            "dimensions": [2, 1],
            "maximum_degree": 1,
            "minimum_degree": 0,
        },
    }


def nonsquare_pass_case() -> dict[str, Any]:
    return {
        "case_id": "nonsquare_pass",
        "f": {
            "components": [matrix(1, 2, [[2, 3]]), matrix(1, 1, [[2]])]
        },
        "g": {
            "components": [zero_matrix(1, 2), zero_matrix(1, 1)]
        },
        "source": {
            "differentials": [matrix(2, 1, [[1], [0]])],
            "dimensions": [2, 1],
            "maximum_degree": 1,
            "minimum_degree": 0,
        },
        "target": {
            "differentials": [matrix(1, 1, [[1]])],
            "dimensions": [1, 1],
            "maximum_degree": 1,
            "minimum_degree": 0,
        },
    }


def zero_degree_case(
    case_id: str, source_dimension: int, target_dimension: int
) -> dict[str, Any]:
    component = zero_matrix(target_dimension, source_dimension)
    return {
        "case_id": case_id,
        "f": {"components": [component]},
        "g": {"components": [copy.deepcopy(component)]},
        "source": {
            "differentials": [],
            "dimensions": [source_dimension],
            "maximum_degree": 0,
            "minimum_degree": 0,
        },
        "target": {
            "differentials": [],
            "dimensions": [target_dimension],
            "maximum_degree": 0,
            "minimum_degree": 0,
        },
    }


class F12DerivedHolonomyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.input_document = json.loads(INPUT.read_text(encoding="utf-8"))
        cls.receipt_document = json.loads(RECEIPT.read_text(encoding="utf-8"))
        cls.provenance_document = json.loads(PROVENANCE.read_text(encoding="utf-8"))
        cls.schema_document = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.generator = load_module(GENERATOR, "bsc_f12_generator_tests")
        cls.checker = load_module(CHECKER, "bsc_f12_checker_tests")

    def run_generator(self, input_path: Path, output_path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(GENERATOR), str(input_path), str(output_path)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
        )

    def run_checker(self, input_path: Path, receipt_path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                "--input",
                str(input_path),
                "--receipt",
                str(receipt_path),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
        )

    def write_document(self, path: Path, value: Any) -> None:
        path.write_bytes(canonical_bytes(value))

    def assert_generator_rejects(
        self, value: Any, expected: str | None = None
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-f12-invalid-input-") as temporary:
            root = Path(temporary)
            input_path = root / "input.json"
            output_path = root / "receipt.json"
            self.write_document(input_path, value)
            completed = self.run_generator(input_path, output_path)
            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(output_path.exists())
            if expected is not None:
                self.assertIn(expected, completed.stderr)

    def assert_checker_rejects(
        self,
        receipt: Any,
        input_value: Any | None = None,
        expected: str | None = None,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-f12-invalid-receipt-") as temporary:
            root = Path(temporary)
            input_path = root / "input.json"
            receipt_path = root / "receipt.json"
            self.write_document(
                input_path,
                self.input_document if input_value is None else input_value,
            )
            self.write_document(receipt_path, receipt)
            completed = self.run_checker(input_path, receipt_path)
            self.assertNotEqual(completed.returncode, 0)
            if expected is not None:
                self.assertIn(expected, completed.stderr)

    def generate_document(self, input_value: Any) -> tuple[bytes, dict[str, Any]]:
        with tempfile.TemporaryDirectory(prefix="bsc-f12-generate-") as temporary:
            root = Path(temporary)
            input_path = root / "input.json"
            output_path = root / "receipt.json"
            self.write_document(input_path, input_value)
            completed = self.run_generator(input_path, output_path)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            data = output_path.read_bytes()
        return data, json.loads(data)

    def test_retained_fixture_passes_independent_checker(self) -> None:
        completed = self.run_checker(INPUT, RECEIPT)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("PASS: 2 exact certificates", completed.stdout)

    def test_receipt_schema_is_complete_enforced_and_mutation_bound(self) -> None:
        schema_bytes = SCHEMA.read_bytes()
        for implementation in (self.generator, self.checker):
            with self.subTest(implementation=implementation.__name__):
                schema = implementation.validate_schema_document(
                    schema_bytes, self.schema_document
                )
                implementation.validate_schema_instance(
                    self.receipt_document, schema, schema
                )

                wrong_polarity = copy.deepcopy(self.receipt_document)
                wrong_polarity["results"][0]["certificate_type"] = "left_null"
                with self.assertRaises(
                    (self.generator.CertificateError, self.checker.VerificationError)
                ):
                    implementation.validate_schema_instance(
                        wrong_polarity, schema, schema
                    )

                weakened = copy.deepcopy(self.schema_document)
                weakened["$defs"]["pass_result"]["properties"]["certificate"] = {
                    "type": "object"
                }
                with self.assertRaises(
                    (self.generator.CertificateError, self.checker.VerificationError)
                ):
                    implementation.validate_schema_document(
                        canonical_bytes(weakened), weakened
                    )

                malformed = copy.deepcopy(self.schema_document)
                malformed["$defs"]["matrix"]["properties"]["entries"] = {
                    "type": "number"
                }
                with self.assertRaises(
                    (self.generator.CertificateError, self.checker.VerificationError)
                ):
                    implementation.validate_schema_definition(malformed)

    def test_required_fixture_outputs_are_exact(self) -> None:
        positive, negative = self.receipt_document["results"]
        self.assertEqual(positive["status"], "pass")
        self.assertEqual(positive["certificate_type"], "homotopy")
        self.assertEqual(
            positive["system"]["coefficient_matrix"],
            matrix(2, 1, [[1], [1]]),
        )
        self.assertEqual(positive["system"]["omega"], [q(1), q(1)])
        self.assertEqual(
            positive["certificate"]["homotopy"][0]["matrix"],
            matrix(1, 1, [[1]]),
        )
        self.assertEqual(negative["status"], "fail")
        self.assertEqual(negative["certificate_type"], "left_null")
        self.assertEqual(
            negative["system"]["coefficient_matrix"], matrix(1, 0, [[]])
        )
        self.assertEqual(negative["system"]["omega"], [q(1)])
        self.assertEqual(negative["certificate"]["left_null_witness"], [q(1)])
        self.assertEqual(negative["certificate"]["left_null_pairing"], q(1))

    def test_exhaustive_scalar_two_term_homology_regression(self) -> None:
        raw = valid = passes = failures = mismatches = 0
        for source_d, target_d, f1, f0, g1, g0 in itertools.product(
            (-1, 0, 1), repeat=6
        ):
            raw += 1
            if target_d * f1 != f0 * source_d:
                continue
            if target_d * g1 != g0 * source_d:
                continue
            valid += 1
            problem = self.generator.parse_problem(
                scalar_case(source_d, target_d, f1, f0, g1, g0), "scalar"
            )
            status, _ = self.generator.solve_system(
                self.generator.build_system(problem)
            )
            homology_equal = (
                source_d != 0
                or target_d != 0
                or (f0 == g0 and f1 == g1)
            )
            solver_equal = status == "pass"
            passes += int(solver_equal)
            failures += int(not solver_equal)
            mismatches += int(solver_equal != homology_equal)
        self.assertEqual(raw, 729)
        self.assertEqual(valid, 153)
        self.assertEqual(passes, 81)
        self.assertEqual(failures, 72)
        self.assertEqual(mismatches, 0)

    def test_deterministic_rref_free_variables_and_left_null_normalization(self) -> None:
        matrix_type = self.generator.Matrix
        system_type = self.generator.LinearSystem
        pass_system = system_type(
            matrix_type(1, 2, ((Fraction(1), Fraction(1)),)),
            (Fraction(1),),
            ((0, 0, 0),),
            ((0, 0, 0), (0, 0, 1)),
        )
        status, solution = self.generator.solve_system(pass_system)
        self.assertEqual(status, "pass")
        self.assertEqual(solution, (Fraction(1), Fraction(0)))

        fail_system = system_type(
            matrix_type(2, 1, ((Fraction(1),), (Fraction(1),))),
            (Fraction(1), Fraction(-1)),
            ((0, 0, 0), (1, 0, 0)),
            ((0, 0, 0),),
        )
        status, witness = self.generator.solve_system(fail_system)
        self.assertEqual(status, "fail")
        self.assertEqual(witness, (Fraction(1, 2), Fraction(-1, 2)))

    def test_nonsquare_known_homotopy_passes_independent_verification(self) -> None:
        input_value = fixture_input([nonsquare_pass_case()])
        data, receipt = self.generate_document(input_value)
        homotopy = receipt["results"][0]["certificate"]["homotopy"]
        self.assertEqual(homotopy[0]["matrix"], matrix(1, 2, [[2, 3]]))
        with tempfile.TemporaryDirectory(prefix="bsc-f12-nonsquare-") as temporary:
            root = Path(temporary)
            input_path = root / "input.json"
            receipt_path = root / "receipt.json"
            self.write_document(input_path, input_value)
            receipt_path.write_bytes(data)
            completed = self.run_checker(input_path, receipt_path)
            self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_zero_complexes_and_zero_dimensional_shapes_pass_exactly(self) -> None:
        input_value = fixture_input(
            [
                zero_degree_case("both_zero", 0, 0),
                zero_degree_case("source_zero", 0, 1),
                zero_degree_case("target_zero", 1, 0),
            ]
        )
        data, receipt = self.generate_document(input_value)
        for result in receipt["results"]:
            with self.subTest(case_id=result["case_id"]):
                self.assertEqual(result["status"], "pass")
                self.assertEqual(result["certificate"], {"homotopy": []})
                self.assertEqual(
                    result["system"]["coefficient_matrix"], matrix(0, 0, [])
                )
                self.assertEqual(result["system"]["omega"], [])
                self.assertEqual(result["system"]["row_coordinates"], [])
                self.assertEqual(result["system"]["column_coordinates"], [])
        with tempfile.TemporaryDirectory(prefix="bsc-f12-zero-") as temporary:
            root = Path(temporary)
            input_path = root / "input.json"
            receipt_path = root / "receipt.json"
            self.write_document(input_path, input_value)
            receipt_path.write_bytes(data)
            completed = self.run_checker(input_path, receipt_path)
            self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_invalid_complex_map_and_rational_inputs_fail_closed(self) -> None:
        mutations: list[tuple[str, Callable[[dict[str, Any]], None], str | None]] = []

        def add(name: str, mutation: Callable[[dict[str, Any]], None], expected: str | None = None) -> None:
            mutations.append((name, mutation, expected))

        def nonzero_d_squared(value: dict[str, Any]) -> None:
            case = value["cases"][0]
            complex_value = {
                "differentials": [matrix(1, 1, [[1]]), matrix(1, 1, [[1]])],
                "dimensions": [1, 1, 1],
                "maximum_degree": 2,
                "minimum_degree": 0,
            }
            case["source"] = copy.deepcopy(complex_value)
            case["target"] = copy.deepcopy(complex_value)
            case["f"]["components"] = [matrix(1, 1, [[1]])] * 3
            case["g"]["components"] = [matrix(1, 1, [[0]])] * 3

        add("d_squared", nonzero_d_squared, "nonzero d^2")
        add(
            "wrong_shape",
            lambda value: value["cases"][0]["source"]["differentials"][0].update(rows=2),
            "shape must be",
        )
        add(
            "invalid_f",
            lambda value: value["cases"][0]["f"]["components"][0]["entries"][0][0].update(numerator=0),
            "is not a chain map",
        )
        add(
            "invalid_g",
            lambda value: value["cases"][0]["g"]["components"][1]["entries"][0][0].update(numerator=1),
            "is not a chain map",
        )
        add(
            "string_fraction",
            lambda value: value["cases"][0]["f"]["components"][0]["entries"][0].__setitem__(0, "1/1"),
            "must be an object",
        )
        add(
            "float",
            lambda value: value["cases"][0]["f"]["components"][0]["entries"][0][0].update(numerator=1.0),
            "must be a JSON integer",
        )
        add(
            "boolean",
            lambda value: value["cases"][0]["f"]["components"][0]["entries"][0][0].update(numerator=True),
            "must be a JSON integer",
        )
        add(
            "zero_denominator",
            lambda value: value["cases"][0]["f"]["components"][0]["entries"][0][0].update(denominator=0),
            "must be positive",
        )
        add(
            "negative_denominator",
            lambda value: value["cases"][0]["f"]["components"][0]["entries"][0][0].update(denominator=-1),
            "must be positive",
        )
        add(
            "unreduced_fraction",
            lambda value: value["cases"][0]["f"]["components"][0]["entries"][0][0].update(numerator=2, denominator=2),
            "must be reduced",
        )
        add(
            "noncanonical_zero",
            lambda value: value["cases"][0]["g"]["components"][0]["entries"][0][0].update(denominator=2),
            "must be reduced",
        )
        add("arbitrary_ring", lambda value: value.update(field="Z"), "must be 'Q'")
        add("real_field", lambda value: value.update(field="R"), "must be 'Q'")
        add("modular_field", lambda value: value.update(field="GF(5)"), "must be 'Q'")
        add("missing_key", lambda value: value.pop("field"), "keys are not exact")
        add("extra_key", lambda value: value.update(version="v1.1.0"), "keys are not exact")

        for name, mutation, expected in mutations:
            with self.subTest(name=name):
                value = copy.deepcopy(self.input_document)
                mutation(value)
                self.assert_generator_rejects(value, expected)

    def test_duplicate_keys_and_nonfinite_numbers_are_rejected(self) -> None:
        canonical = canonical_bytes(self.input_document).decode("utf-8")
        raw_cases = {
            "duplicate": canonical.replace(
                '  "field": "Q",',
                '  "field": "Q",\n  "field": "Q",',
                1,
            ),
            "nan": canonical.replace('  "field": "Q",', '  "field": NaN,', 1),
            "infinity": canonical.replace(
                '  "field": "Q",', '  "field": Infinity,', 1
            ),
        }
        with tempfile.TemporaryDirectory(prefix="bsc-f12-raw-json-") as temporary:
            root = Path(temporary)
            for name, text in raw_cases.items():
                with self.subTest(name=name):
                    input_path = root / f"{name}.json"
                    output_path = root / f"{name}-receipt.json"
                    input_path.write_text(text, encoding="utf-8", newline="\n")
                    completed = self.run_generator(input_path, output_path)
                    self.assertNotEqual(completed.returncode, 0)
                    self.assertFalse(output_path.exists())

    def test_noncanonical_input_and_receipt_serialization_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bsc-f12-noncanonical-") as temporary:
            root = Path(temporary)
            input_path = root / "input.json"
            output_path = root / "output.json"
            input_path.write_text(
                json.dumps(self.input_document, sort_keys=False),
                encoding="utf-8",
                newline="\n",
            )
            completed = self.run_generator(input_path, output_path)
            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(output_path.exists())

            canonical_input = root / "canonical-input.json"
            noncanonical_receipt = root / "receipt.json"
            self.write_document(canonical_input, self.input_document)
            noncanonical_receipt.write_text(
                json.dumps(self.receipt_document, indent=4, sort_keys=True) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            completed = self.run_checker(canonical_input, noncanonical_receipt)
            self.assertNotEqual(completed.returncode, 0)

    def test_namespace_and_provenance_promotions_are_rejected(self) -> None:
        mutations = {
            "holography_claim": ("claim_id", "BSC-HOL-01"),
            "fixture_claim_f09": ("fixture_claim_id", "BSC-FIX-09"),
            "fixture_claim_f10": ("fixture_claim_id", "BSC-FIX-10"),
            "fixture_claim_f11": ("fixture_claim_id", "BSC-FIX-11"),
            "fixture_id_f09": ("fixture_id", "F09"),
            "fixture_id_f10": ("fixture_id", "F10-COUPLED-SURROGATE"),
            "fixture_id_f11": ("fixture_id", "F11-COLLATZ-RECURSIVE-SIEVE"),
            "published_version": ("fixture_id", "v1.1.0"),
            "mechanical_replay": ("evidence_status", "mechanically_replayed"),
            "kernel_status": ("evidence_status", "kernel_verified"),
            "historical_replay": ("historical_replay_status", "REPLAYED"),
        }
        for name, (key, replacement) in mutations.items():
            with self.subTest(name=name):
                value = copy.deepcopy(self.input_document)
                value[key] = replacement
                self.assert_generator_rejects(value)

        for key, replacement in (
            ("classification", "mechanically_replayed"),
            ("historical_replay_status", "REPLAYED"),
            ("kernel_verification_status", "kernel_verified"),
            ("mechanical_replay_status", "mechanically_replayed"),
        ):
            with self.subTest(provenance_key=key):
                value = copy.deepcopy(self.provenance_document)
                value[key] = replacement
                with self.assertRaises(self.checker.VerificationError):
                    self.checker.verify_provenance(value)

    def test_repository_namespace_allocations_are_unique(self) -> None:
        fixture_allocations = {
            "F09_zeta_dqpt_transfer": "F09",
            "F10_coupled_surrogate": "F10-COUPLED-SURROGATE",
            "F11_collatz_recursive_sieve": "F11-COLLATZ-RECURSIVE-SIEVE",
            "F12_derived_holonomy_q": "F12-DERIVED-HOLONOMY-Q",
        }

        def build_namespace(root: Path) -> None:
            ledger = root / "ledgers" / "Claim_Status_Ledger.md"
            ledger.parent.mkdir(parents=True)
            ledger.write_text(
                "\n".join(
                    [
                        "| BSC-DHC-01 | definition |",
                        "| BSC-FIX-09 | definition |",
                        "| BSC-FIX-10 | definition |",
                        "| BSC-FIX-11 | definition |",
                        "| BSC-FIX-12 | definition |",
                    ]
                )
                + "\n",
                encoding="utf-8",
                newline="\n",
            )
            for directory, fixture_id in fixture_allocations.items():
                input_path = root / "fixtures" / directory / "input.json"
                input_path.parent.mkdir(parents=True)
                self.write_document(input_path, {"fixture_id": fixture_id})

        with tempfile.TemporaryDirectory(prefix="bsc-f12-namespace-") as temporary:
            root = Path(temporary)
            build_namespace(root)
            self.checker.verify_namespace_allocations(root)

        mutations = {
            "duplicate_math_claim": lambda root: (
                root / "ledgers" / "Claim_Status_Ledger.md"
            ).write_text(
                (
                    root / "ledgers" / "Claim_Status_Ledger.md"
                ).read_text(encoding="utf-8")
                + "| BSC-DHC-01 | duplicate |\n",
                encoding="utf-8",
                newline="\n",
            ),
            "duplicate_fixture_claim": lambda root: (
                root / "ledgers" / "Claim_Status_Ledger.md"
            ).write_text(
                (
                    root / "ledgers" / "Claim_Status_Ledger.md"
                ).read_text(encoding="utf-8")
                + "| BSC-FIX-12 | duplicate |\n",
                encoding="utf-8",
                newline="\n",
            ),
            "duplicate_runtime_id": lambda root: self.write_document(
                root / "fixtures" / "F13_alias" / "input.json",
                {"fixture_id": "F12-DERIVED-HOLONOMY-Q"},
            ),
            "duplicate_f12_prefix": lambda root: self.write_document(
                root / "fixtures" / "F12_alias" / "input.json",
                {"fixture_id": "UNRELATED"},
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory(
                prefix="bsc-f12-namespace-negative-"
            ) as temporary:
                root = Path(temporary)
                build_namespace(root)
                if name in {"duplicate_runtime_id", "duplicate_f12_prefix"}:
                    (root / "fixtures" / (
                        "F13_alias" if name == "duplicate_runtime_id" else "F12_alias"
                    )).mkdir(parents=True)
                mutation(root)
                with self.assertRaises(self.checker.VerificationError):
                    self.checker.verify_namespace_allocations(root)

    def test_tampered_pass_fail_and_recorded_systems_are_rejected(self) -> None:
        mutations: list[tuple[str, Callable[[dict[str, Any]], None], str | None]] = []

        def add(name: str, mutation: Callable[[dict[str, Any]], None], expected: str | None = None) -> None:
            mutations.append((name, mutation, expected))

        add(
            "tampered_h",
            lambda value: value["results"][0]["certificate"]["homotopy"][0]["matrix"]["entries"][0][0].update(numerator=0),
            "does not satisfy",
        )
        add(
            "wrong_h_shape",
            lambda value: value["results"][0]["certificate"]["homotopy"][0]["matrix"].update(columns=0),
            "shape must be",
        )
        add(
            "tampered_y_zero_pairing",
            lambda value: value["results"][1]["certificate"]["left_null_witness"][0].update(numerator=0),
            "wrong omega pairing",
        )
        add(
            "rescaled_y",
            lambda value: (
                value["results"][1]["certificate"]["left_null_witness"][0].update(numerator=2),
                value["results"][1]["certificate"]["left_null_pairing"].update(numerator=2),
            ),
            "normalized",
        )
        add(
            "polarity_swap",
            lambda value: value["results"][0].update(status="fail"),
            "polarity",
        )
        add(
            "both_witnesses",
            lambda value: value["results"][0]["certificate"].update(left_null_witness=[]),
            "keys are not exact",
        )
        add(
            "neither_witness",
            lambda value: value["results"][0]["certificate"].pop("homotopy"),
            "keys are not exact",
        )
        add(
            "tampered_A",
            lambda value: value["results"][0]["system"]["coefficient_matrix"]["entries"][0][0].update(numerator=0),
            "coordinate system mismatch",
        )
        add(
            "tampered_omega",
            lambda value: value["results"][0]["system"]["omega"][0].update(numerator=0),
            "coordinate system mismatch",
        )
        add(
            "tampered_coordinate",
            lambda value: value["results"][0]["system"]["row_coordinates"][0].update(row=1),
            "coordinate system mismatch",
        )
        add(
            "wrong_case_digest",
            lambda value: value["results"][0].update(case_sha256="0" * 64),
            "case digest mismatch",
        )
        add(
            "wrong_input_digest",
            lambda value: value.update(input_sha256="0" * 64),
            "input_sha256 mismatch",
        )
        add(
            "numerical_proof_flag",
            lambda value: value.update(proof="numerical_agreement"),
            "keys are not exact",
        )
        add(
            "mechanical_status",
            lambda value: value.update(evidence_status="mechanically_replayed"),
            "evidence_status mismatch",
        )

        for name, mutation, expected in mutations:
            with self.subTest(name=name):
                value = copy.deepcopy(self.receipt_document)
                mutation(value)
                self.assert_checker_rejects(value, expected=expected)

    def test_left_null_witness_must_be_null_on_every_A_column(self) -> None:
        input_value = fixture_input([nontrivial_obstruction_case()])
        _, receipt = self.generate_document(input_value)
        result = receipt["results"][0]
        self.assertEqual(result["status"], "fail")
        result["certificate"]["left_null_witness"] = [
            q(1),
            q(0),
            q(0),
            q(1),
            q(0),
        ]
        self.assert_checker_rejects(
            receipt,
            input_value=input_value,
            expected="not null on A column",
        )

    def test_certificate_is_bound_to_exact_input_and_mathematics(self) -> None:
        input_value = copy.deepcopy(self.input_document)
        positive = input_value["cases"][0]
        positive["f"] = copy.deepcopy(positive["g"])
        self.assert_checker_rejects(
            self.receipt_document,
            input_value=input_value,
            expected="input_sha256 mismatch",
        )

        forged = copy.deepcopy(self.receipt_document)
        input_data = canonical_bytes(input_value)
        forged["input_sha256"] = hashlib.sha256(input_data).hexdigest()
        forged["results"][0]["case_sha256"] = hashlib.sha256(
            canonical_bytes(positive)
        ).hexdigest()
        self.assert_checker_rejects(
            forged,
            input_value=input_value,
            expected="coordinate system mismatch",
        )

    def test_generation_is_byte_deterministic_and_refuses_overwrite(self) -> None:
        first, _ = self.generate_document(self.input_document)
        second, _ = self.generate_document(self.input_document)
        self.assertEqual(first, second)
        self.assertEqual(first, RECEIPT.read_bytes())

        with tempfile.TemporaryDirectory(prefix="bsc-f12-overwrite-") as temporary:
            output = Path(temporary) / "existing.json"
            output.write_bytes(b"occupied\n")
            completed = self.run_generator(INPUT, output)
            self.assertNotEqual(completed.returncode, 0)
            self.assertEqual(output.read_bytes(), b"occupied\n")

        retained_before = RECEIPT.read_bytes()
        completed = self.run_generator(INPUT, RECEIPT)
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(RECEIPT.read_bytes(), retained_before)


if __name__ == "__main__":
    unittest.main()
