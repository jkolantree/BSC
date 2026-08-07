from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "q26_queen_domination.py"
NOTE = ROOT / "applications" / "Q26_Queen_Domination_Attack.md"
KNOWN_14 = ROOT / "applications" / "Q26_queen_domination_known_14.json"


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


QDOM = load_module(TOOL, "bsc_q26_queen_domination_tests")


def primary_assignment(board_size: int, queens: tuple[tuple[int, int], ...]) -> set[int]:
    return {
        QDOM.queen_variable(board_size, row - 1, column - 1)
        for row, column in queens
    }


def extends_to_model(cnf: object, primary: set[int], primary_count: int) -> bool:
    fixed = {
        variable: variable in primary
        for variable in range(1, primary_count + 1)
    }

    def solve(assignment: dict[int, bool]) -> bool:
        assignment = dict(assignment)
        while True:
            unit: tuple[int, bool] | None = None
            branch_clause: list[int] | None = None
            for clause in cnf.clauses:
                unassigned: list[int] = []
                satisfied = False
                for literal in clause:
                    variable = abs(literal)
                    if variable not in assignment:
                        unassigned.append(literal)
                    elif assignment[variable] == (literal > 0):
                        satisfied = True
                        break
                if satisfied:
                    continue
                if not unassigned:
                    return False
                if len(unassigned) == 1:
                    literal = unassigned[0]
                    unit = (abs(literal), literal > 0)
                    break
                if branch_clause is None or len(unassigned) < len(branch_clause):
                    branch_clause = unassigned
            if unit is None:
                break
            variable, value = unit
            if variable in assignment and assignment[variable] != value:
                return False
            assignment[variable] = value

        if branch_clause is None:
            return True
        variable = abs(branch_clause[0])
        for value in (False, True):
            branch = dict(assignment)
            branch[variable] = value
            if solve(branch):
                return True
        return False

    return solve(fixed)


class Q26QueenDominationTests(unittest.TestCase):
    def test_known_fourteen_queen_witness_is_valid(self) -> None:
        board_size, limit, queens, source = QDOM.load_witness(KNOWN_14)
        result = QDOM.verify_witness(board_size, limit, queens)
        line_result = QDOM.verify_witness_by_lines(board_size, limit, queens)
        self.assertEqual(board_size, 26)
        self.assertEqual(limit, 14)
        self.assertEqual(result["queen_count"], 14)
        self.assertEqual(result["dominated_squares"], 676)
        self.assertEqual(result, line_result)
        self.assertEqual(source, "https://oeis.org/A075458/a075458.txt")

    def test_witness_mutations_fail_closed(self) -> None:
        document = json.loads(KNOWN_14.read_text(encoding="utf-8"))

        duplicate = copy.deepcopy(document)
        duplicate["queens"][1] = duplicate["queens"][0]
        with self.assertRaises(QDOM.QueenDominationError):
            QDOM.normalize_queens(26, duplicate["queens"])

        outside = copy.deepcopy(document)
        outside["queens"][0] = [0, 6]
        with self.assertRaises(QDOM.QueenDominationError):
            QDOM.normalize_queens(26, outside["queens"])

        with self.assertRaises(QDOM.QueenDominationError):
            QDOM.verify_witness(26, 13, document["queens"])

        ineffective = copy.deepcopy(document)
        ineffective["queens"][0] = [1, 1]
        with self.assertRaises(QDOM.QueenDominationError):
            QDOM.verify_witness(26, 14, ineffective["queens"])
        with self.assertRaises(QDOM.QueenDominationError):
            QDOM.verify_witness_by_lines(26, 14, ineffective["queens"])

        with tempfile.TemporaryDirectory(prefix="bsc-q26-json-") as directory:
            duplicate_key = Path(directory) / "duplicate.json"
            duplicate_key.write_text(
                '{"board_size":26,"board_size":25,"claimed_limit":14,'
                '"queens":[],"source":"test"}\n',
                encoding="utf-8",
                newline="\n",
            )
            with self.assertRaises(QDOM.QueenDominationError):
                QDOM.load_witness(duplicate_key)

    def test_direct_and_line_encodings_match_bruteforce_small_boards(self) -> None:
        for board_size in (1, 2):
            squares = tuple(
                (row, column)
                for row in range(1, board_size + 1)
                for column in range(1, board_size + 1)
            )
            primary_count = board_size * board_size
            for limit in range(primary_count + 1):
                formulas = {
                    name: QDOM.build_cnf(board_size, limit, name)
                    for name in ("direct", "line")
                }
                for count in range(primary_count + 1):
                    for queens in itertools.combinations(squares, count):
                        semantic = count <= limit and all(
                            any(QDOM.queen_attacks(queen, square) for queen in queens)
                            for square in squares
                        )
                        assignment = primary_assignment(board_size, queens)
                        for name, formula in formulas.items():
                            with self.subTest(
                                board_size=board_size,
                                limit=limit,
                                queens=queens,
                                encoding=name,
                            ):
                                self.assertEqual(
                                    extends_to_model(formula, assignment, primary_count),
                                    semantic,
                                )

    def test_cardinality_constructions_are_exact_on_small_inputs(self) -> None:
        for variable_count in range(1, 7):
            literals = list(range(1, variable_count + 1))
            for limit in range(variable_count + 1):
                formulas = []
                sequential = QDOM.CNF(variable_count)
                QDOM._sequential_at_most(sequential, literals, limit)
                formulas.append(("sequential", sequential))
                totalizer = QDOM.CNF(variable_count)
                QDOM._totalizer_at_most(totalizer, literals, limit)
                formulas.append(("totalizer", totalizer))
                for count in range(variable_count + 1):
                    for selected in itertools.combinations(literals, count):
                        for name, formula in formulas:
                            with self.subTest(
                                variables=variable_count,
                                limit=limit,
                                count=count,
                                encoding=name,
                            ):
                                self.assertEqual(
                                    extends_to_model(
                                        formula, set(selected), variable_count
                                    ),
                                    count <= limit,
                                )

    def test_totalizer_lower_and_exact_bounds_are_exact(self) -> None:
        for variable_count in range(1, 7):
            literals = list(range(1, variable_count + 1))
            for minimum in range(variable_count + 1):
                for maximum in range(minimum, variable_count + 1):
                    formula = QDOM.CNF(variable_count)
                    QDOM._totalizer_bounds(
                        formula, literals, minimum, maximum
                    )
                    for count in range(variable_count + 1):
                        for selected in itertools.combinations(literals, count):
                            self.assertEqual(
                                extends_to_model(
                                    formula, set(selected), variable_count
                                ),
                                minimum <= count <= maximum,
                            )

    def test_bidirectional_totalizer_lower_bound_is_exact(self) -> None:
        for variable_count in range(1, 8):
            literals = list(range(1, variable_count + 1))
            for minimum in range(variable_count + 1):
                formula = QDOM.CNF(variable_count)
                QDOM._totalizer_at_least(formula, literals, minimum)
                for assignment in QDOM.iter_assignments(variable_count):
                    self.assertEqual(
                        extends_to_model(formula, assignment, variable_count),
                        len(assignment) >= minimum,
                    )

    def test_d4_transformations_are_distinct_permutations(self) -> None:
        for board_size in (2, 3, 4):
            images = [
                tuple(QDOM._d4_transformed_variables(board_size, transform))
                for transform in range(8)
            ]
            expected = list(range(1, board_size * board_size + 1))
            self.assertEqual(len(set(images)), 8)
            for image in images:
                self.assertEqual(sorted(image), expected)

    def test_d4_is_closed_and_preserves_queen_attacks(self) -> None:
        board_size = 4
        permutations = [
            tuple(QDOM._d4_transformed_variables(board_size, transform))
            for transform in range(8)
        ]
        permutation_set = set(permutations)
        for left in permutations:
            for right in permutations:
                composition = tuple(left[right[index] - 1] for index in range(16))
                self.assertIn(composition, permutation_set)

        for permutation in permutations:
            destination = {
                original: transformed + 1
                for transformed, original in enumerate(permutation)
            }
            for first in range(1, 17):
                first_square = ((first - 1) // 4 + 1, (first - 1) % 4 + 1)
                first_image = destination[first]
                first_image_square = (
                    (first_image - 1) // 4 + 1,
                    (first_image - 1) % 4 + 1,
                )
                for second in range(1, 17):
                    second_square = (
                        (second - 1) // 4 + 1,
                        (second - 1) % 4 + 1,
                    )
                    second_image = destination[second]
                    second_image_square = (
                        (second_image - 1) // 4 + 1,
                        (second_image - 1) % 4 + 1,
                    )
                    self.assertEqual(
                        QDOM.queen_attacks(first_square, second_square),
                        QDOM.queen_attacks(first_image_square, second_image_square),
                    )

    def test_lex_helper_matches_arbitrary_vectors(self) -> None:
        for length in range(1, 6):
            left = list(range(1, length + 1))
            right = list(range(length + 1, 2 * length + 1))
            formula = QDOM.CNF(2 * length)
            QDOM._add_lex_leader(formula, left, right)
            for left_mask in range(1 << length):
                for right_mask in range(1 << length):
                    left_vector = tuple(
                        bool(left_mask & (1 << index)) for index in range(length)
                    )
                    right_vector = tuple(
                        bool(right_mask & (1 << index)) for index in range(length)
                    )
                    assignment = {
                        index + 1
                        for index, value in enumerate(left_vector + right_vector)
                        if value
                    }
                    self.assertEqual(
                        extends_to_model(formula, assignment, 2 * length),
                        left_vector <= right_vector,
                    )

    def test_symmetry_breaking_preserves_small_board_satisfiability(self) -> None:
        for board_size in (1, 2):
            variable_count = board_size * board_size
            transforms = [
                QDOM._d4_transformed_variables(board_size, transform)
                for transform in range(8)
            ]
            order = [
                variable - 1
                for variable in QDOM.ordered_queen_variables(board_size, "hilbert")
            ]
            lex_cnf = QDOM.CNF(variable_count)
            QDOM.add_d4_lex_leaders(lex_cnf, board_size)
            for mask in range(1 << variable_count):
                vector = tuple(
                    1 if mask & (1 << index) else 0
                    for index in range(variable_count)
                )
                orbit = []
                for image in transforms:
                    orbit.append(
                        tuple(vector[image[index] - 1] for index in order)
                    )
                identity = tuple(vector[index] for index in order)
                primary = {
                    index + 1 for index, value in enumerate(vector) if value
                }
                self.assertEqual(
                    extends_to_model(lex_cnf, primary, variable_count),
                    identity == min(orbit),
                )

    def test_hilbert_order_is_a_deterministic_board_permutation(self) -> None:
        for board_size in range(1, 9):
            first = QDOM.ordered_queen_variables(board_size, "hilbert")
            second = QDOM.ordered_queen_variables(board_size, "hilbert")
            self.assertEqual(first, second)
            self.assertEqual(
                sorted(first), list(range(1, board_size * board_size + 1))
            )

    def test_line_bound_is_redundant_on_complete_small_semantics(self) -> None:
        board_size = 2
        squares = tuple(
            (row, column)
            for row in range(1, board_size + 1)
            for column in range(1, board_size + 1)
        )
        for limit in range(board_size * board_size + 1):
            strengthened = QDOM.build_cnf(
                board_size, limit, "line", line_bound=True
            )
            unstrengthened = QDOM.build_cnf(
                board_size, limit, "line", line_bound=False
            )
            for count in range(board_size * board_size + 1):
                for queens in itertools.combinations(squares, count):
                    assignment = primary_assignment(board_size, queens)
                    self.assertEqual(
                        extends_to_model(strengthened, assignment, 4),
                        extends_to_model(unstrengthened, assignment, 4),
                    )

    def test_exact_and_supported_line_modes_match_small_semantics(self) -> None:
        board_size = 2
        squares = tuple(
            (row, column)
            for row in range(1, board_size + 1)
            for column in range(1, board_size + 1)
        )
        for limit in range(board_size * board_size + 1):
            exact = QDOM.build_cnf(
                board_size, limit, "line", line_mode="exact"
            )
            supported = QDOM.build_cnf(
                board_size, limit, "line", line_mode="supported"
            )
            for count in range(board_size * board_size + 1):
                for queens in itertools.combinations(squares, count):
                    assignment = primary_assignment(board_size, queens)
                    self.assertEqual(
                        extends_to_model(exact, assignment, 4),
                        extends_to_model(supported, assignment, 4),
                    )

    def test_q26_structural_constraints_are_scoped_fail_closed(self) -> None:
        with self.assertRaises(QDOM.QueenDominationError):
            QDOM.build_cnf(25, 13, "line", q26_structural=True)
        with self.assertRaises(QDOM.QueenDominationError):
            QDOM.build_cnf(26, 12, "line", q26_structural=True)
        with self.assertRaises(QDOM.QueenDominationError):
            QDOM.build_cnf(26, 13, "direct", q26_structural=True)
        constrained = QDOM.build_cnf(
            26,
            13,
            "line",
            symmetry_breaking=True,
            line_mode="supported",
            q26_structural=True,
        )
        unconstrained = QDOM.build_cnf(
            26,
            13,
            "line",
            symmetry_breaking=True,
            line_mode="supported",
            q26_structural=False,
        )
        self.assertGreater(constrained.variable_count, unconstrained.variable_count)
        self.assertGreater(len(constrained.clauses), len(unconstrained.clauses))

    def test_q26_structural_theorem_mapping(self) -> None:
        formula = QDOM.CNF(26 * 26)
        occupancy, _ = QDOM._line_domination(formula, 26, exact_occupancy=False)
        groups = QDOM._q26_structural_groups(26, occupancy)
        self.assertEqual(len(groups["even"]), 338)
        self.assertEqual(len(groups["odd"]), 338)
        self.assertEqual(
            set(groups["even"]) | set(groups["odd"]), set(range(1, 677))
        )
        self.assertFalse(set(groups["even"]) & set(groups["odd"]))
        self.assertEqual(
            groups["rows"], tuple(occupancy[("row", row)] for row in range(26))
        )
        self.assertEqual(
            groups["columns"],
            tuple(occupancy[("column", column)] for column in range(26)),
        )
        self.assertEqual(QDOM.q26_monochromatic_equation_solutions(), ())
        color_splits = {
            (even, 13 - even)
            for even in range(14)
            if even <= 7 and 13 - even <= 7
        }
        self.assertEqual(color_splits, {(6, 7), (7, 6)})

    def test_dimacs_generation_is_deterministic_and_refuses_overwrite(self) -> None:
        cnf_a = QDOM.build_cnf(4, 2, "direct", True)
        cnf_b = QDOM.build_cnf(4, 2, "direct", True)
        bytes_a = QDOM.dimacs_bytes(cnf_a, 4, 2, "direct", True)
        bytes_b = QDOM.dimacs_bytes(cnf_b, 4, 2, "direct", True)
        self.assertEqual(bytes_a, bytes_b)

        with tempfile.TemporaryDirectory(prefix="bsc-q26-cnf-") as directory:
            output = Path(directory) / "instance.cnf"
            command = [
                sys.executable,
                str(TOOL),
                "encode",
                "--board-size",
                "4",
                "--limit",
                "2",
                "--encoding",
                "direct",
                "--d4-lex",
                "--output",
                str(output),
            ]
            first = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(first.returncode, 0, first.stderr)
            retained = output.read_bytes()
            second = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(output.read_bytes(), retained)

    def test_direct_opb_is_deterministic_and_matches_small_semantics(self) -> None:
        def parse_constraints(data: bytes) -> list[tuple[list[tuple[int, int]], int]]:
            lines = data.decode("ascii").splitlines()
            self.assertRegex(
                lines[0],
                r"^\* #variable= \d+ #constraint= \d+ #equal= 0 intsize= \d+$",
            )
            parsed: list[tuple[list[tuple[int, int]], int]] = []
            for line in lines:
                if not line or line.startswith("*"):
                    continue
                tokens = line.split()
                self.assertEqual(tokens[-1], ";")
                comparator = tokens[-3]
                self.assertEqual(comparator, ">=")
                bound = int(tokens[-2])
                terms: list[tuple[int, int]] = []
                for offset in range(0, len(tokens) - 3, 2):
                    coefficient = int(tokens[offset])
                    self.assertIn(coefficient, (-1, 1))
                    self.assertTrue(tokens[offset + 1].startswith("x"))
                    terms.append((coefficient, int(tokens[offset + 1][1:])))
                parsed.append((terms, bound))
            return parsed

        for board_size in (1, 2, 3):
            variable_count = board_size * board_size
            for limit in range(variable_count + 1):
                first = QDOM.opb_bytes(board_size, limit)
                second = QDOM.opb_bytes(board_size, limit)
                self.assertEqual(first, second)
                constraints = parse_constraints(first)
                self.assertEqual(len(constraints), variable_count + 1)
                for assignment in QDOM.iter_assignments(variable_count):
                    accepted = True
                    for terms, bound in constraints:
                        total = sum(
                            coefficient
                            for coefficient, variable in terms
                            if variable in assignment
                        )
                        accepted &= total >= bound
                    queens = tuple(
                        ((variable - 1) // board_size + 1, (variable - 1) % board_size + 1)
                        for variable in sorted(assignment)
                    )
                    semantic = len(queens) <= limit and all(
                        any(QDOM.queen_attacks(queen, square) for queen in queens)
                        for square in itertools.product(
                            range(1, board_size + 1), repeat=2
                        )
                    )
                    self.assertEqual(accepted, semantic)

    def test_solver_model_parser_accepts_models_and_rejects_status_traps(self) -> None:
        self.assertEqual(
            QDOM.parse_solver_model("c run\ns SATISFIABLE\nv 1 -2\nv 3 0\n"),
            (1, -2, 3),
        )
        self.assertEqual(QDOM.parse_solver_model("SAT\n1 -2 3 0\n"), (1, -2, 3))
        self.assertEqual(QDOM.parse_solver_model("1 -2 3 0\n"), (1, -2, 3))
        rejected = (
            "s UNSATISFIABLE\n",
            "s UNKNOWN\n",
            "s SATISFIABLE\n",
            "s SATISFIABLE\nv 1 -1 0\n",
            "s SATISFIABLE\nv 1 0\nv 2\n",
            "s SATISFIABLE\nv 1 nope 0\n",
            "s SATISFIABLE\nv 1 0\n2 0\n",
        )
        for text in rejected:
            with self.subTest(text=text), self.assertRaises(QDOM.QueenDominationError):
                QDOM.parse_solver_model(text)

    def test_decoded_model_report_binds_model_and_instance(self) -> None:
        _, _, queens, _ = QDOM.load_witness(KNOWN_14)
        literals = sorted(primary_assignment(26, queens))
        model_bytes = ("s SATISFIABLE\nv " + " ".join(map(str, literals)) + " 0\n").encode(
            "ascii"
        )
        with tempfile.TemporaryDirectory(prefix="bsc-q26-model-") as directory:
            model = Path(directory) / "model.txt"
            report = Path(directory) / "report.json"
            model.write_bytes(model_bytes)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    "decode-model",
                    "--limit",
                    "14",
                    "--model",
                    str(model),
                    "--instance-sha256",
                    "0" * 64,
                    "--output",
                    str(report),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            value = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(value["report_type"], "verified_solver_model")
            self.assertEqual(value["source_model_bytes"], len(model_bytes))
            self.assertEqual(
                value["source_model_sha256"], hashlib.sha256(model_bytes).hexdigest()
            )
            self.assertEqual(value["source_instance_sha256"], "0" * 64)

    def test_note_preserves_unsolved_and_namespace_boundaries(self) -> None:
        text = NOTE.read_text(encoding="utf-8")
        self.assertIn("not a solved\ncase", text)
        self.assertIn("allocates no BSC claim identifier", text)
        self.assertIn("allocates no BSC claim identifier or fixture identifier", text)
        self.assertIn("`NOT_PROVED`", text)
        self.assertNotIn("BSC-FIX-14", text)
        self.assertNotIn("F14", text)


if __name__ == "__main__":
    unittest.main()
