# BSC Core v1.5 recent research intake

**Cutoff:** 15 August 2026

**Purpose:** record which recent sources changed this milestone, which only
suggest future work, and which do not alter any BSC claim status

**Review boundary:** bounded primary-source intake, not a systematic review or
novelty certificate

## Reading rule

Recent publication does not itself promote a BSC claim. Each source below is
classified by what it actually changes:

- **adopted now** — an implementation or evidence-design choice in v1.5;
- **close prior art** — narrows wording or creates a comparison obligation;
- **research direction** — informs deferred work without validating it; or
- **workflow evidence** — informs process but supplies no mathematical or
  scientific authority for BSC.

Preprints are labeled. Author-reported system results are not treated as
independent replications.

## Intake table

| Source | Source status at cutoff | Direct relevance | v1.5 disposition | What it does **not** establish |
|---|---|---|---|---|
| [Lean 4.33.0 release notes](https://lean-lang.org/doc/reference/latest/releases/v4.33.0/) and [release](https://github.com/leanprover/lean4/releases/tag/v4.33.0) | Stable upstream release, 10 August 2026 | Current proof-assistant toolchain and additional correctness fixes | **Adopted now:** the separate BSC core project is pinned to Lean and mathlib v4.33.0 | A compiler release does not validate BSC's theorem statements or prose-to-Lean mapping |
| Milikic et al., [*LeanFlow: A Case Study in Workflow-Driven Lean Autoformalization*](https://arxiv.org/abs/2607.20503) | Preprint, 26 June 2026 | Reports document-level Lean project completion in two case studies and workflow ablations | **Workflow evidence:** motivates a small project with explicit statement mapping and audits | General reliability of document-to-Lean translation; external validation of BSC |
| Douglas, [*Axioms for physical reasoning: codifying the Seiberg–Witten solution in Lean*](https://arxiv.org/abs/2607.06379) | Preprint, 7 July 2026 | Exposes named physical postulates and machine-checks their mathematical consequences | **Research direction:** use explicit premise structures for future BSC physics modules | Truth of the postulates, physical validation of BSC, or a proof from first principles |
| Sargsyan, [*A cubical formalisation of conditional independence, Bayesian conditioning, and Pearl's d-separation soundness*](https://arxiv.org/abs/2606.20351) | Preprint, 18 June 2026 | Reports a constructive formalization and a structural weakness in a standard convex interchange axiom | **Research direction:** do not infer the general stochastic/causal layer from plausible algebraic prose | That BSC's current finite deterministic slice already supports Bayesian conditioning or do-calculus |
| Lorenz and Tull, [*Causal and Compositional Abstraction*](https://arxiv.org/abs/2602.16612) | Preprint, 18 February 2026 | Natural-transformation account of abstractions preserving queries and interventions | **Close prior art:** directly limits originality claims for BSC's causal/compositional profile | Formal equivalence to BSC's certificate system; completion of the BSC eight-field composition problem |
| Sargsyan, [*A cubical formalisation of topos causal models*](https://arxiv.org/abs/2607.15629) | Preprint, July 2026 | Machine-checked sieve classification, pullback gluing/collation, and Kripke–Joyal forcing for a 1-topos core over a previously verified probability/do-calculus substrate | **Research direction and close substrate:** compare before building a sheaf/topos causal layer | That directed do-calculus is proved in this topos development, or that BSC already has a sheaf, stack, or verified causal calculus |
| Vanrietvelde, [*Specifying the operational meaning of quantum reference frames*](https://arxiv.org/abs/2607.03417) | Preprint, 3 July 2026 | Centers operationally available measurements for superposed laboratories | **Research direction:** restate the QRF open problem using accessible operations and effects | Any promotion of BSC's existing documentary QRF fixture |
| Ludescher et al., [*Quantum reference frames beyond subsystems*](https://arxiv.org/abs/2607.24976) | Preprint, 27 July 2026 | Generalizes frames from subsystem factors to covariant quantum instruments | **Research direction:** compare covariant-instrument semantics before extending the QRF module | A BSC QRF theorem, experiment, or verified frame-change construction |
| Jin, Li, and Li, [*Measurement Geometry and Design for Trustworthy Generative Inverse Problems*](https://arxiv.org/abs/2606.02309) | Preprint, 1 June 2026 | Separates measurement-supported directions from prior-supplied reconstruction content and proposes acquisition rules | **Research direction:** connect future inverse-problem profiles to claim-relative distinguishability and experiment design | External validity of F14 or a general inverse-reconstruction theorem for BSC |
| Kripner and Straka, [*OpenProver: Agentic and Interactive Theorem Proving with Lean 4*](https://arxiv.org/abs/2607.09217) | Preprint/system report, 10 July 2026 | Planner–worker–verifier proof search with Lean verification | **Workflow evidence:** reinforces role separation in the AI-assisted evidence profile | That multiple workers are independent reviewers or that generated statements match intended mathematics |
| OpenAI, [*Scientific computing in the age of agentic AI*](https://openai.com/index/scientific-computing-agentic-ai/) | Exploratory field report, 28 July 2026 | Reports faster scientific-software work and a shift toward specification, verification, and stewardship | **Workflow evidence:** motivates frozen targets, measurable acceptance tests, and named stewardship | Mathematical correctness, scientific validity, independent replication, or vendor-neutral generality |

## Changes made now

The intake has four concrete effects on BSC Core v1.5:

1. the formal kernel uses the stable Lean 4.33.0 and matching mathlib release;
2. the AI-assisted profile makes statement fidelity and verifier independence
   explicit rather than equating generated code with proof;
3. the causal profile is presented as a bounded proposal with close causal
   abstraction and deficiency antecedents; and
4. the prior-art matrix treats recent minimal-experiment and compositional
   causal work as claim-narrowing evidence.

## Deferred research, not silent promotion

The following remain later projects:

- explicit physical-postulate structures for BSC electromagnetic and quantum
  modules;
- a verified general stochastic kernel, conditioning, and causal calculus;
- a covariant-instrument reformulation of the QRF open problem;
- a measurement-versus-prior decomposition for inverse reconstruction; and
- the displayed or double-category construction for the complete BSC record.

None of these sources changes the truth, execution, empirical, or novelty
status of an existing BSC claim merely by being cited.
