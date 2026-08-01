# F12: exact-Q derived-holonomy certificates

## Identity

- mathematical claim: `BSC-DHC-01`;
- fixture-ledger claim: `BSC-FIX-12`;
- runtime fixture: `F12-DERIVED-HOLONOMY-Q`;
- evidence status: `independent_reconstruction`;
- historical replay: `NOT_REPLAYED`.

This is a post-v1.4.0 development fixture. It does not change the immutable
v1.4.0 eleven-fixture release record.

## Contract

The input encodes finite bounded chain complexes and two chain maps over
$\mathbb Q$. Every rational is a reduced numerator/positive-denominator pair.
Every matrix records its row and column count, including zero-dimensional
shapes. The generator validates $d^2=0$ and both chain-map equations before it
constructs the exact system

```math
A\mathbf h=\boldsymbol\omega,
\qquad
\omega_n=f_n-g_n=d_{n+1}^D h_n+h_{n-1}d_n^C.
```

A pass records exact homotopy matrices. A failure records an exact normalized
left-null witness $y$ with $y^TA=0$ and $y^T\boldsymbol\omega=1$.

## Retained cases

`contractible_identity` has
$A=(1,1)^T$, $\boldsymbol\omega=(1,1)^T$, and $h_0=1$.
`homology_visible_obstruction` has a $1\times0$ matrix $A$,
$\boldsymbol\omega=(1)$, and $y=(1)$.

Run:

```bash
python3 fixtures/F12_derived_holonomy_q/check_fixture.py
```

Expected terminal line:

```text
F12-DERIVED-HOLONOMY-Q: PASS: 2 exact certificates
```

The checker independently reparses and recomputes the mathematics, verifies
the retained pass/fail witnesses, runs the generator in a temporary directory,
and requires byte-identical canonical JSON. It does not import the generator.

## Provenance boundary

`provenance.json` binds the two supplied Markdown identities as
provenance-only inputs. Their source prose is not copied. The named historical
script and receipts were absent and remain `NOT_REPLAYED`. Neither exact
execution nor the finite scalar regression is a trusted-kernel proof or an
arbitrary-ring theorem.
