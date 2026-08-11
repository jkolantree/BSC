import Q26GridAnnihilator.BichromaticRecipe
import Q26GridAnnihilator.BoardShadow
import Q26GridAnnihilator.GridMoment

/-!
# Closing the bichromatic parity shadows

The finite classifier supplies one of two row-based recipes.  This module
binds those recipes back to the actual empty-line sets, uses domination to
obtain polynomial vanishing, and applies the checked moment identities.  No
symmetry transport or five-profile bridge is used.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

private theorem closeStandardRow
    (sixQueens : Finset Square) (queenCard : sixQueens.card = 6)
    (rows columns : Finset Line) (rowCard : rows.card = 6)
    (columnCard : columns.card = 7 ∨ columns.card = 8)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (evaluationPoint row column)
        (occurrencePolynomial sixQueens) = 0)
    (oddRowsCard : (oddRowQueens sixQueens).card = 3)
    (rowSumEven : lineSumInt rows % 2 = 0) : False := by
  have rationalVanishes := occurrence_vanishes_on_rationalLineSets
    sixQueens rows columns vanishes
  have moment :
      6 * queenRowSum sixQueens =
        6 * ∑ row ∈ rationalLineSet rows, row := by
    rcases columnCard with columnSeven | columnEight
    · exact occurrence_six_row_moment_6_7 sixQueens queenCard
        (rationalLineSet rows) (rationalLineSet columns)
        (by simpa using rowCard) (by simpa using columnSeven) rationalVanishes
    · exact occurrence_six_row_moment_6_8 sixQueens queenCard
        (rationalLineSet rows) (rationalLineSet columns)
        (by simpa using rowCard) (by simpa using columnEight) rationalVanishes
  rw [queenRowSum_eq_intCast, rationalLineSet_sum] at moment
  have momentInt :
      6 * queenRowSumInt sixQueens = 6 * lineSumInt rows := by
    exact_mod_cast moment
  have queenParity := queenRowSumInt_mod_two sixQueens
  rw [oddRowsCard] at queenParity
  norm_num at queenParity
  omega

private theorem closeExceptionalRow
    (sixQueens sevenQueens : Finset Square)
    (sixCard : sixQueens.card = 6) (sevenCard : sevenQueens.card = 7)
    (rows smallColumns eightColumns : Finset Line)
    (rowCard : rows.card = 8)
    (smallCard : smallColumns.card = 5 ∨ smallColumns.card = 6)
    (eightCard : eightColumns.card = 8)
    (sixVanishes : ∀ row ∈ rows, ∀ column ∈ smallColumns,
      MvPolynomial.eval (evaluationPoint row column)
        (occurrencePolynomial sixQueens) = 0)
    (sevenVanishes : ∀ row ∈ rows, ∀ column ∈ eightColumns,
      MvPolynomial.eval (evaluationPoint row column)
        (occurrencePolynomial sevenQueens) = 0)
    (oddRowsCard : (oddRowQueens sixQueens).card = 3) : False := by
  have rationalSix := occurrence_vanishes_on_rationalLineSets
    sixQueens rows smallColumns sixVanishes
  have rationalSeven := occurrence_vanishes_on_rationalLineSets
    sevenQueens rows eightColumns sevenVanishes
  have sixMoment :
      8 * queenRowSum sixQueens =
        6 * ∑ row ∈ rationalLineSet rows, row := by
    rcases smallCard with columnFive | columnSix
    · exact occurrence_six_row_moment_8_5 sixQueens sixCard
        (rationalLineSet rows) (rationalLineSet smallColumns)
        (by simpa using rowCard) (by simpa using columnFive) rationalSix
    · exact occurrence_six_row_moment_8_6 sixQueens sixCard
        (rationalLineSet rows) (rationalLineSet smallColumns)
        (by simpa using rowCard) (by simpa using columnSix) rationalSix
  have sevenMoment := occurrence_seven_row_moment_8_8 sevenQueens sevenCard
    (rationalLineSet rows) (rationalLineSet eightColumns)
    (by simpa using rowCard) (by simpa using eightCard) rationalSeven
  rw [queenRowSum_eq_intCast, rationalLineSet_sum] at sixMoment sevenMoment
  have sixMomentInt :
      8 * queenRowSumInt sixQueens = 6 * lineSumInt rows := by
    exact_mod_cast sixMoment
  have sevenMomentInt :
      8 * queenRowSumInt sevenQueens = 7 * lineSumInt rows := by
    exact_mod_cast sevenMoment
  have queenParity := queenRowSumInt_mod_two sixQueens
  rw [oddRowsCard] at queenParity
  norm_num at queenParity
  omega

theorem no_bichromatic_actual_shadow
    (queens : Finset Square) (dominates : Dominates queens)
    (cardThirteen : queens.card = 13)
    (bichromatic : (actualShadow queens).bichromaticCore = true) : False := by
  have rawMember := actualShadow_mem_rawShadows queens dominates cardThirteen
  have recipe :=
    mem_rawShadows_bichromatic_obstruction rawMember bichromatic
  rcases recipe with standard | exceptional
  · simp only [Shadow.standardRowRecipe, actualShadow_color0,
      actualShadow_emptyRowsEven, actualShadow_emptyRowsOdd,
      actualShadow_emptyColumnsEven, actualShadow_emptyColumnsOdd,
      actualShadow_q10, actualShadow_q11, sevenOrEight] at standard
    rcases standard with colorZero | colorOne
    · rcases colorZero with ⟨colorZeroCard, q11Three, evenCase | oddCase⟩
      · rcases evenCase with ⟨rowCard, columnCard⟩
        apply closeStandardRow (queensOfColor queens 0) colorZeroCard
          (emptyRowsOfParity queens 0) (emptyColumnsOfParity queens 0)
          rowCard columnCard
          (occurrence_color_zero_vanishes_on_same_parity_empty_grid dominates 0)
        · rw [oddRowQueens_color_zero]
          exact q11Three
        · apply lineSumInt_even_of_six_even _ rowCard
          intro row rowIn
          exact (mem_emptyRowsOfParity.mp rowIn).2
      · rcases oddCase with ⟨rowCard, columnCard⟩
        apply closeStandardRow (queensOfColor queens 0) colorZeroCard
          (emptyRowsOfParity queens 1) (emptyColumnsOfParity queens 1)
          rowCard columnCard
          (occurrence_color_zero_vanishes_on_same_parity_empty_grid dominates 1)
        · rw [oddRowQueens_color_zero]
          exact q11Three
        · apply lineSumInt_even_of_six_odd _ rowCard
          intro row rowIn
          exact (mem_emptyRowsOfParity.mp rowIn).2
    · rcases colorOne with ⟨colorZeroCard, q10Three, parityCase⟩
      have colorCards := colorClass_cards queens
      rw [cardThirteen, colorZeroCard] at colorCards
      have colorOneCard : (queensOfColor queens 1).card = 6 := by omega
      rcases parityCase with evenCase | oddCase
      · rcases evenCase with ⟨rowCard, columnCard⟩
        apply closeStandardRow (queensOfColor queens 1) colorOneCard
          (emptyRowsOfParity queens 0) (emptyColumnsOfParity queens 1)
          rowCard columnCard
          (occurrence_color_one_vanishes_on_opposite_parity_empty_grid
            dominates (by norm_num))
        · rw [oddRowQueens_color_one]
          exact q10Three
        · apply lineSumInt_even_of_six_even _ rowCard
          intro row rowIn
          exact (mem_emptyRowsOfParity.mp rowIn).2
      · rcases oddCase with ⟨rowCard, columnCard⟩
        apply closeStandardRow (queensOfColor queens 1) colorOneCard
          (emptyRowsOfParity queens 1) (emptyColumnsOfParity queens 0)
          rowCard columnCard
          (occurrence_color_one_vanishes_on_opposite_parity_empty_grid
            dominates (by norm_num))
        · rw [oddRowQueens_color_one]
          exact q10Three
        · apply lineSumInt_even_of_six_odd _ rowCard
          intro row rowIn
          exact (mem_emptyRowsOfParity.mp rowIn).2
  · simp only [Shadow.exceptionalRowRecipe, actualShadow_color0,
      actualShadow_emptyRowsEven, actualShadow_emptyRowsOdd,
      actualShadow_emptyColumnsEven, actualShadow_emptyColumnsOdd,
      actualShadow_q10, actualShadow_q11, fiveOrSix] at exceptional
    rcases exceptional with colorZero | colorOne
    · rcases colorZero with ⟨colorZeroCard, q11Three, parityCase⟩
      have colorCards := colorClass_cards queens
      rw [cardThirteen, colorZeroCard] at colorCards
      have colorOneCard : (queensOfColor queens 1).card = 7 := by omega
      rcases parityCase with evenCase | oddCase
      · rcases evenCase with ⟨rowCard, smallCard, eightCard⟩
        apply closeExceptionalRow (queensOfColor queens 0)
          (queensOfColor queens 1) colorZeroCard colorOneCard
          (emptyRowsOfParity queens 0) (emptyColumnsOfParity queens 0)
          (emptyColumnsOfParity queens 1) rowCard smallCard eightCard
          (occurrence_color_zero_vanishes_on_same_parity_empty_grid dominates 0)
          (occurrence_color_one_vanishes_on_opposite_parity_empty_grid
            dominates (by norm_num))
        rw [oddRowQueens_color_zero]
        exact q11Three
      · rcases oddCase with ⟨rowCard, smallCard, eightCard⟩
        apply closeExceptionalRow (queensOfColor queens 0)
          (queensOfColor queens 1) colorZeroCard colorOneCard
          (emptyRowsOfParity queens 1) (emptyColumnsOfParity queens 1)
          (emptyColumnsOfParity queens 0) rowCard smallCard eightCard
          (occurrence_color_zero_vanishes_on_same_parity_empty_grid dominates 1)
          (occurrence_color_one_vanishes_on_opposite_parity_empty_grid
            dominates (by norm_num))
        rw [oddRowQueens_color_zero]
        exact q11Three
    · rcases colorOne with ⟨colorZeroCard, q10Three, parityCase⟩
      have colorCards := colorClass_cards queens
      rw [cardThirteen, colorZeroCard] at colorCards
      have colorOneCard : (queensOfColor queens 1).card = 6 := by omega
      rcases parityCase with evenCase | oddCase
      · rcases evenCase with ⟨rowCard, smallCard, eightCard⟩
        apply closeExceptionalRow (queensOfColor queens 1)
          (queensOfColor queens 0) colorOneCard colorZeroCard
          (emptyRowsOfParity queens 0) (emptyColumnsOfParity queens 1)
          (emptyColumnsOfParity queens 0) rowCard smallCard eightCard
          (occurrence_color_one_vanishes_on_opposite_parity_empty_grid
            dominates (by norm_num))
          (occurrence_color_zero_vanishes_on_same_parity_empty_grid dominates 0)
        rw [oddRowQueens_color_one]
        exact q10Three
      · rcases oddCase with ⟨rowCard, smallCard, eightCard⟩
        apply closeExceptionalRow (queensOfColor queens 1)
          (queensOfColor queens 0) colorOneCard colorZeroCard
          (emptyRowsOfParity queens 1) (emptyColumnsOfParity queens 0)
          (emptyColumnsOfParity queens 1) rowCard smallCard eightCard
          (occurrence_color_one_vanishes_on_opposite_parity_empty_grid
            dominates (by norm_num))
          (occurrence_color_zero_vanishes_on_same_parity_empty_grid dominates 1)
        rw [oddRowQueens_color_one]
        exact q10Three

end

end Q26GridAnnihilator
