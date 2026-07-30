from __future__ import annotations

import re
import unittest
from fractions import Fraction
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent


class SimulationEvidenceFrameworkTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")

    def test_profile_is_a_certificate_refinement_not_a_morphism_field(
        self,
    ) -> None:
        framework = self.read("framework/Simulation_Evidence_Profile.md")
        self.assertIn(r"\mathsf{SEC}_{c,\iota}", framework)
        self.assertIn("does not add a field to the", framework)
        paper = self.read("paper/source/On_Boundaries_of_Evidence.tex")
        self.assertIn(r"\mathsf{SEC}_{c,\iota}", paper)
        self.assertIn("not a ninth field", paper)

    def test_compatibility_theorem_preserves_uncertainty_and_unit_boundaries(
        self,
    ) -> None:
        framework = self.read("framework/Simulation_Evidence_Profile.md")
        required = (
            r"\ell^1_{c,j}",
            r"\ell^0_{c,j}+\rho_{c,j}",
            r"U^0_{c,j}+\rho_{c,j}\le\tau_{c,j}",
            "is not counted",
            "common units",
            r"I^1_{c,j}",
            "deployment profile is evaluated",
            r"s_{c,j}",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, framework)

    def test_deficiency_and_proxy_boundaries_are_explicit(self) -> None:
        framework = self.read("framework/Simulation_Evidence_Profile.md")
        self.assertIn(
            r"\delta(\mathsf E,\mathsf F)\le e(K_0)",
            framework,
        )
        self.assertIn(r"W_1(P,Q)=\epsilon", framework)
        self.assertIn(r"d_{\mathrm{TV}}(P,Q)=1", framework)
        self.assertIn(r"\delta(\mathsf E,\mathsf F)=\frac12", framework)
        self.assertIn("does not show that $K_0$ is optimal", framework)

    def test_source_and_target_coordinates_are_typed_and_propagated(
        self,
    ) -> None:
        framework = self.read("framework/Simulation_Evidence_Profile.md")
        for fragment in (
            r"I_c^{\ell}",
            r"J_c^{\ell}",
            r"\mathcal V_c=\prod_{i\in I_c^\ell}V_{c,i}",
            r"\mathcal W_c=\prod_{j\in J_c^\ell}W_{c,j}",
            r"\Phi_c:\mathcal V_c\to\mathcal W_c",
            r"\boldsymbol U_c^0",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, framework)

    def test_joint_probability_and_zero_failure_semantics_are_explicit(
        self,
    ) -> None:
        framework = self.read("framework/Simulation_Evidence_Profile.md")
        self.assertIn(
            r"$(\Omega_c,\mathcal F_c,\mathbb P_c)$",
            framework,
        )
        self.assertIn("requires every marginal guarantee", framework)
        self.assertIn("does not by itself prove that the", framework)
        self.assertIn("probability-one admission, not", framework)

    def test_factored_identity_is_synchronized_across_surfaces(self) -> None:
        factors = (
            r"\iota_{\mathrm{cand}}",
            r"\iota_{\mathrm{data}}",
            r"\iota_{\mathrm{analysis}}",
            r"\iota_{\mathrm{env}}",
            r"\iota_{\mathrm{contract}}",
        )
        for relative in (
            "framework/Simulation_Evidence_Profile.md",
            "paper/source/On_Boundaries_of_Evidence.tex",
            "ledgers/Symbol_and_Notation_Ledger.md",
        ):
            text = self.read(relative)
            for factor in factors:
                with self.subTest(path=relative, factor=factor):
                    self.assertIn(factor, text)

    def test_f10_exact_prefix_arithmetic_has_the_declared_transition(
        self,
    ) -> None:
        tolerance = Fraction(1, 20)
        interface_error = Fraction(1, 100)

        def prefixes(a: Fraction) -> list[Fraction]:
            error = Fraction(0)
            values = []
            for _ in range(10):
                error = a * error + interface_error
                values.append(error)
            return values

        host_a = prefixes(Fraction(1, 2))
        host_b = prefixes(Fraction(9, 10))
        self.assertEqual(host_a[-1], Fraction(1023, 51200))
        self.assertLess(host_a[-1], tolerance)
        self.assertLessEqual(host_b[5], tolerance)
        self.assertGreater(host_b[6], tolerance)
        self.assertEqual(
            host_b[-1],
            Fraction(6513215599, 100000000000),
        )

    def test_claim_ids_are_unique_and_publicly_routed(self) -> None:
        ledger = self.read("ledgers/Claim_Status_Ledger.md")
        identifiers = re.findall(r"\|\s*(BSC-(?:SIM|FIX)-\d+)\s*\|", ledger)
        self.assertEqual(len(identifiers), len(set(identifiers)))
        for identifier in (
            "BSC-SIM-01",
            "BSC-SIM-02",
            "BSC-SIM-03",
            "BSC-FIX-10",
        ):
            self.assertIn(identifier, identifiers)
        self.assertIn(
            "framework/Simulation_Evidence_Profile.md",
            self.read("README.md"),
        )
        self.assertIn(
            "framework/Simulation_Evidence_Profile.md",
            self.read("synopsis/Reader_Map.md"),
        )


if __name__ == "__main__":
    unittest.main()
