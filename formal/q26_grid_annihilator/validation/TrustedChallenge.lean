import Mathlib.Data.Finset.Card

set_option autoImplicit false

namespace Q26GridAnnihilator

/-- The verifier-controlled 26-element line type. -/
abbrev Line := Fin 26

/-- The verifier-controlled 26 by 26 board. -/
abbrev Square := Line × Line

/-- The one-based integer coordinate of a board line. -/
def coord (line : Line) : ℤ := line.val + 1

/-- Two squares share one of the two chess diagonals. -/
def DiagonalAttack (queen target : Square) : Prop :=
  coord queen.1 - coord queen.2 = coord target.1 - coord target.2 ∨
  coord queen.1 + coord queen.2 = coord target.1 + coord target.2

/-- Standard queen attack, including the occupied square itself. -/
def Attacks (queen target : Square) : Prop :=
  queen.1 = target.1 ∨ queen.2 = target.2 ∨ DiagonalAttack queen target

/-- Every board square is occupied by or attacked by one of the queens. -/
def Dominates (queens : Finset Square) : Prop :=
  ∀ target : Square, ∃ queen ∈ queens, Attacks queen target

/-- Verifier-controlled exact-cardinality obstruction. -/
theorem no_thirteen_queen_dominator :
    ¬ ∃ queens : Finset Square, Dominates queens ∧ queens.card = 13 := by
  sorry

/-- Verifier-controlled exact ordinary Q26 domination statement. -/
theorem q26_domination_exact :
    (∃ queens : Finset Square, Dominates queens ∧ queens.card = 14) ∧
      ∀ queens : Finset Square, Dominates queens → 14 ≤ queens.card := by
  sorry

end Q26GridAnnihilator
