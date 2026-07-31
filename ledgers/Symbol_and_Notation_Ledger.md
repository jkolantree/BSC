# Symbol and Notation Ledger

The released version for this normative ledger is 1.4.0 of *On
Boundaries of Evidence*, released 31 July 2026 at
`https://github.com/jkolantree/BSC/releases/tag/v1.4.0`. The Zenodo concept DOI
is `10.5281/zenodo.21541160`; the v1.4.0 version DOI assigned after the tagged
bytes were built is recorded on the GitHub release page. The immutable v1.3.0
version DOI is `10.5281/zenodo.21713285`; the immutable v1.2.0 version DOI is
`10.5281/zenodo.21711341`; the immutable v1.1.0 version DOI is
`10.5281/zenodo.21710743`, and the immutable v1.0.1 version DOI remains
`10.5281/zenodo.21541561`. A symbol has no meaning outside the row or local
declaration that types
it. Local specializations are permitted only when their scope is explicit.

The operational-channel and electromagnetic symbols below remain the
version `1.3.0` additions.

## Global conventions

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $\ell,m,n,a,b$ | scale or description labels | Labels, not necessarily real-valued scales. A numerical scale parameter is declared separately. |
| $t,h$ | time and prediction horizon | $t$ belongs to the declared time object; $h>0$ is the repaired horizon symbol. The source-only target record used $H$ for the horizon; the manuscript quotes that record before replacing $H$ by $h$. |
| $X\rightsquigarrow Y$ | Markov kernel | Measurable map $x\mapsto K(x,\cdot)\in\mathcal P(Y)$. |
| $L\odot K$ | composite kernel | $(L\odot K)(x,A)=\int L(y,A)K(x,dy)$. |
| $\delta_f$ | deterministic kernel | Dirac kernel induced by measurable $f$. |
| $f_\sharp\mu$ | probability measure | Pushforward of $\mu$ by $f$. |
| $B_b(X)$ | vector space | Bounded Borel real- or complex-valued functions on $X$. |
| $\lVert \cdot\rVert_{\mathrm{TV}}$ | $[0,1]$ | Total variation; for finite distributions, one half of the $\ell^1$ distance. |
| $W_p$ | $[0,\infty]$ | $p$-Wasserstein distance on a declared metric space; finite-moment assumptions required. |
| $W_{p,Q}$ | $[0,\infty]$ | $p$-Wasserstein distance on the specifically declared metric space $(Q,d_Q)$, with domain $\mathcal P_p(Q)\times\mathcal P_p(Q)$. The subscript $Q$ may be suppressed only inside a scope where the ground metric is unambiguous. |
| $\mathbb P,\mathbb E$ | probability, expectation | Always relative to the locally declared law. |
| $\mathrm{Tr}$ | scalar | Trace on the locally declared trace-class/operator pairing. |
| $\mathrm{id},\mathrm{Id}$ | identity | Identity map or identity operator, clear from type. |
| $\preceq,\bigwedge$ | readiness order and meet | Used only on declared readiness semilattices, not on mathematical verdicts and not as numerical inequality. |

## Retained BSC system objects

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $S_\ell(t)$ | 12-field record | Original Volume I system tuple, transcribed in manuscript equation (4.1) from a hash-identified supplied source that is not independently inspectable in this release. |
| $\widehat S_\ell$ | 14-field record | Supplied measurable repair from Volume II, described by Volume III as adopted and transcribed in equation (4.2), subject to the same source-availability limitation. |
| $\Omega_\ell$ | bounded domain or finite carrier | “Finite” may refer to domain, horizon, resources, or cardinality; the intended meaning must be stated. |
| $\partial\Omega_\ell$ | geometric boundary | Used only when a geometric boundary is part of the model. |
| $\partial_\varepsilon\Omega_\ell$ | measurable sensor layer | $\lbrace x:\mathrm{dist}(x,\partial\Omega_\ell)\le\varepsilon\rbrace$ when geometric; not an ideal trace. |
| $X_\ell$ | standard Borel space | Raw states. |
| $\sim_\ell$ | measurable exact equivalence relation | Gauge, observational, or representational equivalence. |
| $\bar X_\ell=X_\ell/{\sim_\ell}$ | standard Borel quotient when used | The final sigma-algebra and quotient measurability are required. |
| $q_\ell^{\mathrm{quot}}$ | $X_\ell\to\bar X_\ell$ | Canonical measurable quotient map. In a system-quotient-only scope the superscript may be omitted; it must be restored wherever an identity observable is also present. |
| $U_\ell$ | standard Borel space | Legal controls or interventions. |
| $Y_\ell$ | standard Borel space | Instrument outputs. |
| $C_\ell$ | structured standard Borel space | Physical configuration containing context, calibration, instrument, observer/reference frame, controller, and clock state. Distinct from interscale completion $C_{\ell m}$. |
| $(\Xi_\ell,\mathscr A_\ell,\mathbb P_\ell)$ | probability space | Carries the random states, controls, contexts, observations, and history variables for experiment $\ell$. |
| $\mathscr F_{\ell,t}$ | sub-sigma-algebra of $\mathscr A_\ell$ | Legal information through time $t$; increasing in $t$. |
| $\mathscr F_{\ell,t-}$ | sigma-algebra | $\sigma(\bigcup_{s<t}\mathscr F_{\ell,s})$, or the separately declared left-limit filtration for the time object. |
| $(\mathsf H_{\ell,t},\mathscr H_{\ell,t})$ | standard Borel history space | Measurable codomain of the legal history variable. |
| $\mathbf H_{\ell,t}$ | $\Xi_\ell\to\mathsf H_{\ell,t}$ | $\mathscr F_{\ell,t}/\mathscr H_{\ell,t}$-measurable history variable. |
| $K_{\ell,t}^{X}$ | $X_\ell\times U_\ell\times C_\ell\rightsquigarrow X_\ell$ | Raw state-transition kernel. It descends only if it is lumpable through $q_\ell^{\mathrm{quot}}$. |
| $H_{\ell,t}^{X}$ | $X_\ell\times U_\ell\times C_\ell\rightsquigarrow Y_\ell$ | Raw instrument kernel. It descends only if it is constant on $\sim_\ell$-classes for every legal $(u,c)$. |
| $K_{\ell,t}^{\mathrm{dyn}}$ | $\bar X_\ell\times U_\ell\times C_\ell\rightsquigarrow\bar X_\ell$ | Descended local dynamics, defined only after lumpability. The superscript prevents collision with $K_{\ell m}$. |
| $H_{\ell,t}^{\mathrm{obs}}$ | $\bar X_\ell\times U_\ell\times C_\ell\rightsquigarrow Y_\ell$ | Descended instrument-dependent observation channel, defined only after observation invariance. |
| $\pi_{\ell,t}$ | $(\mathsf H_{\ell,t},\mathscr H_{\ell,t})\rightsquigarrow U_\ell\times C_\ell$ | History policy. The implemented randomized law is $\pi_{\ell,t}(\mathbf H_{\ell,t},\cdot)$ and is adapted. A policy not factoring through $\mathbf H_{\ell,t}$ must be declared as an $\mathscr F_{\ell,t}$-measurable random kernel on $\Xi_\ell$. |
| $\bar\pi_{\ell,t}$ | $\bar X_\ell\rightsquigarrow U_\ell\times C_\ell$ | Declared state-Markov control/context policy, or a proved reduction of $\pi_{\ell,t}$. No such reduction is presumed. |
| $J_{\bar\pi_{\ell,t}}$ | $\bar X_\ell\rightsquigarrow\bar X_\ell\times U_\ell\times C_\ell$ | Policy lift $J_{\bar\pi}(x,d(x',u,c))=\delta_x(dx')\bar\pi(du,dc\mid x)$. |
| $F_{\ell,t}^{\bar\pi}$ | $\bar X_\ell\rightsquigarrow\bar X_\ell$ | State-marginal controlled fold $K_{\ell,t}^{\mathrm{dyn}}\odot J_{\bar\pi_{\ell,t}}$. For a genuinely history-dependent policy, history must be included in the state or a conditional-history kernel must be supplied. |
| $G_\ell$ | metric, divergence, loss, or PSD form field | Its domain, units, measurability, and degeneracies must be stated. |
| $V_\ell$ | measurable subset of $\bar X_\ell$ | Admissible or viable region. |
| $R_\ell$ | registry of typed maps/kernels | Inherited family of scale, quotient, reconstruction, and representation maps. It is not a single polymorphic map. |
| $B_\ell$ | typed ledger | Boundary flux, entropy, information, perturbation, calibration, degeneracy, and provenance entries. |
| $\mathrm{rent}_\ell$ | inherited admission diagnostic | Present only in the original tuple. It has no universal numerical type and is moved to admission/certificate records. |
| $\mathscr C_\ell$ | companion record | $`(D_\ell^{\mathrm{rec}},\mathsf{Prov}_\ell,\mathsf{Cert}_\ell)`$; associated with, but not inserted into, $\widehat S_\ell$. |
| $D_\ell^{\mathrm{rec}}$ | reconstruction-data record | Data classes, relations, ambiguity classes, regularity, and stability. |
| $\mathsf{Prov}_\ell$ | provenance DAG | Source IDs, calibration lineage, data/code hashes, and transformations. |
| $\mathsf{Cert}_\ell$ | certificate record | Assumptions, tolerances, proof/execution objects, obligations, and status. |

## Observation and experiment objects

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $a_t$ | 12-field record | Observation atom $(\ell,t,\Omega,\partial_\varepsilon\Omega,x_t,u_t,c_t,H_t,y_t,\Sigma_{y,t},\mathscr F_t)$, with its random entries defined on the declared probability space. |
| $e_t$ | boundary-event record | $(r,t,J_k(r,t),X_k(r,t),\nu(r),\tau(r))$; tensor types and units are model-specific. |
| $\Sigma_{y,t}$ | PSD matrix when $Y_\ell\subseteq\mathbb R^d$, otherwise a declared uncertainty object | Output covariance has output units squared; positivity notation is used only in the vector-valued case. |
| $\mathcal E$ | experiment bundle | $(S,\mathcal T,\mathcal I,\mathcal M_0,\mathcal O,\mathcal N,\mathcal L,\mathcal A,\mathcal D)$. |
| $J_{t,h}$ | finite subset of $[t,t+h]$ | Declared target sampling times; the finite product $Y^{J_{t,h}}$ carries $\mathcal B(Y)^{\otimes J_{t,h}}$. |
| $\mathcal T^{\mathrm{rep}}$ | target record | $(Y,h,q,\mathcal F_t^{\mathrm{legal}})$, with measurable $q:Y^{J_{t,h}}\to Z_q$. The query $q$ and horizon $h$ repair the source record’s undefined target symbol $\tau$; $H^{\mathrm{obs}}$ remains in the system object and is not duplicated here. |
| $\mathcal I$ | intervention class | Legal experimental interventions. |
| $\mathcal M_0$ | baseline model/experiment | Ordinary-domain comparator. |
| $\mathcal O$ | finite or enumerable operator set | Predeclared candidate operators. |
| $\mathcal N$ | null library | Matched null models with their own validity assumptions. |
| $\mathcal L$ | scoring rule | Units and sampling law required. Distinct from loss vector $\mathcal L_{\ell m}$. |
| $\mathcal A$ | admission rule | Maps declared evidence to a local disposition. |
| $\mathcal D$ | disposition map | Codomain $\lbrace\mathrm{admit},\mathrm{sandbox},\mathrm{watch},\mathrm{demote},\mathrm{retire}\rbrace$. |
| $\lambda_{\mathrm{leak}}$ | nonnegative information quantity | $I(Z;Y^{\mathrm{hold}}\mid\mathscr F_{t-})$, when defined; positive value refutes isolation. |
| $d_E$ | pseudometric | Supremum instrument distance defining confusability neighborhoods, not an approximate quotient relation. |

## Boundary operators and inverse problems

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $\tau_\partial$ | $\mathcal X(\Omega)\to\mathcal X_\partial(\partial\Omega)$ | Ideal trace, only for function classes admitting a continuous trace. |
| $L_\varepsilon$ | $\mathcal X(\Omega)\to\mathcal Y_\varepsilon$ | Finite sensor-layer measurement. |
| $L_a$ | differential operator | Governing PDE with coefficient $a$, domain, boundary conditions, and regularity declared. |
| $\Lambda_{a,\Omega}$ | boundary-data space $\to$ boundary-response space | Dirichlet-to-Neumann or analogous response map. |
| $\partial_{\nu,a}$ | conormal derivative | Defined by the governing PDE and orientation. |
| $\mathcal D_\partial$ | boundary-response data class | Namespaced form of the inverse-problem data class written locally as $\mathcal D$ in the manuscript. |
| $\mathcal A_\partial$ | admissible interior class, $\mathcal A_\partial\subseteq\mathcal X(\Omega)$ | Namespaced form of the coefficient/interior class written locally as $\mathcal A$; distinct from the experiment admission rule. |
| $E_\partial$ | relation $\mathcal D_\partial\rightrightarrows\mathcal A_\partial/{\approx}$ | Reconstruction/extension relation; may be set-valued. |
| $e_\partial$ | measurable map $\mathcal D_0\to\mathcal X(\Omega)$, with $e_\partial(\mathcal D_0)\subseteq\mathcal A_\partial$ | A single-valued selected extension on $\mathcal D_0\subseteq\mathcal D_\partial$ whose graph, after quotienting by $\approx$, lies in $E_\partial$. Existence, admissibility, and measurability are assumptions; boundedness and linearity require separate hypotheses. It is not the relation $E_\partial$. |
| $\approx$ | physical inverse-problem equivalence | Gauge or boundary-fixing diffeomorphism ambiguity preserved by the data. |
| $\omega$ | stability modulus | Relates data distance to quotient-interior distance on a declared class. |
| $G_\partial$ | nonnegative information quantity | $I(Y_{t+h};X_{\partial,t}\mid Z_t)$; a boundary-relevance screen, not a sufficiency theorem. |
| $S_{\rm ext}^{\rm aug}$ | nonnegative information quantity | $I(Y_{t+h};X_{{\rm ext},t}\mid X_{\partial,t},X_{\Omega,t}^{\rm obs},Z_t)$; an exterior-closure screen for augmented observed information. |
| $S_{\rm rest}$ | nonnegative information quantity | $I(Y_{t+h};X_{{\rm rest},t}\mid X_{\partial,t},Z_t)$ for the declared relevant remainder; at zero tolerance it states target-relative conditional independence under existence hypotheses. |

## Operational observable structures

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $\mathcal O_\ell$ | function class, operator system, or $C^*$-algebra | Declared accessible observables at description $\ell$. |
| $\mathcal A_{\mathrm{acc}}$ | operator system | Accessible quantum effects/observables. |
| $\rho,\sigma$ | density operators | Positive trace-one operators on a declared Hilbert space. |
| $x\sim_Hx'$ | exact equivalence relation on raw states | Equality $H^X(\cdot\mid x,u,c)=H^X(\cdot\mid x',u,c)$ for every legal $(u,c)$. Only this zero-defect relation supports a quotient. |
| $d_E(x,x')\le\varepsilon$ | symmetric confusability relation | Instrument-relative $\varepsilon$-confusability. For $\varepsilon>0$ it is generally nontransitive and is not an equivalence or quotient relation. |
| $d_{\mathcal A_{\mathrm{acc}}}(\rho,\sigma)$ | $[0,1]$ | $\sup\lbrace\lvert\mathrm{Tr}[E(\rho-\sigma)]\rvert:0\le E\le I,\ E\in\mathcal A_{\mathrm{acc}}\rbrace$; a pseudometric determined by accessible effects. |
| $\rho\sim_{\mathcal A_{\mathrm{acc}}}\sigma$ | exact operational equivalence | Defined by $d_{\mathcal A_{\mathrm{acc}}}(\rho,\sigma)=0$. It asserts equality of all accessible probabilities, not equality of density-matrix representatives. |
| $d_{\mathcal A_{\mathrm{acc}}}(\rho,\sigma)\le\varepsilon$ | $\varepsilon$-confusability relation | For $\varepsilon>0$ it is generally nontransitive; no tilde/equivalence notation is used for it. |
| $\Phi$ | state channel | Positive stochastic or CPTP map, as locally declared. |
| $\Phi^\sharp$ | observable pullback | Adjoint satisfying $\mathrm{Tr}[\Phi(\rho)A]=\mathrm{Tr}[\rho\Phi^\sharp(A)]$. |
| $\eta_{\mathrm{td}}$ | $[0,1]$ | Transform–discard/discard–transform accessible-probability defect. |

## Retained Volume II budgeted-morphism notation

These symbols record the exact inventory of the Volume II morphism. They are
kept distinct from the extended eight-field record in the next section.

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $\mu^{\mathrm{II}}_{a\to b}$ | 8-field record | Volume II morphism $(R_X,R_Y,R_U,R_C,\alpha_H,\alpha_K,q_{ab},b_\mu)$. The superscript is a ledger namespace; the source writes $\mu$. |
| $R_X^\mu$ | $\bar X_a\rightsquigarrow\bar X_b$ | Volume II state kernel or measurable map. Distinct from the current equation residual $R_{\ell m}$. |
| $R_Y^\mu$ | $Y_a\rightsquigarrow Y_b$ | Volume II output kernel or measurable map. |
| $R_U^\mu$ | $U_a\rightsquigarrow U_b$ | Volume II control kernel or measurable map. |
| $R_C^\mu$ | $C_a\rightsquigarrow C_b$ | Volume II context kernel or measurable map. |
| $\alpha_H^\mu,\alpha_K^\mu$ | comparison-witness records | Witness observation and dynamics comparison, respectively. Volume II does not fix universal witness codomains; an application must instantiate their diagrams, metrics, domains, and tolerances before either witness is numerical. |
| $q_{ab}^{\mathrm{compat}}$ | quotient-compatibility witness | Volume II $q_{ab}$; certifies compatibility of representatives, quotient maps, and $R_X^\mu$. It is neither $q_a^{\mathrm{quot}}$ nor an identity observable. |
| $b_\mu$ | $[0,\infty]^7$ | Distortion budget $(b_{\mathrm{type}},b_{\mathrm{quot}},b_{\mathrm{obs}},b_{\mathrm{fil}},b_{\mathrm{cal}},b_{\mathrm{scale}},b_{\mathrm{rent}})$, ordered and added componentwise. |
| $\tau^{\mathrm{II}}$ | $[0,\infty]^7$ | Volume II admissibility threshold. The condition is $b_\mu\le\tau^{\mathrm{II}}$ componentwise, together with all separately declared hard gates. This is not a trace or an exit time. |
| $\kappa(\mu,\nu)$ | $[0,\infty]^7$ | Explicit nonlinearity or naturality-defect surcharge in $b_{\nu\circ\mu}=b_\mu+b_\nu+\kappa(\mu,\nu)$. Associativity requires the Volume II cocycle law. |
| $\alpha_H^{\nu\mu},\alpha_K^{\nu\mu},q_{ac}$ | composite witness records | Observation, dynamics, and quotient witnesses in $\nu\circ\mu$. Their associative composition is an explicit hypothesis of the Volume II category theorem, not a consequence of kernel composition alone. |
| $\mathrm{BSC}_b$ | category, under stated hypotheses | Objects are BSC systems and arrows are Volume II budgeted morphisms when witnesses compose associatively and $\kappa$ satisfies its cocycle law. A fixed-threshold admissible subcollection is only partially closed under composition. |

## Extended typed BSC morphism record

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $\mathfrak M_{\ell\to m}$ | 8-field typed record | $(T_{\ell m},T_{\ell m}^{\sharp},K_{\ell m},R_{\ell m},\Theta_{\ell m},\delta_{\ell m},C_{\ell m},\mathsf{Cert}_{\ell m})$. |
| $\mathsf v$ | variant tag | One of deterministic, stochastic, quantum, correspondence, or defect/fusion. Variants do not share an unqualified composition theorem. |
| $D_{\ell m}$ | measurable subset of $\bar X_\ell$ | Domain of a partial transport. |
| $D_{\ell n}$ | measurable subset of $D_{\ell m}$ | $\lbrace x\in D_{\ell m}:T_{\ell m}(x,D_{mn})=1\rbrace$, the support-compatible domain of a partial composite. |
| $T_{\ell m}$ | $D_{\ell m}\rightsquigarrow\bar X_m$ or variant-specific arrow | State transport. |
| $T_{\ell m}^{\sharp}$ | $B_b(\bar X_m)\to B_b(D_{\ell m})$ | Reverse-direction observable transport; positive and unital for Markov kernels, not generally multiplicative. |
| $T_{\ell m}^{\sharp\mid D_{mn}}$ | $B_b(D_{mn})\to B_b(D_{\ell n})$ | Restricted pullback $\int_{D_{mn}}g(y)T_{\ell m}(x,dy)$. It types the composite $T_{\ell n}^{\sharp}=T_{\ell m}^{\sharp\mid D_{mn}}\circ T_{mn}^{\sharp}$ and is independent of the extension of $g$. |
| $K_{\ell m}$ | $Y_\ell\rightsquigarrow Y_m$ | Interscale post-processing/simulation channel; distinct from $K_\ell^{\mathrm{dyn}}$. |
| $\mathcal E_\ell$ | $\mathsf{Dom}(\mathcal E_\ell)\to Z_\ell$ | Governing equation operator. |
| $Z_\ell$ | normed equation-residual space | Carries declared physical units. |
| $S_{\ell m}$ | $Z_\ell\to Z_m$ | Equation-space transport needed to type residual composition. |
| $R_{\ell m}$ | $D_{\ell m}\to Z_m$, or law-level weak residual record | Target-equation residual. Distinct from inherited registry $R_\ell$. |
| $\mathsf Z_\ell^{\mathrm{sc}}$ | $\bar X_\ell\times U_\ell\times C_\ell$ | Joint state--control--context space. Distinct from the equation-residual space $Z_\ell$. |
| $\widehat D_{\ell m}$ | measurable subset of $\mathsf Z_\ell^{\mathrm{sc}}$ | Domain of the completed joint transport. |
| $\widehat D_{\ell n}$ | measurable subset of $\widehat D_{\ell m}$ | $\lbrace z\in\widehat D_{\ell m}:\widehat T_{\ell m}(z,\widehat D_{mn})=1\rbrace$; completion compatibility also requires its state projection to lie in $D_{\ell n}$. |
| $\widehat T_{\ell m}$ | $\widehat D_{\ell m}\rightsquigarrow\mathsf Z_m^{\mathrm{sc}}$ | Completed joint transport supplied by $C_{\ell m}$; its state marginal must agree with $T_{\ell m}$ under the declared policy/completion. |
| $\Theta_{\ell m}$ | nonnegative defect | Distance between $H_m^{\mathrm{obs}}\odot\widehat T_{\ell m}$ and $K_{\ell m}\odot H_\ell^{\mathrm{obs}}$. |
| $\delta_{\ell m}$ | $[0,1]$ | Directed Le Cam deficiency from experiment $\ell$ to experiment $m$. |
| $C_{\ell m}$ | completion record | Control/context maps, carrier, controller, observer, frame, instrument, clock, resources, and boundary conditions. Distinct from context space $C_\ell$. |
| $\mathsf{Cert}_{\ell m}$ | certificate record | Variant, assumptions, domains, lost information, defects, physical implementation, evidence, verdict, readiness, and unresolved obligations. |
| $\eta(K)$ | $[0,1]$ | Dobrushin contraction coefficient for total variation. |
| $\mathcal R_{\ell m}$ | residual-record space | Variant-specific space containing $R_{\ell m}$; pointwise deterministic and law-level weak records are not conflated. |
| $\mathcal Q_{\ell m}^{\mathrm{res}}$ | declared residual test class | Inputs against which the residual evaluator is bounded. |
| $\mathcal Q_{\ell m}^{\mathrm{law}}$ | subset of admissible input probability laws | Law class over which viability-exit probability is bounded. |
| $\mathsf{ev}_{\ell m}^{\mathrm{res}}$ | $\mathcal R_{\ell m}\times\mathcal Q_{\ell m}^{\mathrm{res}}\to[0,\infty]$ | Typed scalar evaluator for the morphism variant’s residual record; records units and test class. |
| $\mathfrak r_{\ell m}$ | nonnegative residual evaluation | $`\sup_{\zeta\in\mathcal Q_{\ell m}^{\mathrm{res}}}\mathsf{ev}_{\ell m}^{\mathrm{res}}(R_{\ell m},\zeta)`$. The deterministic specialization is $\sup_{x\in D_{\ell m}^{\mathrm{eval}}}\lVert R_{\ell m}(x)\rVert_{Z_m}$; stochastic weak residuals use a different evaluator. |
| $\mathcal L_{\ell m}$ | vector | Residual, naturality, optimal deficiency, implemented-channel error, quotient-loss, and viability-failure coordinates. Never scalarized without a justified decision problem. |
| $\lambda_{\mathrm{quot}}$ | nonnegative query-dependent defect | Diameter of a target query on a quotient class. |
| $\alpha_{\mathrm{exit}}$ | $[0,1]$ | Probability of leaving the viability region before a stated horizon. |
| $\mathfrak Q_c$ | claim specification | $(J_c,\tau_c,G_c,\mathsf{Req}_c)$: required loss coordinates, typed tolerances, hard gates, and minimum readiness. |
| $I_{c,j}$ | proved interval enclosure | $[\underline L_{c,j},\overline L_{c,j}]\ni L_{c,j}$ with units, test class, method, and provenance. |
| $\mathsf{WF}$ | predicate | The transfer record is well formed and type-correct. |
| $\mathsf{Eval}_c$ | predicate | Every claim-required coordinate has a proved enclosure, every required gate is evaluated, and critical obligations are resolved. |
| $\mathsf{Adm}_c$ | predicate | Evaluated for $c$, every upper enclosure is within tolerance, every hard gate passes, and readiness meets $\mathsf{Req}_c$. |

## Statistics, dynamics, scale, and persistence

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $\mathsf E_i=\lbrace P_{i,\theta}\rbrace$ | statistical experiment | Common parameter family required for direct deficiency composition. |
| $\mathfrak K_{\ell m}^{\mathrm{all}}$ | all Markov kernels $Y_\ell\rightsquigarrow Y_m$ | Comparison class for the ordinary Le Cam deficiency. A smaller implementation class $\mathfrak K_{\ell m}^{\mathrm{impl}}\subseteq\mathfrak K_{\ell m}^{\mathrm{all}}$ must be declared separately. |
| $e_{\ell m}(K)$ | $[0,1]$ | Error of one declared or implemented channel $K:Y_\ell\rightsquigarrow Y_m$: $\sup_{\theta\in\Theta}\lVert KP_{\ell,\theta}-P_{m,\theta}\rVert_{\mathrm{TV}}$, where $(KP)(A)=\int K(y,A)P(dy)$. It records the tested channel, not the optimum over channels. |
| $\delta(\mathsf E,\mathsf F)$ | $[0,1]$ | Infimum simulation error from $\mathsf E$ observations to $\mathsf F$ observations. Zero means arbitrarily accurate simulation; an exact simulating channel additionally requires attainment or an applicable randomization theorem. |
| $\delta_{\ell m}$ | $[0,1]$ | Ordinary directed deficiency $\inf_{K\in\mathfrak K_{\ell m}^{\mathrm{all}}}e_{\ell m}(K)$. Always $\delta_{\ell m}\le e_{\ell m}(K)$; equality requires an attained infimum and an optimizing implemented channel, neither of which is automatic. |
| $\delta_{\ell m}^{\mathrm{impl}}$ | $[0,1]$ | Constrained deficiency $\inf_{K\in\mathfrak K_{\ell m}^{\mathrm{impl}}}e_{\ell m}(K)$. It is at least $\delta_{\ell m}$ and must not be reported as the unconstrained Le Cam deficiency. |
| $\Delta(\mathsf E,\mathsf F)$ | $[0,1]$ | Symmetric maximum of the two directed deficiencies; introduced only when needed. |
| $\succeq_B$ | preorder | Blackwell dominance: exact stochastic simulation/garbling. |
| $\mathcal K_F$ | observable operator | Koopman action $`[\mathcal K_Fg](x)=g(F(x))`$. |
| $\phi,\lambda$ | observable and complex scalar | Candidate Koopman eigenfunction and eigenvalue. |
| $\varepsilon_{\mathrm{dyn}}$ | nonnegative norm | Full declared-space residual $\lVert \mathcal K_F\phi-\lambda\phi\rVert$. |
| $q_\ell^{\mathrm{id}}$ | $\bar X_\ell\to(Q,d_Q)$ | Declared identity/task observable used for recurrence and persistence. The manuscript may suppress the superscript in a persistence-only scope; it is distinct from $q_\ell^{\mathrm{quot}}:X_\ell\to\bar X_\ell$. |
| $F_i$ | $\bar X_i\times U_i\times C_i\rightsquigarrow\bar X_{i+1}$ | Completed admissible joint-input fold. |
| $P_i$ | $\bar X_i\rightsquigarrow\bar X_{i+1}$ | State-marginal kernel induced from $F_i$ by a certified state-Markov policy $\bar\pi_i$; history dependence requires state augmentation. |
| $\mu_{i+1}=\mu_iP_i$ | element of $\mathcal P(\bar X_{i+1})$ | State marginal after one fold; $(\mu_iP_i)(A)=\int P_i(x,A)\mu_i(dx)$. |
| $\mathbb P_{\mu_0}^{P_{0:n-1}}$ | probability law on $\prod_{i=0}^{n}\bar X_i$ | Path law generated from $\mu_0$ and the kernels $P_0,\ldots,P_{n-1}$, under standard-Borel/Ionescu--Tulcea hypotheses. Endpoint marginals alone do not determine path events. |
| $\mathbf X_k$ | coordinate random variable with values in $\bar X_k$ | State at prefix $k$ under $\mathbb P_{\mu_0}^{P_{0:n-1}}$; distinct from the raw state space $X_k$. |
| $\mathrm{Rec}_{q,n}$ | $[0,\infty]$ | Endpoint recurrence $`W_{p,Q}((q_0^{\mathrm{id}})_\sharp\mu_0,(q_n^{\mathrm{id}})_\sharp\mu_n)`$, defined only when both identity laws lie in $\mathcal P_p(Q)$. |
| $\tau_V$ | $\mathbb N_0\cup\lbrace\infty\rbrace$-valued stopping time | First viability exit $\inf\lbrace k\ge0:\mathbf X_k\notin V_k\rbrace$ under the declared path law, with $\inf\varnothing=\infty$. Measurability and adaptedness of $V_k$ are required. |
| $\alpha_k^{\mathrm{cum}}$ | $[0,1]$ | Declared cumulative prefix tolerance for $\mathbb P(\tau_V\le k)$. |
| $\beta_i$ | $[0,1]$ | Declared one-step exit-event bound, used in $\mathbb P(\tau_V\le n)\le\sum_{i=0}^{n}\beta_i$. It must not be conflated with the cumulative tolerance $\alpha_n^{\mathrm{cum}}$. |
| $E_i,e_i,L_i$ | common-unit errors and dimensionless propagation factor | Homogeneous identity error, one-step injection, and Lipschitz coefficient. Other defect coordinates remain separate. |
| $R^X_{ab}$ | state scale map | Direct state coarse-graining, namespaced from equation residual. |
| $T^{\mathrm{dyn}}_{ab}$ | nonnegative Wasserstein defect | Failure of a state scale map to intertwine source and target dynamics on a declared Polish target state space $(\bar X_b,d_b)$; all displayed and propagated laws must lie in $\mathcal P_p(\bar X_b)$. |
| $\varepsilon$ | scale or sensor parameter | Units, limiting path, and order declared locally. |

## Claim-relative simulation-evidence profiles

These symbols are version 1.2.0 additions. They refine the
existing certificate, loss-vector, and claim-admissibility machinery. They do
not add a ninth field to the BSC morphism record. Statistical experiment
simulation, numerical execution, and surrogate deployment remain separate
typed uses of the word "simulation."

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $\mathcal U_c$ | intended-use record | $(D_c,H_c,Q_c,\pi_c,\mathsf{BC}_c,\mathsf{Units}_c,\tau_c)$: operating domain, horizon, quantity of interest, policy, initial/boundary conditions, unit declarations, and claim-local tolerances. |
| $\mathsf{SEC}_{c,\iota}$ | claim-relative simulation-evidence profile | $(\mathcal U_c,I_c^\ell,J_c^\ell,J_c^g,\lbrace\mathsf E_{c,i}\rbrace_{i\in I_c^\ell},\lbrace g_{c,k}\rbrace_{k\in J_c^g},\Phi_c,\boldsymbol\rho_c,\mathsf{Prov}_{c,\iota})$. It refines $\mathsf{Cert}$ and is neither a new system object nor a morphism variant. |
| $I_c^\ell$ | finite source-coordinate index set | Indexes estimands and evidence records before propagation into the BSC loss vector. A source coordinate is not silently identified with a target loss coordinate. |
| $J_c^\ell,J_c^g$ | finite target index sets | Applicable coordinates of the existing BSC loss vector and required Boolean hard gates for claim $c$. Missing required evidence is missing or unevaluated, never zero. |
| $\mathcal V_c,\mathcal W_c$ | ordered product spaces with declared units | $\mathcal V_c=\prod_{i\in I_c^\ell}V_{c,i}$ is the source evidence space and $\mathcal W_c=\prod_{j\in J_c^\ell}W_{c,j}$ is the target BSC loss space. |
| $g_{c,k}$ | $\lbrace\mathsf{true},\mathsf{false},\mathsf{unevaluated}\rbrace$ | Claim-required hard gate. Admission requires every required deployment gate to be certified true. |
| $\mathsf E_{c,i}$ | statistical or deterministic source-evidence record | $`(\eta_{c,i},d_{c,i},\mathcal O_{c,i},\widehat\eta_{c,i},n_{c,i},\alpha_{c,i},[L^{\mathrm{src}}_{c,i},U^{\mathrm{src}}_{c,i}],\varepsilon^{\mathrm{opt}}_{c,i},\Psi_{c,i})`$. It binds a source estimand, discrepancy, observation model, evaluator, effort, coverage, source enclosure, optimization gap, and proxy-transfer theorem. |
| $(\Omega_c,\mathcal F_c,\mathbb P_c)$ | joint observation-and-analysis probability space | Every statistical record used together is defined on this common space, and every random interval endpoint is $\mathcal F_c$-measurable. |
| $\mathcal C_c^{\mathrm{src}},\alpha_c$ | joint source-coverage event and failure bound | $`\mathcal C_c^{\mathrm{src}}=\bigcap_i\lbrace\eta_{c,i}\in[L^{\mathrm{src}}_{c,i},U^{\mathrm{src}}_{c,i}]\rbrace`$ with $\mathbb P_c(\mathcal C_c^{\mathrm{src}})\ge1-\alpha_c$. A union-bound justification additionally requires every marginal failure probability to be at most $\alpha_{c,i}$ and $\sum_i\alpha_{c,i}\le\alpha_c$. Setting $\alpha_c=0$ gives probability-one coverage only; a deterministic enclosure must hold pointwise. |
| $\Phi_c$ | monotone unit-respecting map $\mathcal V_c\to\mathcal W_c$ | A proved relation $\boldsymbol\ell_c^0\le_{\mathcal W_c}\Phi_c(\boldsymbol\eta_c)$ transports source estimands into applicable frozen-state BSC loss coordinates. Incommensurate quantities are not added without this map, an applicable norm inequality, or another claim-specific rule. |
| $\boldsymbol U_c^{\mathrm{src}},\boldsymbol U_c^0$ | source and propagated frozen-state target-loss upper-bound vectors | $\boldsymbol U_c^0=\Phi_c(\boldsymbol U_c^{\mathrm{src}})$. Deployment admission compares $U^0_{c,j}+\rho_{c,j}$, not a raw source interval, with $\tau_{c,j}$. |
| $\ell^0_{c,j},\ell^1_{c,j}$ | common-unit loss coordinates | Frozen-evaluation and proposed-deployment losses. Direct inheritance is blocked unless exact identity transfer or a certified compatibility relation applies. |
| $\rho_{c,j},\boldsymbol\rho_c$ | nonnegative compatibility reserve and its vector | Certified additional-loss enclosure satisfying $\ell^1_{c,j}\le\ell^0_{c,j}+\rho_{c,j}$ on the declared domain, horizon, and joint event. It is not unallocated tolerance. Frozen uncertainty already represented in $U^0_{c,j}$ and uncertainty in the deployment change are each represented exactly once. |
| $s_{c,j}$ | signed remaining deployment slack | $\tau_{c,j}-(U^0_{c,j}+\rho_{c,j})$. Positive slack certifies stated headroom, zero passes with no certified reserve, and negative slack blocks admission but does not alone prove actual violation. |
| $\iota$ | factored evidence identity | $(\iota_{\mathrm{cand}},\iota_{\mathrm{data}},\iota_{\mathrm{analysis}},\iota_{\mathrm{env}},\iota_{\mathrm{contract}})$. Evidence transfers exactly only across every identity factor on which it depends; a changed identity needs theorem-class applicability or a certified compatibility morphism. A genuinely absent factor uses a typed not-applicable value rather than being omitted. |
| $\Phi_k,\widehat\Phi_k$ | reference and surrogate-coupled host maps | $\Phi_k(x)=F_k(x,g_k(x))$ and $\widehat\Phi_k(x)=F_k(x,\widehat g_k(x))$ on a certified reachable domain. |
| $E_k,L_k,b_k$ | nonnegative state error, host amplification, and one-step injection | If $E_{k+1}\le L_kE_k+b_k$, then the existing prefix theorem gives the finite-horizon product-sum bound. Average standalone RMSE does not establish a uniform reachable-domain $b_k$. |

## Operational report channels

These are `1.3.0` certificate and application symbols. They describe a
fixed typed preparation-to-report pipeline and do not add a ninth BSC morphism
field or prove the open full quantum composition claim BSC-QOP-03.

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $\mathsf{ORE}$ | operational report envelope | $(\Theta,\lbrace z_0(\theta)\rbrace,\lbrace T_k\rbrace_{k=1}^m,Z,\lbrace P_\theta^Z\rbrace,\mathsf{Cert}_{\mathrm{ORE}})$. It binds preparation, fixed interfaces, controls, dynamics, measurement, report, and the induced classical statistical experiment. Common envelope form does not identify microscopic physics. |
| $z_k,\widehat z_k$ | ideal and implemented state or law | Quantum interfaces carry density operators; classical interfaces carry probability laws. Memory, feedback, clock, and history variables must be included in the state if they affect a Markov-stage claim. |
| $d_k$ | total variation or trace distance | Interface metric declared by type. Quantum trace distance is $D_{\mathrm{tr}}(\rho,\sigma)=\frac12\lVert\rho-\sigma\rVert_1$; the factor $1/2$ is retained at a measurement boundary. |
| $\widehat{\mathcal R}_k$ | implemented reachable set or certified superset | Every stage defect is evaluated on implemented reachable inputs. An ideal-only reachable set does not control the first term of the propagation proof. |
| $\varepsilon_k,\eta_k,E_k$ | local defect, ideal-stage contraction, and propagated discrepancy | $d_k(\widehat T_k\widehat z,T_k\widehat z)\le\varepsilon_k$ on $`\widehat{\mathcal R}_{k-1}`$ and $`d_k(T_k\widehat z,T_kz)\le\eta_kd_{k-1}(\widehat z,z)`$. Then $E_m\le\sum_{k=0}^m\varepsilon_k\prod_{j=k+1}^m\eta_j$. Strict quantum contraction requires a separate theorem. |
| $\mathcal I_\varepsilon(y)$ | identified set in parameter space | $\lbrace\theta:d(F(\theta),y)\le\varepsilon\rbrace$. A target property is exactly report-identifiable only when constant on the applicable identified set; at zero error this is fiber constancy. |
| $\mathcal D_t$ | declared open-system generator term | In $\dot\rho=-i[H,\rho]/\hbar+\mathcal D_t(\rho)$, the decomposition must generate physical trace-preserving evolution and fix a system/bath split and energy zero. |
| $E(t)$ | scalar system-energy expectation | $\mathrm{Tr}[\rho(t)H(t)]$, with $\dot E=\mathrm{Tr}(\rho\dot H)+\mathrm{Tr}(H\mathcal D_t(\rho))$. Measurements, resets, coupling energy, and fields outside the reduced state need additional ledger terms. |
| $U_v,b_v,p_h$ | stored energy, non-port supply, and inward half-edge power | In a finite energy-port diagram, $\dot U_v=b_v+\sum_{h\in H_v}p_h+r_v$. A non-port supply represents an excluded pump, bath, reservoir, or moving support; it is not energy creation. All quantities share a declared clock and rate convention. |
| $r_v,g_e,R_G$ | component, seam, and assembled energy residuals | $r_v=\dot U_v-b_v-\sum_hp_h$, $g_e=p_h+p_{\bar h}$, and $R_G=d(\sum_vU_v)/dt-\sum_vb_v-\sum_{h\in H_{\mathrm{ext}}}p_h$. BSC-ENE-02 gives $R_G=\sum_vr_v+\sum_eg_e$. Global zero does not certify the local terms. |
| $\eta_E,\Phi_N,\eta_{\mathrm{all}}$ | energy efficiency, count yield, and end-to-end conditioned efficiency | $\eta_E=E_{\mathrm{useful,out}}/E_{\mathrm{charged,in}}$ is differently typed from a count yield. $\eta_{\mathrm{all}}$ retains the success indicator rather than normalizing away failures. Stage ratios telescope only across the identical intermediate extensive quantity and evidence identity. |
| $q_x$ | Bernoulli bias conditional on input $x$ | Used only under the declared scalar conditionally-iid model $Y_i\mid X=x\sim\mathrm{Bernoulli}(q_x)$. Hardware variability does not establish iid sampling. |
| $K=\sum_{i=1}^NY_i$ | sufficient count in $\lbrace0,\ldots,N\rbrace$ | Under the scalar conditionally-iid model, $I(X;Y^N)=I(X;K)\le\log_2(N+1)$. For 256 labels, zero-error finite $N$ decoding is impossible because the laws cannot be mutually singular. |
| $\mathcal C_N$ | raw-bit compression factor | $8/N$ for an 8-bit input represented by $N$ output bits. $N=1$ is nominal 8:1 lossy coding; $N\ge8$ is not raw-bit compression. |
| $C,S,P,Q$ | source/target relation matrices and permutation matrices | Under the convention $P_{\phi(i),i}=1$, one same-entity alignment requires $S=PCP^{\mathsf T}$. Independent row/column alignment $S=PCQ^{\mathsf T}$ is weaker and applies naturally only to separately typed roles. |
| $\alpha$ | dimensionless fine-structure constant | Low-energy electromagnetic coupling $e^2/(4\pi\varepsilon_0\hbar c)$. Operational channel topology does not determine its value; a physical and metrological bridge is required. In the revised SI, exact $e,h,c$ imply $\mu_0=\alpha\mkern3mu 2h/(ce^2)$ rather than fixing $\alpha$. |

## Electromagnetic evidence bridge

These are local `1.3.0` symbols for the electromagnetic completion of an
operational report envelope. They neither add a field to the BSC morphism nor
derive a unified microscopic theory or the numerical value of $\alpha$.

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $\mathsf{EMC}$ | typed electromagnetic completion record | $(M,g,P,[\mathcal A],\mathcal F,\mathcal H,\mathcal J,\mathcal C,\mathcal B,\mathcal M,\mathcal R,\mathsf{Cert}_{\mathrm{EM}})$. It binds geometry, bundle and gauge, fields and sources, constitutive response, boundary ports, instrument, report, and certificate. |
| $\mathscr A(P),\mathscr G(P),[\mathcal A]$ | admissible connections, declared gauge group, and gauge class | A connection-level report is physical only if constant on $\mathscr G(P)$-orbits. The local symbol $\mathcal A$ here is a connection and is distinct from the experiment admission rule. |
| $\mathcal F,\mathcal H,\mathcal J$ | curvature two-form, excitation two-form, and current three-form | $d\mathcal F=0$ and $d\mathcal H=\mathcal J$. A smooth global solution implies $d\mathcal J=0$ and exactness of $\mathcal J$; singular or open-boundary models require separately typed distributional or relative forms. |
| $\mathrm{Hol}_\gamma(\mathcal A)$ | element of $U(1)$ | In a single trivialization, closed-loop holonomy is $\exp(i\oint_\gamma\mathcal A)$; a nontrivial bundle also requires its patch transitions. Equal curvature need not imply equal holonomy on nontrivial topology. Open-path phase is not gauge invariant without endpoint or compensating data. |
| $u_{\mathrm{EM}},S_{\mathrm{Poynt}}$ | energy density and Poynting vector | $u_{\mathrm{EM}}=(E\cdot D+H\cdot B)/2$ and $S_{\mathrm{Poynt}}=E\times H$ under a time-independent symmetric positive constitutive law. Modulated or dispersive media need additional pump or material-state terms. |
| $\mathcal U,\mathcal F,\mathcal Q$ | spatial energy-density, flux, and supply forms | On a fixed oriented spatial manifold, $\partial_t\mathcal U+d\mathcal F=\mathcal Q$. Curvature changes measures and divergence, not the source ledger. Time-dependent metrics and moving boundaries require volume-deformation and Reynolds-transport terms. |
| $J_\xi^a$ | stress-energy current associated with $\xi$ | $`J_\xi^a=-T^a{}_b\xi^b`$ obeys $`\nabla_aJ_\xi^a=-f_b\xi^b-T^{ab}\nabla_{(a}\xi_{b)}`$ for $f^b=\nabla_aT^{ab}$. Conservation requires the total included stress-energy and a Killing field, or a separately declared asymptotic or quasi-local charge. |
| $S(\omega),W$ | scattering matrix and positive power metric | Passivity gives $S^\dagger W S\preceq W$ only for the declared port basis, reference plane, normalization, band, hidden-port completion, calibration, and stored-energy state. The symbol $S(\omega)$ is local and is not a BSC system object. |
| $\Lambda_{\varepsilon,\mu}$ | Maxwell boundary-response operator | Maps a declared tangential electric trace space to a declared tangential magnetic trace space for one well-posed forward problem. A finite measured S-parameter matrix is not automatically the full operator. Inverse authority is theorem-, coefficient-class-, gauge-, and data-local. |
| $Z,q,q^2/Z$ | positive field kinetic coefficient, matter coupling, and normalization invariant | Under $A'=\lambda A$, $Z'=Z/\lambda^2$ and $q'=q/\lambda$ while $q^2/Z$ is unchanged. A fixed representation and canonical normalization may remove the coordinate freedom but do not derive the invariant's value. |
| $\mathcal A=(q/\hbar)A_{\mathrm{phys}}$ | dimensionless matter connection | First-Chern integrality constrains $\frac{q}{2\pi\hbar}\int_\Sigma F_{\mathrm{phys}}\in\mathbb Z$ for the declared bundle and closed two-cycle. It constrains a charge-flux product, not $\alpha$ separately. |
| $g(\mu),\beta(g),g(\mu_0)$ | running coupling, beta function, and boundary value | $\mu\mkern3mu dg/d\mu=\beta(g)$ transports a supplied coupling between scales. It does not determine a numerical trajectory without a boundary value; scheme, matching thresholds, truncation, and scale are part of the certificate. |
| $P,\kappa,\mathrm{Stab}_{\mathrm{tr}}$ | tiling partition, electromagnetic coefficient field, and translation stabilizer | Translation-faithful materialization means $\tau_v\kappa=\kappa\Rightarrow\tau_vP=P$, hence $`\mathrm{Stab}_{\mathrm{tr}}(\kappa)\subseteq\mathrm{Stab}_{\mathrm{tr}}(P)`$. It transfers only absence of translation symmetry, not a spectrum, band gap, chirality, or device property. The local $P$ here is a tiling partition, not a preparation kernel or permutation matrix. |
| $C_{\mathrm{sel}},\Phi_{\mathrm{mat}},X_N$ | geometry selector, materialization map, and finite approximant | $C_{\mathrm{sel}}$ chooses tile interiors, edges, vertices, centroids, or another finite point set; $\Phi_{\mathrm{mat}}$ adds scale, thickness, constitutive dispersion, loss, substrate, and interfaces. An infinite tiling theorem does not identify a fabricated finite device without these maps. |
| $F_N(k_x,k_y),I_N$ | scalar point-scatterer amplitude and intensity | $F_N=\sum_{j=1}^N\exp(2\pi i(k_xx_j+k_yy_j))$ and $I_N=\lvert F_N\rvert^2$ for the declared identical-point model. This is not a full Maxwell solution for finite scatterers; selector, weights, form factor, phase, illumination, and calibration remain typed. |

## Certified normalized-scale profiles

These are reusable framework symbols. They do not add a ninth field to the
BSC morphism record, and they do not construct an infinite-system limit.

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $\mathfrak A$ | directed comparison family of certified finite systems | Scale-family record $`(I,P,\lbrace\lambda_i,\mathsf S_i,\mathsf{Cert}_i,\mathfrak M_{ij},A_i,Z_i,L_i,\mathsf O_i\rbrace)`$. It keeps ideal observables and estimator laws distinct and asserts no categorical identity or composition coherence without an additional hypothesis. |
| $I,P$ | directed index and common topological parameter space | Every scale comparison and parameter slice must use these declared objects or an explicitly typed replacement. |
| $\lambda_N$ | positive dimensionless gauge with $\lambda_N\to\infty$ | Denominator of logarithmic rates. Power-law scaling uses $\lambda_N=\log N$; physical volume or qubit normalizations must be stated separately. |
| $A_N,Z_N,L_N$ | complex carrier, nonzero normalizer, and normalized observable | $L_N=A_N/Z_N$. A nonvanishing normalizer preserves finite zero sets but may collapse the raw limit or shift logarithmic rates. |
| $\mathsf O_N$ | observation or estimator kernel | Report law for the ideal observable. It is not identified with the complex scalar $L_N$. |
| $\gamma_N,\kappa_N,\mathcal R_N$ | real logarithmic profiles when finite | $\gamma_N=\log\lvert Z_N\rvert/\lambda_N$, $\kappa_N=-\log\lvert A_N\rvert/\lambda_N$, and $\mathcal R_N=-\log\lvert L_N\rvert/\lambda_N=\gamma_N+\kappa_N$. Exact zeros require an explicit extended-value convention. |
| $\Sigma,\rho$ | closed exceptional set and branch-gap function | A limit $\mathcal R=\gamma+\rho\mathbf1_\Sigma$ has discontinuities on $\partial\Sigma$ under the stated continuity and positivity hypotheses, not automatically on every point of an arbitrary $\Sigma$. |
| $\iota:Q\to P$ | continuous parameter slice | $\mathrm{Disc}(\mathcal R\circ\iota)\subseteq\iota^{-1}(\mathrm{Disc}\mathcal R)$. Equality requires visibility of the competing branches along the slice. |
| $\Omega,m_\Omega,\varepsilon_N$ | Jordan domain, boundary margin, and uniform error | The certified zero-count condition is $\sup_{\partial\Omega}\lvert A_N-A\rvert\le\varepsilon_N<m_\Omega\le\inf_{\partial\Omega}\lvert A\rvert$. |
| $q_\Sigma,d$ | finite-valued query and decoder | Exact stochastic decoding requires a measurable output partition supporting the corresponding laws; non-mutually-singular different-label laws block exact decoding. |

## Engineered zeta–DQPT case-study notation

These symbols are local to the version 1.1.0 case study. They do not redefine
the global BSC system or morphism records.

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $s=\beta_{\mathrm{eff}}+it$ | complex parameter | $\beta_{\mathrm{eff}}=\mathrm{Re}(s)$ and $t=\mathrm{Im}(s)$ in the zeta case study. The experiment encodes $\beta_{\mathrm{eff}}$ in state populations; it is not the inverse of the $305\mkern3mu \mathrm K$ laboratory temperature without a separately supplied energy-unit and calibration bridge. |
| $N,d$ | positive integers | Finite truncation/engineered dimension and qubit count, with $N=2^d$ for the source's rate normalization. Calling $N\to\infty$ a thermodynamic limit requires the declared embedding, normalization, and observable limit; finite $N$ is not a phase-transition singularity. |
| $H_{0,N}$ | self-adjoint operator on the declared $N$-level space | Logarithmic Hamiltonian $\sum_{n=1}^{N}\log n\mkern3mu \lvert n\rangle\langle n\rvert$ used in the engineered correspondence. |
| $Z_N(\beta_{\mathrm{eff}})$ | positive scalar | Finite normalization $\sum_{n=1}^{N}n^{-\beta_{\mathrm{eff}}}$. It is retained explicitly when comparing normalized coherence with an unnormalized Dirichlet sum. |
| $S_N(s)$ | complex scalar | Finite alternating Dirichlet sum $\sum_{n=1}^{N}(-1)^{n+1}n^{-s}$. Its fixed $s$ limit is distinct from a uniform limit over growing time windows. |
| $\eta(s)$ | holomorphic function on $\mathrm{Re}(s)>0$ | Dirichlet eta function $\sum_{n=1}^{\infty}(-1)^{n+1}n^{-s}=(1-2^{1-s})\zeta(s)$. The factor relation at $s=1$ is interpreted through its removable value. |
| $\mathcal L_N(\beta_{\mathrm{eff}},t)$ | complex observable expectation | Finite average accumulated phase factor, normalized so that $Z_N(\beta_{\mathrm{eff}})\mathcal L_N(\beta_{\mathrm{eff}},t)=-S_N(\beta_{\mathrm{eff}}+it)$ for the declared phase operation. A small measured modulus is not an exact zero without a zero-isolation certificate. |
| $\alpha_N(s)$ | nonnegative finite-size exponent when $\mathcal L_N(s)\ne0$ | Local zeta-case notation $-\log\lvert\mathcal L_N(s)\rvert/\log N$. For fixed $0<\mathrm{Re}(s)<1$, its proved limit is $1-\mathrm{Re}(s)$ off the eta zero set and $1$ on it. This fixed $s$ discriminator is not a uniform growing-time or empirical DQPT certificate. |
| $s_0,\beta_0,m,a_m,s_N$ | local zero data | $s_0=\beta_0+it_0$ is a fixed isolated eta/zeta zero in the open strip, $m$ its multiplicity, and $a_m=\eta^{(m)}(s_0)/m!$. The $m$ nearby zeros of $S_N$ localize at scale $N^{-\beta_0/m}$; for $m=1$, $s_N$ denotes the unique simple descendant root. Constants are not uniform over zero height, multiplicity, or the strip boundary. |
| $K,\sigma_K,M_K$ | compact set and nonnegative bounds | For compact $K\subset\lbrace\mathrm{Re}(s)>0\rbrace$, $\sigma_K=\min_K\mathrm{Re}(s)$ and $M_K=\max_K\lvert s\rvert$ type the local-uniform tail bound. They do not provide a uniform large $\lvert t\rvert$ result. |
| $\Gamma,D,\sigma_\Gamma,M_\Gamma,m_\Gamma$ | contour, interior, and positive bounds | $\Gamma$ is a declared positively oriented Jordan contour with interior $D$ in the critical strip; $m_\Gamma=\min_\Gamma\lvert\eta\rvert$ must have a certified positive lower enclosure. The Rouché zero-count transfer requires $N^{-\sigma_\Gamma}(1+M_\Gamma/\sigma_\Gamma)<m_\Gamma$ on the whole contour. |
| $\mathcal G_N(\beta_{\mathrm{eff}},t)$ | complex observable expectation | Finite generalized Loschmidt amplitude in the second engineered construction. Any zeta or DQPT promotion must state the coupled $N,t$ limit and its error bound. |
| $\mathcal F_{1,N}(s),\mathcal F_1(s)$ | finite-size rate and pointwise limit when defined | For $N=2^d$, $\mathcal F_{1,N}=-d^{-1}\log\lvert\mathcal L_N\rvert=(\log 2)\alpha_N$. On the open critical strip, the proved pointwise limit is $(1-\mathrm{Re}(s))\log 2$ off the zeta-zero set and $\log 2$ on it, so its discontinuity set is exactly that zero set. The jump at $s_0$ is $\mathrm{Re}(s_0)\log 2$. This does not supply uniform near-zero convergence or a finite-size empirical singularity. |
| $\iota_\beta(t)=\beta+it$ | continuous real-time slice into the critical strip | The sliced rate is discontinuous exactly at ordinates $t$ for which $\zeta(\beta+it)=0$, with jump $\beta\log 2$. This is an ideal pointwise-limit statement, not an experimental singularity certificate. |

## Collatz recursive-sufficiency case-study notation

These symbols are local to the version 1.4.0 number-theory application. They
do not redefine the global BSC transport, target, time, or system symbols.

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $T:\mathbb N\to\mathbb N$ | shortcut Collatz map | $T(n)=n/2$ for even $n$ and $T(n)=(3n+1)/2$ for odd $n$. This local $T$ is not a BSC state-transport field. |
| $s_j(n)$ | integer in $\lbrace0,\ldots,j\rbrace$ | Number of odd terms among $n,T(n),\ldots,T^{j-1}(n)$. Its length $m$ vector is determined by $n\bmod2^m$. |
| $d(A)$ | number in $[0,1]$ | Natural density of the periodic set $A$ in the Collatz application. |
| $H_2(p)$ | number in $[0,1]$ | Binary entropy $-p\log_2p-(1-p)\log_2(1-p)$, with the continuous endpoint convention. |
| $F_n$ | periodic subset of $\mathbb N$ | Ansari's declared ternary family. The audit proves the first missing layer but does not prove $F_n$ recursively sufficient for $n\ge2$. |
| $U_m$ | periodic subset modulo $2^m$ | Unconditional prefix sieve $\lbrace n:7s_j(n)>4j,\ 1\le j\le m\rbrace$. Its complement has an exact descent prefix. |
| $B_0$ | positive integer | External verified-base boundary $2^{71}$. BSC does not replay the computation below it; its role in BSC-CRS-04–06 is conditional. |
| $V_m$ | periodic subset modulo $2^m$ | Cutoff-conditioned prefix sieve $\lbrace n:485s_j(n)>306j,\ 1\le j\le m\rbrace$. |
| $G$ | five residue classes modulo 36 | $3,7,15,19,27\pmod {36}$, obtained from $F_1$ after removing the explicitly recursive $31$ class. |
| $W_m$ | periodic subset modulo $9\cdot2^m$, $m\ge2$ | $G\cap V_m$. Its recursively-sufficient status inherits the declared $B_0$ condition; the $m\ge2$ scope is required for the displayed $5/9$ CRT density factor. |
| $H_{n,m}$ | periodic recursively-sufficient set | $F_n\cup(F_1\cap S_m)$ for the declared RS safety-net family $S_m\subset4\mathbb N_0+3$. It retains the ternary spine without promoting $F_n$. |

## Sheaf, interface, and symmetry notation

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $\mathscr F$ | sheaf or presheaf | Assigns local observation spaces and restriction maps to contexts. |
| $\rho^U_V$ | restriction map | From sections on $U$ to sections on $V\subseteq U$. |
| $C^0,C^1$ | finite cochain spaces | Vertex assignments and edge discrepancies for the declared cellular sheaf. |
| $d^0$ | $C^0\to C^1$ | Signed restriction difference. |
| $L_{\mathscr F}$ | PSD operator | Sheaf Laplacian $(d^0)^*d^0$ under declared inner products. |
| $\mathcal T$ | set of port types | Used only in the interface-category section; distinct from target record by local scope. |
| $\mathsf I_{\mathcal T}$ | full subcategory of $\mathrm{Set}/\mathcal T$ on finite domains | Finite typed ports and type-preserving maps, even when $\mathcal T$ is infinite. |
| $\mathsf C$ | finite-colimit category | Internal carriers for structured cospans. |
| $L:\mathsf I_{\mathcal T}\to\mathsf C$ | left-adjoint strong symmetric monoidal functor | Embeds a typed interface as a free boundary carrier. |
| $\mathcal D_{\mathsf r,\mathbb T}$ | assumed lax symmetric monoidal functor $(\mathsf C,+)\to(\mathrm{Set},\times)$ | Conditional schema transporting fixed-mode, fixed-clock decorations through carrier maps and pushouts. The manuscript proves the generic cospan theorem under this assumption; a canonical eight-field BSC instance remains open. |
| $L(A)\to N\leftarrow L(B)$ | structured cospan | Open system with internal apex $N$. |
| $\mathbb T_N$ | time object | Discrete monoid, interval category, stochastic clock, or other declared clock. |
| $\mathsf{Beh}_N$ | behavior semantics | Deterministic map/flow, stochastic kernel, or nondeterministic relation. |
| $D_a$ | object of a declared $k$-linear additive monoidal defect category | Non-invertible defect; an action on a physical system requires a monoidal functor to its endomorphism category. |
| $N_{ab}^{\ c}$ | nonnegative integer in the basic finite fusion record | Multiplicity in $D_a\otimes D_b\simeq\bigoplus_cD_c^{\oplus N_{ab}^{\ c}}$. Higher multiplicity objects require a separately typed higher-category variant. |

## Topology, charge, and status

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $[\omega]$ | $H^k(M;A)$ | Cohomology class with declared abelian coefficient group $A$; for de Rham pairing, $A=\mathbb R$ and $\omega$ is a closed form. |
| $[C]$ | $H_k(M;\mathbb Z)$ | Integral homology class. |
| $Q_{\mathrm{top}}$ | $A$ | Kronecker evaluation $\langle[\omega],[C]\rangle$; purely topological. |
| $\chi$ | $\mathrm{Dom}(\chi)\subseteq A\to Q_{\mathrm{phys}}$ | Physically derived bridge required when a claim promotes a topological invariant to physical charge; units and normalization required. It is not a definition of every physical charge. |
| $q_{\mathrm{phys}}$ | physical charge space | $\chi(Q_{\mathrm{top}})$ only for a declared topology-to-charge claim after the bridge is certified. |
| $\mathsf{Stat}(c)$ | six-coordinate record | $(v_{\rm math},s_{\rm math},s_{\rm emp},s_{\rm comp},s_{\rm src},s_{\rm tr})$: a mathematical verdict plus five readiness coordinates. |
| $v_{\rm math}$ | categorical verdict | One of ill-posed, open, true, or false; it is not ordered by evidential strength and never propagates by meet. |
| $s_{\rm math}$ | readiness chain | none, conjectural, conditional, or proved. |
| $D=(\mathcal C,E)$ | finite DAG | Claim-dependency graph. |
| $a\xrightarrow{J}b$ | dependency edge | Names only readiness coordinates constrained by the dependency. |
| $\kappa_{e,j}$ | monotone cap map $\mathsf{Stat}(a)\to L_j$ | Caps descendant readiness coordinate $j$ on dependency edge $e$; it does not set the descendant verdict. |

## Deliberately separated symbol families

| Collision avoided | Manuscript convention |
|---|---|
| dynamics kernel vs post-processing | $K_\ell^{\mathrm{dyn}}$ vs $K_{\ell m}$ |
| context vs completion | $C_\ell$ vs $C_{\ell m}$ |
| inherited transform registry vs equation residual | $R_\ell$ vs $R_{\ell m}$, with namespaced $R^X,R^Y,E_\partial$ where possible |
| observation kernel vs horizon | $H_\ell^{\mathrm{obs}}$ vs $h$ |
| target record vs port-type set | $\mathcal T^{\mathrm{rep}}$ is the repaired experiment target; $\mathcal T$ is used for port types only inside the interface-category section |
| experiment admission/disposition vs inverse-problem classes | $\mathcal A,\mathcal D$ are experiment maps; $\mathcal A_\partial,\mathcal D_\partial$ are the namespaced admissible-interior and boundary-data classes |
| experiment score vs morphism loss vector | $\mathcal L$ vs $\mathcal L_{\ell m}$ |
| trace vs target-time symbol | $\tau_\partial$ is trace; $h$ is horizon; $\tau_V$ is viability exit time |
| reconstruction relation vs selected extension | $E_\partial$ is set-valued and quotient-valued; $e_\partial$ is a chosen representative map with separately assumed regularity |
| quotient map vs identity observable | $q_\ell^{\mathrm{quot}}:X_\ell\to\bar X_\ell$ vs $q_\ell^{\mathrm{id}}:\bar X_\ell\to Q$ |
| implemented channel error vs deficiency | $e_{\ell m}(K)$ evaluates one declared $K$; $\delta_{\ell m}$ optimizes over all Markov kernels, while $\delta_{\ell m}^{\mathrm{impl}}$ optimizes only over the declared implementation class |
| exact equivalence vs tolerance relation | $\sim_H$ and $\sim_{\mathcal A_{\mathrm{acc}}}$ are exact; positive $\varepsilon$ confusability is generally nontransitive |
| history policy vs state-marginal fold | $\pi_{\ell,t}$ acts on histories; $F_{\ell,t}^{\bar\pi}$ exists only after a state-Markov policy or sufficient state augmentation is supplied |
| residual space vs joint configuration space | $Z_\ell$ carries equation residuals; $\mathsf Z_\ell^{\mathrm{sc}}=\bar X_\ell\times U_\ell\times C_\ell$ carries completed joint states |
| Volume II morphism vs extended morphism | $\mu^{\mathrm{II}}$ retains $(R_X,R_Y,R_U,R_C,\alpha_H,\alpha_K,q_{ab},b_\mu)$; $\mathfrak M_{\ell\to m}$ is the later eight-field typed extension |
| cohomology vs path defect | “Cohomology” appears only with a coefficient complex and differential; otherwise use naturality/path defect. |
| persistence exit bound vs zeta parameter | $\beta_i$ is a one-step exit-event bound; $\beta$ or $\beta_{\mathrm{eff}}$ is the locally declared real part/effective inverse-temperature parameter in the zeta–DQPT case study. |
| interface apex vs zeta truncation | $N$ is a structured-cospan apex inside §12.1 and a positive truncation integer only inside the zeta–DQPT case study. |
| state transport vs shortcut Collatz map | $T_{\ell m}$ is a BSC state transport; unadorned $T$ denotes the shortcut Collatz map only inside the BSC-CRS/F11 application. |
