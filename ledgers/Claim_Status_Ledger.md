# Claim-Status Ledger

This ledger accompanies *On Boundaries of Evidence*. It is a status record, not
a substitute for the proofs, sources, or receipts. Each row has a stable claim
identifier. A repaired or materially restricted proposition receives a new
identifier rather than silently inheriting the old one.

## Axis vocabulary

- **Mathematical:** ill-posed; refuted; conjectural; conditional; proved.
- **Empirical:** contradicted; untested; single study; replicated; N/A.
- **Computational:** failed; unexecuted; executed; exact receipt; N/A.
- **Source:** unchecked; internal; present proof; verified preprint; verified
  publication.
- **Transfer:** blocked; local only; bounded; certified; N/A.

Statuses are not averaged. “Proved / untested” is coherent. “Published / blocked”
is coherent. A downstream claim receives no higher status on a named dependency
axis than its weakest undischarged predecessor.

## Foundational objects and formal consequences

| ID | Claim | Mathematical | Empirical | Computational | Source | Transfer | Dependencies | Demotion trigger |
|---|---|---|---|---|---|---|---|---|
| BSC-SYS-01 | The Volume I tuple is the original authoritative BSC system object. | proved | N/A | N/A | internal | local only | supplied Volume I, directly checked; mathematical status records the source fact | Source mismatch or a higher-authority corpus document explicitly retracting it. |
| BSC-SYS-02 | The Volume II tuple is the current measurable repair, and Volume III adopts it. | proved | N/A | N/A | internal | certified | Volumes II–III, directly checked; certification is limited to this manuscript’s notation | Contrary authoritative lineage evidence. |
| BSC-SYS-03 | The system-certificate companion can be associated without replacing the retained tuple. | proved | N/A | N/A | present proof | certified | BSC-SYS-02; present bookkeeping construction | Treating the companion as an inherited tuple slot without explicit revision. |
| BSC-OBS-01 | The observation atom freezes legal predictive information before the outcome. | conditional | untested | unexecuted | present proof | local only | BSC-SYS-02; internal antecedent and present protocol repair; generic implementation not tested or executed | Post-outcome feature, threshold, dictionary, or seed selection. |
| BSC-OBS-02 | Predictable sequential admission with conditional error \(\alpha_t\) and \(\sum\alpha_t\le\alpha\) controls the union probability by \(\alpha\). | proved | N/A | N/A | present proof | certified | filtration and conditional error hypotheses; internal antecedent; certification is assumption-bound | Nonpredictable \(\alpha_t\), invalid conditional bounds, or undeclared adaptive access. |
| BSC-QUO-01 | A quotient-respecting kernel descends uniquely through a standard Borel measurable quotient under the stated \(q\)-measurability condition. | proved | N/A | N/A | present proof | certified | final sigma-algebra; standard Borel spaces; coordinate \(q\)-measurability; classical antecedent; certification is restricted to this setting | Singular quotient, nonmeasurable coordinates, or a kernel varying on a fiber. |
| BSC-QUO-02 | An \(\varepsilon\)-confusability relation is not generally an equivalence relation. | proved | N/A | N/A | present proof | certified | general metric counterexamples; internal repair adopted in the present definition | A separate proof of transitivity for a restricted model. |
| BSC-QOP-01 | Paired state-channel and observable-pullback descriptions give identical accessible probabilities. | proved | N/A | unexecuted | present proof | certified | adjoint pairing and trace-class domains; verified publications; symbolic derivation only, with no execution claimed | Domain failure or use of unpaired observables. |
| BSC-QOP-02 | A transformed channel descends to an operational quotient iff it is constant on quotient fibers, under BSC-QUO-01 hypotheses. | proved | N/A | N/A | present proof | certified | BSC-QUO-01 | Two quotient-equivalent inputs with distinct transformed outputs. |
| BSC-MOR-01 | The eight-field morphism record is type-correct for the declared stochastic variant. | proved | N/A | N/A | present proof | local only | all field domains and completion record; present construction remains local until instantiated | Any absent domain, observable direction, equation-space map, carrier, or certificate field. |
| BSC-MOR-02 | Stochastic morphism composition has \(T_{\ell n}=T_{mn}\odot T_{\ell m}\), \(T_{\ell n}^{\sharp}=T_{\ell m}^{\sharp}\circ T_{mn}^{\sharp}\), and the analogous post-processor law. | proved | N/A | unexecuted | present proof | certified | BSC-MOR-01; compatible interface and clocks; classical kernel-composition antecedent; symbolic derivation only; certification requires completion compatibility | Intermediate-domain failure or incompatible completion. |
| BSC-MOR-03 | Total-variation naturality defects obey the Dobrushin-weighted composition bound. | proved | N/A | unexecuted | present proof | bounded | BSC-MOR-02; common observation square; Dobrushin coefficient; symbolic derivation only | Mismatched metrics/domains or an unbounded/undefined contraction factor. |
| BSC-MOR-04 | Deterministic target-equation residuals obey \(R_{\ell n}=R_{mn}\circ T_{\ell m}+S_{mn}R_{\ell m}\). | proved | N/A | unexecuted | present proof | bounded | deterministic maps; compatible equation domains; bounded linear \(S_{mn}\); typed equation-space transports; symbolic derivation only | Missing or unbounded \(S_{mn}\), stochastic/nonlinear residual substituted without a weak formulation, or domain failure. |
| BSC-STA-01 | Directed deficiency composes by a triangle inequality. | proved | N/A | unexecuted | present proof | certified | same \(\Theta\) or explicit parameter pullback; verified publications; fixture F3 gives an exact rational derivation but no execution receipt; certification is for a common parameter family | Parameter mismatch or reversed simulation direction. |
| BSC-STA-02 | \(\delta(\mathsf E,\mathsf F)=0\) means \(\mathsf E\) can simulate \(\mathsf F\); it need not mean the reverse. | proved | N/A | unexecuted | verified publication | certified | stated Le Cam convention; fixture F3 gives an exact rational derivation but no execution receipt | Calling the directed quantity symmetric. |
| BSC-SHF-01 | Exact compatible sections of an actual sheaf glue uniquely. | proved | N/A | N/A | verified publication | certified | actual sheaf and compatible cover; the result is the sheaf axiom restated in the manuscript | Only a presheaf/relation assignment, noisy mismatch, or failed compatibility. |
| BSC-SHF-02 | Locally nonempty relation data need not admit a global section. | proved | N/A | unexecuted | present proof | certified | fixture F6 supplies an exact finite derivation but no execution receipt | None for the stated parity fixture; a modified relation is a new claim. |
| BSC-OPN-01 | The constructed typed structured cospans form a category under the stated finite-colimit and lax-monoidal-decoration hypotheses. | proved | N/A | unexecuted | present proof | bounded | finite colimits; left-adjoint interface embedding; fixed mode and clock; declared lax symmetric monoidal decoration functor; verified publications | A purported instance without the required functorial pushout transport, or an untyped mixed-mode composition. |
| BSC-DAG-01 | Axiswise meet propagation on a finite claim DAG terminates at the unique greatest feasible status below the inputs. | proved | N/A | unexecuted | present proof | certified | finite DAG and finite meet-semilattices; symbolic derivation only | Cyclic dependency graph or a status domain without the required meets. |

## Boundary, dynamics, scale, and persistence

| ID | Claim | Mathematical | Empirical | Computational | Source | Transfer | Dependencies | Demotion trigger |
|---|---|---|---|---|---|---|---|---|
| BSC-BND-01 | Trace, finite boundary-layer observation, boundary response, and reconstruction are distinct typed operations. | proved | N/A | N/A | present proof | certified | declared function/data spaces; present typing construction; verified publications | Reusing one operator across incompatible domains without a bridge. |
| BSC-BND-02 | A boundary response determines an interior coefficient in every finite open system. | refuted | N/A | unexecuted | present proof | blocked | fixture F2 supplies the mathematical counterexample; verified inverse-problem literature; the universal claim would require a PDE, data class, quotient, regularity, and stability theorem; exact symbolic fixture only, with no execution receipt | Fixture F2 already refutes the universal form. |
| BSC-BND-03 | Published Calderón-type uniqueness results support scoped reconstruction claims. | conditional | N/A | N/A | verified publication | local only | dimension, coefficient class, boundary data, gauge quotient; empirical and computational status are problem-specific and not asserted generically | Application outside the theorem’s regularity/dimension/data regime. |
| BSC-BND-04 | Boundary gain plus low exterior residual is a target-relative statistical sufficiency gate. | conditional | untested | unexecuted | present proof | local only | valid mutual information model and legal conditioning; internal repair and present diagnostic definition; generic implementations remain untested and unexecuted | High exterior residual, leakage, or interpreting the diagnostic as PDE reconstruction. |
| BSC-KOO-01 | The Koopman action on observables is \(g\mapsto g\circ F\). | proved | N/A | N/A | verified publication | certified | measurable dynamics and chosen observable space; the action is definitional/classical | Domain/invariance failure. |
| BSC-KOO-02 | Residual-controlled Koopman algorithms can avoid spectral pollution for their covered information/problem classes. | proved | N/A | unexecuted | verified publication | local only | cited hypotheses and access model; published numerical methods were not rerun here | Application without the required residual/data access or outside the stated class. |
| BSC-KOO-03 | A universal single-procedure Koopman learner succeeds for all declared broad dynamical classes. | refuted | N/A | unexecuted | verified publication | blocked | exact problem and access class; refutation is restricted to the task classes covered by the cited impossibility results; adversarial source constructions were not rerun here | Stronger structure defines a different learnability claim. |
| BSC-REC-01 | Endpoint recurrence is weaker than prefix persistence. | proved | N/A | N/A | present proof | certified | declared identity query and viability tube; proof is by the definitions and possible excursion–return paths; internal repair adopted | A restricted dynamics theorem that forbids intermediate excursion. |
| BSC-REC-02 | The homogeneous identity-error prefix bound follows from \(E_{i+1}\le L_iE_i+e_i\). | proved | N/A | unexecuted | present proof | bounded | common units and declared \(L_i\); symbolic derivation only | Mixing residual, deficiency, viability, or source status into the scalar. |
| BSC-REC-03 | Persistent objects are recursively maintained finite boundary-states across admissible folds. | conjectural | untested | unexecuted | internal | local only | BSC-MOR-01–04; BSC-REC-01–02; claim-specific evidence; organizing definition and conjectural physical principle from internal synthesis, formally stated here; generic implementations are unexecuted | Any required prefix tolerance, viability gate, certificate, or physical bridge fails. |
| BSC-SCL-01 | Dynamical scale defects accumulate geometrically under a uniform one-step bound and target Wasserstein Lipschitz constant. | proved | N/A | unexecuted | present proof | bounded | finite moments, uniform domain, Lipschitz target kernel; internal antecedent; symbolic derivation only | Loss of moment control, uniformity, or the target Lipschitz bound. |
| BSC-SCL-04 | Uniformly elliptic periodic divergence-form equations homogenize to the declared cell-problem tensor under the manuscript’s fixed-domain, fixed-data, Dirichlet hypotheses. | proved | N/A | unexecuted | verified publication | local only | bounded Lipschitz domain; periodic symmetric measurable coefficients; uniform ellipticity; fixed \(f\in H^{-1}\); standard corrector theorem | Quantitative rate, changing domains/data, degeneracy, randomness, nonlinear coupling, or oscillating boundaries without a new theorem. |
| BSC-SCL-02 | Homogenization supplies a universal micro-to-macro derivation independent of scaling, boundary conditions, and convergence topology. | refuted | N/A | N/A | verified publication | blocked | the universal claim is ill-posed without a scale-limit certificate and is contradicted by the hypotheses of verified literature; it would require a nonexistent universal theorem | Any use without a scale-limit certificate. |
| BSC-SCL-03 | The Deng–Hani–Ma program settles all of Hilbert’s sixth problem. | refuted | N/A | unexecuted | verified preprint | blocked | specified hard-sphere/kinetic/fluid program only; the overbroad statement was not rerun and is not claimed by the preprints | The preprints themselves do not claim the universal form. |

## Topology, physics, and application claims

| ID | Claim | Mathematical | Empirical | Computational | Source | Transfer | Dependencies | Demotion trigger |
|---|---|---|---|---|---|---|---|---|
| BSC-TOP-01 | The fixture curve has homology class \((2,-3)\in H_1(T^2;\mathbb Z)\). | proved | N/A | unexecuted | present proof | certified | fixture F1 inputs and orientation; symbolic calculation only; certification is topological | Input/orientation change creates a new claim. |
| BSC-TOP-02 | Integer winding alone selects a unique electric charge. | refuted | untested | unexecuted | present proof | blocked | missing \(\chi\); present no-go proof establishes underdetermination | A physically derived, normalized bridge creates a new scoped claim. |
| BSC-TOP-03 | A topological-to-physical charge map may be admitted when derived from a declared gauge/action/current/anomaly/boundary/measurement structure. | conditional | N/A | N/A | present proof | local only | certified \(\chi\) and its physical dependencies; present admission-rule construction; empirical and computational status are problem-specific; transfer remains local until instantiated | Arbitrary normalization, missing units, anomaly failure, or unmatched measurement. |
| BSC-QCD-01 | Controlled monopole–center-vortex work supplies gauge group, action, compactification, flux, fractional topology, anomaly data, and string-tension calculations in declared regimes. | conditional | N/A | unexecuted | verified publication | local only | cited compactified/semiclassical assumptions; this is a theory comparison, not a new empirical result, and calculations were not rerun here | Extrapolation to undeformed strong-coupling \(\mathbb R^4\) without a bridge. |
| BSC-QCD-02 | Those controlled results prove all physical \(\mathbb R^4\) QCD confinement and hadron spectroscopy. | refuted | untested | unexecuted | verified publication | blocked | missing adiabatic/strong-coupling and spectroscopy bridges; the overbroad inference is unsupported and contradicted by the cited source scope | New rigorous or empirical bridges would define narrower promoted claims. |
| BSC-PF-01 | Klingman’s papers contain a candidate topological carrier and stabilization grammar. | proved | untested | unexecuted | verified publication | local only | checked primary proposal; accurate extraction and classification of field, torus, duality, winding, and stabilization claims | Misquotation or absence of the claimed candidate structure. |
| BSC-PF-02 | Klingman’s current papers derive quark electric charge, QCD, and hadron dynamics. | ill-posed | untested | unexecuted | verified publication | blocked | checked primary proposal; the claimed derivation lacks a typed action, gauge current, anomaly, spin, color, confinement, running, spectra, and scattering bridges | A newly typed and fully discharged bridge satisfying the manuscript’s obligation table creates a different scoped claim. |
| BSC-HOL-01 | BSC proves holography. | refuted | untested | unexecuted | unchecked | blocked | no supporting source; missing bulk/boundary theories, code subspace, dictionary, limit, and reconstruction theorem | A domain-specific theorem cannot be inherited from generic boundary notation. |
| BSC-NIS-01 | Non-invertible defects can have fusion not described by an ordinary group. | proved | N/A | unexecuted | verified publication | local only | constructed theory-specific QFT examples; specified QFT/defect category/anomaly; cited constructions were not rerun | Using schematic integer fusion without the model or with TFT-valued multiplicities omitted. |
| BSC-GL-01 | The checked five-paper geometric Langlands program concerns categorical global unramified geometric Langlands in a specified setting. | proved | N/A | unexecuted | verified preprint | local only | five-paper program and definitions; mathematical status records the checked source-scope statement; the program was not rebuilt | Promotion to arithmetic Langlands or all local/ramified forms. |
| BSC-KAK-01 | The Wang–Zahl and streamlined works claim the Kakeya conjecture in \(\mathbb R^3\). | conditional | N/A | unexecuted | verified preprint | local only | \(\mathbb R^3\) preprint proof claim; the proofs were not rebuilt | Calling it peer reviewed, extending to \(n\ge4\), or importing adjacent conjectures. |

## Fixture ledger

| ID | Fixture result | Mathematical | Computational | Permanent expected output | Failure status |
|---|---|---|---|---|---|
| BSC-FIX-01 | Torus winding \((2,-3)\); electric charge blocked without \(\chi\). | proved | unexecuted | \((2,-3)\), transfer blocked; symbolic derivation only | Any electric-charge scalar without a bridge. |
| BSC-FIX-02 | Two distinct conductivities have identical one-dimensional DN maps. | proved | unexecuted | \(R_{\gamma_1}=R_{\gamma_2}=1\), \(\Lambda_{\gamma_1}=\Lambda_{\gamma_2}\); symbolic derivation only | Profile-identifiability claim refuted. |
| BSC-FIX-03 | Perfect binary experiment Blackwell-dominates the \(1/4\)-noise experiment; directed deficiencies \(0\) and \(1/4\). | proved | unexecuted | \((0,1/4)\) in the declared direction; exact rational derivation, with no execution receipt | Reversed direction or symmetric use of \(\delta\). |
| BSC-FIX-04 | Two-sided-shift pseudomode residual \(\sqrt{2/N}\); finite compression pollutes at \(0\). | proved | unexecuted | residual \(\sqrt{2/N}\), compressed eigenvalues all \(0\); symbolic derivation only | Exact-eigenmode or physical-decay promotion. |
| BSC-FIX-05 | In the finite \(\mathbb Z_2\) QRF fixture, transform–discard does not factor through the reduced system quotient. | proved | unexecuted | quotient-equal inputs produce \(I/2\) and \(|0\rangle\langle0|\), trace distance \(1/2\); the pulled observable algebra is relational and invariant; exact matrix/ket derivation, not separately scripted | A frame-independent reduced channel on the stated two-state class. |
| BSC-FIX-06 | Three locally nonempty parity relations have empty global inverse limit. | proved | unexecuted | cycle parity \(1\), no global section; exact finite derivation, with no execution receipt | Local plausibility promoted to global state. |
| BSC-FIX-07 | Massive-field constant shift has residual \(m^2c\). | proved | unexecuted | \(L^2\)-residual \(m^2|c|\) on \((0,1)\); symbolic derivation only | Alleged symmetry for \(m>0,c\ne0\). |
| BSC-FIX-08 | \(\forall x\in\mathbb R,\sqrt{x^2}=x\) is refuted by \(x=-1\). | proved | exact receipt | `counterexample_confirmed`; the underlying universal claim is refuted; receipt SHA-256 `7b7d416914068b1e1e5510b5658f82d17c9615bfa6954ec5facfb6eeb0f43333` | Any regression returning the false universal identity. |

## Mechanical and empirical claims

| ID | Claim | Mathematical | Empirical | Computational | Source | Transfer | Demotion trigger |
|---|---|---|---|---|---|---|---|
| BSC-CERT-01 | A kernel-accepted proof object in a pinned environment supports the encoded proposition relative to definitions and imported axioms. | conditional | N/A | N/A | verified publication | local only | Conditional metatheoretic claim; an instantiated mechanical-verification claim additionally requires an exact execution receipt. Kernel rejection, unpinned dependencies, hidden axioms, or mismatch between encoding and intended physical claim. |
| BSC-CERT-02 | A proof DAG is itself a proof. | refuted | N/A | N/A | present proof | blocked | Present distinction: a DAG provides dependency structure only. |
| BSC-CERT-03 | A hash proves scientific validity. | refuted | N/A | N/A | present proof | blocked | Present distinction: a hash establishes identity/integrity only. |
| BSC-CERT-04 | Fixture F8 has an actual deterministic execution receipt. | proved | N/A | exact receipt | internal | certified | Retained artifact and present execution; certification is for F8 only. Script or receipt hash mismatch, changed environment without a new receipt, or nonidentical repeat output. |
| BSC-EMP-01 | The supplied BSC corpus reports executed empirical validation of its human, biological, civic, optical, or physical proposals. | refuted | untested | unexecuted | internal | blocked | Complete internal-source audit found untested proposals and predominantly unexecuted computations. New supplied data and independently inspectable receipts would create new claim rows. |

## Dependency policy

1. The **mathematical** coordinate of a physical claim depends on its typed
   physical bridge, not merely on the topological or statistical antecedent.
2. The **computational** coordinate depends on execution artifacts and receipts;
   prose, pseudocode, and stated outputs leave it unexecuted.
3. The **source** coordinate records publication status separately from truth.
4. The **empirical** coordinate never rises because a mathematical theorem was
   proved.
5. The **transfer** coordinate is restricted to the certified domain, scale,
   instrument, boundary conditions, and horizon.
6. New evidence can promote a row only after its identifier, dependencies,
   assumptions, and artifacts are updated. A change in proposition creates a
   new row.
