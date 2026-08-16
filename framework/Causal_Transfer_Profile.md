# BSC causal-transfer profile

**Status:** proposed normative profile for BSC Core v1.5

**Role:** claim-local refinement of `Cert`, not a ninth primitive morphism field

**Implemented finite slice:** F14 checks deterministic finite identifiability,
minimum intervention cost, and tolerance-based target oscillation

## 1. Purpose

A BSC transfer can preserve an observational report while failing under an
intervention. The causal-transfer profile records the additional objects and
assumptions required before evidence may cross that boundary.

Its governing rule is:

> Observational agreement grants observational authority only. An
> interventional or counterfactual conclusion requires an explicitly declared
> causal semantics, identification argument, and claim-local certificate.

The profile does not declare a causal model true. It records exactly which
causal proposition follows if the declared model, population, interventions,
and assumptions are admitted.

## 2. Three authority levels

| Level | Object compared | Permitted conclusion | Not supplied automatically |
|---|---|---|---|
| Observational (`O`) | observed-variable laws | equality or bounded discrepancy of those laws | effects of actions, latent structure, counterfactuals |
| Interventional (`I`) | laws indexed by declared actions | effects of those actions in the declared population | cross-world or unit-level counterfactuals |
| Counterfactual (`C`) | joint potential-outcome or structural semantics | the declared cross-world query | empirical truth of the structural assumptions |

Authority is not upward-inheriting: `O` does not imply `I`, and `I` does not
imply `C`. A certificate may deliberately stop at any level.

## 3. Required record

Every causal-transfer certificate identifies the following fields. In this
fixed certificate record, “not applicable” is a typed value with a reason; it
is not evidence. This differs deliberately from the readiness product: an
axis that does not apply to a claim is absent from that product. A required
record field and an inapplicable readiness coordinate are different types and
must not be converted into one another.

| Field | Required content |
|---|---|
| Claim identity | Frozen proposition, estimand, quantifiers, tolerance, decision threshold, and population |
| Source model | Variables, state spaces, graph or structural equations, exogenous law, and observation map |
| Target model | Variables, state spaces, graph or structural equations, exogenous law, and observation map |
| Abstraction | State/variable map and its domain; any many-to-one identifications are explicit |
| Intervention family | Names, admissible values, operational meaning, scope, and cost |
| Intervention map | How each admitted source action maps to a target action; partiality is explicit |
| Laws | Observational and, when claimed, intervention-indexed laws with their population indices |
| Target functional | The claim-relevant map `q`, loss, estimand, or decision functional |
| Identification assumptions | For example consistency, positivity, exchangeability, exclusion, invariance, or structural restrictions |
| Identification argument | Factorization, adjustment, transport formula, experiment, or checked finite witness |
| Defects | Typed observational, interventional, approximation, and implementation discrepancies |
| Admission gate | Claim-local margins and a rule that does not average incomparable defects |
| Provenance | Source identities, code/data identities, environments, negative results, and verifier identities |
| Authority ceiling | Strongest conclusion admitted and an explicit list of blocked promotions |

Changing the estimand, population, intervention semantics, tolerance, or
decision threshold creates a new target record. Evidence collected while
tuning one target is not untouched validation of another.

## 4. Exact finite identifiability

Let `X` be a finite set of candidate states or completions, let
`q : X -> Z` be the target, and let `r_i : X -> Y_i` be the deterministic
report under intervention or instrument `i`. For a family `J`, write

$$
\rho_J(x)=(r_i(x))_{i\in J}.
$$

The following statements are equivalent:

1. whenever `rho_J(x) = rho_J(x')`, then `q(x) = q(x')`;
2. `ker(rho_J)` is contained in `ker(q)`;
3. `q` factors uniquely through the attainable joint reports: there is a
   unique `q_bar : image(rho_J) -> Z` with `q = q_bar o rho_J`.

The equivalence is elementary: (1) makes `q_bar(rho_J(x)) := q(x)`
well-defined; (3) implies (1); and (1) and (2) are the same fiber condition.
It establishes identifiability inside the declared finite model, not the truth
of that model.

### Pair-cover form

Define the target-separated universe

$$
U_q=\lbrace\lbrace x,x'\rbrace:q(x)\ne q(x')\rbrace
$$

and the pairs distinguished by intervention `i`,

$$
D_i=\lbrace\lbrace x,x'\rbrace:r_i(x)\ne r_i(x')\rbrace.
$$

Then

$$
J\text{ identifies }q
\quad\Longleftrightarrow\quad
U_q\subseteq\bigcup_{i\in J}D_i.
$$

For nonnegative declared costs `c_i`, minimum-cost exact identification is the
weighted set-cover problem on `U_q`. All cost minimizers remain part of the
result. A deterministic selection rule may choose one for downstream use, but
must not erase ties.

## 5. Approximate identifiability and decision margins

Give each report space a declared metric `d_i`, the target space a declared
metric `d_Z`, and each instrument a nonnegative tolerance `epsilon_i`. Define

$$
\omega_q(J,\varepsilon)
=\sup\lbrace d_Z(q(x),q(x')):
d_i(r_i(x),r_i(x'))\le\varepsilon_i
\text{ for every }i\in J\rbrace.
$$

For a finite model this supremum is an exact maximum. Adding interventions or
tightening tolerances cannot increase the admissible-pair set and therefore
cannot increase `omega_q`.

A decision may be promoted only through its declared loss or margin. For
example, a threshold decision with certified separation margin `m` is stable
under this ambiguity when the claim-specific argument proves
`omega_q < m`. Equality at the boundary is not headroom and is not silently
rounded into a pass.

Exact injectivity and tolerance-robust identification are separate statuses.
An injective report can have positive oscillation when its tolerance merges
nearby report values; F14 deliberately demonstrates this distinction.

## 6. Stochastic and causal extensions

The deterministic theorem does not authorize an i.i.d., product, or stochastic
interpretation. A stochastic profile declares joint report laws explicitly.

For experiment families `E` and `F`, one useful interventional discrepancy is

$$
\delta_{\mathrm{do}}(E,F)
=\inf_K\sup_{a,\theta}
d_{\mathrm{TV}}\left(K P^{E}_{a,\theta},P^{F}_{a,\theta}\right),
$$

where `a` ranges over admitted interventions, `theta` ranges over the declared
parameter set, and the comparison kernels `K` have a specified admissible
class. Here total variation is normalized as
`d_TV(P,Q) = sup_A |P(A)-Q(A)|`; on a finite space this is one half of the
`l1` distance and lies in `[0,1]`. Any other normalization must be stated and
its constants changed accordingly. The orientation matters. Reversing source
and target generally changes the quantity.

Any risk-transfer theorem must state its loss class and scaling convention.
An observational deficiency is not relabeled as a causal deficiency, and a
uniform interventional bound is not relabeled as a counterfactual result.

## 7. Transfer and composition discipline

For a proposed composition `A -> B -> C`, admission requires:

1. the target claim and intervention family at each boundary are compatible;
2. the intervention maps compose on the claimed domain;
3. population and selection scopes agree or have an explicit transport rule;
4. observational, interventional, and implementation defects retain their
   types;
5. the composed bound is proved for the declared loss class;
6. certificates refer to semantically compatible claims, not merely matching
   hashes.

The profile does not prescribe a single scalar “causal error.” Independent
coordinates remain independent unless a theorem supplies a justified
aggregation. Raw byte identity supplies integrity, not semantic equivalence.
A public hash is not a confidentiality control: low-entropy or guessable
private material can be recovered by dictionary testing against its digest.

## 8. Admission outcomes

| Outcome | Meaning |
|---|---|
| `ADMITTED_O` | Observational claim and its declared defect are supported |
| `ADMITTED_I` | Named interventions and estimand are identified within the declared assumptions |
| `ADMITTED_C` | Named counterfactual query follows within the declared structural semantics |
| `BOUNDED_ONLY` | A quantitative discrepancy is established, but the decision gate is not met |
| `MODEL_CONDITIONAL` | Mathematics is established conditional on unvalidated model assumptions |
| `NOT_IDENTIFIED` | At least one target-separated possibility remains observationally or interventionally indistinguishable |
| `INVALID_EVIDENCE` | The checker, model identity, target identity, or provenance contract failed |
| `UNKNOWN` | Required evidence is absent or an applicable computation did not close |

Failure at one level blocks only the affected promotion. It does not refute the
underlying scientific claim unless a valid contradiction has been established.

## 9. F14 executable slice

`fixtures/F14_intervention_identifiability/input.json` instantiates four
states, three finite reports, rational costs, finite metrics, and tolerances.
The stdlib-only checker:

- accepts only strict canonical JSON and reduced rationals;
- rejects duplicate keys, identifiers, states, queries, and metric entries;
- requires complete state/report and ordered-pair metric coverage;
- verifies positivity, separation, symmetry, and the triangle inequality;
- rejects inputs above fixed byte, nesting, identifier, metric, query,
  exact-arithmetic, enumeration, or report-size bounds;
- cross-checks fiber constancy against pair coverage on every subset within
  one implementation;
- enumerates all minimum-cost designs with deterministic tie reporting;
- computes exact rational oscillations and witnesses;
- binds the report to the exact input and checker bytes.

The result is an exact finite conditional certificate. It is not a causal or
empirical validation of any external system.

## 10. Originality boundary

Factorization through fibers, sufficient statistics, experiment comparison,
set cover, causal abstraction, and intervention semantics all have substantial
prior literatures. This profile makes no claim to have invented those ideas.
Any later originality claim must be scoped to a specific theorem or integration
and supported by a current, reproducible prior-art review. BSC's proposed
contribution here is a disciplined combination of claim identity,
interventions, typed defects, decision gates, and source-bound certificates.
