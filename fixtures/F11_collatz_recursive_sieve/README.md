# F11: Collatz recursive-sufficiency repair and finite certificate

This executable fixture binds four distinct results:

1. the first residue-layer defect in Ansari's printed ternary induction;
2. the exact parity-prefix count and density of the conditional $W_{173}$
   recursively-sufficient sieve;
3. exact row-by-row replay of 52,686 first-descent certificates; and
4. exhaustive enumeration of every $G$-compatible candidate in the
   ten-billion-wide interval.

The final finite-prefix conclusion is conditional on the external verified
base $n<2^{71}$. BSC did not replay that external computation. This fixture
is not a proof of the Collatz conjecture and is not an official
verification-frontier announcement.

## Files

- `input.json`: frozen map, base, range, threshold, counts, and artifact
  identity.
- `w_10b.tsv`: submitted machine-generated first-descent certificate.
- `verify_collatz_repair.py`: deterministic full enumerator and receipt
  generator.
- `check_fixture.py`: independent exact row replay and optional independent
  full enumeration.
- `receipt.schema.json`: retained receipt contract.
- `verification_receipt.json`: deterministic full-scan receipt.
- `provenance.json`: submitted-source hashes and publication disposition.

The supplied C and C++ scanners are not redistributed. The C source contained
a shared non-atomic failure flag, and the C++ source retained unused ternary
code; neither is needed for the admitted claim. Their hashes remain pinned in
`provenance.json`.

## Routine exact check

From the repository root:

```text
python3 fixtures/F11_collatz_recursive_sieve/check_fixture.py
```

This validates identities, exact counts, all 52,686 rows, and receipt
bindings. It does not repeat the ten-billion full enumeration.

## Publication/full-completeness check

```text
python3 fixtures/F11_collatz_recursive_sieve/check_fixture.py --full-scan
```

This additionally checks all 1,388,888,889 $G$-compatible candidates and
requires the resulting candidate set to equal the retained table exactly.
On the release machine with 16 workers, this takes several minutes.

To regenerate the retained receipt in a new path:

```text
python3 fixtures/F11_collatz_recursive_sieve/verify_collatz_repair.py \
  build/F11_actual_receipt.json --workers 16
```

The generator refuses to overwrite the retained receipt.

## Authority boundary

The exact fixture computation supports BSC-CRS-01, BSC-CRS-05, and the
computational premises of conditional BSC-CRS-06. It does not independently
establish the external $2^{71}$ base, the unresolved $36k+27$
progression, the original $F_n$ induction, the claimed
$4\cdot3^{44}+2$ jump, or universal Collatz convergence.
