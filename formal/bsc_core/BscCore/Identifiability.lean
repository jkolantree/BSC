import Mathlib.Data.Set.Operations

/-!
# Operational identifiability

A report identifies a target exactly when the target is constant on report
fibres.  This is equivalent to factorization through the subtype of attainable
reports, avoiding any arbitrary value on unattainable codomain points.
-/

namespace BscCore

/-- Equality of reports forces equality of the target. -/
def Identifies {X Y Z : Type*} (report : X → Y) (target : X → Z) : Prop :=
  ∀ ⦃x x' : X⦄, report x = report x' → target x = target x'

/-- The subtype of reports actually emitted by some completion. -/
def Attainable {X Y : Type*} (report : X → Y) : Type _ :=
  Set.range report

/-- Every completion canonically yields an attainable report. -/
def toAttainable {X Y : Type*} (report : X → Y) (x : X) : Attainable report :=
  Set.rangeFactorization report x

theorem toAttainable_surjective {X Y : Type*} (report : X → Y) :
    Function.Surjective (toAttainable report) := by
  rintro ⟨y, x, hx⟩
  refine ⟨x, ?_⟩
  exact Subtype.ext hx

/-- A representative-based decoder on attainable reports. -/
noncomputable def decoderOnAttainable
    {X Y Z : Type*} (report : X → Y) (target : X → Z) :
    Attainable report → Z :=
  fun y => target (Set.rangeSplitting report y)

theorem decoderOnAttainable_spec
    {X Y Z : Type*} {report : X → Y} {target : X → Z}
    (h : Identifies report target) (x : X) :
    decoderOnAttainable report target (toAttainable report x) = target x := by
  apply h
  simpa [toAttainable, Set.rangeFactorization] using
    Set.apply_rangeSplitting report (toAttainable report x)

/-- Fibre identifiability is equivalent to factorization through attainable reports. -/
theorem identifies_iff_factors_through_attainable
    {X Y Z : Type*} (report : X → Y) (target : X → Z) :
    Identifies report target ↔
      ∃ decode : Attainable report → Z,
        target = decode ∘ toAttainable report := by
  constructor
  · intro h
    refine ⟨decoderOnAttainable report target, funext fun x => ?_⟩
    exact (decoderOnAttainable_spec h x).symm
  · rintro ⟨decode, hfactor⟩ x x' hreport
    calc
      target x = decode (toAttainable report x) := congrFun hfactor x
      _ = decode (toAttainable report x') := by
        apply congrArg decode
        exact Subtype.ext hreport
      _ = target x' := (congrFun hfactor x').symm

/-- The factor through attainable reports exists uniquely. -/
theorem identifies_iff_existsUnique_factors_through_attainable
    {X Y Z : Type*} (report : X → Y) (target : X → Z) :
    Identifies report target ↔
      ∃! decode : Attainable report → Z,
        target = decode ∘ toAttainable report := by
  constructor
  · intro h
    obtain ⟨decode, hdecode⟩ :=
      (identifies_iff_factors_through_attainable report target).1 h
    refine ⟨decode, hdecode, ?_⟩
    intro other hother
    funext y
    obtain ⟨x, rfl⟩ := toAttainable_surjective report y
    calc
      other (toAttainable report x) = target x := (congrFun hother x).symm
      _ = decode (toAttainable report x) := congrFun hdecode x
  · rintro ⟨decode, hdecode, _⟩
    exact (identifies_iff_factors_through_attainable report target).2
      ⟨decode, hdecode⟩

/-- Identifiability is exactly inclusion of the report kernel in the target kernel. -/
theorem identifies_iff_kernel_inclusion
    {X Y Z : Type*} (report : X → Y) (target : X → Z) :
    Identifies report target ↔
      ∀ x x' : X, report x = report x' → target x = target x' := by
  rfl

end BscCore
