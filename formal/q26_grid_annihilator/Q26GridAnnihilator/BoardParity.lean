import Q26GridAnnihilator.ColorBridge

/-!
# Exact row/column parity supports of an actual queen set

This module contains the finite-set bookkeeping needed to map an actual
thirteen-queen set to the numerical shadow.  It does not use domination or
any polynomial theorem: occupied parity-line supports are literal coordinate
images of the corresponding queen subsets, and empty supports are their
complements among the thirteen board lines of that parity.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

def linesOfParity (parity : ℤ) : Finset Line :=
  Finset.univ.filter fun line => coord line % 2 = parity

def queensInRowsOfParity (queens : Finset Square) (parity : ℤ) : Finset Square :=
  queens.filter fun queen => coord queen.1 % 2 = parity

def queensInColumnsOfParity
    (queens : Finset Square) (parity : ℤ) : Finset Square :=
  queens.filter fun queen => coord queen.2 % 2 = parity

def queensOfLineParities
    (queens : Finset Square) (rowParity columnParity : ℤ) : Finset Square :=
  queens.filter fun queen =>
    coord queen.1 % 2 = rowParity ∧ coord queen.2 % 2 = columnParity

def occupiedRowsOfParity (queens : Finset Square) (parity : ℤ) : Finset Line :=
  (queensInRowsOfParity queens parity).image fun queen => queen.1

def occupiedColumnsOfParity
    (queens : Finset Square) (parity : ℤ) : Finset Line :=
  (queensInColumnsOfParity queens parity).image fun queen => queen.2

@[simp] theorem mem_linesOfParity {line : Line} {parity : ℤ} :
    line ∈ linesOfParity parity ↔ coord line % 2 = parity := by
  simp [linesOfParity]

@[simp] theorem mem_queensInRowsOfParity
    {queens : Finset Square} {queen : Square} {parity : ℤ} :
    queen ∈ queensInRowsOfParity queens parity ↔
      queen ∈ queens ∧ coord queen.1 % 2 = parity := by
  simp [queensInRowsOfParity]

@[simp] theorem mem_queensInColumnsOfParity
    {queens : Finset Square} {queen : Square} {parity : ℤ} :
    queen ∈ queensInColumnsOfParity queens parity ↔
      queen ∈ queens ∧ coord queen.2 % 2 = parity := by
  simp [queensInColumnsOfParity]

@[simp] theorem mem_queensOfLineParities
    {queens : Finset Square} {queen : Square} {rowParity columnParity : ℤ} :
    queen ∈ queensOfLineParities queens rowParity columnParity ↔
      queen ∈ queens ∧ coord queen.1 % 2 = rowParity ∧
        coord queen.2 % 2 = columnParity := by
  simp [queensOfLineParities]

theorem coord_parity_zero_or_one (line : Line) :
    coord line % 2 = 0 ∨ coord line % 2 = 1 := by
  have nonnegative : 0 ≤ coord line % 2 := Int.emod_nonneg _ (by omega)
  have below : coord line % 2 < 2 := Int.emod_lt_of_pos _ (by omega)
  omega

theorem checkerColor_eq_zero_iff_same_parity (queen : Square) :
    checkerColor queen = 0 ↔ coord queen.1 % 2 = coord queen.2 % 2 := by
  constructor
  · intro colorZero
    unfold checkerColor at colorZero
    rw [Int.add_emod] at colorZero
    have rowParity := coord_parity_zero_or_one queen.1
    have columnParity := coord_parity_zero_or_one queen.2
    rcases rowParity with rowZero | rowOne <;>
      rcases columnParity with columnZero | columnOne <;> omega
  · exact checkerColor_eq_zero_of_same_lineParity

theorem checkerColor_eq_one_iff_opposite_parity (queen : Square) :
    checkerColor queen = 1 ↔ coord queen.1 % 2 ≠ coord queen.2 % 2 := by
  constructor
  · intro colorOne sameParity
    have colorZero := checkerColor_eq_zero_of_same_lineParity sameParity
    rw [colorZero] at colorOne
    norm_num at colorOne
  · exact checkerColor_eq_one_of_opposite_lineParity

theorem checkerColor_zero_or_one (queen : Square) :
    checkerColor queen = 0 ∨ checkerColor queen = 1 := by
  unfold checkerColor
  have nonnegative : 0 ≤ (coord queen.1 + coord queen.2) % 2 :=
    Int.emod_nonneg _ (by omega)
  have below : (coord queen.1 + coord queen.2) % 2 < 2 :=
    Int.emod_lt_of_pos _ (by omega)
  omega

theorem rowParityCells_union
    (queens : Finset Square) (rowParity : ℤ) :
    queensOfLineParities queens rowParity 0 ∪
        queensOfLineParities queens rowParity 1 =
      queensInRowsOfParity queens rowParity := by
  ext queen
  simp only [Finset.mem_union, mem_queensOfLineParities,
    mem_queensInRowsOfParity]
  constructor
  · rintro (⟨queenIn, rowAtParity, _columnZero⟩ |
      ⟨queenIn, rowAtParity, _columnOne⟩)
    all_goals exact ⟨queenIn, rowAtParity⟩
  · rintro ⟨queenIn, rowAtParity⟩
    rcases coord_parity_zero_or_one queen.2 with columnZero | columnOne
    · exact Or.inl ⟨queenIn, rowAtParity, columnZero⟩
    · exact Or.inr ⟨queenIn, rowAtParity, columnOne⟩

theorem columnParityCells_union
    (queens : Finset Square) (columnParity : ℤ) :
    queensOfLineParities queens 0 columnParity ∪
        queensOfLineParities queens 1 columnParity =
      queensInColumnsOfParity queens columnParity := by
  ext queen
  simp only [Finset.mem_union, mem_queensOfLineParities,
    mem_queensInColumnsOfParity]
  constructor
  · rintro (⟨queenIn, _rowZero, columnAtParity⟩ |
      ⟨queenIn, _rowOne, columnAtParity⟩)
    all_goals exact ⟨queenIn, columnAtParity⟩
  · rintro ⟨queenIn, columnAtParity⟩
    rcases coord_parity_zero_or_one queen.1 with rowZero | rowOne
    · exact Or.inl ⟨queenIn, rowZero, columnAtParity⟩
    · exact Or.inr ⟨queenIn, rowOne, columnAtParity⟩

theorem lineParityCells_disjoint_columns
    (queens : Finset Square) (rowParity : ℤ) :
    Disjoint (queensOfLineParities queens rowParity 0)
      (queensOfLineParities queens rowParity 1) := by
  rw [Finset.disjoint_left]
  intro queen queenInZero queenInOne
  have columnZero := (mem_queensOfLineParities.mp queenInZero).2.2
  have columnOne := (mem_queensOfLineParities.mp queenInOne).2.2
  omega

theorem lineParityCells_disjoint_rows
    (queens : Finset Square) (columnParity : ℤ) :
    Disjoint (queensOfLineParities queens 0 columnParity)
      (queensOfLineParities queens 1 columnParity) := by
  rw [Finset.disjoint_left]
  intro queen queenInZero queenInOne
  have rowZero := (mem_queensOfLineParities.mp queenInZero).2.1
  have rowOne := (mem_queensOfLineParities.mp queenInOne).2.1
  omega

theorem rowParityCell_cards
    (queens : Finset Square) (rowParity : ℤ) :
    (queensOfLineParities queens rowParity 0).card +
        (queensOfLineParities queens rowParity 1).card =
      (queensInRowsOfParity queens rowParity).card := by
  rw [← Finset.card_union_of_disjoint
    (lineParityCells_disjoint_columns queens rowParity), rowParityCells_union]

theorem columnParityCell_cards
    (queens : Finset Square) (columnParity : ℤ) :
    (queensOfLineParities queens 0 columnParity).card +
        (queensOfLineParities queens 1 columnParity).card =
      (queensInColumnsOfParity queens columnParity).card := by
  rw [← Finset.card_union_of_disjoint
    (lineParityCells_disjoint_rows queens columnParity), columnParityCells_union]

theorem queensOfColor_zero_eq_parityCells (queens : Finset Square) :
    queensOfColor queens 0 =
      queensOfLineParities queens 0 0 ∪ queensOfLineParities queens 1 1 := by
  ext queen
  simp only [mem_queensOfColor, Finset.mem_union, mem_queensOfLineParities]
  constructor
  · rintro ⟨queenIn, colorZero⟩
    have sameParity := (checkerColor_eq_zero_iff_same_parity queen).mp colorZero
    rcases coord_parity_zero_or_one queen.1 with rowZero | rowOne
    · exact Or.inl ⟨queenIn, rowZero, by omega⟩
    · exact Or.inr ⟨queenIn, rowOne, by omega⟩
  · rintro (⟨queenIn, rowZero, columnZero⟩ |
      ⟨queenIn, rowOne, columnOne⟩)
    all_goals
      refine ⟨queenIn, (checkerColor_eq_zero_iff_same_parity queen).mpr ?_⟩
      omega

theorem queensOfColor_one_eq_parityCells (queens : Finset Square) :
    queensOfColor queens 1 =
      queensOfLineParities queens 0 1 ∪ queensOfLineParities queens 1 0 := by
  ext queen
  simp only [mem_queensOfColor, Finset.mem_union, mem_queensOfLineParities]
  constructor
  · rintro ⟨queenIn, colorOne⟩
    have opposite := (checkerColor_eq_one_iff_opposite_parity queen).mp colorOne
    rcases coord_parity_zero_or_one queen.1 with rowZero | rowOne <;>
      rcases coord_parity_zero_or_one queen.2 with columnZero | columnOne
    · omega
    · exact Or.inl ⟨queenIn, rowZero, columnOne⟩
    · exact Or.inr ⟨queenIn, rowOne, columnZero⟩
    · omega
  · rintro (⟨queenIn, rowZero, columnOne⟩ |
      ⟨queenIn, rowOne, columnZero⟩)
    all_goals
      refine ⟨queenIn, (checkerColor_eq_one_iff_opposite_parity queen).mpr ?_⟩
      omega

theorem colorZeroParityCells_disjoint (queens : Finset Square) :
    Disjoint (queensOfLineParities queens 0 0)
      (queensOfLineParities queens 1 1) := by
  rw [Finset.disjoint_left]
  intro queen queenInZero queenInOne
  have rowZero := (mem_queensOfLineParities.mp queenInZero).2.1
  have rowOne := (mem_queensOfLineParities.mp queenInOne).2.1
  omega

theorem colorOneParityCells_disjoint (queens : Finset Square) :
    Disjoint (queensOfLineParities queens 0 1)
      (queensOfLineParities queens 1 0) := by
  rw [Finset.disjoint_left]
  intro queen queenInZero queenInOne
  have rowZero := (mem_queensOfLineParities.mp queenInZero).2.1
  have rowOne := (mem_queensOfLineParities.mp queenInOne).2.1
  omega

theorem colorZeroParityCell_cards (queens : Finset Square) :
    (queensOfLineParities queens 0 0).card +
        (queensOfLineParities queens 1 1).card =
      (queensOfColor queens 0).card := by
  rw [← Finset.card_union_of_disjoint (colorZeroParityCells_disjoint queens),
    ← queensOfColor_zero_eq_parityCells]

theorem colorOneParityCell_cards (queens : Finset Square) :
    (queensOfLineParities queens 0 1).card +
        (queensOfLineParities queens 1 0).card =
      (queensOfColor queens 1).card := by
  rw [← Finset.card_union_of_disjoint (colorOneParityCells_disjoint queens),
    ← queensOfColor_one_eq_parityCells]

theorem colorClasses_union (queens : Finset Square) :
    queensOfColor queens 0 ∪ queensOfColor queens 1 = queens := by
  ext queen
  simp only [Finset.mem_union, mem_queensOfColor]
  constructor
  · rintro (⟨queenIn, _colorZero⟩ | ⟨queenIn, _colorOne⟩)
    all_goals exact queenIn
  · intro queenIn
    rcases checkerColor_zero_or_one queen with colorZero | colorOne
    · exact Or.inl ⟨queenIn, colorZero⟩
    · exact Or.inr ⟨queenIn, colorOne⟩

theorem colorClasses_disjoint (queens : Finset Square) :
    Disjoint (queensOfColor queens 0) (queensOfColor queens 1) := by
  rw [Finset.disjoint_left]
  intro queen queenInZero queenInOne
  have colorZero := (mem_queensOfColor.mp queenInZero).2
  have colorOne := (mem_queensOfColor.mp queenInOne).2
  rw [colorZero] at colorOne
  norm_num at colorOne

theorem colorClass_cards (queens : Finset Square) :
    (queensOfColor queens 0).card + (queensOfColor queens 1).card = queens.card := by
  rw [← Finset.card_union_of_disjoint (colorClasses_disjoint queens), colorClasses_union]

theorem rowParityClasses_union (queens : Finset Square) :
    queensInRowsOfParity queens 0 ∪ queensInRowsOfParity queens 1 = queens := by
  ext queen
  simp only [Finset.mem_union, mem_queensInRowsOfParity]
  constructor
  · rintro (⟨queenIn, _rowZero⟩ | ⟨queenIn, _rowOne⟩)
    all_goals exact queenIn
  · intro queenIn
    rcases coord_parity_zero_or_one queen.1 with rowZero | rowOne
    · exact Or.inl ⟨queenIn, rowZero⟩
    · exact Or.inr ⟨queenIn, rowOne⟩

theorem rowParityClasses_disjoint (queens : Finset Square) :
    Disjoint (queensInRowsOfParity queens 0) (queensInRowsOfParity queens 1) := by
  rw [Finset.disjoint_left]
  intro queen queenInZero queenInOne
  have rowZero := (mem_queensInRowsOfParity.mp queenInZero).2
  have rowOne := (mem_queensInRowsOfParity.mp queenInOne).2
  omega

theorem rowParityClass_cards (queens : Finset Square) :
    (queensInRowsOfParity queens 0).card +
        (queensInRowsOfParity queens 1).card = queens.card := by
  rw [← Finset.card_union_of_disjoint (rowParityClasses_disjoint queens),
    rowParityClasses_union]

theorem lineParityCell_total_card (queens : Finset Square) :
    (queensOfLineParities queens 0 0).card +
        (queensOfLineParities queens 0 1).card +
        (queensOfLineParities queens 1 0).card +
        (queensOfLineParities queens 1 1).card = queens.card := by
  have evenRows := rowParityCell_cards queens 0
  have oddRows := rowParityCell_cards queens 1
  have allRows := rowParityClass_cards queens
  omega

theorem oddRowQueens_color_zero (queens : Finset Square) :
    oddRowQueens (queensOfColor queens 0) =
      queensOfLineParities queens 1 1 := by
  ext queen
  simp only [oddRowQueens, Finset.mem_filter, mem_queensOfColor,
    mem_queensOfLineParities]
  constructor
  · rintro ⟨⟨queenIn, colorZero⟩, rowOdd⟩
    have sameParity :=
      (checkerColor_eq_zero_iff_same_parity queen).mp colorZero
    exact ⟨queenIn, rowOdd, by omega⟩
  · rintro ⟨queenIn, rowOdd, columnOdd⟩
    exact ⟨⟨queenIn,
      (checkerColor_eq_zero_iff_same_parity queen).mpr (by omega)⟩, rowOdd⟩

theorem oddRowQueens_color_one (queens : Finset Square) :
    oddRowQueens (queensOfColor queens 1) =
      queensOfLineParities queens 1 0 := by
  ext queen
  simp only [oddRowQueens, Finset.mem_filter, mem_queensOfColor,
    mem_queensOfLineParities]
  constructor
  · rintro ⟨⟨queenIn, colorOne⟩, rowOdd⟩
    have opposite :=
      (checkerColor_eq_one_iff_opposite_parity queen).mp colorOne
    rcases coord_parity_zero_or_one queen.2 with columnEven | columnOdd
    · exact ⟨queenIn, rowOdd, columnEven⟩
    · exact False.elim (opposite (by omega))
  · rintro ⟨queenIn, rowOdd, columnEven⟩
    exact ⟨⟨queenIn,
      (checkerColor_eq_one_iff_opposite_parity queen).mpr (by omega)⟩, rowOdd⟩

theorem mem_occupiedRowsOfParity
    {queens : Finset Square} {row : Line} {parity : ℤ} :
    row ∈ occupiedRowsOfParity queens parity ↔
      ∃ queen ∈ queens, coord queen.1 % 2 = parity ∧ queen.1 = row := by
  constructor
  · intro membership
    rw [occupiedRowsOfParity, Finset.mem_image] at membership
    obtain ⟨queen, queenIn, rfl⟩ := membership
    exact ⟨queen, (mem_queensInRowsOfParity.mp queenIn).1,
      (mem_queensInRowsOfParity.mp queenIn).2, rfl⟩
  · rintro ⟨queen, queenIn, queenParity, rfl⟩
    rw [occupiedRowsOfParity, Finset.mem_image]
    exact ⟨queen, mem_queensInRowsOfParity.mpr ⟨queenIn, queenParity⟩, rfl⟩

theorem mem_occupiedColumnsOfParity
    {queens : Finset Square} {column : Line} {parity : ℤ} :
    column ∈ occupiedColumnsOfParity queens parity ↔
      ∃ queen ∈ queens, coord queen.2 % 2 = parity ∧ queen.2 = column := by
  constructor
  · intro membership
    rw [occupiedColumnsOfParity, Finset.mem_image] at membership
    obtain ⟨queen, queenIn, rfl⟩ := membership
    exact ⟨queen, (mem_queensInColumnsOfParity.mp queenIn).1,
      (mem_queensInColumnsOfParity.mp queenIn).2, rfl⟩
  · rintro ⟨queen, queenIn, queenParity, rfl⟩
    rw [occupiedColumnsOfParity, Finset.mem_image]
    exact ⟨queen, mem_queensInColumnsOfParity.mpr ⟨queenIn, queenParity⟩, rfl⟩

theorem occupiedRowsOfParity_subset_linesOfParity
    (queens : Finset Square) (parity : ℤ) :
    occupiedRowsOfParity queens parity ⊆ linesOfParity parity := by
  intro row rowIn
  obtain ⟨queen, _queenIn, queenParity, rowEquality⟩ :=
    mem_occupiedRowsOfParity.mp rowIn
  rw [← rowEquality]
  exact mem_linesOfParity.mpr queenParity

theorem occupiedColumnsOfParity_subset_linesOfParity
    (queens : Finset Square) (parity : ℤ) :
    occupiedColumnsOfParity queens parity ⊆ linesOfParity parity := by
  intro column columnIn
  obtain ⟨queen, _queenIn, queenParity, columnEquality⟩ :=
    mem_occupiedColumnsOfParity.mp columnIn
  rw [← columnEquality]
  exact mem_linesOfParity.mpr queenParity

theorem emptyRowsOfParity_eq_sdiff
    (queens : Finset Square) (parity : ℤ) :
    emptyRowsOfParity queens parity =
      linesOfParity parity \ occupiedRowsOfParity queens parity := by
  ext row
  constructor
  · intro rowIn
    have emptyAndParity := mem_emptyRowsOfParity.mp rowIn
    rw [Finset.mem_sdiff]
    refine ⟨mem_linesOfParity.mpr emptyAndParity.2, ?_⟩
    intro occupied
    obtain ⟨queen, queenIn, _queenParity, queenRow⟩ :=
      mem_occupiedRowsOfParity.mp occupied
    exact emptyAndParity.1 queen queenIn queenRow
  · intro rowIn
    rw [Finset.mem_sdiff] at rowIn
    apply mem_emptyRowsOfParity.mpr
    refine ⟨?_, (mem_linesOfParity.mp rowIn.1)⟩
    intro queen queenIn queenRow
    apply rowIn.2
    apply mem_occupiedRowsOfParity.mpr
    exact ⟨queen, queenIn, by simpa [queenRow] using mem_linesOfParity.mp rowIn.1,
      queenRow⟩

theorem emptyColumnsOfParity_eq_sdiff
    (queens : Finset Square) (parity : ℤ) :
    emptyColumnsOfParity queens parity =
      linesOfParity parity \ occupiedColumnsOfParity queens parity := by
  ext column
  constructor
  · intro columnIn
    have emptyAndParity := mem_emptyColumnsOfParity.mp columnIn
    rw [Finset.mem_sdiff]
    refine ⟨mem_linesOfParity.mpr emptyAndParity.2, ?_⟩
    intro occupied
    obtain ⟨queen, queenIn, _queenParity, queenColumn⟩ :=
      mem_occupiedColumnsOfParity.mp occupied
    exact emptyAndParity.1 queen queenIn queenColumn
  · intro columnIn
    rw [Finset.mem_sdiff] at columnIn
    apply mem_emptyColumnsOfParity.mpr
    refine ⟨?_, (mem_linesOfParity.mp columnIn.1)⟩
    intro queen queenIn queenColumn
    apply columnIn.2
    apply mem_occupiedColumnsOfParity.mpr
    exact ⟨queen, queenIn,
      by simpa [queenColumn] using mem_linesOfParity.mp columnIn.1, queenColumn⟩

theorem emptyRows_card_add_occupiedRows_card
    (queens : Finset Square) (parity : ℤ) :
    (emptyRowsOfParity queens parity).card +
        (occupiedRowsOfParity queens parity).card =
      (linesOfParity parity).card := by
  rw [emptyRowsOfParity_eq_sdiff]
  exact Finset.card_sdiff_add_card_eq_card
    (occupiedRowsOfParity_subset_linesOfParity queens parity)

theorem emptyColumns_card_add_occupiedColumns_card
    (queens : Finset Square) (parity : ℤ) :
    (emptyColumnsOfParity queens parity).card +
        (occupiedColumnsOfParity queens parity).card =
      (linesOfParity parity).card := by
  rw [emptyColumnsOfParity_eq_sdiff]
  exact Finset.card_sdiff_add_card_eq_card
    (occupiedColumnsOfParity_subset_linesOfParity queens parity)

theorem linesOfParity_zero_card : (linesOfParity 0).card = 13 := by
  decide

theorem linesOfParity_one_card : (linesOfParity 1).card = 13 := by
  decide

theorem emptyRows_zero_card_eq_half_sub_occupied (queens : Finset Square) :
    (emptyRowsOfParity queens 0).card =
      13 - (occupiedRowsOfParity queens 0).card := by
  have partition := emptyRows_card_add_occupiedRows_card queens 0
  rw [linesOfParity_zero_card] at partition
  omega

theorem emptyRows_one_card_eq_half_sub_occupied (queens : Finset Square) :
    (emptyRowsOfParity queens 1).card =
      13 - (occupiedRowsOfParity queens 1).card := by
  have partition := emptyRows_card_add_occupiedRows_card queens 1
  rw [linesOfParity_one_card] at partition
  omega

theorem emptyColumns_zero_card_eq_half_sub_occupied (queens : Finset Square) :
    (emptyColumnsOfParity queens 0).card =
      13 - (occupiedColumnsOfParity queens 0).card := by
  have partition := emptyColumns_card_add_occupiedColumns_card queens 0
  rw [linesOfParity_zero_card] at partition
  omega

theorem emptyColumns_one_card_eq_half_sub_occupied (queens : Finset Square) :
    (emptyColumnsOfParity queens 1).card =
      13 - (occupiedColumnsOfParity queens 1).card := by
  have partition := emptyColumns_card_add_occupiedColumns_card queens 1
  rw [linesOfParity_one_card] at partition
  omega

theorem occupiedRows_card_le_queenIncidences
    (queens : Finset Square) (parity : ℤ) :
    (occupiedRowsOfParity queens parity).card ≤
      (queensInRowsOfParity queens parity).card := by
  exact Finset.card_image_le

theorem occupiedColumns_card_le_queenIncidences
    (queens : Finset Square) (parity : ℤ) :
    (occupiedColumnsOfParity queens parity).card ≤
      (queensInColumnsOfParity queens parity).card := by
  exact Finset.card_image_le

theorem occupiedRows_card_eq_zero_iff_queenIncidences
    (queens : Finset Square) (parity : ℤ) :
    (occupiedRowsOfParity queens parity).card = 0 ↔
      (queensInRowsOfParity queens parity).card = 0 := by
  simp [occupiedRowsOfParity]

theorem occupiedColumns_card_eq_zero_iff_queenIncidences
    (queens : Finset Square) (parity : ℤ) :
    (occupiedColumnsOfParity queens parity).card = 0 ↔
      (queensInColumnsOfParity queens parity).card = 0 := by
  simp [occupiedColumnsOfParity]

end

end Q26GridAnnihilator
