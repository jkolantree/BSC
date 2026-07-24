# Post-release audit of version 1.0.0

Date: 24 July 2026  
Audited release: `paper-2026-07-24` at commit
`52abd4f3d6dbd048a4c6e6ddbb57e7e428c6bcd4`  
Version DOI: `10.5281/zenodo.21541161`

This was a fresh, adversarial, model-assisted audit conducted after publication.
It is not external peer review. The immutable v1.0.0 record has not been
rewritten. Material repairs are issued as version 1.0.1 with a new version DOI.

## Bottom line

The v1.0.0 bytes, archive, citations, public metadata, privacy boundary, and
eight local fixtures survived integrity review. The central proposal also
survived: a scientific transfer can be audited by keeping state and observable
transport, information loss, target-equation residual, implementation, and
evidence status together.

The audit nevertheless found three material formal defects and several release
engineering defects. They warrant a correction release, not a retraction.

## Material formal findings

| Finding | v1.0.0 effect | v1.0.1 disposition |
|---|---|---|
| Partial observable composition used $T_{\ell m}^{\sharp}\circ T_{mn}^{\sharp}$ even though the inner map lands in $B_b(D_{mn})$, outside the declared domain of the outer map. | BSC-MOR-02 was ill-typed for partial transports. | BSC-MOR-02 remains visibly demoted. BSC-MOR-05 introduces $D_{\ell n}$ and the restricted pullback $T_{\ell m}^{\sharp\mid D_{mn}}$. |
| An accumulated upper bound above tolerance was described as invalidating persistence. | A loose upper bound could be mistaken for proof of violation. | Passing upper enclosures certify; straddling or larger upper bounds merely withdraw certification. Refutation requires an exact value, valid lower bound, or qualified measurement above tolerance. |
| Mathematical status was part of an axiswise meet propagated through the claim DAG. | A false premise could incorrectly manufacture a false descendant verdict. | Mathematical verdict is categorical and claim-local. Only support and other readiness coordinates propagate through edge-specific monotone caps. |
| Two boundary information quantities were called a sufficiency gate. | Undeclared interior predictive information could remain. | They are necessary screens. A declared remainder test $S_{\rm rest}$ is required for target-relative sufficiency. |
| The generic decorated-cospan theorem was phrased too close to a completed BSC-specific construction. | Conditional imported structure could be read as instantiated. | The generic theorem remains proved under its assumptions; constructing the canonical BSC decoration functor is now BSC-OPN-02 and open. |
| The QRF fixture used a correct but weaker two-input presentation. | The obstruction was valid, but the physical state class was less cleanly exposed. | Invariant Bell inputs now have the same reduced state $I/2$ and orthogonal transformed outputs, giving trace distance $1$. |

The audit also typed the filtration on an explicit probability space, narrowed
the selected-extension codomain, qualified zero deficiency when an infimum is
not attained, narrowed the topology-to-charge bridge to claims that actually
make that promotion, and made the unavailable internal-corpus lineage
limitation explicit.

## Release-engineering findings

| Finding | Test that exposed it | v1.0.1 repair |
|---|---|---|
| GitHub displayed Markdown TeX delimiters literally and malformed the central transfer formula. | Rendered-HTML inspection found no math-renderer elements. | All repository Markdown uses GitHub `$...$` and `$$...$$`; CI rejects legacy delimiters. |
| The F8 checker trusted recorded arithmetic and did not parse its schema. | A schema-invalid receipt and a false square-root generator both passed. | The actual schema is parsed and enforced, arithmetic is recomputed independently, schema and script hashes are bound, and both mutants are permanent failing tests. |
| `sha256sum -c` accepted unlisted files. | An extra file left `make verify` green. | The manifest gate rejects missing, extra, duplicate, unsafe, unnormalized, and hash-mismatched paths. |
| CI did not compile the paper or synopsis. | A stale PDF could mask broken source. | CI runs unit tests, complete-set verification, pinned TeX builds, page-count checks, and fatal log scans. |
| Detached PDFs lacked version and DOI. | PDF metadata and visible-page inspection. | Version and DOI are printed in both documents and included in PDF metadata. |
| `main` had no protection. | Public repository/ruleset inspection. | The correction workflow adds protected canonical development after the v1.0.1 checks are established. |
| Mixed licensing was not fully represented by `CITATION.cff`, and early history carried a generic MIT root notice. | History and metadata inspection. | Current file scopes and the historical limitation are explicit; code is MIT and paper/documentation is CC BY 4.0. |

## What passed unchanged

- The immutable GitHub tag and Zenodo v1.0.0 files match their published
  checksums.
- The GitHub archive contains the tagged tree with no traversal paths,
  duplicate members, symlinks, or special files.
- The Zenodo source archive rebuilds the 35-page v1.0.0 paper with matching
  extracted text and page renders.
- The released F8 receipt records the correct counterexample $x=-1$.
- Fixtures F1–F7 are correct exact mathematical derivations, accurately labeled
  as computationally unexecuted.
- No fabricated DOI, unresolved citation key, credential, personal email,
  absolute local path, or undisclosed institution was found.
- The Koopman, QRF, inverse-problem, homogenization, sheaf, formal-proof,
  non-invertible-symmetry, and controlled confinement imports remain scoped to
  their checked sources.
- No manuscript claim establishes holography, QCD, quark charge, hadron
  dynamics, or a universal law of persistence.

## Correction roadmap

1. Preserve v1.0.0 as an immutable historical record.
2. Repair the formal core and keep superseded claim identifiers visible.
3. Harden the executable receipt, complete-set manifest, CI, licensing, and
   detached-document provenance.
4. Rebuild both PDFs, inspect every page, rerun all positive and negative gates,
   and publish the exact checksum-bound tree as v1.0.1.
5. Create a Zenodo version under the existing concept record and verify the
   public GitHub, release, DOI, files, and checksums.
6. Require protected, review-based development for later canonical changes.

Version 1.0.1 executes steps 1–5. Step 6 is a repository administration control
applied after the new checks exist.
