# On Boundaries of Evidence

## Boundary-State Calculus for Typed Observation, Admissible Transfer, and Falsifiable Persistence

**J. Tree · Independent researcher**

**Latest released version:** v1.2.0 · 30 July 2026.

**Repository state:** version 1.2.0 release.

**Release status:** v1.2.0 is a foundational preprint with mathematical
framework, audit artifacts, and explicit claim boundaries; not peer reviewed.

**Canonical repository:** https://github.com/jkolantree/BSC

**Version record:** https://github.com/jkolantree/BSC/releases/tag/v1.2.0

**Zenodo concept DOI (all deposited versions):**
https://doi.org/10.5281/zenodo.21541160

Scientific claims often fail in the crossing between two otherwise valid
descriptions. Boundary-State Calculus (BSC) treats that crossing as a typed,
inspectable, and falsifiable object.

> BSC audits one claimed transfer: what moves, what is lost, what still
> satisfies the target equations, what physically implements the move, and
> what evidence licenses the resulting claim.

The unit of evaluation is not the universe. It is one claimed transfer.

## Start here

| Time | Read | Purpose |
|---|---|---|
| 2 minutes | This page | Understand the claim and its limits |
| 10 minutes | [Technical synopsis](synopsis/Technical_Synopsis.pdf) | See the formal object, status boundaries, and fixture set |
| Field-specific | [Reader map](synopsis/Reader_Map.md) | Go directly to the sections nearest your expertise |
| Full review | [Complete paper](paper/On_Boundaries_of_Evidence.pdf) | Inspect definitions, proofs, fixtures, applications, and references |
| Framework module | [Normalized scale profiles](framework/Normalized_Scale_Profiles.md) | Inspect the reusable finite-family, rate, singularity, zero-transfer, and decision mathematics |
| Framework module | [Simulation evidence profiles](framework/Simulation_Evidence_Profile.md) | Inspect intended-use records, statistical evidence, compatibility reserves, and coupled-surrogate propagation |
| Status audit | [Claim-status ledger](ledgers/Claim_Status_Ledger.md) | Separate mathematical verdict from support and other readiness coordinates |
| Source audit | [Revision memorandum](revision/Revision_Memorandum.md) | See every material repair and unresolved source conflict |
| Release audit | [v1.0.0 audit report](AUDIT_REPORT_v1.0.0.md) | See what survived, what failed, and what v1.0.1 repaired |

## The proposal

The paper proposes a typed transfer record:

```math
\mathfrak M_{\ell\to m}
=
\left(
T_{\ell m},
T_{\ell m}^{\sharp},
K_{\ell m},
R_{\ell m},
\Theta_{\ell m},
\delta_{\ell m},
C_{\ell m},
\mathsf{Cert}_{\ell m}
\right).
```

It keeps together:

- state transport;
- reverse-direction observable transport;
- observation post-processing or statistical simulation;
- target-equation residual;
- naturality or commuting-square defect;
- directed Blackwell–Le Cam deficiency;
- physical carrier, controller, instrument, reference frame, clock, and
  boundary conditions; and
- assumptions, tolerances, sources, proofs or execution artifacts, hashes,
  unresolved obligations, and status.

The originality claim is deliberately narrow: BSC proposes a joint contract
among established mathematical primitives and supplies composition and
demotion semantics for that contract. It does not claim that each primitive is
new, or that no equivalent formalism exists.

## What this is not

BSC is not presented as:

- a fundamental ontology or unified field theory;
- proof of holography, quantum gravity, consciousness, QCD, quark charge, or
  hadron dynamics;
- a proof of the Riemann Hypothesis, an independent physical origin for it, or
  a demonstrated end-to-end quantum advantage;
- a universal law of persistence;
- a claim that every boundary determines an interior;
- a single total error score;
- a machine-checked formalization; or
- a complete reference implementation.

The paper's strongest present territory is the grammar governing when boundary
data, representation change, topology, learned operators, scale transfer,
recurrence, or duality earns the right to support a target claim.

## Available now

- A reviewer-facing preprint and editable LaTeX/BibTeX source.
- Standalone framework modules for certified finite scale families,
  normalization collapse, logarithmic-rate decomposition and stability,
  singular-set and slice visibility, analytic zero transfer, and
  exact-decision bounds; and for claim-relative simulation evidence,
  statistical coverage, factored identity, compatibility-bounded deployment,
  and coupled-surrogate propagation.
- A two-page technical synopsis and field-specific reader map.
- A symbol and notation ledger, claim-status ledger, and revision memorandum.
- Ten exact mathematical fixtures in version 1.2.0; immutable v1.1.0 contains
  nine and immutable v1.0.1 contains eight.
- Two executable fixtures, F8 and F10, with deterministic CPython 3.12.13
  receipts.
- Fail-closed checkers for those receipts and their parsed JSON Schemas, with
  independent semantic recomputation and negative regression tests.
- Reproduction instructions, release metadata, licenses, source-availability
  statement, and file-integrity manifest.
- A complete-set manifest gate that rejects missing, extra, duplicate, unsafe,
  or hash-mismatched release paths.

Fixtures F1–F7 and F9 have exact mathematical derivations
but no separate execution receipts. F9 checks only the finite engineered
zeta–coherence identity; it does not execute the application-level analytic
transfer and is not an NMR-data replay. F10 executes only its declared exact
finite recurrence; it is not empirical or physical validation of a surrogate
model. No proof-assistant artifact is included.

## How to evaluate the contribution

The most useful first responses are:

1. an existing formalism that already provides an equivalent joint record and
   semantics;
2. one ill-typed map or missing hypothesis;
3. a counterexample to a composition law or fixture;
4. a case in which the added record changes no scientific decision; or
5. a nearby valid transfer that the calculus incorrectly blocks.

If established work already supplies the same obligations and demotion
semantics—or if the record never distinguishes an invalid transfer from a
nearby valid one—the additional structure is unnecessary.

Use the repository issue forms for
[prior art](.github/ISSUE_TEMPLATE/prior-art-equivalence.yml),
[type or proof errors](.github/ISSUE_TEMPLATE/type-or-proof-error.yml),
[fixture failures](.github/ISSUE_TEMPLATE/fixture-failure.yml), or
[scope corrections](.github/ISSUE_TEMPLATE/scope-correction.yml).

## Normalized-scale framework and zeta–DQPT instance

Version 1.1.0 adds a reusable normalized-scale profile to the
core calculus and applies it to Wei et al.'s engineered correspondence between
finite quantum observables, the
Riemann zeta function, and dynamical quantum phase transitions
([DOI 10.1038/s41467-026-74935-8](https://doi.org/10.1038/s41467-026-74935-8)).
The general layer separates a carrier $A_N$, nonzero normalizer $Z_N$,
normalized observable $L_N$, logarithmic size gauge, ideal parameter-space
rate, physical parameter slice, and estimator law. It proves normalization
collapse, additive rate signatures, normalization covariance, lower-margin
rate stability, singular-set and slice-visibility theorems,
contour-certified zero transfer, multiplicity-sensitive local root transfer,
and deterministic and stochastic exact-decision bounds. It does not
manufacture an infinite-system state or a physical phase transition from a
finite family.

The zeta instance proves the declared finite alternating-sum identity, an
explicit local-uniform tail bound, the fixed-$s$ decay-exponent split between
zeros and nonzeros, the corresponding pointwise free-energy values and exact
rate-singularity set for $N=2^d$, the exact fixed-$\beta$ real-time
singularity slice, a sharp local finite-root drift, and a bounded zero-count
transfer conditional on a certified whole-contour separation. Confining every
rate singularity to the critical line is an exact re-encoding of RH, not a
proof of it. The release records the five-qubit NMR result as one
source-reported study and blocks promotion from finite agreement to exact zero
certification, a thermodynamic singularity, the universal Riemann Hypothesis,
a comparator-independent quantum advantage, a unique Kelvin temperature, or
an independent physical-origin claim.

No raw-data replay, fitting re-execution, hardware run, or complexity benchmark
has been performed in this repository. The inspected Nature Communications
source was an unedited article-in-press version, so the citation state is also
recorded rather than silently treated as final typeset text.

## Simulation-evidence framework

Version 1.2.0 adds a claim-relative simulation-evidence profile
without changing the eight-field BSC morphism. It separates statistical
simulation, computational simulation, and surrogate deployment; records
intended use, typed source estimands and target BSC losses, hard gates,
estimators, a joint observation law, sampling or oracle models, joint
coverage, optimization gaps, proxy-transfer theorems, and factored evidence
identity; and proves compatibility-bounded deployment after monotone,
unit-respecting propagation:

```math
\ell^{\mathrm{dep}}_{c,j}
\le \ell^0_{c,j}+\rho_{c,j},
\qquad
U^0_{c,j}+\rho_{c,j}\le\tau_{c,j}.
```

Frozen-state estimator uncertainty already enclosed by $U^0_{c,j}$ is not
counted again in $\rho_{c,j}$; uncertainty in estimating the deployment
change is represented exactly once. Quantities with different units are
combined only through a declared propagation map. An implemented statistical
channel gives an upper bound on directed deficiency; it does not establish
the optimum or a lower bound. A zero declared failure probability is only a
probability-one statement unless the bounds hold pointwise.

The finite-horizon specialization shows why standalone surrogate accuracy
does not determine coupled-host accuracy. Executable Fixture F10 uses the same
exact interface error $1/100$ in two stable hosts for ten steps. Host A
($a=1/2$) remains within tolerance with exact maximum error $1023/51200$;
Host B
($a=9/10$) first violates the $1/20$ tolerance at step 7 and ends at
$6513215599/100000000000$. This is a deterministic code-verification result
for that recurrence and loss coordinate, not full BSC admissibility, physical
validation, or a general surrogate guarantee. The V&V disciplines and
finite-horizon coupling mechanism are prior art; BSC's narrower contribution
is their typed integration, transfer authority, and local demotion semantics.

## Current status boundary

| Object | Verdict | Math support | Empirical | Computational | Transfer |
|---|---|---|---|---|---|
| Repaired partial stochastic composite | True | Proved under stated support and completion hypotheses | N/A | Symbolic, unexecuted | Bounded |
| Normalized-scale profile theorems | True | Normalization collapse, additive rates, covariance, singular support, slice visibility, and analytic zero transfer proved | N/A | Unexecuted | Certified |
| Simulation-evidence profile | True | Typed source-to-loss propagation, joint coverage obligations, factored identity, compatibility-bounded deployment, and coupled-surrogate propagation proved | N/A | Unexecuted | Bounded |
| Exact finite-label observation decoding | True | Measurable-partition criterion and total-variation lower bound proved | N/A | Unexecuted | Certified |
| Generic decorated-cospan theorem | True | Proved under the assumed lax-monoidal functor | N/A | Unexecuted | Bounded |
| Canonical BSC-specific decoration functor | Open | Conditional schema only | N/A | Unexecuted | Blocked |
| Persistent-object principle | Open | Conjectural organizing principle | Untested | Unexecuted | Local only |
| Fixtures F1–F7 | True | Exact mathematical derivations | N/A | Unexecuted | Fixture-local |
| Fixture F8 | True fixture result | Proved counterexample | N/A | One exact receipt | Fixture-local |
| Fixture F9: zeta–DQPT scope audit | True fixture result | Finite identity proved; application-level scaling and contour theorems are not fixture executions | N/A | Unexecuted | Fixture-local |
| Fixture F10: coupled-surrogate host dependence | True fixture result | Equal standalone error yields different exact host-relative tolerance disposition under two stable recurrences | N/A | One exact receipt | Fixture-local |
| Finite-resolution observation decides exact zero | False | Query fails operational descent when zero and nonzero amplitudes are confusable | N/A | Unexecuted | Blocked |
| Finite evidence entails limiting DQPT exclusivity or RH | False | Limit, zero-census, and universal quantifier are not discharged | Single study | Unexecuted | Blocked |
| End-to-end quantum advantage | Open | Conditional resource comparison only | Untested | Unexecuted | Blocked |
| Independent physical origin or unique Kelvin temperature | Not established | No causal/ontological or energy-unit/calibration bridge | N/A | Unexecuted | Blocked |
| Generic BSC physical validation | Open | No general bridge | Untested | Unexecuted | Blocked |

The complete axis-by-axis record is in the
[claim-status ledger](ledgers/Claim_Status_Ledger.md).

## Verify the retained executable fixtures

From the repository root:

```bash
python3 fixtures/F08_sqrt_square_sign/check_fixture.py
python3 fixtures/F10_coupled_surrogate/check_fixture.py
```

Neither checker overwrites its retained receipt. Each parses the shipped
schema, validates exact types and constants, verifies bound identities,
independently recomputes the declared mathematics, runs its generator in a
temporary location, and requires byte-identical output. Negative tests retain
the two F8 mutants that the v1.0.0 checker incorrectly accepted and add stale
host, altered-horizon, false-tolerance-disposition, decimal-substitution, and
overwrite controls for F10.

For the full local verification sequence:

```bash
make verify
```

See [REPRODUCING.md](REPRODUCING.md) for the pinned environment and build
commands.

## Repository map

```text
paper/        manuscript PDF and editable source
framework/    reusable normalized-scale and simulation-evidence mathematics
synopsis/     two-page synopsis, source, and reader map
ledgers/      claim status and notation
fixtures/     mathematical fixtures plus executable F8 and F10 receipts
revision/     explicit definition repairs and unresolved obligations
provenance/   supplied-corpus identity records
tools/        complete-set manifest and release verification
tests/        positive and negative release-gate regressions
```

## Citation, disclosure, and licensing

Machine-readable citation metadata is in [CITATION.cff](CITATION.cff).
Version 1.2.0 is published in the immutable
[GitHub release record](https://github.com/jkolantree/BSC/releases/tag/v1.2.0).
The concept DOI
[10.5281/zenodo.21541160](https://doi.org/10.5281/zenodo.21541160)
identifies all deposited versions and resolves to the latest Zenodo deposit.
Any v1.2.0 version DOI assigned after deposit is recorded on the GitHub release
page rather than anticipated in these tagged bytes. The immutable v1.1.0
version DOI is
[10.5281/zenodo.21710743](https://doi.org/10.5281/zenodo.21710743).
The immutable v1.0.1 DOI is
[10.5281/zenodo.21541561](https://doi.org/10.5281/zenodo.21541561), and the
immutable v1.0.0 DOI remains
[10.5281/zenodo.21541161](https://doi.org/10.5281/zenodo.21541161).

Material generative assistance and its limits are recorded in
[DISCLOSURE.md](DISCLOSURE.md). Automated or model-assisted checks are not
independent peer review.

Paper and documentation are licensed under
[CC BY 4.0](LICENSES/paper-and-documentation.txt). Code and machine-readable
fixture tooling are licensed under the [MIT License](LICENSES/code.txt).
The supplied internal source corpus is not redistributed by this repository.
The [license map](LICENSES/README.md) also records the historical clarification
for commits preceding the explicit dual-license notice.

## Contact

Use this repository's Issues. A citation, counterexample, type correction, or
one-sentence scope correction is a complete and valuable contribution.
