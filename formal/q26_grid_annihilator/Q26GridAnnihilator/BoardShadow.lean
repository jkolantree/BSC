import Q26GridAnnihilator.ArbitraryCardinality
import Q26GridAnnihilator.BoardParity
import Q26GridAnnihilator.Shadow

/-!
# Mapping an actual thirteen-queen board to the unrestricted parity shadow

The numerical enumeration in `Shadow` is useful only after every actual
dominating set has been shown to land inside it.  This module constructs the
literal shadow of a queen set and proves the local incidence and all four
color-grid CN obligations.  List-membership and the final classification are
kept as separate theorems so that the semantic bridge cannot be hidden inside
the finite computation.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

def actualShadowQTable (queens : Finset Square) : ShadowQTable where
  q00 := (queensOfLineParities queens 0 0).card
  q01 := (queensOfLineParities queens 0 1).card
  q10 := (queensOfLineParities queens 1 0).card
  q11 := (queensOfLineParities queens 1 1).card

def actualCoarseShadow (queens : Finset Square) : CoarseShadow where
  color0 := (queensOfColor queens 0).card
  rows :=
    { even := (occupiedRowsOfParity queens 0).card
      odd := (occupiedRowsOfParity queens 1).card }
  columns :=
    { even := (occupiedColumnsOfParity queens 0).card
      odd := (occupiedColumnsOfParity queens 1).card }

def actualShadow (queens : Finset Square) : Shadow where
  coarse := actualCoarseShadow queens
  table := actualShadowQTable queens

@[simp] theorem actualShadow_color0 (queens : Finset Square) :
    (actualShadow queens).coarse.color0 = (queensOfColor queens 0).card := rfl

@[simp] theorem actualShadow_emptyRowsEven (queens : Finset Square) :
    (actualShadow queens).coarse.rows.emptyEven =
      (emptyRowsOfParity queens 0).card := by
  simpa [actualShadow, actualCoarseShadow, ShadowSupport.emptyEven,
    shadowBoardHalf] using (emptyRows_zero_card_eq_half_sub_occupied queens).symm

@[simp] theorem actualShadow_emptyRowsOdd (queens : Finset Square) :
    (actualShadow queens).coarse.rows.emptyOdd =
      (emptyRowsOfParity queens 1).card := by
  simpa [actualShadow, actualCoarseShadow, ShadowSupport.emptyOdd,
    shadowBoardHalf] using (emptyRows_one_card_eq_half_sub_occupied queens).symm

@[simp] theorem actualShadow_emptyColumnsEven (queens : Finset Square) :
    (actualShadow queens).coarse.columns.emptyEven =
      (emptyColumnsOfParity queens 0).card := by
  simpa [actualShadow, actualCoarseShadow, ShadowSupport.emptyEven,
    shadowBoardHalf] using
      (emptyColumns_zero_card_eq_half_sub_occupied queens).symm

@[simp] theorem actualShadow_emptyColumnsOdd (queens : Finset Square) :
    (actualShadow queens).coarse.columns.emptyOdd =
      (emptyColumnsOfParity queens 1).card := by
  simpa [actualShadow, actualCoarseShadow, ShadowSupport.emptyOdd,
    shadowBoardHalf] using
      (emptyColumns_one_card_eq_half_sub_occupied queens).symm

@[simp] theorem actualShadow_q00 (queens : Finset Square) :
    (actualShadow queens).table.q00 =
      (queensOfLineParities queens 0 0).card := rfl

@[simp] theorem actualShadow_q01 (queens : Finset Square) :
    (actualShadow queens).table.q01 =
      (queensOfLineParities queens 0 1).card := rfl

@[simp] theorem actualShadow_q10 (queens : Finset Square) :
    (actualShadow queens).table.q10 =
      (queensOfLineParities queens 1 0).card := rfl

@[simp] theorem actualShadow_q11 (queens : Finset Square) :
    (actualShadow queens).table.q11 =
      (queensOfLineParities queens 1 1).card := rfl

@[simp] theorem actualShadowQTable_color0 (queens : Finset Square) :
    (actualShadowQTable queens).color0 = (queensOfColor queens 0).card := by
  exact colorZeroParityCell_cards queens

@[simp] theorem actualShadowQTable_rowEven (queens : Finset Square) :
    (actualShadowQTable queens).rowEven =
      (queensInRowsOfParity queens 0).card := by
  exact rowParityCell_cards queens 0

@[simp] theorem actualShadowQTable_rowOdd (queens : Finset Square) :
    (actualShadowQTable queens).rowOdd =
      (queensInRowsOfParity queens 1).card := by
  exact rowParityCell_cards queens 1

@[simp] theorem actualShadowQTable_columnEven (queens : Finset Square) :
    (actualShadowQTable queens).columnEven =
      (queensInColumnsOfParity queens 0).card := by
  exact columnParityCell_cards queens 0

@[simp] theorem actualShadowQTable_columnOdd (queens : Finset Square) :
    (actualShadowQTable queens).columnOdd =
      (queensInColumnsOfParity queens 1).card := by
  exact columnParityCell_cards queens 1

theorem actualShadowQTable_total (queens : Finset Square) :
    (actualShadowQTable queens).q00 + (actualShadowQTable queens).q01 +
        (actualShadowQTable queens).q10 + (actualShadowQTable queens).q11 =
      queens.card := by
  exact lineParityCell_total_card queens

private theorem shadowSupportValid_of_card_facts
    (support occurrences : Nat)
    (zeroIff : support = 0 ↔ occurrences = 0)
    (cardBound : support ≤ occurrences) :
    shadowSupportValid support occurrences = true := by
  rw [shadowSupportValid, decide_eq_true_eq]
  by_cases occurrencesZero : occurrences = 0
  · exact Or.inl ⟨occurrencesZero, zeroIff.mpr occurrencesZero⟩
  · apply Or.inr
    have supportNonzero : support ≠ 0 := by
      intro supportZero
      exact occurrencesZero (zeroIff.mp supportZero)
    omega

theorem actualRowSupportValid
    (queens : Finset Square) (parity : ℤ) :
    shadowSupportValid (occupiedRowsOfParity queens parity).card
        (queensInRowsOfParity queens parity).card = true := by
  apply shadowSupportValid_of_card_facts
  · exact occupiedRows_card_eq_zero_iff_queenIncidences queens parity
  · exact occupiedRows_card_le_queenIncidences queens parity

theorem actualColumnSupportValid
    (queens : Finset Square) (parity : ℤ) :
    shadowSupportValid (occupiedColumnsOfParity queens parity).card
        (queensInColumnsOfParity queens parity).card = true := by
  apply shadowSupportValid_of_card_facts
  · exact occupiedColumns_card_eq_zero_iff_queenIncidences queens parity
  · exact occupiedColumns_card_le_queenIncidences queens parity

theorem actualShadowTableFits (queens : Finset Square) :
    shadowTableFits (actualCoarseShadow queens) (actualShadowQTable queens) = true := by
  simp [shadowTableFits,
    actualShadowQTable_color0, actualShadowQTable_rowEven,
    actualShadowQTable_rowOdd, actualShadowQTable_columnEven,
    actualShadowQTable_columnOdd, actualCoarseShadow,
    actualRowSupportValid, actualColumnSupportValid]

theorem shadowCNGridOK_of_alternatives
    (rowCount columnCount queenCount : Nat)
    (rowAtMostHalf : rowCount ≤ shadowBoardHalf)
    (columnAtMostHalf : columnCount ≤ shadowBoardHalf)
    (queensAtMostHalf : queenCount ≤ shadowBoardHalf)
    (alternatives : ∀ j ≤ queenCount,
      rowCount ≤ 2 * (queenCount - j) ∨ columnCount ≤ 2 * j) :
    shadowCNGridOK rowCount columnCount queenCount = true := by
  have literal :
      shadowCNGridAlternatives rowCount columnCount queenCount = true := by
    rw [shadowCNGridAlternatives, List.all_eq_true]
    intro j jIn
    rw [decide_eq_true_eq]
    exact alternatives j (by
      rw [List.mem_range] at jIn
      omega)
  have allRows := shadow_cn_forms_agree
  rw [shadowCNFormsAgree, List.all_eq_true] at allRows
  have allColumns := allRows rowCount (by
    rw [List.mem_range]
    omega)
  rw [List.all_eq_true] at allColumns
  have allQueens := allColumns columnCount (by
    rw [List.mem_range]
    omega)
  rw [List.all_eq_true] at allQueens
  have forms := allQueens queenCount (by
    rw [List.mem_range]
    omega)
  rw [decide_eq_true_eq] at forms
  rw [forms, literal]

private theorem actualColorGridCN
    (queens : Finset Square) (color : ℤ)
    (rows columns : Finset Line)
    (rowAtMostHalf : rows.card ≤ shadowBoardHalf)
    (columnAtMostHalf : columns.card ≤ shadowBoardHalf)
    (queensAtMostHalf : (queensOfColor queens color).card ≤ shadowBoardHalf)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (evaluationPoint row column)
        (occurrencePolynomial (queensOfColor queens color)) = 0) :
    shadowCNGridOK rows.card columns.card
        (queensOfColor queens color).card = true := by
  apply shadowCNGridOK_of_alternatives
  · exact rowAtMostHalf
  · exact columnAtMostHalf
  · exact queensAtMostHalf
  have alternatives := occurrence_grid_alternatives_card
    (queensOfColor queens color) (rationalLineSet rows)
    (rationalLineSet columns)
    (occurrence_vanishes_on_rationalLineSets
      (queensOfColor queens color) rows columns vanishes)
  intro j hj
  simpa using alternatives j hj

theorem actualColorZeroEvenGridCN
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13) :
    shadowCNGridOK (emptyRowsOfParity queens 0).card
        (emptyColumnsOfParity queens 0).card
        (queensOfColor queens 0).card = true := by
  apply actualColorGridCN queens 0
  · rw [shadowBoardHalf, emptyRows_zero_card_eq_half_sub_occupied]
    omega
  · rw [shadowBoardHalf, emptyColumns_zero_card_eq_half_sub_occupied]
    omega
  · have subset : queensOfColor queens 0 ⊆ queens := by
      intro queen queenIn
      exact (mem_queensOfColor.mp queenIn).1
    have bound := Finset.card_le_card subset
    rw [cardThirteen] at bound
    simpa [shadowBoardHalf] using bound
  exact occurrence_color_zero_vanishes_on_same_parity_empty_grid dominates 0

theorem actualColorZeroOddGridCN
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13) :
    shadowCNGridOK (emptyRowsOfParity queens 1).card
        (emptyColumnsOfParity queens 1).card
        (queensOfColor queens 0).card = true := by
  apply actualColorGridCN queens 0
  · rw [shadowBoardHalf, emptyRows_one_card_eq_half_sub_occupied]
    omega
  · rw [shadowBoardHalf, emptyColumns_one_card_eq_half_sub_occupied]
    omega
  · have subset : queensOfColor queens 0 ⊆ queens := by
      intro queen queenIn
      exact (mem_queensOfColor.mp queenIn).1
    have bound := Finset.card_le_card subset
    rw [cardThirteen] at bound
    simpa [shadowBoardHalf] using bound
  exact occurrence_color_zero_vanishes_on_same_parity_empty_grid dominates 1

theorem actualColorOneEvenOddGridCN
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13) :
    shadowCNGridOK (emptyRowsOfParity queens 0).card
        (emptyColumnsOfParity queens 1).card
        (queensOfColor queens 1).card = true := by
  apply actualColorGridCN queens 1
  · rw [shadowBoardHalf, emptyRows_zero_card_eq_half_sub_occupied]
    omega
  · rw [shadowBoardHalf, emptyColumns_one_card_eq_half_sub_occupied]
    omega
  · have subset : queensOfColor queens 1 ⊆ queens := by
      intro queen queenIn
      exact (mem_queensOfColor.mp queenIn).1
    have bound := Finset.card_le_card subset
    rw [cardThirteen] at bound
    simpa [shadowBoardHalf] using bound
  exact occurrence_color_one_vanishes_on_opposite_parity_empty_grid
    (queens := queens) dominates (rowParity := 0) (columnParity := 1) (by norm_num)

theorem actualColorOneOddEvenGridCN
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13) :
    shadowCNGridOK (emptyRowsOfParity queens 1).card
        (emptyColumnsOfParity queens 0).card
        (queensOfColor queens 1).card = true := by
  apply actualColorGridCN queens 1
  · rw [shadowBoardHalf, emptyRows_one_card_eq_half_sub_occupied]
    omega
  · rw [shadowBoardHalf, emptyColumns_zero_card_eq_half_sub_occupied]
    omega
  · have subset : queensOfColor queens 1 ⊆ queens := by
      intro queen queenIn
      exact (mem_queensOfColor.mp queenIn).1
    have bound := Finset.card_le_card subset
    rw [cardThirteen] at bound
    simpa [shadowBoardHalf] using bound
  exact occurrence_color_one_vanishes_on_opposite_parity_empty_grid
    (queens := queens) dominates (rowParity := 1) (columnParity := 0) (by norm_num)

theorem actualCoarseShadowCNOK
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13) :
    coarseShadowCNOK (actualCoarseShadow queens) = true := by
  have colorCards := colorClass_cards queens
  rw [cardThirteen] at colorCards
  simp only [coarseShadowCNOK, actualCoarseShadow, ShadowSupport.emptyEven,
    ShadowSupport.emptyOdd, CoarseShadow.color1, shadowBoardHalf,
    Bool.and_eq_true]
  rw [← emptyRows_zero_card_eq_half_sub_occupied,
    ← emptyRows_one_card_eq_half_sub_occupied,
    ← emptyColumns_zero_card_eq_half_sub_occupied,
    ← emptyColumns_one_card_eq_half_sub_occupied]
  have colorOneCard : 13 - (queensOfColor queens 0).card =
      (queensOfColor queens 1).card := by omega
  rw [colorOneCard]
  exact ⟨⟨⟨actualColorZeroEvenGridCN queens dominates cardThirteen,
    actualColorZeroOddGridCN queens dominates cardThirteen⟩,
    actualColorOneEvenOddGridCN queens dominates cardThirteen⟩,
    actualColorOneOddEvenGridCN queens dominates cardThirteen⟩

theorem actualRowSupportPair_mem
    (queens : Finset Square) (cardThirteen : queens.card = 13) :
    (actualCoarseShadow queens).rows ∈ shadowSupportPairs := by
  rw [mem_shadowSupportPairs_iff]
  simp only [actualCoarseShadow, shadowBoardHalf]
  have evenBound := occupiedRows_card_le_queenIncidences queens 0
  have oddBound := occupiedRows_card_le_queenIncidences queens 1
  have partition := rowParityClass_cards queens
  rw [cardThirteen] at partition
  omega

theorem actualColumnSupportPair_mem
    (queens : Finset Square) (cardThirteen : queens.card = 13) :
    (actualCoarseShadow queens).columns ∈ shadowSupportPairs := by
  rw [mem_shadowSupportPairs_iff]
  simp only [actualCoarseShadow, shadowBoardHalf]
  have evenBound := occupiedColumns_card_le_queenIncidences queens 0
  have oddBound := occupiedColumns_card_le_queenIncidences queens 1
  have evenCells := columnParityCell_cards queens 0
  have oddCells := columnParityCell_cards queens 1
  have totalCells := lineParityCell_total_card queens
  rw [cardThirteen] at totalCells
  omega

theorem actualShadowQTable_mem
    (queens : Finset Square) (cardThirteen : queens.card = 13) :
    actualShadowQTable queens ∈ shadowQTables := by
  rw [mem_shadowQTables_iff]
  simpa [shadowBoardHalf, cardThirteen] using actualShadowQTable_total queens

theorem actualCoarseShadow_mem
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13) :
    actualCoarseShadow queens ∈ coarseShadowSurvivors := by
  rw [coarseShadowSurvivors, List.mem_flatMap]
  refine ⟨(queensOfColor queens 0).card, ?_, ?_⟩
  · simp only [List.mem_range, shadowBoardHalf]
    have colorBound : (queensOfColor queens 0).card ≤ queens.card :=
      Finset.card_filter_le _ _
    omega
  · rw [List.mem_flatMap]
    refine ⟨(actualCoarseShadow queens).rows,
      actualRowSupportPair_mem queens cardThirteen, ?_⟩
    rw [List.mem_map]
    refine ⟨(actualCoarseShadow queens).columns, ?_, rfl⟩
    rw [List.mem_filter]
    exact ⟨actualColumnSupportPair_mem queens cardThirteen,
      actualCoarseShadowCNOK queens dominates cardThirteen⟩

theorem actualShadow_mem_shadowsFor (queens : Finset Square)
    (cardThirteen : queens.card = 13) :
    actualShadow queens ∈ shadowsFor (actualCoarseShadow queens) := by
  rw [shadowsFor, List.mem_map]
  refine ⟨actualShadowQTable queens, ?_, rfl⟩
  rw [List.mem_filter]
  exact ⟨actualShadowQTable_mem queens cardThirteen,
    actualShadowTableFits queens⟩

/-- The actual parity summary of every thirteen-queen dominator is one of the
thirty-six finite shadows classified in `Shadow`. -/
theorem actualShadow_mem_rawShadows
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13) :
    actualShadow queens ∈ rawShadows := by
  rw [rawShadows, List.mem_flatMap]
  exact ⟨actualCoarseShadow queens,
    actualCoarseShadow_mem queens dominates cardThirteen,
    actualShadow_mem_shadowsFor queens cardThirteen⟩

/-- Exact unrestricted arithmetic dichotomy for an actual thirteen-queen
dominator.  Neither side has been excluded here. -/
theorem actualShadow_recipe
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13) :
    (actualShadow queens).monochromaticStandard = true ∨
      (actualShadow queens).bichromaticCore = true :=
  mem_rawShadows_recipe
    (actualShadow_mem_rawShadows queens dominates cardThirteen)

end


end Q26GridAnnihilator
