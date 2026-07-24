# On Boundaries of Evidence

## Boundary-State Calculus for Typed Observation, Admissible Transfer, and Falsifiable Persistence

**J. Tree · Independent researcher · version 1.0.1 · 24 July 2026**

**Status:** corrected foundational preprint with audit artifacts; not peer
reviewed.

**Canonical repository:** https://github.com/jkolantree/BSC

**Version DOI:** https://doi.org/10.5281/zenodo.21541561

**All versions:** https://doi.org/10.5281/zenodo.21541160

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
| 10 minutes | [Technical synopsis](synopsis/Technical_Synopsis.pdf) | See the formal object, status boundaries, and eight fixtures |
| Field-specific | [Reader map](synopsis/Reader_Map.md) | Go directly to the sections nearest your expertise |
| Full review | [Complete paper](paper/On_Boundaries_of_Evidence.pdf) | Inspect definitions, proofs, fixtures, applications, and references |
| Status audit | [Claim-status ledger](ledgers/Claim_Status_Ledger.md) | Separate mathematical verdict from support and other readiness coordinates |
| Source audit | [Revision memorandum](revision/Revision_Memorandum.md) | See every material repair and unresolved source conflict |
| Release audit | [v1.0.0 audit report](AUDIT_REPORT_v1.0.0.md) | See what survived, what failed, and what v1.0.1 repaired |

## The proposal

The paper proposes a typed transfer record:

$$
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
$$

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
- A two-page technical synopsis and field-specific reader map.
- A symbol and notation ledger, claim-status ledger, and revision memorandum.
- Eight exact mathematical fixtures in §16 of the paper.
- One executable fixture, F8, with one deterministic CPython 3.12.13 receipt.
- A fail-closed checker for that receipt and its parsed JSON Schema, with
  independent semantic recomputation and negative regression tests.
- Reproduction instructions, release metadata, licenses, source-availability
  statement, and file-integrity manifest.
- A complete-set manifest gate that rejects missing, extra, duplicate, unsafe,
  or hash-mismatched release paths.

Fixtures F1–F7 have exact mathematical derivations but no separate execution
receipts. No proof-assistant artifact is included.

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

## Current status boundary

| Object | Verdict | Math support | Empirical | Computational | Transfer |
|---|---|---|---|---|---|
| Repaired partial stochastic composite | True | Proved under stated support and completion hypotheses | N/A | Symbolic, unexecuted | Bounded |
| Generic decorated-cospan theorem | True | Proved under the assumed lax-monoidal functor | N/A | Unexecuted | Bounded |
| Canonical BSC-specific decoration functor | Open | Conditional schema only | N/A | Unexecuted | Blocked |
| Persistent-object principle | Open | Conjectural organizing principle | Untested | Unexecuted | Local only |
| Fixtures F1–F7 | True | Exact mathematical derivations | N/A | Unexecuted | Fixture-local |
| Fixture F8 | True fixture result | Proved counterexample | N/A | One exact receipt | Fixture-local |
| Generic BSC physical validation | Open | No general bridge | Untested | Unexecuted | Blocked |

The complete axis-by-axis record is in the
[claim-status ledger](ledgers/Claim_Status_Ledger.md).

## Verify the retained executable fixture

From the repository root:

```bash
python3 fixtures/F08_sqrt_square_sign/check_fixture.py
```

The checker does not overwrite the retained receipt. It parses the shipped
schema, validates exact types and constants, verifies the claim, schema, and
script hashes, independently recomputes $\sqrt{x^2}=|x|$ in the declared
integer model, runs the generator in a temporary location, and requires
byte-identical output. Negative tests retain the two mutants that the v1.0.0
checker incorrectly accepted.

For the full local verification sequence:

```bash
make verify
```

See [REPRODUCING.md](REPRODUCING.md) for the pinned environment and build
commands.

## Repository map

```text
paper/        manuscript PDF and editable source
synopsis/     two-page synopsis, source, and reader map
ledgers/      claim status and notation
fixtures/     executable F8 artifact, receipt, schema, and checker
revision/     explicit definition repairs and unresolved obligations
provenance/   supplied-corpus identity records
tools/        complete-set manifest and release verification
tests/        positive and negative release-gate regressions
```

## Citation, disclosure, and licensing

Machine-readable citation metadata is in [CITATION.cff](CITATION.cff).
The version 1.0.1 DOI is
[10.5281/zenodo.21541561](https://doi.org/10.5281/zenodo.21541561).
The concept DOI
[10.5281/zenodo.21541160](https://doi.org/10.5281/zenodo.21541160)
resolves to the latest published version. The immutable v1.0.0 DOI remains
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
