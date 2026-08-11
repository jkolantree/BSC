import Q26GridAnnihilator.MonochromaticPermutation

/-!
# Extracting the two residual monochromatic occurrences

The diagonal-shell argument eventually forces eleven distinct difference
labels.  This module contains the purely finite bookkeeping which turns that
support statement into two residual queen occurrences.  It is deliberately
independent of how the eleven labels were forced.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

private theorem select_mandatory_labels
    (labels : MonoIndex → ℤ) (mandatory : Finset ℤ)
    (subsetSupport : mandatory ⊆ Finset.univ.image labels) :
    ∃ used : Finset MonoIndex,
      used.card = mandatory.card ∧
      (∑ index ∈ used, labels index) = ∑ label ∈ mandatory, label ∧
      (∑ index ∈ used, (labels index - 1) ^ 2) =
        ∑ label ∈ mandatory, (label - 1) ^ 2 := by
  classical
  let select : {label // label ∈ mandatory} → MonoIndex := fun label =>
    Classical.choose (Finset.mem_image.mp (subsetSupport label.property))
  have selectSpec (label : {label // label ∈ mandatory}) :
      labels (select label) = label := by
    exact (Classical.choose_spec
      (Finset.mem_image.mp (subsetSupport label.property))).2
  have selectInjective : Function.Injective select := by
    intro left right equality
    apply Subtype.ext
    calc
      left.1 = labels (select left) := (selectSpec left).symm
      _ = labels (select right) := by rw [equality]
      _ = right.1 := selectSpec right
  let used : Finset MonoIndex := mandatory.attach.image select
  refine ⟨used, ?_, ?_, ?_⟩
  · rw [show used = mandatory.attach.image select by rfl,
      Finset.card_image_iff.mpr selectInjective.injOn,
      Finset.card_attach]
  · rw [show used = mandatory.attach.image select by rfl,
      Finset.sum_image (fun left _ right _ equality => selectInjective equality)]
    simp_rw [selectSpec]
    exact Finset.sum_attach mandatory (fun label : ℤ => label)
  · rw [show used = mandatory.attach.image select by rfl,
      Finset.sum_image (fun left _ right _ equality => selectInjective equality)]
    simp_rw [selectSpec]
    exact Finset.sum_attach mandatory (fun label : ℤ => (label - 1) ^ 2)

/-- Thirteen forced distinct labels exhaust both the support and the thirteen
occurrences.  Consequently every weighted occurrence sum can be evaluated on
the forced label set instead. -/
theorem mono_sum_over_full_forced_support
    (labels : MonoIndex → ℤ) (forced : Finset ℤ)
    (subsetSupport : forced ⊆ Finset.univ.image labels)
    (forcedCard : forced.card = 13) (weight : ℤ → ℤ) :
    (∑ index : MonoIndex, weight (labels index)) =
      ∑ label ∈ forced, weight label := by
  classical
  let support : Finset ℤ := Finset.univ.image labels
  have supportCardLe : support.card ≤ 13 := by
    have imageBound : support.card ≤ (Finset.univ : Finset MonoIndex).card :=
      Finset.card_image_le
    simpa [support] using imageBound
  have forcedEqSupport : forced = support := by
    apply Finset.eq_of_subset_of_card_le
    · simpa only [support] using subsetSupport
    · omega
  have supportCard : support.card = (Finset.univ : Finset MonoIndex).card := by
    simpa [forcedEqSupport] using forcedCard
  have injective : Set.InjOn labels (Finset.univ : Finset MonoIndex) := by
    exact Finset.card_image_iff.mp (by simpa only [support] using supportCard)
  have imageSum := Finset.sum_image (f := weight) injective
  have supportSum :
      (∑ label ∈ support, weight label) =
        ∑ index : MonoIndex, weight (labels index) := by
    simpa only [support] using imageSum
  rw [← forcedEqSupport] at supportSum
  exact supportSum.symm

/-- Twelve distinct forced labels leave exactly one occurrence, with exact
first- and shifted-square-moment decompositions. -/
theorem mono_extract_one_residual_occurrence
    (permutation : MonoIndex ≃ MonoIndex) (mandatory : Finset ℤ)
    (subsetSupport : mandatory ⊆ monoDifferenceSupport permutation)
    (mandatoryCard : mandatory.card = 12) :
    ∃ residual : MonoIndex,
      monoDifference permutation residual =
        13 - ∑ label ∈ mandatory, label ∧
      (∑ index : MonoIndex, (monoDifference permutation index - 1) ^ 2) =
        (∑ label ∈ mandatory, (label - 1) ^ 2) +
          (monoDifference permutation residual - 1) ^ 2 := by
  classical
  obtain ⟨used, usedCard, usedSum, usedSquareSum⟩ :=
    select_mandatory_labels (monoDifference permutation) mandatory (by
      simpa only [monoDifferenceSupport] using subsetSupport)
  have usedSubset : used ⊆ (Finset.univ : Finset MonoIndex) :=
    fun _ _ => Finset.mem_univ _
  have residualCard : ((Finset.univ : Finset MonoIndex) \ used).card = 1 := by
    rw [Finset.card_sdiff_of_subset usedSubset, Finset.card_univ, Fintype.card_fin,
      usedCard, mandatoryCard]
  rw [Finset.card_eq_one] at residualCard
  obtain ⟨residual, residualExact⟩ := residualCard
  refine ⟨residual, ?_, ?_⟩
  · have split :
        (∑ index ∈ (Finset.univ : Finset MonoIndex) \ used,
            monoDifference permutation index) +
            ∑ index ∈ used, monoDifference permutation index =
          ∑ index : MonoIndex, monoDifference permutation index :=
      Finset.sum_sdiff usedSubset
    rw [residualExact, Finset.sum_singleton, usedSum,
      monoDifference_sum] at split
    omega
  · have split :
        (∑ index ∈ (Finset.univ : Finset MonoIndex) \ used,
            (monoDifference permutation index - 1) ^ 2) +
            ∑ index ∈ used, (monoDifference permutation index - 1) ^ 2 =
          ∑ index : MonoIndex,
            (monoDifference permutation index - 1) ^ 2 :=
      Finset.sum_sdiff usedSubset
    rw [residualExact, Finset.sum_singleton, usedSquareSum] at split
    omega

/-- If eleven distinct labels occur among the thirteen difference
occurrences, their complement consists of two occurrences.  Both the first
moment and the shifted-square moment split exactly across those two slots. -/
theorem mono_extract_two_residual_occurrences
    (permutation : MonoIndex ≃ MonoIndex) (mandatory : Finset ℤ)
    (subsetSupport : mandatory ⊆ monoDifferenceSupport permutation)
    (mandatoryCard : mandatory.card = 11) :
    ∃ first second : MonoIndex,
      first ≠ second ∧
      monoDifference permutation first + monoDifference permutation second =
        13 - ∑ label ∈ mandatory, label ∧
      (∑ index : MonoIndex, (monoDifference permutation index - 1) ^ 2) =
        (∑ label ∈ mandatory, (label - 1) ^ 2) +
          (monoDifference permutation first - 1) ^ 2 +
          (monoDifference permutation second - 1) ^ 2 := by
  classical
  have supportForm : monoDifferenceSupport permutation =
      Finset.univ.image (monoDifference permutation) := rfl
  obtain ⟨used, usedCard, usedSum, usedSquareSum⟩ :=
    select_mandatory_labels (monoDifference permutation) mandatory (by
      simpa only [supportForm] using subsetSupport)
  have usedSubset : used ⊆ (Finset.univ : Finset MonoIndex) :=
    fun _ _ => Finset.mem_univ _
  have residualCard : ((Finset.univ : Finset MonoIndex) \ used).card = 2 := by
    rw [Finset.card_sdiff_of_subset usedSubset, Finset.card_univ, Fintype.card_fin,
      usedCard, mandatoryCard]
  rw [Finset.card_eq_two] at residualCard
  obtain ⟨first, second, distinct, residualExact⟩ := residualCard
  refine ⟨first, second, distinct, ?_, ?_⟩
  · have split :
        (∑ index ∈ (Finset.univ : Finset MonoIndex) \ used,
            monoDifference permutation index) +
            ∑ index ∈ used, monoDifference permutation index =
          ∑ index : MonoIndex, monoDifference permutation index :=
      Finset.sum_sdiff usedSubset
    rw [residualExact, Finset.sum_insert (by simpa using distinct),
      Finset.sum_singleton, usedSum, monoDifference_sum] at split
    omega
  · have split :
        (∑ index ∈ (Finset.univ : Finset MonoIndex) \ used,
            (monoDifference permutation index - 1) ^ 2) +
            ∑ index ∈ used, (monoDifference permutation index - 1) ^ 2 =
          ∑ index : MonoIndex,
            (monoDifference permutation index - 1) ^ 2 :=
      Finset.sum_sdiff usedSubset
    rw [residualExact, Finset.sum_insert (by simpa using distinct),
      Finset.sum_singleton, usedSquareSum] at split
    omega

end

end Q26GridAnnihilator
