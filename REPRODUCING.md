# Reproducing release 1.0.1

## Scope

The manuscript and synopsis can be rebuilt from their shipped LaTeX sources.
Fixture F8 can be reproduced byte-for-byte in the pinned Python environment.
The distributed PDF hashes identify the release artifacts; a fresh PDF build is
not claimed to be byte-identical because PDF timestamps and trailer identifiers
may vary. Reproduction of the paper means matching content, pagination,
references, and visual layout.

## Verified environment

- TeX Live 2023/Debian
- pdfTeX 1.40.25
- latexmk 4.83
- BibTeX 0.99d
- CPython 3.12.13

## Verify the exact release tree

```bash
python3 tools/verify_manifest.py
```

This complete-set gate rejects missing, extra, duplicate, unsafe,
unnormalized, symlinked, special, and hash-mismatched payload paths. The
manifest omits itself.

## Verify Fixture F8

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
Both must fail.

## Build the paper

```bash
make paper
```

Output:

```text
build/paper/On_Boundaries_of_Evidence.pdf
```

The final LaTeX log must contain no unresolved citations or references, missing
glyphs, overfull boxes, or fatal errors. The expected page count is 38.

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

This checks the complete release inventory, retained executable fixture,
negative regressions, and build-verifier tests. Building the PDFs is a separate
target because a full TeX installation is larger than the minimal verification
environment.

For the full gate, including both document builds, run:

```bash
make ci
```

The build gate requires a 38-page paper and two-page synopsis, one final PDF
record per log, and no unresolved reference, citation, font, glyph, box, or
fatal TeX warning.

## Source corpus boundary

The twelve supplied corpus documents used to reconstruct BSC's internal
lineage are not included. Their identifiers and SHA-256 hashes are retained in
`provenance/`; see [SOURCE_AVAILABILITY.md](SOURCE_AVAILABILITY.md). Therefore
an external reader can rebuild this release but cannot independently replay the
complete corpus-lineage audit from this archive alone.
