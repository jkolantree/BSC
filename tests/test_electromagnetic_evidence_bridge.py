from __future__ import annotations

import cmath
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
EM_CLAIMS = tuple(f"BSC-EM-{index:02d}" for index in range(1, 12))
AUTHORITATIVE_SURFACES = (
    "framework/Electromagnetic_Evidence_Bridge.md",
    "paper/source/On_Boundaries_of_Evidence.tex",
    "ledgers/Claim_Status_Ledger.md",
)
SYNOPSIS_SURFACES = (
    "synopsis/Technical_Synopsis.md",
    "synopsis/source/Technical_Synopsis.tex",
    "synopsis/Reader_Map.md",
)


def compact_math(value: str) -> str:
    value = value.replace(r"\mathrm{tr}", r"\rm tr")
    value = re.sub(r"\\[,!;:]", "", value)
    return re.sub(r"[\s&]+", "", value)


def plain_prose(value: str) -> str:
    value = value.replace(r"\alpha", "alpha")
    value = re.sub(r"[\$\\{}_*`()\[\]]+", " ", value)
    return " ".join(value.lower().split())


class ElectromagneticEvidenceBridgeTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")

    def assert_math_fragments(
        self,
        relative: str,
        fragments: tuple[str, ...],
    ) -> None:
        text = compact_math(self.read(relative))
        for fragment in fragments:
            with self.subTest(path=relative, fragment=fragment):
                self.assertIn(compact_math(fragment), text)

    def test_claim_roster_is_synchronized_across_authoritative_surfaces(
        self,
    ) -> None:
        for relative in AUTHORITATIVE_SURFACES:
            text = self.read(relative)
            for identifier in EM_CLAIMS:
                with self.subTest(path=relative, identifier=identifier):
                    self.assertIn(identifier, text)

        ledger = self.read("ledgers/Claim_Status_Ledger.md")
        for identifier in EM_CLAIMS:
            with self.subTest(path="claim ledger", identifier=identifier):
                self.assertEqual(ledger.count(f"| {identifier} |"), 1)

    def test_synopsis_routes_the_bridge_and_full_claim_range(self) -> None:
        for relative in SYNOPSIS_SURFACES:
            text = self.read(relative)
            with self.subTest(path=relative):
                self.assertIn("Electromagnetic_Evidence_Bridge.md", text)
                self.assertIn("BSC-EM-01", text)
                self.assertIn("BSC-EM-11", text)

    def test_gauge_source_energy_and_port_equations_are_retained(self) -> None:
        self.assert_math_fragments(
            "framework/Electromagnetic_Evidence_Bridge.md",
            (
                r"d\mathcal F=0",
                r"d\mathcal H=\mathcal J",
                r"R(A^u)=R(A)",
                r"\partial_tu+\nabla\mathbin{\cdot}S=-J\mathbin{\cdot}E",
                r"S(\omega)^\dagger S(\omega)\preceq I",
                r"I-S_{oo}^\dagger S_{oo}=S_{ho}^\dagger S_{ho}",
                r"\alpha_i:=\frac{q_i^2}{4\pi Z}",
                r"\frac q{2\pi\hbar}\int_\Sigma F_{\mathrm{phys}}"
                r"\in\mathbb Z",
                r"\mu\frac{d\alpha}{d\mu}=\beta(\alpha)",
            ),
        )
        self.assert_math_fragments(
            "paper/source/On_Boundaries_of_Evidence.tex",
            (
                r"R=\overline R\circ\pi",
                r"d\mathcal F=0",
                r"d\mathcal G=\mathcal J",
                r"\partial_tu+\nabla\mathbin{\cdot}\mathbf S"
                r"=-\mathbf J\mathbin{\cdot}\mathbf E",
                r"S^\dagger S\preceq I",
                r"I-S_{oo}^\dagger S_{oo}=S_{ho}^\dagger S_{ho}",
                r"\alpha_i=\frac{q_i^2}{4\pi Z}",
                r"\frac{q_i}{2\pi\hbar}\int_\Sigma F_{\rm phys}"
                r"\in\mathbb Z",
            ),
        )

    def test_calibrated_passivity_has_three_dispositions(self) -> None:
        for relative in (
            "framework/Electromagnetic_Evidence_Bridge.md",
            "paper/source/On_Boundaries_of_Evidence.tex",
            "synopsis/Technical_Synopsis.md",
            "synopsis/source/Technical_Synopsis.tex",
        ):
            prose = self.read(relative).lower()
            with self.subTest(path=relative):
                self.assertRegex(prose, r"\bfalsif(?:y|ie[sd])\b")
                self.assertRegex(prose, r"\bcertif(?:y|ie[sd])\b")
                self.assertIn("inconclusive", prose)

        def disposition(
            measured_sigma: Fraction,
            epsilon: Fraction,
        ) -> str:
            if measured_sigma - epsilon > 1:
                return "falsified"
            if measured_sigma + epsilon <= 1:
                return "certified"
            return "inconclusive"

        self.assertEqual(
            disposition(Fraction(11, 10), Fraction(1, 20)),
            "falsified",
        )
        self.assertEqual(
            disposition(Fraction(9, 10), Fraction(1, 20)),
            "certified",
        )
        self.assertEqual(
            disposition(Fraction(1), Fraction(1, 20)),
            "inconclusive",
        )

    def test_pure_delay_has_equal_power_but_unidentified_phase(self) -> None:
        formula = r"S_\tau(\omega)=r e^{-i\omega\tau}"
        for relative in (
            "framework/Electromagnetic_Evidence_Bridge.md",
            "paper/source/On_Boundaries_of_Evidence.tex",
            "synopsis/Technical_Synopsis.md",
            "synopsis/source/Technical_Synopsis.tex",
        ):
            with self.subTest(path=relative):
                self.assertIn(
                    compact_math(formula),
                    compact_math(self.read(relative)),
                )

        radius = 0.8
        frequency = 2.0
        delay = 0.7
        no_delay = complex(radius)
        pure_delay = radius * cmath.exp(-1j * frequency * delay)
        self.assertTrue(
            math.isclose(abs(no_delay) ** 2, abs(pure_delay) ** 2)
        )
        self.assertFalse(
            math.isclose(no_delay.real, pure_delay.real)
            and math.isclose(no_delay.imag, pure_delay.imag)
        )

    def test_revised_si_relation_is_synchronized_and_consistent(self) -> None:
        shared_relation = r"\mu_0=\alpha\frac{2h}{ce^2}"
        for relative in (
            "framework/Electromagnetic_Evidence_Bridge.md",
            "synopsis/Technical_Synopsis.md",
            "synopsis/source/Technical_Synopsis.tex",
        ):
            with self.subTest(path=relative):
                self.assertIn(
                    compact_math(shared_relation),
                    compact_math(self.read(relative)),
                )

        self.assert_math_fragments(
            "paper/source/On_Boundaries_of_Evidence.tex",
            (
                r"\alpha(0)=\frac{e^2}{4\pi\varepsilon_0\hbar c}",
                r"\frac{\mu_0ce^2}{2h}=\frac{Z_0}{2R_{\rm K}}",
                r"\mu_0=\frac{2h\,\alpha(0)}{ce^2}",
            ),
        )
        ledger = compact_math(self.read("ledgers/Claim_Status_Ledger.md"))
        self.assertIn(
            compact_math(r"\mu_0=\alpha\mkern3mu 2h/(ce^2)"),
            ledger,
        )

        alpha = Fraction(7, 1000)
        planck = Fraction(6)
        light_speed = Fraction(5)
        charge = Fraction(2)
        permeability = alpha * 2 * planck / (light_speed * charge**2)
        self.assertEqual(
            permeability * light_speed * charge**2 / (2 * planck),
            alpha,
        )

    def test_rg_flow_transports_but_does_not_create_a_boundary_value(
        self,
    ) -> None:
        for relative in AUTHORITATIVE_SURFACES:
            text = self.read(relative).lower()
            with self.subTest(path=relative):
                self.assertIn("boundary value", text)
                self.assertIn("scheme", text)
                self.assertIn("threshold", text)
        framework = self.read("framework/Electromagnetic_Evidence_Bridge.md")
        normalized_framework = " ".join(framework.split())
        for fragment in (
            r"\alpha(\mu_0)=\alpha_0",
            "undetermined integration constant",
            "running transports and tests a supplied coupling value",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, normalized_framework)

    def test_field_normalization_invariant_is_exact(self) -> None:
        kinetic = Fraction(9)
        charges = (Fraction(6), Fraction(-3))
        scale = Fraction(3)
        transformed_kinetic = kinetic / scale**2
        transformed_charges = tuple(charge / scale for charge in charges)

        for charge, transformed in zip(
            charges,
            transformed_charges,
            strict=True,
        ):
            self.assertEqual(
                charge**2 / kinetic,
                transformed**2 / transformed_kinetic,
            )
        self.assertEqual(
            charges[0] / charges[1],
            transformed_charges[0] / transformed_charges[1],
        )

    def test_binary_and_constructibility_screen_is_exact(self) -> None:
        framework = self.read("framework/Electromagnetic_Evidence_Bridge.md")
        paper = self.read("paper/source/On_Boundaries_of_Evidence.tex")
        expected_orders = {
            "framework": r"\mathrm{ord}_{137}(2)=68",
            "paper": r"\operatorname{ord}_{137}(2)=68",
        }
        for surface, text in (("framework", framework), ("paper", paper)):
            with self.subTest(surface=surface):
                self.assertIn(
                    compact_math(expected_orders[surface]),
                    compact_math(text),
                )

        order = next(
            exponent
            for exponent in range(1, 137)
            if pow(2, exponent, 137) == 1
        )
        self.assertEqual(order, 68)
        self.assertEqual(pow(2, 34, 137), 136)
        self.assertEqual((2**31 - 1) % 137, 16)
        self.assertEqual((2**32 - 1) % 137, 33)
        self.assertEqual(65_537 % 137, 51)
        self.assertEqual(
            3 * 5 * 17 * 257 * 65_537,
            2**32 - 1,
        )

        degree_137 = (137 - 1) // 2
        degree_65537 = (65_537 - 1) // 2
        self.assertNotEqual(degree_137 & (degree_137 - 1), 0)
        self.assertEqual(degree_65537 & (degree_65537 - 1), 0)

    def test_aperiodic_materialization_descent_is_typed_and_exact(self) -> None:
        framework = self.read("framework/Electromagnetic_Evidence_Bridge.md")
        paper = self.read("paper/source/On_Boundaries_of_Evidence.tex")
        expected_stabilizers = {
            "framework": (
                r"\mathrm{Stab}_{\mathrm{tr}}(\kappa)"
                r"\subseteq"
                r"\mathrm{Stab}_{\mathrm{tr}}(P)"
            ),
            "paper": (
                r"\operatorname{Stab}_{\mathrm{tr}}(\kappa)"
                r"\subseteq"
                r"\operatorname{Stab}_{\mathrm{tr}}(P)"
            ),
        }
        for surface, text in (("framework", framework), ("paper", paper)):
            with self.subTest(surface=surface):
                prose = plain_prose(text)
                self.assertIn("eight kites", prose)
                self.assertIn("deltoidal-trihexagonal", prose)
                self.assertIn("translation-faithful", prose)
                self.assertIn(
                    "lattice-periodic coefficient fields materializing only "
                    "the unlabeled carrier",
                    prose,
                )
                self.assertIn(
                    "bragg peaks whose positions were insensitive to "
                    "illumination position",
                    prose,
                )
                self.assertIn(
                    "geometry-to-fabricated-sample-to-report",
                    text,
                )
                self.assertNotIn("position-independent bragg peaks", prose)
                self.assertNotIn("geometry-to-device", prose)
                self.assertIn("BSC-EM-11", text)
                self.assertIn("BSC-EM-OBS-01", text)
                self.assertIn(
                    compact_math(expected_stabilizers[surface]),
                    compact_math(text),
                )

        doi = "10.1038/s41467-026-75023-7"
        self.assertIn(doi, framework)
        self.assertIn(
            doi,
            self.read("paper/source/On_Boundaries_of_Evidence.bib"),
        )

        ledger = self.read("ledgers/Claim_Status_Ledger.md")
        theorem_row = next(
            line for line in ledger.splitlines()
            if line.startswith("| BSC-EM-11 |")
        )
        observation_row = next(
            line for line in ledger.splitlines()
            if line.startswith("| BSC-EM-OBS-01 |")
        )
        theorem_cells = [
            cell.strip() for cell in theorem_row.strip("|").split("|")
        ]
        observation_cells = [
            cell.strip() for cell in observation_row.strip("|").split("|")
        ]
        self.assertEqual(theorem_cells[4], "N/A")
        self.assertEqual(theorem_cells[6], "present proof")
        self.assertEqual(observation_cells[2], "N/A")
        self.assertEqual(observation_cells[3], "N/A")
        self.assertEqual(observation_cells[4], "single study")
        self.assertEqual(observation_cells[6], "verified publication")
        self.assertEqual(observation_cells[7], "local only")

        points = ((0, 0), (1, 0), (0, 1))

        def intensity(
            selected: tuple[tuple[int, int], ...],
            kx: Fraction,
            ky: Fraction,
        ) -> float:
            amplitude = sum(
                cmath.exp(2j * math.pi * float(kx * x + ky * y))
                for x, y in selected
            )
            return abs(amplitude) ** 2

        self.assertEqual(intensity((), Fraction(0), Fraction(0)), 0)
        self.assertEqual(
            intensity(points, Fraction(0), Fraction(0)),
            len(points) ** 2,
        )
        self.assertNotEqual(
            intensity((), Fraction(0), Fraction(0)),
            intensity(points, Fraction(0), Fraction(0)),
        )

        phi = (1 + math.sqrt(5)) / 2
        theta_degrees = math.degrees(math.acos((3 * phi - 1) / 4))
        self.assertAlmostEqual(theta_degrees, 15.52, places=2)

    def test_bsc_never_claims_to_derive_or_predict_alpha(self) -> None:
        unsafe = (
            re.compile(
                r"\b(?:bsc|we|this (?:paper|module|framework)|"
                r"the (?:paper|module|framework|theorem))\s+"
                r"(?:now\s+)?(?:derives?|predicts?)\s+"
                r"(?:the\s+)?(?:numerical\s+)?(?:value\s+of\s+)?"
                r"(?:alpha|the fine-structure constant|1\s*/\s*137|"
                r"137\.035)"
            ),
            re.compile(
                r"\b(?:alpha|fine-structure constant|1\s*/\s*137|"
                r"137\.035).{0,80}\b(?:is|was|has been)\s+"
                r"(?:derived|predicted)\s+by\s+"
                r"(?:bsc|this (?:paper|module|framework))\b"
            ),
        )
        bad_examples = (
            "BSC derives the fine-structure constant.",
            "This paper predicts the numerical value of alpha.",
            "Alpha has been derived by this framework.",
        )
        for example in bad_examples:
            with self.subTest(guard_example=example):
                self.assertTrue(
                    any(pattern.search(example.lower()) for pattern in unsafe)
                )

        for relative in AUTHORITATIVE_SURFACES + SYNOPSIS_SURFACES:
            prose = plain_prose(self.read(relative))
            for pattern in unsafe:
                with self.subTest(path=relative, pattern=pattern.pattern):
                    self.assertIsNone(pattern.search(prose))

        self.assertIn(
            "does **not** derive the fine-structure constant",
            self.read("framework/Electromagnetic_Evidence_Bridge.md"),
        )
        paper = " ".join(
            self.read("paper/source/On_Boundaries_of_Evidence.tex").split()
        )
        self.assertIn(r"does not derive a value of \(\alpha\)", paper)
        self.assertIn(
            "No theorem in BSC derives or predicts",
            self.read("synopsis/Technical_Synopsis.md"),
        )
        self.assertIn(
            "No BSC theorem derives or predicts",
            self.read("synopsis/source/Technical_Synopsis.tex"),
        )


if __name__ == "__main__":
    unittest.main()
