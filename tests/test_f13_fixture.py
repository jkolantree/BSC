from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "F13_lorentz_auxiliary_passivity"
INPUT = FIXTURE / "input.json"
RECEIPT = FIXTURE / "verification_receipt.json"
PROVENANCE = FIXTURE / "provenance.json"
SCHEMA = FIXTURE / "receipt.schema.json"
FRAMEWORK = ROOT / "framework" / "Lorentz_Auxiliary_State_Passivity.md"
GENERATOR = FIXTURE / "verify_lorentz_passivity.py"
CHECKER = FIXTURE / "check_fixture.py"


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def q(numerator: int, denominator: int = 1) -> dict[str, int]:
    return {"denominator": denominator, "numerator": numerator}


def fraction(value: dict[str, int]) -> Fraction:
    return Fraction(value["numerator"], value["denominator"])


GEN = load_module(GENERATOR, "bsc_f13_generator_tests")
CHK = load_module(CHECKER, "bsc_f13_checker_tests")


class F13LorentzPassivityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.input_document = json.loads(INPUT.read_text(encoding="utf-8"))
        cls.receipt_document = json.loads(RECEIPT.read_text(encoding="utf-8"))

    def generate_from_document(self, value: Any) -> dict[str, Any]:
        with tempfile.TemporaryDirectory(prefix="bsc-f13-input-") as directory:
            path = Path(directory) / "input.json"
            path.write_bytes(canonical_bytes(value))
            return GEN.generate_receipt(path)

    def verify_mutated_receipt(self, mutator: Callable[[dict[str, Any]], None]) -> None:
        value = copy.deepcopy(self.receipt_document)
        mutator(value)
        with tempfile.TemporaryDirectory(prefix="bsc-f13-receipt-") as directory:
            receipt_path = Path(directory) / "receipt.json"
            receipt_path.write_bytes(canonical_bytes(value))
            with self.assertRaises(CHK.VerificationError):
                CHK.verify_receipt(
                    receipt_path=receipt_path,
                    regenerate=False,
                    verify_namespaces=False,
                )

    def test_retained_fixture_passes_and_values_are_exact(self) -> None:
        receipt_bytes, count = CHK.verify_receipt(regenerate=False)
        self.assertEqual(count, 4)
        self.assertEqual(receipt_bytes, RECEIPT.read_bytes())

        results = {item["case_id"]: item for item in self.receipt_document["results"]}
        dissipative = results["fixed_dissipative"]
        self.assertEqual(fraction(dissipative["material"]["storage"]), Fraction(7, 4))
        self.assertEqual(fraction(dissipative["material"]["loss_rate"]), 2)
        self.assertEqual(fraction(dissipative["material"]["storage_rate"]), 8)
        self.assertEqual(fraction(dissipative["state"]["v_dot"]), 5)
        self.assertEqual(
            fraction(dissipative["integrated_balance"]["total_energy_rate"]), -32
        )

        lossless = results["fixed_lossless"]
        self.assertEqual(fraction(lossless["material"]["storage"]), Fraction(11, 6))
        self.assertEqual(fraction(lossless["material"]["loss_rate"]), 0)
        self.assertEqual(fraction(lossless["material"]["storage_rate"]), -12)
        self.assertEqual(
            fraction(lossless["integrated_balance"]["material_energy"]),
            Fraction(11, 3),
        )
        self.assertEqual(
            fraction(lossless["integrated_balance"]["material_energy_rate"]), -24
        )
        self.assertEqual(
            fraction(lossless["integrated_balance"]["total_energy_rate"]), 3
        )
        self.assertEqual(
            fraction(lossless["integrated_balance"]["inward_port_power"]), -5
        )

        varying_b = results["varying_b_pump"]
        self.assertEqual(fraction(varying_b["material"]["pump_rate"]), 1)
        self.assertEqual(fraction(varying_b["material"]["storage_rate"]), 9)
        self.assertEqual(
            fraction(varying_b["integrated_balance"]["total_energy_rate"]), -31
        )

        varying_a = results["varying_a_pump"]
        self.assertEqual(fraction(varying_a["material"]["pump_rate"]), Fraction(-7, 4))
        self.assertEqual(
            fraction(varying_a["material"]["storage_rate"]), Fraction(25, 4)
        )
        self.assertEqual(
            fraction(varying_a["integrated_balance"]["total_energy_rate"]),
            Fraction(-135, 4),
        )

        for result in results.values():
            self.assertEqual(
                fraction(result["material"]["storage_rate"]),
                fraction(result["material"]["storage_rate_balance"]),
            )
            self.assertEqual(fraction(result["material"]["material_residual"]), 0)
            self.assertEqual(
                fraction(result["integrated_balance"]["maxwell_residual"]), 0
            )
            self.assertEqual(
                fraction(result["integrated_balance"]["coupled_residual"]), 0
            )
            self.assertEqual(
                fraction(result["integrated_balance"]["inward_port_residual"]), 0
            )

        proof = self.receipt_document["symbolic_proof"]
        self.assertFalse(proof["sampling_used"])
        self.assertEqual(proof["fixed_material_residual_terms"], [])
        self.assertEqual(proof["fixed_coupled_residual_terms"], [])
        self.assertEqual(proof["varying_material_residual_terms"], [])
        self.assertEqual(proof["varying_coupled_residual_terms"], [])
        self.assertEqual(len(proof["varying_pump_scaled_numerator_terms"]), 3)

    def test_generation_is_byte_deterministic_and_refuses_overwrite(self) -> None:
        CHK.regenerate_and_compare(INPUT, RECEIPT.read_bytes(), FIXTURE, FRAMEWORK)

        retained_before = RECEIPT.read_bytes()
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            [
                sys.executable,
                str(GENERATOR),
                "--input",
                str(INPUT),
                "--output",
                str(RECEIPT),
                "--fixture-dir",
                str(FIXTURE),
                "--framework",
                str(FRAMEWORK),
            ],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(RECEIPT.read_bytes(), retained_before)

    def test_nonpositive_storage_and_negative_damping_fail_closed(self) -> None:
        mutations = (
            ("zero_a", "a", q(0)),
            ("negative_a", "a", q(-1)),
            ("zero_b", "b", q(0)),
            ("negative_b", "b", q(-1)),
            ("negative_gamma", "gamma", q(-1)),
            ("zero_measure", "spatial_measure", q(0)),
        )
        for name, key, replacement in mutations:
            with self.subTest(name=name):
                value = copy.deepcopy(self.input_document)
                value["cases"][0][key] = replacement
                with self.assertRaises(GEN.CertificateError):
                    self.generate_from_document(value)

    def test_lossless_dissipative_and_modulation_labels_are_exact(self) -> None:
        mutations = (
            (0, "passive_lossless"),
            (1, "passive_dissipative"),
            (2, "passive_dissipative"),
            (3, "pump_accounted_lossless"),
        )
        for index, classification in mutations:
            with self.subTest(index=index, classification=classification):
                value = copy.deepcopy(self.input_document)
                value["cases"][index]["classification"] = classification
                with self.assertRaises(GEN.CertificateError):
                    self.generate_from_document(value)

    def test_pump_omission_sign_and_each_derivative_term_fail_closed(self) -> None:
        omitted = copy.deepcopy(self.input_document)
        del omitted["cases"][2]["declared_pump_rate"]
        with self.assertRaises(GEN.CertificateError):
            self.generate_from_document(omitted)

        sign_flipped_b = copy.deepcopy(self.input_document)
        sign_flipped_b["cases"][2]["declared_pump_rate"] = q(-1)
        with self.assertRaises(GEN.CertificateError):
            self.generate_from_document(sign_flipped_b)

        sign_flipped_a = copy.deepcopy(self.input_document)
        sign_flipped_a["cases"][3]["declared_pump_rate"] = q(7, 4)
        with self.assertRaises(GEN.CertificateError):
            self.generate_from_document(sign_flipped_a)

        one_term_only = copy.deepcopy(self.input_document)
        case = one_term_only["cases"][2]
        case["a_dot"] = q(2)
        case["declared_pump_rate"] = q(1)
        with self.assertRaises(GEN.CertificateError):
            self.generate_from_document(one_term_only)

        structurally_fixed = copy.deepcopy(self.input_document)
        structurally_fixed["cases"][2]["b_dot"] = q(0)
        with self.assertRaises(GEN.CertificateError):
            self.generate_from_document(structurally_fixed)

    def test_maxwell_polarization_free_current_and_port_signs_fail_closed(self) -> None:
        mutations = (
            ("wrong_polarization_sign", "em_energy_rate_integral", q(-20)),
            ("wrong_free_current_sign", "em_energy_rate_integral", q(30)),
            ("wrong_outward_flux", "outward_flux_integral", q(5)),
        )
        for name, key, replacement in mutations:
            with self.subTest(name=name):
                value = copy.deepcopy(self.input_document)
                value["cases"][0][key] = replacement
                with self.assertRaises(GEN.CertificateError):
                    self.generate_from_document(value)

    def test_rational_and_json_inputs_are_fail_closed(self) -> None:
        rational_mutations = (
            ("boolean", {"denominator": 1, "numerator": True}),
            ("unreduced", q(2, 2)),
            ("negative_denominator", q(1, -2)),
            ("noncanonical_zero", q(0, 2)),
        )
        for name, replacement in rational_mutations:
            with self.subTest(name=name):
                value = copy.deepcopy(self.input_document)
                value["cases"][0]["a"] = replacement
                with self.assertRaises(GEN.CertificateError):
                    self.generate_from_document(value)

        raw_mutants = {
            "float": INPUT.read_bytes().replace(b'"numerator": 2', b'"numerator": 2.0', 1),
            "exponent": INPUT.read_bytes().replace(b'"numerator": 2', b'"numerator": 2e0', 1),
            "nan": INPUT.read_bytes().replace(b'"numerator": 2', b'"numerator": NaN', 1),
            "duplicate": b'{"schema":"x","schema":"y"}\n',
            "crlf": INPUT.read_bytes().replace(b"\n", b"\r\n"),
            "bom": b"\xef\xbb\xbf" + INPUT.read_bytes(),
            "noncanonical_whitespace": INPUT.read_bytes().replace(b"  \"arithmetic_field\"", b" \"arithmetic_field\"", 1),
        }
        with tempfile.TemporaryDirectory(prefix="bsc-f13-json-") as directory:
            for name, data in raw_mutants.items():
                with self.subTest(name=name):
                    path = Path(directory) / f"{name}.json"
                    path.write_bytes(data)
                    with self.assertRaises(GEN.CertificateError):
                        GEN.load_canonical_json(path, name)

    def test_receipt_math_identity_and_scope_tampering_is_rejected(self) -> None:
        mutations: tuple[Callable[[dict[str, Any]], None], ...] = (
            lambda value: value["results"][2]["material"].__setitem__("pump_rate", q(-1)),
            lambda value: value["results"][0]["integrated_balance"].__setitem__(
                "maxwell_residual", q(1)
            ),
            lambda value: value["results"][1]["integrated_balance"].__setitem__(
                "total_energy_rate", q(4)
            ),
            lambda value: value["results"][0]["material"].__setitem__(
                "storage_rate", q(9)
            ),
            lambda value: value["results"][0].__setitem__("classification", "passive_lossless"),
            lambda value: value["symbolic_proof"].__setitem__("sampling_used", True),
            lambda value: value["symbolic_proof"].__setitem__(
                "varying_pump_scaled_numerator_terms", []
            ),
            lambda value: value.__setitem__("claim_id", "BSC-EM-11"),
            lambda value: value.__setitem__("historical_replay_status", "REPLAYED"),
            lambda value: value.__setitem__("device_efficiency", True),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(mutation=index):
                self.verify_mutated_receipt(mutation)

    def test_every_bound_artifact_mutation_is_rejected(self) -> None:
        names = ("input", "framework", "generator", "checker", "schema", "provenance")
        for name in names:
            with self.subTest(artifact=name), tempfile.TemporaryDirectory(
                prefix="bsc-f13-bound-"
            ) as directory:
                root = Path(directory)
                fixture_copy = root / "fixtures" / "F13_lorentz_auxiliary_passivity"
                framework_copy = root / "framework" / FRAMEWORK.name
                fixture_copy.parent.mkdir(parents=True)
                framework_copy.parent.mkdir(parents=True)
                shutil.copytree(FIXTURE, fixture_copy)
                shutil.copy2(FRAMEWORK, framework_copy)

                if name == "input":
                    value = json.loads((fixture_copy / "input.json").read_text(encoding="utf-8"))
                    value["cases"][0]["p"] = q(2)
                    (fixture_copy / "input.json").write_bytes(canonical_bytes(value))
                elif name == "framework":
                    framework_copy.write_bytes(framework_copy.read_bytes() + b"\n")
                elif name == "generator":
                    path = fixture_copy / GENERATOR.name
                    path.write_bytes(path.read_bytes() + b"\n# altered\n")
                elif name == "checker":
                    path = fixture_copy / CHECKER.name
                    path.write_bytes(path.read_bytes() + b"\n# altered\n")
                elif name == "schema":
                    value = json.loads(
                        (fixture_copy / SCHEMA.name).read_text(encoding="utf-8")
                    )
                    value["$id"] = value["$id"] + ":altered"
                    (fixture_copy / SCHEMA.name).write_bytes(canonical_bytes(value))
                elif name == "provenance":
                    value = json.loads(
                        (fixture_copy / PROVENANCE.name).read_text(encoding="utf-8")
                    )
                    value["external_source_dependency"] = "claimed"
                    (fixture_copy / PROVENANCE.name).write_bytes(canonical_bytes(value))

                with self.assertRaises(CHK.VerificationError):
                    CHK.verify_receipt(
                        input_path=fixture_copy / INPUT.name,
                        receipt_path=fixture_copy / RECEIPT.name,
                        fixture_dir=fixture_copy,
                        framework_path=framework_copy,
                        repository_root=ROOT,
                        regenerate=False,
                        verify_namespaces=False,
                    )

    def test_evidence_promotions_and_sample_to_theorem_claims_are_rejected(self) -> None:
        mutations = (
            ("evidence_status", "mechanically_replayed"),
            ("historical_replay_status", "REPLAYED"),
            ("fixture_scope", "sampled_trajectory_proves_continuous_pde"),
            ("theorem_scope", "anisotropic_device_efficiency"),
        )
        for key, replacement in mutations:
            with self.subTest(key=key):
                value = copy.deepcopy(self.input_document)
                value[key] = replacement
                with self.assertRaises(GEN.CertificateError):
                    self.generate_from_document(value)

        unit_promotion = copy.deepcopy(self.input_document)
        unit_promotion["unit_convention"]["absolute_physical_energy_claim"] = True
        with self.assertRaises(GEN.CertificateError):
            self.generate_from_document(unit_promotion)

        case_promotion = copy.deepcopy(self.input_document)
        case_promotion["cases"][0]["case_scope"] = "continuous_solution_verified"
        with self.assertRaises(GEN.CertificateError):
            self.generate_from_document(case_promotion)

        profile_promotion = copy.deepcopy(self.input_document)
        profile_promotion["spatial_profile"] = "arbitrary_profile_or_separate_averages"
        with self.assertRaises(GEN.CertificateError):
            self.generate_from_document(profile_promotion)

    def test_namespace_allocations_are_unique_and_released_roster_is_frozen(self) -> None:
        CHK.verify_namespace_allocations(ROOT)
        ledger = (ROOT / "ledgers" / "Claim_Status_Ledger.md").read_text(encoding="utf-8")
        self.assertEqual(ledger.count("| BSC-EM-12 |"), 1)
        self.assertEqual(ledger.count("| BSC-FIX-13 |"), 1)
        self.assertNotIn(
            "BSC-EM-12",
            (ROOT / "framework" / "Electromagnetic_Evidence_Bridge.md").read_text(
                encoding="utf-8"
            ),
        )
        self.assertNotIn(
            "BSC-EM-12",
            (ROOT / "paper" / "source" / "On_Boundaries_of_Evidence.tex").read_text(
                encoding="utf-8"
            ),
        )
        for synopsis_path in (ROOT / "synopsis").rglob("*"):
            if synopsis_path.is_file() and synopsis_path.suffix in {".md", ".tex"}:
                self.assertNotIn(
                    "BSC-EM-12", synopsis_path.read_text(encoding="utf-8")
                )
        bridge_test = (ROOT / "tests" / "test_electromagnetic_evidence_bridge.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("range(1, 12)", bridge_test)
        self.assertNotIn("range(1, 13)", bridge_test)

    def test_duplicate_ledger_runtime_and_prefix_allocations_are_rejected(self) -> None:
        ledger = (ROOT / "ledgers" / "Claim_Status_Ledger.md").read_text(encoding="utf-8")
        f13_row = next(line for line in ledger.splitlines() if line.startswith("| BSC-FIX-13 |"))

        with tempfile.TemporaryDirectory(prefix="bsc-f13-namespace-") as directory:
            root = Path(directory)
            (root / "ledgers").mkdir()
            fixture = root / "fixtures" / "F13_lorentz_auxiliary_passivity"
            fixture.mkdir(parents=True)
            (root / "ledgers" / "Claim_Status_Ledger.md").write_text(
                ledger + "\n" + f13_row + "\n", encoding="utf-8"
            )
            shutil.copy2(INPUT, fixture / "input.json")
            shutil.copy2(RECEIPT, fixture / "verification_receipt.json")
            with self.assertRaises(CHK.VerificationError):
                CHK.verify_namespace_allocations(root)

        with tempfile.TemporaryDirectory(prefix="bsc-f13-namespace-") as directory:
            root = Path(directory)
            (root / "ledgers").mkdir()
            fixture = root / "fixtures" / "F13_lorentz_auxiliary_passivity"
            fixture.mkdir(parents=True)
            (root / "ledgers" / "Claim_Status_Ledger.md").write_text(
                ledger + "\n  " + f13_row + "\n", encoding="utf-8"
            )
            shutil.copy2(INPUT, fixture / "input.json")
            with self.assertRaises(CHK.VerificationError):
                CHK.verify_namespace_allocations(root)

        with tempfile.TemporaryDirectory(prefix="bsc-f13-namespace-") as directory:
            root = Path(directory)
            (root / "ledgers").mkdir()
            fixtures = root / "fixtures"
            fixture = fixtures / "F13_lorentz_auxiliary_passivity"
            fixture.mkdir(parents=True)
            (fixtures / "F13_alias").mkdir()
            (root / "ledgers" / "Claim_Status_Ledger.md").write_text(
                ledger, encoding="utf-8"
            )
            shutil.copy2(INPUT, fixture / "input.json")
            shutil.copy2(RECEIPT, fixture / "verification_receipt.json")
            with self.assertRaises(CHK.VerificationError):
                CHK.verify_namespace_allocations(root)

        with tempfile.TemporaryDirectory(prefix="bsc-f13-namespace-") as directory:
            root = Path(directory)
            (root / "ledgers").mkdir()
            fixtures = root / "fixtures"
            fixture = fixtures / "F13_lorentz_auxiliary_passivity"
            fixture.mkdir(parents=True)
            (fixtures / "F13").mkdir()
            (root / "ledgers" / "Claim_Status_Ledger.md").write_text(
                ledger, encoding="utf-8"
            )
            shutil.copy2(INPUT, fixture / "input.json")
            with self.assertRaises(CHK.VerificationError):
                CHK.verify_namespace_allocations(root)

        with tempfile.TemporaryDirectory(prefix="bsc-f13-namespace-") as directory:
            root = Path(directory)
            (root / "ledgers").mkdir()
            fixtures = root / "fixtures"
            fixture = fixtures / "F13_lorentz_auxiliary_passivity"
            collision = fixtures / "alias"
            fixture.mkdir(parents=True)
            collision.mkdir()
            (root / "ledgers" / "Claim_Status_Ledger.md").write_text(
                ledger, encoding="utf-8"
            )
            shutil.copy2(INPUT, fixture / "input.json")
            shutil.copy2(RECEIPT, fixture / "verification_receipt.json")
            (collision / "input.json").write_bytes(
                canonical_bytes({"fixture_id": "F13-LORENTZ-AUXILIARY-PASSIVITY"})
            )
            with self.assertRaises(CHK.VerificationError):
                CHK.verify_namespace_allocations(root)

        for name, malformed in (
            ("duplicate_key", b'{"fixture_id":"other","fixture_id":"F13-LORENTZ-AUXILIARY-PASSIVITY"}\n'),
            ("malformed", b'{"fixture_id":\n'),
            ("non_string", b'{"fixture_id":13}\n'),
        ):
            with self.subTest(namespace_input=name), tempfile.TemporaryDirectory(
                prefix="bsc-f13-namespace-"
            ) as directory:
                root = Path(directory)
                (root / "ledgers").mkdir()
                fixtures = root / "fixtures"
                fixture = fixtures / "F13_lorentz_auxiliary_passivity"
                alias = fixtures / "alias"
                fixture.mkdir(parents=True)
                alias.mkdir()
                (root / "ledgers" / "Claim_Status_Ledger.md").write_text(
                    ledger, encoding="utf-8"
                )
                shutil.copy2(INPUT, fixture / "input.json")
                (alias / "input.json").write_bytes(malformed)
                with self.assertRaises(CHK.VerificationError):
                    CHK.verify_namespace_allocations(root)

    def test_checker_is_code_independent_and_cli_fails_on_output_alias(self) -> None:
        checker_source = CHECKER.read_text(encoding="utf-8")
        self.assertNotIn("import verify_lorentz_passivity", checker_source)
        self.assertNotIn("from verify_lorentz_passivity", checker_source)
        input_before = INPUT.read_bytes()
        completed = subprocess.run(
            [
                sys.executable,
                str(GENERATOR),
                "--input",
                str(INPUT),
                "--output",
                str(INPUT),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(INPUT.read_bytes(), input_before)


if __name__ == "__main__":
    unittest.main()
