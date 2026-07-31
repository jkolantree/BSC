from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class CollatzRecursiveSufficiencyApplicationTests(unittest.TestCase):
    @staticmethod
    def shortcut(n: int) -> int:
        return (3 * n + 1) // 2 if n & 1 else n // 2

    @classmethod
    def in_v(cls, n: int, depth: int) -> bool:
        odd_count = 0
        for step in range(1, depth + 1):
            if n & 1:
                odd_count += 1
            n = cls.shortcut(n)
            if 485 * odd_count <= 306 * step:
                return False
        return True

    def test_application_keeps_claims_local_and_conditional(self) -> None:
        text = (
            ROOT / "applications" / "Collatz_Recursive_Sufficiency_Audit.md"
        ).read_text(encoding="utf-8")
        for claim_id in (
            "BSC-CRS-01",
            "BSC-CRS-02",
            "BSC-CRS-03",
            "BSC-CRS-04",
            "BSC-CRS-05",
            "BSC-CRS-06",
        ):
            with self.subTest(claim_id=claim_id):
                self.assertIn(claim_id, text)
        self.assertIn("not a proof of the Collatz conjecture", text)
        self.assertIn("Conditional on the declared verified-prefix assumption", text)
        self.assertIn("36\\mathbb N_0+27", text)
        self.assertIn("remains unresolved", text)

    def test_application_and_fixture_share_exact_certificate_identity(self) -> None:
        application = (
            ROOT / "applications" / "Collatz_Recursive_Sufficiency_Audit.md"
        ).read_text(encoding="utf-8")
        specification = (
            ROOT / "fixtures" / "F11_collatz_recursive_sieve" / "input.json"
        ).read_text(encoding="utf-8")
        digest = (
            "88df1573d49511a4bc93fab35f85d3feb1cade2d40b5444ee"
            "88ae42699aa5250"
        )
        self.assertIn(digest, application)
        self.assertIn(digest, specification)

    def test_first_defect_and_31_class_path(self) -> None:
        f1_mod_36 = {
            (4 * a0 + 3 + 12 * lift) % 36
            for a0 in (0, 1)
            for lift in range(3)
        }
        f2_mod_36 = {
            (4 * (a0 + 3 * a1) + 3) % 36
            for a0 in (0, 1)
            for a1 in (0, 1)
        }
        self.assertEqual(f1_mod_36, {3, 7, 15, 19, 27, 31})
        self.assertEqual(f2_mod_36, {3, 7, 15, 19})
        self.assertEqual(f1_mod_36 - f2_mod_36, {27, 31})

        for k in (0, 1, 2, 17, 1_000_000):
            x = 36 * k + 31
            path = [x, 2 * x, (4 * x - 1) // 3, (8 * x - 5) // 9]
            for left, right in zip(path, path[1:]):
                self.assertTrue(
                    self.shortcut(left) == right
                    or self.shortcut(right) == left
                )
            self.assertEqual(path[-1], 32 * k + 27)
            self.assertLess(path[-1], x)

    def test_five_ninths_factor_starts_at_depth_two(self) -> None:
        g_residues = {3, 7, 15, 19, 27}
        v1 = sum(self.in_v(n, 1) for n in range(36))
        w1 = sum(
            self.in_v(n, 1) and n % 36 in g_residues
            for n in range(36)
        )
        self.assertEqual((v1, w1), (18, 5))
        self.assertNotEqual(9 * w1, 5 * v1)

        for depth in range(2, 9):
            period = 9 * (1 << depth)
            v_count = sum(
                self.in_v(n, depth) for n in range(1 << depth)
            )
            w_count = sum(
                self.in_v(n, depth) and n % 36 in g_residues
                for n in range(period)
            )
            self.assertEqual(w_count, 5 * v_count)


if __name__ == "__main__":
    unittest.main()
