import Q26GridAnnihilator.MonochromaticPermutation
import Q26GridAnnihilator.MonochromaticArithmetic
import Q26GridAnnihilator.MonochromaticExtraction
import Q26GridAnnihilator.MonochromaticEndpointBridge

/-!
# The monochromatic diagonal shell

This module develops the remaining finite support argument for a normalized
monochromatic permutation.  All label arithmetic is over `ℤ`; finite board
indices are used only to define the exact target diagonals.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

def monoTargetPairs : Finset (MonoIndex × MonoIndex) := Finset.univ

def monoTargetDifference (target : MonoIndex × MonoIndex) : ℤ :=
  monoCoord target.1 - monoCoord target.2

def monoTargetSum (target : MonoIndex × MonoIndex) : ℤ :=
  monoCoord target.1 + monoCoord target.2

def monoTargetDifferences : Finset ℤ :=
  monoTargetPairs.image monoTargetDifference

def monoTargetSumsAtDifference (difference : ℤ) : Finset ℤ :=
  (monoTargetPairs.filter fun target =>
    monoTargetDifference target = difference).image monoTargetSum

set_option maxRecDepth 100000 in
theorem monoTargetDifferences_exact :
    monoTargetDifferences = Finset.Icc (-12 : ℤ) 12 := by
  decide

set_option maxRecDepth 100000 in
theorem monoTargetSumsAtDifference_card
    (difference : ℤ) (lower : -12 ≤ difference) (upper : difference ≤ 12) :
    (monoTargetSumsAtDifference difference).card =
      13 - Int.natAbs difference := by
  interval_cases difference <;> decide

theorem MonoCoreCovered.support_cover
    {permutation : MonoIndex ≃ MonoIndex}
    (covered : MonoCoreCovered permutation) (target : MonoIndex × MonoIndex) :
    monoTargetDifference target ∈ monoDifferenceSupport permutation ∨
      monoTargetSum target ∈ monoSumSupport permutation := by
  obtain ⟨index, difference | sum⟩ := covered target.1 target.2
  · exact Or.inl (Finset.mem_image.mpr ⟨index, Finset.mem_univ _, difference.symm⟩)
  · exact Or.inr (Finset.mem_image.mpr ⟨index, Finset.mem_univ _, sum.symm⟩)

theorem targetSums_subset_sumSupport_of_difference_missing
    {permutation : MonoIndex ≃ MonoIndex}
    (covered : MonoCoreCovered permutation) {difference : ℤ}
    (missing : difference ∉ monoDifferenceSupport permutation) :
    monoTargetSumsAtDifference difference ⊆ monoSumSupport permutation := by
  intro sumValue sumIn
  rw [monoTargetSumsAtDifference, Finset.mem_image] at sumIn
  obtain ⟨target, targetIn, targetSum⟩ := sumIn
  have targetDifference := (Finset.mem_filter.mp targetIn).2
  rcases covered.support_cover target with differenceIn | sumIn
  · exact False.elim (missing (targetDifference ▸ differenceIn))
  · simpa [targetSum] using sumIn

def monoEvenOmitted (permutation : MonoIndex ≃ MonoIndex) : Finset ℤ :=
  monoTargetDifferences.filter fun difference =>
    difference % 2 = 0 ∧ difference ∉ monoDifferenceSupport permutation

def monoOddOmitted (permutation : MonoIndex ≃ MonoIndex) : Finset ℤ :=
  monoTargetDifferences.filter fun difference =>
    difference % 2 = 1 ∧ difference ∉ monoDifferenceSupport permutation

theorem neg_twelve_mem_monoEvenOmitted
    (permutation : MonoIndex ≃ MonoIndex) :
    (-12 : ℤ) ∈ monoEvenOmitted permutation := by
  rw [monoEvenOmitted, Finset.mem_filter]
  refine ⟨?_, by norm_num, ?_⟩
  · rw [monoTargetDifferences_exact]
    norm_num
  · intro supportIn
    rw [monoDifferenceSupport, Finset.mem_image] at supportIn
    obtain ⟨index, _indexIn, equality⟩ := supportIn
    have lower := monoDifference_ge_neg_eleven permutation index
    omega

theorem monoEvenOmitted_nonempty (permutation : MonoIndex ≃ MonoIndex) :
    (monoEvenOmitted permutation).Nonempty :=
  ⟨-12, neg_twelve_mem_monoEvenOmitted permutation⟩

def monoMandatoryDifferences (evenThreshold oddThreshold : Nat) : Finset ℤ :=
  monoTargetDifferences.filter fun difference =>
    (difference % 2 = 0 ∧ Int.natAbs difference < evenThreshold) ∨
      (difference % 2 = 1 ∧ Int.natAbs difference < oddThreshold)

theorem monoEvenThreshold_values
    (threshold : Nat) (bound : threshold ≤ 12)
    (parity : threshold % 2 = 0) :
    threshold = 0 ∨ threshold = 2 ∨ threshold = 4 ∨ threshold = 6 ∨
      threshold = 8 ∨ threshold = 10 ∨ threshold = 12 := by
  omega

theorem monoPositiveEvenThreshold_values
    (threshold : Nat) (positive : 0 < threshold) (bound : threshold ≤ 12)
    (parity : threshold % 2 = 0) :
    threshold = 2 ∨ threshold = 4 ∨ threshold = 6 ∨ threshold = 8 ∨
      threshold = 10 ∨ threshold = 12 := by
  omega

theorem monoOddThreshold_values
    (threshold : Nat) (bound : threshold ≤ 13)
    (parity : threshold % 2 = 1) :
    threshold = 1 ∨ threshold = 3 ∨ threshold = 5 ∨ threshold = 7 ∨
      threshold = 9 ∨ threshold = 11 ∨ threshold = 13 := by
  omega

set_option maxRecDepth 100000 in
theorem monoMandatoryDifferences_card
    (evenThreshold oddThreshold : Nat)
    (evenPositive : 0 < evenThreshold)
    (evenBound : evenThreshold ≤ 12) (evenParity : evenThreshold % 2 = 0)
    (oddBound : oddThreshold ≤ 13) (oddParity : oddThreshold % 2 = 1) :
    (monoMandatoryDifferences evenThreshold oddThreshold).card =
      evenThreshold + oddThreshold - 2 := by
  rcases monoPositiveEvenThreshold_values evenThreshold evenPositive evenBound
      evenParity with rfl | rfl | rfl | rfl | rfl | rfl <;>
    rcases monoOddThreshold_values oddThreshold oddBound oddParity with
      rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    decide

set_option maxRecDepth 100000 in
theorem monoMandatoryDifferences_sum
    (evenThreshold oddThreshold : Nat)
    (evenBound : evenThreshold ≤ 12) (evenParity : evenThreshold % 2 = 0)
    (oddBound : oddThreshold ≤ 13) (oddParity : oddThreshold % 2 = 1) :
    (∑ difference ∈ monoMandatoryDifferences evenThreshold oddThreshold,
      difference) = 0 := by
  rcases monoEvenThreshold_values evenThreshold evenBound evenParity with
      rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    rcases monoOddThreshold_values oddThreshold oddBound oddParity with
      rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    decide

theorem monoTargetDifference_natAbs_le_twelve {difference : ℤ}
    (member : difference ∈ monoTargetDifferences) :
    Int.natAbs difference ≤ 12 := by
  rw [monoTargetDifferences_exact] at member
  obtain ⟨lower, upper⟩ := Finset.mem_Icc.mp member
  have squareBound : difference ^ 2 ≤ (12 : ℤ) ^ 2 := by
    nlinarith
  have absoluteBound := Int.natAbs_le_iff_sq_le.mpr squareBound
  norm_num at absoluteBound
  exact absoluteBound

def monoEvenOmittedAbs (permutation : MonoIndex ≃ MonoIndex) : Finset Nat :=
  (monoEvenOmitted permutation).image Int.natAbs

theorem monoEvenOmittedAbs_nonempty (permutation : MonoIndex ≃ MonoIndex) :
    (monoEvenOmittedAbs permutation).Nonempty := by
  obtain ⟨difference, member⟩ := monoEvenOmitted_nonempty permutation
  exact ⟨Int.natAbs difference,
    Finset.mem_image.mpr ⟨difference, member, rfl⟩⟩

def monoEvenThreshold (permutation : MonoIndex ≃ MonoIndex) : Nat :=
  (monoEvenOmittedAbs permutation).min'
    (monoEvenOmittedAbs_nonempty permutation)

def monoOddThresholdCandidates
    (permutation : MonoIndex ≃ MonoIndex) : Finset Nat :=
  insert 13 ((monoOddOmitted permutation).image Int.natAbs)

theorem monoOddThresholdCandidates_nonempty
    (permutation : MonoIndex ≃ MonoIndex) :
    (monoOddThresholdCandidates permutation).Nonempty := by
  exact ⟨13, by simp [monoOddThresholdCandidates]⟩

/-- The value `13` is the sentinel used when no odd target difference is
omitted.  Every genuine omitted odd difference has absolute value at most
eleven, so the sentinel cannot mask one. -/
def monoOddThreshold (permutation : MonoIndex ≃ MonoIndex) : Nat :=
  (monoOddThresholdCandidates permutation).min'
    (monoOddThresholdCandidates_nonempty permutation)

theorem monoEvenThreshold_spec (permutation : MonoIndex ≃ MonoIndex) :
    ∃ difference ∈ monoEvenOmitted permutation,
      Int.natAbs difference = monoEvenThreshold permutation := by
  have member : monoEvenThreshold permutation ∈
      monoEvenOmittedAbs permutation := by
    exact Finset.min'_mem (monoEvenOmittedAbs permutation)
      (monoEvenOmittedAbs_nonempty permutation)
  change monoEvenThreshold permutation ∈
    (monoEvenOmitted permutation).image Int.natAbs at member
  rw [Finset.mem_image] at member
  obtain ⟨difference, differenceMember, equality⟩ := member
  exact ⟨difference, differenceMember, equality⟩

theorem monoOddThreshold_sentinel_or_spec
    (permutation : MonoIndex ≃ MonoIndex) :
    monoOddThreshold permutation = 13 ∨
      ∃ difference ∈ monoOddOmitted permutation,
        Int.natAbs difference = monoOddThreshold permutation := by
  have member : monoOddThreshold permutation ∈
      monoOddThresholdCandidates permutation := by
    exact Finset.min'_mem (monoOddThresholdCandidates permutation)
      (monoOddThresholdCandidates_nonempty permutation)
  change monoOddThreshold permutation ∈
    insert 13 ((monoOddOmitted permutation).image Int.natAbs) at member
  rw [Finset.mem_insert] at member
  rcases member with sentinel | omitted
  · exact Or.inl sentinel
  · rw [Finset.mem_image] at omitted
    obtain ⟨difference, differenceMember, equality⟩ := omitted
    exact Or.inr ⟨difference, differenceMember, equality⟩

theorem monoEvenThreshold_bound (permutation : MonoIndex ≃ MonoIndex) :
    monoEvenThreshold permutation ≤ 12 := by
  obtain ⟨difference, member, equality⟩ := monoEvenThreshold_spec permutation
  rw [← equality]
  exact monoTargetDifference_natAbs_le_twelve
    (Finset.mem_filter.mp member).1

theorem monoEvenThreshold_parity (permutation : MonoIndex ≃ MonoIndex) :
    monoEvenThreshold permutation % 2 = 0 := by
  obtain ⟨difference, member, equality⟩ := monoEvenThreshold_spec permutation
  rw [← equality]
  have integerEven : Even difference :=
    Int.not_odd_iff_even.mp
      (Int.not_odd_iff.mpr (Finset.mem_filter.mp member).2.1)
  exact Nat.even_iff.mp (Int.natAbs_even.mpr integerEven)

theorem monoOddThreshold_bound (permutation : MonoIndex ≃ MonoIndex) :
    monoOddThreshold permutation ≤ 13 := by
  exact Finset.min'_le (monoOddThresholdCandidates permutation) 13
    (by simp [monoOddThresholdCandidates])

theorem monoOddThreshold_parity (permutation : MonoIndex ≃ MonoIndex) :
    monoOddThreshold permutation % 2 = 1 := by
  rcases monoOddThreshold_sentinel_or_spec permutation with sentinel | omitted
  · simp [sentinel]
  · obtain ⟨difference, member, equality⟩ := omitted
    rw [← equality]
    have integerOdd : Odd difference :=
      Int.odd_iff.mpr (Finset.mem_filter.mp member).2.1
    exact Nat.odd_iff.mp (Int.natAbs_odd.mpr integerOdd)

theorem monoEvenThreshold_le_natAbs_of_omitted
    (permutation : MonoIndex ≃ MonoIndex) {difference : ℤ}
    (omitted : difference ∈ monoEvenOmitted permutation) :
    monoEvenThreshold permutation ≤ Int.natAbs difference := by
  exact Finset.min'_le (monoEvenOmittedAbs permutation)
    (Int.natAbs difference)
    (Finset.mem_image.mpr ⟨difference, omitted, rfl⟩)

theorem monoOddThreshold_le_natAbs_of_omitted
    (permutation : MonoIndex ≃ MonoIndex) {difference : ℤ}
    (omitted : difference ∈ monoOddOmitted permutation) :
    monoOddThreshold permutation ≤ Int.natAbs difference := by
  exact Finset.min'_le (monoOddThresholdCandidates permutation)
    (Int.natAbs difference)
    (by
      rw [monoOddThresholdCandidates, Finset.mem_insert]
      exact Or.inr (Finset.mem_image.mpr ⟨difference, omitted, rfl⟩))

theorem monoOddThreshold_spec_of_lt_thirteen
    (permutation : MonoIndex ≃ MonoIndex)
    (strict : monoOddThreshold permutation < 13) :
    ∃ difference ∈ monoOddOmitted permutation,
      Int.natAbs difference = monoOddThreshold permutation := by
  rcases monoOddThreshold_sentinel_or_spec permutation with sentinel | omitted
  · omega
  · exact omitted

/-- By minimality, every target difference inside the two thresholds is a
genuine difference label of the permutation. -/
theorem monoMandatoryDifferences_subset_differenceSupport
    (permutation : MonoIndex ≃ MonoIndex) :
    monoMandatoryDifferences (monoEvenThreshold permutation)
        (monoOddThreshold permutation) ⊆
      monoDifferenceSupport permutation := by
  intro difference member
  rw [monoMandatoryDifferences, Finset.mem_filter] at member
  obtain ⟨targetMember, evenCase | oddCase⟩ := member
  · by_contra missing
    have omitted : difference ∈ monoEvenOmitted permutation := by
      rw [monoEvenOmitted, Finset.mem_filter]
      exact ⟨targetMember, evenCase.1, missing⟩
    have minimal :=
      monoEvenThreshold_le_natAbs_of_omitted permutation omitted
    omega
  · by_contra missing
    have omitted : difference ∈ monoOddOmitted permutation := by
      rw [monoOddOmitted, Finset.mem_filter]
      exact ⟨targetMember, oddCase.1, missing⟩
    have minimal :=
      monoOddThreshold_le_natAbs_of_omitted permutation omitted
    omega

theorem monoTargetDifference_bounds {difference : ℤ}
    (member : difference ∈ monoTargetDifferences) :
    -12 ≤ difference ∧ difference ≤ 12 := by
  rw [monoTargetDifferences_exact] at member
  exact Finset.mem_Icc.mp member

theorem monoTargetSumsAtDifference_disjoint_of_even_odd
    {evenDifference oddDifference : ℤ}
    (evenParity : evenDifference % 2 = 0)
    (oddParity : oddDifference % 2 = 1) :
    Disjoint (monoTargetSumsAtDifference evenDifference)
      (monoTargetSumsAtDifference oddDifference) := by
  rw [Finset.disjoint_left]
  intro sumValue evenMember oddMember
  rw [monoTargetSumsAtDifference, Finset.mem_image] at evenMember oddMember
  obtain ⟨evenTarget, evenTargetMember, evenSum⟩ := evenMember
  obtain ⟨oddTarget, oddTargetMember, oddSum⟩ := oddMember
  have evenDifferenceValue := (Finset.mem_filter.mp evenTargetMember).2
  have oddDifferenceValue := (Finset.mem_filter.mp oddTargetMember).2
  simp only [monoTargetDifference] at evenDifferenceValue oddDifferenceValue
  simp only [monoTargetSum] at evenSum oddSum
  omega

/-- The two omitted-diagonal sum shells cannot contain more than the thirteen
available sum labels.  The odd sentinel `13` makes the statement uniform
when no odd target difference is omitted. -/
theorem monoThreshold_sum_lower
    {permutation : MonoIndex ≃ MonoIndex}
    (covered : MonoCoreCovered permutation) :
    13 ≤ monoEvenThreshold permutation + monoOddThreshold permutation := by
  by_cases sentinel : monoOddThreshold permutation = 13
  · omega
  · have oddStrict : monoOddThreshold permutation < 13 := by
      have oddBound := monoOddThreshold_bound permutation
      omega
    obtain ⟨evenDifference, evenOmitted, evenAbsolute⟩ :=
      monoEvenThreshold_spec permutation
    obtain ⟨oddDifference, oddOmitted, oddAbsolute⟩ :=
      monoOddThreshold_spec_of_lt_thirteen permutation oddStrict
    have evenParts := Finset.mem_filter.mp evenOmitted
    have oddParts := Finset.mem_filter.mp oddOmitted
    have evenSubset :=
      targetSums_subset_sumSupport_of_difference_missing covered evenParts.2.2
    have oddSubset :=
      targetSums_subset_sumSupport_of_difference_missing covered oddParts.2.2
    have unionSubset :
        monoTargetSumsAtDifference evenDifference ∪
            monoTargetSumsAtDifference oddDifference ⊆
          monoSumSupport permutation :=
      Finset.union_subset evenSubset oddSubset
    have unionCardBound := Finset.card_le_card unionSubset
    have disjoint := monoTargetSumsAtDifference_disjoint_of_even_odd
      evenParts.2.1 oddParts.2.1
    have evenBounds := monoTargetDifference_bounds evenParts.1
    have oddBounds := monoTargetDifference_bounds oddParts.1
    have evenCard := monoTargetSumsAtDifference_card evenDifference
      evenBounds.1 evenBounds.2
    have oddCard := monoTargetSumsAtDifference_card oddDifference
      oddBounds.1 oddBounds.2
    have supportCardBound := monoSumSupport_card_le permutation
    rw [Finset.card_union_of_disjoint disjoint, evenCard, oddCard,
      evenAbsolute, oddAbsolute] at unionCardBound
    omega

theorem monoThreshold_sum_upper_of_positive
    (permutation : MonoIndex ≃ MonoIndex)
    (evenPositive : 0 < monoEvenThreshold permutation) :
    monoEvenThreshold permutation + monoOddThreshold permutation ≤ 15 := by
  have mandatorySubset :=
    monoMandatoryDifferences_subset_differenceSupport permutation
  have mandatoryCardBound := Finset.card_le_card mandatorySubset
  have mandatoryCard := monoMandatoryDifferences_card
    (monoEvenThreshold permutation) (monoOddThreshold permutation)
    evenPositive (monoEvenThreshold_bound permutation)
    (monoEvenThreshold_parity permutation)
    (monoOddThreshold_bound permutation) (monoOddThreshold_parity permutation)
  have supportCardBound := monoDifferenceSupport_card_le permutation
  rw [mandatoryCard] at mandatoryCardBound
  omega

/-- In the positive branch the support caps leave the odd total `13` or
`15`; the `15` branch would force thirteen symmetric difference labels and
contradict the fixed difference sum. -/
theorem monoThreshold_sum_eq_thirteen_of_positive
    {permutation : MonoIndex ≃ MonoIndex}
    (covered : MonoCoreCovered permutation)
    (evenPositive : 0 < monoEvenThreshold permutation) :
    monoEvenThreshold permutation + monoOddThreshold permutation = 13 := by
  have lower := monoThreshold_sum_lower covered
  have upper := monoThreshold_sum_upper_of_positive permutation evenPositive
  have evenParity := monoEvenThreshold_parity permutation
  have oddParity := monoOddThreshold_parity permutation
  by_contra notThirteen
  have fifteen :
      monoEvenThreshold permutation + monoOddThreshold permutation = 15 := by
    omega
  let mandatory := monoMandatoryDifferences (monoEvenThreshold permutation)
    (monoOddThreshold permutation)
  have subsetSupport : mandatory ⊆ monoDifferenceSupport permutation := by
    simpa only [mandatory] using
      monoMandatoryDifferences_subset_differenceSupport permutation
  have mandatoryCard : mandatory.card = 13 := by
    have cardFormula := monoMandatoryDifferences_card
      (monoEvenThreshold permutation) (monoOddThreshold permutation)
      evenPositive (monoEvenThreshold_bound permutation)
      evenParity (monoOddThreshold_bound permutation) oddParity
    simpa only [mandatory] using (by omega :
      (monoMandatoryDifferences (monoEvenThreshold permutation)
        (monoOddThreshold permutation)).card = 13)
  have mandatorySum : (∑ label ∈ mandatory, label) = 0 := by
    simpa only [mandatory] using monoMandatoryDifferences_sum
      (monoEvenThreshold permutation) (monoOddThreshold permutation)
      (monoEvenThreshold_bound permutation) evenParity
      (monoOddThreshold_bound permutation) oddParity
  exact no_mono_of_full_difference_shell permutation mandatory subsetSupport
    mandatoryCard mandatorySum

theorem monoTargetSumsAtDifference_neg (difference : ℤ) :
    monoTargetSumsAtDifference (-difference) =
      monoTargetSumsAtDifference difference := by
  ext sumValue
  constructor
  · intro member
    rw [monoTargetSumsAtDifference, Finset.mem_image] at member ⊢
    obtain ⟨target, targetMember, targetSum⟩ := member
    refine ⟨(target.2, target.1), ?_, ?_⟩
    · rw [Finset.mem_filter]
      refine ⟨by simp [monoTargetPairs], ?_⟩
      have differenceValue := (Finset.mem_filter.mp targetMember).2
      simp only [monoTargetDifference] at differenceValue ⊢
      omega
    · simpa only [monoTargetSum, add_comm] using targetSum
  · intro member
    rw [monoTargetSumsAtDifference, Finset.mem_image] at member ⊢
    obtain ⟨target, targetMember, targetSum⟩ := member
    refine ⟨(target.2, target.1), ?_, ?_⟩
    · rw [Finset.mem_filter]
      refine ⟨by simp [monoTargetPairs], ?_⟩
      have differenceValue := (Finset.mem_filter.mp targetMember).2
      simp only [monoTargetDifference] at differenceValue ⊢
      omega
    · simpa only [monoTargetSum, add_comm] using targetSum

theorem monoTargetSumsAtDifference_eq_natAbs (difference : ℤ) :
    monoTargetSumsAtDifference difference =
      monoTargetSumsAtDifference (Int.natAbs difference : ℤ) := by
  rcases Int.natAbs_eq difference with nonnegative | negative
  · exact congrArg monoTargetSumsAtDifference nonnegative
  · calc
      monoTargetSumsAtDifference difference =
          monoTargetSumsAtDifference (-(Int.natAbs difference : ℤ)) := by
            exact congrArg monoTargetSumsAtDifference negative
      _ = monoTargetSumsAtDifference (Int.natAbs difference : ℤ) :=
        monoTargetSumsAtDifference_neg _

theorem monoEvenThreshold_targetSums_subset_sumSupport
    {permutation : MonoIndex ≃ MonoIndex}
    (covered : MonoCoreCovered permutation) :
    monoTargetSumsAtDifference (monoEvenThreshold permutation : ℤ) ⊆
      monoSumSupport permutation := by
  obtain ⟨difference, omitted, absolute⟩ := monoEvenThreshold_spec permutation
  have actualSubset := targetSums_subset_sumSupport_of_difference_missing
    covered (Finset.mem_filter.mp omitted).2.2
  have shellEquality := monoTargetSumsAtDifference_eq_natAbs difference
  rw [absolute] at shellEquality
  rw [← shellEquality]
  exact actualSubset

theorem monoOddThreshold_targetSums_subset_sumSupport
    {permutation : MonoIndex ≃ MonoIndex}
    (covered : MonoCoreCovered permutation)
    (strict : monoOddThreshold permutation < 13) :
    monoTargetSumsAtDifference (monoOddThreshold permutation : ℤ) ⊆
      monoSumSupport permutation := by
  obtain ⟨difference, omitted, absolute⟩ :=
    monoOddThreshold_spec_of_lt_thirteen permutation strict
  have actualSubset := targetSums_subset_sumSupport_of_difference_missing
    covered (Finset.mem_filter.mp omitted).2.2
  have shellEquality := monoTargetSumsAtDifference_eq_natAbs difference
  rw [absolute] at shellEquality
  rw [← shellEquality]
  exact actualSubset

theorem monoCanonicalTargetSums_card (threshold : Nat)
    (bound : threshold ≤ 12) :
    (monoTargetSumsAtDifference (threshold : ℤ)).card = 13 - threshold := by
  simpa using monoTargetSumsAtDifference_card (threshold : ℤ)
    (by omega) (by exact_mod_cast bound)

theorem monoCanonicalTargetSums_disjoint
    (evenThreshold oddThreshold : Nat)
    (evenParity : evenThreshold % 2 = 0)
    (oddParity : oddThreshold % 2 = 1) :
    Disjoint (monoTargetSumsAtDifference (evenThreshold : ℤ))
      (monoTargetSumsAtDifference (oddThreshold : ℤ)) := by
  apply monoTargetSumsAtDifference_disjoint_of_even_odd
  · exact_mod_cast evenParity
  · exact_mod_cast oddParity

set_option maxRecDepth 100000 in
theorem monoMandatoryDifferences_zero_thirteen_card :
    (monoMandatoryDifferences 0 13).card = 12 := by
  decide

set_option maxRecDepth 100000 in
theorem monoZeroShell_evaluation :
    (∑ label ∈ monoMandatoryDifferences 0 13, (label - 1) ^ 2) +
        (13 - 1) ^ 2 +
        (∑ label ∈ monoTargetSumsAtDifference 0, label ^ 2) = 4004 := by
  decide

theorem monoThirteenCanonicalSums_card
    (evenThreshold oddThreshold : Nat)
    (evenPositive : 0 < evenThreshold)
    (evenBound : evenThreshold ≤ 12) (evenParity : evenThreshold % 2 = 0)
    (_oddBound : oddThreshold ≤ 13) (oddParity : oddThreshold % 2 = 1)
    (thresholdSum : evenThreshold + oddThreshold = 13) :
    (monoTargetSumsAtDifference (evenThreshold : ℤ) ∪
      monoTargetSumsAtDifference (oddThreshold : ℤ)).card = 13 := by
  have oddTwelve : oddThreshold ≤ 12 := by omega
  rw [Finset.card_union_of_disjoint
      (monoCanonicalTargetSums_disjoint evenThreshold oddThreshold
        evenParity oddParity),
    monoCanonicalTargetSums_card evenThreshold evenBound,
    monoCanonicalTargetSums_card oddThreshold oddTwelve]
  omega

set_option maxRecDepth 100000 in
/-- Exact kernel evaluation of all six positive threshold shells
`(2,11), (4,9), ..., (12,1)`. -/
theorem monoThirteenShell_evaluation
    (evenThreshold oddThreshold : Nat)
    (evenPositive : 0 < evenThreshold)
    (evenBound : evenThreshold ≤ 12) (evenParity : evenThreshold % 2 = 0)
    (oddBound : oddThreshold ≤ 13) (oddParity : oddThreshold % 2 = 1)
    (thresholdSum : evenThreshold + oddThreshold = 13) :
    (∑ label ∈ monoMandatoryDifferences evenThreshold oddThreshold,
        (label - 1) ^ 2) +
        (∑ label ∈
          (monoTargetSumsAtDifference (evenThreshold : ℤ) ∪
            monoTargetSumsAtDifference (oddThreshold : ℤ)), label ^ 2) =
      24 * (evenThreshold : ℤ) ^ 2 - 312 * (evenThreshold : ℤ) + 3859 := by
  rcases monoPositiveEvenThreshold_values evenThreshold evenPositive evenBound
      evenParity with rfl | rfl | rfl | rfl | rfl | rfl
  · have oddExact : oddThreshold = 11 := by omega
    subst oddThreshold
    decide
  · have oddExact : oddThreshold = 9 := by omega
    subst oddThreshold
    decide
  · have oddExact : oddThreshold = 7 := by omega
    subst oddThreshold
    decide
  · have oddExact : oddThreshold = 5 := by omega
    subst oddThreshold
    decide
  · have oddExact : oddThreshold = 3 := by omega
    subst oddThreshold
    decide
  · have oddExact : oddThreshold = 1 := by omega
    subst oddThreshold
    decide

/-- The sentinel branch `h = 0` supplies twelve symmetric difference labels
and the complete even sum shell. -/
theorem no_mono_of_zero_even_threshold
    {permutation : MonoIndex ≃ MonoIndex}
    (covered : MonoCoreCovered permutation)
    (evenZero : monoEvenThreshold permutation = 0) : False := by
  have thresholdLower := monoThreshold_sum_lower covered
  have oddBound := monoOddThreshold_bound permutation
  have oddThirteen : monoOddThreshold permutation = 13 := by omega
  let forcedDifferences :=
    monoMandatoryDifferences (monoEvenThreshold permutation)
      (monoOddThreshold permutation)
  let forcedSums := monoTargetSumsAtDifference (0 : ℤ)
  have differenceSubset :
      forcedDifferences ⊆ monoDifferenceSupport permutation := by
    simpa only [forcedDifferences] using
      monoMandatoryDifferences_subset_differenceSupport permutation
  have differenceCard : forcedDifferences.card = 12 := by
    simpa only [forcedDifferences, evenZero, oddThirteen] using
      monoMandatoryDifferences_zero_thirteen_card
  have differenceSum : (∑ label ∈ forcedDifferences, label) = 0 := by
    have evaluated := monoMandatoryDifferences_sum
      (monoEvenThreshold permutation) (monoOddThreshold permutation)
      (monoEvenThreshold_bound permutation)
      (monoEvenThreshold_parity permutation)
      (monoOddThreshold_bound permutation)
      (monoOddThreshold_parity permutation)
    simpa only [forcedDifferences] using evaluated
  have sumSubset : forcedSums ⊆ monoSumSupport permutation := by
    have subset := monoEvenThreshold_targetSums_subset_sumSupport covered
    simpa [forcedSums, evenZero] using subset
  have sumCard : forcedSums.card = 13 := by
    simpa [forcedSums] using monoCanonicalTargetSums_card 0 (by omega)
  have shellEvaluation :
      (∑ label ∈ forcedDifferences, (label - 1) ^ 2) +
          (13 - 1) ^ 2 + (∑ label ∈ forcedSums, label ^ 2) = 4004 := by
    simpa only [forcedDifferences, forcedSums, evenZero, oddThirteen] using
      monoZeroShell_evaluation
  exact no_mono_of_zero_threshold_shell permutation forcedDifferences forcedSums
    differenceSubset differenceCard differenceSum sumSubset sumCard shellEvaluation

/-- The positive branch supplies eleven symmetric difference labels and a
thirteen-label canonical sum shell, whose finite evaluation is exactly the
endpoint expression. -/
theorem no_mono_of_positive_even_threshold
    {permutation : MonoIndex ≃ MonoIndex}
    (covered : MonoCoreCovered permutation)
    (evenPositive : 0 < monoEvenThreshold permutation) : False := by
  let evenThreshold := monoEvenThreshold permutation
  let oddThreshold := monoOddThreshold permutation
  have evenBound : evenThreshold ≤ 12 := monoEvenThreshold_bound permutation
  have evenParity : evenThreshold % 2 = 0 := monoEvenThreshold_parity permutation
  have oddBound : oddThreshold ≤ 13 := monoOddThreshold_bound permutation
  have oddParity : oddThreshold % 2 = 1 := monoOddThreshold_parity permutation
  have thresholdSum : evenThreshold + oddThreshold = 13 := by
    simpa only [evenThreshold, oddThreshold] using
      monoThreshold_sum_eq_thirteen_of_positive covered evenPositive
  have oddStrict : oddThreshold < 13 := by omega
  let forcedDifferences := monoMandatoryDifferences evenThreshold oddThreshold
  let forcedSums := monoTargetSumsAtDifference (evenThreshold : ℤ) ∪
    monoTargetSumsAtDifference (oddThreshold : ℤ)
  have differenceSubset :
      forcedDifferences ⊆ monoDifferenceSupport permutation := by
    simpa only [forcedDifferences, evenThreshold, oddThreshold] using
      monoMandatoryDifferences_subset_differenceSupport permutation
  have differenceCard : forcedDifferences.card = 11 := by
    have cardFormula := monoMandatoryDifferences_card evenThreshold oddThreshold
      (by simpa only [evenThreshold] using evenPositive) evenBound evenParity
      oddBound oddParity
    simpa only [forcedDifferences] using (by omega :
      (monoMandatoryDifferences evenThreshold oddThreshold).card = 11)
  have differenceSum : (∑ label ∈ forcedDifferences, label) = 0 := by
    simpa only [forcedDifferences] using monoMandatoryDifferences_sum
      evenThreshold oddThreshold evenBound evenParity oddBound oddParity
  have evenSumSubset :
      monoTargetSumsAtDifference (evenThreshold : ℤ) ⊆
        monoSumSupport permutation := by
    simpa only [evenThreshold] using
      monoEvenThreshold_targetSums_subset_sumSupport covered
  have oddSumSubset :
      monoTargetSumsAtDifference (oddThreshold : ℤ) ⊆
        monoSumSupport permutation := by
    simpa only [oddThreshold] using
      monoOddThreshold_targetSums_subset_sumSupport covered (by
        simpa only [oddThreshold] using oddStrict)
  have sumSubset : forcedSums ⊆ monoSumSupport permutation := by
    exact Finset.union_subset evenSumSubset oddSumSubset
  have sumCard : forcedSums.card = 13 := by
    simpa only [forcedSums] using monoThirteenCanonicalSums_card
      evenThreshold oddThreshold
      (by simpa only [evenThreshold] using evenPositive)
      evenBound evenParity oddBound oddParity thresholdSum
  have shellEvaluation :
      (∑ label ∈ forcedDifferences, (label - 1) ^ 2) +
          (∑ label ∈ forcedSums, label ^ 2) =
        24 * (evenThreshold : ℤ) ^ 2 -
          312 * (evenThreshold : ℤ) + 3859 := by
    simpa only [forcedDifferences, forcedSums] using monoThirteenShell_evaluation
      evenThreshold oddThreshold
      (by simpa only [evenThreshold] using evenPositive)
      evenBound evenParity oddBound oddParity thresholdSum
  exact no_mono_of_thirteen_threshold_shell permutation (evenThreshold : ℤ)
    forcedDifferences forcedSums differenceSubset differenceCard differenceSum
    sumSubset sumCard (by exact_mod_cast (show 0 < evenThreshold from by
      simpa only [evenThreshold] using evenPositive))
    (by exact_mod_cast evenBound) shellEvaluation

/-- No normalized monochromatic permutation covers the opposite-color
`13 × 13` core.  The positive branch terminates at
`no_q26_monochromatic_endpoint`; the zero branch terminates at the checked
`4004 ≠ 3276` shell. -/
theorem no_mono_core_covered (permutation : MonoIndex ≃ MonoIndex)
    (covered : MonoCoreCovered permutation) : False := by
  by_cases evenPositive : 0 < monoEvenThreshold permutation
  · exact no_mono_of_positive_even_threshold covered evenPositive
  · have evenZero : monoEvenThreshold permutation = 0 := by omega
    exact no_mono_of_zero_even_threshold covered evenZero

end Q26GridAnnihilator
