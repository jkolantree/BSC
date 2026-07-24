# Claim-Status Ledger

This ledger accompanies *On Boundaries of Evidence*, version 1.0.1. It is a
status record, not a substitute for proofs, sources, or receipts. A materially
repaired or restricted proposition receives a new identifier; the superseded
row remains visible.

## Status vocabulary

Mathematical verdict and mathematical support are separate:

- **Verdict:** ill-posed; open; true; false; N/A.
- **Math support:** none; conjectural; conditional; proved; N/A.
- **Empirical readiness:** contradicted; untested; single study; replicated;
  N/A.
- **Computational readiness:** failed; unexecuted; executed; exact receipt;
  N/A.
- **Source:** unchecked; internal; present proof; verified preprint; verified
  publication.
- **Transfer:** blocked; local only; bounded; certified; N/A.

The readiness vocabularies are policy orders, not truth orders. Dependency
propagation may cap support or block transfer. It never turns an unsupported
descendant into a false one. A mathematical verdict changes only through
claim-local evidence: a type argument, proof, counterexample, or explicit
reformulation.

## Foundational objects and formal consequences

| ID | Claim | Verdict | Math support | Empirical | Computational | Source | Transfer | Dependencies and demotion trigger |
|---|---|---|---|---|---|---|---|---|
| BSC-SYS-01 | The Volume I tuple is the original supplied BSC system object. | N/A | N/A | N/A | N/A | internal | local only | Transcribed from a hash-identified internal source not independently inspectable in this release; contrary source evidence changes the lineage record. |
| BSC-SYS-02 | The Volume II tuple is the supplied measurable repair adopted by Volume III. | N/A | N/A | N/A | N/A | internal | local only | Same public-inspection limitation as BSC-SYS-01; no external certification is claimed. |
| BSC-SYS-03 | A system-certificate companion can be associated without replacing the retained tuple. | true | proved | N/A | N/A | present proof | certified | BSC-SYS-02; treating it as an inherited tuple slot requires a new source claim. |
| BSC-OBS-01 | The observation atom freezes legal predictive information before the outcome. | open | conditional | untested | unexecuted | present proof | local only | Typed filtered probability space and adapted policy; any post-outcome feature, threshold, dictionary, or seed selection blocks use. |
| BSC-OBS-02 | Predictable sequential admission with conditional error $\alpha_t$ and $\sum_t\alpha_t\le\alpha$ controls the union probability by $\alpha$. | true | proved | N/A | N/A | present proof | certified | Predictability and the conditional bounds are indispensable. |
| BSC-QUO-01 | A quotient-respecting kernel descends uniquely through a standard Borel measurable quotient under the stated $q$-measurability condition. | true | proved | N/A | N/A | present proof | certified | Final sigma-algebra, standard Borel spaces, and fiber constancy. |
| BSC-QUO-02 | An $\varepsilon$-confusability relation is not generally an equivalence relation. | true | proved | N/A | N/A | present proof | certified | A restricted model may separately prove transitivity. |
| BSC-QOP-01 | Paired state-channel and observable-pullback descriptions give identical accessible probabilities. | true | proved | N/A | unexecuted | present proof | certified | Adjoint pairing and trace-class domains; no computation claimed. |
| BSC-QOP-02 | A transformed channel descends to an operational quotient iff it is constant on quotient fibers, under BSC-QUO-01. | true | proved | N/A | N/A | present proof | certified | Two quotient-equal inputs with different outputs refute descent. |
| BSC-MOR-01 | The eight-field morphism record is type-correct for the declared stochastic variant. | true | proved | N/A | N/A | present proof | local only | Every field, domain, observable direction, equation-space map, completion, and certificate must be declared. |
| BSC-MOR-02 | The v1.0.0 partial observable composite $T_{\ell m}^{\sharp}\circ T_{mn}^{\sharp}$ is well typed. | ill-posed | proved | N/A | unexecuted | present proof | blocked | The inner pullback lands in $B_b(D_{mn})$, outside the declared domain of the outer pullback. Superseded by BSC-MOR-05. |
| BSC-MOR-05 | With $D_{\ell n}=\{x\in D_{\ell m}:T_{\ell m}(x,D_{mn})=1\}$, the restricted pullback gives $T_{\ell n}^{\sharp}=T_{\ell m}^{\sharp\mid D_{mn}}\circ T_{mn}^{\sharp}$. | true | proved | N/A | unexecuted | present proof | certified | Measurable support domains and compatible completed interfaces; failure of either makes the composite undefined. |
| BSC-MOR-03 | Total-variation naturality defects obey the Dobrushin-weighted composition bound. | true | proved | N/A | unexecuted | present proof | bounded | BSC-MOR-05, a common observation square, and a defined Dobrushin coefficient. |
| BSC-MOR-04 | Deterministic target-equation residuals obey $R_{\ell n}=R_{mn}\circ T_{\ell m}+S_{mn}R_{\ell m}$. | true | proved | N/A | unexecuted | present proof | bounded | Deterministic compatible equation domains and bounded linear $S_{mn}$. |
| BSC-STA-01 | Directed deficiency composes by a triangle inequality. | true | proved | N/A | unexecuted | present proof | certified | Common parameter family or explicit pullback; simulation direction must be preserved. |
| BSC-STA-02 | $\delta(\mathsf E,\mathsf F)=0$ means arbitrarily accurate simulation of $\mathsf F$ from $\mathsf E$; exact simulation additionally requires attainment of the infimum or an applicable randomization theorem. | true | proved | N/A | unexecuted | verified publication | certified | It does not imply the reverse direction. |
| BSC-SHF-01 | Exact compatible sections of an actual sheaf glue uniquely. | true | proved | N/A | N/A | verified publication | certified | Actual sheaf and compatible cover. |
| BSC-SHF-02 | Locally nonempty relation data need not admit a global section. | true | proved | N/A | unexecuted | present proof | certified | Fixture F6. |
| BSC-OPN-01 | Decorated structured cospans form a category under the stated finite-colimit, adjoint, and lax-monoidal hypotheses. | true | proved | N/A | unexecuted | present proof | bounded | This is the generic conditional construction. |
| BSC-OPN-02 | The eight-field BSC records canonically instantiate the required decoration functor with coherent pushout transport. | open | conditional | N/A | unexecuted | present proof | blocked | A BSC-specific functor and coherence proof remain open. |
| BSC-DAG-01 | Readiness-cap propagation on a finite claim DAG has a unique greatest feasible readiness assignment below the inputs and edge constraints. | true | proved | N/A | unexecuted | present proof | certified | Finite DAG and finite readiness meet-semilattices; verdicts are unchanged. |

## Boundary, dynamics, scale, and persistence

| ID | Claim | Verdict | Math support | Empirical | Computational | Source | Transfer | Dependencies and demotion trigger |
|---|---|---|---|---|---|---|---|---|
| BSC-BND-01 | Trace, finite boundary-layer observation, boundary response, and reconstruction are distinct typed operations. | true | proved | N/A | N/A | present proof | certified | Declared function and data spaces. |
| BSC-BND-02 | A boundary response determines an interior coefficient in every finite open system. | false | proved | N/A | unexecuted | present proof | blocked | Fixture F2 is a counterexample to the universal form. |
| BSC-BND-03 | Published Calderón-type results support reconstruction in their stated regimes. | open | conditional | N/A | N/A | verified publication | local only | Dimension, coefficient class, data, gauge quotient, regularity, and stability theorem. |
| BSC-BND-04 | The v1.0.0 boundary-gain and exterior-residual pair is sufficient by itself to establish boundary sufficiency. | false | proved | untested | unexecuted | present proof | blocked | It can leave undeclared interior predictive information. Superseded by BSC-BND-05. |
| BSC-BND-05 | $G_\partial$ and $S_{\rm ext}^{\rm aug}$ are necessary noncompensating screens; target-relative boundary sufficiency additionally requires a declared remainder test $S_{\rm rest}$. | true | conditional | untested | unexecuted | present proof | local only | Legal conditioning, existence of the information quantities, and claim-specific tolerances; none proves causality or PDE reconstruction. |
| BSC-KOO-01 | The Koopman action is $g\mapsto g\circ F$. | true | proved | N/A | N/A | verified publication | certified | Measurable dynamics and a declared observable space. |
| BSC-KOO-02 | Residual-controlled Koopman algorithms avoid spectral pollution for their covered information/problem classes. | true | proved | N/A | unexecuted | verified publication | local only | Cited access and problem hypotheses; published computations were not rerun. |
| BSC-KOO-03 | One universal Koopman learner succeeds on all broad dynamical classes covered by the cited impossibility results. | false | proved | N/A | unexecuted | verified publication | blocked | Stronger structural assumptions define a different claim. |
| BSC-REC-01 | Endpoint recurrence is weaker than prefix persistence. | true | proved | N/A | N/A | present proof | certified | Declared identity query and viability tube. |
| BSC-REC-02 | The homogeneous prefix upper bound follows from $E_{i+1}\le L_iE_i+e_i$. | true | proved | N/A | unexecuted | present proof | bounded | An upper bound below tolerance certifies; one above tolerance is inconclusive, not a refutation. |
| BSC-REC-03 | Persistent objects are recursively maintained finite boundary-states across claim-admissible folds. | open | conjectural | untested | unexecuted | internal | local only | BSC-MOR-01, BSC-MOR-03–05, BSC-REC-01–02, and claim-specific gates; a proved lower-bound violation blocks the affected prefix. |
| BSC-SCL-01 | Dynamical scale defects accumulate geometrically under a uniform one-step bound and target Wasserstein Lipschitz constant. | true | proved | N/A | unexecuted | present proof | bounded | Finite moments, uniform domain, and target Lipschitz bound. |
| BSC-SCL-04 | The stated periodic elliptic equations homogenize to the declared cell-problem tensor under the fixed hypotheses. | true | proved | N/A | unexecuted | verified publication | local only | No universal rate or changing-domain conclusion is inherited. |
| BSC-SCL-02 | Homogenization is a universal micro-to-macro derivation independent of scale, boundaries, and topology of convergence. | false | proved | N/A | N/A | verified publication | blocked | Published theorems require those data. |
| BSC-SCL-03 | The cited Deng–Hani–Ma program settles all of Hilbert’s sixth problem. | false | proved | N/A | unexecuted | verified preprint | blocked | The version-pinned preprints state a narrower program. |

## Topology, physics, and applications

| ID | Claim | Verdict | Math support | Empirical | Computational | Source | Transfer | Dependencies and demotion trigger |
|---|---|---|---|---|---|---|---|---|
| BSC-TOP-01 | The fixture curve has homology class $(2,-3)\in H_1(T^2;\mathbb Z)$. | true | proved | N/A | unexecuted | present proof | certified | Fixture F1 inputs and orientation. |
| BSC-TOP-02 | Integer winding alone selects a unique electric charge. | false | proved | untested | unexecuted | present proof | blocked | The normalization/bridge map $\chi$ is underdetermined. |
| BSC-TOP-03 | A topology-to-charge promotion may be evaluated when a typed, normalized physical bridge is derived. | open | conditional | N/A | N/A | present proof | local only | Gauge/action/current/anomaly/boundary/measurement structure, units, and normalization. |
| BSC-QCD-01 | Controlled monopole–center-vortex work supplies the listed structures and calculations in its declared regimes. | open | conditional | N/A | unexecuted | verified publication | local only | Compactified/semiclassical hypotheses; no extrapolation to undeformed strong-coupling $\mathbb R^4$. |
| BSC-QCD-02 | Those controlled results prove all physical $\mathbb R^4$ QCD confinement and hadron spectroscopy. | false | proved | untested | unexecuted | verified publication | blocked | Required regime and spectroscopy bridges are absent. |
| BSC-PF-01 | Klingman’s papers contain a candidate topological carrier and stabilization grammar, including a later qualitative solenoidal analogy. | true | proved | untested | unexecuted | verified publication | local only | The 2025 source labels quantitative development incomplete. |
| BSC-PF-02 | Klingman’s present papers derive quark charge, QCD, and hadron dynamics. | ill-posed | proved | untested | unexecuted | verified publication | blocked | The typed action, currents, anomaly, spin, color, confinement, running, spectra, scattering, and falsifier bridges are absent. |
| BSC-HOL-01 | This BSC manuscript proves holography. | false | proved | untested | unexecuted | present proof | blocked | Manuscript inspection finds no bulk/boundary dictionary or reconstruction theorem. |
| BSC-NIS-01 | Non-invertible defects can have fusion not described by an ordinary group. | true | proved | N/A | unexecuted | verified publication | local only | Theory-specific defect category and anomaly data. |
| BSC-GL-01 | The checked five-paper program concerns categorical global unramified geometric Langlands in its specified setting. | true | conditional | N/A | unexecuted | verified preprint | local only | Version-pinned preprints; proofs were not rebuilt. |
| BSC-KAK-01 | The checked Wang–Zahl and streamlined preprints claim the Kakeya conjecture in $\mathbb R^3$. | open | conditional | N/A | unexecuted | verified preprint | local only | No peer-review or higher-dimensional promotion is claimed. |

## Fixture ledger

| ID | Fixture result | Verdict | Math support | Computational | Permanent expected output | Failure status |
|---|---|---|---|---|---|---|
| BSC-FIX-01 | Torus winding $(2,-3)$; electric charge blocked without $\chi$. | true | proved | unexecuted | $(2,-3)$ and blocked charge transfer | Any charge scalar without a derived bridge. |
| BSC-FIX-02 | Distinct conductivities have the same one-dimensional DN map. | true | proved | unexecuted | $R_{\gamma_1}=R_{\gamma_2}=1$ | Profile-identifiability claim fails. |
| BSC-FIX-03 | The perfect binary experiment dominates the $1/4$-noise experiment. | true | proved | unexecuted | directed deficiencies $(0,1/4)$ | Reversed direction or symmetric use of $\delta$. |
| BSC-FIX-04 | A two-sided-shift pseudomode has residual $\sqrt{2/N}$ while the finite compression pollutes at $0$. | true | proved | unexecuted | residual $\sqrt{2/N}$; compressed spectrum $\{0\}$ | Exact-eigenmode promotion. |
| BSC-FIX-05 | Transform–discard does not factor through the reduced-system quotient on the invariant Bell-state class. | true | proved | unexecuted | common input $I/2$; outputs $|0\rangle\langle0|$ and $|1\rangle\langle1|$; trace distance $1$ | A reduced channel producing both outputs from the same input. |
| BSC-FIX-06 | Three locally nonempty parity relations have no global section. | true | proved | unexecuted | cycle parity $1$; empty inverse limit | Local plausibility promoted globally. |
| BSC-FIX-07 | A massive-field constant shift has residual $m^2c$. | true | proved | unexecuted | $L^2$ residual $m^2|c|$ on $(0,1)$ | Symmetry claim for $m>0,c\ne0$. |
| BSC-FIX-08 | $x=-1$ refutes $\forall x\in\mathbb R,\sqrt{x^2}=x$. | true | proved | exact receipt | `counterexample_confirmed`; schema and independent semantic checks pass | Any regression accepting the universal identity. |

## Mechanical, empirical, and release claims

| ID | Claim | Verdict | Math support | Empirical | Computational | Source | Transfer | Demotion trigger |
|---|---|---|---|---|---|---|---|---|
| BSC-CERT-01 | A kernel-accepted proof object supports its encoded proposition relative to declared definitions and axioms. | open | conditional | N/A | N/A | verified publication | local only | Kernel rejection, hidden axioms, or encoding mismatch. |
| BSC-CERT-02 | A proof DAG is itself a proof. | false | proved | N/A | N/A | present proof | blocked | A DAG records dependencies only. |
| BSC-CERT-03 | A hash proves scientific validity. | false | proved | N/A | N/A | present proof | blocked | A hash establishes identity/integrity only. |
| BSC-CERT-04 | Fixture F8 has a deterministic retained receipt. | true | proved | N/A | exact receipt | internal | certified | Script, schema, semantic, or byte-reproduction failure. |
| BSC-EMP-01 | The supplied internal corpus contains independently inspectable executed empirical validation of its broad proposals. | N/A | N/A | untested | unexecuted | internal | blocked | New public data and inspectable receipts require new rows. |
| BSC-REL-01 | The immutable v1.0.0 release bytes and public DOI record are intact. | true | proved | N/A | exact receipt | present proof | certified | Fresh checksum and public-record audit on 24 July 2026. |
| BSC-REL-02 | The v1.0.0 Markdown, manifest, F8 checker, and CI gates were fully fail-closed. | false | proved | N/A | executed | present proof | blocked | Negative regression tests found literal GitHub math, unlisted-file acceptance, and two F8 mutants. Superseded by the v1.0.1 gates. |

## Dependency policy

1. Mathematical verdict does not propagate by meet. A descendant becomes false
   only through descendant-level refuting evidence.
2. Edge-specific monotone caps may reduce mathematical support or other
   readiness coordinates and may block transfer.
3. Computational readiness requires execution artifacts and receipts; prose
   and pseudocode remain unexecuted.
4. Source status records provenance separately from truth.
5. Empirical readiness never rises because a theorem was proved.
6. Transfer is restricted to the declared domain, scale, instrument, boundary
   conditions, horizon, and claim-specific tolerances.
7. A changed proposition receives a new stable identifier.
