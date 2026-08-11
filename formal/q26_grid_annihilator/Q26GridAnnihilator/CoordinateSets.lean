import Q26GridAnnihilator.MomentAlgebra

/-!
# Exact integer-to-rational coordinate bridges

The interpolation layer works over `ℚ`, while board parity lives in `ℤ`.
These lemmas bind the two representations without rounding or division.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

theorem coord_injective : Function.Injective coord := by
  intro left right equality
  apply Fin.ext
  simp only [coord] at equality
  omega

theorem rationalCoord_injective : Function.Injective rationalCoord := by
  intro left right equality
  apply coord_injective
  apply Int.cast_injective (α := ℚ)
  simpa only [rationalCoord] using equality

def rationalLineSet (lines : Finset Line) : Finset ℚ :=
  lines.image rationalCoord

@[simp] theorem rationalLineSet_card (lines : Finset Line) :
    (rationalLineSet lines).card = lines.card := by
  exact Finset.card_image_of_injective lines rationalCoord_injective

def lineSumInt (lines : Finset Line) : ℤ :=
  ∑ line ∈ lines, coord line

theorem rationalLineSet_sum (lines : Finset Line) :
    (∑ value ∈ rationalLineSet lines, value) = (lineSumInt lines : ℚ) := by
  rw [rationalLineSet, Finset.sum_image]
  · simp [lineSumInt, rationalCoord]
  · intro left leftIn right rightIn equality
    exact rationalCoord_injective equality

def queenRowSumInt (queens : Finset Square) : ℤ :=
  ∑ queen ∈ queens, coord queen.1

def queenColumnSumInt (queens : Finset Square) : ℤ :=
  ∑ queen ∈ queens, coord queen.2

theorem queenRowSum_eq_intCast (queens : Finset Square) :
    queenRowSum queens = (queenRowSumInt queens : ℚ) := by
  simp [queenRowSum, queenRowSumInt, rationalCoord]

theorem queenColumnSum_eq_intCast (queens : Finset Square) :
    queenColumnSum queens = (queenColumnSumInt queens : ℚ) := by
  simp [queenColumnSum, queenColumnSumInt, rationalCoord]

/-- The sum of exactly six odd integer line coordinates is even. -/
theorem lineSumInt_even_of_six_odd
    (lines : Finset Line) (cardExact : lines.card = 6)
    (allOdd : ∀ line ∈ lines, coord line % 2 = 1) :
    lineSumInt lines % 2 = 0 := by
  rw [lineSumInt, Finset.sum_int_mod]
  have residues :
      (∑ line ∈ lines, coord line % 2) =
        ∑ _line ∈ lines, (1 : ℤ) := by
    apply Finset.sum_congr rfl
    intro line lineIn
    rw [allOdd line lineIn]
  rw [residues]
  simp [cardExact]

/-- The sum of exactly six even integer line coordinates is even. -/
theorem lineSumInt_even_of_six_even
    (lines : Finset Line) (_cardExact : lines.card = 6)
    (allEven : ∀ line ∈ lines, coord line % 2 = 0) :
    lineSumInt lines % 2 = 0 := by
  rw [lineSumInt, Finset.sum_int_mod]
  have residues :
      (∑ line ∈ lines, coord line % 2) = 0 := by
    rw [Finset.sum_eq_zero]
    intro line lineIn
    exact allEven line lineIn
  rw [residues]
  norm_num

def oddRowQueens (queens : Finset Square) : Finset Square :=
  queens.filter fun queen => coord queen.1 % 2 = 1

/-- The parity of the integer row-coordinate sum is the parity of the number
of queens on odd-indexed rows. -/
theorem queenRowSumInt_mod_two (queens : Finset Square) :
    queenRowSumInt queens % 2 = ((oddRowQueens queens).card : ℤ) % 2 := by
  rw [queenRowSumInt, Finset.sum_int_mod]
  have residues :
      (∑ queen ∈ queens, coord queen.1 % 2) =
        ∑ queen ∈ queens,
          if coord queen.1 % 2 = 1 then (1 : ℤ) else 0 := by
    apply Finset.sum_congr rfl
    intro queen _queenIn
    by_cases odd : coord queen.1 % 2 = 1
    · simp [odd]
    · have nonnegative : 0 ≤ coord queen.1 % 2 := Int.emod_nonneg _ (by omega)
      have below : coord queen.1 % 2 < 2 := Int.emod_lt_of_pos _ (by omega)
      simp [odd]
      omega
  rw [residues]
  have indicator :
      (∑ queen ∈ queens,
          if coord queen.1 % 2 = 1 then (1 : ℤ) else 0) =
        ((oddRowQueens queens).card : ℤ) := by
    simp [oddRowQueens]
  rw [indicator]

theorem rationalPairPoint_coords_eq_evaluationPoint (row column : Line) :
    rationalPairPoint (rationalCoord row) (rationalCoord column) =
      evaluationPoint row column := by
  funext index
  fin_cases index <;> simp

theorem occurrence_vanishes_on_rationalLineSets
    (queens : Finset Square) (rows columns : Finset Line)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (evaluationPoint row column)
        (occurrencePolynomial queens) = 0) :
    ∀ row ∈ rationalLineSet rows, ∀ column ∈ rationalLineSet columns,
      MvPolynomial.eval (rationalPairPoint row column)
        (occurrencePolynomial queens) = 0 := by
  intro row rowIn column columnIn
  rw [rationalLineSet, Finset.mem_image] at rowIn columnIn
  obtain ⟨sourceRow, sourceRowIn, rfl⟩ := rowIn
  obtain ⟨sourceColumn, sourceColumnIn, rfl⟩ := columnIn
  rw [rationalPairPoint_coords_eq_evaluationPoint]
  exact vanishes sourceRow sourceRowIn sourceColumn sourceColumnIn

end

end Q26GridAnnihilator
