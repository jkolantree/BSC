# Normalized scale profiles and analytic transfer

## Status and scope

This development module records reusable mathematics for Boundary-State
Calculus (BSC). It is part of the unreleased `1.1.0-dev` framework and is not
an empirical claim, an execution receipt, or a new field in the eight-field
BSC morphism record. It is not a new morphism field.

The motivating example is the engineered zeta-DQPT construction, but the
definitions below are independent of zeta functions, quantum mechanics, and
phase-transition terminology. The authoritative numbered proofs are also
integrated into the manuscript's scale and quotient sections.

## 1. Certified families and normalized scale profiles

A BSC **certified scale family** is a directed comparison family of existing
finite systems rather than a new morphism variant. Its record declares

$$
\mathfrak A=
\left(
I,P,\{\lambda_i,\mathsf S_i,\mathsf{Cert}_i,
\mathfrak M_{ij},A_i,Z_i,L_i,\mathsf O_i\}
\right).
$$

Here $I$ is a directed scale index, $P$ is one common topological parameter
space, $\lambda_i\to\infty$ is a dimensionless logarithmic size gauge,
$(\mathsf S_i,\mathsf{Cert}_i)$ is a certified finite BSC system,
$\mathfrak M_{ij}$ is an interscale comparison or a declared comparison
defect, $A_i$ is the ideal carrier, $Z_i$ is a nonzero normalizer,
$L_i=A_i/Z_i$ is the ideal normalized observable, and
$\mathsf O_i$ is the observation or estimator law. The ideal scalar and its
estimator distribution are different typed objects. No categorical identity
or composition law is inferred from this record; a strict directed diagram
requires those coherences as additional hypotheses.

Such a comparison family does not by itself construct an infinite-system state,
quasilocal algebra, limiting dynamics, or physical thermodynamic phase. Those
require a separately declared limit object and compatibility theorem.

For a sequence specialization, set $X=P$. Let $\lambda_N>0$ satisfy
$\lambda_N\to\infty$. A **normalized scale profile** consists of functions

$$
A_N:X\to\mathbb C,\qquad
Z_N:X\to\mathbb C\setminus\{0\},\qquad
L_N=\frac{A_N}{Z_N},
$$

together with a declared limiting carrier $A$, uniformity domain, error norm,
and order of limits. Every logarithm acts on a dimensionless quantity, or on a
quantity divided by a declared nonzero reference value. Here $A_N$ is the
carrier, $Z_N$ is the normalizer, and $L_N$ is the reported normalized
observable. A physical normalization is often positive, but nonvanishing is
the mathematical condition needed below.

The logarithmic quantities, whenever the displayed expressions are finite,
are

$$
\gamma_N(x)=\frac{\log|Z_N(x)|}{\lambda_N},\qquad
\kappa_N(x)=-\frac{\log|A_N(x)|}{\lambda_N},\qquad
\mathcal R_N(x)=-\frac{\log|L_N(x)|}{\lambda_N}.
$$

If an exact finite zero is permitted, the extended convention
$-\log0=+\infty$ must be declared rather than silently treating the rate as a
finite number.

### Proposition BSC-SCL-05a (normalization collapse)

For fixed $x\in X$, if $A_N(x)\to A(x)\in\mathbb C$ and
$|Z_N(x)|\to\infty$, then $L_N(x)\to0$. More generally, for $K\subseteq X$,
if $0<\inf_{x\in K}|Z_N(x)|$ for all sufficiently large $N$ and

$$
\frac{\sup_{x\in K}|A_N(x)|}
     {\inf_{x\in K}|Z_N(x)|}\longrightarrow0,
$$

then $\sup_K|L_N|\to0$. At every finite $N$,

$$
\{x:L_N(x)=0\}=\{x:A_N(x)=0\}.
$$

#### Proof

The pointwise claim follows from
$|L_N(x)|=|A_N(x)|/|Z_N(x)|$. Taking the supremum of the numerator and the
infimum of the denominator proves the uniform claim. Nonvanishing of $Z_N$
gives the finite zero-set identity.

Thus a normalized limit may vanish everywhere even though no finite carrier
does. For example, $A_N=1$ and $Z_N=N$ give $L_N\to0$ without any carrier
zero. Divergence of the normalizer is not sufficient by itself: $A_N=N$ and
$Z_N=N$ give $L_N=1$. A normalization-collapse claim therefore requires
numerator control.

### Theorem BSC-SCL-05b (additive scaling signature)

Fix $x\in X$ and suppose $A_N(x)$ and $Z_N(x)$ are eventually nonzero. If

$$
\gamma(x)=\lim_{N\to\infty}\gamma_N(x),\qquad
\kappa(x)=\lim_{N\to\infty}\kappa_N(x)
$$

exist as finite real numbers, then

$$
\lim_{N\to\infty}\mathcal R_N(x)=\gamma(x)+\kappa(x).
$$

If $A_N(x)\to A(x)\ne0$, then $\kappa(x)=0$. If instead

$$
A_N(x)=c(x)e^{-\rho(x)\lambda_N+o(\lambda_N)},
\qquad c(x)\ne0,\quad \rho(x)\in\mathbb R,
$$

then $\kappa(x)=\rho(x)$.

#### Proof

The exact finite identity

$$
-\log|L_N|=\log|Z_N|-\log|A_N|
$$

gives $\mathcal R_N=\gamma_N+\kappa_N$. Taking the declared limits proves the
first statement. If $A_N\to A\ne0$, then $\log|A_N|=O(1)$, so its quotient by
$\lambda_N\to\infty$ vanishes. The final assertion follows by taking
logarithms of the stated asymptotic.

The hypotheses cannot be dropped. If
$A_N=N^{-1}$ for even $N$ and $A_N=N^{-2}$ for odd $N$, with
$\lambda_N=\log N$, the carrier exponent does not converge. If
$A_N(x)=x+1/\log N$, then the limiting carrier has a zero at $x=0$ but the
extra logarithmic decay exponent there is zero, so the zero creates no
positive rate jump.

### Proposition BSC-SCL-05c (normalization covariance)

Let $\widetilde L_N=c_NL_N$ with $c_N(x)\ne0$, and suppose the finite limits

$$
\mathcal R(x)=\lim_{N\to\infty}\mathcal R_N(x),\qquad
\widetilde{\mathcal R}(x)
=\lim_{N\to\infty}\widetilde{\mathcal R}_N(x),
$$

and

$$
\chi(x)=\lim_{N\to\infty}
\frac{\log|c_N(x)|}{\lambda_N}
$$

exist as finite values on a topological domain. Then

$$
\widetilde{\mathcal R}(x)=\mathcal R(x)-\chi(x).
$$

If $\chi$ is continuous, the two limiting rates have the same discontinuity
set. If $\chi=0$, as for a subexponential change relative to $\lambda_N$, the
rate values themselves agree.

#### Proof

The finite identity

$$
-\frac{\log|\widetilde L_N|}{\lambda_N}
=
-\frac{\log|L_N|}{\lambda_N}
-\frac{\log|c_N|}{\lambda_N}
$$

gives the limit formula. Adding or subtracting a continuous finite function
does not change the discontinuity set.

Thus a nonzero prefactor preserves finite zero sets, but only its scaled
logarithm determines whether rate values or merely singular locations are
preserved.

### Proposition BSC-SCL-08 (rate stability away from zero)

Let $L_N,\widehat L_N\ne0$ be dimensionless amplitudes at a fixed parameter
point. If

$$
|L_N|\ge m_N>0,\qquad
|\widehat L_N-L_N|\le\varepsilon_N<m_N,
$$

and $\delta_N=\varepsilon_N/m_N$, then

$$
\left|
-\frac{\log|\widehat L_N|}{\lambda_N}
+\frac{\log|L_N|}{\lambda_N}
\right|
\le
\frac{-\log(1-\delta_N)}{\lambda_N}.
$$

#### Proof

The triangle inequalities give

$$
1-\delta_N
\le\frac{|\widehat L_N|}{|L_N|}
\le1+\delta_N.
$$

Taking logarithms and using
$\log(1+\delta)\le-\log(1-\delta)$ for $0\le\delta<1$ proves the result.

There is no uniform Lipschitz rate bound as $m_N\downarrow0$. Small amplitude
error can become large logarithmic-rate error near a zero. Rate transport
therefore needs a lower margin, a contour certificate, or a root-localization
argument rather than an unqualified amplitude tolerance.

## 2. Exceptional sets and rate singularities

### Theorem BSC-SCL-06 (rate-discontinuity support)

Let $X$ be a metric space, let $\Sigma\subseteq X$ be closed, and let
$\gamma,\rho:X\to\mathbb R$ be continuous with
$\rho(x)>0$ for every $x\in\partial\Sigma$. Define

$$
\mathcal R(x)=\gamma(x)+\rho(x)\mathbf1_\Sigma(x).
$$

Then

$$
\operatorname{Disc}(\mathcal R)=\partial\Sigma.
$$

If $\Sigma$ has empty interior, then
$\operatorname{Disc}(\mathcal R)=\Sigma$. In particular, when $X$ is a
domain in $\mathbb C$, this conclusion applies when $\Sigma$ is the zero set
of a holomorphic function that is not identically zero on any connected
component.

#### Proof

Off $\partial\Sigma$, the indicator $\mathbf1_\Sigma$ is locally constant, so
$\mathcal R$ is continuous. At a boundary point, sequences from $\Sigma$ and
its complement approach the point. Continuity of $\gamma$ and $\rho$, with a
strictly positive boundary value of $\rho$, gives two limiting values
separated by $\rho(x)$. Hence every boundary point is a discontinuity. A
closed set with empty interior equals its boundary. On a one-complex-variable
domain, the zero set of a non-identically-zero holomorphic function is locally
discrete and therefore has empty interior.

The empty-interior condition matters. For $\Sigma=[-1,1]\subset\mathbb R$,
$\mathbf1_\Sigma$ is discontinuous only at $-1$ and $1$, not at every point
of $\Sigma$. Continuity of the background also matters: a singularity already
present in $\gamma$ need not encode $\Sigma$.

### Proposition BSC-QUO-03a (decision descent through a scalar)

Let $R:X\to Y$ and $q_\Sigma=\mathbf1_\Sigma:X\to\{0,1\}$ be measurable. The
membership query descends through $R$ by a measurable decision
$d:Y\to\{0,1\}$ exactly when there is a measurable $B\subseteq Y$ such that

$$
\Sigma=R^{-1}(B).
$$

In particular, if $R(x)=R(x')$ for points on opposite sides of $\Sigma$, no
exact decision can descend through $R$.

#### Proof

If $q_\Sigma=d\circ R$, take $B=d^{-1}(\{1\})$. Conversely, if
$\Sigma=R^{-1}(B)$, the indicator $d=\mathbf1_B$ gives the factorization.

A rate-discontinuity theorem alone does not guarantee this factorization.
For example, with $X=[-2,2]$, $\Sigma=\{0\}$,
$\gamma(x)=x^2$, and $\rho=1$, the exceptional rate at $0$ equals the
background rate at $x=\pm1$. A BSC rate profile must therefore record both
its singular set and the decision query it is claimed to support.

### Proposition BSC-SCL-06b (parameter-slice visibility)

Let $\iota:Q\to X$ be continuous. For every
$\mathcal R:X\to\mathbb R$,

$$
\operatorname{Disc}(\mathcal R\circ\iota)
\subseteq
\iota^{-1}\!\left(\operatorname{Disc}(\mathcal R)\right).
$$

Equality requires an additional visibility hypothesis: every branch
responsible for the ambient discontinuity must be approached through the
image of $\iota$ near the point in question.

#### Proof

If $\mathcal R$ is continuous at $\iota(q)$, continuity of $\iota$ makes
$\mathcal R\circ\iota$ continuous at $q$. This proves the inclusion. Equality
can fail when the slice is locally constant or remains in only one continuity
branch.

Therefore a singular set in a full parameter space does not automatically
become a dynamical phase-transition locus along a physical real-time path.
The path and its visibility condition are part of the mathematical claim.

## 3. Certified analytic finite-to-limit transfer

### Theorem BSC-SCL-07a (bounded holomorphic zero-count transfer)

Let $\Omega$ be a bounded Jordan domain with closure in an open set
$D\subseteq\mathbb C$. Let $A$ and $A_N$ be holomorphic on a neighborhood of
$\overline\Omega$. Suppose certified bounds satisfy

$$
\sup_{z\in\partial\Omega}|A_N(z)-A(z)|
\le\varepsilon_N
<m_\Omega
\le\inf_{z\in\partial\Omega}|A(z)|.
$$

Then $A_N$ and $A$ have the same number of zeros in $\Omega$, counted with
multiplicity.

#### Proof

On $\partial\Omega$,
$|A_N-A|<|A|$. Rouche's theorem gives the same enclosed zero count.

Pointwise convergence is insufficient, and the contour margin must be strict.
For the unit disk,

$$
A(z)=z-1,\qquad
A_N(z)=z-\left(1+\frac{(-1)^N}{N}\right),
$$

the carriers converge uniformly, but their zeros alternate inside and outside
because the limiting zero lies on the boundary.

### Theorem BSC-SCL-07b (local multiplicity transfer)

Let $A$ be holomorphic near $z_0$ and have a zero there of multiplicity $m$:

$$
A(z)=a_m(z-z_0)^m+O(|z-z_0|^{m+1}),\qquad a_m\ne0.
$$

Let $A_N$ be holomorphic on the same neighborhood, and let $r_N\downarrow0$.
If

$$
\frac{\sup_{|z-z_0|=r_N}|A_N(z)-A(z)|}
     {|a_m|r_N^m}
\longrightarrow q<1,
$$

then, for all sufficiently large $N$, $A_N$ has exactly $m$ zeros in
$|z-z_0|<r_N$, counted with multiplicity.

#### Proof

Uniformly on the shrinking circle,
$|A(z)|=|a_m|r_N^m(1+o(1))$. The displayed hypothesis therefore gives
$|A_N-A|<|A|$ on that circle for all sufficiently large $N$. Rouche's
theorem transfers the multiplicity count.

This theorem gives a count inside a declared disk. It does not provide a
canonical pairing of roots, an exact location, or control outside the disk.
When a normalizer depends nonholomorphically on the complex parameter, the
theorem applies to the holomorphic carrier $A_N$, not to the normalized
observable $L_N$. Analytic truncation, implementation, and measurement errors
must be enclosed in the same boundary norm before comparison with
$m_\Omega$.

## 4. Stochastic observations and exact decisions

### Theorem BSC-QUO-03b (finite-label exact decoding)

Let $Q$ be finite with its discrete sigma-algebra, let $q:X\to Q$ be
measurable, and let
$O:X\rightsquigarrow Y$ be an observation kernel on a standard Borel output
space. A measurable decoder $d:Y\to Q$ is exact when

$$
O\bigl(x,d^{-1}(\{q(x)\})\bigr)=1
\quad\text{for every }x\in X.
$$

Such a decoder exists exactly when there is a measurable partition
$(B_a)_{a\in Q}$ of $Y$ satisfying

$$
O(x,B_{q(x)})=1
\quad\text{for every }x\in X.
$$

Consequently, output laws belonging to inputs with different labels must be
mutually singular. For two inputs $x_0,x_1$ with different labels and equal
prior probability, every decoder has average error at least

$$
\frac{1-d_{\mathrm{TV}}(O(x_0,\cdot),O(x_1,\cdot))}{2},
\qquad
d_{\mathrm{TV}}(P,Q)=\sup_B|P(B)-Q(B)|.
$$

#### Proof

The fibers $B_a=d^{-1}(\{a\})$ of an exact decoder form the required
partition. Conversely, the declared partition defines the decoder. Different
labels concentrate their laws on disjoint partition cells and are therefore
mutually singular. For the binary statement, a decision region $B$ has equal
prior error

$$
\frac12\bigl(P(B^c)+Q(B)\bigr)
=\frac12\bigl(1-(P(B)-Q(B))\bigr).
$$

Optimizing over $B$, and allowing the labels to be interchanged, gives the
total-variation formula.

Thus identical output laws make exact classification impossible, while close
laws require a quantitative testing bound. The worst-case error is also at
least the displayed equal-prior average-error bound. A deterministic
finite-resolution cell is the special case in which the kernel is a Dirac
observation. Repeated observations require replacing the one-shot laws by the
declared product or dependent joint laws and recording the sample count.

## 5. Mathematical singularity versus physical DQPT

A **DQPT interpretation certificate** for a normalized scale profile must
declare:

1. the finite-system Hamiltonian or dynamical family;
2. preparation, quench, and control protocols;
3. the physical size or volume normalization;
4. amplitude versus squared-echo convention;
5. the real-time parameter slice;
6. convergence topology and order of limits;
7. the singularity class being claimed - discontinuity, nondifferentiability,
   failure of real analyticity, or complex nonanalyticity;
8. perturbation and robustness regime;
9. estimator and instrument laws; and
10. the implementation evidence.

A mathematical rate discontinuity discharges only the corresponding
mathematical item. It does not construct the physical infinite-system limit or
inherit the remaining certificate fields.

## 6. Zeta-DQPT as an instance

For the engineered alternating-sum construction, take

$$
\lambda_N=\log N,\qquad
A_N(s)=-S_N(s),\qquad
Z_N(s)=Z_N(\operatorname{Re}s),\qquad
L_N(s)=\mathcal L_N(s).
$$

On the open critical strip, the application proves

$$
\gamma(s)=1-\operatorname{Re}s,\qquad
\kappa(s)=
\begin{cases}
0,&\eta(s)\ne0,\\
\operatorname{Re}s,&\eta(s)=0.
\end{cases}
$$

Hence the general rate is $1-\operatorname{Re}s$ off the eta-zero set and
$1$ on it. Under the source convention $N=2^d$, multiplication by $\log2$
gives the physical free-energy rate. The ideal limiting rate does support the
exact query through the Borel decision cell $\{1\}$, equivalently
$\{\log2\}$ after physical rescaling. A finite-resolution experiment does not
thereby obtain the exact limiting rate.

The application's alternating-tail bound instantiates BSC-SCL-07a, and its
shrinking-circle estimate instantiates BSC-SCL-07b with
$r_N=C N^{-\operatorname{Re}(s_0)/m}$. Those analytic statements concern the
holomorphic carrier $S_N$. They do not convert finite measured minima into
exact zeros or into an unrestricted Riemann Hypothesis decision.
