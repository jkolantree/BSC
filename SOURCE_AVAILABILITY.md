# Source availability

The public release includes the complete paper source, bibliography, audit
ledgers, revision memorandum, executable Fixtures F8, F10, and F11, and the
F11 tabular first-descent certificate.

The twelve internal BSC corpus documents from which the manuscript's notation
lineage and repair history were reconstructed are not redistributed here.
Redistribution rights and public canonical locations have not been established
for that corpus. Their basenames, displayed source identities, source status,
and SHA-256 hashes are recorded in
[Supplied_Source_Manifest.csv](provenance/Supplied_Source_Manifest.csv) and in
the original
[hash ledger](provenance/Supplied_Source_SHA256.txt).

The same provenance tables also contain six nonredistributed ASTRA v0.3 audit
records: three PDFs, the source ZIP, its checksum sidecar, and its verification
note. Those records were supplied for a post-release citation-only crosswalk.
They are not part of the twelve-document internal BSC corpus, are not included
in this repository, and do not transfer the ASTRA package's scientific or
licensing authority into BSC.

Consequences:

- The release fixes the identity of the supplied corpus used for this paper.
- Readers can inspect every imported public citation through the bibliography.
- Readers cannot independently replay internal corpus-lineage claims from this
  repository alone.
- Readers likewise cannot replay the ASTRA source-admission audit from this
  repository alone; its six hashes identify external supplied bytes.
- Statements that reproduce the supplied tuple lineage are therefore
  transcriptions from hash-identified internal sources, not independently
  certified public-source facts.
- The displayed identities “Boundary-State Research Program,” “Open Research
  Program,” and related variants reproduce source-document metadata. They are
  not presented as legal institutions or independent reviewing bodies.

Source access may be discussed through repository Issues, subject to
redistribution rights and privacy constraints. A future public corpus deposit
must preserve these hashes or record every changed artifact as a new source
version.

## Post-v1.4.0 BSC Core v1.5 sources

The repository includes every artifact required to replay the declared public
BSC Core v1.5 checks:

- the foundations note, causal-transfer profile, AI-assisted evidence profile,
  prior-art matrix, recent-research intake, and validation report;
- the selected-claim registry and executable readiness graph;
- the F14 and F15 inputs, expected evidence, checkers, and tests;
- the claim-package and readiness evaluators and retained source-bound
  receipts; and
- the complete `formal/bsc_core` Lean source and pinned Lake configuration.

The Lean/mathlib dependency repositories are not vendored. Their exact
versions are pinned by `lean-toolchain`, `lakefile.toml`, and
`lake-manifest.json` and are fetched through the ordinary Lake workflow.
Bibliographic comparisons link to public primary or publisher sources; no
external paper text, proprietary data, model weights, prompts, or source code
is copied into the repository.

The coordinated AI-assisted development history is summarized in the public
validation report, but complete prompts, hidden model state, provider-side
execution records, and every intermediate candidate are not published and are
not reproducible from this repository. They are not required authority for the
retained mathematical proofs, Lean build, finite checks, or package receipts.

This source completeness applies only to the v1.5 milestone artifacts. It does
not make the twelve internal BSC corpus documents or six supplied ASTRA audit
records public, and it does not cure the lineage replay limits described
above. Public SHA-256 values establish artifact identity and integrity, not
confidentiality, authorship, novelty, or scientific validity.
