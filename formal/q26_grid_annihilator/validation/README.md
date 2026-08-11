# External Q26 comparator receipt

This directory preserves the independent validation referenced by the Q26
proof note. `TrustedChallenge.lean` contains the verifier-controlled theorem
statement and intentionally uses `sorry`; it is not imported by the proof and
is not evidence for the solution. Comparator requires that challenge hole so
it can compare the trusted statement with the separately compiled theorem in
`Q26GridAnnihilator.Unconditional`.

The solution was checked with pinned Comparator and lean4export builds, the
Lean 4.32.2 kernel, and the independently implemented nanoda kernel. Only
`propext`, `Quot.sound`, and `Classical.choice` were permitted. See
`comparator_receipt.json` for the scoped result and immutable identities,
`evidence/comparator-q26.txt` for the transcript, and
`reproduce-on-ubuntu.sh` for the fail-closed reproduction procedure.

The reproduction requires substantial resources: the retained run took about
16 minutes and peaked at 21.9 GB of memory. It verifies all pins and hashes,
tests the landrun write boundary, and refuses a source projection that differs
from the retained proof sources. By default it removes its large temporary
tree after a successful run, retains failures for diagnosis, and honors
`KEEP_WORK=1` when successful build state is deliberately needed.
