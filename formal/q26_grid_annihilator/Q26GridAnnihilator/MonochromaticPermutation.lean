import Mathlib

/-!
# Normalized monochromatic permutation data

This module isolates the algebra available after a monochromatic board has
been normalized to queens `(2 i, 2 π(i) - 1)`, with `i = 1, ..., 13`.
It does not yet construct that normalization from a board and it does not yet
prove the omitted-diagonal threshold lemma.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

abbrev MonoIndex := Fin 13

def monoCoord (index : MonoIndex) : ℤ := index.val + 1

def monoDifference (permutation : MonoIndex ≃ MonoIndex)
    (index : MonoIndex) : ℤ :=
  monoCoord index - monoCoord (permutation index) + 1

def monoSum (permutation : MonoIndex ≃ MonoIndex)
    (index : MonoIndex) : ℤ :=
  monoCoord index + monoCoord (permutation index)

def monoDifferenceSupport (permutation : MonoIndex ≃ MonoIndex) : Finset ℤ :=
  Finset.univ.image (monoDifference permutation)

def monoSumSupport (permutation : MonoIndex ≃ MonoIndex) : Finset ℤ :=
  Finset.univ.image (monoSum permutation)

/-- Exactly the diagonal-cover obligation on the normalized `13 × 13`
opposite-color core. -/
def MonoCoreCovered (permutation : MonoIndex ≃ MonoIndex) : Prop :=
  ∀ row column : MonoIndex, ∃ index : MonoIndex,
    monoCoord row - monoCoord column = monoDifference permutation index ∨
      monoCoord row + monoCoord column = monoSum permutation index

theorem monoCoord_bounds (index : MonoIndex) :
    1 ≤ monoCoord index ∧ monoCoord index ≤ 13 := by
  simp only [monoCoord]
  omega

theorem monoCoord_sum : (∑ index : MonoIndex, monoCoord index) = 91 := by
  norm_num [monoCoord, Fin.sum_univ_succ]

theorem monoCoord_square_sum :
    (∑ index : MonoIndex, monoCoord index ^ 2) = 819 := by
  norm_num [monoCoord, Fin.sum_univ_succ]

theorem monoCoord_perm_sum (permutation : MonoIndex ≃ MonoIndex) :
    (∑ index : MonoIndex, monoCoord (permutation index)) = 91 := by
  rw [Equiv.sum_comp permutation monoCoord, monoCoord_sum]

theorem monoCoord_perm_square_sum (permutation : MonoIndex ≃ MonoIndex) :
    (∑ index : MonoIndex, monoCoord (permutation index) ^ 2) = 819 := by
  rw [Equiv.sum_comp permutation (fun index => monoCoord index ^ 2),
    monoCoord_square_sum]

theorem monoDifference_sum (permutation : MonoIndex ≃ MonoIndex) :
    (∑ index : MonoIndex, monoDifference permutation index) = 13 := by
  simp only [monoDifference, Finset.sum_add_distrib, Finset.sum_sub_distrib,
    monoCoord_sum, monoCoord_perm_sum]
  norm_num

theorem monoSum_sum (permutation : MonoIndex ≃ MonoIndex) :
    (∑ index : MonoIndex, monoSum permutation index) = 182 := by
  simp only [monoSum, Finset.sum_add_distrib, monoCoord_sum,
    monoCoord_perm_sum]
  norm_num

theorem mono_second_moment (permutation : MonoIndex ≃ MonoIndex) :
    (∑ index : MonoIndex,
      ((monoDifference permutation index - 1) ^ 2 +
        monoSum permutation index ^ 2)) = 3276 := by
  have pointwise (index : MonoIndex) :
      (monoDifference permutation index - 1) ^ 2 +
          monoSum permutation index ^ 2 =
        2 * monoCoord index ^ 2 +
          2 * monoCoord (permutation index) ^ 2 := by
    simp only [monoDifference, monoSum]
    ring
  simp_rw [pointwise, Finset.sum_add_distrib, ← Finset.mul_sum]
  rw [monoCoord_square_sum, monoCoord_perm_square_sum]
  norm_num

theorem monoDifference_le_thirteen (permutation : MonoIndex ≃ MonoIndex)
    (index : MonoIndex) : monoDifference permutation index ≤ 13 := by
  have leftBounds := monoCoord_bounds index
  have rightBounds := monoCoord_bounds (permutation index)
  simp only [monoDifference]
  omega

theorem monoDifference_ge_neg_eleven (permutation : MonoIndex ≃ MonoIndex)
    (index : MonoIndex) : -11 ≤ monoDifference permutation index := by
  have leftBounds := monoCoord_bounds index
  have rightBounds := monoCoord_bounds (permutation index)
  simp only [monoDifference]
  omega

theorem monoDifferenceSupport_card_le (permutation : MonoIndex ≃ MonoIndex) :
    (monoDifferenceSupport permutation).card ≤ 13 := by
  rw [monoDifferenceSupport]
  exact (Finset.card_image_le.trans_eq (by decide : (Finset.univ : Finset MonoIndex).card = 13))

theorem monoSumSupport_card_le (permutation : MonoIndex ≃ MonoIndex) :
    (monoSumSupport permutation).card ≤ 13 := by
  rw [monoSumSupport]
  exact (Finset.card_image_le.trans_eq (by decide : (Finset.univ : Finset MonoIndex).card = 13))

end Q26GridAnnihilator
