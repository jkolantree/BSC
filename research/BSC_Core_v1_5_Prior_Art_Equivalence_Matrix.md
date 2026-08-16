# BSC Core v1.5 prior-art equivalence matrix

## Scope and verdict vocabulary

This is a claim-limiting research map for the
[BSC Core v1.5 foundations note](../framework/BSC_Core_v1_5_Foundations.md).
It is not a completeness claim and not a novelty certificate. The search
cutoff for this version is **15 August 2026**. Sources below are primary
papers, author manuscripts, or publisher records; preprints remain labeled as
such.

| Relation | Meaning |
|---|---|
| Direct antecedent | The source already contains substantially the same mathematical primitive or theorem family. |
| Close overlap | The structures are materially similar, but no formal equivalence with BSC has been proved. |
| Substrate | The source supplies machinery that BSC may instantiate only after discharging additional hypotheses. |
| Analogy only | Similar language or directionality does not establish a mathematical identification. |
| Novelty unknown | The inspected sources do not settle whether a precisely delimited BSC integration is new. |

## Equivalence matrix

| Area and primary source | Established result in the source | BSC overlap or distinction | Consequence for BSC claims |
|---|---|---|---|
| Markov categories — [Fritz, *A synthetic approach to Markov kernels, conditional independence and theorems on sufficient statistics*](https://arxiv.org/abs/1908.07021) | Develops categorical probability with Markov kernels, conditional independence, disintegration, almost-sure equality, and sufficient statistics. | BSC report channels, stochastic transports, and sufficient-report language use this established substrate. BSC adds claim-local gates and artifact records, not the probability theory. | **Direct antecedent / substrate.** Do not claim invention of categorical stochastic kernels, sufficiency, or data processing. |
| Blackwell comparison — [Blackwell, *Equivalent Comparisons of Experiments*](https://doi.org/10.1214/aoms/1177729032) | Relates informativeness of experiments, decision risks, and stochastic garbling. | BSC's directed experiment comparison is in the Blackwell lineage. | **Direct antecedent.** The order and risk meaning are established statistics. |
| Deficiency and approximate sufficiency — [Le Cam, *Sufficiency and Approximate Sufficiency*](https://doi.org/10.1214/aoms/1177700372); [Torgersen, *Comparison of Statistical Experiments*, chapter 6](https://doi.org/10.1017/CBO9780511666353) | Develops directed deficiency and risk-based comparison of statistical experiments; Torgersen gives a systematic treatment of deficiencies. | BSC's $\delta_{\mathrm{do}}$ is ordinary directed deficiency after expanding the shared parameter index to intervention–parameter pairs and requiring one uniform comparison kernel. | **Direct antecedent.** Intervention indexing does not create a new deficiency theory; BSC's contribution, if any, must lie in the surrounding typed causal and evidence contract. |
| Categorical Blackwell comparison — [Fritz, Gonda, Perrone, and Rischel, *Representable Markov Categories and Comparison of Statistical Experiments in Categorical Probability*](https://arxiv.org/abs/2010.07416) | Proves a categorical Blackwell–Sherman–Stein theorem and studies representable Markov categories. | This is closer prior art than a generic Markov-category citation for any categorical BSC experiment comparison. | **Direct antecedent / substrate.** A BSC theorem must identify its extra typed certificate or defect content precisely. |
| Causal abstraction — [Rubenstein et al., *Causal Consistency of Structural Equation Models*](https://arxiv.org/abs/1707.00819) | Defines exact transformations between structural equation models and stresses agreement under interventions. | BSC's proposed intervention map and do-commutation requirement overlap directly with established causal-consistency questions. | **Direct antecedent.** Observational agreement cannot be promoted to causal abstraction. |
| Exact and approximate causal abstraction — [Beckers and Halpern, *Abstracting Causal Models*](https://arxiv.org/abs/1812.03789); [Beckers, Eberhardt, and Halpern, *Approximate Causal Abstraction*](https://arxiv.org/abs/1906.11583) | Gives increasingly strong exact abstraction notions and extends them to approximate deterministic and probabilistic abstractions. | BSC's proposed causal-transfer profile overlaps in intervention alignment, exactness, approximation, and model-level abstraction. | **Close direct overlap.** BSC must compare definitions and error composition before claiming a new causal abstraction. |
| Compositional causal abstraction — [Lorenz and Tull, *Causal and Compositional Abstraction*](https://arxiv.org/abs/2602.16612), preprint | Defines abstractions as natural transformations for compositional models with queries and semantics in monoidal, cd, or Markov categories; interventions are a central case. | Very close to BSC's proposed causal and compositional layer, including upward and downward query mappings. | **Close overlap / likely substrate.** A BSC-specific contribution must be stated after a definition-by-definition comparison. |
| Optics — [Riley, *Categories of Optics*](https://arxiv.org/abs/1809.00738) | Gives a general optic construction, functoriality, a universal property, and lawfulness conditions for bidirectional accessors. | BSC has forward transport and contravariant observable pullback, but that pair is not automatically an optic and no optic laws or representation theorem have been proved for it. | **Analogy only unless constructed.** Do not market the eight-field record as an optic without a typed equivalence and lawfulness proof. |
| Decorated cospans — [Fong, *Decorated Cospans*](https://arxiv.org/abs/1502.00872) | Builds symmetric monoidal categories from lax braided monoidal decoration functors. | Generic decorated-cospan composition resembles BSC's proposed open-system wiring, but it does not supply BSC's actual decoration functor. | **Substrate.** The BSC-specific functor and its coherence remain proof obligations. |
| Structured and decorated cospan double categories — [Baez, Courser, and Vasilakopoulou, *Structured versus Decorated Cospans*](https://arxiv.org/abs/2101.09363) | Constructs symmetric monoidal double categories of structured and decorated cospans and proves an isomorphism under stated hypotheses. | Supports the proposed displayed or double-category direction. It does not prove closure of BSC's observations, residuals, losses, domains, or certificates. | **Substrate.** Generic theorems cannot be cited as completion of the BSC eight-field composition problem. |
| Assume–guarantee contracts — [Incer, Benveniste, and Sangiovanni-Vincentelli, *Some Algebraic Aspects of Assume-Guarantee Reasoning*](https://arxiv.org/abs/2309.08875) | Develops Boolean-algebra-based contract operations, refinement, composition, quotient, monoids, semirings, actions, and abstractions. | BSC dependency caps and admission rules share compositional-contract concerns but operate on evidence readiness rather than behavior assumptions and guarantees. | **Close overlap.** BSC should compare its cap algebra with contract refinement and quotient operations before claiming a new contract calculus. |
| Monotone fixed points — [Tarski, *A Lattice-Theoretical Fixpoint Theorem and Its Applications*](https://msp.org/pjm/1955/5-2/pjm-v5-n2-p11-s.pdf) | Proves that fixed points of a monotone self-map of a complete lattice form a complete lattice. | The cyclic readiness theorem is a finite descending-iteration specialization with an explicit cap-feasibility interpretation. | **Direct antecedent.** The fixed-point existence and greatestness mechanism is not novel. |
| Iterative lattice analysis — [Cousot and Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*](https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml) | Uses ordered abstractions and fixed-point construction or approximation for program analysis, including finite iterations. | BSC's finite cap iteration is structurally a monotone dataflow closure over a product order. | **Close overlap / direct method antecedent.** BSC's distinctive question is evidentiary typing and claim-local demotion, not fixed-point iteration itself. |
| Semiring provenance — [Green, Karvounarakis, and Tannen, *Provenance Semirings*](https://web.cs.ucdavis.edu/~green/papers/pods07.pdf) | Unifies several database provenance semantics using semiring annotations and polynomial provenance. | BSC's evidence lineage, alternative derivations, and compositional source records overlap with provenance algebra. Hashes add byte identity but not semantic provenance. | **Direct antecedent / substrate.** BSC should specify any provenance semiring or explain why its certificate algebra differs. |
| Test cover — [Gutin, Muciaccia, and Yeo, *(Non-)existence of Polynomial Kernels for the Test Cover Problem*](https://arxiv.org/abs/1204.4368) | Defines binary tests that distinguish pairs of items and seeks a minimum distinguishing subcollection; records hardness results. | When the BSC target query is injective and reports are binary, its distinguishing-pair construction is exactly Test Cover. Multi-valued reports give a partition-test generalization; non-injective targets require only pairs in different target fibers. | **Direct combinatorial antecedent.** The finite reduction to set cover is not itself a novelty candidate. |
| Minimal model-testing experiments — [Healy and Leo, *Which Experiments Test a Model?*](https://doi.org/10.1016/j.jet.2026.106191) | Characterizes experiments that test or classify preference models through separated pairs and solves a resulting set-cover problem for minimal experiments. | This 2026 result is especially close in motivation: target classes induce required separated pairs, experiments distinguish them, and minimum design becomes set cover. Its preference-ranking and boundary-pair geometry are more specialized than the BSC set-map theorem. | **Very close contemporary overlap.** Any BSC originality claim requires a direct comparative proof; current status is novelty unknown. |

## Theorem-by-theorem novelty disposition

| BSC Core v1.5 item | Prior-art disposition | Safe present description |
|---|---|---|
| Product readiness over applicable coordinates | Standard product-order construction; the evidence-field selection is BSC policy. | A typed repair proposal with an elementary product-semilattice proof. |
| `N/A` as an absent dependent coordinate | Standard typing discipline; no located source establishes BSC originality. | A semantics-preserving design choice, not a new theorem of order theory. |
| Finite cyclic greatest-compatible fixed point | Special case of monotone fixed-point and dataflow theory. | A BSC-specific formulation and proof, not a novel fixed-point theorem. |
| DAG one-pass corollary | Standard topological evaluation of acyclic dependencies. | A compatibility result connecting the old DAG rule to the cyclic semantics. |
| Fiber, kernel, quotient, and factorization equivalence | Standard quotient universal-property reasoning. | A self-contained operational identifiability lemma. |
| Target-separated-pair cover | Test-cover and minimal-experiment antecedents are direct and strong. | A target-relative formulation integrated with BSC reports. |
| Oscillation monotonicity | Elementary set containment under added constraints. | A useful BSC certificate quantity, not a novelty claim. |
| Local decision-margin theorem | Elementary metric argument; constants depend on the exact convention. | A carefully scoped sufficient condition for one declared decision. |
| Intervention-indexed deficiency | Ordinary deficiency on the expanded parameter set of intervention–parameter pairs. | A proposed BSC profile specialization; mathematical novelty not claimed. |
| Integrated claim/evidence/certificate architecture | No equivalence established by this review, but every major primitive has close antecedents. | **Novelty unknown.** Candidate originality lies only in a precisely proved integration, if external review confirms it. |

## Required comparisons before any originality claim

1. Give a definition-by-definition translation between the BSC causal profile
   and exact, approximate, and compositional causal abstraction.
2. State whether BSC's intervention selector is a target-relative Test Cover,
   a special case of the Healy–Leo construction, or a distinct constrained
   problem. Prove the claimed relationship.
3. Construct the actual BSC decoration or displayed structure and verify its
   functoriality, units, associativity, and interchange. A citation to the
   generic cospan theorem is insufficient.
4. Decide whether certificate alternatives and conjunctions form a declared
   provenance semiring. If not, state the obstruction.
5. Separate the assume–guarantee behavior algebra from the evidence-readiness
   cap algebra, then prove any bridge between them.
6. Treat forward transport plus observable pullback as an optic only if the
   residual object, laws, and universal comparison have been constructed.
7. Search field-specific experiment-design, sensor-selection, diagnosis, test
   cover, and active-learning literature before assigning a novelty status to
   the integrated intervention theorem.

## Research limitations

- This matrix is a bounded primary-source pass, not a systematic review.
- A missing source is not evidence of novelty.
- Several cited items are preprints and are identified as such.
- The matrix compares mathematical structures, not priority dates for every
  possible verbal formulation.
- No external human specialist has certified the equivalence judgments.
- A formal equivalence or non-equivalence proof remains necessary wherever the
  matrix says close overlap, substrate, or analogy only.

## Current public conclusion

The inspected literature supports BSC's use of these tools, but it sharply
narrows the defensible originality claim. Markov kernels, Blackwell
comparison, causal abstraction, optics, cospan composition, assume–guarantee
algebra, monotone fixed points, semiring provenance, pair separation, and set
cover are established. The only plausible originality question left by this
pass is whether BSC defines and proves a useful **joint contract** connecting
claim-relative identifiability, noncompensating readiness, causal defects, and
artifact-bound admission. That question remains open.
