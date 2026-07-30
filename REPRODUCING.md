# Building development draft 1.1.0-dev

## Scope

The manuscript and synopsis can be rebuilt from their shipped LaTeX sources.
Fixture F8 can be reproduced byte-for-byte in the pinned Python environment.
Fixture F9 is a mathematical and documentary case study and has no execution
receipt. The immutable released version 1.0.1 remains available at DOI
`10.5281/zenodo.21541561`; this development tree does not claim that DOI.
Fresh PDF builds are not claimed to be byte-identical because PDF timestamps
and trailer identifiers may vary. Reproduction of the paper means matching
content, pagination, references, and visual layout.

## Canonical release-gate environment

- TeX Live 2023/Debian
- pdfTeX 1.40.25
- latexmk 4.83
- BibTeX 0.99d
- CPython 3.12.13

## Development render used for this update

The tracked PDFs in this unreleased working tree were also compiled and
visually inspected with Tectonic 0.16.9. The official Windows MSVC archive had
SHA-256
`131a24604785a9600989a3d91225f597df52ac06f00aeffe86fd529f99ee5cdd`.
With `SOURCE_DATE_EPOCH=1785369600`, two independent builds were byte-identical
and produced a 50-page paper and a two-page synopsis:

- paper SHA-256:
  `6a836cdce746cf24a4bcdcabc58f6139db6cd92f430ba5a3b9fb0f6395e167e7`;
- synopsis SHA-256:
  `8337a9d3097f357cd3cd61bd23f1075cc2af8d0fe46ecfd45d8c5933f3cd330e`.

This is a development render check, not a substitute for the canonical
`make ci` release gate above. Before any promotion, rebuild with the canonical
environment and require its clean-log check to pass.

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

## Verify the retained executable Fixture F8

```bash
python3 fixtures/F08_sqrt_square_sign/check_fixture.py
```

Expected terminal line:

```text
F8-SQRT-SQUARE-SIGN: PASS
```

The check parses and validates the shipped JSON Schema, verifies the claim,
schema, and script hashes, independently recomputes the exact integer
arithmetic, refuses to overwrite the retained receipt, runs the generator in
an isolated location, and requires byte-identical output.

## Run the release-gate tests

```bash
python3 -m unittest discover -s tests -v
```

The suite retains one schema-invalid mutant and one false-arithmetic mutant.
Both must fail. It also checks that F9 remains documentary and unexecuted,
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
glyphs, overfull boxes, or fatal errors. The expected page count is 50.

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

This checks the complete development inventory, retained executable fixture,
negative regressions, and build-verifier tests. Building the PDFs is a separate
target because a full TeX installation is larger than the minimal verification
environment.

For the full gate, including both document builds, run:

```bash
make ci
```

The build gate requires a 50-page paper and two-page synopsis, one final PDF
record per log, and no unresolved reference, citation, font, glyph, box, or
fatal TeX warning.

## Source corpus boundary

The twelve supplied corpus documents used to reconstruct BSC's internal
lineage are not included. Their identifiers and SHA-256 hashes are retained in
`provenance/`; see [SOURCE_AVAILABILITY.md](SOURCE_AVAILABILITY.md). Therefore
an external reader can rebuild this development package but cannot
independently replay the complete corpus-lineage audit from this archive
alone.
