import Q26GridAnnihilator.ColorBridge
import Q26GridAnnihilator.GridMoment
import Q26GridAnnihilator.Profiles

/-!
# Conditional assembly of the five canonical Q26 cases

This module does not formalize the cited Weakley reduction.  Its explicit
hypothesis is a canonical realization carrying exactly the cardinality and
parity-incidence consequences needed below.  All geometric vanishing,
polynomial moments, casts, finite profile classification, and final integer
contradictions are proved by the imported modules.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

structure WeakleyCanonicalRealization (profile : Profile) where
  queens : Finset Square
  dominates : Dominates queens
  lift : Lift
  liftFeasible : lift ∈ feasibleLifts profile.inventory profile.pair
  color0Card : (queensOfColor queens 0).card = 6
  color1Card : (queensOfColor queens 1).card = 7
  x0Card : (emptyRowsOfParity queens 0).card =
    (emptyCounts profile.inventory profile.pair).x0
  x1Card : (emptyRowsOfParity queens 1).card =
    (emptyCounts profile.inventory profile.pair).x1
  y0Card : (emptyColumnsOfParity queens 0).card =
    (emptyCounts profile.inventory profile.pair).y0
  y1Card : (emptyColumnsOfParity queens 1).card =
    (emptyCounts profile.inventory profile.pair).y1
  color0OddRows :
    (oddRowQueens (queensOfColor queens 0)).card = lift.table.q11

private theorem closeSixOddRows
    {profile : Profile} (realization : WeakleyCanonicalRealization profile)
    (q11Three : realization.lift.table.q11 = 3)
    (x1Card : (emptyRowsOfParity realization.queens 1).card = 6)
    (moment :
      6 * queenRowSum (queensOfColor realization.queens 0) =
        6 * ∑ row ∈
          rationalLineSet (emptyRowsOfParity realization.queens 1), row) : False := by
  have queenParity :
      queenRowSumInt (queensOfColor realization.queens 0) % 2 =
        (realization.lift.table.q11 : ℤ) % 2 := by
    rw [queenRowSumInt_mod_two, realization.color0OddRows]
  have rowsEven :
      lineSumInt (emptyRowsOfParity realization.queens 1) % 2 = 0 := by
    apply lineSumInt_even_of_six_odd
      (emptyRowsOfParity realization.queens 1) x1Card
    intro row rowIn
    exact (mem_emptyRowsOfParity.mp rowIn).2
  rw [queenRowSum_eq_intCast, rationalLineSet_sum] at moment
  have momentInt :
      6 * queenRowSumInt (queensOfColor realization.queens 0) =
        6 * lineSumInt (emptyRowsOfParity realization.queens 1) := by
    exact_mod_cast moment
  exact six_odd_row_profile_contradiction realization.lift.table.q11
    (queenRowSumInt (queensOfColor realization.queens 0))
    (lineSumInt (emptyRowsOfParity realization.queens 1))
    q11Three queenParity rowsEven momentInt

/-- No actual dominating-set realization can satisfy any of the five
canonical Weakley/profile cases.  Constructing such a realization from an
arbitrary hypothetical 13-queen dominator is the remaining external Weakley
bridge; it is intentionally not represented by an axiom. -/
theorem no_weakley_canonical_realization
    (profile : Profile) (profileCanonical : profile ∈ canonicalProfiles)
    (realization : WeakleyCanonicalRealization profile) : False := by
  have q11Three : realization.lift.table.q11 = 3 := by
    apply q11_eq_three_of_mem_canonical_lifts realization.lift
    exact List.mem_flatMap_of_mem profileCanonical realization.liftFeasible
  simp only [canonicalProfiles, List.mem_cons, List.not_mem_nil, or_false]
    at profileCanonical
  rcases profileCanonical with h | h | h | h | h
  · subst profile
    have x0Card : (emptyRowsOfParity realization.queens 0).card = 8 := by
      simpa [emptyCounts, occupiedRows, occupiedColumns] using realization.x0Card
    have y0Card : (emptyColumnsOfParity realization.queens 0).card = 5 := by
      simpa [emptyCounts, occupiedRows, occupiedColumns] using realization.y0Card
    have y1Card : (emptyColumnsOfParity realization.queens 1).card = 8 := by
      simpa [emptyCounts, occupiedRows, occupiedColumns] using realization.y1Card
    have vanishes00 := occurrence_vanishes_on_rationalLineSets
      (queensOfColor realization.queens 0)
      (emptyRowsOfParity realization.queens 0)
      (emptyColumnsOfParity realization.queens 0)
      (occurrence_color_zero_vanishes_on_same_parity_empty_grid
        realization.dominates 0)
    have vanishes01 := occurrence_vanishes_on_rationalLineSets
      (queensOfColor realization.queens 1)
      (emptyRowsOfParity realization.queens 0)
      (emptyColumnsOfParity realization.queens 1)
      (occurrence_color_one_vanishes_on_opposite_parity_empty_grid
        (queens := realization.queens) realization.dominates
        (rowParity := 0) (columnParity := 1) (by norm_num))
    have moment0 := occurrence_six_row_moment_8_5
      (queensOfColor realization.queens 0) realization.color0Card
      (rationalLineSet (emptyRowsOfParity realization.queens 0))
      (rationalLineSet (emptyColumnsOfParity realization.queens 0))
      (by simpa using x0Card) (by simpa using y0Card) vanishes00
    have moment1 := occurrence_seven_row_moment_8_8
      (queensOfColor realization.queens 1) realization.color1Card
      (rationalLineSet (emptyRowsOfParity realization.queens 0))
      (rationalLineSet (emptyColumnsOfParity realization.queens 1))
      (by simpa using x0Card) (by simpa using y1Card) vanishes01
    rw [queenRowSum_eq_intCast, rationalLineSet_sum] at moment0 moment1
    have moment0Int :
        8 * queenRowSumInt (queensOfColor realization.queens 0) =
          6 * lineSumInt (emptyRowsOfParity realization.queens 0) := by
      exact_mod_cast moment0
    have moment1Int :
        8 * queenRowSumInt (queensOfColor realization.queens 1) =
          7 * lineSumInt (emptyRowsOfParity realization.queens 0) := by
      exact_mod_cast moment1
    have queenParity :
        queenRowSumInt (queensOfColor realization.queens 0) % 2 =
          (realization.lift.table.q11 : ℤ) % 2 := by
      rw [queenRowSumInt_mod_two, realization.color0OddRows]
    exact W0_5_8_divisibility_contradiction realization.lift.table.q11
      (queenRowSumInt (queensOfColor realization.queens 0))
      (queenRowSumInt (queensOfColor realization.queens 1))
      (lineSumInt (emptyRowsOfParity realization.queens 0))
      q11Three queenParity moment0Int moment1Int
  · subst profile
    have x1Card : (emptyRowsOfParity realization.queens 1).card = 6 := by
      simpa [emptyCounts, occupiedRows, occupiedColumns] using realization.x1Card
    have y1Card : (emptyColumnsOfParity realization.queens 1).card = 7 := by
      simpa [emptyCounts, occupiedRows, occupiedColumns] using realization.y1Card
    apply closeSixOddRows realization q11Three x1Card
    apply occurrence_six_row_moment_6_7
      (queensOfColor realization.queens 0) realization.color0Card
      (rationalLineSet (emptyRowsOfParity realization.queens 1))
      (rationalLineSet (emptyColumnsOfParity realization.queens 1))
      (by simpa using x1Card) (by simpa using y1Card)
    apply occurrence_vanishes_on_rationalLineSets
    exact occurrence_color_zero_vanishes_on_same_parity_empty_grid
      realization.dominates 1
  · subst profile
    have x1Card : (emptyRowsOfParity realization.queens 1).card = 6 := by
      simpa [emptyCounts, occupiedRows, occupiedColumns] using realization.x1Card
    have y1Card : (emptyColumnsOfParity realization.queens 1).card = 7 := by
      simpa [emptyCounts, occupiedRows, occupiedColumns] using realization.y1Card
    apply closeSixOddRows realization q11Three x1Card
    apply occurrence_six_row_moment_6_7
      (queensOfColor realization.queens 0) realization.color0Card
      (rationalLineSet (emptyRowsOfParity realization.queens 1))
      (rationalLineSet (emptyColumnsOfParity realization.queens 1))
      (by simpa using x1Card) (by simpa using y1Card)
    apply occurrence_vanishes_on_rationalLineSets
    exact occurrence_color_zero_vanishes_on_same_parity_empty_grid
      realization.dominates 1
  · subst profile
    have x1Card : (emptyRowsOfParity realization.queens 1).card = 6 := by
      simpa [emptyCounts, occupiedRows, occupiedColumns] using realization.x1Card
    have y1Card : (emptyColumnsOfParity realization.queens 1).card = 8 := by
      simpa [emptyCounts, occupiedRows, occupiedColumns] using realization.y1Card
    apply closeSixOddRows realization q11Three x1Card
    apply occurrence_six_row_moment_6_8
      (queensOfColor realization.queens 0) realization.color0Card
      (rationalLineSet (emptyRowsOfParity realization.queens 1))
      (rationalLineSet (emptyColumnsOfParity realization.queens 1))
      (by simpa using x1Card) (by simpa using y1Card)
    apply occurrence_vanishes_on_rationalLineSets
    exact occurrence_color_zero_vanishes_on_same_parity_empty_grid
      realization.dominates 1
  · subst profile
    have x1Card : (emptyRowsOfParity realization.queens 1).card = 6 := by
      simpa [emptyCounts, occupiedRows, occupiedColumns] using realization.x1Card
    have y1Card : (emptyColumnsOfParity realization.queens 1).card = 8 := by
      simpa [emptyCounts, occupiedRows, occupiedColumns] using realization.y1Card
    apply closeSixOddRows realization q11Three x1Card
    apply occurrence_six_row_moment_6_8
      (queensOfColor realization.queens 0) realization.color0Card
      (rationalLineSet (emptyRowsOfParity realization.queens 1))
      (rationalLineSet (emptyColumnsOfParity realization.queens 1))
      (by simpa using x1Card) (by simpa using y1Card)
    apply occurrence_vanishes_on_rationalLineSets
    exact occurrence_color_zero_vanishes_on_same_parity_empty_grid
      realization.dominates 1

end

end Q26GridAnnihilator
