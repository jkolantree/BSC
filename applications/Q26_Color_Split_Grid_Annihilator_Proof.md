# Q26 color-split grid annihilator: proof and unrestricted Lean closure

## 1. Scope, semantics, and status

Write

\[
[26]=\{1,2,\ldots,26\}.
\]

The board is \([26]^2\), with one-based row and column coordinates. A queen at
\((r,c)\) dominates \((x,y)\) when

\[
x=r,\qquad y=c,\qquad x-y=r-c,\qquad\text{or}\qquad x+y=r+c.
\]

A set \(D\subseteq[26]^2\) is a *dominating set* when every board square is
occupied by or dominated by a queen in \(D\). The checkerboard color of a
square is

\[
\chi(r,c)=r+c\pmod 2.
\]

The retained one-based fourteen-queen witness is

\[
\begin{aligned}
&(2,6),(4,20),(6,10),(8,4),(10,16),(10,18),(12,24),\\
&(14,8),(16,14),(18,2),(20,12),(22,22),(24,26),(26,14).
\end{aligned}
\]

Direct independent witness checks confirm that these queens dominate all 676
squares, so \(\gamma(Q_{26})\le14\). Weakley's bound below gives
\(\gamma(Q_{26})\ge13\). Thus the established interval is

\[
13\le\gamma(Q_{26})\le14.
\]

The witness supplies no negative evidence about thirteen queens. Sections
2--10 retain the earlier human-readable five-profile argument. That route is
explicitly conditional on the cited Weakley consequences in Section 2.

Separately, the Lean project now proves the unrestricted thirteen-queen
theorem

```text
Q26GridAnnihilator.no_thirteen_queen_dominator :
  ¬ ∃ queens : Finset Square, Dominates queens ∧ queens.card = 13
```

Here *unrestricted* means that no color split, line inventory, canonical
profile, symmetry representative, or Weakley realization is assumed of the
hypothetical thirteen-queen set. Section 11 summarizes this formal route.
Combined with the cited lower bound and the retained fourteen-queen witness,
the mathematical conclusion is \(\gamma(Q_{26})=14\).

This mathematical theorem is separate from certified computation for the
repository's exact unrestricted Q26 root CNF. No independently replayed proof
certificate for that formula is currently recorded, so the existing root-CNF
receipt remains **UNKNOWN** and is not authority for the theorem. The
companion arithmetic checker is invoked as

```text
python -I -B tools/q26_grid_annihilator_checker.py --check
```

That command checks the finite profile arithmetic, the binomial coefficient
ratios, and the resulting valuation contradictions. It does not check the
Lean theorem, certify the exact root CNF, or independently prove the cited
results of Weakley or Alon.

A pinned Lean 4.32.1 project now checks the board/color geometry, the
arbitrary-cardinality occurrence-polynomial obstruction, the exact finite
shadow classification, both bichromatic obstruction recipes, all four
monochromatic orientations, and the omitted-diagonal endpoint shell. It also
retains the earlier five-profile development:

```text
cd formal/q26_grid_annihilator
lake build
lake env lean Q26GridAnnihilator/AxiomAudit.lean
```

The earlier theorem `no_weakley_canonical_realization` remains available as a
formalization of Sections 2--10. The principal unrestricted theorem is now
`no_thirteen_queen_dominator`; it has no missing Weakley, profile, or symmetry
bridge.

## 2. External theorem-level inputs

The queen-domination inputs are from William D. Weakley, *Queen Domination of
Even Square Boards*, *The Electronic Journal of Combinatorics* 29(2) (2022),
#P2.50, [doi:10.37236/10617](https://doi.org/10.37236/10617). The polynomial
nonvanishing theorem is Theorem 1.2 of Noga Alon, *Combinatorial
Nullstellensatz*, *Combinatorics, Probability and Computing* 8 (1999), 7--29,
[doi:10.1017/S0963548398003411](https://doi.org/10.1017/S0963548398003411).

Assume for contradiction that \(D\) is a dominating set with at most thirteen
queens. The required consequences of Weakley's results are these.

1. Weakley's general lower bound gives

   \[
   |D|\ge
   \min\left\{26,26,\left\lceil\frac{26+26-2}{4}\right\rceil\right\}=13.
   \]

   Hence \(|D|=13\), and \(D\) is minimum.

2. Such a set cannot be monochromatic. Weakley's Proposition 13, Definition
   14, and Theorem 18 would require odd integers \(d,e\), with
   \(1\le d,e\le13\), satisfying

   \[
   d^2+12e^2=741.
   \]

   Positivity gives \(e\in\{1,3,5,7\}\). The corresponding values of \(d^2\)
   are \(729,633,441,153\); the square cases have \(d=27\) or \(d=21\), both
   outside the permitted range. Thus the set is bichromatic.

3. Weakley's Proposition 11 gives checkerboard-color imbalance at most two.
   Since \(|D|=13\), the two color-class sizes are six and seven. Reflection
   in one board axis swaps the colors on an even-sided board, so normalize

   \[
   D=D_0\mathbin{\dot\cup}D_1,
   \qquad |D_0|=6,
   \qquad |D_1|=7,
   \]

   where every queen in \(D_p\) has color \(p\).

4. The equality-case argument in the proof of Weakley's Proposition 11 gives
   at most one repeated row and, independently, at most one repeated column.
   In Weakley's notation, for either line type \(t\), put
   \(H(t)=|L(t)|-h\), where \(|L(t)|\) is the excess line incidence and
   \(h\in\{1,2\}\). The proof gives, for both colors \(p\),

   \[
   |D_p|\ge\left\lceil\frac{13+H(t)}2\right\rceil.
   \]

   If \(H(t)\ge0\), both color classes would have at least seven queens.
   Also \(|L(t)|\ge0\) and \(h\le2\), so \(H(t)\ge-2\). Therefore
   \(H(t)\in\{-2,-1\}\), and
   \(|L(t)|=H(t)+h\le1\). Thus \(D\) occupies twelve or thirteen rows and,
   independently, twelve or thirteen columns.

5. Weakley's Lemma 6 supplies, in each line direction, two empty parallel
   lines at odd distance. Consequently the empty rows contain both index
   parities, and so do the empty columns.

No 69-shell, two-row-correlation, perimeter, SAT, or cube-search reduction is
used below.

## 3. Empty-line notation and incidence tables

Let \(X\subseteq[26]\) be the empty rows and \(Y\subseteq[26]\) the empty
columns. For \(i,j\in\{0,1\}\), define

\[
X_i=\{x\in X:x\equiv i\pmod2\},
\qquad
Y_j=\{y\in Y:y\equiv j\pmod2\},
\]

and write

\[
x_i=|X_i|,
\qquad
y_j=|Y_j|.
\]

Let \(w_r\) and \(w_c\) be the row and column excess incidences. By the
Weakley bridge,

\[
w_r,w_c\in\{0,1\}.
\]

Up to transposing the board, the three line-inventory types are

\[
W_0=(0,0),\qquad W_1=(1,0),\qquad W_2=(1,1).
\]

The numbers of empty rows and columns are \(13+w_r\) and \(13+w_c\).
Let

\[
a=\#\{\text{occupied even-indexed rows}\},
\qquad
b=\#\{\text{occupied even-indexed columns}\}.
\]

Because \([26]\) has thirteen indices of each parity,

\[
(x_0,x_1,y_0,y_1)
=(13-a,\ a+w_r,\ 13-b,\ b+w_c). \tag{3.1}
\]

If \(w_r=1\), let \(\delta_r=1\) when the duplicated occupied row is even and
\(\delta_r=0\) when it is odd; if \(w_r=0\), set \(\delta_r=0\). Define
\(\delta_c\) analogously. The even-row and even-column queen-incidence margins
are

\[
E_r=a+\delta_r,
\qquad
E_c=b+\delta_c. \tag{3.2}
\]

Let \(q_{ij}\) count queens whose row index has parity \(i\) and whose column
index has parity \(j\). The normalized color split says

\[
q_{00}+q_{11}=6,
\qquad
q_{01}+q_{10}=7.
\]

Together with the two incidence margins, this gives the unique table

\[
\begin{aligned}
q_{00}&=\frac{E_r+E_c-7}{2}, &
q_{01}&=\frac{E_r-E_c+7}{2},\\
q_{10}&=\frac{E_c-E_r+7}{2}, &
q_{11}&=\frac{19-E_r-E_c}{2}. \tag{3.3}
\end{aligned}
\]

A duplicate-parity lift is feasible exactly when all four values in (3.3) are
nonnegative integers.

## 4. The occurrence-polynomial vanishing lemma

### Lemma 4.1 (same-color empty-core annihilation)

Fix \(p\in\{0,1\}\), and enumerate the \(k=|D_p|\) queens of color \(p\) as
\((r_t,c_t)\), \(1\le t\le k\). Put

\[
d_t=r_t-c_t,
\qquad
s_t=r_t+c_t,
\]

and define the *occurrence polynomial*

\[
F_p(U,V)=
\prod_{t=1}^{k}(U-V-d_t)(U+V-s_t)
\in\mathbb{Q}[U,V]. \tag{4.1}
\]

If \(i+j\equiv p\pmod2\), then \(F_p\) vanishes on
\(X_i\times Y_j\).

#### Proof

Take \((x,y)\in X_i\times Y_j\). Its row and column are empty, so no queen
can dominate it orthogonally. Since \(D\) dominates the board, some queen must
dominate \((x,y)\) diagonally. A diagonal preserves checkerboard color, so that
queen belongs to \(D_p\). For its index \(t\), either

\[
x-y=d_t
\qquad\text{or}\qquad
x+y=s_t.
\]

The corresponding factor in (4.1) is zero. Hence
\(F_p(x,y)=0\). \(\square\)

The product is over queen occurrences, not over distinct diagonal labels.
Repeated difference or sum labels simply give repeated factors and do not
change the lemma.

## 5. The cardinality obstruction from Alon's theorem

The highest-degree homogeneous part of (4.1) is

\[
\begin{aligned}
(F_p)_{2k}(U,V)
&=(U-V)^k(U+V)^k\\
&=(U^2-V^2)^k\\
&=\sum_{j=0}^{k}(-1)^j\binom{k}{j}
  U^{2(k-j)}V^{2j}. \tag{5.1}
\end{aligned}
\]

### Lemma 5.1 (grid-cardinality bound)

Let nonempty finite \(A,B\subset\mathbb{Q}\), and suppose the occurrence
polynomial of \(k\) queens vanishes on \(A\times B\). Then, for every
\(j\in\{0,1,\ldots,k\}\),

\[
|A|\le2(k-j)
\qquad\text{or}\qquad
|B|\le2j. \tag{5.2}
\]

#### Proof

If both inequalities failed for some \(j\), then

\[
|A|>2(k-j),
\qquad
|B|>2j.
\]

The coefficient of
\(U^{2(k-j)}V^{2j}\) is the nonzero rational number
\((-1)^j\binom{k}{j}\), and its exponents sum to the total degree \(2k\).
Alon's Combinatorial Nullstellensatz, Theorem 1.2, would therefore give a point
of \(A\times B\) at which the polynomial is nonzero, contradicting the
vanishing hypothesis. \(\square\)

Elementary rounding of (5.2) gives the following equivalent compact form. If
\(a=|A|\), \(b=|B|\), and

\[
\epsilon(n)=
\begin{cases}
1,&n\text{ even},\\
0,&n\text{ odd},
\end{cases}
\]

then

\[
a+b\le2k+\epsilon(a)+\epsilon(b). \tag{5.3}
\]

Thus the bound is \(2k+2\) for even-even sizes, \(2k+1\) for mixed
parities, and \(2k\) for odd-odd sizes.

## 6. Grid remainders and the equality moment

Let \(A,B\subset\mathbb{Q}\) have sizes \(a,b\), and define their monic grid
polynomials

\[
g_A(U)=\prod_{\alpha\in A}(U-\alpha),
\qquad
g_B(V)=\prod_{\beta\in B}(V-\beta). \tag{6.1}
\]

Every polynomial has a unique remainder modulo \((g_A,g_B)\) whose separate
degrees satisfy \(\deg_U<a\) and \(\deg_V<b\). If the original polynomial
vanishes on \(A\times B\), so does the remainder. For each fixed
\(\beta\in B\), that remainder is a polynomial in \(U\) of degree below \(a\)
with all \(a\) points of \(A\) as roots, so it is zero. Its coefficients as
polynomials in \(V\), each of degree below \(b\), then vanish at every point
of \(B\), so the remainder is identically zero.

For coefficient bookkeeping, define the Lagrange functional

\[
\Lambda_A(P)=
\sum_{\alpha\in A}\frac{P(\alpha)}{g_A'(\alpha)}. \tag{6.2}
\]

It extracts the coefficient of \(U^{a-1}\) from the remainder of \(P\) modulo
\(g_A\). In particular,

\[
\Lambda_A(U^m)=0\quad(0\le m<a-1),
\qquad
\Lambda_A(U^{a-1})=1,
\qquad
\Lambda_A(U^a)=\sum_{\alpha\in A}\alpha. \tag{6.3}
\]

Define \(\Lambda_B\) analogously and apply the tensor functional
\(\Lambda_A\Lambda_B\). If a polynomial vanishes on \(A\times B\), the
functional is zero.

For the occurrence polynomial, write

\[
R=\sum_{t=1}^{k}r_t,
\qquad
C=\sum_{t=1}^{k}c_t. \tag{6.4}
\]

Each paired factor expands as

\[
\begin{aligned}
(U-V-d_t)(U+V-s_t)
&=U^2-V^2-2r_tU+2c_tV+(r_t^2-c_t^2).
\end{aligned}
\]

Consequently the next homogeneous part after (5.1) is

\[
(F_p)_{2k-1}
=(-2RU+2CV)(U^2-V^2)^{k-1}. \tag{6.5}
\]

### Lemma 6.1 (equality moment)

Suppose the occurrence polynomial of \(k\) queens vanishes on
\(A\times B\).

1. If \(a\) is even, \(b\) is odd, and \(a+b=2k+1\), then

   \[
   aR=k\sum_{\alpha\in A}\alpha. \tag{6.6}
   \]

2. If \(a\) is odd, \(b\) is even, and \(a+b=2k+1\), then

   \[
   bC=k\sum_{\beta\in B}\beta. \tag{6.7}
   \]

3. If \(a,b\) are even and \(a+b=2k+2\), then both (6.6) and (6.7) hold.

#### Proof

First suppose \(a\) is even, \(b\) is odd, and \(a+b=2k+1\). Set

\[
j=\frac{b-1}{2},
\qquad
a=2(k-j).
\]

Because the total degree of \(F_p\) is \(a+b-1\), equations (6.3)--(6.5)
show that the only contributions to
\(\Lambda_A\Lambda_B(F_p)=0\) are

\[
(-1)^j\binom{k}{j}
\left(\sum_{\alpha\in A}\alpha\right)
-2R(-1)^j\binom{k-1}{j}.
\]

Hence

\[
\binom{k}{j}\sum A
=2R\binom{k-1}{j}. \tag{6.8}
\]

Since

\[
\frac{\binom{k-1}{j}}{\binom{k}{j}}
=\frac{k-j}{k}
=\frac{a}{2k},
\]

equation (6.8) is exactly \(aR=k\sum A\).

If \(a\) is odd and \(b\) is even, the symmetric coefficient calculation
gives (6.7).

Finally suppose \(a,b\) are even and \(a+b=2k+2\). Apply
\(\Lambda_A\Lambda_B\) to \(VF_p\), which still vanishes on the grid, and set

\[
j=\frac{b-2}{2},
\qquad
a=2(k-j).
\]

The coefficient ledger is again

\[
(-1)^j\left[
\binom{k}{j}\sum A
-2R\binom{k-1}{j}
\right]=0,
\]

and gives (6.6). Applying the same argument to \(UF_p\), or interchanging
rows and columns, gives (6.7). \(\square\)

The both-odd equality case of (5.3) does **not** supply either first-moment
identity. No such claim is used here.

## 7. Direct reduction to five representatives

Apply (5.3) to the two color-0 rectangles, covered by the six queens in
\(D_0\):

\[
X_0\times Y_0,
\qquad
X_1\times Y_1. \tag{7.1}
\]

Also apply it to the two color-1 rectangles, covered by the seven queens in
\(D_1\):

\[
X_0\times Y_1,
\qquad
X_1\times Y_0. \tag{7.2}
\]

Let

\[
E=\epsilon(x_0)+\epsilon(x_1)+\epsilon(y_0)+\epsilon(y_1).
\]

Adding the two \(k=6\) inequalities for (7.1) gives

\[
26+w_r+w_c
=(x_0+x_1)+(y_0+y_1)
\le24+E. \tag{7.3}
\]

If \(w=0\), the two corresponding empty-line counts sum to thirteen and have
opposite cardinality parities, contributing exactly one to \(E\). If \(w=1\),
they sum to fourteen and have the same cardinality parity, contributing either
zero or two.

- In \(W_0\), \(E=2\), so (7.3) is equality.
- In \(W_1\), (7.3) forces the repeated-direction pair to be even-even,
  hence \(E=3\), again with equality.
- In \(W_2\), it forces all four counts to be even, hence \(E=4\), again
  with equality.

In every type, therefore, each of the two inequalities in (7.1) is separately
tight. Substituting these equalities into the two \(k=7\) inequalities for
(7.2) gives the following complete elementary case split.

The orbit reductions below use only transpose and half-turn. Both preserve
domination and checkerboard color. Transpose swaps row and column data. The
half-turn \((r,c)\mapsto(27-r,27-c)\) swaps even and odd line indices and sends

\[
(a,b)\longmapsto
(13-w_r-a,\ 13-w_c-b). \tag{7.4}
\]

When a direction has a duplicated line, it also sends
\(\delta_r\mapsto1-\delta_r\) or
\(\delta_c\mapsto1-\delta_c\), respectively. Thus it permutes feasible lifts,
swapping \(q_{00}\leftrightarrow q_{11}\) and
\(q_{01}\leftrightarrow q_{10}\); no lift is lost by taking orbit
representatives.

### Type \(W_0\)

Here \(x_0+x_1=y_0+y_1=13\).

- If \(x_0,y_0\) are even, tightness gives \(x_0+y_0=14\), and the cross
  bounds give \(x_0\in\{6,8\}\).
- If \(x_0,y_0\) are odd, tightness gives \(x_0+y_0=12\), and the cross
  bounds give \(x_0\in\{5,7\}\).
- If \(x_0\) is even and \(y_0\) odd, tightness gives
  \(x_0+y_0=13\), and the cross bounds give \(x_0\in\{6,8\}\).
- If \(x_0\) is odd and \(y_0\) even, the cross bounds give
  \(x_0\in\{5,7\}\).

Equivalently, the complete ledger before the exact incidence test is

| Parities of \((x_0,y_0)\) | Possible \((x_0,y_0)\) | Resulting \((a,b)\) |
|:--:|:--:|:--:|
| even, even | \((6,8),(8,6)\) | \((7,5),(5,7)\) |
| odd, odd | \((5,7),(7,5)\) | \((8,6),(6,8)\) |
| even, odd | \((6,7),(8,5)\) | \((7,6),(5,8)\) |
| odd, even | \((5,8),(7,6)\) | \((8,5),(6,7)\) |

The first two rows make \(a+b=26-(x_0+y_0)\) even, so (3.3) is not
integral. The mixed rows leave exactly

\[
(a,b)\in\{(5,8),(6,7),(7,6),(8,5)\}. \tag{7.5}
\]

Transpose and half-turn reduce these to representatives

\[
W_0(5,8),
\qquad
W_0(6,7). \tag{7.6}
\]

### Type \(W_1\)

Normalize by transpose so \((w_r,w_c)=(1,0)\). Then \(x_0,x_1\) are even,
while \(y_0,y_1\) have opposite parities. If \(y_0\) is even, tightness gives
\(y_0=14-x_0\), while \(x_1=14-x_0\) and \(y_1=x_0-1\). The two cross bounds
become

\[
2x_0-1\le15,
\qquad
28-2x_0\le16.
\]

If \(y_0\) is odd, tightness gives \(y_0=13-x_0\) and \(y_1=x_0\). The cross
bounds become

\[
2x_0\le16,
\qquad
27-2x_0\le15.
\]

Both cases give \(6\le x_0\le8\). Since \(x_0\) is even,
\(x_0\in\{6,8\}\), and the four raw pairs are

\[
(a,b)\in\{(5,7),(5,8),(7,5),(7,6)\}. \tag{7.7}
\]

The residual half-turn maps \((a,b)\) to \((12-a,13-b)\), leaving

\[
W_1(5,7),
\qquad
W_1(5,8). \tag{7.8}
\]

### Type \(W_2\)

All four empty parity counts are even. Tightness gives

\[
y_0=14-x_0,
\qquad
x_1=14-x_0,
\qquad
y_1=x_0.
\]

The cross bounds are

\[
2x_0\le16,
\qquad
2(14-x_0)\le16,
\]

so \(6\le x_0\le8\). Since \(x_0\) is even, the raw pairs are

\[
(a,b)\in\{(5,7),(7,5)\}, \tag{7.9}
\]

which form the single orbit represented by

\[
W_2(5,7). \tag{7.10}
\]

Thus the full coarse Weakley domain reduces directly to five representatives;
none of the later 69-shell cuts is part of this implication.

## 8. Every duplicate-parity lift

The following table lists every allowed duplicate-parity assignment for the
five representatives. A dash means that (3.3) is nonintegral and hence no
queen-parity table exists.

| Type and pair | \((x_0,x_1,y_0,y_1)\) | \((\delta_r,\delta_c)\) | \((E_r,E_c)\) | \((q_{00},q_{01},q_{10},q_{11})\) |
|:--|:--:|:--:|:--:|:--:|
| \(W_0(5,8)\) | \((8,5,5,8)\) | \((0,0)\) | \((5,8)\) | \((3,2,5,3)\) |
| \(W_0(6,7)\) | \((7,6,6,7)\) | \((0,0)\) | \((6,7)\) | \((3,3,4,3)\) |
| \(W_1(5,7)\) | \((8,6,6,7)\) | \((0,0)\) | \((5,7)\) | -- |
| \(W_1(5,7)\) | \((8,6,6,7)\) | \((1,0)\) | \((6,7)\) | \((3,3,4,3)\) |
| \(W_1(5,8)\) | \((8,6,5,8)\) | \((0,0)\) | \((5,8)\) | \((3,2,5,3)\) |
| \(W_1(5,8)\) | \((8,6,5,8)\) | \((1,0)\) | \((6,8)\) | -- |
| \(W_2(5,7)\) | \((8,6,6,8)\) | \((0,0)\) | \((5,7)\) | -- |
| \(W_2(5,7)\) | \((8,6,6,8)\) | \((0,1)\) | \((5,8)\) | \((3,2,5,3)\) |
| \(W_2(5,7)\) | \((8,6,6,8)\) | \((1,0)\) | \((6,7)\) | \((3,3,4,3)\) |
| \(W_2(5,7)\) | \((8,6,6,8)\) | \((1,1)\) | \((6,8)\) | -- |

Every feasible lift has

\[
q_{00}=q_{11}=3. \tag{8.1}
\]

Let

\[
R_0=\sum_{(r,c)\in D_0}r,
\qquad
R_1=\sum_{(r,c)\in D_1}r. \tag{8.2}
\]

Only the \(q_{11}\) queens of \(D_0\) lie in odd-indexed rows. Therefore

\[
R_0\equiv q_{11}\equiv1\pmod2. \tag{8.3}
\]

## 9. The five contradictions

For each of

\[
W_0(6,7),\qquad
W_1(5,7),\qquad
W_1(5,8),\qquad
W_2(5,7),
\]

the color-0 rectangle \(X_1\times Y_1\) has size \(6\times7\) or
\(6\times8\). It is tight in Lemma 5.1. Lemma 6.1, with \(k=6\) and row-set
size six, gives

\[
6R_0=6\sum_{x\in X_1}x,
\qquad\text{hence}\qquad
R_0=\sum_{x\in X_1}x. \tag{9.1}
\]

The right side is the sum of six odd integers and is even. This contradicts
(8.3), eliminating four representatives.

It remains to eliminate \(W_0(5,8)\). Here

\[
(x_0,x_1,y_0,y_1)=(8,5,5,8).
\]

Put

\[
A_0=\sum_{x\in X_0}x.
\]

The color-0 rectangle \(X_0\times Y_0\) has size \(8\times5\). Lemma 6.1
with \(k=6\) gives

\[
8R_0=6A_0. \tag{9.2}
\]

The color-1 rectangle \(X_0\times Y_1\) has size \(8\times8\). Lemma 6.1
with \(k=7\) gives

\[
8R_1=7A_0. \tag{9.3}
\]

Since \(R_1,A_0\) are integers and \(\gcd(7,8)=1\), equation (9.3) implies
\(8\mid A_0\). Write \(A_0=8t\). Equation (9.2) then gives

\[
R_0=6t,
\]

which is even, again contradicting (8.3). This eliminates the fifth
representative.

Subject to the cited Weakley bridge and the algebra above, the contradiction
shows that a thirteen-queen dominator of \(Q_{26}\) cannot exist.

## 10. A rejected overclaim: diagonal labels need not be distinct

Nothing in Lemma 4.1 or Alon's theorem says that the values \(d_t\) or
\(s_t\) are distinct. The occurrence polynomial deliberately retains repeated
factors. The leading term (5.1) and moment term (6.5) also count queens with
multiplicity. Therefore the proof above neither assumes nor proves distinct
difference or sum labels.

The stronger statement is false even for a genuine half-board dominator. On
the \(6\times6\) board,

\[
\{(1,1),(3,5),(5,3)\}
\]

is a three-queen dominating set, but its sum labels are \(2,8,8\). Thus
domination does not generally force square-free diagonal support. Any Q26
argument that inserts such a distinctness claim has an additional unsupported
premise; no such premise occurs in Sections 4--9.

## 11. The unrestricted Lean closure

The formal proof does not obtain `WeakleyCanonicalRealization` and does not
pass through the five representatives in Sections 7--9. Its route from an
arbitrary actual thirteen-queen dominator is as follows.

1. **Actual board to an arbitrary-cardinality shadow.** For each checkerboard
   color, the occurrence polynomial is formed from the queens actually in
   that color class. The theorem `occurrence_grid_alternatives_card` proves the
   complete top-coefficient grid alternatives for every cardinality \(k\),
   including \(k=0\). Applied to the four parity grids of empty rows and
   columns, these alternatives and the literal row, column, color, and
   incidence counts put `actualShadow queens` in the unrestricted finite
   `rawShadows` list. No \(6/7\) split is assumed at this stage.

2. **Exact finite split.** Kernel reduction in `exact_shadow_stats` gives
   exactly 36 raw shadows: 32 bichromatic records and four monochromatic
   records. Thus `actualShadow_recipe` sends every actual thirteen-queen
   dominator to one of those two branches. The \(6/7\) split and the small
   repetition excesses in the bichromatic branch are consequences of this
   enumeration, not imported Weakley hypotheses.

3. **The 32 bichromatic records.** `BichromaticRecipe` reduces them to two
   obstruction forms. The standard form has a six-queen color on a six-row by
   seven- or eight-column empty grid. Its checked equality moment identifies
   the queen-row sum with the sum of six same-parity empty rows, contradicting
   the three odd-row queen incidences. The exceptional form uses one common
   eight-row set: the six-queen color vanishes on an \(8\times5\) or
   \(8\times6\) grid, while the seven-queen color vanishes on an
   \(8\times8\) grid. The two checked moments give the incompatible
   divisibility and parity conditions. The theorem
   `no_bichromatic_actual_shadow` closes all 32 records without a
   five-profile or symmetry assumption.

4. **The four monochromatic records.** `MonochromaticRecipe` identifies the
   exact orientations in which all thirteen incidences lie in cell
   \(q_{01}\), \(q_{10}\), \(q_{11}\), or \(q_{00}\), with the corresponding
   full row and column supports. `MonochromaticBoardBridge` treats all four
   orientations, using the required reflections, and constructs a permutation
   \(\pi:[13]\simeq[13]\) whose opposite-parity \(13\times13\) core satisfies
   `MonoCoreCovered`.

5. **Difference and sum ledgers.** With one-based normalized coordinates, put

   \[
   d_i=i-\pi(i)+1,
   \qquad
   s_i=i+\pi(i).
   \]

   The checked permutation identities are

   \[
   \sum_i d_i=13,
   \qquad
   \sum_i s_i=182,
   \qquad
   \sum_i\bigl((d_i-1)^2+s_i^2\bigr)=3276. \tag{11.1}
   \]

   Also \(-11\le d_i\le13\), and each of the two supports has at most
   thirteen labels. Core coverage says that every target pair has either its
   difference in the \(d\)-support or its sum in the \(s\)-support.

6. **Least omitted shells.** The target differences are
   \(-12,-11,\ldots,12\). Since \(-12\) cannot be a queen difference, an even
   difference is omitted. Let \(h\) be the least absolute value of an omitted
   even difference. Let \(o\) be the analogous least omitted odd absolute
   value, using \(o=13\) as the sentinel when none is omitted. Missing a
   difference of absolute value \(t\) forces its full \((13-t)\)-label target
   sum shell into the \(s\)-support. Hence

   \[
   13\le h+o.
   \]

   Every same-parity target difference with smaller absolute value is forced
   into the \(d\)-support. If \(h=0\), then \(o=13\): twelve symmetric
   difference labels and the full thirteen-label even sum shell make the
   second moment \(4004\), contradicting (11.1). If \(h>0\), the forced
   difference set has \(h+o-2\) labels, so the support cap gives
   \(h+o\le15\). Parity leaves 13 or 15. The value 15 would force thirteen
   symmetric difference labels with sum zero, contradicting
   \(\sum d_i=13\). Therefore \(h+o=13\).

   In that remaining case there are eleven forced symmetric difference
   labels and thirteen forced sum labels. The two residual difference
   occurrences are \(a\) and \(13-a\). Exact kernel evaluation of the six
   possibilities \(h=2,4,6,8,10,12\), followed by (11.1), gives

   \[
   (2a-13)^2+12(2h-13)^2=741,
   \qquad 0\le a\le13,
   \qquad 0<h\le12.
   \]

   `no_q26_monochromatic_endpoint` checks that this has no solution, and
   `no_mono_core_covered` closes the monochromatic branch.

7. **Composition.** `Unconditional.lean` composes the exact shadow split,
   `no_bichromatic_actual_shadow`, the four-orientation board bridge, and
   `no_mono_core_covered`. Its exported theorem is

   ```text
   no_thirteen_queen_dominator :
     ¬ ∃ queens : Finset Square, Dominates queens ∧ queens.card = 13
   ```

The root module imports this theorem. `AxiomAudit.lean` reports only Lean's
standard `propext`, `Classical.choice`, and `Quot.sound`; the project uses no
project-defined axiom, `sorry`, or admitted theorem for this closure.

## 12. Evidentiary conclusion

Sections 2--10 remain a human-readable five-profile proof route whose stated
starting reductions depend on Weakley's published results. Section 11 records
a separate unrestricted Lean proof of the no-thirteen-queen theorem from the
bare actual-board assumptions. The two routes share occurrence-polynomial and
moment ideas, but the Lean theorem does not inherit the human route's Weakley
dependency.

Neither route changes the evidence status of the repository's exact
unrestricted root CNF. The existing root-CNF receipt remains **UNKNOWN**,
rather than a checked Q26 UNSAT certificate, unless and until a proof bound to
that exact formula is independently replayed. Solver exit codes, partial
proof files, and the companion arithmetic checker do not supply that missing
certificate authority.
