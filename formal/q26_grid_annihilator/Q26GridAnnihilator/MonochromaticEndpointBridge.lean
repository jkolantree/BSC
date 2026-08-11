import Q26GridAnnihilator.MonochromaticArithmetic
import Q26GridAnnihilator.MonochromaticExtraction

/-!
# Generic endpoint bridges for the monochromatic shell

These theorems contain no threshold construction.  They consume exact forced
difference/sum supports and turn their finite shell evaluations into the
already checked endpoint contradictions.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

private theorem mono_second_moment_split
    (permutation : MonoIndex ≃ MonoIndex) :
    (∑ index : MonoIndex, (monoDifference permutation index - 1) ^ 2) +
        (∑ index : MonoIndex, monoSum permutation index ^ 2) = 3276 := by
  simpa only [Finset.sum_add_distrib] using mono_second_moment permutation

/-- Thirteen forced symmetric difference labels would make their occurrence
sum zero, contradicting the fixed difference sum `13`. -/
theorem no_mono_of_full_difference_shell
    (permutation : MonoIndex ≃ MonoIndex) (forcedDifferences : Finset ℤ)
    (subsetSupport : forcedDifferences ⊆ monoDifferenceSupport permutation)
    (forcedCard : forcedDifferences.card = 13)
    (forcedSum : (∑ label ∈ forcedDifferences, label) = 0) : False := by
  have occurrenceSum := mono_sum_over_full_forced_support
    (monoDifference permutation) forcedDifferences (by
      simpa only [monoDifferenceSupport] using subsetSupport) forcedCard id
  simp only [id_eq] at occurrenceSum
  rw [monoDifference_sum] at occurrenceSum
  omega

/-- The zero-even-threshold branch: twelve forced symmetric difference
labels leave one occurrence, necessarily label `13`; the full forced sum
support then evaluates the second moment to `4004`, not `3276`. -/
theorem no_mono_of_zero_threshold_shell
    (permutation : MonoIndex ≃ MonoIndex)
    (forcedDifferences forcedSums : Finset ℤ)
    (differenceSubset : forcedDifferences ⊆ monoDifferenceSupport permutation)
    (differenceCard : forcedDifferences.card = 12)
    (differenceSum : (∑ label ∈ forcedDifferences, label) = 0)
    (sumSubset : forcedSums ⊆ monoSumSupport permutation)
    (sumCard : forcedSums.card = 13)
    (shellEvaluation :
      (∑ label ∈ forcedDifferences, (label - 1) ^ 2) +
          (13 - 1) ^ 2 + (∑ label ∈ forcedSums, label ^ 2) = 4004) : False := by
  obtain ⟨residual, residualValue, differenceSquares⟩ :=
    mono_extract_one_residual_occurrence permutation forcedDifferences
      differenceSubset differenceCard
  have residualThirteen : monoDifference permutation residual = 13 := by
    rw [differenceSum] at residualValue
    omega
  have sumSquares := mono_sum_over_full_forced_support
    (monoSum permutation) forcedSums (by
      simpa only [monoSumSupport] using sumSubset) sumCard (fun label => label ^ 2)
  have secondMoment := mono_second_moment_split permutation
  rw [differenceSquares, sumSquares, residualThirteen] at secondMoment
  have impossible : (4004 : ℤ) = 3276 := by
    nlinarith [shellEvaluation, secondMoment]
  exact monochromatic_zero_threshold_contradiction impossible

/-- The `h + o = 13` branch: eleven forced symmetric differences leave two
occurrences.  Their fixed first moment makes them `a` and `13-a`; the exact
shell-square evaluation is therefore the endpoint Diophantine equation. -/
theorem no_mono_of_thirteen_threshold_shell
    (permutation : MonoIndex ≃ MonoIndex) (h : ℤ)
    (forcedDifferences forcedSums : Finset ℤ)
    (differenceSubset : forcedDifferences ⊆ monoDifferenceSupport permutation)
    (differenceCard : forcedDifferences.card = 11)
    (differenceSum : (∑ label ∈ forcedDifferences, label) = 0)
    (sumSubset : forcedSums ⊆ monoSumSupport permutation)
    (sumCard : forcedSums.card = 13)
    (hPositive : 0 < h) (hUpper : h ≤ 12)
    (shellEvaluation :
      (∑ label ∈ forcedDifferences, (label - 1) ^ 2) +
          (∑ label ∈ forcedSums, label ^ 2) =
        24 * h ^ 2 - 312 * h + 3859) : False := by
  obtain ⟨first, second, distinct, residualSum, differenceSquares⟩ :=
    mono_extract_two_residual_occurrences permutation forcedDifferences
      differenceSubset differenceCard
  have residualSumThirteen :
      monoDifference permutation first + monoDifference permutation second = 13 := by
    rw [differenceSum] at residualSum
    omega
  have firstUpper := monoDifference_le_thirteen permutation first
  have secondUpper := monoDifference_le_thirteen permutation second
  have firstLower : 0 ≤ monoDifference permutation first := by omega
  have secondLower : 0 ≤ monoDifference permutation second := by omega
  have sumSquares := mono_sum_over_full_forced_support
    (monoSum permutation) forcedSums (by
      simpa only [monoSumSupport] using sumSubset) sumCard (fun label => label ^ 2)
  have secondMoment := mono_second_moment_split permutation
  rw [differenceSquares, sumSquares] at secondMoment
  let a := monoDifference permutation first
  have expanded :
      24 * h ^ 2 - 312 * h + 3859 + (a - 1) ^ 2 + (12 - a) ^ 2 = 3276 := by
    dsimp only [a]
    nlinarith [shellEvaluation, secondMoment, residualSumThirteen]
  have normalized := (monochromatic_moment_normalization a h).mp expanded
  exact no_q26_monochromatic_endpoint a h
    (by simpa only [a] using firstLower)
    (by simpa only [a] using firstUpper) hPositive hUpper normalized

end

end Q26GridAnnihilator
