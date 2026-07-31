# Collatz recursive sufficiency: correction, replacement sieves, and a conditional finite certificate

## Record status

- **BSC scope:** bounded number-theory application and executable evidence
  fixture.
- **Core-framework effect:** none. The eight-field BSC morphism and all
  framework modules are unchanged.
- **Primary claim source:** Mohammad Ansari, *Recursive sufficiency for the
  Collatz conjecture and computational verification*, *Notes on Number Theory
  and Discrete Mathematics* 31(3), 471–480 (2025),
  [DOI 10.7546/nntdm.2025.31.3.471-480](https://doi.org/10.7546/nntdm.2025.31.3.471-480).
- **External computation source:** David Barina, *Improved verification limit
  for the convergence of the Collatz conjecture*, *Journal of Supercomputing*
  81, 810 (2025),
  [DOI 10.1007/s11227-025-07337-0](https://doi.org/10.1007/s11227-025-07337-0),
  and the associated public verification log.
- **Release boundary:** this record is not a proof of the Collatz conjecture,
  an official verification-frontier announcement, a corrigendum issued by
  Ansari or the journal, or a restoration of Ansari's claimed
  $4\cdot3^{44}+2$ interval jump.

Parity vectors, stopping times, residue classes modulo powers of two, and
density arguments are classical in the Collatz literature. The present record
does not claim those methods as new. It audits one published induction,
supplies a replacement theorem under explicit hypotheses, and binds one
finite computation to an exact certificate.

## 1. Definitions

Use the shortcut Collatz map

```math
T(n)=
\begin{cases}
n/2,&n\text{ even},\\
(3n+1)/2,&n\text{ odd}.
\end{cases}
```

Two positive integers **merge** if their forward $T$-orbits meet. A positive
integer $n>1$ is **recursive** if it merges with a positive integer smaller
than $n$. A set is recursive when every one of its elements greater than one
is recursive. A proper set $F\subset\mathbb N$ is **recursively sufficient**
(RS) when $\mathbb N\setminus F$ is recursive.

For a starting integer $n$, let $s_j(n)$ be the number of odd terms among
$n,T(n),\ldots,T^{j-1}(n)$.
For a periodic set $A$, write $d(A)$ for its natural density. Write

```math
H_2(p)=-p\log_2p-(1-p)\log_2(1-p)
```

for binary entropy, with the usual continuous endpoint convention.

## 2. The first defect in the printed ternary induction

Ansari defines

```math
F_n=
\bigcup_{a_0,\ldots,a_{n-1}\in\{0,1\}}
\left(
4\cdot3^n\mathbb N_0+
4\sum_{i=0}^{n-1}a_i3^i+3
\right).
```

The actual first removed layer is

```math
F_1\setminus F_2
=
(36\mathbb N_0+27)\cup(36\mathbb N_0+31),
```

not the single progression needed by the printed induction. Indeed,
$F_1\bmod36=\{3,7,15,19,27,31\}$ and
$F_2\bmod36=\{3,7,15,19\}$.

For $x=36k+31$, the undirected functional graph contains

```math
x
\longleftrightarrow 2x
\longleftrightarrow \frac{4x-1}{3}
\longleftrightarrow \frac{8x-5}{9}
=32k+27<x.
```

Every edge is an exact forward or inverse $T$-edge. Thus the $31$-class is
recursive. Since $F_1$ is RS,

```math
F_2\text{ is RS}
\quad\Longleftrightarrow\quad
36\mathbb N_0+27\text{ is recursive}.
```

This is BSC-CRS-01. It locates the missing obligation; it does not discharge
it. No corrigendum was found on the inspected journal page as of 31 July
2026, but absence from that page is not proof that no correction exists
elsewhere.

## 3. Unconditional parity-prefix replacement

For $m\ge1$, define

```math
U_m=
\{n\ge1:7s_j(n)>4j\text{ for every }1\le j\le m\}.
```

### Proposition BSC-CRS-02

The sets $U_m$ are nested, periodic modulo $2^m$, recursively sufficient,
and have density tending to zero exponentially.

### Proof

Let $n>1$ lie outside $U_m$, and choose $j\le m$ with
$7s_j(n)\le4j$. If an earlier iterate is already below $n$, then $n$ is
recursive. Otherwise every odd iterate in the prefix is at least $3$, so an
odd shortcut step expands by at most $5/3$, while an even step multiplies by
$1/2$. Hence

```math
\frac{T^j(n)}n
\le
\frac{(10/3)^{s_j(n)}}{2^j}
\le
\left(\frac{10^4}{2^7\,3^4}\right)^{j/7}<1.
```

Thus every element of the complement is recursive.

The first $m$ parity bits are determined by $n\bmod2^m$, and the classical
parity-vector bijection assigns every binary word of length $m$ to exactly
one such residue. A surviving word has more than $4m/7$ ones, so

```math
d(U_m)
\le
2^{-m(1-H_2(4/7))},
```

using the standard binomial entropy bound. The exponent is positive. Nesting
is immediate from the prefix definition. $\square$

This proves the existence of periodic RS sieves whose elimination tends to
100%, without relying on the broken ternary induction.

## 4. Safety-net repair retaining the ternary spine

### Lemma BSC-CRS-03

If $B$ and $S$ are RS and $A\subseteq B$, then

```math
H=A\cup(B\cap S)
```

is RS.

### Proof

The complement of $H$ is

```math
(\mathbb N\setminus B)\cup\bigl((B\setminus A)\cap(\mathbb N\setminus S)\bigr).
```

The first term is recursive because $B$ is RS. The second is a subset of
the recursive set $\mathbb N\setminus S$. A union of recursive sets is
recursive. Also $H\subseteq B$, so $H$ is proper. Thus $H$ is RS.
$\square$

Let $S_m$ be any decreasing family of periodic RS sets, contained in
$4\mathbb N_0+3$, with $d(S_m)\to0$. For $m\ge2$, the family $U_m$
above is one choice. Put

```math
H_{n,m}=F_n\cup(F_1\cap S_m).
```

The lemma makes every $H_{n,m}$ RS even though $F_n$ remains unproved for
$n\ge2$. Without any further independence hypothesis,

```math
d(H_{n,m})
\le
\frac14\left(\frac23\right)^n+d(S_m).
```

Consequently $H_{j,j}$ is a nested periodic RS family with density tending
to zero. If, in addition, $S_m$ has a power-of-two period—as $U_m$ does—then
its residue condition is independent of the ternary coordinate and Chinese
remaindering gives the sharper exact identity

```math
d(H_{n,m})
=
\frac14\left(\frac23\right)^n
+\frac23d(S_m)
-\left(\frac23\right)^n d(S_m).
```

The exact formula is not asserted for an arbitrary periodic $S_m$ whose
period may share a factor with $3^n$. The construction is a replacement for
the sieve-existence conclusion, not a proof that the original $F_n$ are RS
and not a restoration of the printed empty-interval argument: the safety-net
term can occupy the intended gap.

## 5. Cutoff-conditioned sharp sieve

Let

```math
B_0=2^{71}=2361183241434822606848
```

and assume every positive integer below $B_0$ has a convergent Collatz orbit;
$B_0$ itself is a power of two. Define

```math
V_m=
\{n\ge1:485s_j(n)>306j\text{ for every }1\le j\le m\}.
```

The exact integer inequality

```math
(3B_0+1)^{306}<2^{485}B_0^{306}
```

holds.

### Proposition BSC-CRS-04

Conditional on the declared verified-prefix assumption, each $V_m$ is RS
and periodic modulo $2^m$.

### Proof

Numbers at most $B_0$ are covered by the assumption. Let $n>B_0$ lie
outside $V_m$, and choose a failing prefix. If an earlier iterate is below
$n$, recursion is immediate. Otherwise every odd iterate $x$ in the
prefix exceeds $B_0$, and

```math
\frac{T(x)}x
=\frac{3+1/x}{2}
<\frac{3+1/B_0}{2}.
```

The displayed exact integer inequality and
$485s_j(n)\le306j$ make the whole prefix multiplier strictly below one.
Periodicity again follows from the parity-vector bijection. $\square$

The exact dynamic program

```math
A_{0,0}=1,\qquad
A_{j,s}=
\mathbf1_{\{485s>306j\}}
\bigl(A_{j-1,s}+A_{j-1,s-1}\bigr)
```

counts the surviving residue classes, with $A_{j,s}=0$ outside
$0\le s\le j$. At $m=173$,

```math
|V_{173}\bmod2^{173}|
=113556863454847668033678912559844765797703296469.
```

Now let

```math
G=F_1\setminus(36\mathbb N_0+31)
```

and, for $m\ge2$, let $W_m=G\cap V_m$. The explicit $31$-class merge makes
$G$ RS, and an
intersection of RS sets is RS because its complement is a union of recursive
sets. The first two prefix inequalities force $V_m\subseteq4\mathbb N_0+3$
in this range. Exactly five of the nine compatible residue classes modulo 36
belong to $G$, so, for every $m\ge2$,

```math
d(W_m)=\frac59d(V_m).
```

Therefore

```math
d(W_{173})
=5.269284326924912742\ldots\times10^{-6},
```

an elimination percentage of
$99.999473071567307508\ldots\%$. This is BSC-CRS-05. The density is an exact
periodic residue count, not a probabilistic convergence claim.

## 6. Conditional ten-billion finite extension

Fixture F11 exhaustively enumerates

```math
W_{173}\cap(B_0,B_0+10^{10}]
```

and retains 52,686 starting values. For every retained value it records the
first exact shortcut iterate below the start. The candidate table has:

- 52,686 records;
- first offset 104,303;
- last offset 9,999,886,847;
- largest first-descent time 438 shortcut steps;
- largest encountered peak
  1,432,075,179,170,128,856,197,670,708,120; and
- SHA-256
  `88df1573d49511a4bc93fab35f85d3feb1cade2d40b5444ee88ae42699aa5250`.

A second CPython checker implementation checked all 1,388,888,889
$G$-compatible candidates in the interval and reproduced exactly the
52,686 table offsets. Its separate arbitrary-precision row path checked every
record's membership, first descent, descent value, and peak.

### Proposition BSC-CRS-06

If every positive integer at most $B_0$ converges, and the F11 enumeration
and descent receipt are correct, then every positive integer at most

```math
B_0+10^{10}=2361183241444822606848
```

converges.

### Proof

Apply strong induction above $B_0$. If $n\notin W_{173}$, recursive
sufficiency gives a merge with a smaller positive integer. If
$n\in W_{173}$, the retained certificate gives a forward iterate below
$n$. In either case, the induction hypothesis supplies convergence of the
smaller orbit, and hence of $n$. $\square$

The conclusion is conditional because BSC did not replay the external
$n<B_0$ verification campaign. F11 verifies only its declared extension
computation and exact mathematical bridge. This result is not presented as a
new official computational record.

## 7. Evidence identity and failure modes

The F11 receipt binds:

- the shortcut map, base, interval, threshold, depth, and residue convention;
- the exact source-table bytes and SHA-256;
- exact dynamic-program and density results;
- complete $G$-candidate enumeration;
- every retained row's first-descent path;
- the generator, checker, schema, input, and provenance hashes; and
- CPython 3.12.13 arbitrary-precision integer semantics.

The claim is invalidated or demoted by any base-frontier mismatch, interval
endpoint mismatch, omitted or extra candidate, parity-threshold change,
certificate-byte change, arithmetic mismatch, source-identity mismatch, or
promotion from the conditional finite prefix to universal convergence.

## 8. Deferred and rejected claims

- The assertion that every original $F_n$ is RS remains open from this
  audit's perspective.
- The progression $36\mathbb N_0+27$ remains unresolved.
- The claimed automatic extension to $4\cdot3^{44}+2$ is not restored.
- A proposed binary ghost-cylinder obstruction and a proposed recursive
  $1/243$-subprogression were not needed for the retained result and were
  withheld pending separate symbolic review.
- No novelty is claimed for parity-vector coding, density-one stopping-time
  results, or sufficient-set methods generally.

## 9. Prior-art boundary

Relevant established context includes Terras's parity-vector stopping-time
analysis, Lagarias's surveys and density work, Monks et al.'s strongly
sufficient sets, and current work on paradoxical parity prefixes. Those
sources prevent a broad novelty claim. The narrow retained contribution is
the exact audit of the printed induction, the safety-net replacement under
declared RS hypotheses, the particular cutoff-conditioned $W_{173}$ sieve,
and its reproducible claim-local finite certificate.
