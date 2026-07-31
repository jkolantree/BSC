# Fixtures

Version 1.4.0 contains eleven exact reference fixtures. Immutable v1.3.0 and
v1.2.0 remain the ten-fixture records, immutable v1.1.0 remains the
nine-fixture record, and immutable v1.0.1 remains the historical
eight-fixture record.

| Fixture | Subject | Current computational status |
|---|---|---|
| F1 | Torus winding without electric charge | Unexecuted mathematical derivation |
| F2 | One-dimensional Dirichlet-to-Neumann ambiguity | Unexecuted mathematical derivation |
| F3 | Exact Blackwell order and directed deficiency | Unexecuted mathematical derivation |
| F4 | Koopman pseudomode and spectral pollution | Unexecuted mathematical derivation |
| F5 | Finite $\mathbb Z_2$ quantum-reference-frame descent | Unexecuted mathematical derivation |
| F6 | Locally satisfiable parity data that do not glue | Unexecuted mathematical derivation |
| F7 | Off-shell massive-field shift | Unexecuted mathematical derivation |
| F8 | $\sqrt{x^2}=x$ regression counterexample | Exact retained CPython receipt |
| F9 | Finite zeta–coherence identity with blocked unsupported promotions | Unexecuted documentary and mathematical audit |
| F10 | Equal standalone surrogate error in two stable coupled hosts | Exact retained CPython receipt |
| F11 | Collatz recursive-sufficiency correction and conditional finite-prefix extension | Exact retained CPython receipt; external base remains conditional |

F8, F10, and F11 are executable in version 1.4.0. F9 has no raw-data
replay, fitting execution, hardware receipt, or complexity benchmark. Each
executable fixture directory includes a retained receipt, generator, parsed
JSON Schema, and fail-closed checker. F8 and F10 run their generators in
temporary locations and require byte-identical output without overwriting the
reference receipt. F11 instead separates a routine exact replay from its
several-minute complete-enumeration gate:

Run from the repository root:

```bash
python3 fixtures/F08_sqrt_square_sign/check_fixture.py
python3 fixtures/F10_coupled_surrogate/check_fixture.py
python3 fixtures/F11_collatz_recursive_sieve/check_fixture.py
```

F10 uses exact rational arithmetic with the same interface error in two stable
hosts. It establishes different exact tolerance dispositions for one declared
loss coordinate. It is code-verification evidence for its finite recurrence
only, not full BSC admissibility or empirical or physical validation of a
deployed surrogate.

F11 uses exact integers to replay every retained first-descent row. Its
publication-only `--full-scan` gate also exhausts all 1,388,888,889
compatible candidates in the declared interval. The resulting finite-prefix
extension is conditional on the externally reported $2^{71}$ base, which BSC
did not replay. F11 is not an official frontier announcement or a proof of
the Collatz conjecture.
