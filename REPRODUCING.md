# Reproducing the release

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

## Verify the released files

```bash
sha256sum -c MANIFEST.sha256
```

## Verify Fixture F8

```bash
python3 fixtures/F08_sqrt_square_sign/check_fixture.py
```

Expected terminal line:

```text
F8-SQRT-SQUARE-SIGN: PASS
```

The check fails if the retained script or claim hash changes, if the predicate
does not evaluate to false, if the result label is inconsistent with the
predicate, if the generated JSON differs from the retained receipt, or if the
subprocess exits unsuccessfully.

## Build the paper

```bash
make paper
```

Output:

```text
build/paper/On_Boundaries_of_Evidence.pdf
```

The final LaTeX log must contain no unresolved citations or references, missing
glyphs, overfull boxes, or fatal errors. The expected page count is 35.

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

This checks the release manifest and the retained executable fixture. Building
the PDFs is a separate target because a full TeX installation is larger than
the minimal verification environment.

## Source corpus boundary

The twelve supplied corpus documents used to reconstruct BSC's internal
lineage are not included. Their identifiers and SHA-256 hashes are retained in
`provenance/`; see [SOURCE_AVAILABILITY.md](SOURCE_AVAILABILITY.md). Therefore
an external reader can rebuild this release but cannot independently replay the
complete corpus-lineage audit from this archive alone.
