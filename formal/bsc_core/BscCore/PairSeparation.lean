import BscCore.Identifiability
import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Data.Finset.Prod

/-!
# Finite heterogeneous intervention families and pair separation

An intervention family identifies a target precisely when it distinguishes
every ordered pair of completions on which the target differs.  Each
intervention may have its own report codomain `Y i`.
-/

namespace BscCore

/-- The dependent joint report emitted by the interventions selected in `J`. -/
def jointReport {I X : Type*} {Y : I → Type*}
    (reports : (i : I) → X → Y i) (J : Finset I) (x : X) :
    (i : J) → Y i.1 :=
  fun i => reports i.1 x

/-- A selected heterogeneous intervention family identifies the target. -/
def IdentifiesFrom {I X Z : Type*} {Y : I → Type*}
    (reports : (i : I) → X → Y i) (target : X → Z) (J : Finset I) : Prop :=
  Identifies (jointReport reports J) target

/-- Every target-separated pair is distinguished by at least one selected report. -/
def PairCover {I X Z : Type*} {Y : I → Type*}
    (reports : (i : I) → X → Y i) (target : X → Z) (J : Finset I) : Prop :=
  ∀ x x' : X, target x ≠ target x' →
    ∃ i ∈ J, reports i x ≠ reports i x'

/-- Operational identifiability is exactly pair separation. -/
theorem identifiesFrom_iff_pairCover
    {I X Z : Type*} {Y : I → Type*}
    (reports : (i : I) → X → Y i)
    (target : X → Z) (J : Finset I) :
    IdentifiesFrom reports target J ↔ PairCover reports target J := by
  constructor
  · intro h x x' htarget
    by_contra hnone
    have hjoint : jointReport reports J x = jointReport reports J x' := by
      funext i
      by_contra hdiff
      exact hnone ⟨i.1, i.2, hdiff⟩
    exact htarget (h hjoint)
  · intro h x x' hjoint
    by_contra htarget
    obtain ⟨i, hi, hdiff⟩ := h x x' htarget
    apply hdiff
    exact congrFun hjoint ⟨i, hi⟩

/-- Adding interventions cannot destroy identifiability. -/
theorem identifiesFrom_mono
    {I X Z : Type*} {Y : I → Type*}
    {reports : (i : I) → X → Y i} {target : X → Z}
    {J K : Finset I} (hJK : J ⊆ K)
    (hJ : IdentifiesFrom reports target J) :
    IdentifiesFrom reports target K := by
  apply (identifiesFrom_iff_pairCover reports target K).2
  intro x x' htarget
  obtain ⟨i, hi, hdiff⟩ :=
    (identifiesFrom_iff_pairCover reports target J).1 hJ x x' htarget
  exact ⟨i, hJK hi, hdiff⟩

section FiniteCover

variable {I X Z : Type*} {Y : I → Type*}
  [Fintype X] [DecidableEq X]
  [∀ i, DecidableEq (Y i)] [DecidableEq Z]

/-- The finite universe of target-separated ordered pairs. -/
def targetSeparatedPairs (target : X → Z) : Finset (X × X) :=
  ((Finset.univ : Finset X).product Finset.univ).filter
    fun p => target p.1 ≠ target p.2

/-- The pairs distinguished by one typed report. -/
def distinguishedPairs {W : Type*} [DecidableEq W]
    (report : X → W) : Finset (X × X) :=
  ((Finset.univ : Finset X).product Finset.univ).filter
    fun p => report p.1 ≠ report p.2

/-- The union of the selected interventions' distinguishing sets. -/
def coveredPairs (reports : (i : I) → X → Y i)
    (J : Finset I) : Finset (X × X) :=
  J.biUnion fun i => distinguishedPairs (reports i)

/-- The pointwise pair condition is exactly finite set cover. -/
theorem pairCover_iff_finset_cover
    (reports : (i : I) → X → Y i) (target : X → Z) (J : Finset I) :
    PairCover reports target J ↔
      targetSeparatedPairs target ⊆ coveredPairs reports J := by
  constructor
  · intro h p hp
    rcases p with ⟨x, x'⟩
    have htarget : target x ≠ target x' := by
      simpa [targetSeparatedPairs] using hp
    obtain ⟨i, hi, hdiff⟩ := h x x' htarget
    simp only [coveredPairs, Finset.mem_biUnion]
    refine ⟨i, hi, ?_⟩
    simpa [distinguishedPairs] using hdiff
  · intro h x x' htarget
    have hp : (x, x') ∈ targetSeparatedPairs target := by
      simp [targetSeparatedPairs, htarget]
    have hcovered := h hp
    simp only [coveredPairs, Finset.mem_biUnion] at hcovered
    obtain ⟨i, hi, hpair⟩ := hcovered
    refine ⟨i, hi, ?_⟩
    simpa [distinguishedPairs] using hpair

/-- Finite operational identifiability is exactly a finite set-cover condition. -/
theorem identifiesFrom_iff_finset_cover
    (reports : (i : I) → X → Y i) (target : X → Z) (J : Finset I) :
    IdentifiesFrom reports target J ↔
      targetSeparatedPairs target ⊆ coveredPairs reports J :=
  (identifiesFrom_iff_pairCover reports target J).trans
    (pairCover_iff_finset_cover reports target J)

end FiniteCover

end BscCore
