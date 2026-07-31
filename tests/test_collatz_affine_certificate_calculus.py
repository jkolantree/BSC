from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "applications" / "Collatz_Affine_Certificate_Calculus.md"


class CollatzAffineCertificateCalculusTests(unittest.TestCase):
    @staticmethod
    def shortcut(n: int) -> int:
        return (3 * n + 1) // 2 if n & 1 else n // 2

    @classmethod
    def iterate(cls, n: int, steps: int) -> int:
        for _ in range(steps):
            n = cls.shortcut(n)
        return n

    @staticmethod
    def orbit(mapping: dict[int, int], start: int) -> set[int]:
        seen: set[int] = set()
        while start not in seen:
            seen.add(start)
            start = mapping[start]
        return seen

    def test_module_is_publicly_routed_and_claim_local(self) -> None:
        module = MODULE.read_text(encoding="utf-8")
        for claim_id in (
            "BSC-CRS-08",
            "BSC-CRS-09",
            "BSC-CRS-10",
            "BSC-CRS-11",
            "BSC-CRS-12",
        ):
            with self.subTest(claim_id=claim_id):
                self.assertIn(claim_id, module)
        ledger = (ROOT / "ledgers" / "Claim_Status_Ledger.md").read_text(
            encoding="utf-8"
        )
        for claim_id in (
            "BSC-CRS-08",
            "BSC-CRS-09",
            "BSC-CRS-10",
            "BSC-CRS-11",
            "BSC-CRS-12",
            "BSC-CRS-13",
        ):
            with self.subTest(ledger_claim_id=claim_id):
                self.assertEqual(ledger.count(f"| {claim_id} |"), 1)

        controlled = {
            "verdict": {"ill-posed", "open", "true", "false", "N/A"},
            "math": {"none", "conjectural", "conditional", "proved", "N/A"},
            "empirical": {
                "contradicted",
                "untested",
                "single study",
                "replicated",
                "N/A",
            },
            "computational": {
                "failed",
                "unexecuted",
                "executed",
                "exact receipt",
                "N/A",
            },
            "source": {
                "unchecked",
                "internal",
                "present proof",
                "verified preprint",
                "verified publication",
            },
            "transfer": {"blocked", "local only", "bounded", "certified", "N/A"},
        }
        rows = {}
        for line in ledger.splitlines():
            if line.startswith("| BSC-CRS-"):
                cells = [
                    cell.strip()
                    for cell in line.strip().strip("|").split("|")
                ]
                rows[cells[0]] = cells
        for claim_id in (
            "BSC-CRS-08",
            "BSC-CRS-09",
            "BSC-CRS-10",
            "BSC-CRS-11",
            "BSC-CRS-12",
            "BSC-CRS-13",
        ):
            with self.subTest(controlled_vocabulary=claim_id):
                cells = rows[claim_id]
                self.assertEqual(len(cells), 9)
                self.assertIn(cells[2], controlled["verdict"])
                self.assertIn(cells[3], controlled["math"])
                self.assertIn(cells[4], controlled["empirical"])
                self.assertIn(cells[5], controlled["computational"])
                self.assertIn(cells[6], controlled["source"])
                self.assertIn(cells[7], controlled["transfer"])
        self.assertIn("does not prove the Collatz conjecture", module)
        self.assertIn("does not prove the remaining $242$", module)
        self.assertIn("does not promote the catalog claims", module)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("post-release presentation and application notes", readme)
        reader_map = (ROOT / "synopsis" / "Reader_Map.md").read_text(
            encoding="utf-8"
        )
        for surface in (readme, reader_map):
            self.assertIn("Collatz_Affine_Certificate_Calculus.md", surface)

    def test_merge_kernel_requires_rs_properness(self) -> None:
        mapping = {1: 2, 2: 1, 3: 4, 4: 3, 5: 4}
        values = set(mapping)
        orbits = {n: self.orbit(mapping, n) for n in values}
        merge_classes = []
        unseen = set(values)
        while unseen:
            seed = min(unseen)
            component = {
                n for n in values if orbits[seed] & orbits[n]
            }
            merge_classes.append(component)
            unseen -= component
        kernel = {min(component) for component in merge_classes}
        self.assertEqual(kernel, {1, 3})

        recursive = {
            n
            for n in values
            if any(m < n and orbits[m] & orbits[n] for m in values)
        }
        self.assertEqual(recursive, {2, 4, 5})

        kernel_star = kernel - {1}
        proper_candidate = {3}
        whole_space = values
        self.assertTrue(kernel_star <= proper_candidate)
        self.assertNotEqual(proper_candidate, values)
        self.assertTrue(
            all(
                n == 1 or n in recursive
                for n in values - proper_candidate
            )
        )
        self.assertTrue(kernel_star <= whole_space)
        self.assertEqual(whole_space, values)

    def test_affine_descent_and_slope_nonconverses(self) -> None:
        for t in (0, 1, 2, 17, 1_000_000):
            start = 8 * t + 5
            meeting = self.iterate(start, 3)
            self.assertEqual(meeting, 3 * t + 2)
            endpoint = 8 * t + 4
            self.assertEqual(self.iterate(endpoint, 3), meeting)
            self.assertLess(endpoint, start)

            slope_only_start = 256 * t + 7
            self.assertEqual(
                self.iterate(slope_only_start, 7), 162 * t + 5
            )
            self.assertEqual(
                self.iterate(slope_only_start, 8), 243 * t + 8
            )
        self.assertGreater(8, 7)

        for a, b, a_prime, b_prime in (
            (8, 5, 8, 4),
            (8748, 6219, 8192, 5823),
            (10, 9, 9, 8),
        ):
            self.assertLessEqual(a_prime, a)
            self.assertLess(b_prime, b)
            for t in range(100):
                self.assertLess(a_prime * t + b_prime, a * t + b)

    def test_strict_depth_boundary_and_two_adic_gate(self) -> None:
        def strict_slope_feasible(
            e: int, b: int, v3_a: int, h: int
        ) -> bool:
            return (
                Fraction(2**e, 2**b)
                * Fraction(3, 2) ** (v3_a + h)
                > 1
            )

        self.assertFalse(strict_slope_feasible(0, 0, 0, 0))
        self.assertTrue(strict_slope_feasible(0, 0, 0, 1))

        def least_h(e: int, b: int, v3_a: int) -> int:
            return next(
                h
                for h in range(100)
                if strict_slope_feasible(e, b, v3_a, h)
            )

        self.assertEqual(least_h(0, 0, 0), 1)
        self.assertEqual(
            [least_h(0, b, 2) for b in range(12)],
            [0, 0, 2, 4, 5, 7, 9, 10, 12, 14, 16, 17],
        )

        a, e, b, r = 1, 1, 0, 0
        a_prime = Fraction(a) * Fraction(2) ** (b - e + r)
        self.assertEqual(a_prime, Fraction(1, 2))
        self.assertGreater(e - b, 0)

        equal_a, equal_e, equal_b, equal_r = 8, 2, 2, 0
        equal_a_prime = (
            Fraction(equal_a)
            * Fraction(2) ** (equal_b - equal_e + equal_r)
        )
        self.assertEqual(equal_a_prime, equal_a)
        self.assertEqual(equal_e - equal_b, 0)
        self.assertLess(8 * 0 + 4, 8 * 0 + 5)

        for s in range(5):
            for e in range(5):
                for c in range(5):
                    for b in range(5):
                        net_slope = (
                            Fraction(2) ** (b - e)
                            * Fraction(2, 3) ** (c - s)
                        )
                        self.assertEqual(
                            net_slope == 1,
                            c == s and b == e,
                        )

    def test_typed_slope_bounds_are_exact(self) -> None:
        self.assertGreater(3**665, 2**1054)
        self.assertLess(3**306, 2**485)
        self.assertEqual(306 * 389 - 179 * 665, -1)

        for s, e in ((0, 1), (1, 1), (10, 6), (179, 105)):
            if 179 * s <= 306 * e:
                forward_slope = Fraction(3**s, 2 ** (s + e))
                self.assertLess(forward_slope, 1)

    def test_ghost_cylinders_force_odd_prefixes_and_expand(self) -> None:
        for depth in range(41):
            modulus = 1 << depth
            ghost_residue = (
                0
                if depth == 0
                else (-7 * pow(9, -1, modulus)) % modulus
            )
            odd_steps = depth + 2
            constant_quotient, remainder = divmod(
                36 * ghost_residue + 28,
                1 << odd_steps,
            )
            self.assertEqual(remainder, 0)
            for t in range(6):
                start = 36 * (ghost_residue + modulus * t) + 27
                n = start
                for _ in range(odd_steps):
                    self.assertEqual(n % 2, 1)
                    n = self.shortcut(n)
                self.assertEqual(
                    n,
                    3**odd_steps * (constant_quotient + 9 * t) - 1,
                )
            next_parities = {
                self.iterate(
                    36 * (ghost_residue + modulus * t) + 27,
                    odd_steps,
                )
                % 2
                for t in (0, 1)
            }
            self.assertEqual(next_parities, {0, 1})

        lower_bound = Fraction(16, 9)
        for b in range(2, 9):
            for r in range(-10, 3):
                slope = Fraction(2**b) * Fraction(2, 3) ** r
                self.assertGreaterEqual(slope, lower_bound)

    def test_exact_8748_progression_witness(self) -> None:
        pair = (8748, 6219)

        def forward_odd(current: tuple[int, int]) -> tuple[int, int]:
            a, b = current
            self.assertEqual(a % 2, 0)
            self.assertEqual(b % 2, 1)
            return 3 * a // 2, (3 * b + 1) // 2

        def reverse_even(current: tuple[int, int]) -> tuple[int, int]:
            a, b = current
            return 2 * a, 2 * b

        def reverse_odd(current: tuple[int, int]) -> tuple[int, int]:
            a, b = current
            self.assertEqual(a % 3, 0)
            self.assertEqual(b % 3, 2)
            predecessor = 2 * a // 3, (2 * b - 1) // 3
            self.assertEqual(predecessor[1] % 2, 1)
            self.assertGreater(predecessor[0], 0)
            self.assertGreater(predecessor[1], 0)
            return predecessor

        meeting = forward_odd(pair)
        self.assertEqual(meeting, (13122, 9329))
        current = meeting
        observed: list[tuple[int, int]] = []
        for letter in "001010111111":
            current = (
                reverse_even(current)
                if letter == "0"
                else reverse_odd(current)
            )
            observed.append(current)

        self.assertEqual(
            observed,
            [
                (26244, 18658),
                (52488, 37316),
                (34992, 24877),
                (69984, 49754),
                (46656, 33169),
                (93312, 66338),
                (62208, 44225),
                (41472, 29483),
                (27648, 19655),
                (18432, 13103),
                (12288, 8735),
                (8192, 5823),
            ],
        )
        self.assertEqual(current, (8192, 5823))

        for t in (0, 1, 2, 17, 1_000_000):
            n = 8748 * t + 6219
            m = 8192 * t + 5823
            self.assertEqual(n - m, 556 * t + 396)
            self.assertGreater(n - m, 0)
            self.assertEqual(self.iterate(m, 12), self.shortcut(n))
            self.assertEqual(2187 * m, 2048 * n - 1611)

    def test_catalog_aggregates_are_not_promoted(self) -> None:
        module = MODULE.read_text(encoding="utf-8")
        ledger = (ROOT / "ledgers" / "Claim_Status_Ledger.md").read_text(
            encoding="utf-8"
        )
        combined = module + ledger
        self.assertNotIn("152,747", combined)
        self.assertNotIn("1,966,261", combined)
        self.assertIn("does not promote the catalog claims", module)
        self.assertIn("complete generated catalogs", module)


if __name__ == "__main__":
    unittest.main()
