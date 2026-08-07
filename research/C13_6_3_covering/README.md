# A 20-block partial $(13,6,3)$ covering and conditional rigidity

## Status and authority

This directory is a standalone finite-combinatorics research artifact. It is
included in the repository for inspection and reproducibility; it is **not** a
BSC theorem, BSC fixture, release result, formal-kernel proof, or claim that
the open covering number has been determined.

The public covering record checked on 7 August 2026 gives

$$
20\leq C(13,6,3)\leq21.
$$

Here $C(v,k,t)$ is the minimum number of $k$-subsets, called blocks, needed to
contain every $t$-subset of a $v$-set. The source record is the
[La Jolla entry for C(13,6,3)](https://ljcr.dmgordon.org/cover/show_cover.php?k=6&t=3&v=13).
Its frozen data family is available from the
[La Jolla Coverings Repository dataset](https://zenodo.org/records/19735294).
The displayed 21-block construction is credited to that record and is
retained in normalized mathematical form in
[`construction.json`](construction.json).

Source attribution: Daniel M. Gordon, *La Jolla Coverings Repository*,
version 1.2, DOI
[`10.5281/zenodo.19735294`](https://doi.org/10.5281/zenodo.19735294), CC BY
4.0. The cited entry was extracted and normalized as integer arrays; its
mathematical blocks were not changed. The independently reconstructed
20-block family and its exact differences from that source are separately
identified.

Two results are separated throughout:

- **C13-COV-01** is an explicit 20-block family covering 284 of the 286
  triples. This is an independently reproduced computational construction.
- **C13-RIG-01** is a conditional rigidity theorem about any hypothetical
  complete 20-block cover. Its proof is hand checked, and every finite
  arithmetic boundary step is replayed by the dependency-free checker.

Neither result proves $C(13,6,3)=21$, proves that 284 is optimal for twenty
blocks, or establishes historical priority.

## C13-COV-01: the two-triple leave

The tracked family contains twenty distinct 6-subsets of
$\lbrace1,\ldots,13\rbrace$. Direct enumeration gives

$$
284\text{ covered triples out of }\binom{13}{3}=286,
$$

with exact leave

$$
\lbrace2,5,7\rbrace,\qquad \lbrace5,7,10\rbrace.
$$

It retains 18 blocks of the archived 21-cover, removes

```text
1 2 7 8 10 11
1 3 4 7 8 12
2 3 5 7 10 12
```

and inserts

```text
1 3 4 7 8 11
2 3 7 8 10 12
```

This is a **3-for-2 block exchange**, not a design trade: the two sides have
unequal sizes and do not preserve all triple incidences.

Every one-block deletion from that particular source cover reaches at most
283 covered triples. Its complete deletion histogram is

```text
271:1  272:3  273:2  274:3  276:2
280:4  281:3  282:1  283:2
```

Thus the exchange is one triple better than simple deletion from the cited
construction. This is a comparison with one source cover, not a global
optimality result.

### Exact construction statistics

The verifier independently obtains:

| Quantity | Exact value |
|---|---:|
| point-degree histogram | $9^{10},10^3$ |
| pair-multiplicity histogram | $3^{24},4^{42},5^{12}$ |
| triple-multiplicity histogram | $0^2,1^{203},2^{58},3^{11},4^{12}$ |
| block-intersection histogram $n_0,\ldots,n_5$ | $(0,6,75,103,0,6)$ |
| $E_2,Q,H,U,D,J$ | $(90,47,35,2,96,90)$ |
| $S_1,S_2,S_3$ | $(495,444,163)$ |

For this partial cover, the corrected identities are

$$
3(Q+U)=E_2+D-39,
\qquad
z_1=172+H-2U.
$$

They read $147=147$ and $203=203$. Applying the complete-cover formulas
$3Q=E_2+D-39$ or $z_1=172+H$ would give false statements. Both mistakes are
retained as negative regressions.

## C13-RIG-01: conditional rigidity

### Theorem

Let $\mathcal B$ be a family of twenty distinct 6-subsets of a 13-set such
that every triple is contained in at least one block. Then the point degrees
have exactly one of the forms

$$
(10^3,9^{10}),\qquad(11,10,9^{11}),\qquad(12,9^{12}).
$$

In those three cases, respectively, at least

$$
183,\qquad184,\qquad185
$$

triples are contained in exactly one block. Consequently, some block contains
at least ten **private triples**, meaning triples contained in that block and
no other.

This is conditional on a 20-cover existing. It neither constructs one nor
rules one out.

### 1. Point degrees and pair-codegree excess

Fixing a point in a 20-cover leaves 5-subsets of the other twelve points that
must cover all pairs. The established value $C(12,5,2)=9$ in the
[La Jolla record](https://ljcr.dmgordon.org/cover/show_cover.php?k=5&t=2&v=12)
therefore gives $r_i\geq9$ for every point. Since

$$
\sum_i r_i=20\cdot6=120=13\cdot9+3,
$$

the three partitions of the remaining three degree units give precisely the
three displayed degree types.

The same public lower bound $C(13,6,3)\geq20$ makes a hypothetical 20-cover
simple: if two blocks were identical, deleting one would leave a 19-cover.

Every pair occurs in at least three blocks, because eleven possible third
points must be covered and one block containing the pair supplies only four.
Write

$$
e_{ij}=\lambda_{ij}-3\geq0,
\qquad
E_2=\sum_{i<j}e_{ij}^2.
$$

Then

$$
\sum_{i<j}e_{ij}=20\binom62-3\binom{13}2=66,
$$

and the excess degree at point $i$ is $5r_i-36$.

### 2. Exact block-intersection moments

Let $n_x$ count unordered block pairs meeting in $x$ points. Distinct
6-subsets of a 13-set have $0\leq x\leq5$. Let $\mu_T$ be the multiplicity of
triple $T$, and put

$$
Q=\sum_T\binom{\mu_T-1}{2},
\qquad
H=\sum_T\max(\mu_T-2,0).
$$

For a complete cover all $\mu_T\geq1$. Double counting points, pairs, and
triples in block intersections gives

$$
S_1=\sum_xxn_x=\sum_i\binom{r_i}{2},
$$

$$
S_2=\sum_x\binom{x}{2}n_x
=\sum_{i<j}\binom{3+e_{ij}}2
=399+\frac{E_2}{2},
$$

and

$$
S_3=\sum_x\binom{x}{3}n_x
=\sum_T\binom{\mu_T}{2}
=114+Q.
$$

The three values of $S_1$ are $495,496,498$. Since

$$
3\binom{x}{3}-2\binom{x}{2}+x
=(0,1,0,0,4,15)_x
$$

for $x=0,\ldots,5$, define

$$
D=n_1+4n_4+15n_5.
$$

The moment identity becomes

$$
3Q=E_2+D-c,
$$

where $c=39,40,42$ in degree types A, B, and C.

### 3. Pair-excess energy minima

For nonnegative integers with total $s$ in $N$ slots, convexity gives

$$
F(s,N)=\min\sum_{\ell=1}^N x_\ell^2
=(N-r)q^2+r(q+1)^2,
$$

where $s=Nq+r$ and $0\leq r<N$.

For type A, let $x$ be the total excess on the three high-high pairs. The
high-low and low-low totals are $42-2x$ and $24+x$, so

$$
E_2\geq
\min_x\bigl(F(x,3)+F(42-2x,30)+F(24+x,45)\bigr)=72.
$$

For type B, let $x$ be the excess on the unique pair of points whose degrees
are 11 and 10. The other category totals give

$$
E_2\geq
\min_x\bigl(x^2+F(19-x,11)+F(14-x,11)+F(33+x,55)\bigr)=82.
$$

For type C, the high-low and low-low totals are 24 and 42, giving

$$
E_2\geq F(24,12)+F(42,66)=90.
$$

The checker evaluates every displayed finite minimum.

### 4. Multiplicity cap through a degree-9 point

Fix a degree-9 point $i$. Its nine residual 5-blocks cover every pair on the
other twelve points. On those twelve points give edge $jk$ weight
$w_{jk}=\mu_{ijk}-1$. The total weight is

$$
9\binom52-\binom{12}2=24.
$$

If $\mu_{ijk}=m$, the weighted degrees at $j$ and $k$ are each at least
$4m-11$. Their two weighted stars share the edge $jk$, of weight $m-1$, so
their union has weight at least

$$
2(4m-11)-(m-1)=7m-21.
$$

Thus $7m-21\leq24$, and $m\leq6$.

Every triple in types B and C contains a degree-9 point. Type A has only one
possible exception, the triple formed by its three degree-10 points, whose
multiplicity is at most ten.

### 5. Residual packing penalty

Suppose a triple $T$ has multiplicity $m$. The $m$ distinct blocks containing
$T$ leave $m$ distinct residual 3-subsets of the other ten points. If their
point degrees are $a_1,\ldots,a_{10}$, then $\sum a_i=3m$ and

$$
P_m=\min\sum_i\binom{a_i}{2}.
$$

Balancing gives

| $m$ | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| $P_m$ | 2 | 5 | 8 | 12 | 18 | 24 | 30 |

Two blocks containing $T$ meet in $3$, $4$, or $5$ points according as their
residual triples meet in zero, one, or two points. Therefore the relevant
high-intersection penalty can be made explicit. Let $N_1(T)$ and $N_2(T)$
count residual-block pairs meeting in one and two points. Then

$$
\sum_i\binom{a_i}{2}=N_1(T)+2N_2(T)
$$

and those same pairs contribute $4N_1(T)+15N_2(T)$ to the global quantity
$J$. Hence

$$
J=4n_4+15n_5
\geq4N_1(T)+15N_2(T)
=4\bigl(N_1(T)+2N_2(T)\bigr)+7N_2(T)
\geq4P_m.
$$

The $n_1$ term in $D$ cannot pay this packing requirement. Also, the three
pairs of $T$ satisfy $e_{ij}\geq m-3$, so

$$
E_2\geq66+3(m-3)(m-4).
$$

### 6. Finite low-H boundary

For every triple of multiplicity $m\geq3$, write $t=m-2$. Its contributions
to $H$ and $Q$ are

$$
t,\qquad\frac{t(t+1)}2.
$$

The checker enumerates every partition of $H<11,12,13$ for types A, B, C,
applies the multiplicity caps, enumerates even $E_2$, reconstructs every
nonnegative $n_0,\ldots,n_5$ from the moment equations, and applies the $J$
and $E_2$ bounds. Forty-nine arithmetic states coalesce into ten boundary
profiles:

| Type | $H$ | positive $t$ parts | Final obstruction |
|---|---:|---|---|
| A | 9 | $3,3,3$ | Three multiplicity-5 triangles need more pair-collision budget. |
| A | 10 | $3,3,3,1$ | The same three-triangle obstruction. |
| A | 10 | $3,3,2,2$ | Two multiplicity-5 triangles need at least five heavy pair edges. |
| A | 10 | $2,2,2,2,2$ | Five multiplicity-4 triples cannot be supported by at most three $x=4$ block pairs. |
| A | 10 | $2,2,2,2,1,1$ | Four multiplicity-4 triples cannot be supported by two $x=4$ block pairs. |
| B | 11 | $4,4,3$ | Two multiplicity-6 triangles exceed the pair-collision budget. |
| B | 11 | $3,3,3,2$ | The packing equality would force five identical 4-point intersections and then at least six $x\geq4$ block pairs. |
| C | 12 | $4,4,4$ | Three multiplicity-6 triangles require at least six very-heavy pair edges; at most five are available. |
| C | 12 | $4,4,3,1$ | Two multiplicity-6 triangles require at least five very-heavy pair edges; at most four are available. |
| C | 12 | $3,3,3,3$ | The type-C energy permits at most two heavy low-low edges and hence at most two multiplicity-5 triangles. |

Here a multiplicity-5 triple is a triangle in the graph of pairs with
$e_{ij}\geq2$, while a multiplicity-6 triple is a triangle where
$e_{ij}\geq3$. Since

$$
E_2=66+2\sum_{i<j}\binom{e_{ij}}2,
$$

the first kind spends at least one collision unit per edge and the second at
least three. Two distinct triangles use at least five edges and three use at
least six.

For the type-A intersection lemma, with no $x=5$ block pair, each
multiplicity-4 triple needs at least two $x=4$ block pairs. If $n_4=2$ and
both block-pair intersections were the same 4-set, at least three blocks
would contain that 4-set, so all three pairs among them would meet in at least
four points; because $n_5=0$, this would force $n_4\geq3$. If the two 4-sets
were distinct, they would share at most one triple. Thus two $x=4$ pairs
cannot support four multiplicity-4 triples.

If $n_4=3$, equality of any two 4-set intersections similarly forces all
three to be the same 4-set, which contains only four triples. Otherwise the
three 4-sets are distinct, and each of their three pairwise comparisons can
share at most one triple, so at most three triples can be supported twice.
Thus three $x=4$ pairs cannot support five multiplicity-4 triples. The type-B
boundary profile has three multiplicity-5 triples, $E_2=82$, $n_4=5$, and
$n_5=0$. For each multiplicity-5 triple the packing bound is an equality, so
all five $x=4$ block pairs must contain that triple. The same three triples
therefore determine the same 4-set in every one of those five intersections.
Five distinct block pairs need at least four endpoint blocks; all six pairs
among four blocks containing that 4-set meet in at least four points. Because
$n_5=0$, they would all be $x=4$ pairs, forcing $n_4\geq6$, a contradiction.

For the final type-C profile there are four multiplicity-5 triples and
$E_2\leq94$. At its unique degree-12 point, the twelve high-low excesses have
sum 24, so convexity gives

$$
\sum_{j\ne i}\binom{e_{ij}}2\geq12.
$$

The total pair-collision budget is
$(E_2-66)/2\leq14$, leaving at most two collision units on low-low edges.
A multiplicity-5 triple through the high point needs one low-low edge with
$e\geq2$; an all-low multiplicity-5 triple needs three. Thus at most two such
triples can exist, contradicting the required four.

The checker records the complete roster and fails unless all ten profiles are
eliminated.

It follows that

$$
H\geq11,12,13.
$$

If $z_1$ is the number of multiplicity-one triples, the total triple excess
$400-286=114$ gives

$$
z_1=172+H.
$$

Hence $z_1\geq183,184,185$. Averaging those private triples over twenty
blocks proves that at least one block contains ten.

## Reproduction

From the repository root, run:

```bash
python research/C13_6_3_covering/verify_c13_covering.py
python -m unittest tests.test_c13_covering -v
```

The checker uses only the Python standard library. It rejects duplicate JSON
keys, malformed or changed blocks, false statistics, source-identity drift,
the uncorrected partial-cover formulas, a missing low-H boundary profile,
and altered claim boundaries.

The checker verifies finite arithmetic; it is not a search for a complete
20-cover and is not a proof-assistant kernel. The established external inputs
$C(12,5,2)=9$ and $C(13,6,3)\geq20$ remain cited dependencies.

## Prior-art and novelty boundary

Partial maximum-coverage problems are established; for example, Damaschke
studies the edge case in
[*Optimal partial clique edge covering guided by potential energy minimization*](https://doi.org/10.1007/s11590-019-01469-y).
Incidence, covering-excess, and block-intersection methods are also standard;
see the
[Gordon--Stinson survey](https://www.dmgordon.org/papers/hcd.pdf),
[Cameron--Soicher block-intersection polynomials](https://doi.org/10.1112/blms/bdm034),
and
[Franceti\'c--Herke--Horsley on covering excesses](https://arxiv.org/abs/1505.05949).

No matching public record for the explicit 284/286 family or the exact
parameter-specific rigidity bounds was located in the search recorded in
[`provenance.json`](provenance.json). The defensible wording is therefore
“no matching public record located,” not “first,” “optimal,” or “best known.”
Pointers to overlooked literature or independent computations are welcome.
