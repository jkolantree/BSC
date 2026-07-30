# Revision Memorandum

## Purpose

This memorandum records every material repair made while constructing and
auditing *On Boundaries of Evidence*, through version 1.0.1, plus the bounded
case-study integration in the unreleased 1.1.0-development draft. The latest
published version remains v1.0.1, dated 24 July 2026, with version DOI
`10.5281/zenodo.21541561`. It is separate from the manuscript so that the paper
can stand as a coherent formal work while the source lineage remains
inspectable. Repairs are classified as:

- **adopted correction:** a later authoritative corpus source explicitly
  corrects an earlier definition;
- **typing repair:** the inherited architecture is retained but domains,
  codomains, lifts, or namespaces are supplied;
- **demotion:** a theorem-like or physical statement is retained only as a
  definition, conditional schema, heuristic, analogy, conjecture, or open
  problem;
- **unresolved obligation:** no source or present proof closes the bridge.

No empirical claim in the supplied corpus was promoted. Reported executions in
the later arithmetic texts were not independently replayable because their
scripts and output artifacts were not among the supplied files.

Version 1.0.1 follows a fresh post-release audit. The immutable v1.0.0 record
is preserved. Its formal and release-engineering findings are listed in
`AUDIT_REPORT_v1.0.0.md`; this memorandum records their mathematical repair.

## 1. System-object lineage

### Source conflict

Volume I defines

$$
S_\ell(t)=
(\Omega_\ell,\partial_\varepsilon\Omega_\ell,X_\ell(t)/{\sim_\ell},
U_\ell(t),Y_\ell(t),H_\ell,G_\ell,V_\ell,R_\ell,K_\ell,B_\ell,
\operatorname{rent}_\ell).
$$

Volume II defines the measurable repair

$$
\widehat S_\ell=
(\Omega_\ell,\partial_\varepsilon\Omega_\ell,X_\ell,\sim_\ell,
U_\ell,Y_\ell,C_\ell,\mathcal F_\ell,K_\ell,H_\ell,G_\ell,V_\ell,R_\ell,
B_\ell).
$$

Volume III reproduces both and expressly states that it works with the second
object while retaining Volume I’s application layers. Volume V also inherits
the repaired tuple. A later Second Catalogue proposes another catalogue-local
canonical tuple that reorders fields and replaces $B_\ell$ by a broader
ledger.

### Repair

Both tuples are transcribed from the hash-identified supplied sources. The
Volume II tuple is treated as the current typed core because the supplied
lineage says it is adopted. Those internal sources are not redistributed, so
the transcription and lineage claim cannot be independently replayed from this
public release. The later Second Catalogue tuple is treated as a proposed
harmonization, not silently substituted.

### Slot changes recorded

1. $X_\ell/{\sim_\ell}$ is split into raw $X_\ell$ and exact
   $\sim_\ell$.
2. $C_\ell$ is typed as a structured physical configuration containing
   context, calibration, instrument, observer/reference frame, controller,
   and clock state.
3. Legal filtration $\mathcal F_{\ell,t}$ is added.
4. Tuple-level $\operatorname{rent}_\ell$ is removed and placed in the
   experiment/admission/certificate layer.
5. $R_\ell$ remains an inherited registry but is prohibited from acting as a
   single polymorphic arrow.
6. $B_\ell$ remains the boundary ledger; provenance is represented by a
   companion record instead of silently broadening the tuple.

### Added companion, not replacement

$$
\mathscr C_\ell=(D_\ell^{\mathrm{rec}},\mathsf{Prov}_\ell,\mathsf{Cert}_\ell)
$$

is associated with $\widehat S_\ell$. It supplies reconstruction data,
provenance, and certificate state required by the new manuscript without
changing the authoritative tuple.

## 2. “Finite domain”

### Conflict

The corpus uses continuous spatial and spacetime domains while sometimes
speaking as if “finite” meant finite cardinality.

### Repair

“Finite open system” is now parameterized by its intended finiteness:
bounded spatial domain, finite observation horizon, finite resources, or finite
state cardinality. These meanings may coexist but are never identified.

## 3. Boundary, layer, trace, response, and reconstruction

### Conflict

Earlier text sometimes used “boundary” for a geometric boundary, measured
finite layer, causal cut, interface, ideal trace, or response channel. This
allowed prediction from a sensor layer to be described as bulk reconstruction.

### Repair

Four distinct objects are required:

$$
\tau_\partial:\mathcal X(\Omega)\to\mathcal X_\partial(\partial\Omega),
$$

$$
L_\varepsilon:\mathcal X(\Omega)\to\mathcal Y_\varepsilon,
$$

$$
\Lambda_{a,\Omega}:f\mapsto\partial_{\nu,a}u_f|_{\partial\Omega},
$$

$$
E_\partial\subseteq\mathcal D\times(\mathcal A/{\approx}).
$$

Trace regularity, finite sensor resolution, the forward PDE, inverse
identifiability, gauge/diffeomorphism ambiguity, and stability are separate
obligations. A fifth symbol is introduced only when a representative is
actually chosen:

$$
e_\partial:\mathcal D_0\to\mathcal A\subseteq\mathcal X(\Omega).
$$

This is a measurable selected extension whose graph, after quotienting, lies
in $E_\partial$. Its codomain must remain in the admissible interior class.
Existence, representative invariance, linearity, and boundedness are separate
assumptions. The relation $E_\partial$ is never used as though it were a linear
operator.

### Incorrect noise direction

Volume II states that reconstruction noise contains a term “at least of order”
$\|E_\partial\|\sigma$. Only a selected bounded linear extension can have
such an operator norm, and it supplies

$$
\|e_\partial\eta\|\le\|e_\partial\|\,\|\eta\|,
$$

an upper worst-case amplification. A lower bound would require a minimum
singular value, a noise direction, or an adversarial supremum. The manuscript
uses only the valid upper bound.

### Boundary information screens

The earlier scalar “boundary gain minus exterior information” allowed a large
boundary term to compensate numerically for a still-open exterior channel. The
Second Catalogue explicitly repairs this. Version 1.0.0 nevertheless
overstated the resulting pair as a sufficiency gate. Version 1.0.1 retains two
noncompensating necessary screens:

$$
G_\partial\ge g_0,\qquad S_{\rm ext}^{\rm aug}\le s_0.
$$

They do not prove that the boundary is sufficient. A target-relative
sufficiency claim must additionally declare the relevant remainder and test

$$
S_{\rm rest}
=I(Y_{t+h};X_{{\rm rest},t}\mid X_{\partial,t},Z_t)
\le s_{\rm rest}.
$$

These are statistical target diagnostics, not causal claims or inverse-PDE
theorems.

## 4. Observation equivalence and approximate confusability

### Incorrect definition

Volume VI calls

$$
\sup_{u,c}d_P(H_E(x,u,c),H_E(x',u,c))\le\varepsilon
$$

an approximate equivalence. A thresholded metric relation is generally not
transitive and therefore generally does not define a quotient.

### Adopted correction

Following the Second Catalogue, the manuscript defines the confusability
pseudometric

$$
d_E(x,x')=\sup_{u,c}d_P(H_E(x,u,c),H_E(x',u,c))
$$

and treats its $\varepsilon$-sublevel sets as balls, graph neighborhoods, or
identified sets. Only exact equality of legal observation laws defines the
ordinary operational quotient.

The same repair is applied to quantum states. The notation
$\rho\sim_{\mathcal A_{\mathrm{acc}}}\sigma$ is reserved for zero accessible
probability defect. Positive-tolerance pairs satisfy
$d_{\mathcal A_{\mathrm{acc}}}(\rho,\sigma)\le\varepsilon$ and are called
confusable, not equivalent.

### Quotient descent hypothesis

The inherited quotient-descent theorem is made explicit: the quotient and
output are standard Borel, the quotient carries the final sigma-algebra, and
each coordinate $M(\cdot,A)$ is measurable through the quotient. Singular
quotients or stabilizer-sensitive problems require groupoid or invariant
algebra methods.

## 5. Experiment target and “executability”

### Undefined symbol

The Volume III target record

$$
\mathcal T=(Y,H,\tau,\mathcal F_t^{\mathrm{legal}})
$$

does not define $\tau$.

### Repair

The source record is quoted exactly before repair. The source text identifies
$H$ as the horizon, so the repair sets $h:=H$, declares a finite sampling
set $J_{t,h}\subset[t,t+h]$, and introduces

$$
q:(Y^{J_{t,h}},\mathcal B(Y)^{\otimes J_{t,h}})\to Z_q,
$$

and uses

$$
\mathcal T^{\mathrm{rep}}=(Y,h,q,\mathcal F_t^{\mathrm{legal}}).
$$

The observation channel $H^{\mathrm{obs}}$ remains in the system object and
is not duplicated in the target.

### Demotion

The corpus’s claim that a proposition is executable if and only if it can be
represented by an experiment bundle is too strong. A represented protocol may
lack data, resources, termination, safety, or a decidable admission procedure.
The manuscript treats bundle representation as the definition of
**BSC-specified**, not proof of practical executability.

## 6. Filtration and leakage

### Impossible condition

An earlier epistemic firewall required two sigma-algebras to have empty
intersection. Any two sigma-algebras contain at least the empty set and sample
space.

### Adopted correction

Version 1.0.1 fixes a probability space
$(\Xi_\ell,\mathscr A_\ell,\mathbb P_\ell)$, an increasing filtration
$(\mathscr F_{\ell,t})$, a standard Borel history space
$(\mathsf H_{\ell,t},\mathscr H_{\ell,t})$, and an
$\mathscr F_{\ell,t}/\mathscr H_{\ell,t}$-measurable variable
$\mathbf H_{\ell,t}$. A history policy is the kernel

$$
\pi_{\ell,t}:
(\mathsf H_{\ell,t},\mathscr H_{\ell,t})
\rightsquigarrow U_\ell\times C_\ell.
$$

The implemented law $\pi_{\ell,t}(\mathbf H_{\ell,t},\cdot)$ is adapted. With
this typing, the manuscript uses:

1. pre-outcome measurability of design, preprocessing, dictionary, nulls,
   thresholds, and seed policy;
2. conditional isolation diagnostics;
3. logged holdout access;
4. predictable sequential admission.

Positive conditional mutual information refutes isolation. Zero conditional
mutual information does not by itself prove the stronger measurability
condition.

## 7. Recursive fold

### Ill-typed inherited formula

The Volume I fold

$$
\Pi_{V_m}^{G_m}\circ R_{\ell m}\circ H_\ell\circ K_\ell
$$

does not compose as displayed: dynamics and observation both require controls
and context; observation outputs data; $R$ sometimes acts on data and
sometimes on states; projection expects a target state.

### Typing repair

The manuscript lifts dynamics and observation to compatible product spaces:

$$
\widetilde K_\ell:
\bar X_\ell\times U_\ell\times C_\ell
\rightsquigarrow
\bar X_\ell\times U_\ell\times C_\ell,
$$

$$
\widetilde H_\ell:
\bar X_\ell\times U_\ell\times C_\ell
\rightsquigarrow Y_\ell\times C_\ell.
$$

It separates:

- observation-to-state inference
  $\Pi\odot R_{\ell m}^{Y}\odot\widetilde H_\ell\odot\widetilde K_\ell$;
- direct state coarse-graining
  $\Pi\odot R_{\ell m}^{X}\odot\delta_{\pi_X}
  \odot\widetilde K_\ell$, where
  $\pi_X:\bar X_\ell\times U_\ell\times C_\ell\to\bar X_\ell$.

No generic arrow is permitted to change type mid-composition.

## 8. Morphism record and composition

### Extension

The requested record

$$
\mathfrak M_{\ell\to m}=
(T_{\ell m},T_{\ell m}^{\sharp},K_{\ell m},R_{\ell m},
\Theta_{\ell m},\delta_{\ell m},C_{\ell m},\mathsf{Cert}_{\ell m})
$$

is new. It extends the Volume I morphism and Volume II budgeted morphism. The
manuscript does not claim it was inherited unchanged.

For lineage, the Volume II record is transcribed from the supplied,
hash-identified internal source as

$$
\mu=(R_X,R_Y,R_U,R_C,\alpha_H,\alpha_K,q_{ab},b_\mu).
$$

Here $q_{ab}$ is quotient compatibility and $b_\mu$ is the distortion
budget. The older $\tau_R$ field is retained as unresolved typed material;
it is not retroactively described as a certificate.

### Observable direction

For a partial Markov state transport
$T_{\ell m}:D_{\ell m}\rightsquigarrow\bar X_m$,

$$
T_{\ell m}^{\sharp}:B_b(\bar X_m)\to B_b(D_{\ell m}),
\qquad
T_{\ell m}^{\sharp}g(x)=\int g(x')T_{\ell m}(x,dx').
$$

Thus observable transport is contravariant. Version 1.0.0 then wrote

$$
T_{\ell n}^{\sharp}
=T_{\ell m}^{\sharp}\circ T_{mn}^{\sharp}.
$$

For partial transports this is ill-typed: $T_{mn}^{\sharp}$ lands in
$B_b(D_{mn})$, outside the declared domain of $T_{\ell m}^{\sharp}$.
Version 1.0.1 defines

$$
D_{\ell n}
=\{x\in D_{\ell m}:T_{\ell m}(x,D_{mn})=1\}
$$

and the restricted pullback

$$
T_{\ell m}^{\sharp\mid D_{mn}}:
B_b(D_{mn})\to B_b(D_{\ell n}),\qquad
T_{\ell m}^{\sharp\mid D_{mn}}g(x)
=\int_{D_{mn}}g(y)T_{\ell m}(x,dy).
$$

The repaired law is

$$
T_{\ell n}^{\sharp}
=T_{\ell m}^{\sharp\mid D_{mn}}\circ T_{mn}^{\sharp}.
$$

Support makes this independent of the chosen full-space extension of $g$.
The unrestricted Markov pullback is positive and unital but not generally
multiplicative.
The extended morphism additionally requires

$$
T_{\ell m}^{\sharp}(\mathcal O_m)
\subseteq\mathcal O_\ell|_{D_{\ell m}},
$$

so transport of the maximal bounded-function space cannot stand in for
transport of the declared observable family.

### Original composition-bound error

Volume I prints

$$
\varepsilon_{ac}\le\varepsilon_{ab}+L_{bc}\varepsilon_{bc}.
$$

For the displayed observation comparison and an $L_{bc}$-Lipschitz
downstream map, insertion gives

$$
\varepsilon_{ac}\le\varepsilon_{bc}+L_{bc}\varepsilon_{ab}.
$$

The manuscript does not reproduce the erroneous ordering.

### Naturality defect

The observation square is fixed as

$$
H_m^{\mathrm{obs}}\odot\widehat T_{\ell m}
\quad\text{versus}\quad
K_{\ell m}\odot H_\ell^{\mathrm{obs}}.
$$

For total variation:

$$
\Theta_{\ell n}
\le\Theta_{mn}+\eta(K_{mn})\Theta_{\ell m},
$$

where $\eta(K_{mn})$ is the Dobrushin contraction coefficient. Unweighted
addition is used only as the weaker consequence $\eta\le1$.

### Implemented channel versus optimal deficiency

The channel stored in a morphism has tested error

$$
e_{\ell m}(K_{\ell m})=\sup_\theta
\|K_{\ell m}P_{\ell,\theta}-P_{m,\theta}\|_{\mathrm{TV}},
$$

whereas Le Cam deficiency is the infimum of this error over all admissible
Markov kernels. Thus
$e_{\ell m}(K_{\ell m})\ge\delta_{\ell m}$. A certificate must
state whether the stored channel attains the infimum or is merely a
near-minimizer.

### Equation residual

A target-equation residual cannot compose without an equation-space map.
For deterministic transports:

$$
R_{\ell m}(x)=
\mathcal E_m(T_{\ell m}x)-S_{\ell m}\mathcal E_\ell(x),
$$

$$
R_{\ell n}(x)=R_{mn}(T_{\ell m}x)+S_{mn}R_{\ell m}(x).
$$

The norm bound requires $S_{mn}$ bounded linear, compatible equation
domains, and a supremum restricted to
$T_{\ell m}(D_{\ell m})$. For nonlinear stochastic equations, a law-level
weak residual remains an open construction; no expectation is silently
substituted.

### Variant separation

Deterministic maps, partial maps, stochastic kernels, quantum channels,
correspondences, and fusion defects do not share one composition theorem.
Every morphism carries a variant tag. Correspondences require selection,
multiplicity, or probability semantics before an observable pullback exists.

### Physical completion

Controllers and carriers do not compose by naïve Cartesian product. The
manuscript requires interface, clock, resource, boundary-condition, and
correlated-failure compatibility. The composite completion is a specified
fiber product over the shared interface. Its completed joint transport is
typed as

$$
\widehat T_{\ell m}:\widehat D_{\ell m}\rightsquigarrow
\bar X_m\times U_m\times C_m,
$$

and composition requires the intermediate law to be supported on
$\widehat D_{mn}$. Otherwise the composite is undefined.

### Well formed, evaluated, and admissible for a claim

Version 1.0.0 used “admissible” too early, for a record that merely documented
the seven required questions. Version 1.0.1 separates three predicates. A
record is **well formed** when every field and type is supplied. It is
**evaluated for claim $c$** when every claim-required loss coordinate has a
proved typed enclosure

$$
I_{c,j}=[\underline L_{c,j},\overline L_{c,j}]\ni L_{c,j},
$$

every hard gate is evaluated, and critical obligations are resolved. It is
**admissible for $c$** only when each upper enclosure is within its typed
tolerance, every hard gate passes, and readiness meets the claim specification.
If an enclosure straddles a tolerance, the certificate fails but violation is
not established.

## 9. Le Cam and Blackwell direction

### Convention fixed

$$
\delta(\mathsf E_\ell,\mathsf E_m)
=\inf_{K:Y_\ell\rightsquigarrow Y_m}
\sup_\theta\|KP_{\ell,\theta}-P_{m,\theta}\|_{\mathrm{TV}}.
$$

Thus zero deficiency means observations from $\mathsf E_\ell$ can simulate
$\mathsf E_m$ arbitrarily accurately. Exact simulation additionally requires
an attained infimum or an applicable randomization theorem. The source
experiment is at least as informative in the corresponding approximate sense.
The symmetric distance, when used, is

$$
\Delta(\mathsf E,\mathsf F)
=\max\{\delta(\mathsf E,\mathsf F),\delta(\mathsf F,\mathsf E)\}.
$$

Directed deficiency is never called a distance.

Because the deficiency infimum need not be attained, the decision-risk
consequence is stated with $M(\delta+\eta)$ for every $\eta>0$; the sharper
$M\delta$ form is used only when an optimizing channel exists.

### Composition condition

The triangle inequality is used only for a common parameter family or after an
explicit pullback to one parameter space.

## 10. Recurrence and persistence

### Conflict

The later corpus defines endpoint recurrence by comparing the initial law to
the law after $n$ cycles. This allows the system to leave the identity or
viability tube and return.

### Repair

The manuscript distinguishes:

- **recurrence:** agreement at a specified endpoint;
- **persistence:** identity, viability, and certificate conditions at every
  required prefix.

For homogeneous identity error:

$$
E_n\le
\left(\prod_{j=0}^{n-1}L_j\right)E_0+
\sum_{i=0}^{n-1}e_i\prod_{j=i+1}^{n-1}L_j.
$$

Every prefix is tested. If the propagated upper bound is below tolerance it
certifies that prefix. If it lies above tolerance it is inconclusive: the
certificate is withdrawn, but the persistence claim is refuted only by an
exact evaluation, a valid lower bound, or a qualified measurement above
tolerance. Contraction after an established violation does not erase it.

The fold chain is also typed. A completed joint fold

$$
F_i:\bar X_i\times U_i\times C_i\rightsquigarrow\bar X_{i+1}
$$

and a certified state-Markov policy $\bar\pi_i$ induce a state kernel

$$
P_i(x,A)=\int F_i((x,u,c),A)\bar\pi_i(d(u,c)\mid x).
$$

History-dependent policies require state augmentation. The path law is
generated by the $P_i$, the ground identity space $(Q,d_Q)$ is Polish with
finite $p$-moments, recurrence uses $W_{p,Q}$, and

$$
\tau_V=\inf\{i\ge0:\mathbf X_i\notin V_i\}
$$

is the declared first-exit time. Cumulative exit tolerances and per-step union
bounds are not conflated.

### Non-scalar loss

Identity error, equation residual, naturality defect, deficiency, viability
failure probability, source status, and empirical status are not added into
one score. They retain independent tolerances and propagation rules.
Because stochastic and nonlinear residuals may be law-level records, the loss
vector now uses a typed scalar evaluator
$\mathsf{ev}_{\ell m}^{\mathrm{res}}$ on a declared residual test class.
The pointwise supremum norm appears only as the deterministic specialization.

## 11. Sheaf and “scale cohomology”

### Overclaim

The corpus used “scale torsion,” “scale curvature,” and at times “scale
cohomology” without a coefficient object, cochain groups, differential,
cocycle equation, coboundary action, or invariant obstruction class.

### Adopted correction

The later corpus itself demotes the language. The manuscript uses path defect,
naturality defect, or path curvature unless it explicitly constructs a
coefficient complex. Cohomology appears only in the parity fixture, where
$\mathbb Z_2$ coefficients, the 3-cycle, and the $H^1$ class are explicit.

### Sheaf scope

Compatible local sections glue because that is the axiom of an actual sheaf.
Locally nonempty relations and surjective overlap projections need not have a
global section. The distinction is tested by the exact parity fixture.

## 12. Open-system category

### Earlier schema

The corpus invoked a boundary-state category and compositionality while
assuming rather than constructing witness and coherence data.

### Conditional construction

The manuscript fixes:

1. the full subcategory of $\mathrm{Set}/\mathcal T$ on finite typed
   interfaces;
2. an internal carrier category with finite colimits;
3. a left-adjoint strong symmetric monoidal functor embedding interfaces as
   boundary carriers;
4. structured cospans;
5. one deterministic, stochastic, or nondeterministic mode and a declared time
   object per category;
6. a lax symmetric monoidal decoration functor
   $\mathcal D_{\mathsf r,\mathbb T}:(\mathsf C,+)\to
   (\mathrm{Set},\times)$;
7. an explicit pushout-decoration formula and unit decoration;
8. a blocked absorbing decoration for illegal unit, clock, boundary, or
   resource identifications.

This gives the generic decorated structured-cospan theorem under inspectable
hypotheses once $\mathcal D_{\mathsf r,\mathbb T}$ is supplied. It does not
prove that the eight-field BSC records canonically instantiate that functor.
Constructing the BSC-specific functor and proving its coherence remain open.
Mixed modes require a separate comparison functor, and stochastic
equality-gluing is unavailable unless the decoration functor supplies it; no
disintegration is inferred from a pushout.

## 13. Quantum reference frames and discard

### Missing operation

“Discard then transform” is undefined after discarding the frame unless a
reduced channel or replacement state is specified.

### Repair

The fixture now instantiates the finite group $G=\mathbb Z_2$. The frame
carries the left-regular action, the system carries $X^g$, and the
frame-trivialization transform is

$$
W=\sum_{g\in G}|g\rangle\langle g|\otimes X^g.
$$

The pulled target algebra is the simultaneous-action-invariant relational
algebra

$$
W^\dagger(I\otimes A)W
=\sum_g|g\rangle\langle g|\otimes X^gAX^g.
$$

Version 1.0.1 uses the simultaneous-action-invariant Bell states

$$
|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2,\qquad
|\Psi^+\rangle=(|01\rangle+|10\rangle)/\sqrt2.
$$

They have the same system marginal $I/2$, while $W$ maps them to
$|+\rangle|0\rangle$ and $|+\rangle|1\rangle$. Transform and frame discard
therefore give the orthogonal outputs $|0\rangle\langle0|$ and
$|1\rangle\langle1|$, with trace distance $1$. This proves nonfactorization
through the reduced quotient on the invariant state class. A
discard--reset--transform route gives $I/2$. The example is a finite-group QRF
fixture, not a universal QRF theorem.

## 14. Koopman learning and spectral pollution

### Scope repair

A small finite-dictionary residual is not automatically a global Koopman
eigenfunction certificate. Every claim must state dictionary, norm, sampling
law, time horizon, perturbation class, limiting order, and learnability class.

### Fixture correction

A one-sided shift was rejected because its spectral disk would not make zero a
polluted value. The manuscript uses the two-sided Bernoulli shift, whose
Koopman operator is unitary. Its finite unilateral compression has only the
spurious eigenvalue zero, while an explicit pseudomode has residual
$\sqrt{2/N}$.

### Impossibility scope

The cited impossibility results concern defined task classes, data access,
topologies, and dynamical-system classes. They do not establish that all
prediction or all learning is impossible.

## 15. Ordered scale limits

### Repair

Every micro-to-macro claim now requires the scale parameter, order of limits,
scaling, convergence topology, boundary conditions, time interval, uniformity
domain, effective parameters, error, and excluded regimes.

The manuscript adds a fully quantified periodic elliptic homogenization
theorem for a bounded Lipschitz domain, measurable symmetric periodic
uniformly elliptic coefficients, fixed $H^{-1}$ forcing, homogeneous
Dirichlet data, cell correctors, weak $H_0^1$ and flux convergence, and
strong $L^2$ convergence. No rate or changing-domain uniformity is claimed
under those hypotheses.

### Demotion

Homogenization is not treated as a universal micro-to-macro theorem. The
Deng–Hani–Ma hard-sphere/kinetic/fluid program is labeled as a preprint result
for its specified regimes, not as a settlement of every reading of Hilbert’s
sixth problem.

## 16. Topological charge and physical charge

### Bridge separation

$$
Q_{\mathrm{top}}=\langle[\omega],[C]\rangle,
\qquad
q_{\mathrm{phys}}=\chi(Q_{\mathrm{top}}).
$$

The first is a topological pairing. When a claim asserts that physical charge
is determined by it, the second requires a physically derived map with units
and normalization. This is an admission condition for that promotion, not a
definition of every physical charge.

### Hard obstruction

Winding in $\mathbb Z$ does not select a unique electric charge because every
$\chi_c(n)=cn$ is a homomorphism and topology selects no $c$, electric
unit, matter representation, or coupling. The torus fixture therefore stops
at homology.

### Comparison scope

Monopole–center-vortex confinement work is used as a stronger comparison
because it supplies a gauge theory, action, compactification, flux, fractional
topology, anomaly constraints, and string tension in controlled regimes. Its
passage to undeformed strongly coupled $\mathbb R^4$ and full hadron
spectroscopy is not promoted.

## 17. Klingman primordial-field treatment

### Preserved candidate structure

The papers are represented fairly as proposing:

- a self-interacting field;
- dual field components;
- toroidal configurations;
- complex or Kähler duality;
- closed paths and winding;
- stabilization by competing effects;
- a winding-to-charge proposal;
- a qualitative solenoidal confinement analogy in the 2025 paper, which
  explicitly leaves quantitative development open.

### Classification

> Candidate grammar: topological carrier and stabilization model.  
> Not established: a derivation of quark charge, QCD, or hadron dynamics.

### Unresolved bridge

The current sources do not supply the complete action and field space,
gauge-covariant current, boundary/regularity class, anomaly analysis, spin
representation, color structure, gauge-invariant confinement criterion,
running coupling, generation/mixing mechanism, hadron spectra, scattering
amplitudes, or independent falsifiers. The manuscript preserves the winding
and toroidal mathematics but blocks physical promotion.

## 18. Claim status and dependency propagation

### Version 1.0.0 defect and version 1.0.1 repair

Version 1.0.0 placed ill-posed, refuted, conjectural, conditional, and proved in
one ordered mathematical axis and propagated axiswise meets. That can
manufacture a false descendant verdict from a false indispensable predecessor.

Version 1.0.1 separates the categorical mathematical verdict

$$
v_{\rm math}\in\{\text{ill-posed},\text{open},\text{true},\text{false}\}
$$

from mathematical support and empirical, computational, source, and transfer
readiness. Dependency edges carry monotone cap maps on named readiness
coordinates. A false or ill-posed indispensable premise may withdraw support or
block transfer; it does not make a descendant false. Only descendant-level
evidence changes the descendant verdict.

### Mechanical verification

A mechanically verified claim requires a proof object accepted by a declared
kernel in a pinned environment. A blueprint, DAG, Lean source file, generated
prose, or repository link is not sufficient. A numerical claim requires actual
execution and a receipt. Hashes establish artifact identity, not validity.

## 19. Other corpus corrections retained in the audit record

The following repairs did not require long treatment in the main paper but
remain binding:

1. **Signed conservation residuals.** Earlier flux and Poynting checks used a
   signed numerator that could pass when strongly negative. A conservation
   identity must use a signed equality plus an absolute or interval-enclosed
   residual with a typed storage term.
2. **Action-specific quotient regret.** Volume VI later inserts an action into
   a quantity already minimized over actions. The Second Catalogue repairs it
   with classwise action regret $\sup_{x\in C}\operatorname{Reg}(a,x)$.
3. **First-person residual.** A mutual information expression treated kernels
   as random variables. Any future use must apply mutual information to
   declared outputs generated by those kernels.
4. **Noncommensurate composite scores.** Mechanism, grounding, reality-surplus,
   biological bridge, and durable-intelligence scores mix quantities without
   common units or a justified decision problem. They remain proposed
   diagnostics, not invariants or mechanisms.
5. **Nonabelian Čech obstruction.** A displayed ordinary
   $\check H^2(\mathcal U,G)$ was not justified for a general nonabelian
   structure group. Future use must restrict coefficients or construct the
   appropriate nonabelian cocycle/gerbe.
6. **Bad-event expectation.** A failure probability $\delta$ bounds expected
   contribution only with bounded loss or a tail-moment condition.
7. **Reported exact executions.** The arithmetic Markdown sources describe
   scripts, JSON, exact cases, and numerical reproductions, but those artifacts
   were not supplied. Their execution status remains source-asserted rather
   than independently replayed.
8. **Optical and physical predictions.** All optical, biofilm, cosmological,
   hardware, and quantum predictions in the corpus remain proposed and
   unexecuted unless a separate receipt and empirical source is supplied.

## 20. Unresolved highest-priority obligations

1. A BSC-specific lax symmetric monoidal decoration functor, with coherent
   pushout transport, instantiating the generic structured-cospan theorem.
2. A compositional weak residual for nonlinear stochastic equations.
3. Long-horizon perturbation theorems for prefix persistence.
4. Inverse-problem stability jointly accounting for finite sensor layers,
   calibration, geometry, and observation-kernel uncertainty.
5. Necessary and sufficient conditions for quantum-frame transformations to
   descend through subsystem quotients.
6. A learnability-aware Koopman recurrence certificate with honest ordered
   limits and finite-data stopping.
7. Any domain-specific, physically derived topology-to-charge map.
8. A pinned proof-assistant formalization and accepted build receipts for the
   finite core theorems.

These obligations are open by design. They are not defects that language can
repair; they require constructions, proofs, experiments, or counterexamples.

## 21. Normalized-scale framework promoted from the application

The first zeta–DQPT pass placed normalization collapse, logarithmic-rate
separation, singular loci, analytic zero transfer, and exact-zero
confusability almost entirely inside one application. That was mathematically
correct but architecturally incomplete: the reusable structure was not part
of BSC's general scale and observation calculus.

The 1.1.0-development framework now adds a certified scale-family record over
existing finite BSC systems and a normalized profile

$$
L_N=\frac{A_N}{Z_N},\qquad
\mathcal R_N=-\frac{\log|L_N|}{\lambda_N}.
$$

It proves:

1. bounded-carrier collapse under a diverging nonzero normalizer, while
   preserving each finite zero set;
2. the exact additive decomposition of the limiting rate into normalizer and
   carrier exponents;
3. covariance of the rate under multiplicative normalization changes, with
   singular-locus preservation only when the scaled logarithmic shift is
   continuous;
4. quantitative rate stability under amplitude perturbations relative to a
   positive lower amplitude margin, and the failure of a uniform bound as the
   margin closes;
5. identification of rate discontinuities with the boundary of a closed
   exceptional set under a continuous positive branch gap;
6. the inclusion of sliced singularities in the inverse image of the ambient
   singular set, with equality requiring visibility along the slice;
7. contour-certified holomorphic zero-count transfer and
   multiplicity-sensitive shrinking-circle transfer; and
8. deterministic and finite-label stochastic exact-decision criteria,
   including the binary total-variation testing bound.

The framework also adds a DQPT interpretation certificate. A mathematical
rate singularity is kept distinct from a finite-system Hamiltonian family,
physical volume normalization, real-time slice, infinite-system construction,
singularity class, estimator law, robustness statement, and implementation
evidence.

This is not a ninth morphism field and does not assert a universal phase
transition. The general profile is a directed comparison family of already
typed finite systems; it asserts no categorical identity or composition
coherence without an additional hypothesis.
The zeta functions, eta-tail constants, RH equivalence, and explicit root
drift remain application-specific.

The application also exposed a separate core obligation: the manuscript's
stochastic morphism composition theorem does not establish closure of the
full quantum variant. This is now recorded as open claim BSC-QOP-03; no
application may inherit the missing theorem.

## 22. Unreleased 1.1.0-development zeta–DQPT instance

### Source state observed

Wei et al., “The Riemann Hypothesis manifested in dynamical quantum phase
transitions,” *Nature Communications* (2026),
DOI `10.1038/s41467-026-74935-8`, was inspected as an unedited
article-in-press version. The source constructs quantum systems whose declared
finite observables encode alternating Dirichlet sums or a Riemann–Siegel-type
expression. It reports a five-qubit NMR proof of principle, polynomial-fit
locations where both measured coherence components approached zero and whose
first five $\beta_{\mathrm{eff}}=1/2$ values agree
with the first five known zero ordinates, and a
$\beta_{\mathrm{eff}}=0.3$ control with no discernible zeros. It also states a
resource comparison with direct Riemann–Siegel evaluation and uses
physical-origin language.

This memorandum records those statements as source claims. No raw-data replay,
fit re-execution, calibration audit, hardware execution, simulation replay, or
complexity benchmark has been performed in this repository.

### Mathematical boundary retained

For the declared finite logarithmic Hamiltonian, normalization, and alternating
phase operation, the case study proves

$$
Z_N(\beta_{\mathrm{eff}})\mathcal L_N(\beta_{\mathrm{eff}},t)
=-S_N(\beta_{\mathrm{eff}}+it).
$$

For $\sigma=\operatorname{Re}(s)>0$, Abel summation gives the explicit bound

$$
|\eta(s)-S_N(s)|
\le N^{-\sigma}\left(1+\frac{|s|}{\sigma}\right).
$$

Thus $S_N\to\eta$ locally uniformly on the half-plane
$\operatorname{Re}(s)>0$, where
$\eta(s)=(1-2^{1-s})\zeta(s)$. For fixed $s=\beta+it$ with
$0<\beta<1$, the Euler-transformed alternating tail and the asymptotic for
$Z_N$ give

$$
-\frac{\log|\mathcal L_N(s)|}{\log N}
\longrightarrow
\begin{cases}
1-\beta,&\eta(s)\ne0,\\
1,&\eta(s)=0.
\end{cases}
$$

The raw normalized coherence therefore tends to zero throughout the strip,
while its fixed-$s$ decay exponent separates the zero and nonzero branches.
For the source scaling $N=2^d$, this proves the pointwise rate formula

$$
\mathcal F_1(s)=
\begin{cases}
(1-\beta)\log 2,&\eta(s)\ne0,\\
\log 2,&\eta(s)=0.
\end{cases}
$$

The formula is pointwise at fixed $s$ and is not uniform near a zero; it is
not by itself a finite-size experimental certificate.
Its discontinuity set in the open strip is exactly the zeta-zero set: at a
zero $s_0=\beta_0+it_0$, the rate lies $\beta_0\log 2$ above the limiting
off-zero background. Thus confining every such discontinuity to
$\operatorname{Re}(s)=1/2$ is equivalent to RH. This is a representation
equivalence, not a proof or an unbounded census.
For every fixed $0<\beta<1$, the real-time slice $t\mapsto\beta+it$ sees
discontinuities exactly at the ordinates satisfying $\zeta(\beta+it)=0$,
with jump $\beta\log 2$. This equality uses visibility of both rate branches
along that slice; the general framework guarantees only inclusion without
such a hypothesis.
For a fixed zero $s_0=\beta_0+it_0$ of multiplicity $m$, Rouché's theorem on
a shrinking circle further gives exactly $m$ roots of $S_N$ within
$O(N^{-\beta_0/m})$. If the zero is simple, the unique root satisfies

$$
s_N-s_0=
\frac{(-1)^N(N+1)^{-s_0}}{2\eta'(s_0)}
+O_{s_0}\!\left(N^{-2\beta_0}\log N+N^{-\beta_0-1}\right).
$$

This is fixed-zero localization with constants depending on the isolation
neighborhood, not a uniform-in-height theorem or an experimental error bar.
More strongly, let $\Gamma$ be a declared Jordan contour in the critical
strip, and define

$$
\sigma_\Gamma=\min_\Gamma\operatorname{Re}(s),\qquad
M_\Gamma=\max_\Gamma|s|,\qquad
m_\Gamma=\min_\Gamma|\eta(s)|.
$$

If the whole-contour separation is certified and

$$
N^{-\sigma_\Gamma}
\left(1+\frac{M_\Gamma}{\sigma_\Gamma}\right)<m_\Gamma,
$$

then Rouché's theorem gives the same enclosed zero count for $S_N$ and
$\zeta$, with multiplicity. This is a bounded positive transfer, not a
uniform growing-$|t|$ result. A plot, point grid, or fitted minimum does not
supply the required contour lower enclosure, and no conclusion about the
unnormalized finite coherence is inherited.

### Demotions and unresolved bridges

The finite identity is engineered into the state, Hamiltonian, and measured
observable. It is a valid correspondence, but not independent evidence for
RH. An exact-zero query does not descend through a finite-resolution
observation class that contains both zero and nonzero amplitudes. A dynamical
phase transition is a nonanalyticity of a certified limiting rate function,
not merely a finite-size dip or fitted zero. Agreement with finitely many
previously known zero ordinates cannot discharge the universal quantifier over
all nontrivial zeros.

The quantum-advantage claim remains conditional on the complete precision,
state-preparation, success-probability, sampling, error-correction, input-size,
and comparator model. The inspected source compares its stated $|t|$ scaling
with direct Riemann–Siegel evaluation and also acknowledges faster classical
methods. No end-to-end best-classical advantage is certified here.

“Physical origin of RH” remains blocked until “origin” receives a typed causal
or ontological criterion and an independent generative bridge. An engineered
representation of $\zeta$ in observable dynamics does not by itself provide
that bridge and does not prove RH. Likewise,
$\beta_{\mathrm{eff}}$ is encoded in level populations. It is not the inverse
of the reported $305\,\mathrm K$ laboratory temperature without a separately
supplied energy-unit and calibration bridge.

### Release and fixture status

Development Fixture F9 records only the exact finite identity and the blocked
promotion boundary. It is an unexecuted documentary fixture, not an execution
of the application-level analytic theorems or an empirical receipt. The
development state has no assigned release date or DOI and does not modify the
immutable v1.0.1 release or its DOI.
