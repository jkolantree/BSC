# Reproducing development version 1.3.0-dev

## Scope

The current development manuscript and synopsis can be rebuilt from their
shipped LaTeX sources. Fixtures F8 and F10 can be reproduced byte-for-byte in
the pinned Python environment. Fixture F9 is a mathematical and documentary
case study and has no execution receipt. This working tree is not a release or
Zenodo deposit. The latest immutable release record is
`https://github.com/jkolantree/BSC/releases/tag/v1.2.0`. The Zenodo concept DOI
for the deposited version family is `10.5281/zenodo.21541160`; the v1.2.0
version DOI assigned after the tagged bytes were built is
`10.5281/zenodo.21711341`. Immutable v1.1.0 remains available at DOI
`10.5281/zenodo.21710743`, and immutable v1.0.1 remains available at DOI
`10.5281/zenodo.21541561`.
Fresh PDF builds are not generally claimed to be byte-identical because PDF timestamps
and trailer identifiers may vary. Reproduction of the paper means matching
content, pagination, references, and visual layout.

## Canonical verification environment

- TeX Live 2023/Debian
- pdfTeX 1.40.25
- latexmk 4.83
- BibTeX 0.99d
- CPython 3.12.13

## Published v1.1.0 render

The tracked PDFs in this release were compiled and
visually inspected with Tectonic 0.16.9. The official Windows MSVC archive had
SHA-256
`131a24604785a9600989a3d91225f597df52ac06f00aeffe86fd529f99ee5cdd`.
With `SOURCE_DATE_EPOCH=1785369600`, two independent builds were byte-identical
and produced a 50-page paper and a two-page synopsis:

- paper SHA-256:
  `7223ff840a098ad90239b96319463af4b948cbcea3eec4a16e3c8ed0d523b460`;
- synopsis SHA-256:
  `446e523b835bde5bba8cc417213016d60e4f657f64f92e0efe5e72f61d8710dd`.

This independent render check does not replace the canonical `make ci` release
gate above. GitHub Actions runs that gate for pull requests, `main`, and
version tags.

These hashes describe the immutable v1.1.0 release, not the current v1.2.0
release PDFs.

## Release v1.2.0 render

The tracked release PDFs were rebuilt after the source changes and are
recorded below. Their hashes and page counts are part of the v1.2.0 release
verification.

- renderer: Tectonic 0.16.9 using its cached dependency bundle;
- paper: 56 pages, SHA-256
  `106631826fc417549d68927418759b856e5610c7c0c27ab53c33665994a60b8c`;
- synopsis: two pages, SHA-256
  `1900a525c66e92cf925de142ed2f7f11447b7af13a36298829d5156ff8965b5c`;
- build logs: no unresolved citations or references, missing glyphs,
  overfull/underfull boxes, package/class/font warnings, or fatal errors;
- visual inspection: title, simulation-evidence definitions and theorem,
  F10, final references, and both synopsis pages checked without clipping or
  overlap.

Accessibility limitation: both PDFs report `Tagged: no`. The inspected paper
fonts embed ToUnicode maps except CMSY10 and CMEX10, so mathematical-symbol
extraction remains tool-dependent even though ordinary text extraction is
available. No tagged-PDF or universal screen-reader claim is made.

## Development 1.3.0-dev render

The tracked development PDFs include the operational-channel core, the
electromagnetic evidence bridge, the four July 2026 source probes, the exact
binary/constructibility screen, and the Einstein-monotile
selector/materialization result. They were compiled with the same official
Tectonic 0.16.9 Windows MSVC archive and cached dependency bundle recorded
above, with `SOURCE_DATE_EPOCH=1785369600`.

- two independent clean output directories produced byte-identical PDFs;
- paper: 69 pages, SHA-256
  `fc2c2869ad07e2278131fa3a7a38160aa03342408b1cf7878fc869aa2553117a`;
- synopsis: two pages, SHA-256
  `cf3b8af28c8d020d91f491f9e52deadaf24948b604d41cbbdcc91d0670bb55be`;
- all four final logs contain no unresolved citations or references, missing
  glyphs, overfull/underfull boxes, package/class/font warnings, or fatal
  errors;
- the full 69-page development render was inspected as contact sheets; after
  the final source-precision corrections, changed paper pages 40--41 and both
  synopsis pages were re-rendered and inspected at larger scale with no
  clipping or overlap.

The host emitted `Fontconfig error: Cannot load default config file: No such
file: (null)` after each otherwise successful Tectonic run. This external
environment message is retained here rather than silently promoted to a clean
controller claim; the two output pairs were nevertheless byte-identical, the
TeX logs passed the declared warning scan, and the affected pages rendered
without missing glyphs.

These bytes are a development candidate, not a GitHub release or Zenodo
deposit. The v1.2.0 hashes above remain the immutable release record.

## Refresh and verify the development tree

After an intentional source change, regenerate the complete-set manifest:

```bash
python3 tools/update_manifest.py
```

Then verify it:

```bash
python3 tools/verify_manifest.py
```

The updater uses the same inventory rules as the verifier. The complete-set
gate rejects missing, extra, duplicate, unsafe, unnormalized, symlinked,
special, and hash-mismatched payload paths. The manifest omits itself.

## Verify the retained executable fixtures

```bash
python3 fixtures/F08_sqrt_square_sign/check_fixture.py
python3 fixtures/F10_coupled_surrogate/check_fixture.py
```

Expected terminal line:

```text
F8-SQRT-SQUARE-SIGN: PASS
F10-COUPLED-SURROGATE: PASS
```

Each check parses and validates its shipped JSON Schema, verifies bound
identities, independently recomputes the exact mathematics, refuses to
overwrite the retained receipt, runs the generator in an isolated location,
and requires byte-identical output.

## Run the verification tests

```bash
python3 -m unittest discover -s tests -v
```

The suite retains one schema-invalid F8 mutant and one false-arithmetic F8
mutant. It also rejects F10 mutants with stale host identity, altered horizon,
false tolerance disposition, decimal substitution for an exact rational, and
attempted receipt overwrite. All must fail. It checks that F9 remains documentary and
unexecuted,
that the application and central ledger expose the same claim-local
BSC-ZDQ identifier roster, that the primary citation and core scope-boundary
language remain present, and that no F9 receipt is shipped. These are
integration regressions, not a semantic proof that every status vector and
theorem hypothesis agrees across every prose surface.
The scale-framework tests also recompute finite sanity witnesses for rate
addition, total-variation and lower-margin bounds, one certified eta-tail
enclosure, and the two fixed-$s$ exponent branches. They are regression tests,
not proofs of the limiting theorems or executions of F9.

## Build the paper

```bash
make paper
```

Output:

```text
build/paper/On_Boundaries_of_Evidence.pdf
```

The final LaTeX log must contain no unresolved citations or references, missing
glyphs, overfull boxes, or fatal errors. The expected page count is 69.

## Build the synopsis

```bash
make synopsis
```

Output:

```text
build/synopsis/Technical_Synopsis.pdf
```

The expected page count is 2.

## Run the complete local gate

```bash
make verify
```

This checks the complete release inventory, both retained executable fixtures,
negative regressions, and build-verifier tests. Building the PDFs is a separate
target because a full TeX installation is larger than the minimal verification
environment.

For the full gate, including both document builds, run:

```bash
make ci
```

The build gate requires a 69-page paper and two-page synopsis, one final PDF
record per log, and no unresolved reference, citation, font, glyph, box, or
fatal TeX warning.

## Build deterministic development archives

With a verified manifest, build the complete-release and manuscript-source
archives:

```bash
make dist VERSION=1.3.0-dev SOURCE_DATE_EPOCH=1785369600
```

These archives are candidates for review, not published release assets. Run
the archive builder again in a separate empty output directory and require
the two runs to be byte-identical. The builder re-verifies the manifest,
rejects unsafe member paths, normalizes ZIP metadata to the release epoch, and
refuses to overwrite an existing archive.

## Source corpus boundary

The twelve supplied corpus documents used to reconstruct BSC's internal
lineage are not included. Their identifiers and SHA-256 hashes are retained in
`provenance/`; see [SOURCE_AVAILABILITY.md](SOURCE_AVAILABILITY.md). Therefore
an external reader can rebuild this release package but cannot
independently replay the complete corpus-lineage audit from this archive
alone.
