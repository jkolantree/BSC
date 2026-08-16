import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Data.Finset.Prod

/-!
# Exact finite approximate-identifiability bounds

Distances and tolerances are natural-valued here.  This keeps the finite maximum
fully executable and avoids hidden analytic assumptions.  The central theorem
states that adding reports shrinks the compatible-pair set, so maximum target
oscillation cannot increase.
-/

namespace BscCore
namespace Approximate

variable {I X : Type*}

/-- Two completions are compatible with all selected tolerance tests. -/
def Compatible
    (reportDistance : I → X → X → Nat) (tolerance : I → Nat)
    (J : Finset I) (x x' : X) : Prop :=
  ∀ i ∈ J, reportDistance i x x' ≤ tolerance i

/-- Computable Boolean presentation of `Compatible`. -/
def compatibleBool
    (reportDistance : I → X → X → Nat) (tolerance : I → Nat)
    (J : Finset I) (x x' : X) : Bool :=
  J.fold (· && ·) true
    fun i => decide (reportDistance i x x' ≤ tolerance i)

theorem compatibleBool_eq_true_iff
    [DecidableEq I]
    (reportDistance : I → X → X → Nat) (tolerance : I → Nat)
    (J : Finset I) (x x' : X) :
    compatibleBool reportDistance tolerance J x x' = true ↔
      Compatible reportDistance tolerance J x x' := by
  induction J using Finset.induction_on with
  | empty => simp [compatibleBool, Compatible]
  | @insert i J hi ih =>
      rw [compatibleBool, Finset.fold_insert hi]
      change
        ((decide (reportDistance i x x' ≤ tolerance i) &&
            compatibleBool reportDistance tolerance J x x') = true) ↔
          Compatible reportDistance tolerance (insert i J) x x'
      simp [ih, Compatible]

/-- Finite collection of completion pairs compatible with all selected reports. -/
def compatiblePairs
    [Fintype X] [Fintype I] [DecidableEq X] [DecidableEq I]
    (reportDistance : I → X → X → Nat) (tolerance : I → Nat)
    (J : Finset I) : Finset (X × X) :=
  ((Finset.univ : Finset X).product Finset.univ).filter
    fun p => compatibleBool reportDistance tolerance J p.1 p.2 = true

/-- Maximum target discrepancy among pairs left compatible by the selected reports. -/
def oscillation
    [Fintype X] [Fintype I] [DecidableEq X] [DecidableEq I]
    (targetDistance : X → X → Nat)
    (reportDistance : I → X → X → Nat) (tolerance : I → Nat)
    (J : Finset I) : Nat :=
  (compatiblePairs reportDistance tolerance J).sup
    fun p => targetDistance p.1 p.2

/-- More selected reports produce a subset of compatible completion pairs. -/
theorem compatiblePairs_anti
    [Fintype X] [Fintype I] [DecidableEq X] [DecidableEq I]
    {reportDistance : I → X → X → Nat} {tolerance : I → Nat}
    {J K : Finset I} (hJK : J ⊆ K) :
    compatiblePairs reportDistance tolerance K ⊆
      compatiblePairs reportDistance tolerance J := by
  intro p hp
  simp only [compatiblePairs, Finset.mem_filter] at hp ⊢
  refine ⟨hp.1, ?_⟩
  rw [compatibleBool_eq_true_iff] at hp ⊢
  intro i hi
  exact hp.2 i (hJK hi)

/-- Tightening every selected tolerance produces a subset of compatible pairs. -/
theorem compatiblePairs_mono_tolerance
    [Fintype X] [Fintype I] [DecidableEq X] [DecidableEq I]
    {reportDistance : I → X → X → Nat}
    {tighter looser : I → Nat} (hTolerance : ∀ i, tighter i ≤ looser i)
    (J : Finset I) :
    compatiblePairs reportDistance tighter J ⊆
      compatiblePairs reportDistance looser J := by
  intro p hp
  simp only [compatiblePairs, Finset.mem_filter] at hp ⊢
  refine ⟨hp.1, ?_⟩
  rw [compatibleBool_eq_true_iff] at hp ⊢
  intro i hi
  exact (hp.2 i hi).trans (hTolerance i)

/-- Adding reports cannot increase exact finite target oscillation. -/
theorem oscillation_mono
    [Fintype X] [Fintype I] [DecidableEq X] [DecidableEq I]
    (targetDistance : X → X → Nat)
    (reportDistance : I → X → X → Nat) (tolerance : I → Nat)
    {J K : Finset I} (hJK : J ⊆ K) :
    oscillation targetDistance reportDistance tolerance K ≤
      oscillation targetDistance reportDistance tolerance J := by
  exact Finset.sup_mono (compatiblePairs_anti hJK)

/-- Tightening report tolerances cannot increase exact finite target oscillation. -/
theorem oscillation_mono_tolerance
    [Fintype X] [Fintype I] [DecidableEq X] [DecidableEq I]
    (targetDistance : X → X → Nat)
    (reportDistance : I → X → X → Nat)
    {tighter looser : I → Nat} (hTolerance : ∀ i, tighter i ≤ looser i)
    (J : Finset I) :
    oscillation targetDistance reportDistance tighter J ≤
      oscillation targetDistance reportDistance looser J := by
  exact Finset.sup_mono (compatiblePairs_mono_tolerance hTolerance J)

/-- A uniform bound over compatible pairs bounds the computed oscillation. -/
theorem oscillation_le_of_bound
    [Fintype X] [Fintype I] [DecidableEq X] [DecidableEq I]
    (targetDistance : X → X → Nat)
    (reportDistance : I → X → X → Nat) (tolerance : I → Nat)
    (J : Finset I) (bound : Nat)
    (hbound : ∀ x x', Compatible reportDistance tolerance J x x' →
      targetDistance x x' ≤ bound) :
    oscillation targetDistance reportDistance tolerance J ≤ bound := by
  apply Finset.sup_le
  intro p hp
  apply hbound p.1 p.2
  exact (compatibleBool_eq_true_iff _ _ _ _ _).1 (Finset.mem_filter.mp hp).2

end Approximate
end BscCore
