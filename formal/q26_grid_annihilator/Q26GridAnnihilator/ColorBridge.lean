import Q26GridAnnihilator.CoordinateSets

/-!
# Checkerboard-color geometry

Diagonal attack preserves checkerboard color.  Therefore, on a square whose
row and column are empty, domination by the full queen set turns into
diagonal cover by the matching color class.  This is the geometric bridge
used by all four occurrence-polynomial grids.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

def checkerColor (square : Square) : ℤ :=
  (coord square.1 + coord square.2) % 2

def queensOfColor (queens : Finset Square) (color : ℤ) : Finset Square :=
  queens.filter fun queen => checkerColor queen = color

def emptyRowsOfParity (queens : Finset Square) (parity : ℤ) : Finset Line := by
  classical
  exact Finset.univ.filter fun row =>
    EmptyRow queens row ∧ coord row % 2 = parity

def emptyColumnsOfParity (queens : Finset Square) (parity : ℤ) : Finset Line := by
  classical
  exact Finset.univ.filter fun column =>
    EmptyColumn queens column ∧ coord column % 2 = parity

@[simp] theorem mem_queensOfColor
    {queens : Finset Square} {color : ℤ} {queen : Square} :
    queen ∈ queensOfColor queens color ↔
      queen ∈ queens ∧ checkerColor queen = color := by
  simp [queensOfColor]

@[simp] theorem mem_emptyRowsOfParity
    {queens : Finset Square} {parity : ℤ} {row : Line} :
    row ∈ emptyRowsOfParity queens parity ↔
      EmptyRow queens row ∧ coord row % 2 = parity := by
  simp [emptyRowsOfParity]

@[simp] theorem mem_emptyColumnsOfParity
    {queens : Finset Square} {parity : ℤ} {column : Line} :
    column ∈ emptyColumnsOfParity queens parity ↔
      EmptyColumn queens column ∧ coord column % 2 = parity := by
  simp [emptyColumnsOfParity]

theorem checkerColor_eq_of_diagonalAttack
    {queen target : Square} (attack : DiagonalAttack queen target) :
    checkerColor queen = checkerColor target := by
  unfold checkerColor DiagonalAttack at *
  rcases attack with difference | sum
  · omega
  · omega

theorem checkerColor_eq_zero_of_same_lineParity
    {row column : Line}
    (sameParity : coord row % 2 = coord column % 2) :
    checkerColor (row, column) = 0 := by
  change (coord row + coord column) % 2 = 0
  rw [Int.add_emod]
  have rowNonnegative : 0 ≤ coord row % 2 := Int.emod_nonneg _ (by omega)
  have rowBelow : coord row % 2 < 2 := Int.emod_lt_of_pos _ (by omega)
  have columnNonnegative : 0 ≤ coord column % 2 := Int.emod_nonneg _ (by omega)
  have columnBelow : coord column % 2 < 2 := Int.emod_lt_of_pos _ (by omega)
  omega

theorem checkerColor_eq_one_of_opposite_lineParity
    {row column : Line}
    (oppositeParity : coord row % 2 ≠ coord column % 2) :
    checkerColor (row, column) = 1 := by
  change (coord row + coord column) % 2 = 1
  rw [Int.add_emod]
  have rowNonnegative : 0 ≤ coord row % 2 := Int.emod_nonneg _ (by omega)
  have rowBelow : coord row % 2 < 2 := Int.emod_lt_of_pos _ (by omega)
  have columnNonnegative : 0 ≤ coord column % 2 := Int.emod_nonneg _ (by omega)
  have columnBelow : coord column % 2 < 2 := Int.emod_lt_of_pos _ (by omega)
  omega

theorem occurrence_color_eval_eq_zero
    {queens : Finset Square} (dominates : Dominates queens)
    {color : ℤ} {row column : Line}
    (rowEmpty : EmptyRow queens row)
    (columnEmpty : EmptyColumn queens column)
    (targetColor : checkerColor (row, column) = color) :
    MvPolynomial.eval (evaluationPoint row column)
        (occurrencePolynomial (queensOfColor queens color)) = 0 := by
  apply occurrence_eval_eq_zero
  obtain ⟨queen, queenIn, diagonal⟩ :=
    diagonal_cover_of_empty dominates rowEmpty columnEmpty
  refine ⟨queen, ?_, diagonal⟩
  rw [mem_queensOfColor]
  exact ⟨queenIn, (checkerColor_eq_of_diagonalAttack diagonal).trans targetColor⟩

theorem occurrence_color_vanishes_on_empty_grid
    {queens : Finset Square} (dominates : Dominates queens)
    (color : ℤ) (rows columns : Finset Line)
    (rowsEmpty : ∀ row ∈ rows, EmptyRow queens row)
    (columnsEmpty : ∀ column ∈ columns, EmptyColumn queens column)
    (gridColor : ∀ row ∈ rows, ∀ column ∈ columns,
      checkerColor (row, column) = color) :
    ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (evaluationPoint row column)
        (occurrencePolynomial (queensOfColor queens color)) = 0 := by
  intro row rowIn column columnIn
  exact occurrence_color_eval_eq_zero dominates
    (rowsEmpty row rowIn) (columnsEmpty column columnIn)
    (gridColor row rowIn column columnIn)

theorem occurrence_color_zero_vanishes_on_same_parity_empty_grid
    {queens : Finset Square} (dominates : Dominates queens) (parity : ℤ) :
    ∀ row ∈ emptyRowsOfParity queens parity,
      ∀ column ∈ emptyColumnsOfParity queens parity,
        MvPolynomial.eval (evaluationPoint row column)
          (occurrencePolynomial (queensOfColor queens 0)) = 0 := by
  apply occurrence_color_vanishes_on_empty_grid dominates 0
  · intro row rowIn
    exact (mem_emptyRowsOfParity.mp rowIn).1
  · intro column columnIn
    exact (mem_emptyColumnsOfParity.mp columnIn).1
  · intro row rowIn column columnIn
    apply checkerColor_eq_zero_of_same_lineParity
    rw [(mem_emptyRowsOfParity.mp rowIn).2,
      (mem_emptyColumnsOfParity.mp columnIn).2]

theorem occurrence_color_one_vanishes_on_opposite_parity_empty_grid
    {queens : Finset Square} (dominates : Dominates queens)
    {rowParity columnParity : ℤ} (opposite : rowParity ≠ columnParity) :
    ∀ row ∈ emptyRowsOfParity queens rowParity,
      ∀ column ∈ emptyColumnsOfParity queens columnParity,
        MvPolynomial.eval (evaluationPoint row column)
          (occurrencePolynomial (queensOfColor queens 1)) = 0 := by
  apply occurrence_color_vanishes_on_empty_grid dominates 1
  · intro row rowIn
    exact (mem_emptyRowsOfParity.mp rowIn).1
  · intro column columnIn
    exact (mem_emptyColumnsOfParity.mp columnIn).1
  · intro row rowIn column columnIn
    apply checkerColor_eq_one_of_opposite_lineParity
    rw [(mem_emptyRowsOfParity.mp rowIn).2,
      (mem_emptyColumnsOfParity.mp columnIn).2]
    exact opposite

end

end Q26GridAnnihilator
