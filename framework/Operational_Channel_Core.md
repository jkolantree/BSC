# Operational channel core

## Status and scope

This module is part of the released `1.3.0` framework.

The module supplies a common mathematical envelope for heterogeneous
experiments:

$$
\text{parameter}
\longrightarrow
\text{preparation}
\longrightarrow
\text{driven evolution}
\longrightarrow
\text{measurement}
\longrightarrow
\text{report}
\longrightarrow
\text{decision}.
$$

The common object is the induced report channel, not a shared microscopic
Hamiltonian, material law, or ontology. Classical systems, quantum systems,
inverse materials problems, and analog information processors may instantiate
the same typed pipeline while retaining entirely different physical dynamics.

The channel theory, data-processing inequalities, trace-distance
contractivity, sufficient statistics, and open-system energy balance used
below, together with boundary energy-flow algebra, are established
mathematics. The BSC contribution is narrower: it binds those results to
reachable-set defects, report-relative decisions, component and seam
residuals, denominator identity, evidence identity, claim-local status, and
explicit demotion rules.

This module does **not** prove closure of the full eight-field quantum BSC
morphism. Claim BSC-QOP-03 remains open.

## 1. Typed report experiments

Let $\Theta$ be a declared parameter or intervention space. For each
$\theta\in\Theta$, preparation produces an initial classical law or quantum
state $z_0(\theta)$. A finite ideal pipeline is

$$
z_0(\theta)
\mathop{\longmapsto}^{T_1}
z_1(\theta)
\mathop{\longmapsto}^{T_2}
\cdots
\mathop{\longmapsto}^{T_m}
P_\theta^Z,
$$

where $P_\theta^Z$ is a classical law on the terminal report space $Z$. Every
interface carries one of the following declared types.

1. A classical interface carries probability laws and total variation
   $d_{\mathrm{TV}}(P,Q)=\sup_A|P(A)-Q(A)|$.

2. A finite-dimensional quantum interface carries density operators and trace
   distance $D_{\mathrm{tr}}(\rho,\sigma)=\frac12\lVert\rho-\sigma\rVert_1$.

3. A quantum-to-classical interface is a declared POVM measurement channel.
4. A classical-to-quantum interface is a declared preparation channel.

A classical stage is a Markov kernel and a quantum stage is completely
positive and trace preserving (CPTP). If a device has memory, feedback,
history-dependent control, or a changing clock, those variables must be
included in the stage state. They may not be suppressed while a Markov or
memoryless theorem is invoked.

### Definition 1.1 (Operational report envelope)

The family

```math
\mathsf{ORE}
=
\left(
\Theta,
\lbrace z_0(\theta)\rbrace_{\theta\in\Theta},
\lbrace T_k\rbrace_{k=1}^m,
Z,
\lbrace P_\theta^Z\rbrace_{\theta\in\Theta},
\mathsf{Cert}_{\mathrm{ORE}}
\right)
```

is an operational report envelope when every interface, control, domain,
measurement, report rule, and evidence identity is declared. It induces the
classical statistical experiment

$$
\mathsf E_Z=\lbrace P_\theta^Z:\theta\in\Theta\rbrace.
$$

The envelope does not identify two physical mechanisms. It says only that
their empirical claims can be compared at a common report-law boundary.

## 2. Compatible fixed-interface propagation

Let $T_k$ and $\widehat T_k$ be ideal and implemented stages with the same
declared input and output interfaces. Put

$$
z_k=T_kz_{k-1},
\qquad
\widehat z_k=\widehat T_k\widehat z_{k-1},
\qquad
E_k=d_k(\widehat z_k,z_k),
$$

where $d_k$ is total variation or trace distance according to the output
type. Let $\widehat{\mathcal R}_{k-1}$ be the implemented reachable set, or a
certified superset containing every implemented input that can occur under the
declared preparation, control, horizon, and prior-stage defects.

### Theorem 2.1 (Contraction-weighted report-channel bound)

Assume:

1. the initial discrepancy obeys
   $d_0(\widehat z_0,z_0)\le\varepsilon_0$;

2. for every implemented reachable input
   $\widehat z\in\widehat{\mathcal R}_{k-1}$,
   $d_k(\widehat T_k\widehat z,T_k\widehat z)\le\varepsilon_k$;

3. for every reachable ideal/implemented pair $(z,\widehat z)$,
   $d_k(T_k\widehat z,T_kz)\le\eta_k d_{k-1}(\widehat z,z)$.

Then

$$
E_k\le\varepsilon_k+\eta_kE_{k-1}
$$

and

$$
\boxed{
E_m
\le
\sum_{k=0}^{m}
\varepsilon_k
\prod_{j=k+1}^{m}\eta_j
}.
$$

The empty product is $1$.

#### Proof

The triangle inequality gives

$$
\begin{aligned}
E_k
&=
d_k(\widehat T_k\widehat z_{k-1},T_kz_{k-1})\\
&\le
d_k(\widehat T_k\widehat z_{k-1},T_k\widehat z_{k-1})
+
d_k(T_k\widehat z_{k-1},T_kz_{k-1})\\
&\le
\varepsilon_k+\eta_kE_{k-1}.
\end{aligned}
$$

Iteration yields the displayed product-sum bound. $\square$

Because total variation and trace distance are at most $1$, the terminal
certificate may use the sharper enclosure

$$
E_m
\le
\min\left\lbrace
1,
\sum_{k=0}^{m}
\varepsilon_k
\prod_{j=k+1}^{m}\eta_j
\right\rbrace.
$$

If any $\varepsilon_k$ or $\eta_k$ is estimated rather than proved
deterministically, its confidence event and simultaneous-coverage rule belong
in $\mathsf{Cert}_{\mathrm{ORE}}$; the algebra does not create coverage.

### Reachability is substantive

A defect bound proved only on the ideal reachable set is insufficient. The
first term in the proof is evaluated at the **implemented** input
$\widehat z_{k-1}$. Certification therefore requires the implemented
reachable set or a proved envelope containing it. This is the same causal
boundary exposed by BSC-SIM-03: a small standalone error outside the coupled
host trajectory does not control the host.

For a classical Markov kernel, $\eta_k$ may be bounded by its Dobrushin
coefficient. For a CPTP channel, trace-distance contractivity gives
$\eta_k\le1$. A strict quantum contraction $\eta_k<1$ requires a separately
proved global or restricted strong-contraction result; it is not automatic.

For a fixed POVM $\mathcal M$,

$$
d_{\mathrm{TV}}\bigl(\mathcal M(\rho),\mathcal M(\sigma)\bigr)
\le D_{\mathrm{tr}}(\rho,\sigma).
$$

A subsequent report kernel also contracts total variation. Identical
measurement and report stages therefore add no defect. An implemented
measurement or report rule that differs from the ideal one is another stage
and needs its own reachable-set defect.

Postselection requires special care. A complete quantum instrument that keeps
both success and failure outcomes is CPTP and remains contractive. Dividing by
the success probability to report only a normalized successful branch is
nonlinear and can increase trace distance. Theorem 2.1 applies to that
conditioned report only with a separate conditioning estimate and a certified
positive success-probability lower bound.

### Non-transfer to BSC-QOP-03

Theorem 2.1 propagates one state-or-law metric through a fixed compatible
pipeline. It does not construct, compose, or prove associativity for

$$
(T,T^\sharp,K,R,\Theta,\delta,C,\mathsf{Cert}).
$$

In particular it supplies no general closure theorem for partial domains,
observable pullbacks, completions, equation residuals, deficiencies,
certificate witnesses, or physical interfaces. It is a restricted corollary
of BSC-SIM-03 plus classical and quantum data processing. BSC-QOP-03 remains
blocked.

## 3. No downstream resurrection

### Proposition 3.1 (Report data processing)

For any classical report kernel $R$,

$$
d_{\mathrm{TV}}(RP,RQ)\le d_{\mathrm{TV}}(P,Q).
$$

For any CPTP channel $\Phi$,

$$
D_{\mathrm{tr}}(\Phi(\rho),\Phi(\sigma))
\le D_{\mathrm{tr}}(\rho,\sigma).
$$

For a fixed measurement followed by a report kernel, combine these two
inequalities. Consequently, downstream processing cannot increase the
distinguishability lost by an upstream channel. If two parameters induce the
same terminal report law, no decoder using only that report can distinguish
them.

Exact finite-label decoding is possible only when different-label report laws
are supported on a measurable partition, as in BSC-QUO-03. A visually
separated statistic, a fitted classifier, or an average reconstruction metric
does not replace this condition.

### Definition 3.2 (Deterministic identified set)

For a deterministic forward report $F:\Theta\to Y$, observation $y$, metric
$d_Y$, and certified error radius $\varepsilon$, define

```math
\mathcal I_\varepsilon(y)
=
\lbrace\theta\in\Theta:d_Y(F(\theta),y)\le\varepsilon\rbrace.
```

For a target property $q:\Theta\to Q$, an exact claim $q(\theta)=q_0$ is
licensed by this report only if $q$ is constant on
$\mathcal I_\varepsilon(y)$. For a declared center rule $c:Y\to Q$, a
tolerance claim of radius $\tau$ requires

$$
\sup_{\theta\in\mathcal I_\varepsilon(y)}
d_Q(q(\theta),c(y))\le\tau.
$$

If the center may be chosen after fixing the identified set, the exact
condition is

$$
\inf_{c\in Q}\sup_{\theta\in\mathcal I_\varepsilon(y)}
d_Q(q(\theta),c)\le\tau.
$$

Diameter at most $2\tau$ is necessary but is not sufficient in a general
metric space. At zero error, exact factorization through $F$ is equivalent to
constancy of $q$ on every fiber of $F$.

This is the inverse-problem form of no downstream resurrection. A measured
composition or crystal structure may strongly constrain a formation history
without uniquely reconstructing it.

### Proposition 3.3 (Forward error encloses compatible inverse sets)

Let actual and ideal deterministic reports $F,G:\Theta\to Y$ obey

$$
\sup_{\theta\in\Theta}d_Y(F(\theta),G(\theta))\le B.
$$

For

```math
\mathcal I_F(y,\delta)
=
\lbrace\theta:d_Y(F(\theta),y)\le\delta\rbrace,
```

and the analogous set $\mathcal I_G(y,\delta)$,

$$
\boxed{
\mathcal I_F(y,\delta)
\subseteq
\mathcal I_G(y,\delta+B),
\qquad
\mathcal I_G(y,\delta)
\subseteq
\mathcal I_F(y,\delta+B)
}.
$$

#### Proof

If $\theta\in\mathcal I_F(y,\delta)$, the triangle inequality gives

$$
d_Y(G(\theta),y)
\le
d_Y(G(\theta),F(\theta))
+
d_Y(F(\theta),y)
\le B+\delta.
$$

The other inclusion follows after interchanging $F$ and $G$. $\square$

This is claim BSC-CHN-03. A deterministic target is robustly licensed only
when it is constant on the applicable enlarged set, or satisfies the
declared enclosing-radius criterion there. The proposition supplies no
parameter-space Hausdorff stability or small parameter error without inverse
regularity. Sampling uncertainty is added to $\delta$ under its own coverage
statement; it is not created or absorbed by $B$.

### Proposition 3.4 (Spectral intensity agreement is not quantum identity)

Let $|\omega_1\rangle,|\omega_2\rangle$ be orthogonal modes and define

```math
|\psi\rangle
=
\frac{|\omega_1\rangle+|\omega_2\rangle}{\sqrt2},
\qquad
|\phi\rangle
=
\frac{|\omega_1\rangle-|\omega_2\rangle}{\sqrt2}.
```

The two pure states have identical spectral-intensity laws and hence unit
intensity-overlap score, but

$$
\langle\psi|\phi\rangle=0,
\qquad
D_{\mathrm{tr}}
\left(
|\psi\rangle\langle\psi|,
|\phi\rangle\langle\phi|
\right)
=1.
$$

Thus equality of a measured marginal, even with overlap score $1$, does not
license equality or closeness of the full quantum states. Relative phase and
all other unmeasured modes remain completion variables. This is claim
BSC-QPH-02.

### Proposition 3.5 (Conditioning can amplify distinguishability)

Let

```math
\rho
=
\frac12
\left(
|0\rangle\langle0|+|1\rangle\langle1|
\right),
\qquad
\sigma
=
\frac12
\left(
|0\rangle\langle0|+|2\rangle\langle2|
\right).
```

Then $D_{\mathrm{tr}}(\rho,\sigma)=1/2$. Filter onto
$\mathrm{span}\lbrace|1\rangle,|2\rangle\rbrace$ and normalize on success. The
conditional states are $|1\rangle\langle1|$ and $|2\rangle\langle2|$, whose
trace distance is $1$. The complete instrument, including failure, remains
contractive; the amplification is introduced by conditioning.

## 4. Energy accounting for driven quantum channels

Let a finite-dimensional open quantum system obey

```math
\dot\rho(t)
=
-\frac{i}{\hbar}[H(t),\rho(t)]
+\mathcal D_t(\rho(t)),
```

where the total generator defines physical trace-preserving evolution. Fix an
energy zero and define

$$
E(t)=\mathrm{Tr}[\rho(t)H(t)].
$$

### Proposition 4.1 (Driven open-system energy identity)

If $\rho$ and $H$ are differentiable, then

```math
\boxed{
\dot E(t)
=
\mathrm{Tr}[\rho(t)\dot H(t)]
+
\mathrm{Tr}[H(t)\mathcal D_t(\rho(t))]
}.
```

#### Proof

Differentiate $\mathrm{Tr}(\rho H)$. The Hamiltonian commutator
contributes

$$
-\frac{i}{\hbar}\mathrm{Tr}([H,\rho]H)=0
$$

by cyclicity of trace. The two displayed terms remain. $\square$

The terms are conventionally called drive/work power and dissipative energy
flow under a fixed system/bath split. The identity has strict limits.

- The split between $H$ and $\mathcal D_t$ is not unique under strong
  coupling, Lamb-shift conventions, feedback, or non-Markovian reduction.
- A time-dependent additive gauge $c(t)I$ changes the apparent work term
  unless the energy zero is fixed.
- The dissipative term can cool, heat, or leave energy invariant.
- A periodic Hamiltonian need not perform zero net work over a period.
- Measurements, resets, jumps, coupling energy, and output-field energy need
  explicit additional ledgers.

Parametric amplification is therefore compatible with conservation because a
drive can supply energy. The identity alone proves neither amplification nor
positive net work in a particular experiment.

The finite-dimensional hypothesis is substantive. A full bosonic cavity
requires either a declared finite-dimensional truncation with controlled
error or trace-class and domain hypotheses sufficient to justify the
differentiation and cyclic trace steps.

### Definition 4.2 (Typed finite energy-port diagram)

Let $V$ be a finite set of components. For each $v\in V$, let
$U_v:[t_0,t_1]\to\mathbb R$ be absolutely continuous stored energy,
$b_v\in L^1([t_0,t_1])$ a declared non-port supply rate that is positive
into $v$, and $H_v$ a finite set of port half-edges with inward powers
$p_h\in L^1([t_0,t_1])$. Define the component residual

```math
r_v
=
\dot U_v-b_v-\sum_{h\in H_v}p_h.
```

A gluing is a partial matching $\mathcal M$ of disjoint half-edges. For a
matched seam $e=\lbrace h,\bar h\rbrace\in\mathcal M$, define

$$
g_e=p_h+p_{\bar h}.
$$

Unmatched half-edges form the external set $H_{\mathrm{ext}}$. The assembled
global residual is

```math
R_G
=
\frac{d}{dt}\sum_{v\in V}U_v
-\sum_{v\in V}b_v
-\sum_{h\in H_{\mathrm{ext}}}p_h.
```

The diagram is physically admissible only under an additive storage
decomposition. Coupling energy, interface storage, a material sheet, or an
unresolved loss omitted by $\sum_vU_v$ must be promoted to its own component
or retained as an external port. Matched half-edges must share the same
carrier, unit, clock and rate convention, reference cut or plane, time
window, bandwidth, calibration, and evidence identity, with opposite
orientation. Coordinate-time power, proper-time power, band-averaged power,
and instantaneous broadband power are not interchangeable without a
conversion certificate.

### Theorem 4.3 (Energy-port gluing and residual localization)

For every typed finite energy-port diagram,

```math
\boxed{
R_G
=
\sum_{v\in V}r_v
+
\sum_{e\in\mathcal M}g_e
}
```

almost everywhere. Consequently, exact component balances and exact seam
matching imply

```math
\frac{d}{dt}\sum_{v\in V}U_v
=
\sum_{v\in V}b_v
+
\sum_{h\in H_{\mathrm{ext}}}p_h.
```

If $|r_v|\le\varepsilon_v$ and $|g_e|\le\delta_e$, then

$$
|R_G|
\le
\sum_{v\in V}\varepsilon_v
+
\sum_{e\in\mathcal M}\delta_e,
$$

and

```math
\left|
\Delta U_G
-
\int_{t_0}^{t_1}
\left(
\sum_vb_v+\sum_{h\in H_{\mathrm{ext}}}p_h
\right)dt
\right|
\le
\sum_v\int_{t_0}^{t_1}|r_v|\mkern3mu dt
+
\sum_e\int_{t_0}^{t_1}|g_e|\mkern3mu dt.
```

#### Proof

Summing the component residuals partitions the half-edge powers into
unmatched ports and matched pairs:

```math
\sum_vr_v
=
R_G-\sum_{e=\lbrace h,\bar h\rbrace\in\mathcal M}
(p_h+p_{\bar h})
=
R_G-\sum_eg_e.
```

Rearrangement proves the identity. The pointwise and integrated bounds follow
from the triangle inequality and absolute continuity. $\square$

This is BSC-ENE-02. Its non-converse is essential: $R_G=0$ does not imply
$r_v=0$ or $g_e=0$ separately. Local component and seam errors can cancel.
A global conservation residual therefore does not certify local seams,
component dynamics, state continuity, Maxwell trace compatibility, or PDE
well-posedness.

The term $b_v$ is not energy creation. It represents exchange with a drive,
pump, bath, reservoir, moving support, or other component excluded from the
displayed graph. If that system enters scope, $b_v$ must become a matched
port. Proposition 4.1 is a one-component reduced-model instance, but calling
$\mathrm{Tr}(H\mathcal D_t(\rho))$ a literal heat or bath current
requires a declared microscopic system-bath split. At strong coupling,
interaction energy must be retained. For example, if

```math
H_{\mathrm{tot}}(t)
=
H_S(t)+\sum_\nu H_\nu+V(t)
```

and the $H_\nu$ are time independent, then with
$J_E^{(\nu)}=-d\langle H_\nu\rangle/dt$,

```math
\frac{d}{dt}\langle H_S+V\rangle
=
\left\langle\partial_t(H_S+V)\right\rangle
+
\sum_\nu J_E^{(\nu)}.
```

Suppressing $V$ is licensed only by an approximation whose error is part of
the certificate.

### Definition 4.4 (Denominator-typed yield and efficiency)

For one boundary, interval, clock, and evidence identity, define

```math
\eta_E
=
\frac{E_{\mathrm{useful,out}}}{E_{\mathrm{charged,in}}},
\qquad
E_{\mathrm{charged,in}}>0.
```

All external drive energy and any decrease of initially stored energy used to
produce the output must be charged. A count yield

$$
\Phi_N=\frac{N_{\mathrm{declared\ event}}}{N_{\mathrm{declared\ input}}}
$$

is not an energy efficiency. Incident photons, absorbed photons, collected
charges, transferred excitations, and chemical products are different
denominators and numerators. For a success event $S$, the end-to-end quantity
is

```math
\eta_{\mathrm{all}}
=
\frac{
\mathbb E[\mathbf 1_S E_{\mathrm{useful,out}}]
}{
\mathbb E[E_{\mathrm{charged,in}}]
},
```

not the efficiency of the normalized successful subensemble alone.

### Proposition 4.5 (Typed efficiency telescoping)

If $E_0,\ldots,E_m$ are positive values of the same typed extensive quantity
at consecutive interfaces, with one boundary chain, interval, cohort,
spectral weighting, and evidence identity, and

$$
\eta_k=\frac{E_k}{E_{k-1}},
$$

then

$$
\prod_{k=1}^m\eta_k=\frac{E_m}{E_0}.
$$

#### Proof

Every intermediate $E_k$ cancels once in the numerator and once in the
denominator. $\square$

This is BSC-ENE-03. Changing the intermediate quantity, boundary, interval,
conditioning event, or evidence identity removes the cancellation and
therefore the inference. Current and chemical product energy cannot both be
counted as independent useful outputs when the current is the charge ledger
that produces that product. Likewise, a probability sink is not an energy port
unless an energy per event or sink Hamiltonian is supplied.

For a declared passive boundary, $\eta_E>1$ is evidence of incomplete ports,
released stored energy, inconsistent valuation, or uncertainty before it is
evidence of anomalous production. A point estimate above one establishes
violation only when its uncertainty interval or a lower bound excludes one.

## 5. Scalar Bernoulli encoders

Let $X$ be an input symbol and suppose that, conditional on $X=x$,

$$
Y_1,\ldots,Y_N
\mathrel{\overset{\mathrm{iid}}{\sim}}
\mathrm{Bernoulli}(q_x),
\qquad
K=\sum_{i=1}^NY_i.
$$

The conditional-iid hypothesis is a claim that must be tested. Phase memory,
drift, coupling between samples, adaptive thresholds, or cached measurements
define a different channel.

### Theorem 5.1 (Sufficient count and information bound)

The count $K$ is sufficient for $X$ relative to $Y^N$, and

$$
I(X;Y^N)=I(X;K)\le H(K)\le\log_2(N+1).
$$

#### Proof

For a binary sequence $y$ of Hamming weight $k$,

$$
\Pr(Y^N=y\mid X=x)=q_x^k(1-q_x)^{N-k}.
$$

The likelihood depends on $y$ only through $K$. Conditional on $K=k$, every
sequence of weight $k$ is equiprobable independently of $x$, so
$X\to K\to Y^N$. Since $K$ is also a function of $Y^N$, the mutual
information is equal. The count has at most $N+1$ values. $\square$

For a uniform 8-bit symbol, exact decoding would require eight bits of mutual
information. Thus $N\ge255$ is necessary under this scalar conditionally-iid
model.

### Theorem 5.2 (Finite-sample zero-error obstruction)

Under the scalar conditionally-iid Bernoulli model, exact zero-error recovery
of 256 input symbols is impossible for every finite $N$.

#### Proof

For every $q_x\in(0,1)$, the law of $K$ has positive mass at every
$k=0,\ldots,N$. The endpoint parameters $q_x=0$ and $q_x=1$ have singleton
supports $\lbrace0\rbrace$ and $\lbrace N\rbrace$. Hence at most two conditional laws can have
pairwise disjoint supports. The 256 different labels required for exact
decoding cannot satisfy the measurable-partition condition of BSC-QUO-03.
$\square$

Distinct interior values of $q_x$ can permit an error probability tending to
zero as $N\to\infty$ under additional separation assumptions. That is not
finite $N$ lossless coding.

The raw record contains $N$ output bits per 8-bit input symbol. Its nominal
raw-output factor is therefore

$$
\mathcal C_N=\frac{8}{N}.
$$

Only $N<8$ is compression by raw output-bit count. At $N\ge8$ the record is
not compressed, even if averaging improves a distortion metric. The wire cost
is $N$ bits only if every draw is transmitted; cached or receiver-local
sampling has a different communications ledger. The sufficient count can
itself be stored in $\lceil\log_2(N+1)\rceil$ bits, but this compresses the
repeated output record, not the original symbol, and does not remove the
zero-error obstruction.

### Corollary 5.3 (Finite-channel learnability is not security)

For $M$ input symbols, estimate each $q_x$ by $n$ independent samples. Then
Hoeffding's inequality and a union bound give

$$
\Pr\left\lbrace
\max_x|\widehat q_x-q_x|>\varepsilon
\right\rbrace
\le
2M\exp(-2n\varepsilon^2).
$$

For $M=256$ and $n=300$, this is
$512\exp(-600\varepsilon^2)$. Thus, under the conditional-iid model, a finite
lookup channel is query-learnable. Device specificity, analog complexity, or
phase sensitivity alone is not a cryptographic security proof. A security
claim needs a threat model, secret distribution, attack class, security game,
and quantitative advantage bound.

## 6. Semantic relation alignment

Suppose $C$ and $S$ are adjacency or association matrices for endorelations
on one source entity type and one target entity type. If one bijection
$\phi$ identifies the entities in both argument positions, with permutation
matrix convention $P_{\phi(i),i}=1$, exact alignment requires

$$
\boxed{S=PCP^{\mathsf T}}.
$$

Independent row and column permutations establish only

$$
S=PCQ^{\mathsf T},
$$

which permits an entity to acquire different identities in the two argument
positions.

### Proposition 6.1 (Independent alignment does not certify one identity)

There are square relations admitting a perfect independent row/column match
but no match by a single identity bijection.

#### Proof

Let $C=I$ and let $S=R$ be a nonidentity permutation matrix. Independent
choices $P=R$ and $Q=I$ give $S=PCQ^{\mathsf T}$. But

$$
PIP^{\mathsf T}=I
$$

for every permutation $P$, so no single-identity relation isomorphism exists.
$\square$

The exact or approximate single-identity problem

$$
\min_{P\in\Pi_n}\lVert S-PCP^{\mathsf T}\rVert_F
$$

is a graph-matching or quadratic-assignment problem in general, not an
ordinary linear assignment. Automorphisms can leave several optimal
permutations. Independent row/column maps remain valid for genuinely
different row and column entity types, but that bipartite typing must be
declared.

## 7. Dimensionless constants and the 1/137 boundary

The low-energy fine-structure constant is

```math
\alpha
=
\frac{e^2}{4\pi\varepsilon_0\hbar c},
\qquad
\alpha^{-1}\approx137.036.
```

It is a dimensionless electromagnetic coupling, not a generic channel
invariant. The 2022 CODATA recommended value is
$\alpha^{-1}=137.035\mkern3mu 999\mkern3mu 177(21)$.

### Proposition 7.1 (Channel form does not determine a coupling constant)

The operational report-envelope axioms do not determine $\alpha$, or any
other numerical coupling absent from their typed physical completion.

#### Proof

The operational-envelope axioms contain no equation fixing $\alpha$. They
admit typed physical completions with different coupling values and,
generally, different induced channels. Hence no universal numerical value
follows from the axioms alone. Noninjectivity over one fixed report envelope
would require a separately exhibited pair of operationally equivalent
completions and is not asserted here. $\square$

A derivation of $\alpha$ would need a dimensionless physical model, a map from
its parameters to a measured electromagnetic observable, renormalization-scale
and convention control, and a comparison with metrological data. Repetition
of the decimal 137, a graph degree, a spectral ratio, or a fitted scale is not
such a bridge.

## 8. BSC claim bindings

The central claim identifiers are:

| ID | Mathematical content | Boundary |
|---|---|---|
| BSC-CHN-01 | The contraction-weighted compatible fixed-interface bound of Theorem 2.1. | State/law error only; does not resolve BSC-QOP-03. |
| BSC-CHN-02 | Classical, quantum, measurement, and reporting data processing forbid downstream resurrection of lost distinguishability. | Exact decision still uses BSC-QUO-03. |
| BSC-CHN-03 | A uniform deterministic forward-report error gives the two enlarged identified-set containments of Proposition 3.3. | No inverse stability without additional regularity; sampling error is separate. |
| BSC-QPH-02 | Identical spectral intensities, even with unit overlap, need not imply close quantum states. | Relative phase and unmeasured modes remain completion variables. |
| BSC-ENE-01 | The driven open-system energy identity of Proposition 4.1. | Accounting under a declared split; no experiment-specific gain is inherited. |
| BSC-ENE-02 | A typed finite energy-port gluing has global residual $R_G=\sum_vr_v+\sum_eg_e$, with pointwise and integrated absolute bounds. | Additive storage and compatible same-clock ports are required; global closure does not certify local seams or full state gluing. |
| BSC-ENE-03 | Count yield, energy efficiency, and conditioned efficiency remain differently typed; compatible stage efficiencies telescope only across the identical intermediate extensive quantity. | Ratio algebra supplies no empirical efficiency, port completeness, or passivity. |
| BSC-ENC-01 | The Bernoulli count is sufficient and carries at most $\log_2(N+1)$ bits. | Conditional-iid scalar channel only. |
| BSC-ENC-02 | A 256-symbol scalar Bernoulli encoder has no finite $N$ zero-error decoder. | Does not preclude lossy or asymptotically reliable coding. |
| BSC-ENC-03 | A finite vector of Bernoulli biases is uniformly query-learnable under the declared sampling model. | Learnability is not a security analysis. |
| BSC-SEM-01 | A single entity identity requires conjugation $S=PCP^{\mathsf T}$; independent row/column fits are weaker. | Bipartite relations may legitimately use two maps. |
| BSC-UNI-01 | Operational channel form alone does not determine $\alpha$. | A typed electromagnetic completion remains necessary. |

## 9. Prior-art and novelty boundary

Statistical experiments and garblings, Dobrushin contraction, trace-distance
contractivity, POVM data processing, quantum networks, sufficient statistics,
Hoeffding bounds, graph matching, open-system energy accounting, and
boundary port-Hamiltonian theory are not BSC inventions. Relevant primary
references, separated by subject, include:

- G. Chiribella, G. M. D'Ariano, and P. Perinotti,
  [Theoretical framework for quantum networks](https://doi.org/10.1103/PhysRevA.80.022339),
  *Physical Review A* 80, 022339 (2009).
- R. L. Dobrushin,
  [Central limit theorem for nonstationary Markov chains I](https://doi.org/10.1137/1101006),
  *Theory of Probability and Its Applications* 1, 65--80 (1956).
- D. Perez-Garcia, M. M. Wolf, D. Petz, and M. B. Ruskai,
  [Contractivity of positive and trace-preserving maps under
  $`L_p`$ norms](https://doi.org/10.1063/1.2218675),
  *Journal of Mathematical Physics* 47, 083506 (2006).
- R. A. Fisher,
  [On the mathematical foundations of theoretical
  statistics](https://doi.org/10.1098/rsta.1922.0009),
  *Philosophical Transactions of the Royal Society A* 222, 309--368
  (1922).
- W. Hoeffding,
  [Probability inequalities for sums of bounded random
  variables](https://doi.org/10.1080/01621459.1963.10500830),
  *Journal of the American Statistical Association* 58, 13--30 (1963).
- R. Alicki,
  [The quantum open system as a model of the heat
  engine](https://doi.org/10.1088/0305-4470/12/5/007),
  *Journal of Physics A* 12, L103--L107 (1979).
- A. J. van der Schaft and B. M. Maschke,
  [Hamiltonian formulation of distributed-parameter systems with boundary
  energy flow](https://doi.org/10.1016/S0393-0440(01)00083-3),
  *Journal of Geometry and Physics* 42, 166--194 (2002).
- S. Sahni and T. Gonzalez,
  [P-complete approximation problems](https://doi.org/10.1145/321958.321975),
  *Journal of the ACM* 23, 555--565 (1976).
- P. J. Mohr, D. B. Newell, B. N. Taylor, and E. Tiesinga,
  [CODATA recommended values of the fundamental physical constants:
  2022](https://doi.org/10.1103/RevModPhys.97.025002),
  *Reviews of Modern Physics* 97, 025002 (2025).

The BSC claim is the claim-relative integration: the implemented
reachable-set obligation, mixed quantum/classical report boundary,
non-resurrection rule, evidence and control identity, bit-rate and semantic
alignment audits, and explicit refusal to infer a shared physical law from a
shared channel diagram.
