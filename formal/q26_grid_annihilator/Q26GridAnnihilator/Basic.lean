import Mathlib.Combinatorics.Nullstellensatz

/-!
# Q26 board semantics and the occurrence polynomial

This file fixes the board convention and proves the geometric vanishing
lemma used by the color-split argument.  Coordinates are the one-based
integers `1, ..., 26`; diagonal subtraction is therefore integer
subtraction, never truncated natural subtraction.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

abbrev Line := Fin 26
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

def Dominates (queens : Finset Square) : Prop :=
  ∀ target : Square, ∃ queen ∈ queens, Attacks queen target

def EmptyRow (queens : Finset Square) (row : Line) : Prop :=
  ∀ queen ∈ queens, queen.1 ≠ row

def EmptyColumn (queens : Finset Square) (column : Line) : Prop :=
  ∀ queen ∈ queens, queen.2 ≠ column

/-- An empty-row/empty-column square in a dominated board must be covered
diagonally. -/
theorem diagonal_cover_of_empty
    {queens : Finset Square} (hdom : Dominates queens)
    {row column : Line} (hrow : EmptyRow queens row)
    (hcolumn : EmptyColumn queens column) :
    ∃ queen ∈ queens, DiagonalAttack queen (row, column) := by
  obtain ⟨queen, hqueen, hattack⟩ := hdom (row, column)
  refine ⟨queen, hqueen, ?_⟩
  rcases hattack with hsameRow | hsameColumn | hdiagonal
  · exact False.elim (hrow queen hqueen hsameRow)
  · exact False.elim (hcolumn queen hqueen hsameColumn)
  · exact hdiagonal

abbrev Bivariate := MvPolynomial (Fin 2) ℚ

def U : Bivariate := MvPolynomial.X 0
def V : Bivariate := MvPolynomial.X 1

def rationalCoord (line : Line) : ℚ := coord line

/-- One paired difference/sum factor, indexed by a queen occurrence. -/
def occurrenceFactor (queen : Square) : Bivariate :=
  (U - V - MvPolynomial.C (rationalCoord queen.1 - rationalCoord queen.2)) *
  (U + V - MvPolynomial.C (rationalCoord queen.1 + rationalCoord queen.2))

/-- The product deliberately ranges over queen occurrences.  Repeated
diagonal labels therefore remain repeated factors. -/
def occurrencePolynomial (queens : Finset Square) : Bivariate :=
  ∏ queen ∈ queens, occurrenceFactor queen

def evaluationPoint (row column : Line) : Fin 2 → ℚ :=
  fun index => if index = 0 then rationalCoord row else rationalCoord column

@[simp] theorem evaluationPoint_zero (row column : Line) :
    evaluationPoint row column 0 = rationalCoord row := by
  simp [evaluationPoint]

@[simp] theorem evaluationPoint_one (row column : Line) :
    evaluationPoint row column 1 = rationalCoord column := by
  simp [evaluationPoint]

theorem eval_occurrenceFactor
    (queen : Square) (row column : Line) :
    MvPolynomial.eval (evaluationPoint row column) (occurrenceFactor queen) =
      (rationalCoord row - rationalCoord column -
          (rationalCoord queen.1 - rationalCoord queen.2)) *
        (rationalCoord row + rationalCoord column -
          (rationalCoord queen.1 + rationalCoord queen.2)) := by
  simp [occurrenceFactor, U, V]

theorem eval_occurrenceFactor_eq_zero_of_diagonal
    {queen : Square} {row column : Line}
    (hdiagonal : DiagonalAttack queen (row, column)) :
    MvPolynomial.eval (evaluationPoint row column) (occurrenceFactor queen) = 0 := by
  rw [eval_occurrenceFactor]
  rcases hdiagonal with hdifference | hsum
  · apply mul_eq_zero_of_left
    simp only [rationalCoord]
    have hzero :
        coord row - coord column - (coord queen.1 - coord queen.2) = 0 :=
      sub_eq_zero.mpr (by simpa using hdifference.symm)
    exact_mod_cast hzero
  · apply mul_eq_zero_of_right
    simp only [rationalCoord]
    have hzero :
        coord row + coord column - (coord queen.1 + coord queen.2) = 0 :=
      sub_eq_zero.mpr (by simpa using hsum.symm)
    exact_mod_cast hzero

/-- Abstract same-color empty-core annihilation.  The caller supplies the
diagonal-cover fact for the selected queen occurrences; no distinctness of
their diagonal labels is required. -/
theorem occurrence_eval_eq_zero
    {queens : Finset Square} {row column : Line}
    (hcover : ∃ queen ∈ queens, DiagonalAttack queen (row, column)) :
    MvPolynomial.eval (evaluationPoint row column)
        (occurrencePolynomial queens) = 0 := by
  obtain ⟨queen, hqueen, hdiagonal⟩ := hcover
  simp only [occurrencePolynomial, MvPolynomial.eval_prod]
  apply Finset.prod_eq_zero hqueen
  exact eval_occurrenceFactor_eq_zero_of_diagonal hdiagonal

end

end Q26GridAnnihilator
