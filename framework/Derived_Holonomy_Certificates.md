# Exact rational derived-holonomy certificates

## Status and scope

`BSC-DHC-01` is a post-v1.4.0 finite-dimensional certificate claim. It is an
independent reconstruction over the field $\mathbb Q$. It is not a replay of a
historical source script, a proof-assistant kernel result, an arbitrary-ring
theorem, an electromagnetic holonomy calculation, or a change to any released
paper or fixture.

Let $C$ and $D$ be finite bounded chain complexes of finite-dimensional
$\mathbb Q$-vector spaces on one declared degree interval. Their
differentials use homological grading,

```math
d_n^C:C_n\longrightarrow C_{n-1},
\qquad
d_n^D:D_n\longrightarrow D_{n-1}.
```

The input must satisfy $d_{n-1}^C d_n^C=0$ and
$d_{n-1}^D d_n^D=0$ exactly. Two proposed maps $f,g:C\to D$ must separately
satisfy the chain-map equations

```math
d_n^D f_n=f_{n-1}d_n^C,
\qquad
d_n^D g_n=g_{n-1}d_n^C.
```

Malformed dimensions, non-chain maps, noncanonical rationals, floating-point
entries, and any field label other than `Q` are rejected before certificate
generation.

## Claim BSC-DHC-01

Set $\omega_n=f_n-g_n$. A degree-one homotopy consists of maps
$h_n:C_n\to D_{n+1}$. In the fixed sign convention, $f$ and $g$ are chain
homotopic exactly when

```math
\omega_n=d_{n+1}^D h_n+h_{n-1}d_n^C
```

at every declared degree. Vectorizing all matrix entries turns these equations
into one finite rational system

```math
A\mathbf h=\boldsymbol\omega.
```

The implementation orders degrees increasingly, then matrix columns, then
matrix rows. Homotopy blocks use the same order. Explicit matrix dimensions
distinguish $0\times n$, $m\times0$, and $0\times0$ matrices.

There are two exact certificate forms:

1. A pass certificate records rational matrices $h_n$. The independent
   checker recomputes every equation $\omega_n=d^D h+h d^C$ directly and also
   checks $A\mathbf h=\boldsymbol\omega$.
2. A fail certificate records a rational row vector $y$ satisfying
   $y^T A=0$ and $y^T\boldsymbol\omega=1$.

   The nonzero pairing contradicts solvability. This is a linear-algebra
   inconsistency certificate, not a positivity or numerical-separation
   argument.

Deterministic Gauss--Jordan elimination scans columns left to right, selects
the first eligible pivot row, and sets free variables to zero. On an
inconsistent system, the first inconsistent transformed row is normalized so
that its pairing with $\boldsymbol\omega$ is exactly $1$. All arithmetic uses
`fractions.Fraction`; no rank or equality decision uses floating point.

## Why the certificate is complete in this scope

The matrix encoding is a coordinate presentation of the linear map

```math
L(h)=d^D h+h d^C.
```

Consequently, a solution of $A\mathbf h=\boldsymbol\omega$ is exactly a chain
homotopy. If the system is inconsistent, exact row operations produce a row
of the transformation matrix that annihilates every column of $A$ but not
$\boldsymbol\omega$; normalization gives the recorded $y$. Conversely, the
existence of such a $y$ rules out every solution. These statements use finite
linear algebra over $\mathbb Q$.

For finite-dimensional complexes over a field, equality of induced homology
maps is equivalent to null-homotopy of $f-g$ after choosing the usual splitting
into boundaries, homology representatives, and complements. The executable
gate decides the chain-homotopy equation itself. Its finite scalar regression
compares that decision with an independently computed homology criterion; it
does not replace the general proof.

## Retained fixture F12

`BSC-FIX-12`, runtime ID `F12-DERIVED-HOLONOMY-Q`, retains two cases:

- On the contractible complex $\mathbb Q\xrightarrow{1}\mathbb Q$, take
  $f=\mathrm{id}$ and $g=0$. The raw difference is nonzero, but
  $A=(1,1)^T$, $\boldsymbol\omega=(1,1)^T$, and $h_0=1$ is an exact pass
  certificate.
- On the degree-zero complex $\mathbb Q$ with zero differential, take
  $f=\mathrm{id}$ and $g=0$. Then $A$ has shape $1\times0$,
  $\boldsymbol\omega=(1)$, and $y=(1)$ is a homology-visible obstruction.

The checker also exercises a non-square case, deterministic free-variable
selection, normalized row-operation witnesses, and all 153 valid ordered
scalar two-term chain-map pairs with coefficients in `{-1, 0, 1}`. The exact
census is 81 homotopic and 72 obstructed, with zero mismatch against the
independent scalar homology test.

## Run the gate

From the repository root:

```bash
python3 fixtures/F12_derived_holonomy_q/check_fixture.py
```

The generator accepts a canonical input and a fresh output path:

```bash
python3 fixtures/F12_derived_holonomy_q/verify_derived_holonomy.py \
  fixtures/F12_derived_holonomy_q/input.json \
  build/F12_actual_receipt.json
```

It refuses every existing destination and the retained receipt path. The
independent checker does not import the generator; it reconstructs the chain
complexes, maps, $A$, $\boldsymbol\omega$, and witness equations from the
input, then requires isolated regeneration to match the retained bytes.

## Evidence and transfer boundary

The two hash-identified supplied Markdown notes are recorded only as
provenance inputs. Their bytes are not redistributed, their absent scripts and
receipts remain `NOT_REPLAYED`, and this implementation does not establish
historical continuity or novelty. The receipt is `independent_reconstruction`
evidence and is neither `mechanically_replayed` nor `kernel_verified`.

The dense matrix and dense RREF implementation is intended for bounded exact
certificates. It makes no sparse-scaling or large-complex performance claim.
It does not reorder or absorb the repository's Collatz, electrostatic,
electromagnetic, or formal-kernel work.
