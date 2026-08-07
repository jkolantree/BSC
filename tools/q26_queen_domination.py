#!/usr/bin/env python3
"""Generate and independently check exact queen-domination instances.

The core module is dependency-free.  It deliberately separates three roles:

* witness checking, which is direct integer geometry;
* deterministic CNF generation, which does not call a SAT solver; and
* optional model decoding, which never treats an unchecked solver status as a
  mathematical certificate.

Two equisatisfiable CNF encodings are provided.  ``direct`` uses one inclusive
attack-neighbourhood clause per square and a sequential unary counter.
``line`` introduces row/column/diagonal support variables and uses a balanced
totalizer.  A third, direct OPB generator independently reconstructs the
coverage constraints without either CNF geometry helper.  These lanes share
only the coordinate convention and deterministic writers, not their
domination or cardinality constructions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence


Q26_BOARD_SIZE = 26
Q26_TARGET = 13


class QueenDominationError(ValueError):
    """Raised when an input, encoding, or claimed witness is invalid."""


Square = tuple[int, int]


def _closed_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise QueenDominationError(f"{label} must be an object")
    actual = set(value)
    if actual != keys:
        raise QueenDominationError(
            f"{label} keys mismatch: missing={sorted(keys - actual)}, "
            f"extra={sorted(actual - keys)}"
        )
    return value


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise QueenDominationError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def normalize_queens(board_size: int, values: Iterable[Sequence[int]]) -> tuple[Square, ...]:
    if type(board_size) is not int or board_size < 1:
        raise QueenDominationError("board_size must be a positive integer")
    queens: list[Square] = []
    for index, value in enumerate(values):
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise QueenDominationError(f"queen {index} must be a coordinate pair")
        row, column = value
        if type(row) is not int or type(column) is not int:
            raise QueenDominationError(f"queen {index} coordinates must be integers")
        if not (1 <= row <= board_size and 1 <= column <= board_size):
            raise QueenDominationError(
                f"queen {index} is outside the {board_size}x{board_size} board"
            )
        queens.append((row, column))
    if len(set(queens)) != len(queens):
        raise QueenDominationError("queen coordinates must be distinct")
    return tuple(sorted(queens))


def queen_attacks(queen: Square, square: Square) -> bool:
    row, column = queen
    target_row, target_column = square
    return (
        row == target_row
        or column == target_column
        or row - column == target_row - target_column
        or row + column == target_row + target_column
    )


def inclusive_neighbourhood(board_size: int, square: Square) -> tuple[Square, ...]:
    row, column = square
    return tuple(
        (candidate_row, candidate_column)
        for candidate_row in range(1, board_size + 1)
        for candidate_column in range(1, board_size + 1)
        if queen_attacks((candidate_row, candidate_column), (row, column))
    )


def verify_witness(
    board_size: int,
    limit: int,
    queens: Iterable[Sequence[int]],
) -> dict[str, Any]:
    if type(limit) is not int or limit < 0:
        raise QueenDominationError("limit must be a nonnegative integer")
    normalized = normalize_queens(board_size, queens)
    if len(normalized) > limit:
        raise QueenDominationError(
            f"witness has {len(normalized)} queens, exceeding limit {limit}"
        )
    undominated = [
        [row, column]
        for row in range(1, board_size + 1)
        for column in range(1, board_size + 1)
        if not any(queen_attacks(queen, (row, column)) for queen in normalized)
    ]
    if undominated:
        raise QueenDominationError(
            f"witness leaves {len(undominated)} squares undominated: "
            f"{undominated[:8]}"
        )
    return {
        "board_size": board_size,
        "dominated_squares": board_size * board_size,
        "queen_count": len(normalized),
        "queens": [[row, column] for row, column in normalized],
        "valid": True,
    }


def verify_witness_by_lines(
    board_size: int,
    limit: int,
    queens: Iterable[Sequence[int]],
) -> dict[str, Any]:
    """Independently check domination through occupied-line sets."""
    if type(limit) is not int or limit < 0:
        raise QueenDominationError("limit must be a nonnegative integer")
    normalized = normalize_queens(board_size, queens)
    if len(normalized) > limit:
        raise QueenDominationError(
            f"witness has {len(normalized)} queens, exceeding limit {limit}"
        )
    rows = {row for row, _ in normalized}
    columns = {column for _, column in normalized}
    diagonals = {row - column for row, column in normalized}
    antidiagonals = {row + column for row, column in normalized}
    undominated = [
        [row, column]
        for row in range(1, board_size + 1)
        for column in range(1, board_size + 1)
        if row not in rows
        and column not in columns
        and row - column not in diagonals
        and row + column not in antidiagonals
    ]
    if undominated:
        raise QueenDominationError(
            f"line-set checker leaves {len(undominated)} squares undominated: "
            f"{undominated[:8]}"
        )
    return {
        "board_size": board_size,
        "dominated_squares": board_size * board_size,
        "queen_count": len(normalized),
        "queens": [[row, column] for row, column in normalized],
        "valid": True,
    }


def load_witness(path: Path) -> tuple[int, int, tuple[Square, ...], str]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise QueenDominationError(f"cannot read witness: {exc}") from exc
    if data.startswith(b"\xef\xbb\xbf") or b"\r" in data:
        raise QueenDominationError("witness must be strict UTF-8 with LF line endings")
    try:
        value = json.loads(
            data.decode("utf-8", errors="strict"),
            object_pairs_hook=_unique_json_object,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise QueenDominationError(f"invalid witness JSON: {exc}") from exc
    document = _closed_object(
        value,
        {"board_size", "claimed_limit", "queens", "source"},
        "witness",
    )
    board_size = document["board_size"]
    limit = document["claimed_limit"]
    source = document["source"]
    if type(board_size) is not int or type(limit) is not int:
        raise QueenDominationError("board_size and claimed_limit must be integers")
    if not isinstance(source, str) or not source:
        raise QueenDominationError("source must be a nonempty string")
    if not isinstance(document["queens"], list):
        raise QueenDominationError("queens must be an array")
    queens = normalize_queens(board_size, document["queens"])
    return board_size, limit, queens, source


def queen_variable(board_size: int, row: int, column: int) -> int:
    if not (0 <= row < board_size and 0 <= column < board_size):
        raise QueenDominationError("zero-based square is outside the board")
    return row * board_size + column + 1


@dataclass
class CNF:
    variable_count: int
    clauses: list[tuple[int, ...]] = field(default_factory=list)

    def new_variable(self) -> int:
        self.variable_count += 1
        return self.variable_count

    def add_clause(self, literals: Iterable[int]) -> None:
        clause: list[int] = []
        seen: set[int] = set()
        for literal in literals:
            if type(literal) is not int or literal == 0:
                raise QueenDominationError("CNF literals must be nonzero integers")
            if abs(literal) > self.variable_count:
                raise QueenDominationError(
                    f"literal {literal} exceeds variable count {self.variable_count}"
                )
            if -literal in seen:
                return
            if literal not in seen:
                seen.add(literal)
                clause.append(literal)
        if not clause:
            raise QueenDominationError("refusing to add an empty CNF clause")
        self.clauses.append(tuple(clause))


def _sequential_at_most(cnf: CNF, literals: Sequence[int], limit: int) -> None:
    """Encode at-most-limit through one-way prefix-count implications."""
    if limit < 0:
        raise QueenDominationError("cardinality limit must be nonnegative")
    if limit >= len(literals):
        return
    if limit == 0:
        for literal in literals:
            cnf.add_clause([-literal])
        return
    cap = limit + 1
    previous: list[int] = []
    for index, literal in enumerate(literals, start=1):
        current = [cnf.new_variable() for _ in range(min(index, cap))]
        cnf.add_clause([-literal, current[0]])
        for count, prior in enumerate(previous, start=1):
            cnf.add_clause([-prior, current[count - 1]])
        for count, prior in enumerate(previous, start=1):
            if count + 1 <= len(current):
                cnf.add_clause([-literal, -prior, current[count]])
        previous = current
    cnf.add_clause([-previous[cap - 1]])


def _totalizer_outputs(cnf: CNF, literals: Sequence[int], cap: int) -> list[int]:
    if len(literals) == 1:
        return [literals[0]]
    midpoint = len(literals) // 2
    left = _totalizer_outputs(cnf, literals[:midpoint], cap)
    right = _totalizer_outputs(cnf, literals[midpoint:], cap)
    output = [cnf.new_variable() for _ in range(min(cap, len(left) + len(right)))]
    for count, literal in enumerate(left, start=1):
        cnf.add_clause([-literal, output[min(count, cap) - 1]])
    for count, literal in enumerate(right, start=1):
        cnf.add_clause([-literal, output[min(count, cap) - 1]])
    for left_count, left_literal in enumerate(left, start=1):
        for right_count, right_literal in enumerate(right, start=1):
            combined = min(left_count + right_count, cap)
            cnf.add_clause([-left_literal, -right_literal, output[combined - 1]])
    return output


def _totalizer_bounds(
    cnf: CNF,
    literals: Sequence[int],
    minimum: int,
    maximum: int,
) -> None:
    if not (0 <= minimum <= maximum <= len(literals)):
        raise QueenDominationError("invalid totalizer cardinality bounds")
    if minimum:
        _totalizer_at_most(cnf, [-literal for literal in literals], len(literals) - minimum)
    if maximum < len(literals):
        _totalizer_at_most(cnf, literals, maximum)


def _totalizer_at_most(cnf: CNF, literals: Sequence[int], limit: int) -> None:
    if limit < 0 or limit > len(literals):
        raise QueenDominationError("cardinality limit is outside the valid range")
    if limit >= len(literals):
        return
    if limit == 0:
        for literal in literals:
            cnf.add_clause([-literal])
        return
    output = _totalizer_outputs(cnf, literals, limit + 1)
    cnf.add_clause([-output[limit]])


def _bidirectional_totalizer_outputs(
    cnf: CNF, literals: Sequence[int], cap: int
) -> list[int]:
    """Return exact unary threshold outputs up to ``cap``.

    Unlike the propagation-only totalizer used for upper bounds, every output
    here is equivalent to the corresponding threshold.  This makes it sound to
    assert a positive output when encoding a small lower bound.
    """
    if not literals or cap < 1:
        raise QueenDominationError("bidirectional totalizer requires inputs and cap")
    if len(literals) == 1:
        return [literals[0]]
    midpoint = len(literals) // 2
    left = _bidirectional_totalizer_outputs(cnf, literals[:midpoint], cap)
    right = _bidirectional_totalizer_outputs(cnf, literals[midpoint:], cap)
    output = [cnf.new_variable() for _ in range(min(cap, len(left) + len(right)))]

    # If the children certify i and j true inputs, the parent certifies i+j.
    for left_count in range(len(left) + 1):
        for right_count in range(len(right) + 1):
            combined = left_count + right_count
            if combined == 0 or combined > len(output):
                continue
            clause: list[int] = []
            if left_count:
                clause.append(-left[left_count - 1])
            if right_count:
                clause.append(-right[right_count - 1])
            clause.append(output[combined - 1])
            cnf.add_clause(clause)

    # Conversely, threshold k implies that for every split i+j=k-1, the left
    # reaches i+1 or the right reaches j+1.  These clauses prevent an auxiliary
    # output from being asserted without enough true inputs.
    for left_count in range(len(left) + 1):
        for right_count in range(len(right) + 1):
            threshold = left_count + right_count + 1
            if threshold > len(output):
                continue
            clause = [-output[threshold - 1]]
            if left_count < len(left):
                clause.append(left[left_count])
            if right_count < len(right):
                clause.append(right[right_count])
            cnf.add_clause(clause)
    return output


def _totalizer_at_least(cnf: CNF, literals: Sequence[int], minimum: int) -> None:
    if not (0 <= minimum <= len(literals)):
        raise QueenDominationError("cardinality minimum is outside the valid range")
    if minimum == 0:
        return
    output = _bidirectional_totalizer_outputs(cnf, literals, minimum)
    cnf.add_clause([output[minimum - 1]])


def _direct_domination(cnf: CNF, board_size: int) -> None:
    for row in range(board_size):
        for column in range(board_size):
            square = (row + 1, column + 1)
            cnf.add_clause(
                queen_variable(board_size, q_row - 1, q_column - 1)
                for q_row, q_column in inclusive_neighbourhood(board_size, square)
            )


def opb_bytes(board_size: int, limit: int) -> bytes:
    """Return a direct pseudo-Boolean decision instance.

    This deliberately reconstructs each attack neighbourhood from its four
    integer equalities instead of calling ``inclusive_neighbourhood`` or the
    line-CNF builder.  It is the compact semantic-audit lane for proof-logging
    pseudo-Boolean solvers.
    """
    if type(board_size) is not int or board_size < 1:
        raise QueenDominationError("board_size must be a positive integer")
    variable_count = board_size * board_size
    if type(limit) is not int or not (0 <= limit <= variable_count):
        raise QueenDominationError("limit is outside the valid cardinality range")

    constraints: list[str] = []
    largest_absolute_sum = 0
    for target_row in range(board_size):
        for target_column in range(board_size):
            variables: list[int] = []
            for queen_row in range(board_size):
                for queen_column in range(board_size):
                    if (
                        queen_row == target_row
                        or queen_column == target_column
                        or queen_row - queen_column == target_row - target_column
                        or queen_row + queen_column == target_row + target_column
                    ):
                        variables.append(
                            queen_row * board_size + queen_column + 1
                        )
            terms = " ".join(f"+1 x{variable}" for variable in variables)
            constraints.append(f"{terms} >= 1 ;")
            largest_absolute_sum = max(
                largest_absolute_sum, len(variables) + 1
            )
    cardinality = " ".join(
        f"-1 x{variable}" for variable in range(1, variable_count + 1)
    )
    constraints.append(f"{cardinality} >= {-limit} ;")
    largest_absolute_sum = max(
        largest_absolute_sum, variable_count + abs(limit)
    )
    lines = [
        f"* #variable= {variable_count} #constraint= {len(constraints)} "
        f"#equal= 0 intsize= {largest_absolute_sum.bit_length()}",
        "* BSC independent direct queen-domination decision encoding",
        f"* board_size {board_size}",
        f"* limit {limit}",
        *constraints,
    ]
    return ("\n".join(lines) + "\n").encode("ascii")


def _line_domination(
    cnf: CNF,
    board_size: int,
    exact_occupancy: bool,
) -> tuple[dict[tuple[str, int], int], dict[int, int]]:
    lines: dict[tuple[str, int], list[int]] = {}
    for row in range(board_size):
        lines[("row", row)] = []
        lines[("column", row)] = []
    for diagonal in range(-(board_size - 1), board_size):
        lines[("diagonal", diagonal)] = []
    for antidiagonal in range(2 * board_size - 1):
        lines[("antidiagonal", antidiagonal)] = []

    for row in range(board_size):
        for column in range(board_size):
            variable = queen_variable(board_size, row, column)
            lines[("row", row)].append(variable)
            lines[("column", column)].append(variable)
            lines[("diagonal", row - column)].append(variable)
            lines[("antidiagonal", row + column)].append(variable)

    occupancy: dict[tuple[str, int], int] = {}
    line_lengths: dict[int, int] = {}
    for key in sorted(lines):
        line_variable = cnf.new_variable()
        occupancy[key] = line_variable
        members = lines[key]
        line_lengths[line_variable] = len(members)
        if exact_occupancy:
            for queen in members:
                cnf.add_clause([-queen, line_variable])
        cnf.add_clause([-line_variable, *members])

    for row in range(board_size):
        for column in range(board_size):
            cnf.add_clause(
                [
                    occupancy[("row", row)],
                    occupancy[("column", column)],
                    occupancy[("diagonal", row - column)],
                    occupancy[("antidiagonal", row + column)],
                ]
            )
    return occupancy, line_lengths


def _q26_structural_groups(
    board_size: int,
    occupancy: dict[tuple[str, int], int],
) -> dict[str, tuple[int, ...]]:
    if board_size != Q26_BOARD_SIZE:
        raise QueenDominationError("Q26 structural groups require board size 26")
    expected = {
        *(('row', index) for index in range(board_size)),
        *(('column', index) for index in range(board_size)),
    }
    if not expected.issubset(occupancy):
        raise QueenDominationError("Q26 occupancy map is missing rows or columns")
    return {
        "even": tuple(
            queen_variable(board_size, row, column)
            for row in range(board_size)
            for column in range(board_size)
            if (row + column) % 2 == 0
        ),
        "odd": tuple(
            queen_variable(board_size, row, column)
            for row in range(board_size)
            for column in range(board_size)
            if (row + column) % 2 == 1
        ),
        "rows": tuple(occupancy[("row", row)] for row in range(board_size)),
        "columns": tuple(
            occupancy[("column", column)] for column in range(board_size)
        ),
    }


def q26_monochromatic_equation_solutions() -> tuple[tuple[int, int], ...]:
    """Enumerate Weakley's admissible odd ``(d, e)`` pairs for Q26."""
    return tuple(
        (d, e)
        for d in range(1, 14, 2)
        for e in range(1, 14, 2)
        if d * d + 12 * e * e == 741
    )


def hilbert_distance(row: int, column: int, bits: int) -> int:
    """Return the standard two-dimensional Hilbert distance."""
    if bits < 0 or not (0 <= row < 1 << bits and 0 <= column < 1 << bits):
        raise QueenDominationError("Hilbert coordinate is outside its square")
    x, y = row, column
    distance = 0
    scale = 1 << (bits - 1) if bits else 0
    while scale:
        rx = 1 if x & scale else 0
        ry = 1 if y & scale else 0
        distance += scale * scale * ((3 * rx) ^ ry)
        if ry == 0:
            if rx == 1:
                x = 2 * scale - 1 - x
                y = 2 * scale - 1 - y
            x, y = y, x
        scale //= 2
    return distance


def ordered_queen_variables(board_size: int, ordering: str) -> list[int]:
    coordinates = [
        (row, column)
        for row in range(board_size)
        for column in range(board_size)
    ]
    if ordering == "row-major":
        pass
    elif ordering == "hilbert":
        bits = (board_size - 1).bit_length()
        coordinates.sort(
            key=lambda square: hilbert_distance(square[0], square[1], bits)
        )
    elif ordering == "domination-degree":
        coordinates.sort(
            key=lambda square: (
                -len(
                    inclusive_neighbourhood(
                        board_size, (square[0] + 1, square[1] + 1)
                    )
                ),
                square,
            )
        )
    else:
        raise QueenDominationError(f"unknown literal ordering: {ordering}")
    return [
        queen_variable(board_size, row, column) for row, column in coordinates
    ]


def _d4_transformed_variables(board_size: int, transform: int) -> list[int]:
    transformed = [0] * (board_size * board_size)
    for row in range(board_size):
        for column in range(board_size):
            if transform == 0:
                new_row, new_column = row, column
            elif transform == 1:
                new_row, new_column = column, board_size - 1 - row
            elif transform == 2:
                new_row, new_column = board_size - 1 - row, board_size - 1 - column
            elif transform == 3:
                new_row, new_column = board_size - 1 - column, row
            elif transform == 4:
                new_row, new_column = row, board_size - 1 - column
            elif transform == 5:
                new_row, new_column = board_size - 1 - row, column
            elif transform == 6:
                new_row, new_column = column, row
            elif transform == 7:
                new_row, new_column = board_size - 1 - column, board_size - 1 - row
            else:
                raise QueenDominationError(f"unknown D4 transform {transform}")
            transformed[new_row * board_size + new_column] = queen_variable(
                board_size, row, column
            )
    return transformed


def _add_lex_leader(cnf: CNF, left: Sequence[int], right: Sequence[int]) -> None:
    """Require left <=lex right, with 0 preceding 1."""
    if len(left) != len(right):
        raise QueenDominationError("lex-leader vectors must have equal length")
    prefix_equal: int | None = None
    for left_literal, right_literal in zip(left, right):
        if prefix_equal is None:
            cnf.add_clause([-left_literal, right_literal])
        else:
            cnf.add_clause([-prefix_equal, -left_literal, right_literal])

        next_prefix = cnf.new_variable()
        if prefix_equal is not None:
            cnf.add_clause([-next_prefix, prefix_equal])
            cnf.add_clause(
                [-prefix_equal, -left_literal, -right_literal, next_prefix]
            )
            cnf.add_clause(
                [-prefix_equal, left_literal, right_literal, next_prefix]
            )
        else:
            cnf.add_clause([-left_literal, -right_literal, next_prefix])
            cnf.add_clause([left_literal, right_literal, next_prefix])
        cnf.add_clause([-next_prefix, -left_literal, right_literal])
        cnf.add_clause([-next_prefix, left_literal, -right_literal])
        prefix_equal = next_prefix


def add_d4_lex_leaders(cnf: CNF, board_size: int, ordering: str = "hilbert") -> None:
    order = [variable - 1 for variable in ordered_queen_variables(board_size, ordering)]
    identity_full = _d4_transformed_variables(board_size, 0)
    identity = [identity_full[index] for index in order]
    for transform in range(1, 8):
        transformed = _d4_transformed_variables(board_size, transform)
        _add_lex_leader(
            cnf,
            identity,
            [transformed[index] for index in order],
        )


def build_cnf(
    board_size: int,
    limit: int,
    encoding: str,
    symmetry_breaking: bool = False,
    ordering: str = "hilbert",
    line_bound: bool = True,
    line_mode: str = "exact",
    q26_structural: bool = False,
) -> CNF:
    if type(board_size) is not int or board_size < 1:
        raise QueenDominationError("board_size must be a positive integer")
    if type(limit) is not int or not (0 <= limit <= board_size * board_size):
        raise QueenDominationError("limit is outside the valid cardinality range")
    if line_mode not in {"exact", "supported"}:
        raise QueenDominationError(f"unknown line mode: {line_mode}")
    if q26_structural and (board_size, limit, encoding) != (26, 13, "line"):
        raise QueenDominationError(
            "Q26 structural constraints require the 26x26 line instance at limit 13"
        )
    cnf = CNF(variable_count=board_size * board_size)
    queens = ordered_queen_variables(board_size, ordering)
    if encoding == "direct":
        _direct_domination(cnf, board_size)
        _sequential_at_most(cnf, queens, limit)
    elif encoding == "line":
        occupancy, line_lengths = _line_domination(
            cnf, board_size, exact_occupancy=line_mode == "exact"
        )
        line_variables = list(occupancy.values())
        _totalizer_at_most(cnf, queens, limit)
        if line_bound and 4 * limit < len(line_variables):
            ordered_lines = sorted(
                line_variables, key=lambda variable: (-line_lengths[variable], variable)
            )
            _totalizer_at_most(cnf, ordered_lines, 4 * limit)
        if q26_structural:
            # Weakley's strict lower bound gamma(Q_n) > (n - 1) / 2 makes an
            # at-most-13 Q26 witness an exactly-13 witness.  Encoding the
            # theorem-derived lower side improves propagation without changing
            # the decision problem.
            _totalizer_at_least(cnf, queens, 13)
            groups = _q26_structural_groups(board_size, occupancy)
            _totalizer_at_most(cnf, groups["even"], 7)
            _totalizer_at_most(cnf, groups["odd"], 7)
            _totalizer_bounds(cnf, groups["rows"], 12, board_size)
            _totalizer_bounds(cnf, groups["columns"], 12, board_size)
    else:
        raise QueenDominationError(f"unknown encoding: {encoding}")
    if symmetry_breaking:
        add_d4_lex_leaders(cnf, board_size, ordering)
    return cnf


def dimacs_bytes(
    cnf: CNF,
    board_size: int,
    limit: int,
    encoding: str,
    symmetry_breaking: bool,
    ordering: str = "hilbert",
    line_bound: bool = True,
    line_mode: str = "exact",
    q26_structural: bool = False,
) -> bytes:
    lines = [
        "c BSC independent queen-domination decision encoding",
        f"c board_size {board_size}",
        f"c limit {limit}",
        f"c encoding {encoding}",
        f"c literal_ordering {ordering}",
        f"c line_bound {str(line_bound and encoding == 'line').lower()}",
        f"c line_mode {line_mode if encoding == 'line' else 'not-applicable'}",
        f"c q26_structural {str(q26_structural).lower()}",
        f"c d4_lex_leaders {str(symmetry_breaking).lower()}",
        f"p cnf {cnf.variable_count} {len(cnf.clauses)}",
    ]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in cnf.clauses)
    return ("\n".join(lines) + "\n").encode("ascii")


def decode_model(board_size: int, model: Iterable[int]) -> tuple[Square, ...]:
    positive = {literal for literal in model if literal > 0}
    return tuple(
        (row + 1, column + 1)
        for row in range(board_size)
        for column in range(board_size)
        if queen_variable(board_size, row, column) in positive
    )


def parse_solver_model(text: str) -> tuple[int, ...]:
    """Parse a DIMACS-style SAT model while rejecting non-SAT statuses.

    Accepted inputs are ordinary ``s SATISFIABLE`` plus one or more ``v``
    records, MiniSat-style ``SAT`` plus numeric records, or a bare numeric model.
    Comments and blank lines are ignored.  Contradictory literals, content after
    the terminating zero, malformed records, and UNSAT/UNKNOWN statuses fail
    closed.
    """
    if not isinstance(text, str):
        raise QueenDominationError("solver model must be decoded text")
    status: str | None = None
    records: list[list[str]] = []
    saw_v_record = False
    saw_raw_record = False

    def set_status(candidate: str) -> None:
        nonlocal status
        normalized = candidate.strip().upper()
        aliases = {
            "SAT": "SAT",
            "SATISFIABLE": "SAT",
            "UNSAT": "UNSAT",
            "UNSATISFIABLE": "UNSAT",
            "UNKNOWN": "UNKNOWN",
            "INDETERMINATE": "UNKNOWN",
        }
        if normalized not in aliases:
            raise QueenDominationError(f"unrecognized solver status: {candidate}")
        resolved = aliases[normalized]
        if status is not None and status != resolved:
            raise QueenDominationError("conflicting solver statuses")
        status = resolved

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        parts = line.split()
        head = parts[0]
        if head == "s":
            if len(parts) != 2:
                raise QueenDominationError(
                    f"malformed solver status on line {line_number}"
                )
            set_status(parts[1])
        elif len(parts) == 1 and head.upper() in {
            "SAT",
            "SATISFIABLE",
            "UNSAT",
            "UNSATISFIABLE",
            "UNKNOWN",
            "INDETERMINATE",
        }:
            set_status(head)
        elif head == "v":
            saw_v_record = True
            records.append(parts[1:])
        else:
            saw_raw_record = True
            records.append(parts)

    if saw_v_record and saw_raw_record:
        raise QueenDominationError("cannot mix prefixed and bare model records")
    if status is not None and status != "SAT":
        raise QueenDominationError(f"solver status is {status}, not SAT")
    if not records:
        raise QueenDominationError("solver output contains no model literals")

    literals: list[int] = []
    terminated = False
    seen: set[int] = set()
    for record in records:
        if not record:
            raise QueenDominationError("empty solver model record")
        for token in record:
            try:
                literal = int(token)
            except ValueError as exc:
                raise QueenDominationError(
                    f"non-integer solver model token: {token}"
                ) from exc
            if terminated:
                raise QueenDominationError("content follows the model terminator")
            if literal == 0:
                terminated = True
                continue
            if -literal in seen:
                raise QueenDominationError(
                    f"solver model contains both {literal} and {-literal}"
                )
            if literal not in seen:
                seen.add(literal)
                literals.append(literal)
    if not literals:
        raise QueenDominationError("solver output contains no nonzero literals")
    return tuple(literals)


def iter_assignments(variable_count: int) -> Iterator[set[int]]:
    for mask in range(1 << variable_count):
        yield {
            variable
            for variable in range(1, variable_count + 1)
            if mask & (1 << (variable - 1))
        }


def clause_satisfied(clause: Sequence[int], assignment: set[int]) -> bool:
    return any(
        (literal > 0 and literal in assignment)
        or (literal < 0 and -literal not in assignment)
        for literal in clause
    )


def _write_new_file(path: Path, data: bytes) -> None:
    try:
        with path.open("xb") as stream:
            stream.write(data)
    except FileExistsError as exc:
        raise QueenDominationError(
            f"refusing to overwrite existing file: {path}"
        ) from exc


def _validated_sha256(value: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise QueenDominationError("instance SHA-256 must be 64 lowercase hex digits")
    return value


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    verifier = subparsers.add_parser("verify", help="verify a JSON queen witness")
    verifier.add_argument("witness", type=Path)

    encoder = subparsers.add_parser("encode", help="write a deterministic DIMACS CNF")
    encoder.add_argument("--board-size", type=int, default=Q26_BOARD_SIZE)
    encoder.add_argument("--limit", type=int, default=Q26_TARGET)
    encoder.add_argument("--encoding", choices=("direct", "line"), required=True)
    encoder.add_argument(
        "--ordering",
        choices=("row-major", "hilbert", "domination-degree"),
        default="hilbert",
    )
    encoder.add_argument("--no-line-bound", action="store_true")
    encoder.add_argument("--line-mode", choices=("exact", "supported"), default="exact")
    encoder.add_argument("--q26-structural", action="store_true")
    encoder.add_argument("--d4-lex", action="store_true")
    encoder.add_argument("--output", type=Path, required=True)

    opb_encoder = subparsers.add_parser(
        "encode-opb", help="write an independent deterministic direct OPB instance"
    )
    opb_encoder.add_argument("--board-size", type=int, default=Q26_BOARD_SIZE)
    opb_encoder.add_argument("--limit", type=int, default=Q26_TARGET)
    opb_encoder.add_argument("--output", type=Path, required=True)

    model = subparsers.add_parser(
        "decode-model", help="decode positive DIMACS literals and verify the witness"
    )
    model.add_argument("--board-size", type=int, default=Q26_BOARD_SIZE)
    model.add_argument("--limit", type=int, default=Q26_TARGET)
    model.add_argument("--model", type=Path, required=True)
    model.add_argument(
        "--instance-sha256",
        required=True,
        help="SHA-256 of the exact solver input that produced the model",
    )
    model.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "verify":
            board_size, limit, queens, source = load_witness(args.witness)
            result = verify_witness(board_size, limit, queens)
            if result != verify_witness_by_lines(board_size, limit, queens):
                raise QueenDominationError("independent witness checkers disagree")
            result["source"] = source
            sys.stdout.buffer.write(_canonical_json(result))
            return 0

        if args.command == "encode":
            cnf = build_cnf(
                args.board_size,
                args.limit,
                args.encoding,
                args.d4_lex,
                args.ordering,
                not args.no_line_bound,
                args.line_mode,
                args.q26_structural,
            )
            data = dimacs_bytes(
                cnf,
                args.board_size,
                args.limit,
                args.encoding,
                args.d4_lex,
                args.ordering,
                not args.no_line_bound,
                args.line_mode,
                args.q26_structural,
            )
            _write_new_file(args.output, data)
            print(
                json.dumps(
                    {
                        "board_size": args.board_size,
                        "clauses": len(cnf.clauses),
                        "encoding": args.encoding,
                        "limit": args.limit,
                        "line_bound": not args.no_line_bound and args.encoding == "line",
                        "line_mode": args.line_mode if args.encoding == "line" else None,
                        "ordering": args.ordering,
                        "q26_structural": args.q26_structural,
                        "sha256": hashlib.sha256(data).hexdigest(),
                        "symmetry_breaking": args.d4_lex,
                        "variables": cnf.variable_count,
                    },
                    sort_keys=True,
                )
            )
            return 0

        if args.command == "encode-opb":
            data = opb_bytes(args.board_size, args.limit)
            _write_new_file(args.output, data)
            print(
                json.dumps(
                    {
                        "board_size": args.board_size,
                        "constraints": args.board_size * args.board_size + 1,
                        "encoding": "direct-opb",
                        "limit": args.limit,
                        "sha256": hashlib.sha256(data).hexdigest(),
                        "variables": args.board_size * args.board_size,
                    },
                    sort_keys=True,
                )
            )
            return 0

        if args.command == "decode-model":
            model_bytes = args.model.read_bytes()
            integers = parse_solver_model(model_bytes.decode("ascii", errors="strict"))
            queens = decode_model(args.board_size, integers)
            result = verify_witness(args.board_size, args.limit, queens)
            if result != verify_witness_by_lines(args.board_size, args.limit, queens):
                raise QueenDominationError("independent witness checkers disagree")
            result["report_type"] = "verified_solver_model"
            result["source_model_bytes"] = len(model_bytes)
            result["source_model_sha256"] = hashlib.sha256(model_bytes).hexdigest()
            result["source_instance_sha256"] = _validated_sha256(
                args.instance_sha256
            )
            _write_new_file(args.output, _canonical_json(result))
            return 0
    except (OSError, UnicodeError, ValueError, QueenDominationError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    raise AssertionError("unreachable command")


if __name__ == "__main__":
    raise SystemExit(main())
