# Collatz affine-certificate calculus

## Record status

- **BSC scope:** post-v1.4.0 number-theory application mathematics.
- **Core-framework effect:** none. The eight-field BSC morphism, framework
  modules, and deployment authority are unchanged.
- **Released-artifact effect:** none. The immutable v1.4.0 tag, paper PDFs,
  Fixture F11, GitHub release, and Zenodo record are not modified by this
  note.
- **Evidence type:** exact symbolic proofs with machine-checkable regression
  examples. No new orbit census or verification frontier is claimed.
- **Non-claims:** this note does not prove the Collatz conjecture, prove that
  all of $36\mathbb N_0+27$ is recursive, restore Ansari's original $F_n$
  induction, or certify a depth-28, depth-30, or depth-32 catalog.

This module continues the released
[recursive-sufficiency application](Collatz_Recursive_Sufficiency_Audit.md).
It promotes only the statements that survived a separate symbolic review:
the merge-kernel characterization, the exact affine descent criterion, a
typed valuation screen, one narrow one-turn binary-cylinder obstruction, and
one explicit recursive subprogression.

No novelty is claimed here for tail equivalence, elementary affine
inequalities, valuation bookkeeping, or standard $p$-adic cylinder facts.
The contribution is their corrected, claim-local assembly as a BSC
certificate calculus and the exact examples proved below; any broader
priority claim requires a separate literature review.

## 1. Proof-carrying affine paths

Use the shortcut map

```math
T(n)=
\begin{cases}
n/2,&n\text{ even},\\
(3n+1)/2,&n\text{ odd}.
\end{cases}
```

Write

```math
\tau_0(x)=x/2,
\qquad
\tau_1(x)=(3x+1)/2
```

for forward even and odd edges, and

```math
\rho_0(x)=2x,
\qquad
\rho_1(x)=(2x-1)/3
```

for their inverse edges. An arithmetic cylinder is

```math
C(A,B)=\lbrace At+B:t\in\mathbb N_0\rbrace,
\qquad A,B\in\mathbb N.
```

A **uniform affine path certificate** on $C(A,B)$ consists of a fixed word in
$\tau_0,\tau_1,\rho_0,\rho_1$ and an affine form $A_i t+B_i$ at every
intermediate node.
The checker obligations are separate:

1. every forward edge has the declared parity;
2. every $\rho_1$ input is $2\pmod3$, so its predecessor is an odd positive
   integer;
3. every intermediate affine form is integral and positive for all
   $t\in\mathbb N_0$;
4. the endpoint $A't+B'$ shares a forward iterate with the start; and
5. the endpoint is strictly smaller than the start.

A residue class or a contracting coefficient alone is not a proof object.

## 2. Merge kernels

Let $(X,<)$ be well ordered and let $T:X\to X$ be a total deterministic map.
Define

```math
x\sim_Ty
\quad\Longleftrightarrow\quad
T^a(x)=T^b(y)
\text{ for some }a,b\in\mathbb N_0.
```

Determinism makes this relation transitive: two meeting points on the forward
orbit of the middle element can be aligned by further iteration. Hence
$\sim_T$ is an equivalence relation. Well-ordering gives a least member of
each class, so define

```math
K_T=\lbrace\min C:C\in X/{\sim_T}\rbrace.
```

### Theorem BSC-CRS-08 (merge-kernel characterization)

An element $x\in X$ merges with a strictly smaller element if and only if
$x\notin K_T$.

For shortcut Collatz on $\mathbb N$, put

```math
K_T^\star=K_T\setminus\lbrace1\rbrace.
```

Under BSC's definition of recursive sufficiency,

```math
F\text{ is RS}
\quad\Longleftrightarrow\quad
F\subsetneq\mathbb N
\text{ and }
K_T^\star\subseteq F.
```

#### Proof

The least member of a merge class has no smaller member in that class. Every
other member does. Applying this pointwise to $\mathbb N\setminus F$ gives
the kernel-containment condition, while $F\subsetneq\mathbb N$ is required
separately by the adopted RS definition. $\square$

The properness clause cannot be dropped: $F=\mathbb N$ contains
$K_T^\star$ but is not RS under that definition. The released safety-net
lemma remains valid under its $A\subseteq B$ hypothesis because
$A\cup(B\cap S)\subseteq B$ keeps the result proper when $B$ is proper.

For the shortcut map, the ordinary Collatz conjecture is equivalent to
$K_T=\lbrace1\rbrace$. This is a reformulation, not a proof.

## 3. Exact affine descent

### Theorem BSC-CRS-09 (uniform affine descent)

Let an admissible path on $C(A,B)$ have positive integral endpoint
$A't+B'$. Then

```math
A't+B'<At+B
\text{ for every }t\in\mathbb N_0
```

if and only if

```math
A'\le A
\qquad\text{and}\qquad
B'<B.
```

#### Proof

The start-minus-end difference is

```math
(A-A')t+(B-B').
```

At $t=0$, strict descent forces $B'<B$. If $A'>A$, the difference becomes
negative for sufficiently large $t$. Conversely, $A'\le A$ and $B'<B$
make the difference positive for every nonnegative $t$. $\square$

Equal slopes are allowed. The exact path

```math
8t+5
\xrightarrow{\tau_1\tau_0\tau_0}
3t+2
\xrightarrow{\rho_1\rho_0\rho_0}
8t+4
```

is a uniform merge certificate with $A'=A$ and $B'=B-1$.

Strict slope contraction is not sufficient. Direct iteration gives

```math
T^7(256t+7)=162t+5,
\qquad
T^8(256t+7)=243t+8.
```

Although $243<256$, the member $t=0$ is sent from $7$ to $8$. If $A'<A$
but $B'\ge B$, strict descent begins only at

```math
t_{\min}
=
\left\lfloor\frac{B'-B}{A-A'}\right\rfloor+1.
```

Values below that threshold require separate certificates.

## 4. Typed log-slope and valuation capacity

Consider a one-turn path whose forward segment has $s$ odd and $e$ even
steps, and whose reverse suffix has $c$ inverse-odd and $b$ inverse-even
steps. Put $r=c-s$. The coefficient multiplier is

```math
\lambda=\frac{A'}A
=
\frac{3^s}{2^{s+e}}\cdot2^b\left(\frac23\right)^c
=
2^{b-e}\left(\frac23\right)^r.
```

Let

```math
\gamma=\log_2(3/2).
```

Then the net log-slope contraction is

```math
D=-\log_2\lambda=e+\gamma r-b.
```

This is an exact arithmetic identity. It is not a physical energy or
conservation law, and its sign does not decide intercept descent.

### Proposition BSC-CRS-10 (valuation screen and strict depth)

For an admissible integral endpoint,

```math
v_3(A')=v_3(A)-r,
\qquad
v_2(A')=v_2(A)+b-e+r.
```

Consequently,

```math
r\le v_3(A),
\qquad
v_2(A)+b-e+r\ge0,
```

and

```math
D\le e+\gamma v_3(A)-b.
```

Therefore:

- $e+\gamma v_3(A)<b$ rules out every uniform affine descent certificate,
  because it forces $A'>A$;
- $e+\gamma v_3(A)=b$ rules out strict slope contraction but does not rule
  out an equal-slope certificate with $B'<B$; and
- $e+\gamma v_3(A)>b$ says only that strict slope contraction is not excluded
  by this valuation bound.

Intermediate congruences, positivity, coverage, final coefficient
integrality, and the intercept condition remain independent gates.

If fixing $h$ additional ternary digits increases $v_3(A)$ by exactly $h$,
then the least nonnegative depth not ruled out for **strict slope
contraction** is

```math
h_{\min}
=
\max\left(
0,
\left\lfloor
\frac{b-e}{\gamma}-v_3(A)
\right\rfloor+1
\right).
```

The floor-plus-one is forced by the strict inequality. At
$b=e$ and $v_3(A)=0$, the answer is $h_{\min}=1$, not zero.

The three neutral equations are separately typed:

```math
\begin{aligned}
\text{forward:}&\quad \gamma s=e,\\
\text{reverse:}&\quad \gamma c=b,\\
\text{combined:}&\quad \gamma(c-s)=b-e.
\end{aligned}
```

When their denominators are nonzero, the corresponding ratios are

```math
\frac{s}{e}=\frac1\gamma,
\qquad
\frac{c}{b}=\frac1\gamma,
\qquad
\frac{c-s}{b-e}=\frac1\gamma.
```

They are not a common ratio. Since $\gamma$ is irrational, the integer-count
equalities are exact only in the zero cases:

```math
\gamma s=e\iff(s,e)=(0,0),
\qquad
\gamma c=b\iff(c,b)=(0,0),
```

and

```math
\gamma(c-s)=b-e
\iff
c=s\text{ and }b=e.
```

The last case permits nonempty equal-slope paths, as the example above
demonstrates.

The exact rational bracket

```math
\frac{389}{665}<\gamma<\frac{179}{306}
```

follows from $3^{665}>2^{1054}$ and $3^{306}<2^{485}$. Thus, for a nonempty
forward word, $179s\le306e$ is an integer-only sufficient test for forward
**coefficient contraction**, not endpoint descent.

## 5. A scoped binary-cylinder obstruction

For $R\ge1$, let $g_R$ be the least nonnegative representative satisfying

```math
g_R\equiv-7\,9^{-1}\pmod {2^R}
```

and set $g_0=0$ for the depth-zero cylinder. Consider

```math
k=g_R+2^Rt,
\qquad
n=36k+27.
```

Then $2^{R+2}$ divides $n+1$, so the first $R+2$ shortcut steps are uniformly
odd. After those steps the coefficient of $t$ is odd, so the next parity
varies with $t$; no longer uniform forward word exists on the whole cylinder.
The starting coefficient is $36\cdot2^R$ and has $3$-adic valuation two.

### Theorem BSC-CRS-11 (ghost-cylinder no-go)

No fixed, reduced, uniformly admissible one-turn affine path certifies the
entire cylinder above by descent to a smaller positive endpoint.

#### Proof

At forward depth zero, every start is divisible by three. Inverse doublings
preserve that residue, so no inverse-odd edge becomes admissible. If $b=0$,
the path is the identity and $B'=B$; if $b>0$, then $A'=2^bA>A$.

At forward depth $j\ge1$, an immediate inverse-odd edge merely retraces the
last forward edge. The turning value is $2\pmod3$; one inverse doubling
changes it to $1\pmod3$, where an inverse-odd edge is inadmissible, while two
inverse doublings return it to $2\pmod3$. Thus, if a reduced reverse suffix
contains an inverse-odd edge, at least two inverse doublings precede its first
such edge, so $b\ge2$. The turning coefficient has $3$-adic valuation $j+2$,
so endpoint integrality gives $c\le j+2$ and hence $r=c-j\le2$. When $c>0$,

```math
\lambda
=2^b\left(\frac23\right)^r
\ge2^2\left(\frac23\right)^2
=\frac{16}{9}>1.
```

If $c=0$, then $r=-j$ and
$\lambda=2^b(3/2)^j>1$. In every case $A'>A$, contradicting the affine
descent criterion. $\square$

Any immediate $\tau_1\rho_1$ retrace in a fixed one-turn word can be deleted
uniformly without changing its endpoint. Repeating this deletion produces a
reduced word, so the theorem also rules out an unreduced fixed word that
would otherwise claim the same endpoint certificate.

The compatible cylinders converge in $\mathbb Z_2$ to

```math
k_\star=-7/9,
\qquad
36k_\star+27=-1,
```

the odd $2$-adic fixed point. Since $\mathbb N_0$ is dense in $\mathbb Z_2$,
a finite union of binary cylinders that covers every ordinary parameter is
closed and must also cover $k_\star$. One leaf is therefore an obstructed
ghost cylinder. Hence no finite binary-cylinder cover with one fixed uniform
one-turn affine path per leaf proves all of $36\mathbb N_0+27$ recursive.

This theorem does not exclude an infinite well-founded tree, mixed
$2$-adic and $3$-adic refinement, fixed multi-turn paths, multiple further
subcases, or a global argument. It is an obstruction to one declared proof
architecture only.

## 6. One exact recursive subprogression

### Proposition BSC-CRS-12

The progression

```math
8748\mathbb N_0+6219
```

is recursive.

#### Proof

Write $n=8748t+6219$, which is the parameter class
$k=243t+172$ inside $n=36k+27$. One forward odd step gives

```math
T(n)=13122t+9329.
```

Apply the reverse word `001010111111` from left to right, where `0` is
$\rho_0$ and `1` is $\rho_1$. The coefficient/intercept pairs are

```math
\begin{aligned}
&(26244,18658),(52488,37316),(34992,24877),(69984,49754),\\
&(46656,33169),(93312,66338),(62208,44225),(41472,29483),\\
&(27648,19655),(18432,13103),(12288,8735),(8192,5823).
\end{aligned}
```

Every $\rho_1$ input is uniformly $2\pmod3$, every predecessor is a positive
odd integer, and the endpoint $m=8192t+5823$ satisfies

```math
T^{12}(m)=T(n),
\qquad
n-m=556t+396>0.
```

Thus $m<n$ and the two forward orbits meet. Equivalently,

```math
m=\frac{2048n-1611}{2187}<n.
```

This proves one $1/243$-subprogression of the unresolved $36k+27$ class. It
does not prove the remaining $242$ parameter classes. $\square$

## 7. Arithmetic certificate bars

Fix an integer base $p\ge2$ with canonical digits $0,\ldots,p-1$. A finite
word in base $p$ is read least-significant digit first and denotes a $p$-adic
cylinder. A prefix-free family $\mathfrak B_p$ is an **arithmetic certificate
bar** for a progression when:

1. every cylinder in $\mathfrak B_p$ carries a checked uniform affine path
   certificate; and
2. every eventually-zero base $p$ digit sequence has a prefix in
   $\mathfrak B_p$.

### Lemma (bar sufficiency)

An arithmetic certificate bar proves every ordinary nonnegative parameter in
the progression recursive.

#### Proof

Eventually-zero $p$-adic digit sequences are exactly the nonnegative
integers. The bar condition assigns every such parameter to a certified
cylinder. $\square$

Full $p$-adic coverage and Haar measure one are not required. The unresolved
work is a machine-checkable eventual-zero completeness argument, not a large
boundary-measure percentage.

## 8. Computational evidence boundary

The supplied F11 table is byte-identical to the released Fixture F11 and is
not new evidence. The artifacts retained in this repository update do not
contain the proposed depth-28, depth-30, or depth-32 catalog TSVs, a catalog
manifest, the claimed
breadth-first and depth-first miners, or an independent catalog replay
program. Aggregate counts in prose cannot establish row existence,
prefix-freeness, affine admissibility, descent, or independent agreement.

Accordingly, BSC does not promote the catalog claims. A future computational
claim requires, at minimum:

- the complete generated catalogs with content hashes;
- both independently implemented miners or one miner plus an independent
  exhaustive checker;
- exact replay of every affine path, congruence, positivity, and descent
  condition;
- prefix-free and nonnesting verification;
- a manifest binding parameters, source, runtime, and outputs; and
- negative fixtures for omitted, duplicated, malformed, or understated
  rows.

Even those artifacts would certify only the declared restricted finite
catalog. They would not establish an arithmetic bar, the entire
$36k+27$ progression, Ansari's $F_2$, or the Collatz conjecture.

## 9. Retained non-converses

- Coefficient contraction does not imply affine descent.
- Positive valuation capacity does not imply path existence or certificate
  success.
- Kernel containment without properness does not imply RS under BSC's
  definition.
- One recursive subprogression does not prove its parent progression.
- Positive or increasing $p$-adic coverage does not prove eventual-zero
  completeness.
- A finite catalog does not establish a universal certificate tree.
- A log-slope identity is not a physical conservation law.
