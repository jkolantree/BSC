# BSC Core v1.5 — internal adversarial validation report

**Candidate:** *BSC Core v1.5 — Identifiability, Causal Transfer, and
Auditable Evidence*

**Audit date:** 15 August 2026

**Repository base:** `906acc87e6927255974012f1e1dd0b64ec5e5516`

**Review class:** correlated internal AI-assisted review lanes, not outside
human referees and not independent replication

## What this report establishes

This report records an adversarial review of the selected v1.5 milestone
claims and the repairs made before publication. The machine-readable claim
registry remains the authoritative list of selected statements, verdicts,
dependencies, evidence paths, and authority ceilings. The retained package
receipt binds its final bytes.

An `internal-adversarial-complete` readiness value means that the named
internal review work below was completed. It does **not** mean external peer
review, non-collusive replication, novelty clearance, or empirical
validation. Node verdicts and initial readiness values in the graph are
curator-supplied premises. The evaluator checks cap propagation and byte
relationships; it does not prove those premises.

## Review lanes

| Lane | Primary attack surface | Independence boundary |
|---|---|---|
| Foundations and prior art | theorem hypotheses, false equivalences, novelty language, direct antecedents | Separate reasoning pass over the prose and cited primary sources; still an AI lane in the same coordinated audit |
| Formal correspondence | exact proposition encoded, applicability typing, theorem scope, axioms, prohibited constructs | Lean kernel checking plus statement-to-prose review; bundled `leanchecker` is same-implementation replay, not an external checker |
| Executable and security | exhaustive arithmetic, alternative finite criteria, parser and resource abuse, deterministic output | F14 replays the same implementation with internal criteria; F15 adds exhaustive enumeration but shares parsing/model code; neither is called an independent implementation |
| Claim graph and publication | dependency completeness, readiness semantics, evidence binding, navigation, rendering, stale global statements | Separate repository-level audit; not a mathematical referee report |

## Material findings and resolutions

1. **Verdict was initially inside readiness.** The Lean draft originally put
   outcome polarity in the readiness product and encoded applicability at the
   whole-record level. The repair removes verdict/outcome from readiness,
   provides per-axis applicability, and makes cross-applicability comparisons
   false.
2. **Broad and kernel-checked cap theorems were conflated.** The heterogeneous
   finite theorem is now `BSC-RDY-02` with human-proof-recorded support. The
   Lean theorem is separately frozen as `BSC-RDY-03`: a homogeneous common
   complete-lattice system, with finite descending stabilization when both
   the vertex set and lattice are finite.
3. **Several formal labels exceeded the encoded proposition.** The Lean map
   now distinguishes finite pair cover from weighted optimization and records
   both added-report and tightened-tolerance oscillation monotonicity. The
   formal README explicitly lists every deferred generalization.
4. **Readiness axes forced unrelated gates into non-cumulative chains.** The
   graph labels are now cumulative gate bundles. `unproved` is the bottom of
   the formal axis, and the open category claim no longer carries a prose-proof
   label.
5. **The dependency projection was incomplete.** Registry dependencies and
   graph edges are now required to agree exactly; omitted causal, readiness,
   and identifiability edges are a hard failure.
6. **Fixture replay was overstated as independent.** F14 is labeled a
   same-implementation replay with internal cross-check criteria. F15 is an
   exhaustive shared-model cross-check. The documentation and provenance use
   those exact descriptions.
7. **Hostile JSON could escape through resource or parser errors.** Both tools
   now bound bytes, nesting, item counts, string lengths, integer digits,
   combinatorial work, and output size. Malformed inputs fail on standard
   error without tracebacks or local-path disclosure.
8. **Causal deficiency was under-specified.** The foundations now require a
   nonempty aligned parameter index, standard-Borel spaces, all Markov
   kernels for the ordinary deficiency claim, measurable bounded loss, and
   explicit Markov decision rules and risk. Restricted kernel classes are
   named as a different construction and require composition closure for a
   triangle inequality.
9. **The closest statistical antecedent was missing.** The prior-art matrix
   now includes Le Cam's approximate sufficiency and Torgersen's comparison
   of statistical experiments. Novelty remains `unknown`.
10. **Hash language risked implying confidentiality.** The evidence profile
    now states that public hashes support integrity and identity, not secrecy.
11. **Verdict fields mixed truth with maturity.** Early graph drafts used
    `proposed` for normative profiles and `unknown` for novelty. The closed
    verdict vocabulary now uses `N/A` for the two profiles and `open` for the
    unresolved novelty and category claims; schemas, tools, and tests enforce
    that separation.
12. **Ledger rows conflated formal and computational evidence.** Duplicate
    F14/F15 identifiers were removed, Lean-only claims no longer inherit an
    `executed` computation label, and F14 is described as a retained report
    rather than an exact receipt.
13. **The F15 schema was documentary but described as checked.** Its fixture
    checker now parses and validates the structural receipt schema, and the
    selected-claim package binds the schema and provenance record.
14. **A recent-research summary overstated a formal causal result.** The
    Sargsyan entry now attributes machine checking only to sieve
    classification, pullback gluing, and Kripke–Joyal forcing in the new
    1-topos core; it separately identifies the previously verified
    probability/do-calculus substrate.

## Verified finite results

The finite arithmetic was recomputed from the canonical inputs rather than
copied from the prose:

- F14 evaluates all eight intervention families. Its exact minimum cost is
  `2`; the minimizers are `direct` and `column` plus `row`; the selected
  tolerant direct report has target oscillation `3/2`.
- F15 has exactly `84` feasible readiness assignments below its declared
  ceilings. The retained fixed point is componentwise greatest, and the
  synchronous descent changes four times before stabilizing.

The focused hostile and positive test suites pass `23/23` intervention tests
and `12/12` readiness tests. The retained F14 report and F15 receipt replay
exactly.

## Lean boundary

The project is pinned to Lean `4.33.0` at commit
`d8b18978322de05a8f3dba51ef03cf5461676c17` and mathlib `v4.33.0` at commit
`db584cd6d46c92f209a44c0f1c829460d327499d`. A full `lake build` completed
successfully with 800 jobs, the public tests elaborated, and the axiom audit
reported only the standard Lean axioms `propext`, `Classical.choice`, and
`Quot.sound` where used. The source scan found no `sorry`, `admit`,
project-defined axiom, unsafe declaration, native decision shortcut, or
unbounded heartbeat override.

The exact formal boundary is:

- coordinatewise meet/top for one active-axis signature;
- per-axis non-applicability and no verdict coordinate;
- the homogeneous cyclic greatest-feasible fixed point and its finite
  stabilization specialization;
- unique factorization through attainable reports;
- finite heterogeneous-report pair-cover equivalence; and
- finite natural-valued oscillation monotonicity under added reports and
  tightened tolerances.

It does not include the heterogeneous cap theorem, DAG one-pass corollary,
weighted optimization, real-valued suprema, causal deficiency, physical
models, or the full BSC category.

## Residual limits

- No outside human mathematical referee participated in this milestone.
- Universal novelty, priority, and literature completeness remain unknown.
- The causal-transfer and AI-assisted evidence profiles are proposed
  certificate disciplines, not validated scientific models.
- No new empirical data or application-level physical validation is supplied.
- The full eight-field categorical coherence theorem remains open.
- Machine validation of a selected registry never substitutes for checking
  the frozen mathematical statement itself.

These limits are publication boundaries, not unfinished hidden claims.
