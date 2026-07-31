# License map

Copyright © 2026 J. Tree.

The repository uses two licenses:

- **CC BY 4.0** covers the manuscript, synopsis, bibliography, ledgers, revision
  memorandum, README files, roadmap, disclosure, provenance descriptions,
  figures, tables, and other human-readable documentation.
- **MIT** covers Python code, JSON Schema, machine-readable fixture tooling,
  workflow files, and the Makefile.
- **CC BY 4.0** also covers the retained F11 tabular certificate as a
  machine-generated factual dataset. Its provenance and exact bytes are
  separately pinned; the submitted C/C++ sources are not redistributed.

The retained execution receipt is distributed with the fixture tooling under
the MIT License. `CITATION.cff` and `.zenodo.json` are factual metadata and may
be copied as needed to cite or deposit the work.

## File-scope map

| Paths | License |
|---|---|
| `paper/**`, `synopsis/**`, `ledgers/**`, `revision/**`, `provenance/**`, `*.md` | CC BY 4.0 |
| `fixtures/**/*.py`, `fixtures/**/*.json`, `tools/**`, `tests/**` | MIT |
| `fixtures/**/*.tsv` | CC BY 4.0 |
| `.github/**`, `Makefile` | MIT |
| `CITATION.cff`, `.zenodo.json`, `MANIFEST.sha256` | Factual metadata; copying for citation, deposit, and verification is permitted |

If a path falls into more than one row, the more specific row governs. The
complete license texts are `paper-and-documentation.txt` and `code.txt`.

The twelve internal source documents listed in `provenance/` are not included
and receive no license through this repository.

## Historical clarification

Early repository commits preceding the canonical v1.0.0 tree contained a
generic root MIT notice while manuscript files were being staged. The explicit
file-scope map above was added in commit
`52abd4f3d6dbd048a4c6e6ddbb57e7e428c6bcd4` and governs the current release
tree. This notice documents the history; it cannot retroactively withdraw any
rights a recipient may already have obtained from an earlier published
snapshot.
