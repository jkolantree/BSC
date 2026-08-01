# Electrostatic critical-point transfer

## Status, provenance, and scope

This post-v1.4.0 application is an **independent reconstruction**. It is not a
merge or replay of an earlier candidate, and it does not change the BSC core,
the released paper, any fixture, or any release record.

The mathematical source records admitted for comparison are:

| Work record | Audited byte record | SHA-256 | Status |
|---|---|---|---|
| Arathoon, Ball, and Kvalheim, *The Maxwell Conjecture is False*, [arXiv:2607.27197v1](https://arxiv.org/abs/2607.27197v1) | PDF | `4178ddc5a4efcdc11726bea6d6d20785575c55564095dbf53bfaa6d26055a958` | arXiv v1; CC BY 4.0 |
| same arXiv version | source TAR | `85d3859f0c8bcf797911202890f885bbc2fd54e30ef930424f19493abd5b0dd5` | eight-entry source package; no script or receipt supplied |
| Edelsbrunner, Fillmore, and Oliveira, *Counting Equilibria of the Electrostatic Potential*, [arXiv:2501.05315v2](https://arxiv.org/abs/2501.05315v2) | PDF | `d2f91a62abcdf96170f81224cafc9ece7d7950c0663651e10b8ce9a1f6b0f489` | author manuscript v2; CC BY 4.0 |
| same arXiv version | source TAR | `5b135fd315afc0efdf5df3a6900904fd5cc611e3c95ea77f634a7ee3af9e1e6b` | source package; no script or receipt supplied |

The second work is published as DOI
[10.1112/plms.70163](https://doi.org/10.1112/plms.70163). The publisher's
version-of-record bytes were `NOT_OBTAINED`. Historical scripts, notebooks,
and machine receipts for the first work were `NOT_SUPPLIED`; consequently no
claim below is `mechanically_replayed`. The sources are credited and linked,
but their prose is not copied here.

The result is deliberately bounded. It does **not** provide:

- an exact global critical-point count for a finite configuration;
- an explicit generic perturbation or a certified robustness radius;
- an interval certificate for the illustrated value
  $\varepsilon=1/6$;
- a mechanically replayed historical calculation or kernel proof;
- stable electrostatic traps;
- an automatic extension from point charges to finite-size charge
  distributions;
- a four-charge maximum, novelty claim, or priority claim; or
- any identification of F12 derived holonomy with electromagnetic Wilson
  holonomy.

## 1. Normalized critical-point transfer

Let $V_\varepsilon$ be $C^2$ on a punctured domain in $\mathbb R^d$. Fix a
nonsingular center $x_0$, a length $r_\varepsilon>0$, a nonzero potential
normalization $a_\varepsilon$, and an additive reference $c_\varepsilon$.
For a compact set $K$ with
$x_0+r_\varepsilon K$ inside the nonsingular domain, put

```math
\Phi_\varepsilon(X)
=
\frac{V_\varepsilon(x_0+r_\varepsilon X)-c_\varepsilon}
     {a_\varepsilon}.
```

The exact chain rule is

```math
\nabla_X\Phi_\varepsilon
=\frac{r_\varepsilon}{a_\varepsilon}\nabla_xV_\varepsilon,
\qquad
D_X^2\Phi_\varepsilon
=\frac{r_\varepsilon^2}{a_\varepsilon}D_x^2V_\varepsilon.
```

Criticality and Hessian nonsingularity therefore correspond. A positive
$a_\varepsilon$ preserves Morse index. A negative normalization reverses all
Hessian signs, sending index $j$ to $d-j$.

### BSC-ECP-01: quantitative local Morse transfer

Assume $\Phi_\varepsilon\to\Phi_0$ in $C^2(K)$. Let
$p_1,\ldots,p_m$ be nondegenerate critical points of $\Phi_0$ in the interior
of $K$. For each $i$, choose a bounded open convex domain $\Omega_i$ such
that

```math
p_i\in\Omega_i,
\qquad
\overline{\Omega_i}\subset\mathrm{int}\,K,
```

the closures are pairwise disjoint, and $p_i$ is the only zero of
$\nabla\Phi_0$ on $\overline{\Omega_i}$. Define

```math
H_i=D^2\Phi_0(p_i),
\qquad
\mu_i=\sigma_{\min}(H_i)>0,
```

```math
\omega_i=
\sup_{X\in\Omega_i}\|D^2\Phi_0(X)-H_i\|,
\qquad
b_i=
\inf_{X\in\partial\Omega_i}\|\nabla\Phi_0(X)\|,
```

and, for the selected $\varepsilon$,

```math
d_1=\sup_K\|\nabla\Phi_\varepsilon-\nabla\Phi_0\|,
\qquad
d_2=\sup_K\|D^2\Phi_\varepsilon-D^2\Phi_0\|.
```

If

```math
d_1<\min_i b_i,
\qquad
\omega_i+d_2<\mu_i
\quad\text{for every }i,
```

then each $\Omega_i$ contains one and only one critical point of
$\Phi_\varepsilon$. It is nondegenerate, has the same scaled Morse index as
$p_i$, and converges to $p_i$. The corresponding point of $V_\varepsilon$ is
$x_0+r_\varepsilon p_i(\varepsilon)$, with its physical index determined by
the sign of $a_\varepsilon$.

To prove existence, join the two gradients by a straight homotopy. The
boundary margin prevents a zero on $\partial\Omega_i$, so degree is retained:

```math
\deg(\nabla\Phi_\varepsilon,\Omega_i,0)
=
\deg(\nabla\Phi_0,\Omega_i,0)
=
\mathrm{sign}\det H_i.
```

For uniqueness, convexity permits the averaged Hessian identity

```math
\nabla\Phi_\varepsilon(X)-\nabla\Phi_\varepsilon(Y)
=A_{XY}(X-Y),
```

```math
A_{XY}
=\int_0^1D^2\Phi_\varepsilon(Y+t(X-Y))\,dt.
```

The norm bound
$\lVert A_{XY}-H_i\rVert\le\omega_i+d_2<\sigma_{\min}(H_i)$ makes $A_{XY}$
invertible, hence the gradient injective on $\Omega_i$. The same symmetric
matrix perturbation bound preserves Hessian inertia at the zero.

This theorem is local. If $\Phi_0$ has no other critical point in $K$, define

```math
\eta=
\inf_{K\setminus\bigcup_i\Omega_i}\|\nabla\Phi_0\|>0.
```

Only the additional inequality $d_1<\eta$ proves that the listed points are
the exact roster on $K$. A global count still needs an independent compact
containment and no-escape argument.

### Derivative requirement for a Morse-Bott split

Let $M$ be a compact boundaryless critical submanifold of a $C^3$ function
$f_0$, and suppose its normal Hessian is invertible. If on a fixed tube

```math
f_\varepsilon=f_0+\varepsilon g+O_{C^3}(\varepsilon^2)
```

and $g|_M$ is Morse, the normal implicit-function problem reduces the nearby
critical set to a function on $M$. The reduced remainder is controlled in
$C^2$, so there is exactly one nearby nondegenerate point for each critical
point of $g|_M$ and no others in a smaller tube. Its index is the negative
eigenvalue count of the normal Hessian of $f_0$ plus the index of $g|_M$.
The $C^3$ hypothesis is kept explicit; coefficient matching or $C^0$
convergence cannot replace it.

Nondegenerate critical points on fixed compact neighborhoods away from the
blow-up center persist under $C^2$ convergence. Disjoint such neighborhoods
may be added to a shrinking local roster, but only after their separation
from the singular set and from one another is recorded.

## 2. Positive sources and generic finiteness

For distinct sites $a_1,\ldots,a_n\in\mathbb R^d$ and positive strengths,
consider

```math
V_q(x)=\sum_{i=1}^n\frac{q_i}{\|x-a_i\|},
\qquad q_i>0.
```

At a critical point,

```math
x=\frac{\sum_iw_i a_i}{\sum_iw_i},
\qquad
w_i=\frac{q_i}{\|x-a_i\|^3}>0,
```

so every critical point lies in the convex hull of the sites. Because the
sites are singular, that observation alone is not compactness.

Fix a small strength neighborhood with bounds $q_i^-\le q_i\le q_i^+$.
Inside a ball of radius $r$ about $a_i$, the field from source $i$ is at least
$q_i^-/r^2$, whereas all other fields are at most

```math
\sum_{j\ne i}
\frac{q_j^+}{(\|a_i-a_j\|-r)^2}.
```

For sufficiently small positive $r$, the first quantity is larger. These
uniform exclusion balls leave one compact subset of the nonsingular domain
containing every critical point for all strengths in the neighborhood.

### BSC-ECP-02: generic finite Morse completion

If the distinct sites affinely span $\mathbb R^d$, arbitrarily small positive
strength perturbations make $V_q$ Morse. Any already certified finite roster
of nondegenerate critical points can be retained, and the completed potential
has finitely many critical points.

Indeed, define

```math
F(q,x)=-\nabla_xV_q(x).
```

Its strength-derivative columns are positive scalar multiples of
$(x-a_i)/\lVert x-a_i\rVert^3$. A covector annihilating all columns would place every
$a_i$ in a common affine hyperplane through $x$, contradicting affine
spanning. Thus $F$ is a submersion. Parametric transversality supplies a
dense residual, locally full-measure set of strengths for which zero is a
regular value of $F(q,\cdot)$. Persistence protects the certified roster.
Regular zeros are discrete, and the uniform compact containment above turns
that discrete set into a finite one.

This is an existential genericity statement. It gives no named perturbation,
radius, success probability, or physical sampling law.

## 3. Four unequal positive charges with at least nine points

Put unit triangle charges at

```math
a_1=(1,0,0),
\quad
a_2=(-1/2,\sqrt3/2,0),
\quad
a_3=(-1/2,-\sqrt3/2,0).
```

With $\rho^2=x^2+y^2$ and $R^2=\rho^2+z^2$, their potential has expansion

```math
V_\triangle
=3+\frac34H_2+\frac{15}{8}H_3+\frac9{64}H_4+O(R^5),
```

where

```math
H_2=\rho^2-2z^2,
\qquad
H_3=x^3-3xy^2=\rho^3\cos(3\theta),
```

```math
H_4=3\rho^4-24\rho^2z^2+8z^4.
```

The exact triangle projections $u_j=(x,y)\cdot(a_j)_{xy}$ satisfy

```math
\sum_ju_j=0,
\quad
\sum_ju_j^2=\frac32\rho^2,
\quad
\sum_ju_j^3=\frac34(x^3-3xy^2),
\quad
\sum_ju_j^4=\frac98\rho^4.
```

Add a fourth site and strength

```math
a_4=(0,0,\varepsilon),
\qquad
q_4=c\varepsilon^3,
\qquad
c>\frac49.
```

On compact sets avoiding $e_3=(0,0,1)$, use $x=\varepsilon X$ and

```math
\Phi_\varepsilon(X)
=
\frac{V_\varepsilon(\varepsilon X)-V_\varepsilon(0)}
     {\varepsilon^2}.
```

Then

```math
\Phi_\varepsilon
=\Phi_0+\varepsilon G+O_{C^3}(\varepsilon^2),
```

```math
\Phi_0(\rho,z)
=\frac34(\rho^2-2z^2)
+c\left(\frac1{\sqrt{\rho^2+(z-1)^2}}-1\right),
```

```math
G(\rho,\theta)=\frac{15}{8}\rho^3\cos(3\theta).
```

Writing $d^2=\rho^2+(z-1)^2$, a nonaxial critical point satisfies

```math
z_0=\frac13,
\qquad
d_0=\left(\frac{2c}{3}\right)^{1/3},
\qquad
\rho_0^2=d_0^2-\frac49.
```

The strict threshold is necessary. On the nonsingular axis segment the only
possible equation in $0\le z<1$ is $c=3z(1-z)^2$, and

```math
\frac49-3z(1-z)^2
=\frac{(3z-1)^2(4-3z)}9.
```

At $c=4/9$ the radius collapses to zero and the limit is degenerate. For
$c>4/9$ there is no axial zero and the complete limit critical set is the
circle $(\rho,z)=(\rho_0,1/3)$.

Its Hessian in the two normal directions is

```math
A=
\begin{pmatrix}
\dfrac92\dfrac{\rho_0^2}{d_0^2}
&-\dfrac{3\rho_0}{d_0^2}\\
-\dfrac{3\rho_0}{d_0^2}
&-\dfrac92+\dfrac2{d_0^2}
\end{pmatrix},
```

```math
\det A=-\frac{81}{4}\frac{\rho_0^2}{d_0^2}<0.
```

There is one positive and one negative normal direction. The restriction
$G|_C=(15/8)\rho_0^3\cos(3\theta)$ has exactly six nondegenerate critical
points. The $C^3$ Morse-Bott transfer therefore gives three index-1 and three
index-2 points in the shrinking cluster.

Three more points come from the triangle at fixed scale. Let $\tau$ be the
unique root in $(69/100,7/10)$ of

```math
h(t)=t^6+t^3-3t^2+1,
```

and set

```math
\xi=\frac{\tau^3-1}{\tau^3+2}.
```

The endpoint values have opposite signs, while
$h'(t)=3t(2t^4+t-2)<0$ throughout the interval. Hence the root is isolated.
At $(\xi,0,0)$ the triangle Hessian is diagonal. Its $z$ eigenvalue is
negative, and its $x$ eigenvalue has the sign of

```math
4\tau^5-3\tau^3+5\tau^2-3,
```

which is negative on the isolating interval. Harmonicity makes the remaining
eigenvalue positive. This point and its two $2\pi/3$ rotations are
nondegenerate index-2 points. The apex field is $O(\varepsilon^3)$ in $C^2$
on their fixed, disjoint neighborhoods, so all three persist.

### BSC-ECP-03: four-charge lower bound

For every fixed $c>4/9$ and all sufficiently small positive $\varepsilon$,
the declared four-source family has at least nine nondegenerate critical
points: six local and three remote. The sites affinely span $\mathbb R^3$.
An arbitrarily small positive strength perturbation can therefore be chosen
outside every equality hyperplane and in the generic set of BSC-ECP-02. The
result is four pairwise-unequal positive charges with a finite globally Morse
critical set retaining at least nine points.

This is **not exactly nine**, not a four-charge maximum, and not a novelty or
priority conclusion. No explicit numerical value of $\varepsilon$ is
certified here.

## 4. Five-charge reconstruction

Retain the triangle and add equal axial charges at
$a_{4,5}=(0,0,\pm\varepsilon)$ with

```math
q_\varepsilon
=\frac34\varepsilon^3-\frac5{32}\varepsilon^5.
```

Scale by $x=\varepsilon^2X$ and normalize by $\varepsilon^6$:

```math
\Phi_\varepsilon(X)
=
\frac{V_\varepsilon(\varepsilon^2X)-V_\varepsilon(0)}
     {\varepsilon^6}.
```

The pair's quadratic term cancels the triangle's quadratic term in the same
units. On every fixed compact set away from the rescaled axial sites,

```math
\Phi_\varepsilon
=\Phi_0+O_{C^k}(\varepsilon^2)
\quad\text{for each fixed }k,
```

with

```math
\Phi_0=\frac5{32}H_2+\frac{15}{8}H_3+\frac3{16}H_4.
```

In cylindrical coordinates the polynomial is

```math
32\Phi_0
=18r^4+60r^3\cos(3\theta)-144r^2z^2
+5r^2+48z^4-10z^2.
```

Its complete critical roster follows from the factored derivatives:

| Case | Coordinates | Count | Hessian signs |
|---|---|---:|---|
| axial center | $r=0$, $z=0$ | 1 | $(++-)$ |
| axial pair | $r=0$, $z=\pm\sqrt{15}/12$ | 2 | $(+--)$ |
| planar | $z=0$, $\cos(3\theta)=-1$, $r=(15\pm\sqrt{205})/12$ | 6 | outer $(++-)$; inner $(+--)$ |
| off-plane outer | $r=1/3$, $z=\pm\sqrt{39}/12$, $\cos(3\theta)=1$ | 6 | $(+--)$ |
| off-plane inner | $r=1/6$, $z=\pm\sqrt{21}/12$, $\cos(3\theta)=1$ | 6 | $(++-)$ |

For $r>0$, the angular derivative forces $\sin(3\theta)=0$. When $z=0$,
only $\cos(3\theta)=-1$ gives positive roots, from

```math
36r^2-90r+5=0.
```

When $z\ne0$, the vertical equation gives

```math
z^2=\frac{72r^2+5}{48},
```

and the radial equation reduces to

```math
18r^2-9\cos(3\theta)r+1=0.
```

Positive roots occur only for $\cos(3\theta)=1$, namely $r=1/6$ and
$r=1/3$. These mutually exclusive factors prove completeness rather than
merely list numerical roots. Exact Hessian signs give ten index-1 and eleven
index-2 points, all nondegenerate.

### BSC-ECP-04: five-charge lower bound

For every sufficiently small positive $\varepsilon$, the declared symmetric
five-charge potential has at least 24 nondegenerate critical points: the 21
lifted polynomial points and the three persistent remote triangle points.
A sufficiently small positive generic strength perturbation gives a finite
Morse potential retaining them.

The source theorem is `source_asserted` by arXiv:2607.27197v1. The proof and
regressions retained here are an `independent_reconstruction`, not a replay
of the absent historical computation. The conclusion is at least 24, not
exactly 24. At $\varepsilon=1/6$ the displayed strength is exactly

```math
q_\varepsilon=\frac{859}{248832},
```

but that identity does not certify the roots at that finite parameter.

## 5. Pair insertion and the derivative gate

Let a positive-source potential be analytic on a source-free ball of radius
$r_*$ about the origin, invariant under $D_3\times\mathbb Z_2$, and have the
derivative-controlled jet

```math
U(x)=U(0)+\alpha H_2(x)+\beta H_3(x)+O(\|x\|^4),
\qquad
\alpha,\beta>0.
```

Writing the remainder as $R_4$, derivative control means
$D^jR_4(x)=O(\lVert x\rVert^{4-j})$ for $0\le j\le2$. When this jet is used inside a
Morse-Bott reduction, the corresponding $C^3$ remainder control is required.

Choose $\gamma>0$ and

```math
0<\eta<\min\{r_*,\sqrt{\alpha/\gamma}\},
```

avoiding every old source radius. Add equal positive charges

```math
q_\eta=\alpha\eta^3-\gamma\eta^5
```

at $\pm\eta e_3$, and scale $x=\lambda\eta^2X$. After subtracting the
central value and dividing by $\eta^6$, the normalized potential converges in
$C^2$ to

```math
\gamma\lambda^2H_2
+\beta\lambda^3H_3
+\frac{\alpha}{4}\lambda^4H_4.
```

The calculation uses the exact even pair expansion

```math
\frac1{\|e_3-tX\|}+\frac1{\|e_3+tX\|}-2
=-t^2H_2(X)+\frac{t^4}{4}H_4(X)+O_{C^2}(t^6).
```

Thus the order $\eta^4$ pair term cancels the base $H_2$ term; symmetry alone
does not establish the cancellation. The choices

```math
\lambda=\frac{2\beta}{5\alpha},
\qquad
\gamma=\frac{\beta^2}{30\alpha}
```

make the resulting coefficient triple a positive scalar multiple of the
21-point polynomial's coefficient triple. Equivalently, the limit is a
positive multiple of that polynomial. The new central quadratic and cubic
coefficients are

```math
\alpha_{\mathrm{new}}=\gamma\eta^2>0,
\qquad
\beta_{\mathrm{new}}=\beta>0.
```

At each stage choose the next scale only after the existing sources and
disjoint certified neighborhoods are fixed. The origin remains one of the 21
local points, so each inserted pair adds 20 new points while the old remote
roster persists: on every fixed old neighborhood away from the origin and the
new sites, the inserted pair is $O_{C^2}(\eta^3)$. For the triangle, symmetry
makes the origin critical and its Hessian is
$\mathrm{diag}(3/2,3/2,-3)$; together with the three remote points, this
supplies the four-point induction base. Thus

```math
3+2m\ \text{positive sources with at least }4+20m
\ \text{nondegenerate critical points}.
```

For $m\ge1$, affine spanning permits the final generic finite Morse completion
of BSC-ECP-02. This generic cleanup is applied only after all symmetric pair
insertions and persistence choices have been completed.

### BSC-ECP-05: jet-engineering gate

A source jet supports this transfer only when the record contains all of:

1. an explicit same-unit source-to-jet map;
2. a nonzero normalization and its sign;
3. $C^2$ control for isolated Morse points and $C^3$ control for the
   Morse-Bott reduction;
4. an exact limit roster or certified isolating neighborhoods;
5. disjoint remote neighborhoods when lower bounds are added; and
6. compact containment plus source exclusion for global finiteness.

Plots, floating-point roots, symmetry, formal coefficients, or an unavailable
CAS run do not activate this gate.

## 6. Claim boundary

| Claim | Retained result | Demotion trigger |
|---|---|---|
| BSC-ECP-01 | Quantitative $C^2$ local transfer; exact compact roster only with the exterior gradient gap. | Missing convex degree domains, margins, normalization sign, or global no-escape evidence. |
| BSC-ECP-02 | Existential positive finite Morse completion at affinely spanning sites. | Treating genericity as an explicit perturbation, radius, or probability. |
| BSC-ECP-03 | Four pairwise-unequal positive charges with a finite Morse set containing at least nine points. | Replacing $c>4/9$ by equality, dropping $C^3$, or asserting exactly nine, a maximum, novelty, or priority. |
| BSC-ECP-04 | The audited five-charge family has at least 24 points for sufficiently small $\varepsilon$. | Certifying $\varepsilon=1/6$, asserting exactly 24, or calling absent scripts replayed. |
| BSC-ECP-05 | Explicit pair insertion yields the conditional $3+2m$ / $4+20m$ lower bound under the full derivative and separation gate. | Using coefficient matching without derivative control, completeness, persistence, or compactness. |

These are mathematical point-source results. They supply neither experimental
evidence nor a bridge to finite-size electrostatic bodies, electromagnetic
devices, or F12 derived holonomy.
