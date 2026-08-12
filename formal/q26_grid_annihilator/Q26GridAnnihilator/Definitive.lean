import Q26GridAnnihilator.Unconditional

/-!
# Definitive Q26 domination result

This module combines the unrestricted obstruction at cardinality thirteen with
an explicit fourteen-queen dominating set.  A monotonicity and finite-padding
argument upgrades the exact-cardinality obstruction to a lower bound for every
dominating set.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

/-- The retained one-based witness
`(2,6), (4,20), ..., (26,14)`, represented internally by zero-based `Fin 26`
coordinates. -/
def fourteenQueenWitnessList : List Square :=
  [ ((1 : Line), (5 : Line)),
    ((3 : Line), (19 : Line)),
    ((5 : Line), (9 : Line)),
    ((7 : Line), (3 : Line)),
    ((9 : Line), (15 : Line)),
    ((9 : Line), (17 : Line)),
    ((11 : Line), (23 : Line)),
    ((13 : Line), (7 : Line)),
    ((15 : Line), (13 : Line)),
    ((17 : Line), (1 : Line)),
    ((19 : Line), (11 : Line)),
    ((21 : Line), (21 : Line)),
    ((23 : Line), (25 : Line)),
    ((25 : Line), (13 : Line)) ]

/-- The explicit fourteen-queen witness as a finite set. -/
def fourteenQueenWitness : Finset Square := fourteenQueenWitnessList.toFinset

theorem fourteenQueenWitness_card : fourteenQueenWitness.card = 14 := by
  decide

private def decidesAttacks (queen target : Square) : Bool :=
  queen.1 = target.1 || queen.2 = target.2 ||
    coord queen.1 - coord queen.2 = coord target.1 - coord target.2 ||
    coord queen.1 + coord queen.2 = coord target.1 + coord target.2

private theorem decidesAttacks_iff (queen target : Square) :
    decidesAttacks queen target = true ↔ Attacks queen target := by
  simp only [decidesAttacks, Bool.or_eq_true, decide_eq_true_eq,
    Attacks, DiagonalAttack]
  tauto

private def allLines : List Line := List.ofFn fun line : Line => line

private theorem mem_allLines (line : Line) : line ∈ allLines := by
  change line ∈ List.ofFn (fun index : Line => index)
  rw [List.mem_ofFn]
  exact ⟨line, rfl⟩

private def decidesWitnessDominates : Bool :=
  allLines.all fun row => allLines.all fun column =>
    fourteenQueenWitnessList.any fun queen => decidesAttacks queen (row, column)

private theorem decidesWitnessDominates_iff :
    decidesWitnessDominates = true ↔ Dominates fourteenQueenWitness := by
  constructor
  · intro h target
    unfold decidesWitnessDominates at h
    have hrow := (List.all_eq_true.mp h) target.1 (mem_allLines target.1)
    have hcolumn :=
      (List.all_eq_true.mp hrow) target.2 (mem_allLines target.2)
    obtain ⟨queen, hqueen, hattack⟩ := List.any_eq_true.mp hcolumn
    exact ⟨queen, by simpa [fourteenQueenWitness] using hqueen,
      (decidesAttacks_iff queen target).mp hattack⟩
  · intro h
    unfold decidesWitnessDominates
    apply List.all_eq_true.mpr
    intro row _
    apply List.all_eq_true.mpr
    intro column _
    obtain ⟨queen, hqueen, hattack⟩ := h (row, column)
    apply List.any_eq_true.mpr
    exact ⟨queen, by simpa [fourteenQueenWitness] using hqueen,
      (decidesAttacks_iff queen (row, column)).mpr hattack⟩

set_option maxHeartbeats 2000000 in
theorem fourteenQueenWitness_dominates : Dominates fourteenQueenWitness := by
  rw [← decidesWitnessDominates_iff]
  decide

/-- Adding queens cannot destroy domination. -/
theorem dominates_mono {queens larger : Finset Square}
    (hsubset : queens ⊆ larger) (hdominates : Dominates queens) :
    Dominates larger := by
  intro target
  obtain ⟨queen, hqueen, hattack⟩ := hdominates target
  exact ⟨queen, hsubset hqueen, hattack⟩

/-- No Q26 dominating set has at most thirteen queens. -/
theorem no_dominator_card_le_thirteen :
    ¬ ∃ queens : Finset Square, Dominates queens ∧ queens.card ≤ 13 := by
  rintro ⟨queens, hdominates, hcard⟩
  obtain ⟨padded, hsubset, hpadded⟩ :=
    Finset.exists_superset_card_eq (s := queens) hcard (by norm_num [Square, Line])
  exact no_thirteen_queen_dominator
    ⟨padded, dominates_mono hsubset hdominates, hpadded⟩

/-- Every Q26 dominating set contains at least fourteen queens. -/
theorem dominator_card_ge_fourteen {queens : Finset Square}
    (hdominates : Dominates queens) : 14 ≤ queens.card := by
  by_contra hnot
  apply no_dominator_card_le_thirteen
  exact ⟨queens, hdominates, by omega⟩

/-- A finite-cardinality characterization of a domination number. -/
def IsDominationNumber (n : ℕ) : Prop :=
  (∃ queens : Finset Square, Dominates queens ∧ queens.card = n) ∧
    ∀ queens : Finset Square, Dominates queens → n ≤ queens.card

theorem q26_has_fourteen_dominator :
    ∃ queens : Finset Square, Dominates queens ∧ queens.card = 14 :=
  ⟨fourteenQueenWitness, fourteenQueenWitness_dominates,
    fourteenQueenWitness_card⟩

theorem q26_has_no_at_most_thirteen_dominator :
    ¬ ∃ queens : Finset Square, Dominates queens ∧ queens.card ≤ 13 :=
  no_dominator_card_le_thirteen

/-- The domination number of the 26 by 26 queen graph is exactly fourteen. -/
theorem q26_domination_number_eq_fourteen : IsDominationNumber 14 := by
  refine ⟨q26_has_fourteen_dominator, ?_⟩
  intro queens hdominates
  exact dominator_card_ge_fourteen hdominates

/-- Direct verdict theorem, stated without a project-specific wrapper. -/
theorem q26_domination_exact :
    (∃ queens : Finset Square, Dominates queens ∧ queens.card = 14) ∧
      ∀ queens : Finset Square, Dominates queens → 14 ≤ queens.card :=
  q26_domination_number_eq_fourteen

end Q26GridAnnihilator
