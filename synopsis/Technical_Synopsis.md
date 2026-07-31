# On Boundaries of Evidence

## Two-page technical synopsis

**J. Tree · Independent researcher**

**Repository state:** version 1.4.0 release, dated 31 July 2026.

**Version record:** https://github.com/jkolantree/BSC/releases/tag/v1.4.0

**Zenodo concept DOI:** https://doi.org/10.5281/zenodo.21541160

Scientific claims often fail not within either of two descriptions, but in the
passage between them: from an interior state to boundary data, one instrument
to another, a fine model to a coarse model, a learned operator to a dynamical
claim, or a topological invariant to a physical quantity. *On Boundaries of
Evidence* develops Boundary-State Calculus (BSC) as a typed audit calculus for
this passage.

BSC is not proposed as an ontology, a unified physical theory, or a proof of
holography, quantum gravity, consciousness, QCD, or the Riemann Hypothesis. It
does not independently establish a physical origin for RH or an end-to-end
quantum advantage. Its unit of evaluation is one claimed transfer. The
question is whether that transfer states:

1. what moves;
2. which observables remain meaningful;
3. what information is destroyed;
4. whether the target equations remain satisfied;
5. which diagrams fail to commute;
6. what physically implements the passage; and
7. what evidence licenses the resulting claim.

The paper transcribes the supplied BSC corpus's original finite-system tuple
and its later measurable repair rather than replacing them with a cleaner
retrospective object (§3). Those hash-identified internal sources are not
redistributed, so the lineage cannot be independently replayed from this
release. The repaired system separates raw state from exact
observational equivalence and includes controls, outputs, physical context,
legal filtration, dynamics, observation, comparison geometry, viability,
transformation registries, and a boundary ledger. A companion record supplies
reconstruction data, provenance, and certificate state without silently
changing the inherited tuple. The instrument, controller, observer or reference
frame, clock, and calibration state are physical configuration variables, not
informal metadata.

Several operations that boundary language often conflates are kept distinct
(§5): an ideal trace, a finite sensor-layer observation, a boundary
response such as a Dirichlet-to-Neumann map, a reconstruction relation, and a
selected extension. A boundary response supports an interior claim only
relative to a governing equation, admissible coefficient class, equivalence or
gauge class, regularity assumptions, data regime, and stability theorem.

The central added object is the typed transfer record (§7):

```math
\mathfrak M_{\ell\to m}
=
\left(
T_{\ell m},
T_{\ell m}^{\sharp},
K_{\ell m},
R_{\ell m},
\Theta_{\ell m},
\delta_{\ell m},
C_{\ell m},
\mathsf{Cert}_{\ell m}
\right).
```

Here $T_{\ell m}$ transports states, while $T_{\ell m}^{\sharp}$ pulls
target observables in the reverse direction. $K_{\ell m}$ is an observation
post-processing or simulation channel. $R_{\ell m}$ records failure to
satisfy the target equations after transport. $\Theta_{\ell m}$ measures a
declared naturality or commuting-square defect. $\delta_{\ell m}$ is the
directed Blackwell–Le Cam deficiency: the best achievable error when the source
experiment attempts to simulate the target experiment. $C_{\ell m}$ records
the carrier, controller, instrument, reference frame, clock, resource
interface, and boundary conditions. $\mathsf{Cert}_{\ell m}$ binds
assumptions, tolerances, sources, proof or execution artifacts, hashes,
unresolved obligations, a mathematical verdict, and separate readiness
coordinates.

These coordinates are not collapsed into one score. Equation residual,
observation defect, statistical deficiency, quotient loss, and viability
failure occupy different spaces and obey different propagation laws (§8,
§7.2). A missing type makes a record not well formed; a missing required
evaluation leaves it unevaluated; a failed claim-specific tolerance or gate
makes it inadmissible for that claim.

For compatible partial stochastic transfers, state kernels compose forward on
the support-compatible domain
$D_{\ell n}=\lbrace x\in D_{\ell m}:T_{\ell m}(x,D_{mn})=1\rbrace$. Observable
pullbacks compose in reverse through the restricted map
$T_{\ell m}^{\sharp\mid D_{mn}}:B_b(D_{mn})\to B_b(D_{\ell n})$. Observation defects obey
a contraction-weighted bound, directed deficiencies obey a triangle
inequality, and deterministic equation residuals propagate only when a
compatible equation-space map has been supplied (§7.1). The
resulting claim-admissible chain bounds are collected in §15. If clocks,
interfaces, resource contracts, or boundary conditions do not match, the
composite is undefined rather than merely inaccurate.

Persistence is defined at the level of induced path laws (§9).
Endpoint return is insufficient. Persistent identity requires every required
prefix of a fold chain to be admissible for the persistence claim. An upper
error enclosure below tolerance certifies that coordinate; one crossing the
tolerance is inconclusive unless a valid lower bound or exact evaluation proves
violation. The statement that a persistent
object is a recursively maintained finite boundary-state is therefore a formal
organizing principle and a target-relative definition. Its promotion to a
universal physical law remains conjectural, empirically untested, and
computationally unexecuted.

The version 1.2.0 simulation-evidence profile refines the existing certificate
rather than adding a morphism field. For each claim and evidence identity it
fixes intended use, typed numeric losses, hard gates, statistical estimators
and oracle models on a joint probability space, joint coverage, optimization
gaps, proxy-transfer relations, a monotone unit-respecting map from source
estimands to target BSC losses, compatibility reserves, and factored
provenance. Statistical simulation between experiments, computational
simulation, and surrogate deployment remain distinct.

If the propagated frozen loss obeys $\ell^0_{c,j}\le U^0_{c,j}$ and a certified change
obeys $`\ell^{\rm dep}_{c,j}\le\ell^0_{c,j}+\rho_{c,j}`$, deployment is admitted
only when $U^0_{c,j}+\rho_{c,j}\le\tau_{c,j}$ for every required coordinate,
all hard gates are true, and readiness is adequate. Estimator uncertainty
already inside $U^0_{c,j}$ is not counted again; deployment-change uncertainty
is counted once. The conclusion holds with at least the declared joint
coverage. Failure probability zero is not determinism without pointwise
bounds. Zero slack has no certified robustness.

The coupled-surrogate corollary specializes the prefix-error theorem:
standalone component error propagates through host sensitivity and horizon.
Exact executable Fixture F10 gives both stable hosts the same interface error
$1/100$ for ten steps. Host A ($a=1/2$) stays within $1/20$, while Host B
($a=9/10$) first violates it at step 7. This is code verification of one
finite recurrence, not empirical or physical validation. Established V&V/UQ
and finite-horizon coupling work remain prior art; BSC claims only the typed
integration, evidence-transfer rule, and local demotion behavior.

Version 1.3.0 adds a restricted operational-channel core for fixed
compatible preparation-to-report pipelines. Classical laws use total
variation, quantum states use trace distance, POVMs form the
quantum-to-classical boundary, and every local defect must cover implemented
reachable inputs. The propagated report error obeys

$$
E_m\le
\sum_{k=0}^{m}\varepsilon_k
\prod_{j=k+1}^{m}\eta_j.
$$

Unconditioned downstream channels cannot resurrect lost distinguishability;
normalization on a successful postselected branch is nonlinear and can
amplify it. A uniform forward-report defect gives two-sided containment of
compatible inverse sets after radius enlargement. An exact phase-sign
counterexample shows that unit spectral-intensity overlap need not imply
quantum-state closeness. The same module proves a finite-dimensional driven
open-system energy identity; finite energy-port gluing with exact component
and seam residual localization; and denominator-typed count, energy, and
conditioned efficiencies. Global energy closure does not certify local seams,
and strong-coupling interaction energy must remain explicit. The module also
proves a sufficient-count and finite-sample zero-error obstruction for scalar
iid Bernoulli encoders and a single-permutation criterion for same-entity
relation alignment. It also proves that generic
channel form cannot determine the electromagnetic fine-structure constant:
1/137 needs a physical and metrological bridge. These results do not close the
full eight-field quantum composition claim BSC-QOP-03.

The [electromagnetic completion](../framework/Electromagnetic_Evidence_Bridge.md)
makes that bridge explicit (BSC-EM-01 through BSC-EM-11). It types the route
from bundle and gauge class through Maxwell
sources, constitutive response, boundary ports, instrument report, and
inference. Gauge descent, holonomy, source compatibility, Poynting balance,
passive scattering, inverse-problem scope, field normalization, flux
quantization, revised-SI metrology, and renormalization-group transport remain
different obligations. They do not become one microscopic theory.

For a power-normalized, closed-port passive model,
$S^\dagger S\preceq I$. If a simultaneous calibration certificate gives
$\lVert \widehat S-S\rVert_2\le\varepsilon$, then
$\sigma_{\max}(\widehat S)-\varepsilon>1$ falsifies that declared passive
model, $\sigma_{\max}(\widehat S)+\varepsilon\le1$ certifies contractivity on
the declared configuration and band, and the remaining interval is
inconclusive. An observed deficit may instead be power transferred to hidden
ports. The causal passive pair

$$
S_0(\omega)=r,
\qquad
S_\tau(\omega)=r e^{-i\omega\tau},
\qquad
0<r\le1,
$$

has the same power response, $|S_0(\omega)|^2=|S_\tau(\omega)|^2=r^2$, but
different phase and delay. Magnitude-only data therefore do not identify a
coherent waveform. A finite measured scattering matrix likewise does not
become a full Maxwell boundary operator or select a unique constitutive
interior without the applicable calibration, coefficient class, quotient,
uniqueness, and stability theorem.

At low energy the revised SI gives the exact relations

```math
\alpha
=
\frac{e^2}{4\pi\varepsilon_0\hbar c}
=
\frac{\mu_0ce^2}{2h}
=
\frac{Z_0}{2R_{\mathrm K}},
\qquad
\mu_0=\alpha\frac{2h}{ce^2}.
```

Fixed $e,h,c$ therefore do not fix $\alpha$; the measured uncertainty is
carried by $\alpha$ and hence by $\mu_0$. Field rescaling preserves
$q_i^2/Z$, Chern or Dirac quantization constrains a charge-flux product, and
Ward identities constrain matching, but none selects the remaining
dimensionless coupling. The equation
$\mu\mkern3mu d\alpha/d\mu=\beta(\alpha)$ transports a supplied boundary value
$\alpha(\mu_0)=\alpha_0$ across a declared scheme, scale, threshold, and
particle content. No theorem in BSC derives or predicts
$\alpha^{-1}=137.035\mkern3mu 999\mkern3mu 177(21)$.

BSC-EM-11 adds the selector-and-materialization boundary for aperiodic
geometry. The Hat is an aperiodic union of eight kites from the periodic
deltoidal-trihexagonal carrier grid, while the Spectre supplies a distinct
strictly chiral tiling theorem. If a coefficient field $\kappa$ faithfully
encodes a tiling partition $P$ so that
$\tau_v\kappa=\kappa\Rightarrow\tau_vP=P$, then
$`\mathrm{Stab}_{\mathrm{tr}}(\kappa)\subseteq\mathrm{Stab}_{\mathrm{tr}}(P)`$. Without that hypothesis, a constant or
carrier-periodic material map erases the aperiodicity. Published Hat
point-scatterer diffraction is correspondingly periodic despite the
aperiodic tiling. The 2026 centroid-selected SiN experiment supplies
single-study evidence along one specific finite
geometry-to-fabricated-sample-to-report chain and observes chiral diffraction;
it does not close the full Maxwell, calibration, or uncertainty obligations
and does not establish a universal band gap, nonreciprocity, or a coupling
value.

The first crosswalk applies the core to atom–quantum-dot two-photon
interference, a driven plasmonic photonic time crystal, a blast-forged
multicomponent alloy, and a microwave probabilistic-bit processor. It retains
the reported local measurements while blocking, respectively, unexecuted
network protocols, pump-free gain, unique historical reconstruction, and
lossless/security/semantic promotion. This is a unification of evidentiary
form, not of microscopic laws.

Version 1.1.0 adds certified normalized-scale
profiles $L_N=A_N/Z_N$. A diverging normalizer can collapse the raw limit
without creating finite zeros, while logarithmic rates split exactly into
normalizer and carrier exponents. Continuous scaled normalization changes
preserve singular loci; quantitative rate stability requires a positive
amplitude margin; positive branch gaps expose the boundary of an exceptional
set; continuous parameter slices may hide ambient singularities; and strict
holomorphic contour margins transfer zero counts and local multiplicity.
Ideal scalars remain distinct from their estimator laws.
Exact finite-label decoding requires measurably separated output laws, with a
total-variation lower bound when they overlap.

The zeta–DQPT construction is the first substantial instance. It proves the
declared finite identity
$Z_N(\beta_{\rm eff})\mathcal L_N(\beta_{\rm eff},t)=-S_N(\beta_{\rm eff}+it)$, local-uniform alternating-tail control, and a
fixed $s$ decay exponent that separates eta zeros from nonzeros. For
$N=2^d$ this recovers the source's pointwise free-energy values
$(1-\mathrm{Re}(s))\log 2$ off the zero set and $\log 2$ on it. The
rate discontinuities are therefore exactly the zeta zeros, with jump
$\mathrm{Re}(s_0)\log 2$ at $s_0$; confining all of them to the
critical line is equivalent to, rather than a proof of, RH. Near a fixed zero
of multiplicity $m$, the $m$ roots of the finite partial sum localize at scale
$N^{-\mathrm{Re}(s_0)/m}$; a simple root has an explicit signed leading
displacement. On each fixed $\beta$ real-time slice, the rate
discontinuities are exactly the ordinates of zeros on that line. The instance
also proves a bounded Rouché zero-count transfer conditional on certified
whole-contour separation.
It separately records the reported five-qubit NMR agreement with
the first five known zero ordinates as one un-replayed study. Finite agreement
does not certify an exact zero, thermodynamic nonanalyticity, the universal RH
quantifier, a comparator-independent quantum advantage, a unique Kelvin
temperature, or an independent physical origin.

## Mathematical provenance and status

| Layer | Content | Status in this paper |
|---|---|---|
| Electromagnetic evidence bridge | Gauge and bundle theory; Maxwell source laws and Poynting balance; passive scattering and calibration; scoped electromagnetic inversion; Chern/Dirac quantization; revised-SI and coupling metrology; Ward identities and RG flow; aperiodic tilings and point diffraction | The physical mathematics is imported. BSC adds the typed route, exact nonidentifiability tests, three-valued calibrated passivity disposition, pure-delay phase no-go, aperiodic selector/materialization descent, and local demotion when a coupling boundary value or other bridge coordinate is absent. It does not derive or predict $\alpha$. |
| Established imports | Markov kernels and operational quotients; Blackwell–Le Cam comparison; boundary trace and Calderón-type response; Koopman operators and stated learnability limits; periodic homogenization; sheaf descent; structured cospans; non-invertible defects; proof checking | Imported under their published or preprint hypotheses. These ingredients are not claimed as new BSC discoveries. |
| Paper-level consequences | Quotient and exact-decision descent; repaired restricted-pullback composition; paired state–observable probability preservation; defect, deficiency, and deterministic residual propagation; simulation-evidence typing, compatibility-bounded deployment, and coupled-surrogate prefix propagation; fixed-interface operational-channel error propagation, no downstream resurrection, nonlinear-postselection and spectral-marginal counterexamples, robust inverse-set enclosure, driven open-system energy accounting, energy-port residual localization, denominator-typed efficiency, scalar Bernoulli information/zero-error bounds, and same-identity relation alignment; normalized-scale rate decomposition and covariance; singular-set and slice visibility; analytic zero and multiplicity transfer; the zeta-specific alternating-tail bound, pointwise exponent/rate split, ambient and fixed $\beta$ singular sets, bounded contour count, and local root drift; persistence certification; generic decorated-cospan composition; readiness-cap propagation; the blocks from winding to physical charge and from channel form to $\alpha$ | Proved locally under the manuscript's stated assumptions. The canonical BSC decoration functor and full quantum-morphism composition remain open. No empirical status is inherited. |
| Reference fixtures | Eleven examples covering winding, inverse ambiguity, directed deficiency, Koopman pollution, quantum-reference-frame descent, sheaf obstruction, off-shell residual, exact counterexample retention, zeta–DQPT scope separation, stable-host surrogate dependence, and a Collatz recursive-sufficiency repair | Fixtures 1–7 and 9 have exact mathematical derivations but no separate execution receipts. Fixtures 8, 10, and 11 have deterministic CPython receipts. F11's finite extension remains conditional on the separately sourced $2^{71}$ base. Immutable v1.1.0 contains Fixtures 1–9; immutable v1.0.1 contains Fixtures 1–8. |
| Open status | Universal persistence, generic empirical validation, nonlinear stochastic residual composition, full quantum-morphism composition (BSC-QOP-03), instrument-uncertain reconstruction, QRF quotient characterization, learnability-aware recurrence, faithfulness of operational report envelopes under added interventions, non-iid hardware rate-distortion, physical charge bridges, end-to-end zeta-algorithm advantage, temperature/origin bridges, and a machine-checked BSC kernel | Conjectural, untested, unexecuted, blocked, or open as individually recorded. |

The fixtures (§16) compute a torus winding class $(2,-3)$ while
blocking electric charge without a physical bridge; exhibit two distinct
one-dimensional conductivities with the same Dirichlet-to-Neumann map; obtain
directed deficiencies $0$ and $1/4$ for two binary experiments; separate a
Koopman pseudomode residual $\sqrt{2/N}$ from polluted compression
eigenvalues; prove that invariant Bell inputs with the same reduced state
$I/2$ produce orthogonal transformed outputs, so a finite $\mathbb Z_2$ frame
transformation does not descend through the stated reduced-system quotient;
give locally nonempty
parity constraints with no global section; detect the nonzero residual $m^2c$
of an off-shell field shift; and retain a deterministic receipt for the
counterexample $x=-1$ to $\sqrt{x^2}=x$. Fixture 9 retains only
the finite zeta–coherence identity while blocking unsupported promotion from
the unexecuted fixture to the application-level analytic transfer, RH, a
limiting DQPT, broad quantum advantage, unique Kelvin temperature, or
independent physical origin. Fixture 10 retains exact prefix trajectories for
equal standalone surrogate error in two stable hosts and demonstrates
different host-relative tolerance dispositions for one loss coordinate,
without promoting the recurrence to full admissibility or physical validation.
Fixture 11 identifies the first missing residue layer in a published Collatz
recursive-sufficiency induction, proves replacement zero-density
recursively-sufficient sieves, and retains exact row-replay and exhaustive
candidate-enumeration evidence for a conditional ten-billion extension beyond
$2^{71}$. It does not independently replay the external base computation,
repair the unresolved $36k+27$ class, or prove the Collatz conjecture.

The paper also makes physical promotion deliberately expensive. Winding and
physical charge are different typed objects (§13, p. 21). A charge claim needs
a derived bridge from a gauge representation, action and current, Gauss law,
anomaly condition, boundary condition, or calibrated measurement protocol. The
application section therefore treats primordial-field toroidal models as
candidate topological and stabilization grammar, not as an established
derivation of quark charge, QCD, or hadron dynamics (§17).

Claims carry a categorical mathematical verdict plus separate mathematical,
empirical, computational, source, and transfer readiness (§2.2). A dependency
graph propagates only edge-specific readiness caps; it does not manufacture a
descendant verdict (§2.3). A theorem does not raise empirical readiness;
a hash establishes artifact identity rather than truth; a proof DAG is not
itself a proof; and an unexecuted numerical description remains unexecuted
(§14).

The appropriate test is narrow and adversarial. Ask whether an equivalent
compositional record already exists, whether any map is ill-typed, whether a
composition law fails, whether a fixture has a counterexample, or whether the
record changes no scientific decision. If an established formalism already
supplies the same obligations and demotion semantics, or if BSC never
distinguishes an invalid transfer from a nearby valid one, the additional
structure is unnecessary. If it exposes such a distinction and preserves it
through composition, that—not a claim about the universe—is the contribution
requiring further development.
