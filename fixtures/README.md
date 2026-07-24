# Fixtures

Section 16 of the paper defines eight exact reference fixtures.

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

Only F8 is executable in this release. Its directory includes:

- the original receipt generator;
- the retained reference receipt;
- a JSON Schema;
- a fail-closed checker that runs in a temporary directory and does not
  overwrite the reference receipt.

Run from the repository root:

```bash
python3 fixtures/F08_sqrt_square_sign/check_fixture.py
```
