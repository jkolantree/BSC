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

- Lean: `leanprover/lean4:v4.32.2`
- Mathlib: `905b95818eb32af7874a58b427f50c1711a5e96c`
- The generated `lake-manifest.json` records the full dependency closure.

With the pinned toolchain available:

```text
lake update
lake exe cache get
lake build
lake env lean Q26GridAnnihilator/AxiomAudit.lean
lake env leanchecker Q26GridAnnihilator.Unconditional
```

`AxiomAudit.lean` reports `[propext, Classical.choice, Quot.sound]` for the
unrestricted theorem and its algebraic/geometric chain. Exact finite roster
computations such as `exact_shadow_stats` report no axioms. `leanchecker`
replays the target module through the patched Lean 4.32.2 kernel; it is a
second Lean-kernel replay, not an independent checker implementation.

The repository CI builds the tracked project, runs the patched-kernel module
replay, and prints the axiom audit. This CI path does not claim an independent
checker implementation. The imported proof sources use no `sorry`, `admit`,
project-defined `axiom`, `native_decide`, or unlimited heartbeat setting. (The
separate verifier-controlled challenge is documented below.) The tracked
commit and `MANIFEST.sha256`, rather than the hash of
`Unconditional.lean` alone, bind the complete local import closure.

The separate [external validation receipt](../../applications/Q26_lean_4_32_2_validation.json)
records a pinned, landrun-sandboxed Comparator run with nanoda enabled. Both
the Lean 4.32.2 kernel and the independently implemented nanoda kernel accepted
the theorem while permitting only `propext`, `Quot.sound`, and
`Classical.choice`. Its [source projection](../../applications/Q26_lean_4_32_2_source_sha256.txt)
binds all 26 proof-project Lean files (the theorem sources and audit modules)
plus `lean-toolchain`, `lakefile.toml`, and `lake-manifest.json`. The separate
verifier-controlled challenge is bound by its hash in the Comparator receipt;
the receipt also records the distinct local `leanchecker --fresh` timeout as
`NOT_CHECKED`, not as a pass. The compact [Comparator bundle](validation/README.md)
retains the trusted challenge, configuration, transcript, and reproduction
script.
