# BSC Core v1.5 — formal kernel

This is a small, statement-faithful Lean kernel for the BSC v1.5 foundations
milestone. It does not formalize the applications compendium, make a physical
claim, or assert that the full eight-field BSC record forms a category.

The project is pinned to Lean `4.33.0`. `lakefile.toml` requests mathlib
`v4.33.0`; `lake-manifest.json` resolves that tag to commit
`db584cd6d46c92f209a44c0f1c829460d327499d`.

## Exact theorem-to-claim map

| Claim boundary | Lean declarations | Exact scope |
|---|---|---|
| RDY-01: fixed-signature readiness product | `ActiveReadiness`, `ActiveReadiness.meet_apply`, `meet_le_left`, `meet_le_right`, `le_meet`, `top_apply` | Dependent product over the chosen active axes; component orders supply meet/top. This is the meet-semilattice law within one applicability signature. |
| Per-axis applicability | `Axis`, `Axis.Refines`, `Axis.notApplicable_not_refines_applicable`, `Axis.applicable_not_refines_notApplicable` | `notApplicable` is a tag, not an element/top/bottom of an axis. Cross-signature refinement is false. `Readiness` is the four-axis fixed-registry encoding. Outcome/polarity is absent. |
| Product-order laws | `Readiness.refines_refl`, `refines_trans`, `refines_antisymm` | Coordinatewise maturity/scope/authority/identity refinement, with no scalarization. |
| Homogeneous cyclic readiness closure | `HomogeneousCapSystem.step_monotone`, `greatestFeasible_fixed`, `greatestFeasible_isGreatest`, `greatestFeasible_le_initial` | Finite vertex set, one common complete lattice `L`, monotone typed-by-endpoint caps specialized to `L →o L`; cycles allowed. |
| RDY finite descending stabilization, homogeneous specialization | `finite_antitone_stabilizes`, `HomogeneousCapSystem.descendingSequence_stabilizes`, `exists_descendingSequence_eq_greatestFeasible` | If `L` is finite, iteration from `top` stabilizes before `card (V → L)` states and the stabilized iterate equals the greatest feasible point. This is not the heterogeneous-lattice theorem. |
| IDN-01: identifiability/factorization | `identifies_iff_factors_through_attainable`, `identifies_iff_existsUnique_factors_through_attainable` | A report identifies a target iff the target factors uniquely through the subtype of attainable reports. |
| IDN-02: pair separation/set cover | `identifiesFrom_iff_pairCover`, `pairCover_iff_finset_cover`, `identifiesFrom_iff_finset_cover` | Finite completion space and heterogeneous report codomains `Y i`; ordered completion pairs are used. This proves the cover equivalence, not weighted optimization. |
| IDN-03: monotonicity | `identifiesFrom_mono`, `Approximate.oscillation_mono`, `Approximate.oscillation_mono_tolerance` | Adding reports preserves identification and cannot increase exact finite oscillation; tightening every selected natural-valued tolerance cannot increase it either. |

## Readiness semantics

There are two complementary encodings:

1. `ActiveReadiness AxisId Value` is the literal dependent product for a chosen
   set of active axes. Omitting an axis from `AxisId` is type-level
   non-applicability. The ordinary pointwise Pi instances provide its
   semilattice operations.
2. `Readiness Maturity Scope Authority Identity` is a fixed four-field registry.
   Each field is an `Axis A := notApplicable | applicable A`. This tag records
   absence without pretending `N/A` belongs to `A`. Consequently, cross-tag
   values are incomparable; no fake global meet is declared on `Axis A`.

Outcome or verdict is intentionally not a readiness coordinate.

## Homogeneous cap theorem

For finite `V` and a common complete lattice `L`, the formal operator is

```text
F(r)(v) = initial(v) ∧ ⋀ u,
  if edge(u,v) then cap(u,v)(r(u)) else ⊤.
```

Every cap is a bundled monotone map. Feasibility is `r ≤ F(r)`.
Knaster–Tarski proves that `gfp(F)` is fixed and is the greatest feasible
assignment. If `L` is also finite, the antitone chain
`top, F(top), F²(top), ...` stabilizes before the finite state bound and its
stable value is `gfp(F)`.

This is deliberately named `HomogeneousCapSystem`: the manuscript's more
general family of vertex-specific lattices and maps `R_u → R_v` remains
deferred. No DAG one-pass theorem is claimed here.

## Identifiability and finite cover

`Identifies report target` says equal reports force equal target values. The
factorization decoder exists uniquely on `Set.range report`, so no value is
invented for an unattainable report.

For reports `reports : (i : I) → X → Y i`, intervention `i` covers `(x,x')`
when its two typed outputs differ. A selected family identifies the target iff
the union of these distinguishing sets covers every pair where the target
differs. Ordered pairs avoid an unnecessary quotient and yield the same cover
condition. Weighted optimization and complexity are not formalized.

## Approximate monotonicity

The executable finite definition uses natural-valued report discrepancies,
tolerances, and target discrepancies. `oscillation` is the maximum target
discrepancy among pairs compatible with every selected tolerance test. Adding
tests or lowering tolerances shrinks that pair set, so the maximum cannot rise.
No metric axioms are assumed.

## Validation

From this directory:

```powershell
lake build
lake env lean BscCore/Tests.lean
lake env lean BscCore/AxiomAudit.lean
```

The checked-in Lake manifest is authoritative. Run `lake update` only when
intentionally refreshing and reviewing dependency pins, not as a routine
validation step.

`AxiomAudit.lean` prints the transitive axioms of the boundary theorems. Any
project-specific axiom is prohibited. Publication also requires a source scan
for proof placeholders, project axioms, unsafe declarations, non-kernel native
decision shortcuts, and unbounded heartbeat overrides.

## Deliberately deferred

- heterogeneous readiness lattices and endpoint-typed cap transport;
- a separate DAG one-pass evaluator;
- quotient descent beyond the attainable-report subtype factorization;
- weighted set-cover algorithms and complexity claims;
- real- or extended-real oscillation suprema;
- causal deficiency and do-operator commutation;
- a displayed/double category for the complete BSC record;
- application-specific physical postulates and results.

None of these deferred results follows merely from compiling this kernel.
