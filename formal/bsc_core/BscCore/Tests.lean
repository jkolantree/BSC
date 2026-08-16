import BscCore

/-!
# Compile-time regression checks

These examples check the intended public signatures.  They contain no separate
axioms and invoke no external decision procedure.
-/

namespace BscCore.Tests

example
    {X Y Z : Type*} (report : X → Y) (target : X → Z) :
    Identifies report target ↔
      ∃ decode : Attainable report → Z,
        target = decode ∘ toAttainable report :=
  identifies_iff_factors_through_attainable report target

example
    {X Y Z : Type*} (report : X → Y) (target : X → Z) :
    Identifies report target ↔
      ∃! decode : Attainable report → Z,
        target = decode ∘ toAttainable report :=
  identifies_iff_existsUnique_factors_through_attainable report target

example
    {I X Z : Type*} {Y : I → Type*} [Fintype X] [DecidableEq X]
    [DecidableEq I] [∀ i, DecidableEq (Y i)] [DecidableEq Z]
    (reports : (i : I) → X → Y i) (target : X → Z) (J : Finset I) :
    IdentifiesFrom reports target J ↔
      targetSeparatedPairs target ⊆ coveredPairs reports J :=
  identifiesFrom_iff_finset_cover reports target J

example
    {V L : Type*} [Fintype V] [CompleteLattice L]
    (S : HomogeneousCapSystem V L) :
    IsGreatest {r : V → L | S.Feasible r} S.greatestFeasible :=
  S.greatestFeasible_isGreatest

example
    {V L : Type*} [Fintype V] [DecidableEq V]
    [CompleteLattice L] [Fintype L]
    (S : HomogeneousCapSystem V L) :
    ∃ n < Fintype.card (V → L),
      S.descendingSequence n = S.greatestFeasible :=
  S.exists_descendingSequence_eq_greatestFeasible

end BscCore.Tests
