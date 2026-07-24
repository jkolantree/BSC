# On Boundaries of Evidence

## Two-page technical synopsis

**J. Tree · Independent researcher · version 1.0.1 · 24 July 2026**

**DOI:** https://doi.org/10.5281/zenodo.21541561

Scientific claims often fail not within either of two descriptions, but in the
passage between them: from an interior state to boundary data, one instrument
to another, a fine model to a coarse model, a learned operator to a dynamical
claim, or a topological invariant to a physical quantity. *On Boundaries of
Evidence* develops Boundary-State Calculus (BSC) as a typed audit calculus for
this passage.

BSC is not proposed as an ontology, a unified physical theory, or a proof of
holography, quantum gravity, consciousness, or QCD. Its unit of evaluation is
one claimed transfer. The question is whether that transfer states:

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
(§5, pp. 9–10): an ideal trace, a finite sensor-layer observation, a boundary
response such as a Dirichlet-to-Neumann map, a reconstruction relation, and a
selected extension. A boundary response supports an interior claim only
relative to a governing equation, admissible coefficient class, equivalence or
gauge class, regularity assumptions, data regime, and stability theorem.

The central added object is the typed transfer record (§7, pp. 11–14):

$$
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
$$

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
pp. 14–15). A missing type makes a record not well formed; a missing required
evaluation leaves it unevaluated; a failed claim-specific tolerance or gate
makes it inadmissible for that claim.

For compatible partial stochastic transfers, state kernels compose forward on
the support-compatible domain
$D_{\ell n}=\{x\in D_{\ell m}:T_{\ell m}(x,D_{mn})=1\}$. Observable
pullbacks compose in reverse through the restricted map
$T_{\ell m}^{\sharp\mid D_{mn}}:B_b(D_{mn})\to B_b(D_{\ell n})$. Observation defects obey
a contraction-weighted bound, directed deficiencies obey a triangle
inequality, and deterministic equation residuals propagate only when a
compatible equation-space map has been supplied (§7.1, pp. 13–14). The
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

## Mathematical provenance and status

| Layer | Content | Status in this paper |
|---|---|---|
| Established imports | Markov kernels and operational quotients; Blackwell–Le Cam comparison; boundary trace and Calderón-type response; Koopman operators and stated learnability limits; periodic homogenization; sheaf descent; structured cospans; non-invertible defects; proof checking | Imported under their published or preprint hypotheses. These ingredients are not claimed as new BSC discoveries. |
| Paper-level consequences | Quotient descent; repaired restricted-pullback composition; paired state–observable probability preservation; defect, deficiency, and deterministic residual propagation; persistence certification; operational factorization; generic decorated-cospan composition; readiness-cap propagation; the block from winding to physical charge | Proved locally under the manuscript's stated assumptions. The canonical BSC decoration functor remains open. No empirical status is inherited. |
| Reference fixtures | Eight finite examples covering winding, inverse ambiguity, directed deficiency, Koopman pollution, quantum-reference-frame descent, sheaf obstruction, off-shell residual, and exact counterexample retention | Fixtures 1–7 have exact mathematical derivations but no separate execution receipts. Fixture 8 has a deterministic CPython receipt. |
| Open status | Universal persistence, generic empirical validation, nonlinear stochastic residual composition, instrument-uncertain reconstruction, QRF quotient characterization, learnability-aware recurrence, physical charge bridges, and a machine-checked BSC kernel | Conjectural, untested, unexecuted, or open as individually recorded. |

The fixtures (§16, pp. 24–27) compute a torus winding class $(2,-3)$ while
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
counterexample $x=-1$ to $\sqrt{x^2}=x$.

The paper also makes physical promotion deliberately expensive. Winding and
physical charge are different typed objects (§13, p. 21). A charge claim needs
a derived bridge from a gauge representation, action and current, Gauss law,
anomaly condition, boundary condition, or calibrated measurement protocol. The
application section therefore treats primordial-field toroidal models as
candidate topological and stabilization grammar, not as an established
derivation of quark charge, QCD, or hadron dynamics (§17, pp. 28–30).

Claims carry a categorical mathematical verdict plus separate mathematical,
empirical, computational, source, and transfer readiness (§2.2). A dependency
graph propagates only edge-specific readiness caps; it does not manufacture a
descendant verdict (§2.3). A theorem does not raise empirical readiness;
a hash establishes artifact identity rather than truth; a proof DAG is not
itself a proof; and an unexecuted numerical description remains unexecuted
(§14, pp. 21–23).

The appropriate test is narrow and adversarial. Ask whether an equivalent
compositional record already exists, whether any map is ill-typed, whether a
composition law fails, whether a fixture has a counterexample, or whether the
record changes no scientific decision. If an established formalism already
supplies the same obligations and demotion semantics, or if BSC never
distinguishes an invalid transfer from a nearby valid one, the additional
structure is unnecessary. If it exposes such a distinction and preserves it
through composition, that—not a claim about the universe—is the contribution
requiring further development.
