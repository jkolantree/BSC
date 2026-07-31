# Reproducing version 1.4.0

## Scope

The release manuscript and synopsis can be rebuilt from their shipped LaTeX
sources. Fixtures F8 and F10 can be reproduced byte-for-byte, and Fixture F11
can be replayed and fully re-enumerated, in the pinned Python environment.
Fixture F9 is a mathematical and documentary case study and has no execution
receipt. The immutable release record is
`https://github.com/jkolantree/BSC/releases/tag/v1.4.0`. The Zenodo concept DOI
for the deposited version family is `10.5281/zenodo.21541160`; the v1.4.0
version DOI is assigned only after publication and is recorded on the GitHub
release page. Immutable v1.3.0 remains available at DOI
`10.5281/zenodo.21713285`, immutable v1.2.0 at DOI
`10.5281/zenodo.21711341`, immutable v1.1.0 at DOI
`10.5281/zenodo.21710743`, and immutable v1.0.1 at DOI
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

These hashes describe the immutable v1.1.0 release, not the current v1.4.0
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

## Release v1.3.0 render

The tracked release PDFs include the operational-channel core, the
electromagnetic evidence bridge, the four July 2026 source probes, the exact
binary/constructibility screen, and the Einstein-monotile
selector/materialization result. They were compiled with the same official
Tectonic 0.16.9 Windows MSVC archive and cached dependency bundle recorded
above, with `SOURCE_DATE_EPOCH=1785369600`.

- two independent clean output directories produced byte-identical PDFs;
- paper: 71 pages, SHA-256
  `a45469c2f3695de54b5b3498c1d46445caa34b9623c1cad07c7a0cc9517576ed`;
- synopsis: two pages, SHA-256
  `dff9888788039d60906a13846c2fde49fad11b8bab65af884f30e8e343126b50`;
- all four final logs contain no unresolved citations or references, missing
  glyphs, overfull/underfull boxes, package/class/font warnings, or fatal
  errors;
- the full 71-page release render was inspected as contact sheets; the title,
  energy-port theorem, electromagnetic scope gates, final references, and
  both synopsis pages were inspected at larger scale with no clipping or
  overlap.

The host emitted `Fontconfig error: Cannot load default config file: No such
file: (null)` after each otherwise successful Tectonic run. This external
environment message is retained here rather than silently promoted to a clean
controller claim; the two output pairs were nevertheless byte-identical, the
TeX logs passed the declared warning scan, and the affected pages rendered
without missing glyphs.

These tracked bytes are the v1.3.0 release record. Earlier release hashes
remain immutable in their own tags and deposits.

## Release v1.4.0 render

The tracked release PDFs add the corrected Collatz recursive-sufficiency
audit, its exact full-scan receipt, and the associated claim-status and
provenance boundaries. They were compiled with Tectonic 0.16.9 and its cached
dependency bundle, with `SOURCE_DATE_EPOCH=1785456000`.

- two independent clean output directories produced byte-identical PDFs;
- paper: 75 pages, SHA-256
  `08a5fd3fa6c061d681606b09ae8b93b681b0c148fda70cdce8df70adc387e1ab`;
- synopsis: two pages, SHA-256
  `4f5ba34ec1cbfbe203ada362b64624007b0558a0857919ea6fdee0cf71594f18`;
- all four final logs contain no unresolved citations or references, missing
  glyphs, overfull/underfull boxes, package/class/font warnings, or fatal
  errors;
- all 75 paper pages were inspected as contact sheets, the Collatz transition
  pages were inspected at larger scale, and both synopsis pages were
  inspected at full resolution with no clipping, overlap, or unreadable
  tables.

The host emitted `Fontconfig error: Cannot load default config file: No such
file: (null)` after each otherwise successful Tectonic run. This external
environment message is retained as a controller limitation: both output pairs
were nevertheless byte-identical, the TeX logs passed the declared warning
scan, and the rendered pages contained no missing glyphs.

Accessibility limitation: both PDFs report `Tagged: no`; this release does not
claim tagged-PDF or universal screen-reader conformance.

These tracked bytes are the v1.4.0 release record.

## Refresh and verify the release tree

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
python3 fixtures/F11_collatz_recursive_sieve/check_fixture.py
```

Expected terminal lines:

```text
F8-SQRT-SQUARE-SIGN: PASS
F10-COUPLED-SURROGATE: PASS
F11-COLLATZ-RECURSIVE-SIEVE: PASS
```

Each check parses and validates its shipped JSON Schema and verifies the bound
artifact identities and exact mathematics. F8 and F10 also run their
generators in isolated locations and require byte-identical output. F11's
routine check replays all 52,686 retained rows, recomputes its exact dynamic
program and density arithmetic, and verifies the retained full-scan receipt;
it does not silently repeat the ten-billion enumeration.

For the publication-only F11 completeness gate, run:

```bash
python3 fixtures/F11_collatz_recursive_sieve/check_fixture.py --full-scan
```

Expected terminal line:

```text
F11-COLLATZ-RECURSIVE-SIEVE: FULL-SCAN PASS
```

This tests all 1,388,888,889 compatible candidates and requires exact equality
with the retained ordered offset set. It takes several minutes and is also
run by the GitHub workflow on version tags.

## Run the verification tests

```bash
python3 -m unittest discover -s tests -v
```

The suite retains one schema-invalid F8 mutant and one false-arithmetic F8
mutant. It also rejects F10 mutants with stale host identity, altered horizon,
false tolerance disposition, decimal substitution for an exact rational, and
attempted receipt overwrite. F11 tests reject changed table bytes, false
completeness, wrong nested schema types, a changed self-hash policy, and
attempted receipt overwrite. All must fail. Cheap arithmetic regressions also
recompute the first $F_1\setminus F_2$ residue layer, the exact $31$-class
path, and the fact that the $5/9$ density factor begins at depth two. It
checks that F9 remains documentary and unexecuted,
that the application and central ledger expose the same claim-local
BSC-ZDQ identifier roster, that the primary citation and core scope-boundary
language remain present, and that no F9 receipt is shipped. These are
integration regressions, not a semantic proof that every status vector and
theorem hypothesis agrees across every prose surface.
The scale-framework tests also recompute finite sanity witnesses for rate
addition, total-variation and lower-margin bounds, one certified eta-tail
enclosure, and the two fixed $s$ exponent branches. They are regression tests,
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
glyphs, overfull boxes, or fatal errors. The expected page count is 75.

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

This checks the complete release inventory, all three retained executable
fixtures, negative regressions, and build-verifier tests. Building the PDFs is
a separate target because a full TeX installation is larger than the minimal
verification environment.

For the full gate, including both document builds, run:

```bash
make ci
```

The build gate requires a 75-page paper and two-page synopsis, one final PDF
record per log, and no unresolved reference, citation, font, glyph, box, or
fatal TeX warning.

## Build deterministic release archives

With a verified manifest, build the complete-release and manuscript-source
archives:

```bash
make dist VERSION=1.4.0 SOURCE_DATE_EPOCH=1785456000
```

Run the archive builder again in a separate empty output directory and require
the two runs to be byte-identical before uploading them as release assets. The
builder re-verifies the manifest, rejects unsafe member paths, normalizes ZIP
metadata to the release epoch, and refuses to overwrite an existing archive.

## Source corpus boundary

The twelve supplied corpus documents used to reconstruct BSC's internal
lineage are not included. Their identifiers and SHA-256 hashes are retained in
`provenance/`; see [SOURCE_AVAILABILITY.md](SOURCE_AVAILABILITY.md). Therefore
an external reader can rebuild this release package but cannot
independently replay the complete corpus-lineage audit from this archive
alone.
