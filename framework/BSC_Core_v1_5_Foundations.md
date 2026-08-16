# BSC Core v1.5 foundations

## Product readiness, cyclic caps, and operational identifiability

## Status and reading contract

This note is a candidate foundations module for **BSC Core v1.5**. It does
not revise or reinterpret an immutable earlier release.

| Item | Status in this note |
|---|---|
| Product readiness semantics | Defined and proved closed under coordinatewise meet |
| Cyclic readiness propagation | Finite greatest-compatible-fixed-point theorem proved |
| Exact operational identifiability | Fiber, kernel, quotient, and factorization equivalences proved |
| Finite intervention selection | Exact reduction to weighted set cover proved |
| Approximate identifiability | Oscillation monotonicity and a local decision theorem proved |
| Intervention-indexed deficiency | Proposed extension with elementary conditional consequences |
| Machine verification | Not supplied by this note |
| Mathematical novelty | Unknown; no novelty claim is made |
| Physical or empirical validation | Not supplied by these abstract theorems |

Here, **proved** means that a human-readable proof appears below. It does not
mean kernel checked. The proposed architecture is deliberately separated from
the theorems. The accompanying
[prior-art equivalence matrix](../research/BSC_Core_v1_5_Prior_Art_Equivalence_Matrix.md)
records close antecedents and the resulting limits on originality claims.

The order convention is important. For readiness values, $x\le y$ means that
$x$ licenses no more uses than $y$. Dependency propagation therefore moves
downward or stays fixed. It never promotes a claim.

## 1. Product readiness semantics

### 1.1 Verdict, outcome, and readiness are different types

A claim $c$ has three logically different records.

1. Its **claim-local verdict** records whether its proposition is true, false,
   open, or ill-posed. Verdicts have the discrete order: dependency propagation
   does not change them.
2. Its **outcome or polarity record** records supporting, adverse, mixed, or
   absent observations. Polarity is not a support ladder. In particular, an
   independently replicated contradiction is not below an untested claim.
3. Its **readiness record** states which declared uses are licensed by the
   maturity, scope, authority, identity, and other applicable gates.

If a project needs an order on polarity, it must declare what the order means.
For example, inclusion of separately retained supporting and adverse artifact
sets is an information order, not an endorsement order. An adverse artifact
may increase the information recorded while decreasing the set of claims that
remain admissible. BSC therefore keeps polarity out of the default readiness
meet.

This separation repairs the main defects of a single displayed chain:

| Legacy compression | Typed replacement |
|---|---|
| `contradicted < untested < single study < replicated` | empirical polarity and empirical maturity |
| `failed < unexecuted < executed < exact receipt` | execution state, outcome, exactness, and identity |
| `present proof < verified preprint < verified publication` | proof availability, review status, and authority flags |
| `local only < bounded < certified` | transfer scope and certification authority |

The replacement does not assert that every factor is a chain. Two scopes can
be incomparable, and two authority bundles can pass different independent
checks.

### Definition 1.1 (Applicable readiness signature)

Let $\mathcal J$ be the registry of readiness-coordinate names. For each claim
$c$, let the following be a finite set:

```math
A(c)\subseteq\mathcal J
```

be the set of coordinates whose questions are meaningful for that claim. For
each $j\in A(c)$, let $L_{c,j}$ be a finite meet-semilattice with top element
$\top_{c,j}$. Its order has the licensing interpretation fixed above.

The readiness type of $c$ is the dependent product

```math
R_c=\prod_{j\in A(c)}L_{c,j}.
```

For $r,s\in R_c$, define

```math
r\le_c s
\quad\Longleftrightarrow\quad
r_j\le_{c,j}s_j\text{ for every }j\in A(c).
```

The top and meet are coordinatewise:

```math
(\top_c)_j=\top_{c,j},
\qquad
(r\wedge_c s)_j=r_j\wedge_{c,j}s_j.
```

The complete typed status is a dependent record

```math
\mathsf{Status}(c)
=
\bigl(v_c,o_c,A(c),r_c\bigr),
```

where $v_c$ is the verdict, $o_c$ is the outcome record, and $r_c\in R_c$.

### Proposition 1.2 (Product readiness is a finite meet-semilattice)

For every claim $c$, the product $R_c$ in Definition 1.1 is a finite
meet-semilattice with top. Its partial order, meet, and top are the
coordinatewise ones displayed there.

#### Proof

Reflexivity, antisymmetry, and transitivity hold in each factor and therefore
coordinatewise in the product. For $r,s\in R_c$, the coordinatewise meet is
below both. If $t\le_c r$ and $t\le_c s$, then in every coordinate $j$,
$t_j$ is below $r_j\wedge_{c,j}s_j$; hence $t\le_c r\wedge_c s$. Thus the
displayed element is the greatest lower bound. The coordinatewise tuple of top
elements is above every element. Finiteness follows from finiteness of
$A(c)$ and of all its factors. $\square$

### 1.2 Why `N/A` is not a readiness value

Not applicable is represented by $j\notin A(c)$. It is an absence of a
coordinate from the claim's type, not an element of $L_{c,j}$.

There is no semantics-preserving universal placement of `N/A` inside a
readiness order:

- If `N/A` is top, a requirement on an inapplicable axis is silently passed.
- If `N/A` is bottom, a claim to which the axis is meaningless is silently
  blocked.
- If `N/A` is an intermediate element, it creates arbitrary comparisons
  between meaningful evidence and a question that was never asked.

Consequently, two readiness records are compared directly only when their
applicability signatures agree. A translation between different signatures
must be an explicit typed reindexing map. A dependency edge is well formed
only when every source coordinate it reads and every target coordinate it
caps is present in the corresponding signature. This makes an accidental
dependency on `N/A` a type error rather than a policy decision hidden in an
ordering convention.

### 1.3 Concrete factor design

The following factors are recommended, but BSC Core does not force a single
universal vocabulary.

- **Maturity:** a finite lattice of passed methodological stages. A powerset
  of named gates, ordered by inclusion, avoids pretending that incomparable
  review processes form one chain.
- **Scope:** an intersection-closed finite family of licensed contexts,
  ordered by inclusion. Meet is intersection. The full finite powerset is the
  simplest such choice.
- **Authority:** a set of independently satisfied authority checks, ordered
  by inclusion. Publication venue, proof availability, and independent replay
  should be different atoms.
- **Identity:** a set of bound identities, such as claim, source, data, code,
  environment, and output identity, ordered by inclusion.

An admission rule is a claim-local predicate on verdict, outcome, and
readiness. It need not be a scalar threshold and must not average independent
coordinates.

## 2. Cyclic readiness caps

The original DAG recursion has an unambiguous one-pass semantics. Feedback
contracts require a fixed-point semantics. This section supplies one for
finite cap systems.

### Definition 2.1 (Finite monotone cap system)

Let $G=(V,E)$ be a finite directed graph; loops and directed cycles are
allowed. Each vertex $v$ has a finite meet-semilattice with top $R_v$ and an
independently assigned initial readiness $r_v^0\in R_v$. Each edge
$e:u\to v$ has a monotone typed cap map

```math
\kappa_e:R_u\longrightarrow R_v.
```

An edge that affects only selected coordinates returns top in all unaffected
target coordinates. Let

```math
R=\prod_{v\in V}R_v
```

with its product order. Define $F:R\to R$ by

```math
F(r)_v
=
r_v^0\wedge_v
\bigwedge_{e:u\to v}\kappa_e(r_u),
```

where an empty meet is $\top_v$.

An assignment $s\in R$ is **cap-feasible** when

```math
s_v\le_v r_v^0
\quad\text{and}\quad
s_v\le_v\kappa_e(s_u)
\text{ for every edge }e:u\to v.
```

Equivalently, $s$ is cap-feasible exactly when $s\le F(s)$. A
**cap-stable** assignment is a fixed point $s=F(s)$.

### Theorem 2.2 (Finite cyclic greatest-compatible-fixed-point theorem)

For every finite monotone cap system, the iteration

```math
r^{(0)}=r^0,
\qquad
r^{(n+1)}=F\bigl(r^{(n)}\bigr)
```

is descending and stabilizes after finitely many steps at an assignment
$r^{\star}$. The limit $r^{\star}$ is cap-stable and is the unique greatest cap-feasible
assignment. In particular,

```math
r^{\star}\le r^0.
```

#### Proof

Every cap map is monotone, and finite meets are monotone in their arguments,
so $F$ is monotone. Directly from its definition,
$r^{(1)}=F(r^0)\le r^0$. If $r^{(n)}\le r^{(n-1)}$, monotonicity gives

```math
r^{(n+1)}=F\bigl(r^{(n)}\bigr)
\le
F\bigl(r^{(n-1)}\bigr)=r^{(n)}.
```

Thus the sequence descends. The finite product $R$ has no infinite strictly
descending sequence, so for some $N$,
$r^{(N+1)}=r^{(N)}$. Put $r^{\star}=r^{(N)}$; then
$F(r^{\star})=r^{\star}$.

It remains to prove greatestness. Let $s$ be any cap-feasible assignment. By
definition, $s\le r^0=r^{(0)}$ and $s\le F(s)$. Suppose inductively that
$s\le r^{(n)}$. Monotonicity gives

```math
s\le F(s)\le F\bigl(r^{(n)}\bigr)=r^{(n+1)}.
```

Hence $s\le r^{(n)}$ for every $n$, and therefore
$s\le r^{\star}$. So $r^{\star}$ is
the greatest cap-feasible assignment. A greatest element is unique. Finally,
$r^{\star}\le r^0$ follows from descent. $\square$

### Corollary 2.3 (No dependency promotion)

With fixed initial evidence, edge set, and cap maps, cyclic propagation can
only preserve or lower readiness. It cannot alter a verdict or create a
readiness coordinate absent from the initial typed record.

#### Proof

The verdict is not an input to the readiness update unless an explicit cap
reads it, and the update has no verdict output. Theorem 2.2 gives
$r^{\star}\le r^0$. Applicability signatures are fixed by the types. $\square$

### Corollary 2.4 (DAG one-pass recursion)

If $G$ is acyclic, choose a topological ordering and define

```math
\widehat r_v
=
r_v^0\wedge_v
\bigwedge_{e:u\to v}\kappa_e(\widehat r_u)
```

when vertex $v$ is reached. Then $\widehat r=r^{\star}$. Thus the existing DAG
recursion is the one-topological-sweep specialization of Theorem 2.2.

#### Proof

Every predecessor of $v$ occurs earlier, so the recursion is well defined.
After the sweep, each displayed equality holds, hence
$F(\widehat r)=\widehat r$. For any feasible $s$, induction through the
topological order gives $s_v\le\widehat r_v$: the initial bound and the edge
bounds hold at a source, and monotonicity of each cap propagates the induction
hypothesis at later vertices. Therefore $\widehat r$ is the greatest feasible
assignment, which is $r^{\star}$ by Theorem 2.2. $\square$

### 2.1 What the greatest fixed point does not prove

The theorem computes the largest assignment compatible with declared upper
bounds. It is a theorem about cap propagation, not a theorem that the initial
evidence is justified.

A cycle of identity caps can preserve high initial values. That does not make
the claims mutual proofs of one another. Grounded justification still needs
independent source artifacts, axioms, or an explicitly different inductive
least-fixed-point semantics. The certificate should therefore retain both the
cap graph and the provenance or proof graph. Conflating them would permit
circular support even though Theorem 2.2 itself performs no promotion.

The fixed-point result is a finite specialization of established monotone
fixed-point theory. No novelty is claimed for it.

## 3. Exact operational-envelope identifiability

### Definition 3.1 (Joint report and target query)

Let $X$ be a set of admissible physical completions, models, or parameter
states. Let $I$ be an intervention or instrument catalog. Intervention $i$
has a deterministic report map

```math
r_i:X\longrightarrow Y_i.
```

For $J\subseteq I$, define

```math
Y_J=\prod_{i\in J}Y_i,
\qquad
\rho_J:X\longrightarrow Y_J,
\qquad
\rho_J(x)=\bigl(r_i(x)\bigr)_{i\in J}.
```

The empty product is a singleton. Let $q:X\to Z$ be the target query. The
attainable report space is

```math
R_J=\rho_J(X)\subseteq Y_J,
```

and $\widehat\rho_J:X\to R_J$ is the same map with codomain restricted to its
image.

We say that $J$ **identifies** $q$ when equal joint reports force equal target
values.

### Theorem 3.2 (Operational identifiability equivalences)

The following statements are equivalent.

1. $J$ identifies $q$.
2. For all $x,x'\in X$,
   $\rho_J(x)=\rho_J(x')$ implies $q(x)=q(x')$.
3. The kernel relation of the joint report refines the kernel relation of the
   query:

```math
\ker(\rho_J)\subseteq\ker(q),
```

where $\ker(f)=\lbrace(x,x'):f(x)=f(x')\rbrace$.
4. The query is constant on every fiber of $\rho_J$.
5. There is a unique map $\overline q_J:R_J\to Z$ such that

```math
q=\overline q_J\mathbin\circ\widehat\rho_J.
```

6. The query descends uniquely to the quotient $X/{\sim_J}$, where
   $x\sim_Jx'$ exactly when $\rho_J(x)=\rho_J(x')$.

#### Proof

Statements 1 and 2 are the definition. Statement 2 says exactly that every
pair in $\ker(\rho_J)$ belongs to $\ker(q)$, proving equivalence with 3. It
also says exactly that $q$ is constant on every report fiber, proving
equivalence with 4.

Assume 4. For $y\in R_J$, define $\overline q_J(y)$ to be the unique $z$ for
which some $x$ satisfies $\rho_J(x)=y$ and $q(x)=z$. Such an $x$ exists by
the definition of $R_J$, and fiber constancy makes $z$ unique. The resulting
map is well defined and gives the factorization in 5. Since
$\widehat\rho_J$ is onto $R_J$, any factorization has this value at every
$y$, so it is unique. Conversely, a factorization makes $q(x)=q(x')$ whenever
$\rho_J(x)=\rho_J(x')$. Thus 4 and 5 are equivalent.

The equivalence with 6 is the same construction using equivalence classes
instead of attainable report tuples. $\square$

### Important codomain qualification

Uniqueness in Theorem 3.2 is on the attainable report space $R_J$. A map from
the entire ambient product $Y_J$ need not be unique away from $R_J$, and it
need not extend there without additional structure. Public statements should
not omit this qualification.

### Corollary 3.3 (Adding exact interventions refines ambiguity)

If $J\subseteq K\subseteq I$, every fiber of $\rho_K$ is contained in a
fiber of $\rho_J$. Therefore, if $J$ identifies $q$, then $K$ identifies
$q$.

#### Proof

Equality of all $K$-reports implies equality of the subfamily of $J$-reports.
Apply Theorem 3.2. $\square$

Identifiability is claim relative. The same $J$ may identify one query and
fail to identify another. It is also intervention relative: equality under an
observational report does not imply equality under interventions that were
not included in $J$.

## 4. Finite intervention selection is weighted set cover

Assume in this section that both $X$ and the candidate catalog $I$ are finite.
For each unordered two-element subset of $X$, write $\lbrace x,x'\rbrace$.

### Definition 4.1 (Target-separated and intervention-distinguished pairs)

Define

```math
U_q
=
\left\{
\lbrace x,x'\rbrace\subseteq X:
x\ne x'\text{ and }q(x)\ne q(x')
\right\}.
```

For each $i\in I$, define

```math
D_i
=
\left\{
\lbrace x,x'\rbrace\in U_q:
r_i(x)\ne r_i(x')
\right\}.
```

Thus $U_q$ contains exactly the pairs that the target query requires us to
separate, and $D_i$ records the required pairs separated by intervention $i$.

### Theorem 4.2 (Distinguishing-pair cover theorem)

For every $J\subseteq I$,

```math
J\text{ identifies }q
\quad\Longleftrightarrow\quad
U_q\subseteq\bigcup_{i\in J}D_i.
```

Consequently, for nonnegative intervention costs $w_i$, a minimum-cost
identifying family is exactly an optimal weighted set cover of universe $U_q$
by the derived sets $D_i$.

#### Proof

Suppose $J$ identifies $q$, and let $\lbrace x,x'\rbrace\in U_q$. Since
$q(x)\ne q(x')$, Theorem 3.2 implies that the joint reports cannot be equal.
Hence $r_i(x)\ne r_i(x')$ for some $i\in J$, so the pair belongs to $D_i$.
The sets indexed by $J$ cover $U_q$.

Conversely, suppose the sets indexed by $J$ cover $U_q$. If
$\rho_J(x)=\rho_J(x')$, then no $i\in J$ distinguishes the pair. The pair
cannot belong to $U_q$, because every member of $U_q$ is covered by some
$D_i$ with $i\in J$. Therefore $q(x)=q(x')$, and Theorem 3.2 shows that $J$
identifies $q$.

The feasible intervention families are therefore exactly the feasible set
covers, and both objectives are $\sum_{i\in J}w_i$. Their optima coincide.
$\square$

### Corollary 4.3 (Exact binary optimization form)

Introduce $z_i\in\lbrace0,1\rbrace$ to indicate whether intervention $i$ is
selected. The minimum-cost problem is

```math
\begin{aligned}
\text{minimize}\quad
&\sum_{i\in I}w_i z_i,\\
\text{subject to}\quad
&\sum_{i:\,p\in D_i}z_i\ge1
&&\text{for every }p\in U_q,\\
&z_i\in\lbrace0,1\rbrace
&&\text{for every }i\in I.
\end{aligned}
```

If $U_q$ is empty, $q$ is constant and the empty family is optimal. If some
pair in $U_q$ belongs to no $D_i$, the declared catalog contains no
identifying family.

When $q$ is injective and every report is binary, this is the classical
test-cover requirement of distinguishing every pair of models. Multi-valued
reports give the corresponding partition-test generalization. For general
$q$, it is target relative. These direct connections materially limit any
novelty claim for the combinatorial reduction.

## 5. Approximate operational identifiability

Exact equality is often too brittle for measured reports. Let every $Y_i$
carry a pseudometric $d_i$, and let $Z$ carry a metric $d_Z$. Fix nonnegative
tolerances $\varepsilon_i$.

### Definition 5.1 (Compatible pairs and target oscillation)

For $J\subseteq I$, define the compatible-pair relation

```math
C(J,\varepsilon)
=
\left\{
(x,x')\in X^2:
d_i\bigl(r_i(x),r_i(x')\bigr)\le\varepsilon_i
\text{ for every }i\in J
\right\}.
```

Define the target oscillation, allowing the value $+\infty$, by

```math
\omega_q(J,\varepsilon)
=
\sup_{(x,x')\in C(J,\varepsilon)}
d_Z\bigl(q(x),q(x')\bigr).
```

If $X$ is empty, take the supremum to be zero. For finite nonempty $X$, the
supremum is a maximum.

The relation $C(J,\varepsilon)$ need not be transitive when tolerances are
positive. It is therefore not silently treated as a quotient relation.

### Theorem 5.2 (Oscillation monotonicity)

The following monotonicity statements hold.

1. If $J\subseteq K$ and the tolerances agree on $J$, then

```math
\omega_q(K,\varepsilon)
\le
\omega_q(J,\varepsilon|_J).
```

2. On a fixed $J$, if $\varepsilon'_i\le\varepsilon_i$ for every $i\in J$,
   then

```math
\omega_q(J,\varepsilon')
\le
\omega_q(J,\varepsilon).
```

#### Proof

Adding interventions adds simultaneous constraints, so
$C(K,\varepsilon)\subseteq C(J,\varepsilon|_J)$. Tightening tolerances also
shrinks the compatible-pair set. A supremum of the same nonnegative function
over a subset cannot exceed its supremum over the original set. $\square$

### Theorem 5.3 (Carefully scoped decision-margin consequence)

Let $D:Z\to\mathcal A$ be a deterministic decision rule and fix a reference
completion $x_0\in X$. Define its claim-relative decision margin by

```math
m_D(x_0)
=
\inf\left\{
d_Z\bigl(q(x_0),z\bigr):
z\in q(X),\ D(z)\ne D\bigl(q(x_0)\bigr)
\right\},
```

with the infimum of the empty set taken as $+\infty$. If

```math
\omega_q(J,\varepsilon)<m_D(x_0),
```

then every $x$ satisfying $(x_0,x)\in C(J,\varepsilon)$ has

```math
D\bigl(q(x)\bigr)=D\bigl(q(x_0)\bigr).
```

#### Proof

For such an $x$, Definition 5.1 gives

```math
d_Z\bigl(q(x_0),q(x)\bigr)
\le\omega_q(J,\varepsilon)<m_D(x_0).
```

If the two decisions differed, $q(x)$ would be one of the points over which
the defining infimum for $m_D(x_0)$ is taken, forcing its distance from
$q(x_0)$ to be at least that infimum. This is a contradiction. $\square$

The strict inequality is essential without an additional boundary
convention. The theorem is local to the declared decision $D$, target $q$,
reference $x_0$, intervention family, and tolerances. It is not a global
inverse-stability theorem.

### Measurement-error conversion

Suppose a measured report $y_i$ is used to define candidate completions by

```math
d_i\bigl(r_i(x),y_i\bigr)\le\eta_i.
```

Two such candidates are separated by at most $2\eta_i$ by the triangle
inequality. Therefore a pairwise oscillation certificate for the whole
candidate set must normally use $\varepsilon_i=2\eta_i$, not
$\varepsilon_i=\eta_i$. A sharper constant requires additional structure.

Oscillation is a diameter bound. In a general metric space, diameter at most
$2\tau$ is necessary but not sufficient for containment in a ball of radius
$\tau$ with an allowed center. Theorem 5.3 avoids that false inference by using
a declared reference point and decision margin.

## 6. Proposed intervention-indexed causal deficiency

> **Architecture status:** proposed. The definition below is an ordinary
> directed deficiency applied to an intervention-expanded experiment. Its
> elementary properties are proved conditionally, but neither the definition
> nor those properties are claimed as novel.

### Definition 6.1 (Aligned interventional experiments)

Let $\mathcal A$ be a declared intervention set and $\Theta$ a parameter set,
with $\mathcal A\times\Theta$ nonempty. After an explicit intervention and
parameter alignment, let

```math
\mathsf E
=
\left\{P^{\mathsf E}_{a,\theta}:
(a,\theta)\in\mathcal A\times\Theta\right\}
```

be laws on a standard Borel report space $X_E$, and let

```math
\mathsf F
=
\left\{P^{\mathsf F}_{a,\theta}:
(a,\theta)\in\mathcal A\times\Theta\right\}
```

be laws on a standard Borel report space $X_F$. Using

```math
\lVert P-Q\rVert_{\mathrm{TV}}
=
\sup_B\lvert P(B)-Q(B)\rvert,
```

define

```math
\delta_{\mathrm{do}}(\mathsf E,\mathsf F)
=
\inf_K
\sup_{(a,\theta)\in\mathcal A\times\Theta}
\left\lVert
KP^{\mathsf E}_{a,\theta}
-P^{\mathsf F}_{a,\theta}
\right\rVert_{\mathrm{TV}},
```

where the infimum is over all Markov kernels
$K:X_E\rightsquigarrow X_F$, one of which is used uniformly for every
intervention and parameter. The existence of the displayed probability laws
and at least one such comparison kernel is part of the alignment contract; it
is not inferred from notation alone.

A restricted kernel class defines a different quantity. The elementary bounds
below remain valid for a nonempty restricted class, but the singleton-family
identification with ordinary deficiency requires the unrestricted class, and
the triangle inequality requires the declared classes to be closed under the
relevant kernel composition.

Allowing a different kernel $K_a$ for every intervention defines a different,
generally smaller quantity. A certificate must say which problem it solves.

### Proposition 6.2 (Basic consequences under the declared convention)

For the definition above:

1. $0\le\delta_{\mathrm{do}}\le1$.
2. If $\mathcal A$ has one element, the definition is ordinary directed
   total-variation deficiency.
3. Enlarging the intervention family cannot decrease the deficiency when all
   existing laws and the shared-kernel requirement remain fixed.
4. For three aligned experiments on the same $\mathcal A\times\Theta$,

```math
\delta_{\mathrm{do}}(\mathsf E,\mathsf G)
\le
\delta_{\mathrm{do}}(\mathsf E,\mathsf F)
+
\delta_{\mathrm{do}}(\mathsf F,\mathsf G).
```

#### Proof

The first two claims are immediate from total variation, nonemptiness of the
index and kernel classes, and the definition.
For the third, enlarging the supremum index set can only increase the error of
each fixed kernel; taking an infimum preserves the inequality.

For the fourth, choose kernels $K_{EF}$ and $K_{FG}$ within arbitrary
$\eta>0$ of their respective infima and use $K_{FG}K_{EF}$. For every
$(a,\theta)$, insert the corresponding intermediate target law between the
composed law and the final target law. The triangle inequality and contraction of
total variation under $K_{FG}$ bound the result by the two errors plus
$2\eta$. Take the supremum and let $\eta$ tend to zero. $\square$

### Proposition 6.3 (Bounded interventional risk transfer)

Under the total-variation convention in Definition 6.1, let the decision
space $D$ be standard Borel. Let
$L:\mathcal A\times\Theta\times D\to[0,M]$ be bounded and measurable in its
decision argument for every $(a,\theta)$. An intervention-indexed randomized
decision rule on $\mathsf F$ is a family of Markov kernels
$d_a:X_F\rightsquigarrow D$. Define its pointwise risk by

```math
R_{\mathsf F}(a,\theta;d)
=
\int_{X_F}\!\int_D
L(a,\theta,z)\,d_a(x,dz)\,
P^{\mathsf F}_{a,\theta}(dx).
```

If $\delta_{\mathrm{do}}(\mathsf E,\mathsf F)\le\epsilon$, then for every
$\eta>0$ and every such rule $d$, there is a rule on $\mathsf E$ whose risk
at every $(a,\theta)$ exceeds $R_{\mathsf F}(a,\theta;d)$ by at most
$M(\epsilon+\eta)$. If an optimizing comparison kernel exists, $\eta$ may be
zero.

#### Proof

Choose one comparison kernel $K$ within $\eta$ of the deficiency infimum and
use the composite decision kernel $d_aK$ on $X_E$. For fixed $(a,\theta)$,
the function

```math
x\longmapsto\int_D L(a,\theta,z)\,d_a(x,dz)
```

is measurable and takes values in $[0,M]$. The difference of its expectations
under $KP^{\mathsf E}_{a,\theta}$ and
$`P^{\mathsf F}_{a,\theta}`$ is therefore at most $M$ times their total
variation under the stated convention. Apply the uniform bound at each index.
$\square$

Different normalizations of total variation change the displayed constant.
Unbounded losses require separate integrability and tail hypotheses.

### 6.1 Why the subscript `do` is not enough

Indexing laws by symbols called interventions does not establish causal
validity. A causal-transfer certificate must additionally declare:

- the source and target causal-model classes;
- the intervention map and its domain;
- the observational and interventional laws;
- the estimand and identification assumptions;
- whether one shared garbling kernel is scientifically meaningful;
- the do-operation commutation defect or exact commutation theorem;
- the distinction between interventional and counterfactual claims;
- the optimization-gap evidence for any numerical deficiency claim; and
- the claim, source, data, code, environment, and output identities.

Without those items, $\delta_{\mathrm{do}}$ is only deficiency of a labeled
family of experiments. Observational equality alone cannot populate missing
interventional laws.

## 7. Claim boundary and adoption gates

### Proved in this note

- Product readiness over a fixed applicability signature is a finite
  meet-semilattice.
- Finite monotone cyclic caps have a greatest cap-feasible fixed point reached
  by descending iteration.
- The existing DAG rule is the acyclic one-pass corollary.
- Exact identifiability is equivalent to fiber constancy, kernel refinement,
  quotient descent, and unique factorization through attainable reports.
- Finite minimum-cost target identification is the derived weighted set-cover
  problem.
- Added reports and tightened tolerances cannot increase target oscillation.
- A strict local decision-margin condition transfers one declared decision.
- The elementary deficiency bounds hold for the proposed aligned
  intervention-expanded experiment.

### Proposed architecture

- Replace legacy readiness chains with typed outcome fields and product
  readiness factors.
- Retain `N/A` in the applicability signature rather than any lattice.
- Use cyclic cap closure for feedback contracts while preserving a separate
  grounded provenance or proof graph.
- Add target-relative intervention design and approximate oscillation to the
  operational-envelope profile.
- Add an intervention-indexed causal-transfer certificate as a refinement of
  the certificate layer, not as an unproved ninth morphism field.

### Unknown or not established here

- Novelty of the integrated BSC package.
- A BSC-specific categorical universal property.
- Associativity and coherence of the complete eight-field BSC record.
- Grounded proof semantics for arbitrary cyclic justification graphs.
- Statistical estimation of oscillation or deficiency from finite data.
- Efficient solution of the general intervention-selection optimization.
- Validity of any particular physical causal model or intervention map.
- Machine-checked correspondence for the full note: the shipped Lean theorem
  slice covers only the exact scope listed in its formal README, not the
  heterogeneous cap theorem, DAG corollary, weighted optimizer, local decision
  theorem, or causal-deficiency section.

## 8. Recommended public wording

The strongest wording supported by this document is:

> BSC Core v1.5 supplies human-readable proofs for a finite cyclic
> readiness-cap closure, exact target identifiability through operational
> reports, a finite target-relative set-cover formulation for intervention
> selection, and monotonic approximate target oscillation. It also proposes an
> intervention-indexed deficiency profile. These results use established
> order, quotient, experiment-comparison, and covering ideas; originality of
> their BSC integration remains unestablished pending external prior-art
> review. A bounded Lean-checked slice covers product readiness, a homogeneous
> cap specialization, attainable-report factorization, finite pair cover, and
> finite oscillation monotonicity; the remaining results require further
> formalization.

It would be inaccurate to say that this note proves a new foundational
category, validates a physical theory, establishes causal identification from
observational data, or proves the novelty of the intervention theorem.
