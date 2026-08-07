# A reproducible 156-shell symmetry-parity structural over-cover for $Q_{26}$

## Status and authority

Every hypothetical thirteen-queen dominator of $Q_{26}$ maps to one of 156
canonical parity-profile shells, or 142 after applying Weakley's empty-line
parity lemma. This note defines and reproduces that structural over-cover.

An earlier public summary incorrectly described these 156 shells as
exhaustively searched cases. No retained solver run returned `UNSAT`; the
objects reconstructed here are coarse structural shells, not solved SAT
instances.

Here a **shell** means only an occupied-line-count type together with two parity
counts; it is not a queen placement.

The conclusion is deliberately limited:

- every hypothetical thirteen-queen dominating set is covered by one of three
  occupied-line-count types;
- a reconstructed coarse quotient has $16+91+49=156$ shells;
- applying Weakley's empty-line parity lemma tightens that quotient to
  $15+78+49=142$ shells; and
- both totals are **over-covers**, not counts of realizable queen placements.

This note does **not** prove that thirteen queens cannot dominate $Q_{26}$, does
not establish $\gamma(Q_{26})=14$, and is not an independently reproducible
replay of historical computational work. The earlier asserted exhaustive search
has no retained case expander, generated instances, complete logs, or proof
artifacts; this repository generator reconstructs only the shell roster. No
retained solver output, LRAT or DRAT certificate, or equivalent artifact
establishes that every shell is unsatisfiable.

> **Current conclusion:** the structural over-cover and its orbit counts are
> reproducible; an exhaustive computational elimination of its cases is not.

As of 7 August 2026, the cited public record supports

$$
13\leq\gamma(Q_{26})\leq14.
$$

The lower bound follows from Theorem 1 of Weakley's 2022 paper, which supplies a
new proof of the previously published rectangular bound. The displayed sequence
in [OEIS A075458](https://oeis.org/A075458) ends at $n=25$, while
[Dmitry Kamenetsky's best-known-solution file](https://oeis.org/A075458/a075458.txt)
records the fourteen-queen upper bound $a(26)\leq14$. The unresolved decision
addressed here is whether thirteen queens suffice.

## 1. Coordinates, colors, and line inventories

Index rows and columns by $1,\ldots,26$. A queen on $(r,c)$ occupies an
**even-colored** square when

$$
r+c\equiv0\pmod2,
$$

and an odd-colored square otherwise. For a queen set $D$, write $D_0$ and
$D_1$ for its even- and odd-colored subsets.

Assume throughout that $D$ is a hypothetical dominating set with $|D|=13$.
Let

$$
\rho=\left|\lbrace\text{rows occupied by }D\rbrace\right|,\qquad
\kappa=\left|\lbrace\text{columns occupied by }D\rbrace\right|.
$$

Following Weakley's excess-index notation, define

$$
w_r=13-\rho=|L(\mathrm{row})|,
\qquad
w_c=13-\kappa=|L(\mathrm{column})|.
$$

Thus $w_r$ and $w_c$ count repeated row and column incidences beyond the first
queen on each occupied line. They do not count empty lines. The numbers of
empty rows and columns are $13+w_r$ and $13+w_c$, respectively.

Later, after fixing an occupied-line-count type, define

$$
a=\left|\lbrace\text{occupied even-indexed rows}\rbrace\right|,\qquad
b=\left|\lbrace\text{occupied even-indexed columns}\rbrace\right|.
$$

Here "even-indexed" refers to the one-based row or column number, not to the
checkerboard color of a square.

## 2. Published structural bridge

The theorem-level inputs in this section come from William D. Weakley,
["Queen Domination of Even Square Boards"](https://doi.org/10.37236/10617),
*The Electronic Journal of Combinatorics* 29(2) (2022), #P2.50
([direct PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p50/pdf/)).
The profile counts in later sections are elementary orbit calculations made in
this note; they are not claims made in Weakley's paper.

### 2.1 Exactly thirteen queens

Weakley's general bound is

$$
\gamma(Q_{m\times n})\geq
\min\left\lbrace
m,n,\left\lceil\frac{m+n-2}{4}\right\rceil
\right\rbrace.
$$

For $m=n=26$, the right-hand side is $13$. Consequently, any dominating set
with at most thirteen queens has exactly thirteen queens and is minimum.

### 2.2 A thirteen-queen set cannot be monochromatic

Suppose $D$ were monochromatic. Weakley's Proposition 13 and Definition 14
allow such a set to be put in the standard orientation required by Theorem 18.
Because $26\equiv2\pmod4$, that theorem then applies. With $k=26/2=13$, it
requires odd integers $d,e$ with $1\leq d,e\leq13$ satisfying

$$
d^2+(k-1)e^2=\frac{k(k^2+2)}{3},
$$

or

$$
d^2+12e^2=741.
$$

Positivity of $d^2$ forces $e\leq7$. The possible positive odd values give

| $e$ | $d^2=741-12e^2$ | Result |
|---:|---:|:---|
| 1 | 729 | $d=27>13$ |
| 3 | 633 | not a square |
| 5 | 441 | $d=21>13$ |
| 7 | 153 | not a square |

No admissible $(d,e)$ exists. Therefore a hypothetical $D$ must be
bichromatic.

### 2.3 The checkerboard split is $6/7$

Weakley's Proposition 11 says that a bichromatic dominating set of size $k$
on $Q_{2k}$ has checkerboard-color imbalance at most two. For odd $k=13$,
this gives

$$
\lbrace|D_0|,|D_1|\rbrace=\lbrace6,7\rbrace.
$$

A reflection in one board axis swaps the two checkerboard colors on an
even-sided board. Reflect once if necessary and henceforth normalize by

$$
|D_0|=6,\qquad |D_1|=7.
$$

### 2.4 At most one repeated row and one repeated column

The proof of Proposition 11 supplies a little more structure than its headline
color bound. For either line type
$t\in\lbrace\mathrm{row},\mathrm{column}\rbrace$, it
introduces

$$
H(t)=|L(t)|-h,
\qquad h\in\lbrace1,2\rbrace,
$$

and obtains, for both colors $q\in\lbrace0,1\rbrace$,

$$
|D_q|\geq
\left\lceil\frac{k+|L(t)|-h}{2}\right\rceil =
\left\lceil\frac{k+H(t)}{2}\right\rceil.
$$

For $k=13$, any $H(t)\geq0$ would force both color classes to contain at least
seven queens, contradicting $|D|=13$. Since $|L(t)|\geq0$ and $h\leq2$, one
also has $H(t)\geq-2$. Hence

$$
H(t)\in\lbrace-2,-1\rbrace.
$$

It follows that

$$
|L(t)|=H(t)+h\leq1.
$$

Therefore

$$
w_r,w_c\in\lbrace0,1\rbrace,
$$

so $D$ occupies either twelve or thirteen rows and, independently, twelve or
thirteen columns. Up to transpose, there are three occupied-line-count types:

| Type | $(w_r,w_c)$ | Occupied rows | Occupied columns |
|:---|:---:|---:|---:|
| $W_0$ | $(0,0)$ | 13 | 13 |
| $W_1$ | $(1,0)$ | 12 | 13 |
| $W_2$ | $(1,1)$ | 12 | 12 |

### 2.5 Empty lines of both index parities

Weakley's Lemma 6 states that, for each of rows and columns, a bichromatic
dominating set of size $n/2$ on even $Q_n$ with $n>4$ has two parallel empty
lines at odd distance. Their indices have opposite parity. Thus the empty rows
must include both index parities, and so must the empty columns.

This constraint will tighten the reconstructed 156-shell partition to 142
shells in Section 6.

## 3. Symmetry normalization

After the $|D_0|=6$ color orientation is fixed, the color-preserving subgroup
of the board's dihedral symmetries is

$$
G=\langle T,R\rangle=\lbrace\mathrm{id},T,R,TR\rbrace,
$$

where

$$
T(r,c)=(c,r),\qquad
R(r,c)=(27-r,27-c).
$$

Here $T$ is transpose and $R$ is the half-turn. The other four board
symmetries swap checkerboard colors; their role has already been used to choose
which color contains six queens. Because six and seven are unequal, fixing the
six-queen color loses no full-dihedral orbits.

If a dimension has $o$ occupied lines and $e$ of them have even index, the
half-turn reverses index parity and sends

$$
e\longmapsto o-e.
$$

Consequently, the action on a profile pair $(a,b)$ depends on the inventory
type. Each orbit below is represented by its lexicographically least pair.

This quotient acts only on the occupied-line parity pair $(a,b)$. It is not a
placement-level symmetry-breaking condition on the thirteen queen coordinates.

## 4. The reconstructed coarse quotient: 156 shells

### 4.1 Type $W_0$: thirteen occupied rows and columns

There are no repeated rows or columns. Each occupied row and each occupied
column contains exactly one queen, so $a$ and $b$ are also the row- and
column-parity margins of the queens.

Let $q_{ij}$ be the number of queens whose row index has parity $i$ and column
index has parity $j$, where $0$ means even and $1$ means odd. Write
$x=q_{00}$. The margins give

$$
\begin{pmatrix}
q_{00}&q_{01}\\
q_{10}&q_{11}
\end{pmatrix} =
\begin{pmatrix}
x&a-x\\
b-x&13-a-b+x
\end{pmatrix}.
$$

The even-colored queens occupy the even/even and odd/odd cells, so the
normalization $|D_0|=6$ gives

$$
x+(13-a-b+x)=6,
$$

and therefore

$$
x=\frac{a+b-7}{2}.
$$

Retain exactly those $(a,b)$ for which $x$ is integral and all four table
entries are nonnegative. Equivalently, the two diagonal cells are arbitrary
nonnegative integers summing to six, while the two off-diagonal cells are
arbitrary nonnegative integers summing to seven. There are therefore

$$
(6+1)(7+1)=7\cdot8=56
$$

raw tables, in one-to-one correspondence with the retained margin pairs.

On these pairs, the four group elements act as

$$
(a,b),\qquad
(b,a),\qquad
(13-a,13-b),\qquad
(13-b,13-a).
$$

The Burnside fixed-point counts are:

- identity: all $56$ pairs;
- transpose: $0$, because feasibility requires $a+b$ odd, while $a=b$ makes
  it even;
- half-turn: $0$, because it would require $a=b=13/2$; and
- transpose followed by half-turn: $8$, namely the feasible pairs with
  $a+b=13$.

Thus $W_0$ contributes

$$
\frac{56+0+0+8}{4}=16
$$

coarse orbit labels.

### 4.2 Type $W_1$: twelve occupied rows and thirteen columns

Use transpose once to put the twelve-line dimension in the rows. Then

$$
0\leq a\leq12,\qquad 0\leq b\leq13,
$$

giving $13\cdot14=182$ raw pairs.

At this coarse layer, all pairs in the rectangle are retained. The repeated
row means that $a$ alone does not say whether thirteen queens include $a$ or
$a+1$ even-row incidences; the answer depends on the parity of the duplicated
row. The fine checkerboard contingency constraints are deliberately deferred
rather than guessed from $(a,b)$.

Transpose exchanges the $(12,13)$ and $(13,12)$ orientations and has already
been consumed by the convention that the twelve-line dimension is called
"rows." The only remaining nontrivial action on normalized $W_1$ pairs is the
half-turn

$$
(a,b)\longmapsto(12-a,13-b).
$$

It has no fixed point because a fixed pair would require $b=13/2$. Hence

$$
\frac{13\cdot14}{2}=91
$$

coarse orbit labels remain.

### 4.3 Type $W_2$: twelve occupied rows and columns

Here

$$
0\leq a,b\leq12,
$$

so there are $13^2=169$ raw pairs. The orbit is

$$
\lbrace(a,b),(b,a),(12-a,12-b),(12-b,12-a)\rbrace.
$$

The Burnside fixed-point counts are:

- identity: $169$;
- transpose: $13$ pairs with $a=b$;
- half-turn: the single pair $(6,6)$; and
- transpose followed by half-turn: $13$ pairs with $a+b=12$.

Therefore $W_2$ contributes

$$
\frac{169+13+1+13}{4}=49
$$

coarse orbit labels.

### 4.4 Coarse total

The reconstructed coarse partition is

$$
16+91+49=\boxed{156}.
$$

This is the exact orbit count of the reconstructed scheme above. It is
exhaustive only as an over-cover and deliberately includes labels that cannot
lift to a $6/7$ queen placement.

## 5. Why 156 is an exhaustive over-cover

Let $D$ be any hypothetical thirteen-queen dominating set.

1. Section 2 makes $D$ bichromatic with a $6/7$ split and restricts it to one
   of $W_0,W_1,W_2$ up to transpose.
2. A color-swapping reflection, if necessary, puts the six-queen color on
   even-colored squares.
3. The occupied-line counts of $D$ determine a pair $(a,b)$ in the stated
   range for its type.
4. A color-preserving symmetry sends that pair to the canonical representative
   of its orbit.

Therefore every hypothetical $D$ maps to one of the 156 shells. No converse
has been asserted: a shell need not determine, or even admit, a queen
placement.

## 6. Lemma-6 tightening: 142 shells

Suppose a dimension has $o$ occupied lines and $e$ of them have even index.
Because the board has thirteen lines of each index parity, the counts of empty
even- and odd-indexed lines are

$$
13-e,
\qquad
13-(o-e)=13-o+e.
$$

Lemma 6 requires both numbers to be positive. Therefore:

- when $o=13$, one must have $1\leq e\leq12$;
- when $o=12$, both numbers are already positive for every
  $0\leq e\leq12$.

Apply this separately to rows and columns.

### 6.1 Tightened $W_0$ count

Require $1\leq a,b\leq12$. This removes four raw pairs forming the single
orbit represented by $(0,7)$. The fixed-point counts become
$52,0,0,8$, so

$$
\frac{52+0+0+8}{4}=15.
$$

The fifteen canonical $W_0$ representatives are

$$
\begin{aligned}
&(1,6),(1,8),\\
&(2,5),(2,7),(2,9),\\
&(3,4),(3,6),(3,8),(3,10),\\
&(4,5),(4,7),(4,9),\\
&(5,6),(5,8),\\
&(6,7).
\end{aligned}
$$

### 6.2 Tightened $W_1$ count

The twelve occupied rows need no further restriction, but thirteen occupied
columns require $1\leq b\leq12$. There are now

$$
13\cdot12=156
$$

raw pairs. The half-turn still has no fixed point, so $W_1$ contributes

$$
156/2=78
$$

shells.

### 6.3 Tightened $W_2$ count

Both dimensions have twelve occupied lines, so Lemma 6 is automatic throughout
the existing range. The count remains $49$.

### 6.4 Tightened total

| Type | Coarse shells | After Lemma 6 |
|:---|---:|---:|
| $W_0$: $(13,13)$ occupied lines | 16 | 15 |
| $W_1$: $(12,13)$ occupied lines | 91 | 78 |
| $W_2$: $(12,12)$ occupied lines | 49 | 49 |
| **Total** | **156** | **142** |

Thus the published empty-line parity constraint tightens the over-cover to

$$
15+78+49=\boxed{142}.
$$

The safe description is **142 canonical shells in a tightened exhaustive
over-cover**. It is not correct to call them 142 realizable placements or 142
independently certified UNSAT cases.

## 7. Standard-library reproduction

The repository retains the canonical dependency-free generator at
[`tools/q26_symmetry_profiles.py`](../tools/q26_symmetry_profiles.py) and its
complete materialized roster at
[`Q26_symmetry_parity_profiles.json`](Q26_symmetry_parity_profiles.json). Run

```text
python tools/q26_symmetry_profiles.py
python tools/q26_symmetry_profiles.py --check applications/Q26_symmetry_parity_profiles.json
```

The compact standard-library program below independently regenerates both totals
directly from the definitions above. It is a fresh enumerator for this note, not
a replay of the discarded exploratory scripts.

```python
from itertools import product


def w0_raw_pairs():
    pairs = set()
    for a, b in product(range(14), repeat=2):
        numerator = a + b - 7
        if numerator % 2:
            continue
        x = numerator // 2
        cells = (x, a - x, b - x, 13 - a - b + x)
        if min(cells) >= 0:
            pairs.add((a, b))
    return pairs


def quotient_w0(pair):
    a, b = pair
    return min(
        (a, b),
        (b, a),
        (13 - a, 13 - b),
        (13 - b, 13 - a),
    )


def quotient_w1(pair):
    a, b = pair
    return min((a, b), (12 - a, 13 - b))


def quotient_w2(pair):
    a, b = pair
    return min(
        (a, b),
        (b, a),
        (12 - a, 12 - b),
        (12 - b, 12 - a),
    )


s0 = w0_raw_pairs()
s1 = set(product(range(13), range(14)))
s2 = set(product(range(13), repeat=2))

coarse = (
    {quotient_w0(pair) for pair in s0},
    {quotient_w1(pair) for pair in s1},
    {quotient_w2(pair) for pair in s2},
)

tightened = (
    {
        quotient_w0(pair)
        for pair in s0
        if 1 <= pair[0] <= 12 and 1 <= pair[1] <= 12
    },
    {
        quotient_w1(pair)
        for pair in s1
        if 1 <= pair[1] <= 12
    },
    {quotient_w2(pair) for pair in s2},
)

assert len(s0) == 56
assert tuple(map(len, coarse)) == (16, 91, 49)
assert tuple(map(len, tightened)) == (15, 78, 49)

print(tuple(map(len, coarse)), sum(map(len, coarse)))
print(tuple(map(len, tightened)), sum(map(len, tightened)))
print(sorted(tightened[0]))
```

Expected output:

```text
(16, 91, 49) 156
(15, 78, 49) 142
[(1, 6), (1, 8), (2, 5), (2, 7), (2, 9), (3, 4), (3, 6), (3, 8), (3, 10), (4, 5), (4, 7), (4, 9), (5, 6), (5, 8), (6, 7)]
```

## 8. What a shell contains—and what it omits

A shell records only

$$
(W_i,\text{ canonical }(a,b)).
$$

It does not specify:

- which particular rows and columns are occupied or empty;
- which line is duplicated in $W_1$ or $W_2$, or the parity of that duplicate;
- whether the duplicated row and duplicated column meet at the same queen;
- the queen-level $2\times2$ parity contingency table in the repeated-line
  cases;
- the thirteen queen coordinates; or
- diagonal domination.

This coarseness is why even 142 is not a minimal feasibility count. For
example, the $W_2$ label $(a,b)=(0,0)$ survives Lemma 6, but it forces every
occupied row and column to have odd index. Every queen would then lie on an
even-colored square, contradicting the required $6/7$ color split. Keeping
such a label cannot omit a solution; it only creates unnecessary downstream
work.

For a complete search, each retained shell must expand to **every** compatible
concrete row and column inventory, every compatible repeated-line choice, and
every queen placement consistent with those inventories. The resulting
placement must then satisfy the original domination predicate on all 676 board
squares.

## 9. What would constitute a reproducible resolution

A new negative computation should, at minimum:

1. regenerate and retain the canonical shell roster;
2. prove or mechanically check that every allowed concrete inventory is
   assigned to a shell;
3. encode every surviving placement case without undocumented pruning;
4. retain every generated instance with its byte length and cryptographic hash;
5. produce machine-checkable UNSAT evidence covering every negative instance;
6. independently replay every certificate;
7. mechanically verify that the case cover is complete and unchanged, rejecting
   missing, duplicate, contradictory, or altered instances; and
8. archive the generator, environment, formulas, cover, logs, certificates,
   checker versions, and hashes.

An independently verified thirteen-queen coordinate list would settle the
positive branch immediately. A timeout, solver agreement, conflict count,
`UNKNOWN`, or a `NO_WITNESS` summary does not settle the negative branch.

Useful falsification targets for this note are correspondingly narrow:

- exhibit a valid thirteen-queen dominator that maps to none of the 142 shells;
- identify an invalid theorem specialization in Section 2;
- find an incorrect group action or Burnside fixed-point count;
- make the reproduction program disagree with its asserted counts; or
- show that a claimed downstream search failed to expand some compatible
  inventory or placement within a retained shell.

Finding an impossible retained shell is **not** a counterexample to
exhaustiveness; it confirms that the partition is an over-cover.

## Scope boundary

This is a bounded independent reconstruction of one structural case split. It
is not a priority claim, a proof of a new domination number, a claim of the
surrounding BSC framework, or evidence that an unretained computation
succeeded. Corrections and counterexamples to the theorem bridge, symmetry
action, counts, or reproduction code are welcome.
