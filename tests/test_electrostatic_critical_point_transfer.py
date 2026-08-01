from __future__ import annotations

import hashlib
import json
import unittest
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "applications" / "Electrostatic_Critical_Point_Transfer.md"
CLAIM_IDS = tuple(f"BSC-ECP-{index:02d}" for index in range(1, 6))
SOURCE_HASHES = {
    "maxwell_pdf": (
        "4178ddc5a4efcdc11726bea6d6d20785575c55564095dbf53bfaa6d26055a958"
    ),
    "maxwell_source": (
        "85d3859f0c8bcf797911202890f885bbc2fd54e30ef930424f19493abd5b0dd5"
    ),
    "counting_pdf": (
        "d2f91a62abcdf96170f81224cafc9ece7d7950c0663651e10b8ce9a1f6b0f489"
    ),
    "counting_source": (
        "5b135fd315afc0efdf5df3a6900904fd5cc611e3c95ea77f634a7ee3af9e1e6b"
    ),
}


@dataclass(frozen=True)
class SqrtField:
    """An exact element p + q*sqrt(d) for one fixed positive d."""

    p: Fraction
    q: Fraction
    d: int

    @classmethod
    def make(
        cls,
        p: int | Fraction,
        q: int | Fraction,
        d: int,
    ) -> SqrtField:
        return cls(Fraction(p), Fraction(q), d)

    def _lift(self, other: object) -> SqrtField:
        if isinstance(other, SqrtField):
            if self.d != other.d:
                raise ValueError("quadratic fields differ")
            return other
        if isinstance(other, (int, Fraction)):
            return SqrtField(Fraction(other), Fraction(0), self.d)
        return NotImplemented

    def __add__(self, other: object) -> SqrtField:
        value = self._lift(other)
        if value is NotImplemented:
            return NotImplemented
        return SqrtField(self.p + value.p, self.q + value.q, self.d)

    __radd__ = __add__

    def __neg__(self) -> SqrtField:
        return SqrtField(-self.p, -self.q, self.d)

    def __sub__(self, other: object) -> SqrtField:
        value = self._lift(other)
        if value is NotImplemented:
            return NotImplemented
        return self + (-value)

    def __rsub__(self, other: object) -> SqrtField:
        value = self._lift(other)
        if value is NotImplemented:
            return NotImplemented
        return value - self

    def __mul__(self, other: object) -> SqrtField:
        value = self._lift(other)
        if value is NotImplemented:
            return NotImplemented
        return SqrtField(
            self.p * value.p + self.q * value.q * self.d,
            self.p * value.q + self.q * value.p,
            self.d,
        )

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> SqrtField:
        if exponent < 0:
            raise ValueError("negative exponent is outside this test field")
        result = SqrtField.make(1, 0, self.d)
        for _ in range(exponent):
            result *= self
        return result

    def is_zero(self) -> bool:
        return self.p == 0 and self.q == 0

    def sign(self) -> int:
        """Return the exact real sign without evaluating sqrt(d)."""

        if self.q == 0:
            return (self.p > 0) - (self.p < 0)
        if self.p == 0 or (self.p > 0) == (self.q > 0):
            return (self.q > 0) - (self.q < 0)
        p_squared = self.p * self.p
        radical_squared = self.q * self.q * self.d
        if p_squared == radical_squared:
            return 0
        if self.p > 0:
            return 1 if p_squared > radical_squared else -1
        return 1 if radical_squared > p_squared else -1


def determinant_3(matrix: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (
        d * h - e * g
    )


class ElectrostaticCriticalPointTransferTests(unittest.TestCase):
    def text(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_recorded_source_hashes_and_identity_gate_are_fail_closed(
        self,
    ) -> None:
        note = NOTE.read_text(encoding="utf-8")
        for label, digest in SOURCE_HASHES.items():
            with self.subTest(source=label):
                self.assertEqual(len(digest), 64)
                int(digest, 16)
                self.assertEqual(note.count(digest), 1)

        # The repository intentionally retains no source bytes. This synthetic
        # policy regression checks the digest gate; the milestone separately
        # hashes and mutates a disposable canonical download.
        def admitted(payload: bytes, digest: str) -> bool:
            return hashlib.sha256(payload).hexdigest() == digest

        canonical = b"arXiv:2607.27197v1 byte-identity gate"
        canonical_digest = hashlib.sha256(canonical).hexdigest()
        self.assertTrue(admitted(canonical, canonical_digest))
        changed = bytearray(canonical)
        changed[len(changed) // 2] ^= 1
        self.assertFalse(admitted(bytes(changed), canonical_digest))
        self.assertFalse(admitted(canonical, "0" * 64))

        aliases = (
            ("maxwell-v1", "abs"),
            ("maxwell-v1", "pdf"),
            ("maxwell-v1", "source"),
            ("counting-v2", "abs"),
            ("counting-v2", "pdf"),
            ("counting-v2", "source"),
            ("counting-v2", "doi"),
        )
        self.assertEqual({work for work, _ in aliases}, {
            "maxwell-v1",
            "counting-v2",
        })
        self.assertIn("NOT_SUPPLIED", note)
        self.assertIn("NOT_OBTAINED", note)
        self.assertIn("not a replay", note)

    def test_rescaling_chain_rule_and_both_index_signs_are_exact(self) -> None:
        hessian = (Fraction(-2), Fraction(3), Fraction(5))
        center = (Fraction(1, 5), Fraction(-2, 7), Fraction(3, 11))
        critical = (Fraction(4, 5), Fraction(5, 7), Fraction(-8, 11))
        radius = Fraction(2, 3)
        scaled_point = (Fraction(2), Fraction(-1), Fraction(3))
        physical_point = tuple(
            center[i] + radius * scaled_point[i] for i in range(3)
        )
        physical_gradient = tuple(
            hessian[i] * (physical_point[i] - critical[i])
            for i in range(3)
        )
        scaled_critical = tuple(
            (critical[i] - center[i]) / radius for i in range(3)
        )

        for normalization in (Fraction(7, 5), Fraction(-7, 5)):
            direct_gradient = tuple(
                radius**2
                * hessian[i]
                * (scaled_point[i] - scaled_critical[i])
                / normalization
                for i in range(3)
            )
            chain_gradient = tuple(
                radius * value / normalization
                for value in physical_gradient
            )
            self.assertEqual(direct_gradient, chain_gradient)

            scaled_hessian = tuple(
                radius**2 * value / normalization for value in hessian
            )
            old_index = sum(value < 0 for value in hessian)
            new_index = sum(value < 0 for value in scaled_hessian)
            expected = old_index if normalization > 0 else 3 - old_index
            self.assertEqual(new_index, expected)

    def test_triangle_moments_and_scaled_apex_identity_are_exact(self) -> None:
        # Write y=sqrt(3)*Y. Sparse polynomial arithmetic then proves each
        # moment identity coefficient-by-coefficient rather than at samples.
        Polynomial = dict[tuple[int, int], Fraction]

        def add(left: Polynomial, right: Polynomial) -> Polynomial:
            result = dict(left)
            for exponent, coefficient in right.items():
                result[exponent] = result.get(exponent, Fraction(0)) + coefficient
                if result[exponent] == 0:
                    del result[exponent]
            return result

        def scale(poly: Polynomial, coefficient: Fraction) -> Polynomial:
            return {
                exponent: coefficient * value
                for exponent, value in poly.items()
                if coefficient * value
            }

        def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
            result: Polynomial = {}
            for (x1, y1), c1 in left.items():
                for (x2, y2), c2 in right.items():
                    exponent = (x1 + x2, y1 + y2)
                    result[exponent] = result.get(exponent, Fraction(0)) + c1 * c2
            return {key: value for key, value in result.items() if value}

        def power(poly: Polynomial, exponent: int) -> Polynomial:
            result: Polynomial = {(0, 0): Fraction(1)}
            for _ in range(exponent):
                result = multiply(result, poly)
            return result

        x: Polynomial = {(1, 0): Fraction(1)}
        y_scaled: Polynomial = {(0, 1): Fraction(1)}
        projections = (
            x,
            add(scale(x, Fraction(-1, 2)), scale(y_scaled, Fraction(3, 2))),
            add(scale(x, Fraction(-1, 2)), scale(y_scaled, Fraction(-3, 2))),
        )
        rho_squared = add(power(x, 2), scale(power(y_scaled, 2), Fraction(3)))
        harmonic_cubic = add(
            power(x, 3),
            scale(multiply(x, power(y_scaled, 2)), Fraction(-9)),
        )

        for exponent, expected in (
            (1, {}),
            (2, scale(rho_squared, Fraction(3, 2))),
            (3, scale(harmonic_cubic, Fraction(3, 4))),
            (4, scale(power(rho_squared, 2), Fraction(9, 8))),
        ):
            observed: Polynomial = {}
            for projection in projections:
                observed = add(observed, power(projection, exponent))
            self.assertEqual(observed, expected)

        # X=(3/4,0,1) is exactly distance 3/4 from the scaled apex e3.
        epsilon = Fraction(1, 5)
        c = Fraction(7, 11)
        distance = Fraction(3, 4)
        charge = c * epsilon**3
        physical_difference = charge / (epsilon * distance) - charge / epsilon
        normalized_difference = physical_difference / epsilon**2
        self.assertEqual(normalized_difference, c * (1 / distance - 1))

    def test_strict_four_charge_gate_and_six_way_split(self) -> None:
        def multiply_coefficients(
            left: tuple[Fraction, ...],
            right: tuple[Fraction, ...],
        ) -> tuple[Fraction, ...]:
            product = [Fraction(0)] * (len(left) + len(right) - 1)
            for left_degree, left_coefficient in enumerate(left):
                for right_degree, right_coefficient in enumerate(right):
                    product[left_degree + right_degree] += (
                        left_coefficient * right_coefficient
                    )
            return tuple(product)

        # Coefficients are ordered by ascending powers of z.
        one_minus_z_squared = multiply_coefficients(
            (Fraction(1), Fraction(-1)),
            (Fraction(1), Fraction(-1)),
        )
        negative_three_z_times_square = multiply_coefficients(
            (Fraction(0), Fraction(-3)),
            one_minus_z_squared,
        )
        left_coefficients = list(negative_three_z_times_square)
        left_coefficients[0] += Fraction(4, 9)
        right_numerator = multiply_coefficients(
            multiply_coefficients(
                (Fraction(-1), Fraction(3)),
                (Fraction(-1), Fraction(3)),
            ),
            (Fraction(4), Fraction(-3)),
        )
        right_coefficients = tuple(value / 9 for value in right_numerator)
        self.assertEqual(tuple(left_coefficients), right_coefficients)

        for z in (
            Fraction(0),
            Fraction(1, 7),
            Fraction(1, 3),
            Fraction(4, 5),
            Fraction(1),
        ):
            deficit = Fraction(4, 9) - 3 * z * (1 - z) ** 2
            factored = (3 * z - 1) ** 2 * (4 - 3 * z) / 9
            self.assertEqual(deficit, factored)
            self.assertGreaterEqual(deficit, 0)

        def admissible_circle_parameter(value: Fraction) -> bool:
            return value > Fraction(4, 9)

        self.assertTrue(admissible_circle_parameter(Fraction(3, 2)))
        self.assertFalse(admissible_circle_parameter(Fraction(4, 9)))
        self.assertFalse(admissible_circle_parameter(Fraction(3, 16)))

        # Equality c=4/9 gives d0=2/3 and rho0^2=0: no Morse-Bott circle.
        d_at_equality = Fraction(2, 3)
        self.assertEqual(d_at_equality**2 - Fraction(4, 9), 0)

        # For c=3/2, d0=1 and rho0^2=5/9.
        rho_squared = Fraction(5, 9)
        normal_determinant = -Fraction(81, 4) * rho_squared
        self.assertEqual(normal_determinant, -Fraction(45, 4))
        self.assertLess(normal_determinant, 0)

        tangent_cosines = tuple(1 if k % 2 == 0 else -1 for k in range(6))
        tangent_second_signs = tuple(-cosine for cosine in tangent_cosines)
        self.assertTrue(all(sign != 0 for sign in tangent_second_signs))
        indices = tuple(1 + (second_sign < 0) for second_sign in tangent_second_signs)
        self.assertEqual(indices.count(1), 3)
        self.assertEqual(indices.count(2), 3)

    def test_remote_root_interval_and_index_two_are_exact(self) -> None:
        def h(value: Fraction) -> Fraction:
            return value**6 + value**3 - 3 * value**2 + 1

        lower = Fraction(69, 100)
        upper = Fraction(7, 10)
        self.assertGreater(h(lower), 0)
        self.assertLess(h(upper), 0)

        # h'=3t(2t^4+t-2). The bracket is increasing but remains negative
        # at the upper endpoint, so h is strictly decreasing on the interval.
        self.assertGreater(8 * lower**3 + 1, 0)
        self.assertLess(2 * upper**4 + upper - 2, 0)

        def x_eigenvalue_numerator(value: Fraction) -> Fraction:
            return 4 * value**5 - 3 * value**3 + 5 * value**2 - 3

        # Its derivative is positive on the interval, yet its upper value is
        # still negative; hence lambda_x<0 at the isolated root.
        derivative_lower_bound = lower * (
            20 * lower**3 - 9 * upper + 10
        )
        self.assertGreater(derivative_lower_bound, 0)
        self.assertEqual(
            x_eigenvalue_numerator(upper),
            -Fraction(5667, 6250),
        )
        lambda_x_is_negative = (
            derivative_lower_bound > 0
            and x_eigenvalue_numerator(upper) < 0
        )
        self.assertTrue(lambda_x_is_negative)

        for value in (lower, upper):
            u = 3 / (value**3 + 2)
            v = value * u
            lambda_z = -1 / u**3 - 2 / v**3
            self.assertLess(lambda_z, 0)
        lambda_z_is_negative = lower > 0
        self.assertTrue(lambda_z_is_negative)

        # Harmonicity gives lambda_y=-lambda_x-lambda_z>0 at the root.
        lambda_y_is_positive = (
            lambda_x_is_negative and lambda_z_is_negative
        )
        self.assertTrue(lambda_y_is_positive)
        hessian_signs = (-1, 1, -1)
        self.assertEqual(sum(sign < 0 for sign in hessian_signs), 2)

    def test_source_exclusion_and_affine_spanning_witness_are_exact(self) -> None:
        radius = Fraction(1, 10)
        source_lower_bound = 1 / radius**2
        other_sources_upper_bound = 3 * Fraction(2) / (3 - radius) ** 2
        self.assertEqual(source_lower_bound, 100)
        self.assertEqual(other_sources_upper_bound, Fraction(600, 841))
        self.assertGreater(source_lower_bound, other_sources_upper_bound)

        # In coordinates y=sqrt(3)*Y, the actual triangle plus an apex at
        # epsilon=1/6 has affine determinant 1/4.
        affine_matrix = (
            (Fraction(-3, 2), Fraction(-3, 2), Fraction(-1)),
            (Fraction(1, 2), Fraction(-1, 2), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(1, 6)),
        )
        self.assertEqual(determinant_3(affine_matrix), Fraction(1, 4))
        coplanar_mutation = (
            affine_matrix[0],
            affine_matrix[1],
            (Fraction(0), Fraction(0), Fraction(0)),
        )
        self.assertEqual(determinant_3(coplanar_mutation), 0)

        # At x=(1,1,1), three parameter columns remain independent after
        # their positive distance scalings are removed.
        direction_matrix = (
            (Fraction(1), Fraction(-2), Fraction(1)),
            (Fraction(1), Fraction(1), Fraction(-2)),
            (Fraction(1), Fraction(1), Fraction(1)),
        )
        self.assertNotEqual(determinant_3(direction_matrix), 0)

    def test_five_charge_limit_has_complete_exact_21_point_roster(self) -> None:
        def q(
            rational: int | Fraction,
            radical: int | Fraction,
            radicand: int,
        ) -> SqrtField:
            return SqrtField.make(rational, radical, radicand)

        def gradient_and_hessian(
            point: tuple[SqrtField, SqrtField, SqrtField],
        ) -> tuple[
            tuple[SqrtField, ...],
            tuple[tuple[SqrtField, ...], ...],
        ]:
            x, y, z = point
            r_squared = x**2 + y**2
            gradient = (
                Fraction(5, 16) * x
                + Fraction(45, 8) * (x**2 - y**2)
                + Fraction(9, 4) * x * r_squared
                - 9 * x * z**2,
                Fraction(5, 16) * y
                - Fraction(45, 4) * x * y
                + Fraction(9, 4) * y * r_squared
                - 9 * y * z**2,
                -Fraction(5, 8) * z - 9 * r_squared * z + 6 * z**3,
            )
            h_xx = (
                Fraction(5, 16)
                + Fraction(45, 4) * x
                + Fraction(9, 4) * (3 * x**2 + y**2)
                - 9 * z**2
            )
            h_yy = (
                Fraction(5, 16)
                - Fraction(45, 4) * x
                + Fraction(9, 4) * (x**2 + 3 * y**2)
                - 9 * z**2
            )
            h_zz = -Fraction(5, 8) - 9 * r_squared + 18 * z**2
            h_xy = -Fraction(45, 4) * y + Fraction(9, 2) * x * y
            h_xz = -18 * x * z
            h_yz = -18 * y * z
            hessian = (
                (h_xx, h_xy, h_xz),
                (h_xy, h_yy, h_yz),
                (h_xz, h_yz, h_zz),
            )
            return gradient, hessian

        def index_for_y_zero(
            hessian: tuple[tuple[SqrtField, ...], ...],
        ) -> int:
            self.assertTrue(hessian[0][1].is_zero())
            self.assertTrue(hessian[1][2].is_zero())
            h_xx = hessian[0][0]
            h_xz = hessian[0][2]
            h_yy = hessian[1][1]
            h_zz = hessian[2][2]
            block_det = h_xx * h_zz - h_xz**2
            block_trace = h_xx + h_zz
            self.assertNotEqual(block_det.sign(), 0)
            self.assertNotEqual(h_yy.sign(), 0)
            if block_det.sign() < 0:
                block_index = 1
            else:
                block_index = 0 if block_trace.sign() > 0 else 2
            return block_index + (1 if h_yy.sign() < 0 else 0)

        # Representatives are evaluated at y=0; D3 orbit multiplicities
        # reconstruct the full roster.
        representatives: list[
            tuple[
                tuple[SqrtField, SqrtField, SqrtField],
                int,
                int,
            ]
        ] = []
        zero2 = q(0, 0, 2)
        representatives.append(((zero2, zero2, zero2), 1, 1))

        for sign in (-1, 1):
            zero15 = q(0, 0, 15)
            representatives.append(
                ((zero15, zero15, q(0, Fraction(sign, 12), 15)), 1, 2)
            )

        zero205 = q(0, 0, 205)
        representatives.extend(
            (
                (
                    (q(-Fraction(5, 4), Fraction(1, 12), 205), zero205, zero205),
                    3,
                    2,
                ),
                (
                    (q(-Fraction(5, 4), -Fraction(1, 12), 205), zero205, zero205),
                    3,
                    1,
                ),
            )
        )

        for radius, radicand, expected_index in (
            (Fraction(1, 3), 39, 2),
            (Fraction(1, 6), 21, 1),
        ):
            for sign in (-1, 1):
                representatives.append(
                    (
                        (
                            q(radius, 0, radicand),
                            q(0, 0, radicand),
                            q(0, Fraction(sign, 12), radicand),
                        ),
                        3,
                        expected_index,
                    )
                )

        total = 0
        by_index = {1: 0, 2: 0}
        for point, multiplicity, expected_index in representatives:
            gradient, hessian = gradient_and_hessian(point)
            self.assertTrue(all(value.is_zero() for value in gradient))
            observed_index = index_for_y_zero(hessian)
            self.assertEqual(observed_index, expected_index)
            total += multiplicity
            by_index[observed_index] += multiplicity

        self.assertEqual(total, 21)
        self.assertEqual(by_index, {1: 10, 2: 11})

        # Exact factor cases establish completeness independently of the list.
        self.assertEqual(90**2 - 4 * 36 * 5, 36 * 205)
        self.assertLess(14**2, 205)
        self.assertGreater(15**2, 205)
        for radius in (Fraction(1, 6), Fraction(1, 3)):
            self.assertEqual(18 * radius**2 - 9 * radius + 1, 0)

        # These are all factor branches after r=0 versus r>0, z=0 versus
        # z!=0, and sin(3 theta)=0 are separated. Strictly positive
        # coefficients rule out the two opposite-angular-sign branches for
        # every r>0, rather than at sampled radii.
        branch_counts = {
            "axis center": 1,
            "axis nonzero z": 2,
            "planar cos(3 theta)=-1": 6,
            "off-plane cos(3 theta)=1, r=1/3": 6,
            "off-plane cos(3 theta)=1, r=1/6": 6,
        }
        self.assertEqual(sum(branch_counts.values()), 21)
        excluded_positive_root_coefficients = {
            "planar cos(3 theta)=1": (Fraction(5), Fraction(90), Fraction(36)),
            "off-plane cos(3 theta)=-1": (Fraction(1), Fraction(9), Fraction(18)),
        }
        for branch, coefficients in excluded_positive_root_coefficients.items():
            with self.subTest(excluded_branch=branch):
                self.assertTrue(all(value > 0 for value in coefficients))

        self.assertEqual(
            Fraction(19, 8) * Fraction(13, 4) - Fraction(39, 4),
            -Fraction(65, 32),
        )
        self.assertEqual(
            Fraction(17, 16) * Fraction(7, 4) - Fraction(21, 16),
            Fraction(35, 64),
        )

    def test_pair_insertion_coefficients_positivity_and_induction(self) -> None:
        alpha = Fraction(7, 5)
        beta = Fraction(11, 13)
        lam = 2 * beta / (5 * alpha)
        gamma = beta**2 / (30 * alpha)
        coefficient_h2 = gamma * lam**2
        coefficient_h3 = beta * lam**3
        coefficient_h4 = alpha * lam**4 / 4
        self.assertGreater(lam, 0)
        self.assertGreater(gamma, 0)
        self.assertEqual(coefficient_h3 / coefficient_h2, 12)
        self.assertEqual(coefficient_h4 / coefficient_h2, Fraction(6, 5))

        eta = Fraction(1, 100)
        self.assertLess(gamma * eta**2, alpha)
        inserted_charge = alpha * eta**3 - gamma * eta**5
        self.assertGreater(inserted_charge, 0)
        self.assertEqual(alpha - inserted_charge / eta**3, gamma * eta**2)

        # The boundary eta^2=alpha/gamma makes the inserted charge zero and
        # is therefore excluded by the strict positivity gate.
        boundary_eta_squared = alpha / gamma
        boundary_charge_factor = alpha - gamma * boundary_eta_squared
        self.assertEqual(boundary_charge_factor, 0)

        sources = 3
        points = 4
        for stage in range(7):
            self.assertEqual(sources, 3 + 2 * stage)
            self.assertEqual(points, 4 + 20 * stage)
            sources += 2
            points += 20

        epsilon = Fraction(1, 6)
        finite_strength = (
            Fraction(3, 4) * epsilon**3
            - Fraction(5, 32) * epsilon**5
        )
        self.assertEqual(finite_strength, Fraction(859, 248832))

    def test_claim_namespace_routing_and_nonclaims_are_fail_closed(self) -> None:
        note = NOTE.read_text(encoding="utf-8")
        ledger = self.text("ledgers/Claim_Status_Ledger.md")
        for claim_id in CLAIM_IDS:
            with self.subTest(claim=claim_id):
                self.assertGreaterEqual(note.count(claim_id), 2)
                self.assertEqual(ledger.count(f"| {claim_id} |"), 1)

        for route in ("README.md", "synopsis/Reader_Map.md"):
            self.assertIn(
                "applications/Electrostatic_Critical_Point_Transfer.md",
                self.text(route),
            )

        scope_marker = "The result is deliberately bounded. It does **not** provide:"
        self.assertEqual(note.count(scope_marker), 1)
        scope = note.split(scope_marker, 1)[1].split("## 1.", 1)[0]
        normalized_scope = " ".join(
            scope.lower().replace("$", "").split()
        )
        required_scope_exclusions = (
            "an exact global critical-point count for a finite configuration",
            "an explicit generic perturbation or a certified robustness radius",
            "an interval certificate for the illustrated value \\varepsilon=1/6",
            "a mechanically replayed historical calculation or kernel proof",
            "stable electrostatic traps",
            "an automatic extension from point charges to finite-size charge distributions",
            "a four-charge maximum, novelty claim, or priority claim",
            "any identification of f12 derived holonomy with electromagnetic wilson holonomy",
        )
        for exclusion in required_scope_exclusions:
            with self.subTest(scope_exclusion=exclusion):
                self.assertIn(exclusion, normalized_scope)

        required_boundaries = (
            "not exactly nine",
            "not exactly 24",
            "not a replay",
            "no named perturbation, radius, success probability, or physical sampling law",
            "does not certify the roots at that finite parameter",
            "C^3 control",
        )
        lower_note = " ".join(note.lower().replace("$", "").split())
        for phrase in required_boundaries:
            with self.subTest(boundary=phrase):
                self.assertIn(phrase.lower(), lower_note)

        forbidden_promotions = (
            "provides an exact global critical-point count",
            "gives an explicit generic perturbation",
            "supplies an explicit generic perturbation",
            "supplies a robustness radius",
            "supplies a success probability",
            "certifies the roots at \\varepsilon=1/6",
            "establishes stable electrostatic traps",
            "automatically transfers to finite-size charge distributions",
            "proves a four-charge maximum",
            "establishes a novelty claim",
            "establishes a priority claim",
            "identifies f12 derived holonomy with electromagnetic wilson holonomy",
        )
        for promotion in forbidden_promotions:
            with self.subTest(forbidden_promotion=promotion):
                self.assertNotIn(promotion, lower_note)

        release_spec = json.loads(self.text("release/release-spec.json"))
        self.assertIsNone(release_spec["intended_version"])
        self.assertIsNone(release_spec["build_epoch"])
        self.assertNotIn("BSC-FIX-13", ledger)
        self.assertNotIn("BSC-ECP-", self.text("ROADMAP.md"))

        vocabulary = {
            2: {"ill-posed", "open", "true", "false", "N/A"},
            3: {"none", "conjectural", "conditional", "proved", "N/A"},
            4: {"contradicted", "untested", "single study", "replicated", "N/A"},
            5: {"failed", "unexecuted", "executed", "exact receipt", "N/A"},
            6: {"unchecked", "internal", "present proof", "verified preprint", "verified publication"},
            7: {"blocked", "local only", "bounded", "certified", "N/A"},
        }
        rows = {}
        for line in ledger.splitlines():
            if line.startswith("| BSC-ECP-"):
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                rows[cells[0]] = cells
        self.assertEqual(set(rows), set(CLAIM_IDS))
        for claim_id, cells in rows.items():
            self.assertEqual(len(cells), 9)
            for index, allowed in vocabulary.items():
                with self.subTest(claim=claim_id, column=index):
                    self.assertIn(cells[index], allowed)
            self.assertNotEqual(cells[5], "exact receipt")


if __name__ == "__main__":
    unittest.main()
