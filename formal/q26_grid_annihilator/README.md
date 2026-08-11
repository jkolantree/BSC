# Q26 grid-annihilator formalization

This pinned Lean project proves the unrestricted theorem

```lean
Q26GridAnnihilator.no_thirteen_queen_dominator :
  ¬ ∃ queens : Finset Square, Dominates queens ∧ queens.card = 13
```

The proof does not assume the earlier `WeakleyCanonicalRealization`. From an
arbitrary thirteen-queen dominator it constructs the actual row/column/color
parity shadow, applies arbitrary-cardinality occurrence-polynomial
Nullstellensatz bounds, and checks the exact finite roster: 36 shadows, split
as 32 bichromatic and four monochromatic.

The bichromatic branch is closed by exact grid-moment identities. In the
monochromatic branch, all four parity orientations are normalized to a
permutation of thirteen rows and columns. A least-omitted-diagonal shell then
forces either the impossible second moment `4004 = 3276`, a full symmetric
difference shell contradicting the fixed difference sum, or the checked
endpoint equation

```text
(2*a - 13)^2 + 12*(2*h - 13)^2 = 741,
```

which has no admissible integer solution. The earlier conditional
five-profile theorem remains available as a regression theorem, but is no
longer the bridge for the unrestricted result.

The unrestricted Q26 root-CNF proof status is a separate evidence track and
remains **UNKNOWN**. This Lean theorem is not an LRAT/DRAT replay receipt and
does not promote that CNF receipt to UNSAT.

## Reproducible environment

- Lean: `leanprover/lean4:v4.32.1`
- Mathlib: `520045ab14e26149ee970e2e617ca04b09bde5d6`
- The generated `lake-manifest.json` records the full dependency closure.

With the pinned toolchain available:

```text
lake update
lake exe cache get
lake build
lake env lean Q26GridAnnihilator/AxiomAudit.lean
```

The final command reports `[propext, Classical.choice, Quot.sound]` for the
unrestricted theorem and its algebraic/geometric chain. Exact finite roster
computations such as `exact_shadow_stats` report no axioms. The project
sources use no `sorry`, `admit`, project-defined `axiom`, `native_decide`, or
unlimited heartbeat setting.
