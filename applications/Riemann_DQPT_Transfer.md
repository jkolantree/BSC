# Riemann zeros and dynamical quantum phase transitions as a BSC scale instance

## Record status

- **BSC baseline:** [`b56495bc9c33dae73c28228708110450586b46e7`](https://github.com/jkolantree/BSC/tree/b56495bc9c33dae73c28228708110450586b46e7), version 1.0.1.
- **Integration state:** incorporated into version 1.1.0 together with the
  central manuscript, claim ledger, fixture index, and manifest, and published
  in the immutable
  [`v1.1.0` release](https://github.com/jkolantree/BSC/releases/tag/v1.1.0).
  The Zenodo concept DOI is `10.5281/zenodo.21541160`; Zenodo subsequently
  assigned v1.1.0 the version DOI `10.5281/zenodo.21710743`.
- **Version 1.2.0 interaction:** version 1.2.0 adds the
  [simulation-evidence profile](../framework/Simulation_Evidence_Profile.md).
  It does not change any Riemann, zeta–DQPT, physical-origin, temperature, or
  quantum-advantage verdict below.
- **Execution:** unexecuted. No experiment, simulation, interval computation,
  zero census, complexity replay, or independent reproduction was performed
  for this record.
- **Source boundary:** the primary
  [Nature Communications article](https://doi.org/10.1038/s41467-026-74935-8)
  and version-pinned
  [arXiv manuscript](https://arxiv.org/abs/2511.11199v1). News reports are not
  evidence inputs.

The result is the first substantial instance of BSC's reusable
[normalized-scale profile](../framework/Normalized_Scale_Profiles.md), not a
new axiom and not evidence that BSC or the experiment proves the Riemann
hypothesis (RH). The paper supplies an exact finite-dimensional identity and
proposes physical, limit, zero-identification, DQPT, and resource
interpretations. The framework separates the finite carrier, its
normalization, logarithmic rate, analytic zero transfer, parameter slice, and
observation law.

**Mathematical provenance.** The eta factorization, Abel summation, Euler
transformation of an alternating tail, harmonic-sum asymptotics, isolated
holomorphic zeros, and Rouché's theorem are classical imported ingredients.
The numbered BSC statements below are self-contained consequences assembled
for this framework: the explicit bounds, normalization diagnosis, pointwise
rate split, singular-set and slice corollaries, and local root-displacement
formula are derived here from those ingredients. No claim of historical
priority is made for these consequences.

In particular, the finite experiment does not prove the Riemann hypothesis.

The simulation-evidence profile can type a future replay more sharply:
high-zero numerical simulation needs a frozen estimator, oracle and error
model; ideal-to-NMR transfer needs pulse, noise, calibration, readout, clock,
and compatibility coordinates; an implementation-deficiency bound must
distinguish one tested channel from the optimized deficiency; and any
quantum-advantage claim needs a matched classical comparator identity. None of
those evidence objects is present here, so every existing execution and
promotion boundary remains unchanged.

## 1. What the primary paper establishes and reports

The source constructs two engineered quantum models:

1. an accumulated-phase/coherence model with a logarithmic Hamiltonian; and
2. a generalized Loschmidt-amplitude model based on a Riemann--Siegel
   approximation.

For the first model, one probe qubit reads a working system with energies
$\log n$. The published proof-of-principle experiment uses five nuclear
spins: one probe and four working qubits, hence a $16$-dimensional working
system. It was run on a $600$ MHz NMR spectrometer at 305 K. The paper
reports locations extracted by polynomial fitting where both measured
coherence components approached zero:
$$
14.12,\quad20.96,\quad25.09,\quad30.44,\quad32.93
$$
against reference values
$$
14.13,\quad21.02,\quad25.01,\quad30.43,\quad32.94.
$$
Those are results reported by one primary publication; they have not been
reproduced here. The paper also reports numerical, not hardware, simulations
near the $10^{12}$-th zero using an $18$-spin model.

The symbol called inverse temperature in the model is an encoded population
parameter, not the laboratory temperature. This record writes it as
$\beta_{\mathrm{eff}}$:
$$
  p_n(\beta_{\mathrm{eff}})
  =\frac{n^{-\beta_{\mathrm{eff}}}}{Z_N(\beta_{\mathrm{eff}})}.
$$
It is not $1/(k_B\,305\ {\rm K})$. The 305 K value describes the
laboratory carrier; $\beta_{\mathrm{eff}}$ describes the target population
profile prepared by control pulses. Equating the two would be a type and units
error.

## 2. Exact finite accumulated-phase identity

Let $N\in\mathbb N$, $\beta_{\mathrm{eff}}\in\mathbb R$,
$t\in\mathbb R$, and
$$
  s=\beta_{\mathrm{eff}}+it.
$$
On $\mathbb C^N$, define
$$
\begin{aligned}
  H_N&=\sum_{n=1}^{N}\log(n)\lvert n\rangle\langle n\rvert,\\
  Z_N(\beta_{\mathrm{eff}})
    &=\sum_{n=1}^{N}n^{-\beta_{\mathrm{eff}}},\\
  \rho_{\beta_{\mathrm{eff}},N}
    &=Z_N(\beta_{\mathrm{eff}})^{-1}
      \sum_{n=1}^{N}n^{-\beta_{\mathrm{eff}}}
      \lvert n\rangle\langle n\rvert,\\
  P_N&=\sum_{n=1}^{N}(-1)^n\lvert n\rangle\langle n\rvert,\\
  S_N(s)&=\eta_N(s)
    =\sum_{n=1}^{N}(-1)^{n-1}n^{-s}.
\end{aligned}
$$
The ideal finite accumulated-phase observable is
$$
  L_N(\beta_{\mathrm{eff}},t)
  =\operatorname{Tr}\!\left(
       \rho_{\beta_{\mathrm{eff}},N}e^{-itH_N}P_N
    \right).
$$

### Proposition BSC-ZDQ-01 (finite identity)

For every finite $N$, real $\beta_{\mathrm{eff}}$, and real $t$,
$$
  \boxed{\;
  L_N(\beta_{\mathrm{eff}},t)
  =-\frac{S_N(s)}{Z_N(\beta_{\mathrm{eff}})}
  \;},\qquad s=\beta_{\mathrm{eff}}+it.
$$

#### Proof

All three operators in the trace are diagonal in the declared basis.
Therefore
$$
\begin{aligned}
L_N(\beta_{\mathrm{eff}},t)
 &=\frac{1}{Z_N(\beta_{\mathrm{eff}})}
   \sum_{n=1}^{N}
   n^{-\beta_{\mathrm{eff}}}e^{-it\log n}(-1)^n\\
 &=\frac{1}{Z_N(\beta_{\mathrm{eff}})}
   \sum_{n=1}^{N}(-1)^n n^{-s}
 =-\frac{S_N(s)}{Z_N(\beta_{\mathrm{eff}})}.
\end{aligned}
$$
No thermodynamic limit, zero approximation, experiment, or RH assumption is
used. $\square$

Here $S_N=\eta_N$ is the truncated Dirichlet eta sum; the symbol $S_N$
will be used for the finite sum below. The sign is not cosmetic: it follows
from the source convention that the
phase on level $n$ is $(-1)^n$. A different pulse or basis convention must
be represented by an explicit observation postprocessor $K$, not silently
absorbed into the identity.

## 3. The analytic bridge: a tail bound and a zero-count certificate

For $\operatorname{Re}s>0$, let
$$
  \eta(s)=\sum_{n=1}^{\infty}(-1)^{n-1}n^{-s}.
$$
On the open critical strip $0<\operatorname{Re}s<1$,
$$
  \eta(s)=(1-2^{1-s})\zeta(s),
$$
and the prefactor has no zeros there. Thus $\eta$ and $\zeta$ have the
same zeros, with multiplicity, in that strip. Connecting a finite $S_N$ to
that zero set still requires a uniform error statement.

### Proposition BSC-ZDQ-02a (summation-by-parts tail bound)

If $s=\beta+it$ with $\beta>0$, then
$$
  \boxed{\;
  \left|\eta(s)-S_N(s)\right|
  \leq N^{-\beta}\left(1+\frac{|s|}{\beta}\right)
  \;}.
$$

#### Proof

Put $a_n=(-1)^{n-1}$ and
$A(x)=\sum_{n\leq x}a_n$, so $|A(x)|\leq1$.
Abel summation applied to the tail after $N$, with
$\frac{d}{dx}x^{-s}=-s x^{-s-1}$, bounds its endpoint term by
$N^{-\beta}$ and its integral term by
$$
  |s|\int_N^{\infty}x^{-\beta-1}\,dx
  =\frac{|s|}{\beta}N^{-\beta}.
$$
Adding the two bounds gives the result.
$\square$

Consequently, on a compact set $K\subset\{\operatorname{Re}s>0\}$, if
$$
  \beta_K=\min_{s\in K}\operatorname{Re}s>0,\qquad
  S_K=\max_{s\in K}|s|,
$$
then
$$
  \sup_{s\in K}|\eta(s)-S_N(s)|
  \leq N^{-\beta_K}
    \left(1+\frac{S_K}{\beta_K}\right).
$$

### Proposition BSC-ZDQ-02b (Rouché finite zero census)

Let $\Omega$ be a bounded Jordan domain whose closure lies in
$0<\operatorname{Re}s<1$. Assume $\eta$ has no zero on
$\partial\Omega$, and define
$$
\begin{aligned}
  m_\Omega&=\inf_{s\in\partial\Omega}|\eta(s)|>0,\\
  \beta_\Omega&=\min_{s\in\partial\Omega}\operatorname{Re}s>0,\\
  S_\Omega&=\max_{s\in\partial\Omega}|s|.
\end{aligned}
$$
If
$$
  N^{-\beta_\Omega}
  \left(1+\frac{S_\Omega}{\beta_\Omega}\right)<m_\Omega,
$$
then $S_N$, $\eta$, and $\zeta$ have the same number of zeros in
$\Omega$, counted with multiplicity.

#### Proof

Proposition BSC-ZDQ-02a gives
$$
  |\eta(s)-S_N(s)|<|\eta(s)|
  \quad\text{for every }s\in\partial\Omega.
$$
Rouché's theorem therefore gives equal zero counts for $S_N$ and
$\eta$ in $\Omega$. The factor $1-2^{1-s}$ is holomorphic and nonzero
on $\overline\Omega$, so $\eta$ and $\zeta$ have the same zeros there,
with multiplicity. $\square$

This is BSC-SCL-07a with an explicit application-specific boundary error and
margin.

This is a zero-count statement on a certified contour. It does **not** say
that evaluating $L_N$ at a known zeta zero produces an exact finite-$N$
zero, nor that a small value at one sampled point certifies a zero.

### The renormalization gate

The analytic object with a nontrivial limit is
$$
  Z_N(\beta_{\mathrm{eff}})
  L_N(\beta_{\mathrm{eff}},t)
  =-S_N(s)
  \longrightarrow
  (2^{1-s}-1)\zeta(s).
$$
The raw normalized coherence has a different limit. For fixed
$0<\beta_{\mathrm{eff}}\leq1$, $Z_N(\beta_{\mathrm{eff}})\to\infty$
while $S_N(s)\to\eta(s)$. Hence
$$
  L_N(\beta_{\mathrm{eff}},t)\longrightarrow0
$$
for every fixed $t$, whether or not $\zeta(s)=0$. Therefore
$$
  \lim_{N\to\infty}L_N(\beta_{\mathrm{eff}},t)=0
  \quad\Longleftrightarrow\quad
  \zeta(s)=0
$$
is false on the critical strip. A valid descendant claim must instead use a
renormalized amplitude, a finite-$N$ contour count with an error bound, or a
properly defined rate-function limit.

This is Proposition BSC-SCL-05a with carrier $A_N=-S_N$ and positive
normalizer $Z_N$. The normalization preserves every finite zero but collapses
the raw pointwise limit.

### Proposition BSC-ZDQ-02c (fixed-$s$ scaling discriminator)

Fix $s=\beta+it$ with $0<\beta<1$, write
$L_N(s)=L_N(\beta,t)$, and, for $N\geq2$ whenever $L_N(s)\ne0$, define
$$
  \alpha_N(s)=-\frac{\log|L_N(s)|}{\log N}.
$$
Then $L_N(s)$ is nonzero for all sufficiently large $N$, and
$$
  \lim_{N\to\infty}\alpha_N(s)
  =
  \begin{cases}
    1-\beta,& \eta(s)\ne0,\\
    1,& \eta(s)=0.
  \end{cases}
$$

#### Proof

Write $R_N(s)=\eta(s)-S_N(s)$, put $m=N+1$, set
$f_n=n^{-s}$, and use $\Delta f_n=f_n-f_{n+1}$. The one-step Euler
identity is
$$
  \sum_{k=0}^{\infty}(-1)^k f_{m+k}
  =\frac12 f_m
   +\frac12\sum_{k=0}^{\infty}(-1)^k\Delta f_{m+k}.
$$
Here $\Delta f_n=O_s(n^{-\beta-1})$ and
$\Delta^2f_n=O_s(n^{-\beta-2})$. Abel summation applied to the second
alternating series therefore bounds it by
$$
  O_s\!\left(
    |\Delta f_m|+\sum_{n=m}^{\infty}|\Delta^2f_n|
  \right)
  =O_s(m^{-\beta-1}).
$$
Restoring the sign of the first omitted term gives
$$
  R_N(s)
  =(-1)^N\left(
     \frac{1}{2}(N+1)^{-s}+O_s(N^{-\beta-1})
   \right).
$$
The same difference estimates are uniform on every fixed compact
$U\Subset\{\operatorname{Re}(s)>0\}$: writing the error as $E_N(s)$, there is
a $C_U$ such that
$$
  |E_N(s)|\leq C_U N^{-\operatorname{Re}(s)-1},
  \qquad s\in U.
$$
Integral comparison also gives
$$
  Z_N(\beta)=\frac{N^{1-\beta}}{1-\beta}+O_\beta(1).
$$
If $\eta(s)\ne0$, then $S_N(s)=\eta(s)+o(1)$ and therefore
$$
  L_N(s)=-(1-\beta)\eta(s)N^{\beta-1}(1+o(1)).
$$
If $\eta(s)=0$, then $S_N(s)=-R_N(s)$ and
$$
  L_N(s)
  =(-1)^N\frac{1-\beta}{2}N^{-1-it}(1+o(1)).
$$
Both leading coefficients are nonzero, so $L_N(s)$ is nonzero for all
sufficiently large $N$. Taking logarithms proves the two limits. $\square$

In the general scale-profile notation,
$$
  \lambda_N=\log N,\qquad
  \gamma(s)=1-\beta,\qquad
  \kappa(s)=
  \begin{cases}
    0,&\eta(s)\ne0,\\
    \beta,&\eta(s)=0.
  \end{cases}
$$
Thus BSC-SCL-05b identifies the reusable mechanism as an additive
normalization background plus an exceptional carrier-decay exponent.

Because $1-2^{1-s}$ is nonzero in the open critical strip, the second branch
is exactly the zeta-zero branch. This resolves the apparent paradox: raw
coherence decays throughout the strip, but its fixed-$s$ decay exponent
changes at a zero.

For the source's qubit scaling $N=2^d$, define the finite-size rate
$$
  \mathcal F_{1,N}(s)=-\frac{1}{d}\log|L_N(s)|
  =(\log 2)\alpha_N(s).
$$
The proposition therefore gives the pointwise fixed-$s$ limit
$$
  \mathcal F_1(s)
  =
  \begin{cases}
    (1-\beta)\log 2,&\eta(s)\ne0,\\
    \log 2,&\eta(s)=0.
  \end{cases}
$$
This supplies the precise mathematical bridge to the paper's reported
free-energy formula. It is not uniform near a zero, does not interchange a
growing-$t$ limit with $N\to\infty$, and is not a finite-size experimental
DQPT certificate. An empirical promotion still requires a finite-size error
budget and an implementation certificate.

### Corollary BSC-ZDQ-02d (rate singularity set)

On the open critical strip, the discontinuity set of the pointwise limiting
rate $\mathcal F_1$ is exactly the zero set of $\zeta$. If
$s_0=\beta_0+it_0$ is such a zero, the rate value exceeds its limiting
off-zero background by
$$
  \log 2-(1-\beta_0)\log 2=\beta_0\log 2.
$$
Indeed, $\eta$ is analytic and not identically zero, so its zeros are
isolated. At a nonzero point it remains nonzero on a neighborhood and the
rate is the continuous function $(1-\operatorname{Re}(s))\log 2$. At a zero,
approach through nonzeros and use the two branches above.

Consequently,
$$
  \mathrm{RH}
  \quad\Longleftrightarrow\quad
  \operatorname{Disc}(\mathcal F_1)
  \subseteq\{s:\operatorname{Re}(s)=1/2\}
  \quad\text{within }0<\operatorname{Re}(s)<1.
$$
This is an exact representation equivalence inside the ideal engineered
model. It does not decide either side, supply an unbounded zero census, or
turn finite fitted minima into exact singularities.

### Corollary BSC-ZDQ-02d.1 (fixed-$\beta$ real-time slice)

For fixed $0<\beta<1$, put $\iota_\beta(t)=\beta+it$. Then
$$
  \operatorname{Disc}(\mathcal F_1\circ\iota_\beta)
  =
  \{t\in\mathbb R:\zeta(\beta+it)=0\},
$$
and every such sliced jump has size $\beta\log 2$.

The general slice theorem gives inclusion in the ambient singular set. Here
the off-zero branch is constant along the line and nonzero points approach
every isolated zero, so the singularity is visible and equality holds.

In the exact limiting model, zero membership also descends through the scalar
rate via the Borel decision cell $\{\log2\}$. This statement requires the
exact pointwise limit. A finite noisy estimator does not inherit that exact
decision. BSC-SCL-08 makes the obstruction quantitative: the logarithmic rate
is stable under amplitude error only while a certified nonzero lower margin
remains, and that margin necessarily closes at an exact zero. Near-zero
finite data therefore require a contour or root-localization certificate, not
an unqualified rate tolerance.

### Proposition BSC-ZDQ-02e (local finite-$N$ zero drift)

Let $s_0=\beta_0+it_0$, with $0<\beta_0<1$, be a zero of $\eta$ of
multiplicity $m$, and put
$$
  a_m=\frac{\eta^{(m)}(s_0)}{m!}\ne0.
$$
For every fixed
$$
  C>(2|a_m|)^{-1/m},
$$
the partial sum $S_N$ has exactly $m$ zeros, counted with multiplicity, in
$$
  |s-s_0|<C N^{-\beta_0/m}
$$
for all sufficiently large $N$. If $m=1$, the unique zero $s_N$ in this disk
is simple and satisfies
$$
  s_N-s_0
  =
  \frac{(-1)^N(N+1)^{-s_0}}{2\eta'(s_0)}
  +O_{s_0}\!\left(
    N^{-2\beta_0}\log N+N^{-\beta_0-1}
  \right).
$$

#### Proof

Choose a compact disk $U\Subset\{0<\operatorname{Re}(s)<1\}$ centered at
$s_0$ and containing no other eta zero. On the shrinking circle
$|s-s_0|=C N^{-\beta_0/m}$,
$$
  \eta(s)=a_m(s-s_0)^m(1+o(1)),
$$
so
$$
  |\eta(s)|
  =\bigl(|a_m|C^m+o(1)\bigr)N^{-\beta_0}.
$$
The compact-uniform Euler expansion above and
$N^{-\beta_0/m}\log N\to0$ give, uniformly on that circle,
$$
  R_N(s)=\eta(s)-S_N(s)
  =(-1)^N\left(\frac12(N+1)^{-s}
    +O_U(N^{-\operatorname{Re}(s)-1})\right)
$$
and hence
$$
  \sup |R_N(s)|
  =\left(\frac12+o(1)\right)N^{-\beta_0}.
$$
The strict condition on $C$ makes $|R_N|<|\eta|$ for large $N$.
Rouché's theorem then gives exactly $m$ zeros of $S_N=\eta-R_N$ in the
disk. This is the BSC-SCL-07b local multiplicity theorem with
$r_N=C N^{-\beta_0/m}$.

For $m=1$, write the unique root as $s_N=s_0+\delta_N$. The disk result gives
$\delta_N=O(N^{-\beta_0})$. Expanding
$$
  \eta(s_N)=\eta'(s_0)\delta_N+O(\delta_N^2)
$$
and using
$$
  (N+1)^{-s_N}
  =(N+1)^{-s_0}\bigl(1+O(\delta_N\log N)\bigr)
$$
in the uniform tail expansion yields the stated formula. $\square$

Because $1-2^{1-s_0}$ is nonzero in the strip, eta and zeta multiplicities
agree. The zeros of $S_N$ are also the zeros of the normalized ideal
coherence because $Z_N(\operatorname{Re}(s))>0$, although the normalized
function is not holomorphic in $s$. For a simple critical-line zero the ideal
root displacement is $O(N^{-1/2})$. Its real and imaginary parts may both
move, so a scan constrained to $\beta_{\mathrm{eff}}=1/2$ need not contain an
exact finite-$N$ zero. This is an ideal asymptotic localization theorem, not a
calibrated error bar for the five-qubit experiment and not uniform over zero
height, multiplicity, or the strip boundary.

## 4. The generalized Loschmidt chain

Write
$$
  D_N(s)=\sum_{n=1}^{N}n^{-s}
$$
and let $\theta(t)$ be the declared Riemann--Siegel theta function. The
source's finite generalized Loschmidt amplitude is
$$
  G_N(\beta_{\mathrm{eff}},t)
  =\frac{
     e^{i\theta(t)}D_N(\beta_{\mathrm{eff}}+it)
     +e^{-i\theta(t)}D_N(\beta_{\mathrm{eff}}-it)}
     {2Z_N(\beta_{\mathrm{eff}})}.
$$
This is an exact finite definition. Its connection to the Hardy
$Z$-function uses a Riemann--Siegel truncation, a choice
$N=N(t)\asymp\sqrt{|t|/(2\pi)}$, a remainder estimate, and a joint
large-$t$/large-$N$ statement. An approximate equality does not preserve
exact zeros without a contour margin or another root-stability theorem.

The paper's $18$-spin result near the $10^{12}$-th zero is a numerical
simulation of this chain. It is not an $18$-spin hardware execution and is
not an infinite zero census.

## 5. BSC multi-morphism record

The applicable BSC object is the
[`(T,T^\sharp,K,R,\Theta,\delta,C,\mathrm{Cert})` typed morphism](https://github.com/jkolantree/BSC/blob/b56495bc9c33dae73c28228708110450586b46e7/paper/source/On_Boundaries_of_Evidence.tex#L916-L1005).
For this application the transfer must be split as follows.

| Arrow | $T$ and domain | $T^\sharp$ / accessible query | $K$ | Residual, defect, or deficiency | Required certificate |
|---|---|---|---|---|---|
| $\mathfrak M_{\rm ana}$: $(\beta_{\mathrm{eff}},t,N)\mapsto(S_N,L_N,G_N)$ | Declared finite sums, $N\in\mathbb N$, stated strip/domain | Pull back complex-amplitude and contour-zero-count queries | Exact algebraic normalization/sign convention | $R_{\eta,N}=\eta-S_N$; Riemann--Siegel remainder for $G_N$ | Present finite proof; uniform tail or approximation bound; nonzero contour margin |
| $\mathfrak M_{\rm model}$: analytic terms $\mapsto$ ideal quantum model | $n\mapsto\lvert n\rangle$, $H_N$, $\rho_{\beta_{\mathrm{eff}},N}$, phase operator | Probe $\sigma_x+i\sigma_y$ pulls back to the declared system operator | Ideal probe readout | Preparation, Hamiltonian, phase, and readout residuals are separate | Basis encoding, units, precision, accessible algebra, controller, clock |
| $\mathfrak M_{\rm impl}$: ideal model $\mapsto$ NMR implementation | Restricted to the $16$-level work system and the published pulse protocol | Actual NMR effects paired with the ideal probe query | Calibration, pulse compilation, ensemble readout, fitting | $\Theta_{\rm impl}$ and directed experiment deficiency $\delta_{\rm impl}$ need measured enclosures | Raw data, pulse files, calibration, exclusions, uncertainty, hashes; absent here |
| $\mathfrak M_{\rm obs}$: traces $\mapsto$ a zero report | Complex estimates plus uncertainty at predeclared sample points | Query “zero in contour/interval,” not merely “small magnitude” | Frozen estimator, interpolation, root isolation, multiplicity handling | Coverage, discretization, fit bias, and confidence error | Exact-zero or contour-count rule fixed before evaluation |
| $\mathfrak M_{\rm dqpt}$: amplitudes $\mapsto$ DQPT statement | A declared joint or iterated limit and rate function | Nonanalyticity of the limiting rate, not finite visual sharpness | Limit/renormalization map | Finite-size, log-near-zero, and limit-interchange residuals | Full scale-limit certificate |
| $\mathfrak M_{\rm RH}$: certified critical set $\mapsto$ RH claim | Entire open critical strip, or a theorem reducing it to a certified domain | Universal query “every nontrivial zero has real part $1/2$” | Logical promotion only after complete coverage | Uncovered height/real-part region is a hard gate, not a small error | Complete zero census or independent proof; neither is present |

The completed context $C$ must retain the distinction among the mathematical
parameter $\beta_{\mathrm{eff}}$, laboratory temperature, NMR carrier,
state-preparation controller, pulse compiler, instrument, clock, estimator,
and classical reference-zero data. The loss vector must keep analytic
truncation, implementation naturality defect, statistical deficiency,
readout error, quotient loss, and limit failure in separate coordinates.

The central paper currently defines quantum operational quotients but proves
composition explicitly only for the stochastic variant. Accordingly, this
table is a well-typed application proposal; it is not a claim that a complete
BSC quantum-composition theorem already exists.

## 6. Release claim statuses

These identifiers are synchronized with the central claim ledger in version
1.1.0.

| ID | Claim | Verdict | Math support | Empirical | Computational | Source | Transfer |
|---|---|---|---|---|---|---|---|
| BSC-ZDQ-01 | The declared finite model satisfies $L_N=-S_N/Z_N$, where $S_N=\eta_N$. | true | proved | N/A | unexecuted | present proof | bounded |
| BSC-ZDQ-02a | The alternating eta tail obeys the displayed pointwise and compact-uniform bound on $\operatorname{Re}(s)>0$. | true | proved | N/A | unexecuted | present proof | certified |
| BSC-ZDQ-02b | A declared contour with certified whole-boundary separation transfers its zero count from $S_N$ to $\eta$ and $\zeta$. | true | proved | N/A | unexecuted | present proof | bounded |
| BSC-ZDQ-02c | At fixed $s$ in the open strip, the coherence decay exponent and pointwise rate separate eta zeros from nonzeros. | true | proved | N/A | unexecuted | present proof | bounded |
| BSC-ZDQ-02d | The ideal pointwise rate-discontinuity set is exactly the zeta-zero set, and its confinement to the critical line is equivalent to RH. | true | proved | N/A | unexecuted | present proof | bounded |
| BSC-ZDQ-02d.1 | A fixed-$\beta$ real-time rate slice is discontinuous exactly at zeta-zero ordinates on that line. | true | proved | N/A | unexecuted | present proof | bounded |
| BSC-ZDQ-02e | Finite partial-sum zeros localize near each fixed limiting zero at the proved multiplicity-dependent scale, with an explicit simple-root displacement. | true | proved | N/A | unexecuted | present proof | bounded |
| BSC-ZDQ-03 | An exact-zero query factors through a finite-resolution report that identifies zero with a nonzero amplitude. | false | proved | N/A | unexecuted | present proof | blocked |
| BSC-ZDQ-04 | The publication reports finite NMR coherence signatures at the first five fitted locations under its five-qubit protocol. | N/A | N/A | single study | unexecuted | verified publication | local only |
| BSC-ZDQ-05 | The reported finite evidence entails thermodynamic exclusivity at $\beta_{\mathrm{eff}}=1/2$ or RH over the full critical strip. | false | proved | single study | unexecuted | present proof | blocked |
| BSC-ZDQ-06 | The proposed algorithm gives an end-to-end advantage under a matched zero-search task, error norm, success probability, and resource accounting. | open | conditional | untested | unexecuted | verified publication | local only |

BSC-ZDQ-05 is a non-entailment verdict about the **sufficiency of finite or
confusable evidence for a stronger promotion**, not a verdict that RH itself
is false.

## 7. Finite-resolution exact-zero obstruction

### Corollary BSC-ZDQ-03 (zero/nonzero confusability)

Let $A\subseteq\mathbb C$ contain $0$, let $Y$ be any report space, and
let $O:A\to Y$ be an observation map. Define the exact-zero predicate
$$
  q:A\to\{0,1\},\qquad q(a)=\mathbf 1_{\{0\}}(a).
$$
If there is a $z\in A\setminus\{0\}$ such that $O(z)=O(0)$, then no
decision map $d:Y\to\{0,1\}$ can satisfy $q=d\circ O$ on $A$.

This is the deterministic specialization of BSC-QUO-03: the report fiber
$O^{-1}(O(0))$ crosses the exact-zero decision boundary.

For a deterministic finite-resolution report, any report cell containing
both $0$ and a nonzero amplitude satisfies the hypothesis. A set-valued disk
or confidence-region report consistent with both values likewise cannot, by
itself, certify exact zero. For a stochastic instrument the same conclusion
follows when the two amplitudes induce non-mutually-singular output laws.
For binary equal-prior laws $P_0,P_1$, every decoder has average, and hence
worst-case, error at least
$$
  \frac{1-d_{\mathrm{TV}}(P_0,P_1)}{2}.
$$
Repeated measurements must use the declared product or dependent joint laws
and state the sample count. The corollary is deliberately scoped:

- an enclosure excluding $0$ can certify nonzero;
- an analytic identity, a validated contour count, or another independent
  proof may certify a zero;
- the obstruction applies to the finite-resolution report alone, not to all
  possible combinations of measurement and mathematics.

This is the framework's
[exact-decision descent theorem](../framework/Normalized_Scale_Profiles.md#4-stochastic-observations-and-exact-decisions):
the exact-zero query does not descend through an observation that fails to
separate zero from nonzero output laws.

## 8. Limit gates

The following gates are noncompensating.

1. **Finite algebra gate.** Verify the exact definitions of $H_N$,
   $\rho_{\beta_{\mathrm{eff}},N}$, the phase convention, $L_N$, and
   $G_N$.
2. **Analytic truncation gate.** State the domain and a uniform error bound.
   Pointwise convergence is insufficient for zero counts.
3. **Renormalization gate.** Distinguish $L_N$ from $Z_NL_N$. The raw
   coherence tends to zero throughout the fixed critical strip.
4. **Root-stability gate.** Supply a boundary lower bound and a Rouché,
   argument-principle, or equivalent validated root-isolation certificate.
5. **Implementation gate.** Bound state-preparation, Hamiltonian, pulse,
   decoherence, readout, fitting, and sampling errors in the same observable
   and units.
6. **DQPT gate.** Supply the complete DQPT interpretation certificate:
   finite dynamical family; preparation and quench; physical size
   normalization; amplitude or echo convention; real-time slice; convergence
   and limit order; singularity class; robustness regime; estimator law; and
   implementation evidence. A small finite-system coherence is not itself a
   thermodynamic nonanalyticity.
7. **Joint-limit gate for $G_N$.** Declare $N(t)$, rounding, limit order,
   Riemann--Siegel remainder, uniformity domain, and root-stability margin.
8. **Universal-coverage gate.** A bounded list of zeros, however high, does
   not decide a universal claim over all nontrivial zeros.
9. **Decision gate.** Show that the target query descends through the actual
   report law; a discontinuity in an ideal limiting profile is not itself an
   exact finite-data decoder.

These instantiate BSC's scale-limit, normalized-profile, parameter-slice, and
decision-descent framework.

## 9. Requirements for a zero census

A finite-domain claim should declare one or more bounded Jordan domains
$\Omega_j$ and provide, for each:

1. exact boundary geometry and orientation;
2. proof that the relevant analytic function has no boundary zero;
3. a rigorous lower enclosure for
   $\inf_{\partial\Omega_j}|\eta|$, or an equivalent validated contour
   certificate;
4. a uniform truncation/remainder bound strictly below that margin;
5. a validated count including multiplicities;
6. proof that contour interiors are disjoint or a deduplication rule;
7. treatment of poles, trivial zeros, and the factor $1-2^{1-s}$;
8. coverage of every point in the stated finite region; and
9. artifact identity, code, environment, tolerances, outputs, and retained
   receipts for any numerical step.

Measured values add a sampling frame, instrument and calibration record,
uncertainty model, exclusion policy, frozen fitting/root-isolation procedure,
and raw-data provenance. A scan only on
$\beta_{\mathrm{eff}}=1/2$ can find on-line candidates but cannot exclude
off-line zeros. A scan at $\beta_{\mathrm{eff}}=0.3$ over a finite time
window excludes neither other real parts nor other heights.

A finite census proves a finite census. To establish RH it must be joined to
an independent theorem covering the unbounded remainder. No such theorem or
complete empirical coverage is supplied here.

## 10. Recurrence is not persistence

“Vanishing and revival” describes recurrence of an endpoint observable:
$L_N$ or $G_N$ returns near a selected value at selected times. BSC
persistence is stronger. It requires every prefix of the composed protocol to
remain inside its viability tube with admissible certificates.

For this application, prefix persistence would require bounds after at least:

1. population encoding;
2. phase-sign imprinting;
3. logarithmic Hamiltonian evolution;
4. probe coupling;
5. ensemble readout;
6. complex-coherence estimation;
7. interpolation/root isolation; and
8. analytic-limit and zero-count promotion.

A later fitted match cannot erase a demonstrated earlier excursion. This is
the distinction formalized by BSC's
[`recurrence and persistence`](https://github.com/jkolantree/BSC/blob/b56495bc9c33dae73c28228708110450586b46e7/paper/source/On_Boundaries_of_Evidence.tex#L1371-L1441).

## 11. Resource comparison

The primary paper derives, for its quantum evaluation construction in the
critical strip, a reported overall bound
$$
  \delta^{-1}|t|^{(1-\beta_{\mathrm{eff}})/2}
  \operatorname{Poly}\!\left(
    \log\delta^{-1},\log|t|,
    (1-\beta_{\mathrm{eff}})^{-1},
    \beta_{\mathrm{eff}}^{-1}
  \right).
$$
At $\beta_{\mathrm{eff}}=1/2$, it reports
$$
  \delta^{-1}|t|^{1/4}
  \operatorname{Poly}(\log\delta^{-1},\log|t|)
$$
against the paper's direct Riemann--Siegel comparator scaling
$\sim |t|^{1/2}$.

That comparison is conditional on the source's state-preparation and
Hamiltonian-simulation constructions, finite-precision arithmetic,
$N=\Theta(\sqrt{|t|})$, and amplitude amplification or quantum amplitude
estimation. The source itself states that direct sampling has quadratic
dependence on the required expectation precision before that improvement.
The asymptotic must not be relabeled “verified end-to-end quantum advantage”
until the same task and accuracy contract includes:

- state preparation and its success probability/repetitions;
- controlled evolution and arithmetic-oracle synthesis;
- logical versus physical gates and fault-tolerance assumptions;
- ancillas, depth, memory, and classical preprocessing;
- amplitude-estimation success probability;
- the number of candidate points/contours needed for search and census;
- root conditioning and the conversion from amplitude error to location
  error;
- confidence allocation across all tested regions; and
- a matched classical implementation and error criterion.

The hardware proof of principle does not execute this asymptotic algorithm at
scale. The large-zero examples are numerical simulations. BSC-ZDQ-06
therefore remains conditional and computationally unexecuted in this package.

## 12. Engineered representation is not an independent origin

The construction chooses $H_N$ with eigenvalues $\log n$, prepares
weights $n^{-\beta_{\mathrm{eff}}}$, and applies phases $(-1)^n$.
BSC-ZDQ-01 then produces the truncated eta sum term by term. This is an exact
and useful physical representation, but the zeta structure is an input to the
engineering map. Without a separately derived physical law that selects the
same Hamiltonian, populations, phase operator, and observable independently
of the target number-theoretic function, the representation does not by
itself establish a physical *origin* of RH.

Nor does $\beta_{\mathrm{eff}}=1/2$ identify a unique Kelvin temperature.
If a dimensional Hamiltonian is written
$$
  H_N^{\mathrm{phys}}
  =\varepsilon\sum_{n=1}^{N}\log(n)\lvert n\rangle\langle n\rvert,
$$
then a physical Gibbs exponent has
$$
  \beta_{\mathrm{phys}}H_N^{\mathrm{phys}}
  =\frac{\varepsilon}{k_BT_{\mathrm{lab}}}
    \sum_{n=1}^{N}\log(n)\lvert n\rangle\langle n\rvert,
$$
so
$$
  \beta_{\mathrm{eff}}
  =\frac{\varepsilon}{k_BT_{\mathrm{lab}}}.
$$
The value $1/2$ corresponds to a Kelvin temperature only after the energy
scale $\varepsilon$ and a genuine Gibbs-preparation bridge are fixed.
Rescaling $\varepsilon$ changes the corresponding Kelvin value while
leaving the dimensionless model unchanged. In the reported NMR experiment,
the target populations are engineered at a carrier temperature of $305$ K;
the publication does not identify $305$ K with
$\beta_{\mathrm{eff}}=1/2$.

## 13. F09 documentary fixture

[`fixtures/F09_zeta_dqpt_transfer/`](../fixtures/F09_zeta_dqpt_transfer/)
specifies an exact $N=4$, $\beta_{\mathrm{eff}}=1$, $t=0$ instance of
BSC-ZDQ-01:
$$
\begin{aligned}
 Z_4(1)&=\frac{25}{12},\\
 \eta_4(1)&=\frac{7}{12},\\
 Z_4(1)L_4(1,0)&=-\frac{7}{12},\\
 L_4(1,0)&=-\frac{7}{25}.
\end{aligned}
$$
A nearby invalid control flips only the fourth phase and gives
$-13/25$, so it must fail the declared identity check. The instance is
chosen for exact rational arithmetic, not as a zeta-zero or DQPT test.

F09 contains inputs and expected outputs only. It deliberately has no
execution receipt and makes no empirical claim.

## 14. Remaining obligations

1. Obtain the paper's underlying data and code, which the primary manuscript
   says are available from the corresponding author on reasonable request,
   before attempting independent empirical or computational replay.
2. Specify and execute a validated contour census with interval bounds and a
   retained receipt.
3. Build a full implementation morphism with calibration, pulse, raw-data,
   fit, and uncertainty artifacts.
4. Supply the physical DQPT interpretation certificate for the already-proved
   ideal fixed-$s$ pointwise rate: construct the compatible infinite-system
   family, physical volume normalization, convergence topology and limit
   order, and a finite-size/implementation error bridge. The mathematical
   limit in BSC-ZDQ-02c is not an open obligation.
5. Audit BSC-ZDQ-06 against a matched end-to-end classical comparator.
6. Resolve BSC-QOP-03 by adding the missing quantum-morphism composition
   theorem or keeping composition explicitly restricted to the already proved
   variants.

The existing BSC inheritance boundary already states that no RH proof is
inherited from finite arithmetic constructions and that finite truncations do
not certify an infinite spectral correspondence:
[`inheritance ledger`](https://github.com/jkolantree/BSC/blob/b56495bc9c33dae73c28228708110450586b46e7/paper/source/On_Boundaries_of_Evidence.tex#L1927-L1937).
