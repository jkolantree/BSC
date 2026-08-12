# External Q26 Comparator validation

`TrustedChallenge.lean` is verifier-controlled and self-contained: it defines
the 26 by 26 board, integer coordinates, queen attacks, and domination without
importing any submitted Q26 module. Its two intentional `sorry` declarations
state the exact-cardinality-13 obstruction and the direct domination-number-14
result. The challenge is not imported by the solution and is not evidence for
the solution. Comparator requires those challenge holes so it can compare the
trusted declarations and statements with the separately compiled theorems in
`Q26GridAnnihilator.Definitive`.

## Evidence boundary

`comparator_receipt.json`, `evidence/comparator-q26.txt`, and
`evidence/lean-source-projection-sha256.txt` bind the exact self-contained
challenge, configuration, and 27-file Lean source projection accepted in the
retained run. `evidence/external-run-q26.txt` additionally records the archive,
tool-binary, sandbox, and source-invariance gates surrounding Comparator.

The run used pinned Comparator and lean4export builds, the Lean 4.32.2 kernel,
and the independently implemented nanoda kernel. Only `propext`, `Quot.sound`,
and `Classical.choice` were permitted. Comparator built the 608-job challenge
and the 8,676-job solution, matched both named statements, and both kernels
accepted. The Comparator service took 15 minutes 22.842 seconds, consumed 19
minutes 29.182 seconds of CPU, and peaked at 21.8 GB with no swap.

`reproduce-on-ubuntu.sh` verifies pins and hashes, tests the landrun write
boundary, and refuses a source projection that differs from the retained proof
sources. Its nanoda build remaps the random work-root path so the pinned binary
hash is reproducible. By default it removes its large temporary tree after
success, retains failures for diagnosis, and honors `KEEP_WORK=1` when
successful build state is deliberately needed.

This validation is about the stated Lean theorems only. It does not change the
separate root-CNF status, which remains `UNKNOWN` without a checked proof.
