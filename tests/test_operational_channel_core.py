from __future__ import annotations

import math
import re
import unittest
from fractions import Fraction
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent


def matmul(
    left: tuple[tuple[int, ...], ...],
    right: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


def transpose(
    matrix: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(zip(*matrix, strict=True))


class OperationalChannelCoreTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")

    def test_core_claim_roster_is_synchronized(self) -> None:
        identifiers = (
            "BSC-CHN-01",
            "BSC-CHN-02",
            "BSC-CHN-03",
            "BSC-QPH-02",
            "BSC-ENE-01",
            "BSC-ENE-02",
            "BSC-ENE-03",
            "BSC-ENC-01",
            "BSC-ENC-02",
            "BSC-ENC-03",
            "BSC-SEM-01",
            "BSC-UNI-01",
        )
        for relative in (
            "framework/Operational_Channel_Core.md",
            "ledgers/Claim_Status_Ledger.md",
            "paper/source/On_Boundaries_of_Evidence.tex",
        ):
            text = self.read(relative)
            for identifier in identifiers:
                with self.subTest(path=relative, identifier=identifier):
                    self.assertIn(identifier, text)

    def test_energy_port_gluing_localizes_exact_rational_residuals(
        self,
    ) -> None:
        def residual(
            dot_energy: Fraction,
            supply: Fraction,
            ports: tuple[Fraction, ...],
        ) -> Fraction:
            return dot_energy - supply - sum(ports)

        r_a = residual(Fraction(4), Fraction(10), (Fraction(-6),))
        r_b = residual(
            Fraction(4),
            Fraction(0),
            (Fraction(6), Fraction(-2)),
        )
        seam = Fraction(-6) + Fraction(6)
        global_residual = (
            Fraction(4 + 4) - Fraction(10) - Fraction(-2)
        )
        self.assertEqual((r_a, r_b, seam, global_residual), (0, 0, 0, 0))
        self.assertEqual(global_residual, r_a + r_b + seam)

        r_b_missing = residual(
            Fraction(3),
            Fraction(0),
            (Fraction(5), Fraction(-2)),
        )
        missing_seam = Fraction(-6) + Fraction(5)
        missing_global = (
            Fraction(4 + 3) - Fraction(10) - Fraction(-2)
        )
        self.assertEqual((r_a, r_b_missing), (0, 0))
        self.assertEqual(missing_seam, -1)
        self.assertEqual(missing_global, -1)
        self.assertEqual(missing_global, r_a + r_b_missing + missing_seam)

        r_interface = residual(
            Fraction(1),
            Fraction(0),
            (Fraction(6), Fraction(-5)),
        )
        seam_a_i = Fraction(-6) + Fraction(6)
        seam_i_b = Fraction(-5) + Fraction(5)
        repaired_global = (
            Fraction(4 + 1 + 3) - Fraction(10) - Fraction(-2)
        )
        self.assertEqual((r_interface, seam_a_i, seam_i_b), (0, 0, 0))
        self.assertEqual(repaired_global, 0)

        cancelling_seams = (Fraction(1), Fraction(-1))
        self.assertEqual(sum(cancelling_seams), 0)
        self.assertTrue(all(value != 0 for value in cancelling_seams))

    def test_energy_yields_keep_denominators_and_failures_typed(self) -> None:
        incident = Fraction(100)
        absorbed = Fraction(50)
        events = Fraction(40)
        self.assertEqual(events / incident, Fraction(2, 5))
        self.assertEqual(events / absorbed, Fraction(4, 5))
        self.assertNotEqual(events / incident, events / absorbed)

        success_probability = Fraction(1, 100)
        conditional_output = Fraction(1)
        input_per_attempt = Fraction(1)
        unconditional_efficiency = (
            success_probability * conditional_output / input_per_attempt
        )
        self.assertEqual(unconditional_efficiency, Fraction(1, 100))
        self.assertNotEqual(unconditional_efficiency, conditional_output)

        stages = (Fraction(4, 5), Fraction(3, 4), Fraction(1, 2))
        self.assertEqual(math.prod(stages), Fraction(3, 10))

    def test_energy_port_scope_gates_are_public_and_fail_closed(self) -> None:
        core = self.read("framework/Operational_Channel_Core.md")
        electromagnetic = self.read(
            "framework/Electromagnetic_Evidence_Bridge.md"
        )
        manuscript = self.read("paper/source/On_Boundaries_of_Evidence.tex")
        for fragment in (
            "global conservation residual therefore does not certify local seams",
            "Coordinate-time power, proper-time power",
            "interaction energy must be retained",
            "probability sink",
            "not an energy port",
        ):
            with self.subTest(surface="core", fragment=fragment):
                self.assertIn(fragment, core)
        for fragment in (
            "moving boundary",
            "Killing field",
            "directed surface element",
            "no universal local gravitational",
        ):
            with self.subTest(surface="electromagnetic", fragment=fragment):
                self.assertIn(fragment, electromagnetic)
        for fragment in ("BSC-ENE-02", "BSC-ENE-03"):
            with self.subTest(surface="manuscript", fragment=fragment):
                self.assertIn(fragment, manuscript)

    def test_pipeline_bound_uses_implemented_reachable_inputs(self) -> None:
        core = self.read("framework/Operational_Channel_Core.md")
        for fragment in (
            r"\widehat{\mathcal R}_{k-1}",
            "implemented reachable input",
            r"d_k(\widehat T_k\widehat z,T_k\widehat z)",
            r"\sum_{k=0}^{m}",
            r"\prod_{j=k+1}^{m}\eta_j",
            "does not resolve BSC-QOP-03",
            "normalized successful branch",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, core)

    def test_product_sum_recurrence_is_exact_over_rationals(self) -> None:
        defects = (
            Fraction(1, 100),
            Fraction(1, 50),
            Fraction(1, 40),
            Fraction(1, 25),
        )
        contractions = (
            None,
            Fraction(1, 2),
            Fraction(3, 4),
            Fraction(2, 3),
        )

        error = defects[0]
        for stage in range(1, len(defects)):
            error = defects[stage] + contractions[stage] * error

        weighted = sum(
            defects[k]
            * math.prod(
                contractions[j] for j in range(k + 1, len(defects))
            )
            for k in range(len(defects))
        )
        self.assertEqual(error, weighted)
        self.assertEqual(error, Fraction(83, 1200))

    def test_classical_report_kernel_contracts_total_variation(self) -> None:
        p = (Fraction(3, 4), Fraction(1, 4))
        q = (Fraction(1, 4), Fraction(3, 4))
        kernel = (
            (Fraction(3, 4), Fraction(1, 4)),
            (Fraction(1, 2), Fraction(1, 2)),
        )

        def push(law: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
            return tuple(
                sum(law[i] * kernel[i][j] for i in range(2))
                for j in range(2)
            )

        def tv(
            left: tuple[Fraction, ...],
            right: tuple[Fraction, ...],
        ) -> Fraction:
            return sum(abs(a - b) for a, b in zip(left, right)) / 2

        self.assertEqual(tv(p, q), Fraction(1, 2))
        self.assertEqual(tv(push(p), push(q)), Fraction(1, 8))
        self.assertLessEqual(tv(push(p), push(q)), tv(p, q))

    def test_forward_error_enlarges_inverse_compatible_sets(self) -> None:
        parameters = ("a", "b", "c", "d")
        actual = {"a": 0, "b": 2, "c": 5, "d": 9}
        ideal = {"a": 1, "b": 1, "c": 6, "d": 8}
        bound = max(abs(actual[x] - ideal[x]) for x in parameters)
        self.assertEqual(bound, 1)

        def compatible(
            report: dict[str, int],
            observation: int,
            radius: int,
        ) -> set[str]:
            return {
                x
                for x in parameters
                if abs(report[x] - observation) <= radius
            }

        for observation in range(-1, 11):
            for radius in range(4):
                with self.subTest(observation=observation, radius=radius):
                    self.assertLessEqual(
                        compatible(actual, observation, radius),
                        compatible(ideal, observation, radius + bound),
                    )
                    self.assertLessEqual(
                        compatible(ideal, observation, radius),
                        compatible(actual, observation, radius + bound),
                    )

    def test_spectral_marginal_and_postselection_counterexamples(self) -> None:
        root_half = 1 / math.sqrt(2)
        psi = (complex(root_half), complex(root_half))
        phi = (complex(root_half), complex(-root_half))
        self.assertEqual(
            tuple(abs(value) ** 2 for value in psi),
            tuple(abs(value) ** 2 for value in phi),
        )
        overlap = sum(a.conjugate() * b for a, b in zip(psi, phi))
        self.assertAlmostEqual(abs(overlap), 0.0)
        self.assertAlmostEqual(math.sqrt(1 - abs(overlap) ** 2), 1.0)

        rho = (Fraction(1, 2), Fraction(1, 2), Fraction(0))
        sigma = (Fraction(1, 2), Fraction(0), Fraction(1, 2))
        pre_distance = sum(abs(a - b) for a, b in zip(rho, sigma)) / 2
        self.assertEqual(pre_distance, Fraction(1, 2))
        rho_success = (Fraction(1), Fraction(0))
        sigma_success = (Fraction(0), Fraction(1))
        post_distance = (
            sum(abs(a - b) for a, b in zip(rho_success, sigma_success)) / 2
        )
        self.assertEqual(post_distance, 1)

    def test_bernoulli_count_support_blocks_finite_zero_error(self) -> None:
        for horizon in (1, 2, 7, 255):
            interior_support = set(range(horizon + 1))
            self.assertTrue({0}.intersection(interior_support))
            self.assertTrue({horizon}.intersection(interior_support))
            self.assertEqual(len(interior_support), horizon + 1)

        self.assertLess(math.log2(255), 8)
        self.assertEqual(math.log2(256), 8)
        self.assertEqual(Fraction(8, 1), Fraction(8, 1))
        self.assertEqual(Fraction(8, 8), 1)
        self.assertLess(Fraction(8, 10), 1)

        epsilon_95 = math.sqrt(math.log(512 / 0.05) / 600)
        self.assertAlmostEqual(epsilon_95, 0.12405682097728107)

    def test_same_identity_alignment_is_stronger_than_two_role_fit(self) -> None:
        identity = ((1, 0), (0, 1))
        swap = ((0, 1), (1, 0))

        independent = matmul(matmul(swap, identity), transpose(identity))
        self.assertEqual(independent, swap)

        permutations = (identity, swap)
        conjugates = {
            matmul(matmul(permutation, identity), transpose(permutation))
            for permutation in permutations
        }
        self.assertEqual(conjugates, {identity})
        self.assertNotIn(swap, conjugates)

    def test_source_crosswalk_is_primary_and_scope_bounded(self) -> None:
        application = self.read(
            "applications/Operational_Channel_Crosswalk_2026.md"
        )
        for doi in (
            "10.1038/s41377-026-02399-y",
            "10.1038/s41586-026-10825-9",
            "10.1126/sciadv.aeg8299",
            "10.1038/s41467-026-75783-2",
            "10.5281/zenodo.17906138",
        ):
            with self.subTest(doi=doi):
                self.assertIn(doi, application)
        for boundary in (
            "not an independent laboratory replay",
            "not a unified field",
            "pairwise disjoint finite-sample supports",
            "does not present",
            "None of the four studies derives that value",
            "supports no debris-population prevalence estimate",
            "controlled finite-dimensional truncation",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, application)

    def test_new_claim_ids_are_unique(self) -> None:
        ledger = self.read("ledgers/Claim_Status_Ledger.md")
        identifiers = re.findall(
            r"\|\s*(BSC-(?:CHN|ENE|ENC|SEM|UNI|QPH|PTC|HIR|MWN)-\d+)\s*\|",
            ledger,
        )
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(
            set(identifiers),
            {
                "BSC-CHN-01",
                "BSC-CHN-02",
                "BSC-CHN-03",
                "BSC-QPH-02",
                "BSC-ENE-01",
                "BSC-ENE-02",
                "BSC-ENE-03",
                "BSC-ENC-01",
                "BSC-ENC-02",
                "BSC-ENC-03",
                "BSC-SEM-01",
                "BSC-UNI-01",
                "BSC-QPH-01",
                "BSC-PTC-01",
                "BSC-HIR-01",
                "BSC-MWN-01",
            },
        )


if __name__ == "__main__":
    unittest.main()
