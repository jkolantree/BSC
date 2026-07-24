# Roadmap

This file records planned work. Nothing listed here is part of the current
evidence base.

## Completed in 1.0.1

- Typed the partial stochastic composite with a restricted observable pullback.
- Split mathematical verdict from support/readiness propagation.
- Distinguished well-formed, evaluated, and claim-admissible transfers.
- Corrected persistence certification and boundary-screening language.
- Hardened F8, complete-set manifest verification, Markdown rendering, and CI.
- Added version/DOI provenance and a transparent post-release audit.

## Highest-leverage next work

1. **External adversarial reading**
   - Seek prior-art equivalence, type errors, failed hypotheses, and fixture
     counterexamples from field-specific readers.
   - Record corrections and demotions publicly.

2. **Small machine-checked kernel**
   - Formalize one bounded object first: dependency-DAG demotion, the binary
     deficiency fixture, or the parity-gluing obstruction.
   - Pin the proof-assistant environment and retain accepted proof objects.

3. **Executable fixtures F1–F7**
   - Implement each fixture independently.
   - Require deterministic inputs, expected outputs, failure behavior, hashes,
     and receipts.
   - Do not call the set a reference implementation until the general transfer
     record and its gates are implemented.

4. **BSC-specific decoration functor**
   - Construct the actual lax symmetric monoidal decoration functor for one
     fixed mode and clock.
   - Prove functorial pushout transport and coherence. The generic
     decorated-cospan theorem does not discharge this obligation.

5. **Domain-specific scientific tests**
   - Choose one real transfer with public data and a nearby invalid control.
   - Determine whether the BSC record changes an inspectable scientific
     decision.

## Promotion rule

Completing one item promotes only the claims that explicitly depend on it.
Software execution does not promote empirical status; a formal proof does not
establish physical adequacy; a citation does not discharge a missing bridge.
