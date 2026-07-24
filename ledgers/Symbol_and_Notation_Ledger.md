# Symbol and Notation Ledger

This ledger is normative for *On Boundaries of Evidence*, version 1.0.1. A symbol has no
meaning outside the row or local declaration that types it. Local
specializations are permitted only when their scope is explicit.

## Global conventions

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $\ell,m,n,a,b$ | scale or description labels | Labels, not necessarily real-valued scales. A numerical scale parameter is declared separately. |
| $t,h$ | time and prediction horizon | $t$ belongs to the declared time object; $h>0$ is the repaired horizon symbol. The source-only target record used $H$ for the horizon; the manuscript quotes that record before replacing $H$ by $h$. |
| $X\rightsquigarrow Y$ | Markov kernel | Measurable map $x\mapsto K(x,\cdot)\in\mathcal P(Y)$. |
| $L\odot K$ | composite kernel | $(L\odot K)(x,A)=\int L(y,A)K(x,dy)$. |
| $\delta_f$ | deterministic kernel | Dirac kernel induced by measurable $f$. |
| $f_\#\mu$ | probability measure | Pushforward of $\mu$ by $f$. |
| $B_b(X)$ | vector space | Bounded Borel real- or complex-valued functions on $X$. |
| $\|\cdot\|_{\mathrm{TV}}$ | $[0,1]$ | Total variation; for finite distributions, one half of the $\ell^1$ distance. |
| $W_p$ | $[0,\infty]$ | $p$-Wasserstein distance on a declared metric space; finite-moment assumptions required. |
| $W_{p,Q}$ | $[0,\infty]$ | $p$-Wasserstein distance on the specifically declared metric space $(Q,d_Q)$, with domain $\mathcal P_p(Q)\times\mathcal P_p(Q)$. The subscript $Q$ may be suppressed only inside a scope where the ground metric is unambiguous. |
| $\mathbb P,\mathbb E$ | probability, expectation | Always relative to the locally declared law. |
| $\operatorname{Tr}$ | scalar | Trace on the locally declared trace-class/operator pairing. |
| $\mathrm{id},\mathrm{Id}$ | identity | Identity map or identity operator, clear from type. |
| $\preceq,\bigwedge$ | readiness order and meet | Used only on declared readiness semilattices, not on mathematical verdicts and not as numerical inequality. |

## Retained BSC system objects

| Symbol | Type or codomain | Meaning and constraints |
|---|---|---|
| $S_\ell(t)$ | 12-field record | Original Volume I system tuple, transcribed in manuscript equation (4.1) from a hash-identified supplied source that is not independently inspectable in this release. |
| $\widehat S_\ell$ | 14-field record | Supplied measurable repair from Volume II, described by Volume III as adopted and transcribed in equation (4.2), subject to the same source-availability limitation. |
| $\Omega_\ell$ | bounded domain or finite carrier | “Finite” may refer to domain, horizon, resources, or cardinality; the intended meaning must be stated. |
| $\partial\Omega_\ell$ | geometric boundary | Used only when a geometric boundary is part of the model. |
| $\partial_\varepsilon\Omega_\ell$ | measurable sensor layer | $\{x:\operatorname{dist}(x,\partial\Omega_\ell)\le\varepsilon\}$ when geometric; not an ideal trace. |
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
| $\operatorname{rent}_\ell$ | inherited admission diagnostic | Present only in the original tuple. It has no universal numerical type and is moved to admission/certificate records. |
| $\mathscr C_\ell$ | companion record | $(D_\ell^{\mathrm{rec}},\mathsf{Prov}_\ell,\mathsf{Cert}_\ell)$; associated with, but not inserted into, $\widehat S_\ell$. |
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
| $\mathcal D$ | disposition map | Codomain $\{\mathrm{admit},\mathrm{sandbox},\mathrm{watch},\mathrm{demote},\mathrm{retire}\}$. |
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
| $d_{\mathcal A_{\mathrm{acc}}}(\rho,\sigma)$ | $[0,1]$ | $\sup\{|\operatorname{Tr}[E(\rho-\sigma)]|:0\le E\le I,\ E\in\mathcal A_{\mathrm{acc}}\}$; a pseudometric determined by accessible effects. |
| $\rho\sim_{\mathcal A_{\mathrm{acc}}}\sigma$ | exact operational equivalence | Defined by $d_{\mathcal A_{\mathrm{acc}}}(\rho,\sigma)=0$. It asserts equality of all accessible probabilities, not equality of density-matrix representatives. |
| $d_{\mathcal A_{\mathrm{acc}}}(\rho,\sigma)\le\varepsilon$ | $\varepsilon$-confusability relation | For $\varepsilon>0$ it is generally nontransitive; no tilde/equivalence notation is used for it. |
| $\Phi$ | state channel | Positive stochastic or CPTP map, as locally declared. |
| $\Phi^\sharp$ | observable pullback | Adjoint satisfying $\operatorname{Tr}[\Phi(\rho)A]=\operatorname{Tr}[\rho\Phi^\sharp(A)]$. |
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
| $D_{\ell n}$ | measurable subset of $D_{\ell m}$ | $\{x\in D_{\ell m}:T_{\ell m}(x,D_{mn})=1\}$, the support-compatible domain of a partial composite. |
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
| $\widehat D_{\ell n}$ | measurable subset of $\widehat D_{\ell m}$ | $\{z\in\widehat D_{\ell m}:\widehat T_{\ell m}(z,\widehat D_{mn})=1\}$; completion compatibility also requires its state projection to lie in $D_{\ell n}$. |
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
| $\mathfrak r_{\ell m}$ | nonnegative residual evaluation | $\sup_{\zeta\in\mathcal Q_{\ell m}^{\mathrm{res}}}\mathsf{ev}_{\ell m}^{\mathrm{res}}(R_{\ell m},\zeta)$. The deterministic specialization is $\sup_{x\in D_{\ell m}^{\mathrm{eval}}}\|R_{\ell m}(x)\|_{Z_m}$; stochastic weak residuals use a different evaluator. |
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
| $\mathsf E_i=\{P_{i,\theta}\}$ | statistical experiment | Common parameter family required for direct deficiency composition. |
| $\mathfrak K_{\ell m}^{\mathrm{all}}$ | all Markov kernels $Y_\ell\rightsquigarrow Y_m$ | Comparison class for the ordinary Le Cam deficiency. A smaller implementation class $\mathfrak K_{\ell m}^{\mathrm{impl}}\subseteq\mathfrak K_{\ell m}^{\mathrm{all}}$ must be declared separately. |
| $e_{\ell m}(K)$ | $[0,1]$ | Error of one declared or implemented channel $K:Y_\ell\rightsquigarrow Y_m$: $\sup_{\theta\in\Theta}\|KP_{\ell,\theta}-P_{m,\theta}\|_{\mathrm{TV}}$, where $(KP)(A)=\int K(y,A)P(dy)$. It records the tested channel, not the optimum over channels. |
| $\delta(\mathsf E,\mathsf F)$ | $[0,1]$ | Infimum simulation error from $\mathsf E$ observations to $\mathsf F$ observations. Zero means arbitrarily accurate simulation; an exact simulating channel additionally requires attainment or an applicable randomization theorem. |
| $\delta_{\ell m}$ | $[0,1]$ | Ordinary directed deficiency $\inf_{K\in\mathfrak K_{\ell m}^{\mathrm{all}}}e_{\ell m}(K)$. Always $\delta_{\ell m}\le e_{\ell m}(K)$; equality requires an attained infimum and an optimizing implemented channel, neither of which is automatic. |
| $\delta_{\ell m}^{\mathrm{impl}}$ | $[0,1]$ | Constrained deficiency $\inf_{K\in\mathfrak K_{\ell m}^{\mathrm{impl}}}e_{\ell m}(K)$. It is at least $\delta_{\ell m}$ and must not be reported as the unconstrained Le Cam deficiency. |
| $\Delta(\mathsf E,\mathsf F)$ | $[0,1]$ | Symmetric maximum of the two directed deficiencies; introduced only when needed. |
| $\succeq_B$ | preorder | Blackwell dominance: exact stochastic simulation/garbling. |
| $\mathcal K_F$ | observable operator | Koopman action $[\mathcal K_Fg](x)=g(F(x))$. |
| $\phi,\lambda$ | observable and complex scalar | Candidate Koopman eigenfunction and eigenvalue. |
| $\varepsilon_{\mathrm{dyn}}$ | nonnegative norm | Full declared-space residual $\|\mathcal K_F\phi-\lambda\phi\|$. |
| $q_\ell^{\mathrm{id}}$ | $\bar X_\ell\to(Q,d_Q)$ | Declared identity/task observable used for recurrence and persistence. The manuscript may suppress the superscript in a persistence-only scope; it is distinct from $q_\ell^{\mathrm{quot}}:X_\ell\to\bar X_\ell$. |
| $F_i$ | $\bar X_i\times U_i\times C_i\rightsquigarrow\bar X_{i+1}$ | Completed admissible joint-input fold. |
| $P_i$ | $\bar X_i\rightsquigarrow\bar X_{i+1}$ | State-marginal kernel induced from $F_i$ by a certified state-Markov policy $\bar\pi_i$; history dependence requires state augmentation. |
| $\mu_{i+1}=\mu_iP_i$ | element of $\mathcal P(\bar X_{i+1})$ | State marginal after one fold; $(\mu_iP_i)(A)=\int P_i(x,A)\mu_i(dx)$. |
| $\mathbb P_{\mu_0}^{P_{0:n-1}}$ | probability law on $\prod_{i=0}^{n}\bar X_i$ | Path law generated from $\mu_0$ and the kernels $P_0,\ldots,P_{n-1}$, under standard-Borel/Ionescu--Tulcea hypotheses. Endpoint marginals alone do not determine path events. |
| $\mathbf X_k$ | coordinate random variable with values in $\bar X_k$ | State at prefix $k$ under $\mathbb P_{\mu_0}^{P_{0:n-1}}$; distinct from the raw state space $X_k$. |
| $\operatorname{Rec}_{q,n}$ | $[0,\infty]$ | Endpoint recurrence $W_{p,Q}((q_0^{\mathrm{id}})_\#\mu_0,(q_n^{\mathrm{id}})_\#\mu_n)$, defined only when both identity laws lie in $\mathcal P_p(Q)$. |
| $\tau_V$ | $\mathbb N_0\cup\{\infty\}$-valued stopping time | First viability exit $\inf\{k\ge0:\mathbf X_k\notin V_k\}$ under the declared path law, with $\inf\varnothing=\infty$. Measurability and adaptedness of $V_k$ are required. |
| $\alpha_k^{\mathrm{cum}}$ | $[0,1]$ | Declared cumulative prefix tolerance for $\mathbb P(\tau_V\le k)$. |
| $\beta_i$ | $[0,1]$ | Declared one-step exit-event bound, used in $\mathbb P(\tau_V\le n)\le\sum_{i=0}^{n}\beta_i$. It must not be conflated with the cumulative tolerance $\alpha_n^{\mathrm{cum}}$. |
| $E_i,e_i,L_i$ | common-unit errors and dimensionless propagation factor | Homogeneous identity error, one-step injection, and Lipschitz coefficient. Other defect coordinates remain separate. |
| $R^X_{ab}$ | state scale map | Direct state coarse-graining, namespaced from equation residual. |
| $T^{\mathrm{dyn}}_{ab}$ | nonnegative Wasserstein defect | Failure of a state scale map to intertwine source and target dynamics on a declared Polish target state space $(\bar X_b,d_b)$; all displayed and propagated laws must lie in $\mathcal P_p(\bar X_b)$. |
| $\varepsilon$ | scale or sensor parameter | Units, limiting path, and order declared locally. |

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
| $\chi$ | $\operatorname{Dom}(\chi)\subseteq A\to Q_{\mathrm{phys}}$ | Physically derived bridge required when a claim promotes a topological invariant to physical charge; units and normalization required. It is not a definition of every physical charge. |
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
| exact equivalence vs tolerance relation | $\sim_H$ and $\sim_{\mathcal A_{\mathrm{acc}}}$ are exact; positive-$\varepsilon$ confusability is generally nontransitive |
| history policy vs state-marginal fold | $\pi_{\ell,t}$ acts on histories; $F_{\ell,t}^{\bar\pi}$ exists only after a state-Markov policy or sufficient state augmentation is supplied |
| residual space vs joint configuration space | $Z_\ell$ carries equation residuals; $\mathsf Z_\ell^{\mathrm{sc}}=\bar X_\ell\times U_\ell\times C_\ell$ carries completed joint states |
| Volume II morphism vs extended morphism | $\mu^{\mathrm{II}}$ retains $(R_X,R_Y,R_U,R_C,\alpha_H,\alpha_K,q_{ab},b_\mu)$; $\mathfrak M_{\ell\to m}$ is the later eight-field typed extension |
| cohomology vs path defect | “Cohomology” appears only with a coefficient complex and differential; otherwise use naturality/path defect. |
