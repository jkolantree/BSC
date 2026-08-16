import Mathlib.Algebra.Order.Pi
import Mathlib.Order.Basic

/-!
# Product readiness with per-axis applicability

Verdict or outcome is deliberately absent from readiness.  Each readiness axis
is independently tagged as applicable or not applicable.  `notApplicable` is
not an element, top, or bottom of the underlying axis order: it is comparable
only with itself.
-/

namespace BscCore

/-- A fixed-registry encoding of whether one readiness axis is present. -/
inductive Axis (A : Type*) where
  | notApplicable
  | applicable (value : A)
deriving DecidableEq, Repr

namespace Axis

/-- Refinement within one axis; cross-applicability comparisons are false. -/
def Refines {A : Type*} [LE A] : Axis A → Axis A → Prop
  | .notApplicable, .notApplicable => True
  | .applicable x, .applicable y => x ≤ y
  | _, _ => False

theorem refines_refl {A : Type*} [Preorder A] (x : Axis A) : Refines x x := by
  cases x with
  | notApplicable => trivial
  | applicable _ => exact le_rfl

theorem refines_trans {A : Type*} [Preorder A]
    {x y z : Axis A} (hxy : Refines x y) (hyz : Refines y z) : Refines x z := by
  cases x <;> cases y <;> cases z <;> simp_all [Refines]
  exact hxy.trans hyz

theorem refines_antisymm {A : Type*} [PartialOrder A]
    {x y : Axis A} (hxy : Refines x y) (hyx : Refines y x) : x = y := by
  cases x with
  | notApplicable =>
      cases y with
      | notApplicable => rfl
      | applicable _ => simp [Refines] at hxy
  | applicable x =>
      cases y with
      | notApplicable => simp [Refines] at hxy
      | applicable y =>
          simp only [Refines] at hxy hyx
          exact congrArg applicable (hxy.antisymm hyx)

@[simp]
theorem notApplicable_refines_notApplicable {A : Type*} [LE A] :
    Refines (notApplicable : Axis A) notApplicable :=
  True.intro

@[simp]
theorem notApplicable_not_refines_applicable
    {A : Type*} [LE A] (x : A) :
    ¬ Refines notApplicable (.applicable x) := by
  simp [Refines]

@[simp]
theorem applicable_not_refines_notApplicable
    {A : Type*} [LE A] (x : A) :
    ¬ Refines (.applicable x) notApplicable := by
  simp [Refines]

end Axis

/-- Four independent readiness axes.  Outcome/polarity is intentionally separate. -/
@[ext]
structure Readiness (Maturity Scope Authority Identity : Type*) where
  maturity : Axis Maturity
  scope : Axis Scope
  authority : Axis Authority
  identity : Axis Identity
deriving DecidableEq, Repr

namespace Readiness

/-- Coordinatewise readiness refinement, with no scalarization or compensation. -/
def Refines
    {Maturity Scope Authority Identity : Type*}
    [LE Maturity] [LE Scope] [LE Authority] [LE Identity]
    (x y : Readiness Maturity Scope Authority Identity) : Prop :=
  Axis.Refines x.maturity y.maturity ∧
    Axis.Refines x.scope y.scope ∧
    Axis.Refines x.authority y.authority ∧
    Axis.Refines x.identity y.identity

theorem refines_refl
    {Maturity Scope Authority Identity : Type*}
    [Preorder Maturity] [Preorder Scope] [Preorder Authority] [Preorder Identity]
    (x : Readiness Maturity Scope Authority Identity) : Refines x x := by
  exact
    ⟨Axis.refines_refl _, Axis.refines_refl _,
      Axis.refines_refl _, Axis.refines_refl _⟩

theorem refines_trans
    {Maturity Scope Authority Identity : Type*}
    [Preorder Maturity] [Preorder Scope] [Preorder Authority] [Preorder Identity]
    {x y z : Readiness Maturity Scope Authority Identity}
    (hxy : Refines x y) (hyz : Refines y z) : Refines x z := by
  rcases hxy with ⟨hm, hs, ha, hi⟩
  rcases hyz with ⟨hm', hs', ha', hi'⟩
  exact
    ⟨Axis.refines_trans hm hm', Axis.refines_trans hs hs',
      Axis.refines_trans ha ha', Axis.refines_trans hi hi'⟩

theorem refines_antisymm
    {Maturity Scope Authority Identity : Type*}
    [PartialOrder Maturity] [PartialOrder Scope]
    [PartialOrder Authority] [PartialOrder Identity]
    {x y : Readiness Maturity Scope Authority Identity}
    (hxy : Refines x y) (hyx : Refines y x) : x = y := by
  rcases hxy with ⟨hm, hs, ha, hi⟩
  rcases hyx with ⟨hm', hs', ha', hi'⟩
  apply Readiness.ext
  · exact Axis.refines_antisymm hm hm'
  · exact Axis.refines_antisymm hs hs'
  · exact Axis.refines_antisymm ha ha'
  · exact Axis.refines_antisymm hi hi'

end Readiness

/--
The genuinely typed product for a chosen finite set of active axes.  Omitting an
axis from `AxisId` is literal type-level non-applicability.
-/
abbrev ActiveReadiness (AxisId : Type*) (Value : AxisId → Type*) :=
  (i : AxisId) → Value i

namespace ActiveReadiness

theorem meet_apply
    {AxisId : Type*} {Value : AxisId → Type*}
    [∀ i, SemilatticeInf (Value i)]
    (x y : ActiveReadiness AxisId Value) (i : AxisId) :
    (x ⊓ y) i = x i ⊓ y i :=
  rfl

theorem meet_le_left
    {AxisId : Type*} {Value : AxisId → Type*}
    [∀ i, SemilatticeInf (Value i)]
    (x y : ActiveReadiness AxisId Value) : x ⊓ y ≤ x :=
  inf_le_left

theorem meet_le_right
    {AxisId : Type*} {Value : AxisId → Type*}
    [∀ i, SemilatticeInf (Value i)]
    (x y : ActiveReadiness AxisId Value) : x ⊓ y ≤ y :=
  inf_le_right

theorem le_meet
    {AxisId : Type*} {Value : AxisId → Type*}
    [∀ i, SemilatticeInf (Value i)]
    {x y z : ActiveReadiness AxisId Value}
    (hxy : x ≤ y) (hxz : x ≤ z) : x ≤ y ⊓ z :=
  le_inf hxy hxz

theorem top_apply
    {AxisId : Type*} {Value : AxisId → Type*}
    [∀ i, LE (Value i)] [∀ i, OrderTop (Value i)] (i : AxisId) :
    (⊤ : ActiveReadiness AxisId Value) i = ⊤ :=
  rfl

end ActiveReadiness

end BscCore
