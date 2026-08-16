# BSC AI-assisted research evidence profile

**Status:** proposed normative certificate profile for BSC Core v1.5

**Role:** govern AI-assisted mathematical and scientific work without treating
model confidence, agent agreement, or presentation quality as independent
evidence

## 1. Governing principle

AI assistance may increase the rate of conjecture generation, proof search,
formalization, software construction, literature retrieval, and adversarial
testing. It does not change the authority required for the resulting claim.

> Freeze the target before evaluation. Separate candidate generation from
> verification. Bind every promotion to the exact proposition, artifact, trust
> base, and evidence that actually passed.

This profile refines the BSC certificate field. It does not add an “AI” badge
to the truth value of a claim and does not create a ninth morphism component.

## 2. Frozen target record

Before a validation run begins, record:

- a stable claim identifier;
- the exact mathematical or scientific statement;
- all quantifiers, domains, side conditions, conventions, and units;
- the decision threshold and tolerance, if any;
- the allowed axioms, source results, datasets, and external assumptions;
- the acceptance and rejection criteria;
- the evaluation fixtures and mutation policy;
- the intended authority ceiling;
- canonical bytes and a cryptographic digest of the record.

### Target-change rule

Any material change to the proposition, hypotheses, domain, semantics,
tolerance, acceptance rule, or trusted base creates a new target and a new run.
Evidence used to discover or tune the revised target becomes development or
regression evidence. It is not untouched evaluation evidence for the revision.

Typographical normalization may retain the target identity only when an
independent semantic review records that the proposition is unchanged.

## 3. Required evidence record

| Section | Required content |
|---|---|
| Target | Frozen target identity, bytes, digest, scope, and authority ceiling |
| Candidate | Exact proof, program, model, dataset, or argument submitted for judgment |
| Generation provenance | Model/tool names, version identities, system and user instructions, sampling controls, seeds when exposed, budgets, retrieval sources, and run identifiers |
| Environment | Operating system, architecture, dependencies, solver/checker versions, lockfiles, and relevant resource bounds |
| Search history | Material failed candidates, counterexamples, target revisions, and invalid trials |
| Semantic mapping | Human-readable explanation of how the artifact expresses the frozen target |
| Mechanical verification | Exact command or procedure, exit status, outputs, hashes, axioms/trust report, and resource outcome |
| Independent verification | Verifier implementation and organizational/model independence classification |
| Scientific validation | Dataset identity, design, controls, identification assumptions, statistical method, and external validity limits |
| Prior-art review | Queries, dates, databases, candidate matches, adjudication, and unresolved search gaps |
| Human review | Named role or pseudonymous stable identity, expertise scope, conflicts, judgment, and unresolved objections |
| Promotion | Exact claim-local conclusion admitted, blocked promotions, and linked evidence identities |

Unavailable secret-bearing prompts or private data may be retained in an
access-controlled location with an identity record available to authorized
auditors. Do not publish a bare hash as if it supplied confidentiality:
low-entropy or guessable private material can be recovered by dictionary
testing. Where a public commitment is necessary, use a reviewed salted or
keyed construction appropriate to the threat model, keep the secret material
private, and state that the public run is not fully reproducible.

For fixed certificate schemas, a required but inapplicable field is a typed
`NOT_APPLICABLE` value with a reason. In a readiness product, by contrast, an
inapplicable axis is absent. Neither convention promotes N/A into evidence.

## 4. Separation of roles

At minimum distinguish these roles:

1. **specification owner** — fixes the target and acceptance contract;
2. **candidate generator** — proposes proofs, code, experiments, or revisions;
3. **adversarial tester** — searches for counterexamples, hidden assumptions,
   statement mismatch, and harness defects;
4. **mechanical verifier** — applies a deterministic checker to the frozen
   artifact;
5. **semantic reviewer** — checks that the formal or computational statement
   is the intended claim;
6. **prior-art reviewer** — evaluates novelty and attribution;
7. **promotion authority** — accepts only the claim supported by all applicable
   lanes.

One person may occupy several roles, but the record must say so. Multiple AI
agents instantiated from the same provider, model family, prompt, retrieval
index, or code base are correlated reviewers. Their agreement is useful for
search coverage, not independent verification.

## 5. Independence classes

| Class | Example | Permitted interpretation |
|---|---|---|
| `SELF_REPLAY` | Same model or checker repeats the run | Reproducibility signal only |
| `SAME_IMPLEMENTATION` | Different process, identical verifier code | Environment/replay diversity |
| `INDEPENDENT_IMPLEMENTATION` | Separately implemented checker over the same formal object | Stronger mechanical evidence |
| `INDEPENDENT_FORMALISM` | Different proof assistant, solver proof format, or mathematical reconstruction | Cross-formalism corroboration |
| `DOMAIN_EXPERT_REVIEW` | Qualified human checks meaning and assumptions | Semantic/scientific review within stated expertise |
| `EXTERNAL_REPLICATION` | Independent group reconstructs the result from the frozen public package | Strong reproducibility evidence |

No label is inferred from the number of agents. Independence is an evidenced
property of implementations, information paths, and institutions.

## 6. Formal-proof evidence

A proof-assistant success establishes that the encoded theorem follows from
the admitted trust base. The evidence profile must retain:

- theorem name and fully elaborated statement;
- source projection and hashes for every imported local module;
- proof-assistant and standard-library versions;
- build manifest and dependency identities;
- axiom or assumption audit;
- prohibited escape-hatch scan appropriate to the system;
- kernel/checker output;
- an independently implemented replay where proportionate to the claim;
- a semantic review matching the theorem to the public wording.

“Compiled,” “accepted,” and “checked” are incomplete without the exact checker
identity and trust boundary. A patched verifier supersedes a known-vulnerable
one for new promotions; replay through the same vulnerable implementation is
not independent repair.

## 7. Computational and empirical evidence

For exact or exhaustive computation, retain:

- canonical input and output formats;
- deterministic serialization;
- exact arithmetic or a proved enclosure discipline;
- coverage decomposition and a no-gap check;
- fail-closed resource outcomes;
- retained negative results and invalid trials;
- same-implementation receipt replay labeled as such, plus a separately
  implemented reconstruction when independent evidence is claimed;
- explicit distinction between a candidate failure and a harness failure.

For empirical science, additionally retain the design, population, sampling
frame, preprocessing, missingness, interventions, controls, uncertainty model,
and external-validity boundary. Predictive fit does not by itself identify a
causal effect. Synthetic success does not by itself establish real-world
adequacy.

## 8. Literature and novelty discipline

AI retrieval can expand search breadth but cannot certify nonexistence of prior
work. A novelty record should preserve:

- frozen claim fragments and synonyms;
- databases and date ranges searched;
- exact queries or reproducible query construction;
- citation-graph expansion;
- closest positive and negative matches;
- primary-source inspection rather than snippet-only judgments;
- domain-expert adjudication;
- unresolved language, access, indexing, and chronology gaps.

Permitted wording scales with the evidence. “We did not find a prior result in
the recorded search” is not “no prior result exists.” Standard ingredients do
not become novel merely because BSC combines them. Any originality claim must
name the specific theorem, definition, integration, or implementation at issue.

## 9. Validation lifecycle

### Gate 0 — identity freeze

Freeze target, candidate, acceptance contract, environment, and authority
ceiling. If any changes materially, issue a new run identifier.

### Gate 1 — hostile specification review

Check vacuity, inconsistent premises, missing domains, quantifier reversals,
unit errors, boundary cases, and whether the encoded claim answers the intended
question.

### Gate 2 — adversarial search

Search for counterexamples, mutation survivors, alternative interpretations,
uncovered cases, numerical instability, and hidden external assumptions.
Preserve failures; do not rerun selectively until a favorable sample appears.

### Gate 3 — deterministic verification

Run the fixed checker or experiment. Capture exact identities, outputs, resource
limits, and failure classifications. A broken controller yields
`INVALID_TRIAL`, not candidate pass or candidate failure.

### Gate 4 — independent reconstruction

Use a genuinely separate implementation, formalism, or organization where the
claim warrants it. Replaying identical code is still useful, but is labeled
accordingly.

### Gate 5 — semantic and scientific review

Confirm that the verified artifact expresses the frozen proposition and that
the admitted assumptions justify the intended scientific interpretation.

### Gate 6 — prior-art and attribution review

Resolve the closest known work and weaken novelty wording wherever the search
does not support a stronger statement.

### Gate 7 — claim-local promotion

Publish only the exact conclusion supported by the weakest applicable evidence
lane. Bind the promoted artifact to the verified commit, tree, manifest, and
receipts, then reverify the public state.

## 10. Status vocabulary

| Status | Meaning |
|---|---|
| `CANDIDATE` | Generated artifact not yet admitted |
| `COUNTEREXAMPLE_FOUND` | Valid witness refutes the frozen claim |
| `CANDIDATE_FAILED` | Valid checker rejected the candidate |
| `INVALID_TRIAL` | Harness, environment, identity, or controller made the run non-evidentiary |
| `MECHANICALLY_CHECKED` | Frozen artifact passed the named mechanical trust base |
| `SEMANTICALLY_REVIEWED` | The checked statement matches the intended public claim within the review scope |
| `INDEPENDENTLY_RECONSTRUCTED` | A separately identified route supports the same frozen claim |
| `EMPIRICALLY_SUPPORTED` | The named study supports the bounded scientific claim |
| `NOVELTY_SEARCH_RECORDED` | A reproducible search was performed; universal novelty is not implied |
| `ADMITTED` | The exact claim-local promotion rule passed |
| `UNKNOWN` | Required evidence is missing or did not terminate validly |

Statuses form a multidimensional record, not one prestige ladder. For example,
a theorem may be mechanically checked yet have unresolved novelty, or an
experiment may be replicated while contradicting a proposed model.

## 11. Minimum public certificate

A concise public certificate should expose:

1. target digest and readable statement;
2. candidate/source digest and repository identity;
3. verifier identities and independence classes;
4. exact result and status;
5. assumptions and authority ceiling;
6. preserved material failures or a pointer to them;
7. novelty wording and search boundary;
8. public artifact digest or manifest, with an explicit warning that hashes
   provide integrity binding rather than secrecy;
9. remaining unknowns.

It must not disclose secrets, private participant data, credentials, or
unreleased vulnerable details merely to maximize reproducibility. Those
constraints are reported as limitations.

## 12. Authority and originality boundary

This profile is a proposed governance integration. It does not establish that
AI-generated work is correct, that a given verifier is sound, that a scientific
model is true, or that the workflow itself is novel. Formal verification,
causal inference, provenance, reproducible computation, adversarial testing,
and scholarly review all have extensive prior literatures. Any later novelty
claim must be made separately, narrowly, and with a source-bound prior-art
record.
