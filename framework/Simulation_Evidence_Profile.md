# Simulation evidence profiles

## Status and scope

This module is part of the released `1.2.0` framework. It was not part of the
immutable v1.1.0 release.

This module defines a reusable simulation-evidence profile for Boundary-State
Calculus (BSC). It refines the existing certificate, loss-vector, and
claim-relative admissibility machinery. It does not add a field to the
eight-field BSC morphism record, and it does not turn verification,
validation, or uncertainty quantification into one scalar score.

The profile is claim-relative. A model can be adequate for one intended use
and inadmissible or unevaluated for another. A mathematical proof, a numerical
execution, a calibration result, and an empirical validation result remain
different evidence objects with different transfer authority.

This module contains definitions, a proved deployment-admission theorem, a
coupled-surrogate corollary of the existing BSC prefix-error theorem, and an
exact fixture specification. Fixture F10 executes that specification with
exact rational arithmetic and retains a deterministic receipt.

## 1. Terminology

The word "simulation" has three different meanings in this module.

1. **Statistical simulation** is Blackwell or Le Cam simulation between
   statistical experiments. A Markov kernel post-processes observations from
   one experiment to approximate another. Its BSC quantities are directed
   deficiency and implemented-channel error.
2. **Computational simulation** is numerical execution of a mathematical
   model, such as a time integrator, finite-element solver, Monte Carlo
   calculation, or coupled multiphysics code. Its evidence includes model
   equations, discretization, code and solution verification, numerical error,
   execution identity, and quantities of interest.
3. **Surrogate deployment** replaces a component of a computational simulator
   with an approximation, learned operator, emulator, reduced model, or other
   fitted transport. Standalone surrogate accuracy does not by itself bound
   the error of the coupled host simulator.

No conclusion may move between these meanings merely because each is called
"simulation."

## 2. Claim-relative simulation-evidence profile

Let $c$ be a declared scientific or engineering claim. Its intended-use
record is

$$
\mathcal U_c
=
(D_c,H_c,Q_c,\pi_c,\mathsf{BC}_c,\mathsf{Units}_c,\tau_c).
$$

Here $D_c$ is the operating domain, $H_c$ is the time or iteration
horizon, $Q_c$ is the quantity of interest, $\pi_c$ is the intervention or
control policy, $\mathsf{BC}_c$ contains initial and boundary conditions,
$\mathsf{Units}_c$ types every numeric quantity, and $\tau_c$ supplies
claim-local tolerances.

### Definition 2.1 (Simulation-evidence profile)

For claim $c$ and evidence identity $\iota$, a simulation-evidence profile
is the record

$$
\mathsf{SEC}_{c,\iota}
=
\left(
\mathcal U_c,
I_c^{\ell},
J_c^{\ell},
J_c^{g},
\{\mathsf E_{c,i}\}_{i\in I_c^{\ell}},
\{g_{c,k}\}_{k\in J_c^{g}},
\Phi_c,
\boldsymbol\rho_c,
\mathsf{Prov}_{c,\iota}
\right).
$$

The fields have the following types.

- $I_c^{\ell}$ is the finite set of source evidence coordinates.
- $J_c^{\ell}$ is the finite set of applicable coordinates of the existing
  BSC loss vector used by the claim.
- $J_c^{g}$ is the finite set of Boolean hard gates used by the claim.
- $\mathsf E_{c,i}$ is the evidence record for source coordinate $i$.
- $g_{c,k}\in\{\mathsf{true},\mathsf{false},\mathsf{unevaluated}\}$ is a hard
  gate.
- For each $i\in I_c^\ell$, $(V_{c,i},\preceq_{c,i})$ is an ordered source
  value space with declared units. For each $j\in J_c^\ell$,
  $(W_{c,j},\le_{c,j})$ is the ordered value space and units of that BSC loss
  coordinate. Put

  $$
  \mathcal V_c=\prod_{i\in I_c^\ell}V_{c,i},
  \qquad
  \mathcal W_c=\prod_{j\in J_c^\ell}W_{c,j}.
  $$

- $\Phi_c:\mathcal V_c\to\mathcal W_c$ is a declared monotone,
  unit-respecting propagation map, with a proved relation

  $$
  \boldsymbol\ell_c^0
  \le_{\mathcal W_c}
  \Phi_c(\boldsymbol\eta_c)
  $$

  from the vector of source estimands $\boldsymbol\eta_c$ to the applicable
  frozen-state BSC loss vector $\boldsymbol\ell_c^0$.
- $\boldsymbol\rho_c$ is a certified compatibility reserve for transport
  in $\mathcal W_c$ from the frozen evaluation state to the declared
  deployment state.
- $\mathsf{Prov}_{c,\iota}$ is a content-addressed, claim-relevant provenance
  graph.

The profile refines a BSC certificate. It is not a new system object or a new
morphism variant.

### Numeric coordinates and hard gates

Candidate source evidence coordinates include:

- model-form discrepancy;
- numerical discretization and solver error;
- calibration and parameter-estimation error;
- validation error on a declared validation domain;
- surrogate interface error;
- operating-distribution or domain-shift loss;
- host-coupling error;
- clock or synchronization error;
- observation and estimator uncertainty.

Candidate hard gates include:

- code-verification status;
- solver-convergence or solution-verification status when a numeric enclosure
  is unavailable;
- presence and validity of an execution receipt;
- candidate, data, analysis, environment, and contract identity match;
- applicability of the validation domain to the intended-use domain;
- required physical, controller, clock, instrument, and boundary records.

This list is not universal. A coordinate or gate is included only when the
claim depends on it. Missing required evidence is represented as missing or
unevaluated, not as zero.

Different source coordinates need not share units. They may be transported
into the applicable BSC loss coordinates only through the typed propagation
map $\Phi_c$, an applicable norm inequality, or a claim-specific decision
rule. For example, seconds of clock error cannot be added directly to volts
of interface error.

## 3. Statistical evidence records

### Definition 3.1 (Statistical evidence record)

For a source evidence coordinate $i\in I_c^\ell$, define

$$
\mathsf E_{c,i}
=
\left(
\eta_{c,i},
d_{c,i},
\mathcal O_{c,i},
\widehat\eta_{c,i},
n_{c,i},
\alpha_{c,i},
[L^{\mathrm{src}}_{c,i},U^{\mathrm{src}}_{c,i}],
\varepsilon^{\mathrm{opt}}_{c,i},
\Psi_{c,i}
\right).
$$

The fields mean:

- $\eta_{c,i}$ is the source estimand.
- $d_{c,i}$ is the metric, norm, discrepancy, or loss defining the
  estimand.
- $\mathcal O_{c,i}$ is the observation model, including ordinary samples,
  paired samples, simulator queries, conditional samples, density access, or
  another oracle.
- $\widehat\eta_{c,i}$ is the estimator or deterministic evaluator.
- $n_{c,i}$ is the sample or query count and allocation.
- $\alpha_{c,i}$ is the declared coverage-failure probability.
- $[L^{\mathrm{src}}_{c,i},U^{\mathrm{src}}_{c,i}]$ is a confidence or
  pointwise deterministic enclosure in $V_{c,i}$.
- $\varepsilon^{\mathrm{opt}}_{c,i}$ is a certified optimization gap when
  the estimand contains an infimum, supremum, or fitted optimization.
- $\Psi_{c,i}$ is a proved proxy-transfer relation, or the explicit value
  "none."

A pointwise deterministic proof or interval enclosure may use
$\alpha_{c,i}=0$. Conversely, $\alpha_{c,i}=0$ states only an almost-sure
coverage claim under the declared law; it does not by itself prove that the
endpoint is deterministic. A finite-sample confidence interval is not
relabeled a deterministic enclosure.

### Definition 3.2 (Joint coverage)

All statistical records used together are defined on one declared joint
observation-and-analysis probability space
$(\Omega_c,\mathcal F_c,\mathbb P_c)$. Random interval endpoints are
$\mathcal F_c$-measurable. The profile records the joint source event

$$
\mathcal C_c^{\mathrm{src}}
=
\bigcap_{i\in I_c^{\ell}}
\left\{
\eta_{c,i}\in
[L^{\mathrm{src}}_{c,i},U^{\mathrm{src}}_{c,i}]
\right\}
$$

and a justified bound

$$
\mathbb P_c(\mathcal C_c^{\mathrm{src}})\ge 1-\alpha_c.
$$

Marginal coverage statements do not automatically establish joint coverage.
Without a stronger dependence argument, the union-bound justification
requires every marginal guarantee

$$
\mathbb P_c\!\left(
\eta_{c,i}\notin
[L^{\mathrm{src}}_{c,i},U^{\mathrm{src}}_{c,i}]
\right)
\le \alpha_{c,i}
\quad(i\in I_c^\ell)
$$

and

$$
\sum_{i\in I_c^{\ell}}\alpha_{c,i}\le\alpha_c.
$$

Any data-dependent choice of coordinates, thresholds, operating regions,
proxies, or estimators is included in the coverage analysis or frozen before
evaluation.

Put

$$
\boldsymbol U_c^{\mathrm{src}}
=
(U^{\mathrm{src}}_{c,i})_{i\in I_c^\ell},
\qquad
\boldsymbol U_c^0
=
\Phi_c(\boldsymbol U_c^{\mathrm{src}})
=
(U^0_{c,j})_{j\in J_c^\ell}.
$$

On $\mathcal C_c^{\mathrm{src}}$, monotonicity and the proved propagation
relation give the typed target-coordinate enclosure

$$
\boldsymbol\ell_c^0
\le_{\mathcal W_c}
\Phi_c(\boldsymbol\eta_c)
\le_{\mathcal W_c}
\boldsymbol U_c^0.
$$

### Statistical deficiency is not implemented-channel error

For experiments
$\mathsf E=\{P_\theta:\theta\in\Theta\}$ and
$\mathsf F=\{Q_\theta:\theta\in\Theta\}$, directed total-variation
deficiency is

$$
\delta(\mathsf E,\mathsf F)
=
\inf_K\sup_{\theta\in\Theta}
\lVert KP_\theta-Q_\theta\rVert_{\mathrm{TV}}.
$$

For one implemented channel $K_0$, its error is

$$
e(K_0)
=
\sup_{\theta\in\Theta}
\lVert K_0P_\theta-Q_\theta\rVert_{\mathrm{TV}},
$$

and therefore

$$
\delta(\mathsf E,\mathsf F)\le e(K_0).
$$

A confidence upper bound on $e(K_0)$ is an upper bound on deficiency. It
does not show that $K_0$ is optimal or that the deficiency is close to that
upper bound. Claiming a numerical enclosure for deficiency itself requires an
optimization-gap certificate or another theorem controlling the infimum.
A lower bound on deficiency requires a separate witness, dual bound,
randomization obstruction, or applicable impossibility theorem.

### Definition 3.3 (Proxy-transfer certificate)

Suppose a tractable proxy $p(P,Q)$ is used in place of the target
discrepancy $d(P,Q)$. A proxy-transfer certificate is a proved, hypothesis
checked inequality

$$
d(P,Q)\le \psi(p(P,Q),\eta)
$$

on the declared model class, where $\psi$ is monotone in the proxy argument
and $\eta$ records all auxiliary constants and assumptions.

If the profile establishes $p(P,Q)\le U_p$, then it may conclude only

$$
d(P,Q)\le\psi(U_p,\eta).
$$

Without such a theorem, the proxy has no authority for the target
discrepancy.

For example, let $P=\delta_0$ and $Q=\delta_\epsilon$ on
$\mathbb R$, with $\epsilon>0$. Then

$$
W_1(P,Q)=\epsilon
\quad\text{while}\quad
d_{\mathrm{TV}}(P,Q)=1.
$$

Thus small Wasserstein distance, small pointwise error, or small RMSE does not
by itself imply small total variation. The same caution applies to MMD or a
learned discriminator unless a valid transfer theorem is supplied.

The obstruction persists at the experiment level. Let
$\Theta=\{-1,+1\}$,

$$
P_{-1}=P_{+1}=\delta_0,
\qquad
Q_{-1}=\delta_{-\epsilon},
\qquad
Q_{+1}=\delta_{+\epsilon}.
$$

The corresponding laws have
$\sup_\theta W_1(P_\theta,Q_\theta)=\epsilon$. But every channel applied to
the source experiment produces the same law $R$ for both parameter values,
and the total-variation triangle inequality gives

$$
\max_{\theta\in\Theta}
\lVert R-Q_\theta\rVert_{\mathrm{TV}}
\ge\frac12.
$$

The equal mixture
$R=(\delta_{-\epsilon}+\delta_{+\epsilon})/2$ attains this bound, so

$$
\delta(\mathsf E,\mathsf F)=\frac12.
$$

Hence even uniformly small corresponding-law Wasserstein error does not imply
small directed total-variation deficiency.

## 4. Compatibility-bounded deployment

Let $\ell^0_{c,j}$ be the loss coordinate for the frozen evaluation identity
and $\ell^1_{c,j}$ the corresponding coordinate in the proposed deployment
state.

### Definition 4.1 (Compatibility reserve)

A compatibility reserve $\rho_{c,j}\ge0$ is valid only when a proof,
qualified measurement, or confidence-qualified compatibility certificate
establishes

$$
\ell^1_{c,j}
\le
\ell^0_{c,j}+\rho_{c,j}
$$

in common units on the declared operating domain and horizon.

The reserve is not unused tolerance chosen by preference. It is an enclosure
of the additional loss introduced by the declared change. Frozen-state
estimator uncertainty already represented in $U^0_{c,j}$ is not counted
again in $\rho_{c,j}$. Uncertainty in estimating the deployment change must
be represented exactly once: either inside the compatibility reserve on the
joint event or as a separate source coordinate propagated into that reserve,
but not both.

For coordinates that do not admit an additive comparison, the profile uses
the declared monotone propagation map $\Phi_c$ instead. The additive theorem
below applies after quantities have been transported into a common loss
coordinate.

### Theorem 4.2 (Compatibility-bounded deployment admission)

Assume:

1. the frozen and deployment profiles are well formed for claim $c$, with
   the declared intended use and evidence identities bound;
2. on a joint event $\mathcal C_c^{\mathrm{dep}}$ with
   $\Pr(\mathcal C_c^{\mathrm{dep}})\ge1-\alpha_c$,

   $$
   \ell^0_{c,j}\le U^0_{c,j}
   \quad\text{and}\quad
   \ell^1_{c,j}\le\ell^0_{c,j}+\rho_{c,j}
   $$

   for every $j\in J_c^\ell$;
3. every required deployment gate is certified true;
4. every required readiness coordinate transfers or is freshly established;
5. for every numeric coordinate,

   $$
   U^0_{c,j}+\rho_{c,j}\le\tau_{c,j}.
   $$

Then the deployment profile is admissible for $c$ on
$\mathcal C_c^{\mathrm{dep}}$, an event with probability at least
$1-\alpha_c$. It is a deterministic admission statement only when the
enclosures and compatibility inequalities hold pointwise, independently of
$\omega\in\Omega_c$ (in particular, on a singleton probability space).
Merely setting $\alpha_c=0$ establishes probability-one admission, not
determinism.

#### Proof

On $\mathcal C_c^{\mathrm{dep}}$, for each $j$,

$$
\ell^1_{c,j}
\le
\ell^0_{c,j}+\rho_{c,j}
\le
U^0_{c,j}+\rho_{c,j}
\le
\tau_{c,j}.
$$

Every coordinate of the existing BSC loss vector is nonnegative. Therefore,
on the same event,

$$
I^1_{c,j}
=
[0,U^0_{c,j}+\rho_{c,j}]
$$

is a proved deployment enclosure containing $\ell^1_{c,j}$, so the
deployment profile is evaluated for $c$. The well-formedness, gate, and
readiness hypotheses discharge the remaining claim-relative admissibility
conditions. The joint event has probability at least $1-\alpha_c$, which
gives the stated qualification. Pointwise hypotheses remove dependence on
the event and give the deterministic specialization. $\square$

### Reserve and equality

Define the remaining deployment slack

$$
s_{c,j}
=
\tau_{c,j}-(U^0_{c,j}+\rho_{c,j}).
$$

- $s_{c,j}>0$ certifies tolerance to additional loss up to that amount in
  the same coordinate and under the same gates.
- $s_{c,j}=0$ satisfies the displayed admission inequality but has zero
  certified reserve for any additional positive loss.
- $s_{c,j}<0$ fails to certify deployment admission.

An upper bound above tolerance is not by itself evidence that the actual loss
violates tolerance. A violation requires an exact value, a certified lower
bound above tolerance, or a qualified measurement establishing it.

## 5. Factored evidence identity

### Definition 5.1 (Factored identity)

The evidence identity is

$$
\iota
=
(\iota_{\mathrm{cand}},
  \iota_{\mathrm{data}},
  \iota_{\mathrm{analysis}},
  \iota_{\mathrm{env}},
  \iota_{\mathrm{contract}}).
$$

The factors identify:

- candidate model, simulator, solver, surrogate, and configuration;
- training, calibration, validation, and reference data;
- analysis code, estimator, optimization, random seeds, and report schema;
- libraries, runtime, hardware, services, clocks, and relevant environment;
- intended use, claim, thresholds, metrics, gates, and evaluation policy.

Each factor is the root of a canonical claim-relevant dependency graph. A
repository-wide hash is neither necessary nor sufficient: it can change for
irrelevant prose while omitting an external library or service that changes
the execution.

### Exact transfer rule

Artifact-specific proof or execution evidence transfers exactly when:

1. every identity factor on which that evidence depends is equal;
2. the claim and intended-use record are equal;
3. the evidence verifier validates the same immutable object.

An old receipt remains valid historical evidence for its old identity. A new
analysis run creates a new evidence object rather than overwriting it.

### Compatible transfer rule

When $\iota\ne\iota'$, prior evidence transfers only if one of the following
holds.

1. The evidence is a theorem quantified over a declared class, and a fresh
   applicability proof establishes that both identities lie in the theorem's
   class.
2. A compatibility morphism from $\iota$ to $\iota'$ declares its domain,
   target, changed dependencies, loss propagation, reserve
   $\boldsymbol\rho_c$, gates, and proof or execution receipt. The deployment
   theorem in Section 4 then discharges or blocks the target claim.

In particular,

$$
\mathsf{ExecCert}(c,\iota)
\ \land\
\iota'\ne\iota
\quad\not\Rightarrow\quad
\mathsf{ExecCert}(c,\iota').
$$

The inequality of identities does not prove the new candidate wrong. It
blocks direct inheritance of identity-bound evidence until exact or compatible
transfer is established.

## 6. Coupled-surrogate propagation

Let $(X,d)$ be a metric state space, let $D\subseteq X$ be the certified
operating domain, and define the reference and surrogate-coupled host maps

$$
\Phi_k(x)=F_k(x,g_k(x)),
\qquad
\widehat\Phi_k(x)=F_k(x,\widehat g_k(x)).
$$

Assume both trajectories remain in $D$ through the declared horizon.

### Corollary 6.1 (Finite-horizon coupled-surrogate bound)

Suppose, for all relevant $x,y\in D$,

$$
d(\Phi_k(x),\Phi_k(y))\le L_k d(x,y)
$$

and

$$
d(\widehat\Phi_k(x),\Phi_k(x))\le b_k,
$$

where $L_k,b_k\ge0$ are certified. If

$$
x_{k+1}=\Phi_k(x_k),
\qquad
\widehat x_{k+1}=\widehat\Phi_k(\widehat x_k),
\qquad
E_k=d(\widehat x_k,x_k),
$$

then

$$
E_n
\le
\left(\prod_{j=0}^{n-1}L_j\right)E_0
+
\sum_{i=0}^{n-1}
b_i\prod_{j=i+1}^{n-1}L_j.
$$

#### Proof

The triangle inequality gives

$$
\begin{aligned}
E_{k+1}
&=
d(\widehat\Phi_k(\widehat x_k),\Phi_k(x_k))\\
&\le
d(\widehat\Phi_k(\widehat x_k),\Phi_k(\widehat x_k))
+
d(\Phi_k(\widehat x_k),\Phi_k(x_k))\\
&\le b_k+L_kE_k.
\end{aligned}
$$

Apply the existing BSC prefix-error theorem to this recurrence. $\square$

A useful certified decomposition is

$$
b_k
\le
G_k\epsilon_k+\nu_k+\chi_k,
$$

where $\epsilon_k$ is a surrogate interface-error enclosure on the reachable
domain, $G_k$ is host sensitivity to that interface, $\nu_k$ is numerical
error, and $\chi_k$ is a coupling or clock defect, all transported into the
state-error coordinate.

Average standalone RMSE does not supply the uniform $b_k$ hypothesis. The
profile must either certify a reachable-domain bound or prove a
distribution-to-trajectory transfer with its own coverage and shift
assumptions.

## 7. Exact stable-host fixture F10

Fixture F10 uses exact rational arithmetic in two stable hosts. Its verifier,
schema, retained receipt, and negative mutants are in
`fixtures/F10_coupled_surrogate/`.

### Reference and surrogate components

Let the reference and surrogate component outputs be

$$
g(x)=0,
\qquad
\widehat g(x)=\frac{1}{100}.
$$

The standalone surrogate interface error is exactly

$$
\sup_x|\widehat g(x)-g(x)|=\frac{1}{100}
$$

in every fixture case.

### Stable hosts

For host parameter $a_h$, define the exact reference and surrogate-coupled
recurrences

$$
x_{k+1}^{(h)}=a_hx_k^{(h)}+g(x_k^{(h)}),
\qquad
\widehat x_{k+1}^{(h)}
=a_h\widehat x_k^{(h)}+\widehat g(\widehat x_k^{(h)}),
$$

with $x_0^{(h)}=\widehat x_0^{(h)}=0$. The reference trajectory is zero.
Because every error is nonnegative,

$$
E_{k+1}^{(h)}
=a_hE_k^{(h)}+\frac1{100},
\qquad
E_k^{(h)}
=\frac1{100}\sum_{r=0}^{k-1}a_h^r.
$$

Both fixture hosts satisfy $0\le a_h<1$, and their errors increase with $k$.
Thus the endpoint error equals the maximum prefix error through the declared
horizon.

Use horizon $H=10$ and common tolerance

$$
\tau=\frac{1}{20}.
$$

The two exact cases are:

| Host | $a_h$ | $E_{10}^{(h)}$ | First violation | Exact tolerance disposition |
|---|---:|---:|---:|---|
| A | $1/2$ | $1023/51200$ | none | within tolerance |
| B | $9/10$ | $6513215599/100000000000$ | $k=7$ | tolerance violated |

Host A and Host B isolate dynamic amplification at fixed standalone error,
horizon, initial state, and tolerance. Host B also supplies a horizon
contrast internally: its prefix through $k=6$ remains within tolerance, while
its exact error first exceeds tolerance at $k=7$. Both conclusions use exact
actual errors rather than an upper enclosure above tolerance. This is one
numeric loss-coordinate disposition; it is not by itself full BSC
claim-relative admissibility, which also requires every applicable gate,
coordinate, and readiness condition.

### Required receipt fields

The fixture input and receipt must bind:

- claim and fixture identifiers;
- exact rational reference and surrogate definitions;
- exact rational host recurrence;
- host recurrence parameter, horizon, initial condition, and tolerance;
- every exact reference and surrogate trajectory value;
- endpoint and maximum-prefix errors;
- expected disposition and the comparison that establishes it;
- candidate, data, analysis, environment, and contract identity mappings,
  with a typed not-applicable value where the exact data-free fixture has no
  data identity;
- verifier, generator, schema, fixture-input, environment, and host hashes;
- runtime identity and deterministic serialization rules.

The receipt does not contain its own hash. The repository manifest binds the
final retained receipt bytes externally, avoiding an impossible self-hash
requirement.

The verifier must independently recompute the rational trajectories and refuse
to overwrite the retained receipt. Required negative mutants include:

- a stale host or contract hash;
- a changed horizon with an unchanged recorded error;
- an incorrect within-tolerance disposition for Host B;
- a decimal approximation substituted for an exact rational field.

This fixture falsifies the universal statement:

> Equal standalone surrogate error entails equal coupled-host tolerance
> disposition.

It does not establish accuracy for an untested simulator, operating region,
coupling, horizon, or physical system.

## 8. Prior-art boundary

The narrow BSC contribution is the integration of claim-local typed losses,
hard gates, statistical evidence records, factored identity, compatibility
reserves, and admissibility propagation in one inspectable profile. The
following subjects are prior art and must not be claimed as original BSC
discoveries.

- [NASA-STD-7009B, Standard for Models and Simulations](https://standards.nasa.gov/standard/nasa/nasa-std-7009)
  supplies lifecycle modeling-and-simulation credibility requirements,
  acceptance criteria, verification, validation, uncertainty, and
  intended-use discipline.
- [NASA-HDBK-7009B, implementation guide](https://standards.nasa.gov/standard/nasa/nasa-hdbk-7009)
  supplies detailed credibility-assessment and reuse guidance.
- [Jakeman, Barba, Martins, and O'Leary-Roseberry (2025)](https://arxiv.org/abs/2502.15496)
  develops verification and validation guidance for trustworthy scientific
  machine learning, including code and solution verification, calibration,
  validation, application domains, uncertainty, data provenance, and
  distribution shift.
- [Ellinas, Chaudhuri, Vorwerk, and Chatzivasileiadis (2026)](https://arxiv.org/abs/2603.17836)
  studies surrogate components inside a host dynamic simulator and derives a
  finite-horizon relation involving interface error, coupling sensitivity,
  dynamic amplification, and horizon.
- [ECMWF (2026), Farewell to external AI models](https://www.ecmwf.int/en/about/media-centre/aifs-blog/2026/farewell-external-ai-models)
  reports an operational example in which upstream-system changes affected
  external machine-learning forecast workflows.
- [Meel, Kumar, and Pote (2025)](https://proceedings.mlr.press/v258/meel25a.html)
  records exponential standard-sampling lower bounds for high-dimensional
  distribution-distance estimation and gives a polynomial-query result under
  a stronger conditional-sampling oracle.

Accordingly, BSC may claim a typed integration and executable falsification
contract. It must not claim to have invented verification and validation,
deployment headroom, finite-horizon surrogate amplification, continuous
credibility, or the sample-complexity limits of statistical-distance
estimation.

## 9. Scope and stopping rules

A simulation-evidence profile does not by itself prove:

- that the mathematical model represents external reality;
- that a code-verification result validates the model form;
- that calibration data are independent validation data;
- that a small equation residual gives a small trajectory error;
- that average standalone surrogate accuracy controls a coupled host;
- that one implemented statistical channel attains deficiency;
- that one proxy metric controls another;
- that confidence-qualified evidence is a deterministic proof;
- that an old receipt executes a changed candidate;
- that admission for one intended use transfers to another.

When any required type, enclosure, gate, identity factor, proxy theorem,
operating-domain condition, or compatibility bound is missing, the affected
claim is unevaluated or not certified. It is not assigned a convenient small
error.
