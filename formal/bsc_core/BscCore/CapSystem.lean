import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Fintype.Pigeonhole
import Mathlib.Order.FixedPoints
import Mathlib.Order.Monotone.Basic

/-!
# Monotone cap systems and cyclic readiness closure

A finite cap system has an initial ceiling at each vertex and a monotone cap
transport on every possible directed edge.  Absent edges contribute `top`.
The step operator is therefore

`F(r) v = initial v inf inf_u (if edge u v then cap u v (r u) else top)`.

Feasibility means `r <= F(r)`.  Knaster--Tarski supplies a greatest feasible
assignment, and that assignment is a fixed point.  Cycles are allowed.
-/

namespace BscCore

/-- Any antitone sequence in a finite partial order has stabilized before `card` steps. -/
theorem finite_antitone_stabilizes
    {A : Type*} [Fintype A] [PartialOrder A]
    (sequence : Nat → A) (hanti : Antitone sequence) :
    ∃ n < Fintype.card A, sequence (n + 1) = sequence n := by
  let sample : Fin (Fintype.card A + 1) → A := fun n => sequence n.1
  obtain ⟨a, b, hab, heq⟩ := Fintype.exists_ne_map_eq_of_card_lt sample (by
    rw [Fintype.card_fin]
    exact Nat.lt_succ_self (Fintype.card A))
  change sequence a.1 = sequence b.1 at heq
  have hval : a.1 ≠ b.1 := by
    intro h
    exact hab (Fin.ext h)
  rcases lt_or_gt_of_ne hval with hablt | hbalt
  · refine ⟨a.1, lt_of_lt_of_le hablt (Nat.lt_succ_iff.mp b.isLt), ?_⟩
    apply le_antisymm
    · exact hanti (Nat.le_succ a.1)
    · rw [heq]
      exact hanti (Nat.succ_le_iff.mpr hablt)
  · refine ⟨b.1, lt_of_lt_of_le hbalt (Nat.lt_succ_iff.mp a.isLt), ?_⟩
    apply le_antisymm
    · exact hanti (Nat.le_succ b.1)
    · rw [← heq]
      exact hanti (Nat.succ_le_iff.mpr hbalt)

/-- A finite monotone readiness-cap system with one common complete lattice. -/
structure HomogeneousCapSystem (V L : Type*) [Fintype V] [Preorder L] where
  initial : V → L
  edge : V → V → Bool
  cap : V → V → (L →o L)

namespace HomogeneousCapSystem

variable {V L : Type*} [Fintype V] [CompleteLattice L]

/-- One simultaneous cap-propagation step. -/
def step (S : HomogeneousCapSystem V L) (r : V → L) : V → L :=
  fun v => S.initial v ⊓ ⨅ u, if S.edge u v = true then S.cap u v (r u) else ⊤

theorem step_monotone (S : HomogeneousCapSystem V L) : Monotone S.step := by
  intro r s hrs v
  apply inf_le_inf le_rfl
  refine iInf_mono fun u => ?_
  by_cases h : S.edge u v = true
  · rw [if_pos h, if_pos h]
    exact (S.cap u v).monotone (hrs u)
  · rw [if_neg h, if_neg h]

/-- The cap step as a bundled monotone endomorphism. -/
def stepHom (S : HomogeneousCapSystem V L) : (V → L) →o (V → L) where
  toFun := S.step
  monotone' := S.step_monotone

/-- A readiness assignment obeys every declared baseline and incoming cap. -/
def Feasible (S : HomogeneousCapSystem V L) (r : V → L) : Prop :=
  r ≤ S.step r

/-- The greatest feasible readiness assignment, including for cyclic graphs. -/
noncomputable def greatestFeasible (S : HomogeneousCapSystem V L) : V → L :=
  S.stepHom.gfp

theorem greatestFeasible_fixed (S : HomogeneousCapSystem V L) :
    S.step S.greatestFeasible = S.greatestFeasible := by
  exact S.stepHom.map_gfp

theorem greatestFeasible_feasible (S : HomogeneousCapSystem V L) :
    S.Feasible S.greatestFeasible := by
  exact S.greatestFeasible_fixed.ge

theorem feasible_le_greatestFeasible (S : HomogeneousCapSystem V L)
    {r : V → L} (hr : S.Feasible r) : r ≤ S.greatestFeasible := by
  exact S.stepHom.le_gfp hr

/-- The fixed point is exactly the greatest post-fixed (feasible) assignment. -/
theorem greatestFeasible_isGreatest (S : HomogeneousCapSystem V L) :
    IsGreatest {r : V → L | S.Feasible r} S.greatestFeasible := by
  exact S.stepHom.isGreatest_gfp_le

/-- Readiness closure can never exceed the declared initial ceiling. -/
theorem greatestFeasible_le_initial (S : HomogeneousCapSystem V L) (v : V) :
    S.greatestFeasible v ≤ S.initial v := by
  rw [← congrFun S.greatestFeasible_fixed v]
  exact inf_le_left

/-- Iteration from `top`; this is the executable descending readiness chain. -/
def descendingSequence (S : HomogeneousCapSystem V L) (n : Nat) : V → L :=
  (S.step^[n]) ⊤

theorem descendingSequence_succ (S : HomogeneousCapSystem V L) (n : Nat) :
    S.descendingSequence (n + 1) = S.step (S.descendingSequence n) := by
  simp [descendingSequence, Function.iterate_succ_apply']

theorem descendingSequence_succ_le (S : HomogeneousCapSystem V L) (n : Nat) :
    S.descendingSequence (n + 1) ≤ S.descendingSequence n := by
  induction n with
  | zero =>
      rw [S.descendingSequence_succ]
      exact le_top
  | succ n ih =>
      simpa only [S.descendingSequence_succ] using S.step_monotone ih

theorem descendingSequence_antitone (S : HomogeneousCapSystem V L) :
    Antitone S.descendingSequence :=
  antitone_nat_of_succ_le S.descendingSequence_succ_le

/-- On a finite lattice, descending iteration stabilizes within the finite state bound. -/
theorem descendingSequence_stabilizes
    [DecidableEq V] [Fintype L] (S : HomogeneousCapSystem V L) :
    ∃ n < Fintype.card (V → L),
      S.step (S.descendingSequence n) = S.descendingSequence n := by
  obtain ⟨n, hn, hstable⟩ :=
    finite_antitone_stabilizes S.descendingSequence S.descendingSequence_antitone
  refine ⟨n, hn, ?_⟩
  rw [← S.descendingSequence_succ n]
  exact hstable

theorem greatestFeasible_le_descendingSequence
    (S : HomogeneousCapSystem V L) (n : Nat) :
    S.greatestFeasible ≤ S.descendingSequence n := by
  induction n with
  | zero => exact le_top
  | succ n ih =>
      rw [S.descendingSequence_succ n]
      calc
        S.greatestFeasible = S.step S.greatestFeasible :=
          S.greatestFeasible_fixed.symm
        _ ≤ S.step (S.descendingSequence n) := S.step_monotone ih

/-- Every stabilized descending iterate is the greatest feasible fixed point. -/
theorem descendingSequence_eq_greatestFeasible_of_fixed
    (S : HomogeneousCapSystem V L) (n : Nat)
    (hfixed : S.step (S.descendingSequence n) = S.descendingSequence n) :
    S.descendingSequence n = S.greatestFeasible := by
  apply le_antisymm
  · apply S.feasible_le_greatestFeasible
    exact hfixed.ge
  · exact S.greatestFeasible_le_descendingSequence n

/-- On a finite lattice, some bounded descending iterate is the greatest feasible point. -/
theorem exists_descendingSequence_eq_greatestFeasible
    [DecidableEq V] [Fintype L] (S : HomogeneousCapSystem V L) :
    ∃ n < Fintype.card (V → L),
      S.descendingSequence n = S.greatestFeasible := by
  obtain ⟨n, hn, hfixed⟩ := S.descendingSequence_stabilizes
  exact ⟨n, hn, S.descendingSequence_eq_greatestFeasible_of_fixed n hfixed⟩

end HomogeneousCapSystem

end BscCore
