from __future__ import annotations

import csv
import hashlib
import json
import math
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "applications" / "ASTRA_Dual_Rent_Crosswalk.md"

SOURCE_HASHES = {
    "ASTRA_Dual_Rent_Local_to_Global_Audit_Form_v0.3.0.pdf": (
        "62ee91f1d855fba12781e44aed8a5958b159508459bce53e5dc9eaefe48936ef"
    ),
    "ASTRA_v0.3.0_Public_Ground_Reading.pdf": (
        "cc722b73741049440caaf307d0fbeee7b543755c53f8114a114b7adcef0e7c28"
    ),
    "ASTRA_v0.3.0_Verification_Report.pdf": (
        "a7c0f9b9b979ec6bc5aeb685aa3165a5d1c89a60f712573a5a1871cf2831b35e"
    ),
    "ASTRA_Framework_v0.3.0_Dual_Rent_Arithmetic_Seams.zip": (
        "2f8c26c92826c0464ae88048d9c3e68a4404ee5d9b8f46a660a0733ccddd75ab"
    ),
    "ASTRA_Framework_v0.3.0_Dual_Rent_Arithmetic_Seams.zip.sha256": (
        "9a6cd6158024df295000da160af73451676313602700e9aac9749a0adb13d9a4"
    ),
    "ASTRA_Framework_v0.3.0_Dual_Rent_Arithmetic_Seams.zip.verify.txt": (
        "14d9452b3f092a8497e61cafa4ce24fedbf4afdd41e59692150babafa8979594"
    ),
}


def mutual_information(
    joint: dict[tuple[int, int], Fraction],
) -> float:
    marginal_k: dict[int, Fraction] = {}
    marginal_y: dict[int, Fraction] = {}
    for (candidate, report), probability in joint.items():
        marginal_k[candidate] = marginal_k.get(candidate, Fraction(0)) + probability
        marginal_y[report] = marginal_y.get(report, Fraction(0)) + probability
    total = 0.0
    for (candidate, report), probability in joint.items():
        if not probability:
            continue
        ratio = probability / (
            marginal_k[candidate] * marginal_y[report]
        )
        total += float(probability) * math.log2(float(ratio))
    return total


def total_variation(
    first: dict[int, Fraction], second: dict[int, Fraction]
) -> Fraction:
    support = set(first) | set(second)
    return sum(
        (abs(first.get(x, Fraction(0)) - second.get(x, Fraction(0)))
         for x in support),
        Fraction(0),
    ) / 2


def verify_digest(payload: bytes, expected: str) -> None:
    actual = hashlib.sha256(payload).hexdigest()
    if actual != expected:
        raise ValueError(f"source digest mismatch: {actual}")


def require_comparable(
    reference: dict[str, object], seam: dict[str, object]
) -> None:
    for field in (
        "candidates",
        "prior",
        "physical_space",
        "report_space",
        "horizon",
    ):
        if reference[field] != seam[field]:
            raise ValueError(f"dual-rent comparison changed {field}")


def require_complete_postselection(
    success_probability: Fraction,
    has_failure_outcome: bool,
) -> None:
    if success_probability <= 0:
        raise ValueError("success probability must be positive")
    if not has_failure_outcome:
        raise ValueError("complete instrument must retain failure")


def apply_binary_report_kernel(
    joint: dict[tuple[int, int], Fraction],
    probability_one: tuple[Fraction, Fraction],
) -> dict[tuple[int, int], Fraction]:
    transformed: dict[tuple[int, int], Fraction] = {}
    for (candidate, report), probability in joint.items():
        for output in (0, 1):
            conditional = (
                probability_one[report]
                if output == 1
                else 1 - probability_one[report]
            )
            key = (candidate, output)
            transformed[key] = transformed.get(key, Fraction(0)) + (
                probability * conditional
            )
    return transformed


def solve_rational(
    matrix: list[list[Fraction]], vector: list[Fraction]
) -> list[Fraction]:
    size = len(vector)
    rows = [matrix[i][:] + [vector[i]] for i in range(size)]
    for column in range(size):
        pivot = next(
            row for row in range(column, size) if rows[row][column]
        )
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [entry / scale for entry in rows[column]]
        for row in range(size):
            if row == column:
                continue
            factor = rows[row][column]
            rows[row] = [
                rows[row][index] - factor * rows[column][index]
                for index in range(size + 1)
            ]
    return [rows[row][-1] for row in range(size)]


class AstraDualRentCrosswalkTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_source_identities_are_bound_on_all_surfaces(self) -> None:
        note = NOTE.read_text(encoding="utf-8")
        with (ROOT / "provenance" / "Supplied_Source_Manifest.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        manifest_rows = {row["basename"]: row for row in rows}
        sidecar = self.read("provenance/Supplied_Source_SHA256.txt")
        availability = self.read("SOURCE_AVAILABILITY.md")

        for basename, digest in SOURCE_HASHES.items():
            with self.subTest(source=basename):
                self.assertEqual(manifest_rows[basename]["sha256"], digest)
                self.assertIn(digest, note)
                self.assertEqual(sidecar.count(digest), 1)
                self.assertEqual(
                    manifest_rows[basename]["redistribution_status"],
                    "not exercised",
                )
        self.assertIn("six nonredistributed ASTRA v0.3 audit", availability)
        self.assertIn("not part of the twelve-document internal BSC corpus", availability)

    def test_digest_gate_rejects_one_byte_mutation(self) -> None:
        payload = bytearray(b"frozen ASTRA source identity")
        expected = hashlib.sha256(payload).hexdigest()
        verify_digest(bytes(payload), expected)
        payload[7] ^= 1
        with self.assertRaisesRegex(ValueError, "source digest mismatch"):
            verify_digest(bytes(payload), expected)

    def test_duplicate_aliases_are_not_independent_evidence(self) -> None:
        note = " ".join(NOTE.read_text(encoding="utf-8").lower().split())
        self.assertIn("byte-identical aliases", note)
        self.assertIn("not counted as independent evidence", note)
        self.assertIn("share one source root", note)

    def test_exact_dual_rent_countermodels(self) -> None:
        half = Fraction(1, 2)

        physical_reference = {
            0: {0: Fraction(1)},
            1: {1: Fraction(1)},
        }
        physical_seam = physical_reference
        dynamical = sum(
            half * total_variation(
                physical_seam[candidate], physical_reference[candidate]
            )
            for candidate in (0, 1)
        )
        report_reference = {(0, 0): half, (1, 0): half}
        report_seam = {(0, 0): half, (1, 1): half}
        self.assertEqual(dynamical, 0)
        self.assertEqual(mutual_information(report_reference), 0.0)
        self.assertEqual(mutual_information(report_seam), 1.0)

        physical_reference = {
            0: {0: Fraction(1)},
            1: {0: Fraction(1)},
        }
        physical_seam = {
            0: {1: Fraction(1)},
            1: {1: Fraction(1)},
        }
        dynamical = sum(
            half * total_variation(
                physical_seam[candidate], physical_reference[candidate]
            )
            for candidate in (0, 1)
        )
        self.assertEqual(dynamical, 1)
        self.assertEqual(mutual_information(report_reference), 0.0)

    def test_common_binary_report_channels_never_increase_information(self) -> None:
        noisy = {
            (0, 0): Fraction(3, 8),
            (0, 1): Fraction(1, 8),
            (1, 0): Fraction(1, 8),
            (1, 1): Fraction(3, 8),
        }
        source_information = mutual_information(noisy)
        self.assertGreater(source_information, 0)
        self.assertLess(source_information, 1)
        probabilities = (Fraction(0), Fraction(1, 2), Fraction(1))
        strict_reductions = 0
        for p_one_given_zero in probabilities:
            for p_one_given_one in probabilities:
                with self.subTest(
                    p_one_given_zero=p_one_given_zero,
                    p_one_given_one=p_one_given_one,
                ):
                    transformed = apply_binary_report_kernel(
                        noisy,
                        (p_one_given_zero, p_one_given_one),
                    )
                    result = mutual_information(transformed)
                    self.assertLessEqual(result, source_information + 1e-12)
                    if result < source_information - 1e-12:
                        strict_reductions += 1
        self.assertGreater(strict_reductions, 0)

    def test_changed_comparison_identity_is_rejected(self) -> None:
        reference: dict[str, object] = {
            "candidates": ("chain", "triangle"),
            "prior": (Fraction(1, 2), Fraction(1, 2)),
            "physical_space": "three temperatures",
            "report_space": "surface trace",
            "horizon": Fraction(10),
        }
        require_comparable(reference, reference.copy())
        mutations: dict[str, object] = {
            "candidates": ("chain", "star"),
            "prior": (Fraction(1, 3), Fraction(2, 3)),
            "physical_space": "four temperatures",
            "report_space": "surface spectrum",
            "horizon": Fraction(11),
        }
        for field, replacement in mutations.items():
            seam = reference.copy()
            seam[field] = replacement
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    require_comparable(reference, seam)

    def test_postselection_requires_probability_and_failure_outcome(self) -> None:
        require_complete_postselection(Fraction(1, 4), True)
        with self.assertRaisesRegex(ValueError, "positive"):
            require_complete_postselection(Fraction(0), True)
        with self.assertRaisesRegex(ValueError, "retain failure"):
            require_complete_postselection(Fraction(1, 4), False)

    def test_two_distinct_reservoirs_have_the_same_static_surface(self) -> None:
        chain = [
            [Fraction(1), Fraction(-1), Fraction(0)],
            [Fraction(-1), Fraction(2), Fraction(-1)],
            [Fraction(0), Fraction(-1), Fraction(1)],
        ]
        triangle = [
            [Fraction(2), Fraction(-1), Fraction(-1)],
            [Fraction(-1), Fraction(2), Fraction(-1)],
            [Fraction(-1), Fraction(-1), Fraction(2)],
        ]
        source = [Fraction(1), Fraction(2), Fraction(3)]
        sink = Fraction(2)
        expected_surface = sum(source, Fraction(0)) / sink
        interiors = []
        for laplacian in (chain, triangle):
            operator = [row[:] for row in laplacian]
            operator[0][0] += sink
            equilibrium = solve_rational(operator, source)
            self.assertEqual(equilibrium[0], expected_surface)
            interiors.append(equilibrium[1:])
        self.assertNotEqual(interiors[0], interiors[1])

    def test_defects_and_nonpromotions_are_fail_closed(self) -> None:
        note = NOTE.read_text(encoding="utf-8")
        normalized = " ".join(note.lower().split())
        required = (
            "not independent or fail-closed verification",
            "not_admitted",
            "source asserted",
            "same-package tests or a retained log promoted to independent verification",
            "passive common processing presented as positive information gain",
            "postselection without the complete instrument and success probability",
            "finite or numerical agreement promoted to a universal proof",
            "the higher-dimensional result does not settle dimension two",
            "allocates no new bsc claim or fixture identifier",
            "not blind in evaluation-integrity terms",
            "boxcar-averages the signal",
            "clips negative estimates to zero",
            "illustrative rather than complete",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, normalized)

        contradictory_values = (
            "(16.0319, 0.271916)",
            "(20.1111, 0.201304)",
            "(42.340425531914896, 0.16627084041143314)",
            "(20.079787234042556, 0.1975524418167117)",
        )
        for value in contradictory_values:
            self.assertIn(value, note)

        self.assertNotIn("BSC-SEAM-", note)
        self.assertNotIn("BSC-ASTRA-", note)
        self.assertNotIn("BSC-FIX-13", note)
        self.assertNotIn("F14", note)
        self.assertNotIn("ASTRA", self.read("ROADMAP.md"))

        release_spec = json.loads(self.read("release/release-spec.json"))
        self.assertIsNone(release_spec["intended_version"])
        self.assertIsNone(release_spec["build_epoch"])


if __name__ == "__main__":
    unittest.main()
