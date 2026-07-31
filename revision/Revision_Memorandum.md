# Revision Memorandum

## Purpose

This memorandum records every material repair made while constructing and
auditing *On Boundaries of Evidence* through published version 1.4.0, dated
31 July 2026, with immutable GitHub release record
`https://github.com/jkolantree/BSC/releases/tag/v1.4.0` and Zenodo concept DOI
`10.5281/zenodo.21541160`. The v1.4.0 version DOI assigned after the tagged
bytes were built is recorded on the GitHub release page. The immutable
v1.3.0 version DOI is `10.5281/zenodo.21713285`; the immutable v1.2.0 version
DOI is `10.5281/zenodo.21711341`; the immutable v1.1.0 version DOI is
`10.5281/zenodo.21710743`; the immutable v1.0.1 version DOI remains
`10.5281/zenodo.21541561`. This memorandum is separate from the manuscript
so that the paper can stand as a coherent formal work while the source lineage
remains inspectable. Repairs are classified as:

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
\mathrm{rent}_\ell).
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
4. Tuple-level $\mathrm{rent}_\ell$ is removed and placed in the
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
$\lVert E_\partial\rVert\sigma$. Only a selected bounded linear extension can have
such an operator norm, and it supplies

$$
\lVert e_\partial\eta\rVert\le\lVert e_\partial\rVert\mkern3mu \lVert \eta\rVert,
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
  $\Pi\odot R_{\ell m}^{X}\odot\delta_{\pi_X}\odot\widetilde K_\ell$, where
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
=\lbrace x\in D_{\ell m}:T_{\ell m}(x,D_{mn})=1\rbrace
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
\lVert K_{\ell m}P_{\ell,\theta}-P_{m,\theta}\rVert_{\mathrm{TV}},
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
\sup_\theta\lVert KP_{\ell,\theta}-P_{m,\theta}\rVert_{\mathrm{TV}}.
$$

Thus zero deficiency means observations from $\mathsf E_\ell$ can simulate
$\mathsf E_m$ arbitrarily accurately. Exact simulation additionally requires
an attained infimum or an applicable randomization theorem. The source
experiment is at least as informative in the corresponding approximate sense.
The symmetric distance, when used, is

$$
\Delta(\mathsf E,\mathsf F)
=\max\lbrace\delta(\mathsf E,\mathsf F),\delta(\mathsf F,\mathsf E)\rbrace.
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
\tau_V=\inf\lbrace i\ge0:\mathbf X_i\notin V_i\rbrace
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
   $\mathcal D_{\mathsf r,\mathbb T}:(\mathsf C,+)\to(\mathrm{Set},\times)$;
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
v_{\rm math}\in\lbrace\text{ill-posed},\text{open},\text{true},\text{false}\rbrace
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
   with classwise action regret $\sup_{x\in C}\mathrm{Reg}(a,x)$.
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

Version 1.1.0 adds a certified scale-family record over
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

## 22. Version 1.1.0 zeta–DQPT instance

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

For $\sigma=\mathrm{Re}(s)>0$, Abel summation gives the explicit bound

$$
|\eta(s)-S_N(s)|
\le N^{-\sigma}\left(1+\frac{|s|}{\sigma}\right).
$$

Thus $S_N\to\eta$ locally uniformly on the half-plane
$\mathrm{Re}(s)>0$, where
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
while its fixed $s$ decay exponent separates the zero and nonzero branches.
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
$\mathrm{Re}(s)=1/2$ is equivalent to RH. This is a representation
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
+O_{s_0}\mkern-3mu \left(N^{-2\beta_0}\log N+N^{-\beta_0-1}\right).
$$

This is fixed-zero localization with constants depending on the isolation
neighborhood, not a uniform-in-height theorem or an experimental error bar.
More strongly, let $\Gamma$ be a declared Jordan contour in the critical
strip, and define

$$
\sigma_\Gamma=\min_\Gamma\mathrm{Re}(s),\qquad
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
uniform growing $|t|$ result. A plot, point grid, or fitted minimum does not
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
of the reported $305\mkern3mu \mathrm K$ laboratory temperature without a separately
supplied energy-unit and calibration bridge.

### Release and fixture status

Fixture F9 records only the exact finite identity and the blocked
promotion boundary. It is an unexecuted documentary fixture, not an execution
of the application-level analytic theorems or an empirical receipt. Version
1.1.0 was released on 30 July 2026 and does not modify the immutable v1.0.1
release or its DOI.

## 23. Version 1.2.0 simulation-evidence refinement

### Architectural gap

The released framework already separates proofs, execution receipts,
provenance, typed loss coordinates, hard gates, and claim-relative
admissibility. It did not yet provide one reusable record for evidence about a
computational model or for transferring that evidence when a previously
evaluated component is deployed inside a changed host. In particular, the
shared word "simulation" could obscure three different constructions:

1. statistical simulation of one experiment from another by a Markov kernel;
2. numerical execution of a mathematical model; and
3. deployment of a learned or reduced surrogate inside a computational host.

The version 1.2.0 repair keeps these meanings distinct and adds no field to the
eight-field BSC morphism record.

### Claim-relative profile

For a claim $c$, the released framework declares the intended-use record

```math
\mathcal U_c
=
(D_c,H_c,Q_c,\pi_c,\mathsf{BC}_c,\mathsf{Units}_c,\tau_c)
```

and the simulation-evidence profile

```math
\mathsf{SEC}_{c,\iota}
=
\left(
\mathcal U_c,
I_c^\ell,
J_c^\ell,
J_c^g,
\lbrace\mathsf E_{c,i}\rbrace_{i\in I_c^\ell},
\lbrace g_{c,k}\rbrace_{k\in J_c^g},
\Phi_c,
\boldsymbol\rho_c,
\mathsf{Prov}_{c,\iota}
\right).
```

The source index $I_c^\ell$ and target index $J_c^\ell$ are deliberately
different. For $i\in I_c^\ell$, the evidence record is

```math
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
```

Thus $\eta_{c,i}$ and
$`[L^{\mathrm{src}}_{c,i},U^{\mathrm{src}}_{c,i}]`$ belong to a typed source
evidence space. The applicable coordinates of the existing BSC loss vector
are indexed by $j\in J_c^\ell$. They are connected only by a proved monotone,
unit-respecting propagation relation

$$
\boldsymbol\ell_c^0
\le_{\mathcal W_c}
\Phi_c(\boldsymbol\eta_c).
$$

Writing

```math
\boldsymbol U_c^0
=
\Phi_c(\boldsymbol U_c^{\mathrm{src}})
=
(U^0_{c,j})_{j\in J_c^\ell}
```

therefore produces frozen-state target-loss bounds; it does not relabel the
source intervals as BSC losses. Numeric coordinates and Boolean hard gates
remain noncompensating.

All statistical records used together live on one declared joint
observation-and-analysis probability space
$(\Omega_c,\mathcal F_c,\mathbb P_c)$. Their source coverage event is

```math
\mathcal C_c^{\mathrm{src}}
=
\bigcap_{i\in I_c^\ell}
\left\lbrace
\eta_{c,i}\in
[L^{\mathrm{src}}_{c,i},U^{\mathrm{src}}_{c,i}]
\right\rbrace.
```

A union-bound justification requires each marginal guarantee

$$
\mathbb P_c\mkern-3mu \left(
\eta_{c,i}\notin
[L^{\mathrm{src}}_{c,i},U^{\mathrm{src}}_{c,i}]
\right)
\le\alpha_{c,i}
$$

and $\sum_i\alpha_{c,i}\le\alpha_c$. Marginal interval labels without these
hypotheses or another joint argument do not establish
$\mathbb P_c(\mathcal C_c^{\mathrm{src}})\ge1-\alpha_c$. Data-dependent
coordinate, threshold, proxy, or estimator selection must be included in the
coverage analysis or frozen before evaluation.

A proxy such as RMSE, Wasserstein distance, MMD, or a learned discriminator
has authority for a target discrepancy only through a proved,
hypothesis-checked transfer inequality. The two-point experiment makes the
failure concrete. Let

$$
\Theta=\lbrace-1,+1\rbrace,
\qquad
P_{-1}=P_{+1}=\delta_0,
\qquad
Q_{\pm1}=\delta_{\pm\epsilon},
\quad\epsilon>0.
$$

Although
$\sup_\theta W_1(P_\theta,Q_\theta)=\epsilon$, every channel applied to the
source produces one common law $R$. The total-variation triangle inequality
gives

$$
\max_{\theta\in\Theta}
\lVert R-Q_\theta\rVert_{\mathrm{TV}}
\ge\frac12.
$$

The mixture
$R=(\delta_{-\epsilon}+\delta_{+\epsilon})/2$ attains the bound, so
$\delta(\mathsf E,\mathsf F)=1/2$. Uniformly small corresponding-law
Wasserstein error therefore does not imply small directed total-variation
deficiency.

The evidence identity is factored as

```math
\iota
=
(\iota_{\mathrm{cand}},
  \iota_{\mathrm{data}},
  \iota_{\mathrm{analysis}},
  \iota_{\mathrm{env}},
  \iota_{\mathrm{contract}}).
```

Exact transfer requires equality of every factor on which the evidence
depends. A changed identity does not make the new candidate false, but it
blocks direct inheritance until theorem-class applicability or a certified
compatibility morphism is supplied.

### Compatibility-bounded deployment theorem

The repair proves a claim-local admission rule. If, on a joint event
$\mathcal C_c^{\mathrm{dep}}$ with
$\mathbb P_c(\mathcal C_c^{\mathrm{dep}})\ge1-\alpha_c$,

$$
\ell^0_{c,j}\le U^0_{c,j},
\qquad
\ell^1_{c,j}\le\ell^0_{c,j}+\rho_{c,j},
\qquad
U^0_{c,j}+\rho_{c,j}\le\tau_{c,j}
$$

for every required coordinate, the frozen and deployment profiles are well
formed, and every required deployment gate and readiness coordinate passes,
then nonnegativity makes
$[0,U^0_{c,j}+\rho_{c,j}]$ the proved deployment enclosure required for
evaluated status, and the deployment is admissible for $c$ on that event.
Setting $\alpha_c=0$ establishes probability-one admission only. A
deterministic admission statement requires the enclosures and compatibility
inequalities to hold pointwise, independently of
$\omega\in\Omega_c$.

The compatibility reserve $\rho_{c,j}$ is a proved or qualified enclosure of
additional loss introduced by the declared change. It is not spare tolerance
chosen by preference. Frozen uncertainty already included in $U^0_{c,j}$ is
not counted again, and uncertainty in the deployment change is represented
exactly once. The remaining slack

$$
s_{c,j}=\tau_{c,j}-(U^0_{c,j}+\rho_{c,j})
$$

distinguishes positive certified headroom, equality with no certified reserve,
and failure to certify. A negative slack or an upper bound above tolerance is
not by itself proof of an actual violation.

### Coupled-surrogate prefix corollary

For reference and surrogate-coupled host maps $\Phi_k$ and
$\widehat\Phi_k$, suppose the trajectories remain in the certified domain and

$$
E_{k+1}\le L_kE_k+b_k.
$$

The existing BSC prefix theorem then gives

$$
E_n
\le
\left(\prod_{j=0}^{n-1}L_j\right)E_0
+
\sum_{i=0}^{n-1}b_i\prod_{j=i+1}^{n-1}L_j.
$$

This isolates host amplification, horizon, and one-step injection. A
standalone average error does not establish the reachable-domain bound $b_k$
and therefore does not by itself certify the coupled host.

### Executed exact fixture F10

The version 1.2.0 fixture uses exact rational arithmetic, the common interface
error $1/100$, horizon 10, and tolerance $1/20$ in two stable scalar hosts:

| Host | Stable coefficient | Exact maximum error | Disposition |
|---|---:|---:|---|
| HOST-A | $a=1/2$ | $1023/51200$ | within tolerance |
| HOST-B | $a=9/10$ | $6513215599/100000000000$ | tolerance violated first at step 7 |

The retained deterministic receipt reports
`host_relative_tolerance_disposition_confirmed`. It binds the fixture's finite
recurrence claim; exact rational reference and surrogate component
definitions; every exact reference and surrogate-coupled trajectory value;
horizon, initial condition, and tolerance; generator, checker, schema, input,
environment, and host hashes; runtime; and candidate, analysis, environment,
and contract identity mappings. The data identity is explicitly typed not
applicable for this data-free fixture. The manifest, rather than the receipt,
binds the final receipt bytes so that the receipt does not require an
impossible self-hash.

The checker independently recomputes the trajectories, tolerance comparisons,
factored identities, schema, and byte-identical regeneration. This refutes the
universal claim that equal standalone surrogate error entails equal
coupled-host tolerance disposition. It proves one numeric loss-coordinate
disposition for the declared finite recurrence, not full BSC admissibility. It
does not validate an external simulator, an operating region, a physical
system, or any zeta–DQPT claim.

### Prior-art and originality boundary

The version 1.2.0 module treats the following as prior art rather than BSC
discoveries:

- [NASA-STD-7009B](https://standards.nasa.gov/standard/nasa/nasa-std-7009) and
  [NASA-HDBK-7009B](https://standards.nasa.gov/standard/nasa/nasa-hdbk-7009)
  for modeling-and-simulation credibility, acceptance, verification,
  validation, uncertainty, intended use, and reuse;
- [Jakeman, Barba, Martins, and O'Leary-Roseberry (2025)](https://arxiv.org/abs/2502.15496)
  for scientific-machine-learning verification, validation, application
  domains, uncertainty, provenance, and distribution shift;
- [Ellinas, Chaudhuri, Vorwerk, and Chatzivasileiadis (2026)](https://arxiv.org/abs/2603.17836)
  for finite-horizon error propagation of surrogate components inside host
  dynamic simulators;
- [ECMWF's 2026 operational account](https://www.ecmwf.int/en/about/media-centre/aifs-blog/2026/farewell-external-ai-models)
  of upstream-system changes affecting external machine-learning workflows;
  it motivates selective re-verification of claims affected by changed
  dependencies, not automatic recertification of a workflow; and
- [Meel, Kumar, and Pote (2025)](https://proceedings.mlr.press/v258/meel25a.html)
  for finite-sample limits in high-dimensional distribution-distance
  estimation.

The narrow BSC addition is their integration with claim-local typed losses,
noncompensating gates, factored evidence identity, compatibility reserves, and
the existing admissibility and prefix-propagation calculus. The module does not
claim a universal credibility scalar, universal validation procedure, optimal
sample complexity, automatic cross-version transfer, or physical validation.
Its transfer status is bounded by the declared claim, intended use, source and
target coordinate types, identity factors, joint event, horizon, domain,
gates, and tolerances.
The Riemann-hypothesis and DQPT verdicts recorded in version 1.1.0 remain
unchanged.

## 24. Version 1.3.0 operational-channel refinement

### Architectural gap

The prior framework already had Markov-kernel composition, paired quantum
state/observable transport, operational quotients, total-variation defects,
prefix error propagation, and claim-relative simulation evidence. It did not
state one bounded theorem for a mixed classical/quantum
preparation-to-measurement-to-report pipeline. That omission encouraged two
opposite errors:

1. physical systems with similar report diagrams could be rhetorically
   identified despite different microscopic laws; and
2. ordinary channel contractivity could be overpromoted to the still-open
   closure of the full eight-field quantum BSC morphism.

### Adopted fixed-interface repair

The new operational report envelope binds a parameter family, preparation,
fixed typed stages, controls, measurement, terminal report laws, and a
certificate. Classical interfaces use total variation; finite-dimensional
quantum interfaces use

```math
D_{\mathrm{tr}}(\rho,\sigma)
=
\frac12\lVert\rho-\sigma\rVert_1.
```

For ideal and implemented stages, the local defect

$$
d_k(\widehat T_k\widehat z,T_k\widehat z)\le\varepsilon_k
$$

must hold on the **implemented** reachable set or a proved envelope containing
it. An ideal-only reachable set is insufficient because the triangle
inequality evaluates the defect at the implemented input. With ideal-stage
contraction $\eta_k$,

$$
E_m
\le
\sum_{k=0}^{m}
\varepsilon_k
\prod_{j=k+1}^{m}\eta_j.
$$

Classical Dobrushin contraction and quantum trace-distance contractivity may
supply $\eta_k$. A strict quantum contraction is not automatic. A changed
measurement or report is another stage and needs its own defect.

This is BSC-CHN-01, a state/report-law consequence of existing BSC-SIM-03 and
data processing. It does not prove composition of partial domains, observable
pullbacks, equation residuals, deficiencies, completions, or certificate
witnesses. BSC-QOP-03 remains open.

### Added exact consequences

The version 1.3.0 module adds separately scoped results:

- **No downstream resurrection:** Markov, CPTP, POVM, and report channels
  cannot increase the relevant distinguishability. Deterministic inverse
  claims are therefore evaluated on
  $\mathcal I_\varepsilon(y)=\lbrace\theta:d(F(\theta),y)\le\varepsilon\rbrace$.
- **Postselection boundary:** a complete success/failure instrument is
  contractive, while normalization on a successful branch is nonlinear and
  can amplify trace distance. Success probability and conditioning error are
  separate certificate coordinates.
- **Robust inverse enclosure:** a uniform forward-report defect $B$ gives
  $\mathcal I_F(y,\delta)\subseteq\mathcal I_G(y,\delta+B)$ and the converse
  inclusion after swapping $F,G$. This is not parameter-space stability
  without inverse regularity.
- **Spectral-marginal no-go:** two orthogonal pure photon states with opposite
  relative phase have identical spectral intensities. Unit intensity overlap
  therefore does not certify equality of full quantum states.
- **Driven energy accounting:** for
  $\dot\rho=-i[H,\rho]/\hbar+\mathcal D_t(\rho)$, one has
  $`\dot E=\mathrm{Tr}(\rho\dot H)
  +\mathrm{Tr}(H\mathcal D_t(\rho))`$. The labels depend on the declared
  system/bath split and energy zero. Measurements, resets, coupling energy,
  and output fields need additional terms.
- **Energy-port residual localization:** a finite additive port diagram obeys
  $`R_G=\sum_vr_v+\sum_eg_e`$. Exact components and opposite-orientation
  seams therefore glue to the external balance, with pointwise and integrated
  absolute bounds. The converse is false: cancelling component or seam errors
  can give $R_G=0$. Coupling or interface energy must be retained as a
  component, and strong-coupling interaction energy cannot be silently
  discarded.
- **Denominator-typed efficiency:** count yield, energy efficiency, and
  conditioned efficiency remain different quantities. Stage efficiencies
  telescope only when consecutive ratios use the identical intermediate
  extensive quantity, boundary, interval, cohort, weighting, and evidence
  identity. A probability sink is not an energy port without an energy
  bridge.
- **Scalar Bernoulli encoding:** under the conditional-iid model,
  $K=\sum_iY_i$ is sufficient and
  $I(X;Y^N)=I(X;K)\le\log_2(N+1)$. For a uniform 8-bit input, $N\ge255$ is
  necessary but not sufficient for exact decoding. In fact, 256 scalar
  Bernoulli laws cannot have pairwise disjoint finite-sample supports, so
  zero-error recovery is impossible for every finite $N$ in this model.
- **Semantic alignment:** if both relation axes denote the same entities, one
  identity map, under $P_{\phi(i),i}=1$, requires
  $S=PCP^{\mathsf T}$. Independent row and column maps
  certify only $S=PCQ^{\mathsf T}$ and are valid without further proof only
  for separately typed roles.

### Four-source crosswalk

The source-bound application note records:

- Kim et al.'s warm-cesium/quantum-dot two-photon interference as a tested
  tuned and post-selected compatibility result, not a completed hybrid
  network or full-state equality certificate;
- Guo et al.'s plasmonic photonic time crystal as an externally driven Floquet
  experiment whose pump remains in the energy ledger and whose lasing and
  correlated-plasmon extensions remain predictions; its effective-mass change
  is model-inferred, and the bosonic energy model needs truncation or domain
  control;
- Bindi et al.'s grain-local diffraction and composition as direct material
  evidence from a purposive selection funnel, with neither prevalence nor a
  unique formation history inherited; and
- Govind, Raigoza, and Apsel's microwave features and probabilistic bits as a
  measured hardware channel whose cached image demo, repeated-bit rate,
  semantic alignment, iid law, and security status remain separate claims.

BSC has not replayed any of the four hardware experiments, raw datasets,
spectroscopic or crystallographic fits, classifier training, or image
reconstruction.

### The 1/137 boundary

The operational-envelope axioms contain no equation fixing the
fine-structure constant. They admit typed physical completions with different
couplings and generally different induced channels, so no numerical value
follows from the axioms alone. Noninjectivity over one fixed report envelope
has not been exhibited and is not asserted. A derivation of
$\alpha^{-1}\approx137.036$ requires a typed electromagnetic model,
normalization and renormalization conventions, a dimensionless prediction,
and metrological comparison. A recurrence of 137 in a fit, graph, or scale is
not a bridge.

### Prior-art and originality boundary

Quantum networks, Markov/CPTP/POVM data processing, Dobrushin and trace-distance
contractivity, sufficient statistics, Hoeffding bounds, graph matching,
open-system energy accounting, boundary port-Hamiltonian systems, and CODATA
metrology are prior art. The
BSC-specific addition is their claim-relative integration with implemented
reachable sets, evidence identity, physical completion, decision descent, and
local demotion. It is a unification of evidentiary form, not a unified field
theory.

## 25. Version 1.3.0 electromagnetic evidence bridge

### Remaining physical-completion gap

The operational report envelope blocked a derivation of the fine-structure
constant because abstract channel form contains no equation fixing an
electromagnetic interaction strength. That negative result was correct but
did not yet expose the exact layers at which electromagnetic evidence enters:
bundle and gauge, local field equations, constitutive response, boundary
ports, calibrated instrument report, inverse theorem, coupling normalization,
renormalization, and metrology.

### Adopted typed completion

The version 1.3.0 bridge introduces the companion record

```math
\mathsf{EMC}
=
\left(
M,g,P,[\mathcal A],\mathcal F,\mathcal H,\mathcal J,
\mathcal C,\mathcal B,\mathcal M,\mathcal R,
\mathsf{Cert}_{\mathrm{EM}}
\right).
```

It is a physical completion of the existing operational report envelope, not
a ninth morphism field. The local Maxwell equations

$$
d\mathcal F=0,
\qquad
d\mathcal H=\mathcal J
$$

do not choose a constitutive law, topology, boundary condition, instrument,
or coupling. Each remains an independently typed certificate coordinate.

### Exact bridge claims and no-go results

The claim ledger adds BSC-EM-01 through BSC-EM-11:

1. **Gauge descent (EM-01):** a connection-level report is physical exactly
   when constant on the declared gauge orbits.
2. **Holonomy (EM-02):** on suitable nontrivial topology, equal curvature can
   coexist with different gauge-invariant closed-loop holonomy.
3. **Sources and flux (EM-03):** a smooth global solution of
   $d\mathcal H=\mathcal J$ requires $d\mathcal J=0$ and makes
   $\mathcal J$ exact; singular and open systems need relative or
   distributional typing. Local source-free laws and tangential power traces
   do not select a normal topological-flux sector.
4. **Poynting balance (EM-04):** time-independent symmetric positive
   constitutive tensors separate stored field energy, outward boundary power,
   and work on current. Modulation and dispersion add pump or material-state
   obligations. Static curved geometry changes measures rather than supplying
   energy; moving boundaries and time-dependent metrics require their
   transport terms. A relativistic energy current is conserved only after
   the included total stress-energy and Killing or asymptotic charge
   construction are declared.
5. **Passive scattering (EM-05):** a complete power-normalized passive report
   is contractive in its declared metric. Hidden ports, reference planes,
   impedance, basis, de-embedding, bandwidth, stored energy, and simultaneous
   calibration uncertainty remain in the report identity.
6. **Phase no-go (EM-06):** $r$ and $re^{-i\omega\tau}$ have identical power
   but different phase and delay, so magnitude-only data cannot license a
   coherent time-domain claim.
7. **Field normalization (EM-07):** under $A'=\lambda A$, the bare
   coefficients change while $q^2/Z$ is invariant. Gauge form does not select
   that invariant's value.
8. **Flux-product quantization (EM-08):** Chern/Dirac integrality constrains
   $\frac{q}{2\pi\hbar}\int_\Sigma F_{\mathrm{phys}}$, not $q$, $Z$,
   $q^2/Z$, or $\alpha$ separately.
9. **Revised-SI metrology (EM-09):** exact $e,h,c$ imply
   $\mu_0=\alpha\mkern3mu 2h/(ce^2)$; the obsolete pre-2019 exact value of $\mu_0$
   cannot be recycled as independent evidence for $\alpha$.
10. **RG boundary-value no-go (EM-10):** the equation
    $\mu\frac{dg}{d\mu}=\beta(g)$ transports a supplied coupling between
    scales but does not determine its
    boundary value. The exact case $\beta\equiv0$ admits every constant
    $g(\mu)=g_0$; for nonzero $\beta$, an integration constant remains.
    Scheme, thresholds, matching, truncation, and scale are additional
    certificate coordinates.
11. **Aperiodic materialization descent (EM-11):** a tiling predicate becomes
    a field or scattering predicate only when it is constant over the
    selector-and-materialization fiber. If a coefficient field $\kappa$
    faithfully encodes a tiling partition $P$ in the sense
    $\tau_v\kappa=\kappa\Rightarrow\tau_vP=P$, then
    $`\mathrm{Stab}_{\mathrm{tr}}(\kappa)\subseteq\mathrm{Stab}_{\mathrm{tr}}(P)`$. Constant coefficient fields and
    lattice-periodic coefficient fields materializing only the unlabeled
    carrier grid are exact counterexamples to an unconditional transfer.

Maxwell boundary inversion is retained as theorem-local rather than assigned
a universal EM claim: every promotion names the forward problem, coefficient
class, gauge or diffeomorphism quotient, full or partial data, frequency or
time regime, calibration bridge, uniqueness theorem, stability class, and
target identified set. A finite S-parameter matrix is not automatically the
full boundary-response operator.

### Binary-width and polygon screen

Version 1.3.0 also tests a proposed arithmetic route through
$2^{31}-1$, $2^{32}-1$, the Year 2038 signed-integer boundary, and the
constructible regular $65\mkern3mu 537$-gon. The exact positive result is that
$\mathrm{ord}_{137}(2)=68$, so the rational $1/137$ has a 68-bit
repetend. The exact negative results are

$$
2^{31}-1\equiv16,\qquad
2^{32}-1\equiv33,\qquad
65\mkern3mu 537\equiv51
\pmod{137},
$$

and the real cyclotomic degree for the regular $137$-gon is
$(137-1)/2=68$, not a power of two. These facts explain a real base-two
connection while blocking promotion to a physical identification. The
measured low-energy constant is not exactly $1/137$, and the integer
relations supply no action, normalization, RG boundary condition, or
metrological equation for $\alpha$.

### Einstein monotile and diffraction screen

The Hat theorem is routed through the electromagnetic bridge rather than
through numerical analogy. The Hat is a union of eight kites in the periodic
$[3.4.6.4]$ Laves, or deltoidal-trihexagonal, tiling and nevertheless forces
an aperiodic partition into Hats. The later Spectre construction separately
forces homochiral nonperiodic tilings. These statements concern planar
translations, reflections, and hierarchical supertiles; they are not
Maxwell, reciprocity, or constitutive theorems.

The adopted physical chain is

$$
P\longrightarrow C_{\rm sel}(P)=X_N
\longrightarrow\Phi_{\rm mat}(X_N)
\longrightarrow\mathcal P_{\lambda,p}
\longrightarrow Y.
$$

It distinguishes an infinite tiling, a finite point/edge/interior selector,
physical scale and material contrast, the electromagnetic forward problem,
and the calibrated report. This distinction is forced by a concrete
published counterexample: the Hat tiling is aperiodic while its vertex
point-scatterer diffraction is two-periodic because the selected vertices
inherit an underlying periodic hexagonal net. Spectre point diffraction is
instead nonperiodic and chiral. Reciprocal-space periodicity therefore does
not report real-space aperiodicity without the selection and observation map.

The 2026 Nature Communications experiment instantiates one such chain by
selecting centroids of an $H_6$ Hat approximant, fabricating $372\mkern3mu 100$ holes
in a $350\mkern3mu \mathrm{nm}$ SiN film, and measuring sharp Bragg peaks whose
positions were insensitive to illumination position, mirror-reversing
pinwheel patterns, and helicity-dependent intensity. Its declared scalar
model is

$$
F_N(k_x,k_y)=
\sum_{j=1}^N e^{2\pi i(k_xx_j+k_yy_j)},
\qquad I_N=|F_N|^2,
$$

with a golden-ratio/Fibonacci-inflation-derived orientation

```math
\theta_{\rm chiral}
=
\arccos\mkern-3mu \left(\frac{3(1+\sqrt5)/2-1}{4}\right)
\approx15.52^\circ.
```

The publication supplies single-study evidence along that finite
geometry-to-fabricated-sample-to-report chain. It does not close the full
Maxwell, calibration, or uncertainty obligations and does not establish a
universal band gap, localization, nonreciprocity, or a coupling value. Eight
kites, golden-ratio/Fibonacci inflation geometry, and sixfold intensity
symmetry do not provide a map to $\alpha$ or $1/137$.

### Status and release boundary

These are symbolic claims with no local hardware execution. The
2026 monotile optical report is one experimental study and was not replayed
here. The framework changes do not derive
$\alpha^{-1}\approx137.036$, quantize the full electromagnetic
field, prove a material model, execute a calibrated scattering experiment, or
establish a unified field theory. They belong only to the `1.3.0`
manuscript, framework, synopsis, ledgers, and regression suite. The immutable
v1.2.0 release, tag, GitHub assets, and Zenodo deposit remain unchanged.

## Version 1.4.0: Collatz recursive-sufficiency correction and certificate

### Source defect and mathematical repair

The release audits Mohammad Ansari's 2025 recursive-sufficiency induction
against the published definitions. Exact residue expansion gives

```math
F_1\setminus F_2
=(36\mathbb N_0+27)\cup(36\mathbb N_0+31).
```

The $31$-class has an explicit exact merge to $32k+27<36k+31$; the
$27$-class remains unresolved. The release therefore does not restore the
printed induction, the original $F_n$ claim, or the claimed
$4\cdot3^{44}+2$ jump.

The retained replacement consists of:

- an unconditional parity-prefix RS family $U_m$ with exponentially
  vanishing density;
- the safety-net lemma $A\cup(B\cap S)$ for $A\subseteq B$ and RS
  $B,S$, giving a ternary-spine family without promoting $F_n$;
- a $2^{71}$-conditioned family $V_m$;
- the refined $W_m=G\cap V_m$ for $m\ge2$, with exact density
  $d(W_m)=\frac59d(V_m)$ in that range; and
- an explicit preservation of the classical parity-vector, stopping-time,
  density, and sufficient-set prior-art boundary.

The proposed ghost-cylinder theorem and $1/243$ subprogression were not
needed for this repair and were withheld pending separate symbolic review.

### Executed exact fixture F11

Fixture F11 retains a 4,826,862-byte, 52,686-row first-descent table with
SHA-256
`88df1573d49511a4bc93fab35f85d3feb1cade2d40b5444ee88ae42699aa5250`.
The routine checker independently replays every row with arbitrary-precision
integers. The publication gate additionally exhausts all 1,388,888,889
$G$-compatible offsets in the ten-billion-wide interval and requires the
candidate set to match exactly.

Strong induction then gives the exact implication

```math
\bigl[\text{convergence through }2^{71}\bigr]
\Longrightarrow
\bigl[\text{convergence through }2^{71}+10^{10}\bigr],
```

conditional on the retained computation. BSC did not replay the external
$2^{71}$ campaign. The result is an unreviewed claim-local
computer-assisted extension, not an official frontier announcement or a
Collatz proof.

### Framework and release boundary

No BSC core morphism, defect algebra, simulation profile, operational channel,
or electromagnetic theorem changes. The update is limited to the
number-theory application, F11, claim and notation ledgers, paper, synopsis,
tests, metadata, and release artifacts. Version 1.3.0 and every earlier tag,
asset, and Zenodo record remain immutable.
