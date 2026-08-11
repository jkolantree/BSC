import Q26GridAnnihilator.BoardShadow
import Q26GridAnnihilator.MonochromaticPermutation
import Q26GridAnnihilator.MonochromaticRecipe

/-!
# Actual-board bridge for the normalized monochromatic core

This module starts with the `q01` orientation: all thirteen queens occupy
even rows and odd columns.  The occupied-row and occupied-column cardinalities
make both coordinate projections bijections.  Their canonical one-based
coordinate indices therefore define the permutation used by
`MonoCoreCovered`.

No monochromatic impossibility theorem is claimed here.  The result only
constructs the normalized permutation and transports actual domination to its
opposite-parity `13 × 13` diagonal core.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

/-- The even board line with normalized one-based index `index + 1`. -/
def monoEvenLine (index : MonoIndex) : Line :=
  ⟨2 * index.val + 1, by omega⟩

/-- The odd board line with normalized one-based index `index + 1`. -/
def monoOddLine (index : MonoIndex) : Line :=
  ⟨2 * index.val, by omega⟩

@[simp] theorem coord_monoEvenLine (index : MonoIndex) :
    coord (monoEvenLine index) = 2 * monoCoord index := by
  simp only [coord, monoEvenLine, monoCoord]
  omega

@[simp] theorem coord_monoOddLine (index : MonoIndex) :
    coord (monoOddLine index) = 2 * monoCoord index - 1 := by
  simp only [coord, monoOddLine, monoCoord]
  omega

@[simp] theorem coord_monoEvenLine_mod_two (index : MonoIndex) :
    coord (monoEvenLine index) % 2 = 0 := by
  rw [coord_monoEvenLine]
  omega

@[simp] theorem coord_monoOddLine_mod_two (index : MonoIndex) :
    coord (monoOddLine index) % 2 = 1 := by
  rw [coord_monoOddLine]
  omega

abbrev MonoEvenBoardLine := {line : Line // coord line % 2 = 0}
abbrev MonoOddBoardLine := {line : Line // coord line % 2 = 1}

def monoEvenBoardLine (index : MonoIndex) : MonoEvenBoardLine :=
  ⟨monoEvenLine index, coord_monoEvenLine_mod_two index⟩

def monoOddBoardLine (index : MonoIndex) : MonoOddBoardLine :=
  ⟨monoOddLine index, coord_monoOddLine_mod_two index⟩

theorem monoEvenBoardLine_injective : Function.Injective monoEvenBoardLine := by
  intro left right equality
  have valueEquality :=
    congrArg (fun line : MonoEvenBoardLine => line.val.val) equality
  apply Fin.ext
  simp only [monoEvenBoardLine, monoEvenLine] at valueEquality
  omega

theorem monoOddBoardLine_injective : Function.Injective monoOddBoardLine := by
  intro left right equality
  have valueEquality :=
    congrArg (fun line : MonoOddBoardLine => line.val.val) equality
  apply Fin.ext
  simp only [monoOddBoardLine, monoOddLine] at valueEquality
  omega

theorem monoEvenBoardLine_bijective : Function.Bijective monoEvenBoardLine := by
  apply (Fintype.bijective_iff_injective_and_card monoEvenBoardLine).2
  exact ⟨monoEvenBoardLine_injective, by decide⟩

theorem monoOddBoardLine_bijective : Function.Bijective monoOddBoardLine := by
  apply (Fintype.bijective_iff_injective_and_card monoOddBoardLine).2
  exact ⟨monoOddBoardLine_injective, by decide⟩

noncomputable def monoEvenLineEquiv : MonoIndex ≃ MonoEvenBoardLine :=
  Equiv.ofBijective monoEvenBoardLine monoEvenBoardLine_bijective

noncomputable def monoOddLineEquiv : MonoIndex ≃ MonoOddBoardLine :=
  Equiv.ofBijective monoOddBoardLine monoOddBoardLine_bijective

/-- Reflection in the midpoint of the 26 board lines. -/
def monoReflectedLine (line : Line) : Line :=
  ⟨25 - line.val, by omega⟩

@[simp] theorem coord_monoReflectedLine (line : Line) :
    coord (monoReflectedLine line) = 27 - coord line := by
  simp only [coord, monoReflectedLine]
  omega

def monoReflectedEvenLine (index : MonoIndex) : Line :=
  monoReflectedLine (monoEvenLine index)

def monoReflectedOddLine (index : MonoIndex) : Line :=
  monoReflectedLine (monoOddLine index)

@[simp] theorem coord_monoReflectedEvenLine (index : MonoIndex) :
    coord (monoReflectedEvenLine index) = 27 - 2 * monoCoord index := by
  simp [monoReflectedEvenLine]

@[simp] theorem coord_monoReflectedOddLine (index : MonoIndex) :
    coord (monoReflectedOddLine index) = 28 - 2 * monoCoord index := by
  simp [monoReflectedOddLine]
  omega

@[simp] theorem coord_monoReflectedEvenLine_mod_two (index : MonoIndex) :
    coord (monoReflectedEvenLine index) % 2 = 1 := by
  rw [coord_monoReflectedEvenLine]
  omega

@[simp] theorem coord_monoReflectedOddLine_mod_two (index : MonoIndex) :
    coord (monoReflectedOddLine index) % 2 = 0 := by
  rw [coord_monoReflectedOddLine]
  omega

def monoReflectedEvenBoardLine (index : MonoIndex) : MonoOddBoardLine :=
  ⟨monoReflectedEvenLine index, coord_monoReflectedEvenLine_mod_two index⟩

def monoReflectedOddBoardLine (index : MonoIndex) : MonoEvenBoardLine :=
  ⟨monoReflectedOddLine index, coord_monoReflectedOddLine_mod_two index⟩

theorem monoReflectedEvenBoardLine_injective :
    Function.Injective monoReflectedEvenBoardLine := by
  intro left right equality
  have valueEquality :=
    congrArg (fun line : MonoOddBoardLine => line.val.val) equality
  apply Fin.ext
  simp only [monoReflectedEvenBoardLine, monoReflectedEvenLine,
    monoReflectedLine, monoEvenLine] at valueEquality
  omega

theorem monoReflectedOddBoardLine_injective :
    Function.Injective monoReflectedOddBoardLine := by
  intro left right equality
  have valueEquality :=
    congrArg (fun line : MonoEvenBoardLine => line.val.val) equality
  apply Fin.ext
  simp only [monoReflectedOddBoardLine, monoReflectedOddLine,
    monoReflectedLine, monoOddLine] at valueEquality
  omega

theorem monoReflectedEvenBoardLine_bijective :
    Function.Bijective monoReflectedEvenBoardLine := by
  apply (Fintype.bijective_iff_injective_and_card
    monoReflectedEvenBoardLine).2
  exact ⟨monoReflectedEvenBoardLine_injective, by decide⟩

theorem monoReflectedOddBoardLine_bijective :
    Function.Bijective monoReflectedOddBoardLine := by
  apply (Fintype.bijective_iff_injective_and_card
    monoReflectedOddBoardLine).2
  exact ⟨monoReflectedOddBoardLine_injective, by decide⟩

noncomputable def monoReflectedEvenLineEquiv :
    MonoIndex ≃ MonoOddBoardLine :=
  Equiv.ofBijective monoReflectedEvenBoardLine
    monoReflectedEvenBoardLine_bijective

noncomputable def monoReflectedOddLineEquiv :
    MonoIndex ≃ MonoEvenBoardLine :=
  Equiv.ofBijective monoReflectedOddBoardLine
    monoReflectedOddBoardLine_bijective

private theorem monoCoreCovered_of_orientationCards
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13)
    (rowParity columnParity : ℤ)
    (parityCellCard :
      (queensOfLineParities queens rowParity columnParity).card = 13)
    (occupiedRowCard : (occupiedRowsOfParity queens rowParity).card = 13)
    (occupiedColumnCard :
      (occupiedColumnsOfParity queens columnParity).card = 13)
    (rowLines : MonoIndex ≃ {line : Line // coord line % 2 = rowParity})
    (columnLines :
      MonoIndex ≃ {line : Line // coord line % 2 = columnParity})
    (targetRows targetColumns : MonoIndex → Line)
    (targetRowOpposite :
      ∀ index, coord (targetRows index) % 2 ≠ rowParity)
    (targetColumnOpposite :
      ∀ index, coord (targetColumns index) % 2 ≠ columnParity)
    (normalizes : ∀ queenRow queenColumn targetRow targetColumn,
      DiagonalAttack
          ((rowLines queenRow).val, (columnLines queenColumn).val)
          (targetRows targetRow, targetColumns targetColumn) →
        monoCoord targetRow - monoCoord targetColumn =
            monoCoord queenRow - monoCoord queenColumn + 1 ∨
          monoCoord targetRow + monoCoord targetColumn =
            monoCoord queenRow + monoCoord queenColumn) :
    ∃ permutation : MonoIndex ≃ MonoIndex, MonoCoreCovered permutation := by
  have parityCellSubset :
      queensOfLineParities queens rowParity columnParity ⊆ queens := by
    intro queen queenIn
    exact (mem_queensOfLineParities.mp queenIn).1
  have allInParityCell :
      queensOfLineParities queens rowParity columnParity = queens := by
    apply Finset.eq_of_subset_of_card_le parityCellSubset
    omega
  have queenParities {queen : Square} (queenIn : queen ∈ queens) :
      coord queen.1 % 2 = rowParity ∧
        coord queen.2 % 2 = columnParity := by
    have parityCell :
        queen ∈ queensOfLineParities queens rowParity columnParity := by
      rw [allInParityCell]
      exact queenIn
    exact (mem_queensOfLineParities.mp parityCell).2
  have rowParityQueens :
      queensInRowsOfParity queens rowParity = queens := by
    rw [queensInRowsOfParity]
    apply Finset.filter_true_of_mem
    intro queen queenIn
    exact (queenParities queenIn).1
  have columnParityQueens :
      queensInColumnsOfParity queens columnParity = queens := by
    rw [queensInColumnsOfParity]
    apply Finset.filter_true_of_mem
    intro queen queenIn
    exact (queenParities queenIn).2
  have rowImageCard :
      (queens.image fun queen => queen.1).card = queens.card := by
    calc
      (queens.image fun queen => queen.1).card =
          (occupiedRowsOfParity queens rowParity).card := by
            rw [occupiedRowsOfParity, rowParityQueens]
      _ = 13 := occupiedRowCard
      _ = queens.card := cardThirteen.symm
  have columnImageCard :
      (queens.image fun queen => queen.2).card = queens.card := by
    calc
      (queens.image fun queen => queen.2).card =
          (occupiedColumnsOfParity queens columnParity).card := by
            rw [occupiedColumnsOfParity, columnParityQueens]
      _ = 13 := occupiedColumnCard
      _ = queens.card := cardThirteen.symm
  have rowProjectionInjective : Function.Injective
      (fun queen : {queen // queen ∈ queens} => queen.val.1) := by
    intro left right rowEquality
    apply Subtype.ext
    exact Finset.injOn_of_card_image_eq rowImageCard
      left.property right.property rowEquality
  have columnProjectionInjective : Function.Injective
      (fun queen : {queen // queen ∈ queens} => queen.val.2) := by
    intro left right columnEquality
    apply Subtype.ext
    exact Finset.injOn_of_card_image_eq columnImageCard
      left.property right.property columnEquality
  let rowIndex : {queen // queen ∈ queens} → MonoIndex := fun queen =>
    rowLines.symm ⟨queen.val.1, (queenParities queen.property).1⟩
  let columnIndex : {queen // queen ∈ queens} → MonoIndex := fun queen =>
    columnLines.symm ⟨queen.val.2, (queenParities queen.property).2⟩
  have rowIndexInjective : Function.Injective rowIndex := by
    intro left right equality
    apply rowProjectionInjective
    dsimp [rowIndex] at equality
    have lineEquality :
        (⟨left.val.1, (queenParities left.property).1⟩ :
            {line : Line // coord line % 2 = rowParity}) =
          ⟨right.val.1, (queenParities right.property).1⟩ :=
      rowLines.symm.injective equality
    exact congrArg Subtype.val lineEquality
  have columnIndexInjective : Function.Injective columnIndex := by
    intro left right equality
    apply columnProjectionInjective
    dsimp [columnIndex] at equality
    have lineEquality :
        (⟨left.val.2, (queenParities left.property).2⟩ :
            {line : Line // coord line % 2 = columnParity}) =
          ⟨right.val.2, (queenParities right.property).2⟩ :=
      columnLines.symm.injective equality
    exact congrArg Subtype.val lineEquality
  have rowIndexBijective : Function.Bijective rowIndex := by
    apply (Fintype.bijective_iff_injective_and_card rowIndex).2
    exact ⟨rowIndexInjective, by simpa using cardThirteen⟩
  have columnIndexBijective : Function.Bijective columnIndex := by
    apply (Fintype.bijective_iff_injective_and_card columnIndex).2
    exact ⟨columnIndexInjective, by simpa using cardThirteen⟩
  let rowEquiv : {queen // queen ∈ queens} ≃ MonoIndex :=
    Equiv.ofBijective rowIndex rowIndexBijective
  let columnEquiv : {queen // queen ∈ queens} ≃ MonoIndex :=
    Equiv.ofBijective columnIndex columnIndexBijective
  have queenRow_normalized (queen : {queen // queen ∈ queens}) :
      queen.val.1 = (rowLines (rowEquiv queen)).val := by
    have applied := rowLines.apply_symm_apply
      ⟨queen.val.1, (queenParities queen.property).1⟩
    have values := congrArg Subtype.val applied
    change queen.val.1 = (rowLines (rowIndex queen)).val
    exact values.symm
  have queenColumn_normalized (queen : {queen // queen ∈ queens}) :
      queen.val.2 = (columnLines (columnEquiv queen)).val := by
    have applied := columnLines.apply_symm_apply
      ⟨queen.val.2, (queenParities queen.property).2⟩
    have values := congrArg Subtype.val applied
    change queen.val.2 = (columnLines (columnIndex queen)).val
    exact values.symm
  let permutation : MonoIndex ≃ MonoIndex := rowEquiv.symm.trans columnEquiv
  refine ⟨permutation, ?_⟩
  intro targetRow targetColumn
  have targetRowEmpty : EmptyRow queens (targetRows targetRow) := by
    intro queen queenIn rowEquality
    apply targetRowOpposite targetRow
    simpa [← rowEquality] using (queenParities queenIn).1
  have targetColumnEmpty : EmptyColumn queens (targetColumns targetColumn) := by
    intro queen queenIn columnEquality
    apply targetColumnOpposite targetColumn
    simpa [← columnEquality] using (queenParities queenIn).2
  obtain ⟨queen, queenIn, diagonal⟩ :=
    diagonal_cover_of_empty dominates targetRowEmpty targetColumnEmpty
  let actualQueen : {queen // queen ∈ queens} := ⟨queen, queenIn⟩
  let index : MonoIndex := rowEquiv actualQueen
  have permutationIndex : permutation index = columnEquiv actualQueen := by
    simp [permutation, index]
  have queenRow : queen.1 = (rowLines index).val := by
    exact queenRow_normalized actualQueen
  have queenColumn : queen.2 = (columnLines (permutation index)).val := by
    rw [permutationIndex]
    exact queenColumn_normalized actualQueen
  unfold DiagonalAttack at diagonal
  rw [queenRow, queenColumn] at diagonal
  refine ⟨index, ?_⟩
  rcases normalizes index (permutation index) targetRow targetColumn diagonal with
    difference | sum
  · left
    simpa [monoDifference] using difference
  · right
    simpa [monoSum] using sum

private theorem q01_diagonal_normalizes
    (queenRow queenColumn targetRow targetColumn : MonoIndex)
    (attack : DiagonalAttack
      (monoEvenLine queenRow, monoOddLine queenColumn)
      (monoOddLine targetRow, monoEvenLine targetColumn)) :
    monoCoord targetRow - monoCoord targetColumn =
        monoCoord queenRow - monoCoord queenColumn + 1 ∨
      monoCoord targetRow + monoCoord targetColumn =
        monoCoord queenRow + monoCoord queenColumn := by
  rcases attack with difference | sum
  · left
    simp only [coord_monoEvenLine, coord_monoOddLine] at difference
    omega
  · right
    simp only [coord_monoEvenLine, coord_monoOddLine] at sum
    omega

private theorem q10_diagonal_normalizes
    (queenRow queenColumn targetRow targetColumn : MonoIndex)
    (attack : DiagonalAttack
      (monoReflectedEvenLine queenRow, monoReflectedOddLine queenColumn)
      (monoReflectedOddLine targetRow,
        monoReflectedEvenLine targetColumn)) :
    monoCoord targetRow - monoCoord targetColumn =
        monoCoord queenRow - monoCoord queenColumn + 1 ∨
      monoCoord targetRow + monoCoord targetColumn =
        monoCoord queenRow + monoCoord queenColumn := by
  rcases attack with difference | sum
  · left
    simp only [coord_monoReflectedEvenLine,
      coord_monoReflectedOddLine] at difference
    omega
  · right
    simp only [coord_monoReflectedEvenLine,
      coord_monoReflectedOddLine] at sum
    omega

private theorem q11_diagonal_normalizes
    (queenRow queenColumn targetRow targetColumn : MonoIndex)
    (attack : DiagonalAttack
      (monoReflectedEvenLine queenRow, monoOddLine queenColumn)
      (monoReflectedOddLine targetRow, monoEvenLine targetColumn)) :
    monoCoord targetRow - monoCoord targetColumn =
        monoCoord queenRow - monoCoord queenColumn + 1 ∨
      monoCoord targetRow + monoCoord targetColumn =
        monoCoord queenRow + monoCoord queenColumn := by
  rcases attack with difference | sum
  · right
    simp only [coord_monoReflectedEvenLine,
      coord_monoReflectedOddLine, coord_monoEvenLine,
      coord_monoOddLine] at difference
    omega
  · left
    simp only [coord_monoReflectedEvenLine,
      coord_monoReflectedOddLine, coord_monoEvenLine,
      coord_monoOddLine] at sum
    omega

private theorem q00_diagonal_normalizes
    (queenRow queenColumn targetRow targetColumn : MonoIndex)
    (attack : DiagonalAttack
      (monoEvenLine queenRow, monoReflectedOddLine queenColumn)
      (monoOddLine targetRow, monoReflectedEvenLine targetColumn)) :
    monoCoord targetRow - monoCoord targetColumn =
        monoCoord queenRow - monoCoord queenColumn + 1 ∨
      monoCoord targetRow + monoCoord targetColumn =
        monoCoord queenRow + monoCoord queenColumn := by
  rcases attack with difference | sum
  · right
    simp only [coord_monoReflectedEvenLine,
      coord_monoReflectedOddLine, coord_monoEvenLine,
      coord_monoOddLine] at difference
    omega
  · left
    simp only [coord_monoReflectedEvenLine,
      coord_monoReflectedOddLine, coord_monoEvenLine,
      coord_monoOddLine] at sum
    omega

/-- An actual `q01` monochromatic orientation supplies the normalized
permutation whose opposite-parity core is diagonally covered. -/
theorem q01_actualShadow_monoCoreCovered
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13)
    (q01 : MonochromaticOrientation.q01.shadow = actualShadow queens) :
    ∃ permutation : MonoIndex ≃ MonoIndex, MonoCoreCovered permutation := by
  refine monoCoreCovered_of_orientationCards queens dominates cardThirteen 0 1
    ?_ ?_ ?_ monoEvenLineEquiv monoOddLineEquiv monoOddLine monoEvenLine
    ?_ ?_ q01_diagonal_normalizes
  · have equality := congrArg (fun shadow : Shadow => shadow.table.q01) q01
    simpa [MonochromaticOrientation.shadow] using equality.symm
  · have equality := congrArg (fun shadow : Shadow => shadow.coarse.rows.even) q01
    simpa [MonochromaticOrientation.shadow, actualShadow, actualCoarseShadow]
      using equality.symm
  · have equality := congrArg (fun shadow : Shadow => shadow.coarse.columns.odd) q01
    simpa [MonochromaticOrientation.shadow, actualShadow, actualCoarseShadow]
      using equality.symm
  · intro index
    simp
  · intro index
    simp

theorem q10_actualShadow_monoCoreCovered
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13)
    (q10 : MonochromaticOrientation.q10.shadow = actualShadow queens) :
    ∃ permutation : MonoIndex ≃ MonoIndex, MonoCoreCovered permutation := by
  refine monoCoreCovered_of_orientationCards queens dominates cardThirteen 1 0
    ?_ ?_ ?_ monoReflectedEvenLineEquiv monoReflectedOddLineEquiv
    monoReflectedOddLine monoReflectedEvenLine ?_ ?_ q10_diagonal_normalizes
  · have equality := congrArg (fun shadow : Shadow => shadow.table.q10) q10
    simpa [MonochromaticOrientation.shadow] using equality.symm
  · have equality := congrArg (fun shadow : Shadow => shadow.coarse.rows.odd) q10
    simpa [MonochromaticOrientation.shadow, actualShadow, actualCoarseShadow]
      using equality.symm
  · have equality := congrArg (fun shadow : Shadow => shadow.coarse.columns.even) q10
    simpa [MonochromaticOrientation.shadow, actualShadow, actualCoarseShadow]
      using equality.symm
  · intro index
    simp
  · intro index
    simp

theorem q11_actualShadow_monoCoreCovered
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13)
    (q11 : MonochromaticOrientation.q11.shadow = actualShadow queens) :
    ∃ permutation : MonoIndex ≃ MonoIndex, MonoCoreCovered permutation := by
  refine monoCoreCovered_of_orientationCards queens dominates cardThirteen 1 1
    ?_ ?_ ?_ monoReflectedEvenLineEquiv monoOddLineEquiv
    monoReflectedOddLine monoEvenLine ?_ ?_ q11_diagonal_normalizes
  · have equality := congrArg (fun shadow : Shadow => shadow.table.q11) q11
    simpa [MonochromaticOrientation.shadow] using equality.symm
  · have equality := congrArg (fun shadow : Shadow => shadow.coarse.rows.odd) q11
    simpa [MonochromaticOrientation.shadow, actualShadow, actualCoarseShadow]
      using equality.symm
  · have equality := congrArg (fun shadow : Shadow => shadow.coarse.columns.odd) q11
    simpa [MonochromaticOrientation.shadow, actualShadow, actualCoarseShadow]
      using equality.symm
  · intro index
    simp
  · intro index
    simp

theorem q00_actualShadow_monoCoreCovered
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13)
    (q00 : MonochromaticOrientation.q00.shadow = actualShadow queens) :
    ∃ permutation : MonoIndex ≃ MonoIndex, MonoCoreCovered permutation := by
  refine monoCoreCovered_of_orientationCards queens dominates cardThirteen 0 0
    ?_ ?_ ?_ monoEvenLineEquiv monoReflectedOddLineEquiv
    monoOddLine monoReflectedEvenLine ?_ ?_ q00_diagonal_normalizes
  · have equality := congrArg (fun shadow : Shadow => shadow.table.q00) q00
    simpa [MonochromaticOrientation.shadow] using equality.symm
  · have equality := congrArg (fun shadow : Shadow => shadow.coarse.rows.even) q00
    simpa [MonochromaticOrientation.shadow, actualShadow, actualCoarseShadow]
      using equality.symm
  · have equality := congrArg (fun shadow : Shadow => shadow.coarse.columns.even) q00
    simpa [MonochromaticOrientation.shadow, actualShadow, actualCoarseShadow]
      using equality.symm
  · intro index
    simp
  · intro index
    simp

/-- All four explicit monochromatic orientations normalize to the same
`MonoCoreCovered` interface. -/
theorem monochromaticOrientation_actualShadow_monoCoreCovered
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13)
    (orientation : MonochromaticOrientation)
    (shadowEquality : orientation.shadow = actualShadow queens) :
    ∃ permutation : MonoIndex ≃ MonoIndex, MonoCoreCovered permutation := by
  cases orientation with
  | q01 => exact q01_actualShadow_monoCoreCovered queens dominates cardThirteen shadowEquality
  | q10 => exact q10_actualShadow_monoCoreCovered queens dominates cardThirteen shadowEquality
  | q11 => exact q11_actualShadow_monoCoreCovered queens dominates cardThirteen shadowEquality
  | q00 => exact q00_actualShadow_monoCoreCovered queens dominates cardThirteen shadowEquality

/-- An actual monochromatic-standard thirteen-queen dominator has a checked
normalized diagonal-core permutation. -/
theorem monochromatic_actualShadow_monoCoreCovered
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13)
    (monochromatic : (actualShadow queens).monochromaticStandard = true) :
    ∃ permutation : MonoIndex ≃ MonoIndex, MonoCoreCovered permutation := by
  have rawMember := actualShadow_mem_rawShadows queens dominates cardThirteen
  obtain ⟨orientation, _orientationIn, shadowEquality⟩ :=
    mem_rawShadows_monochromatic_orientation rawMember monochromatic
  exact monochromaticOrientation_actualShadow_monoCoreCovered
    queens dominates cardThirteen orientation shadowEquality

end

end Q26GridAnnihilator
