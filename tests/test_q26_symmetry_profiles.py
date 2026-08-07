from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "q26_symmetry_profiles.py"
REPORT = ROOT / "applications" / "Q26_symmetry_parity_profiles.json"
NOTE = ROOT / "applications" / "Q26_Symmetry_Parity_Profile_Reduction.md"
MAIN_NOTE = ROOT / "applications" / "Q26_Queen_Domination_Attack.md"


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


QPROF = load_module(TOOL, "bsc_q26_symmetry_profile_tests")


class Q26SymmetryProfileTests(unittest.TestCase):
    def test_exact_raw_and_shell_counts(self) -> None:
        document = QPROF.build_report()
        self.assertEqual(
            tuple(
                document["types"][label]["coarse"]["raw_pairs"]
                for label in ("W0", "W1", "W2")
            ),
            (56, 182, 169),
        )
        self.assertEqual(
            tuple(
                document["types"][label]["coarse"]["shells"]
                for label in ("W0", "W1", "W2")
            ),
            (16, 91, 49),
        )
        self.assertEqual(
            tuple(
                document["types"][label]["after_weakley_lemma_6"]["shells"]
                for label in ("W0", "W1", "W2")
            ),
            (15, 78, 49),
        )
        self.assertEqual(document["totals"]["coarse_shells"], 156)
        self.assertEqual(
            document["totals"]["after_weakley_lemma_6_shells"], 142
        )

    def test_orbits_cover_every_raw_pair_without_omission(self) -> None:
        cases = (
            (QPROF.w0_raw_pairs(), QPROF.orbit_w0),
            (QPROF.w1_raw_pairs(), QPROF.orbit_w1),
            (QPROF.w2_raw_pairs(), QPROF.orbit_w2),
        )
        for domain, orbit_function in cases:
            with self.subTest(raw_pairs=len(domain)):
                reps = QPROF.representatives(domain, orbit_function)
                covered: set[tuple[int, int]] = set()
                for representative in reps:
                    orbit = orbit_function(representative)
                    self.assertTrue(orbit <= domain)
                    self.assertEqual(representative, min(orbit))
                    self.assertTrue(covered.isdisjoint(orbit))
                    covered.update(orbit)
                self.assertEqual(covered, set(domain))

    def test_weakley_tightening_and_w0_roster(self) -> None:
        raw0 = QPROF.w0_raw_pairs()
        tight0 = frozenset(
            pair
            for pair in raw0
            if 1 <= pair[0] <= 12 and 1 <= pair[1] <= 12
        )
        removed = raw0 - tight0
        self.assertEqual(removed, {(0, 7), (7, 0), (13, 6), (6, 13)})
        self.assertEqual(
            QPROF.representatives(tight0, QPROF.orbit_w0),
            QPROF.EXPECTED_TIGHTENED_W0,
        )

        raw1 = QPROF.w1_raw_pairs()
        tight1 = frozenset(pair for pair in raw1 if 1 <= pair[1] <= 12)
        self.assertEqual(len(tight0), 52)
        self.assertEqual(len(tight1), 156)
        self.assertEqual(len(QPROF.w2_raw_pairs()), 169)

    def test_independent_burnside_fixed_point_counts(self) -> None:
        raw0 = QPROF.w0_raw_pairs()
        raw1 = QPROF.w1_raw_pairs()
        raw2 = QPROF.w2_raw_pairs()
        tight0 = frozenset(
            pair
            for pair in raw0
            if 1 <= pair[0] <= 12 and 1 <= pair[1] <= 12
        )
        tight1 = frozenset(pair for pair in raw1 if 1 <= pair[1] <= 12)

        def fixed(
            domain: frozenset[tuple[int, int]],
            transform: Callable[[tuple[int, int]], tuple[int, int]],
        ) -> int:
            return sum(transform(pair) == pair for pair in domain)

        w0_transforms = (
            lambda pair: pair,
            lambda pair: (pair[1], pair[0]),
            lambda pair: (13 - pair[0], 13 - pair[1]),
            lambda pair: (13 - pair[1], 13 - pair[0]),
        )
        w2_transforms = (
            lambda pair: pair,
            lambda pair: (pair[1], pair[0]),
            lambda pair: (12 - pair[0], 12 - pair[1]),
            lambda pair: (12 - pair[1], 12 - pair[0]),
        )
        w1_half_turn = lambda pair: (12 - pair[0], 13 - pair[1])

        self.assertEqual(
            tuple(fixed(raw0, action) for action in w0_transforms),
            (56, 0, 0, 8),
        )
        self.assertEqual(
            tuple(fixed(tight0, action) for action in w0_transforms),
            (52, 0, 0, 8),
        )
        self.assertEqual((len(raw1), fixed(raw1, w1_half_turn)), (182, 0))
        self.assertEqual((len(tight1), fixed(tight1, w1_half_turn)), (156, 0))
        self.assertEqual(
            tuple(fixed(raw2, action) for action in w2_transforms),
            (169, 13, 1, 13),
        )

    def test_materialized_report_is_canonical_and_deterministic(self) -> None:
        first = QPROF.canonical_bytes()
        second = QPROF.canonical_bytes()
        self.assertEqual(first, second)
        self.assertEqual(REPORT.read_bytes(), first)
        QPROF.verify_report(json.loads(first.decode("utf-8")))

    def test_report_mutations_fail_closed(self) -> None:
        mutations: list[dict[str, object]] = []

        missing = copy.deepcopy(QPROF.build_report())
        missing["types"]["W1"]["coarse"]["representatives"].pop()
        mutations.append(missing)

        duplicate = copy.deepcopy(QPROF.build_report())
        representatives = duplicate["types"]["W2"]["coarse"]["representatives"]
        representatives.append(copy.deepcopy(representatives[0]))
        mutations.append(duplicate)

        altered_total = copy.deepcopy(QPROF.build_report())
        altered_total["totals"]["coarse_shells"] = 155
        mutations.append(altered_total)

        weakened_lemma = copy.deepcopy(QPROF.build_report())
        weakened_lemma["types"]["W0"]["after_weakley_lemma_6"]["raw_pairs"] = 56
        mutations.append(weakened_lemma)

        for mutation in mutations:
            with self.subTest(mutation=mutations.index(mutation)):
                with self.assertRaises(QPROF.ProfileError):
                    QPROF.verify_report(mutation)

    def test_cli_summary_json_check_and_mismatch(self) -> None:
        summary = subprocess.run(
            [sys.executable, str(TOOL)],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertIn("coarse: (16, 91, 49) total=156", summary)
        self.assertIn("after Weakley Lemma 6: (15, 78, 49) total=142", summary)

        encoded = subprocess.run(
            [sys.executable, str(TOOL), "--json"],
            check=True,
            capture_output=True,
        ).stdout
        self.assertEqual(encoded, REPORT.read_bytes())

        subprocess.run(
            [sys.executable, str(TOOL), "--check", str(REPORT)],
            check=True,
            capture_output=True,
            text=True,
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            written = Path(temporary_directory) / "written.json"
            subprocess.run(
                [sys.executable, str(TOOL), "--write", str(written)],
                check=True,
                capture_output=True,
                text=True,
            )
            retained = written.read_bytes()
            overwrite = subprocess.run(
                [sys.executable, str(TOOL), "--write", str(written)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(overwrite.returncode, 0)
            self.assertEqual(written.read_bytes(), retained)

            altered = Path(temporary_directory) / "altered.json"
            altered.write_bytes(REPORT.read_bytes() + b"\n")
            result = subprocess.run(
                [sys.executable, str(TOOL), "--check", str(altered)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("does not match", result.stderr)

    def test_published_compact_reproduction_executes(self) -> None:
        text = NOTE.read_text(encoding="utf-8")
        block = text.split("```python", 1)[1].split("```", 1)[0].strip()
        output = subprocess.run(
            [sys.executable, "-c", block],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertEqual(
            output.splitlines(),
            [
                "(16, 91, 49) 156",
                "(15, 78, 49) 142",
                "[(1, 6), (1, 8), (2, 5), (2, 7), (2, 9), (3, 4), "
                "(3, 6), (3, 8), (3, 10), (4, 5), (4, 7), (4, 9), "
                "(5, 6), (5, 8), (6, 7)]",
            ],
        )

    def test_public_scope_and_cross_links_are_explicit(self) -> None:
        note = NOTE.read_text(encoding="utf-8")
        normalized_note = " ".join(note.split())
        self.assertIn("both totals are **over-covers**", note)
        self.assertIn("incorrectly described these 156 shells", normalized_note)
        self.assertIn("No retained solver run returned `UNSAT`", normalized_note)
        self.assertIn("does **not** prove that thirteen queens cannot dominate", note)
        self.assertIn("No retained solver output", normalized_note)
        self.assertIn("13\\leq\\gamma(Q_{26})\\leq14", note)
        self.assertIn("tools/q26_symmetry_profiles.py", note)
        self.assertIn("Q26_symmetry_parity_profiles.json", note)

        main_note = MAIN_NOTE.read_text(encoding="utf-8")
        normalized_main_note = " ".join(main_note.split())
        self.assertIn("Q26_Symmetry_Parity_Profile_Reduction.md", main_note)
        self.assertIn(
            "not a list of queen placements or solved SAT instances",
            normalized_main_note,
        )


if __name__ == "__main__":
    unittest.main()
