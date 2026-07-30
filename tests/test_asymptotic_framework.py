from __future__ import annotations

import cmath
import math
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
FRAMEWORK_CLAIMS = (
    "BSC-QUO-03",
    "BSC-SCL-05",
    "BSC-SCL-06",
    "BSC-SCL-07",
    "BSC-SCL-08",
)


class AsymptoticFrameworkTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")

    def test_framework_module_is_linked_from_public_surfaces(self) -> None:
        module = self.read("framework/Normalized_Scale_Profiles.md")
        readme = self.read("README.md")
        application = self.read("applications/Riemann_DQPT_Transfer.md")
        self.assertIn("normalized scale profile", module.lower())
        self.assertIn(
            "framework/Normalized_Scale_Profiles.md",
            readme,
        )
        self.assertIn(
            "../framework/Normalized_Scale_Profiles.md",
            application,
        )

    def test_general_claim_ids_are_unique_in_ledger(self) -> None:
        ledger = self.read("ledgers/Claim_Status_Ledger.md")
        for claim_id in FRAMEWORK_CLAIMS:
            self.assertEqual(
                ledger.count(f"| {claim_id} |"),
                1,
                f"{claim_id} must have exactly one ledger row",
            )

    def test_manuscript_contains_core_theorem_package(self) -> None:
        manuscript = self.read(
            "paper/source/On_Boundaries_of_Evidence.tex"
        )
        for label in (
            "def:certscalefamily",
            "def:normscaleprofile",
            "prop:normcollapse",
            "thm:rateadd",
            "prop:normcovariance",
            "prop:ratestability",
            "thm:ratesupport",
            "prop:slicevisibility",
            "def:dqptcert",
            "thm:analyticzerotransfer",
            "thm:rootstability",
            "prop:decisiondescent",
        ):
            self.assertIn(label, manuscript)

    def test_normalization_collapse_does_not_create_finite_zeros(self) -> None:
        values = [1.0 / n for n in (10, 100, 1000, 10000)]
        self.assertTrue(all(value != 0.0 for value in values))
        self.assertTrue(
            all(later < earlier for earlier, later in zip(values, values[1:]))
        )
        self.assertLess(values[-1], 1e-3)

    def test_additive_power_rate_identity(self) -> None:
        gamma = 0.7
        kappa = 0.3
        for n in (10, 100, 1000, 10000):
            carrier = n ** (-kappa)
            normalizer = n**gamma
            observable = carrier / normalizer
            rate = -math.log(abs(observable)) / math.log(n)
            self.assertTrue(math.isclose(rate, gamma + kappa))

    def test_eta_tail_bound_has_a_certified_numerical_witness(self) -> None:
        s = 0.6 + 2.3j
        truncation = 40
        reference_truncation = 5000

        def partial_eta(limit: int) -> complex:
            return sum(
                (1 if index % 2 else -1)
                * cmath.exp(-s * math.log(index))
                for index in range(1, limit + 1)
            )

        def certified_tail_bound(limit: int) -> float:
            beta = s.real
            return limit ** (-beta) * (1.0 + abs(s) / beta)

        certified_upper_enclosure = abs(
            partial_eta(reference_truncation) - partial_eta(truncation)
        ) + certified_tail_bound(reference_truncation)
        self.assertLessEqual(
            certified_upper_enclosure,
            certified_tail_bound(truncation),
        )

    def test_fixed_s_exponent_regression_separates_known_branches(self) -> None:
        beta = 0.5
        ordinates_and_targets = (
            (0.0, 1.0 - beta),
            (14.134725141734693, 1.0),
        )
        truncations = (500, 5000, 50000)

        def exponent(limit: int, ordinate: float) -> float:
            s = beta + 1j * ordinate
            carrier = sum(
                (1 if index % 2 else -1)
                * cmath.exp(-s * math.log(index))
                for index in range(1, limit + 1)
            )
            normalizer = sum(
                index ** (-beta) for index in range(1, limit + 1)
            )
            coherence = -carrier / normalizer
            return -math.log(abs(coherence)) / math.log(limit)

        for ordinate, target in ordinates_and_targets:
            errors = [
                abs(exponent(limit, ordinate) - target)
                for limit in truncations
            ]
            self.assertTrue(
                all(
                    later < earlier
                    for earlier, later in zip(errors, errors[1:])
                )
            )
            self.assertLess(errors[-1], 0.15)

    def test_binary_total_variation_bound_is_attained_in_fixture(self) -> None:
        p0 = (0.9, 0.1)
        p1 = (0.4, 0.6)
        total_variation = 0.5 * sum(
            abs(left - right) for left, right in zip(p0, p1)
        )
        lower_bound = (1.0 - total_variation) / 2.0
        optimal_equal_prior_error = (p0[1] + p1[0]) / 2.0
        self.assertTrue(
            math.isclose(lower_bound, optimal_equal_prior_error)
        )

    def test_rate_stability_bound_holds_away_from_zero(self) -> None:
        ideal = 0.5
        observed = 0.51
        margin = 0.5
        epsilon = abs(observed - ideal)
        scale = math.log(100)
        actual = abs(
            -math.log(abs(observed)) / scale
            + math.log(abs(ideal)) / scale
        )
        bound = -math.log(1.0 - epsilon / margin) / scale
        self.assertLessEqual(actual, bound)

    def test_proof_audit_hypotheses_remain_explicit(self) -> None:
        module = " ".join(
            self.read("framework/Normalized_Scale_Profiles.md").split()
        )
        for required in (
            r"0<\inf_{x\in K}|Z_N(x)|",
            r"\rho(x)\in\mathbb R",
            r"domain in $\mathbb C$",
            "finite with its discrete sigma-algebra",
            r"\mathcal R(x)=\lim_{N\to\infty}\mathcal R_N(x)",
        ):
            self.assertIn(required, module)

    def test_zeta_rate_is_a_framework_instance_with_visible_slice(self) -> None:
        application = self.read("applications/Riemann_DQPT_Transfer.md")
        normalized = application.replace(" ", "")
        self.assertIn(r"\lambda_N=\logN", normalized)
        self.assertIn("BSC-SCL-05b", application)
        self.assertIn("BSC-SCL-07b", application)
        self.assertIn("fixed-$\\beta$ real-time slice", application)
        self.assertIn(r"\{\log2\}", normalized)

    def test_framework_does_not_assert_an_infinite_system(self) -> None:
        module = self.read("framework/Normalized_Scale_Profiles.md").lower()
        for boundary in (
            "does not by itself construct an infinite-system state",
            "not a new morphism field",
            "mathematical singularity versus physical dqpt",
            "estimator distribution",
        ):
            self.assertIn(boundary, module)

    def test_scale_family_does_not_change_the_morphism_tuple(self) -> None:
        manuscript = self.read(
            "paper/source/On_Boundaries_of_Evidence.tex"
        )
        equation = re.search(
            r"\\begin\{equation\}\\label\{eq:morphism\}"
            r"(.*?)\\end\{equation\}",
            manuscript,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(equation)
        compact = " ".join(equation.group(1).split())
        self.assertEqual(
            compact,
            r"\mathfrak M_{\ell\to m}= \left( "
            r"T_{\ell m},T_{\ell m}^{\sharp},K_{\ell m},R_{\ell m}, "
            r"\Theta_{\ell m},\delta_{\ell m},C_{\ell m},"
            r"\Cert_{\ell m} \right),",
        )
        module = self.read("framework/Normalized_Scale_Profiles.md")
        module_flat = " ".join(module.split())
        self.assertIn("directed comparison family", module)
        self.assertIn(
            "No categorical identity or composition law is inferred",
            module_flat,
        )


if __name__ == "__main__":
    unittest.main()
