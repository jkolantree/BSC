# Fixtures

Version 1.2.0 defines ten exact reference fixtures. Immutable v1.1.0 remains
the nine-fixture record, and immutable v1.0.1 remains the
historical eight-fixture record.

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

F8 and F10 are executable in version 1.2.0. F9 has no raw-data
replay, fitting execution, hardware receipt, or complexity benchmark. Each
executable fixture directory includes:

- the original receipt generator;
- the retained reference receipt;
- a JSON Schema;
- a fail-closed checker that runs in a temporary directory and does not
  overwrite the reference receipt.

Run from the repository root:

```bash
python3 fixtures/F08_sqrt_square_sign/check_fixture.py
python3 fixtures/F10_coupled_surrogate/check_fixture.py
```

F10 uses exact rational arithmetic with the same interface error in two stable
hosts. It establishes different exact tolerance dispositions for one declared
loss coordinate. It is code-verification evidence for its finite recurrence
only, not full BSC admissibility or empirical or physical validation of a
deployed surrogate.
