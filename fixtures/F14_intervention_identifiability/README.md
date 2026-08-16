# F14 — finite intervention identifiability

F14 is a small exact witness for BSC's proposed intervention-identifiability
layer. It asks which declared measurements are sufficient to recover a target
on four finite states, and which sufficient family has minimum declared cost.

The fixture is intentionally transparent:

- `column` reports one state bit and costs 1;
- `row` reports the other bit and costs 1;
- `direct` reports the full state and costs 2;
- the target takes four distinct values;
- all costs, finite-metric distances, and tolerances are reduced rationals.

The exact optimum is 2. There are two minimum-cost identifying families:
`[direct]` and `[column, row]`. The deterministic selection rule chooses
`[direct]` because it has smaller cardinality. This selection is a reporting
tie-break; it does not erase the second optimizer.

## Files

- `input.json` is the canonical closed input.
- `expected_report.json` is the retained source-bound result.
- `check_fixture.py` performs a same-implementation replay and byte comparison;
  it is not an independent verifier.
- `../../tools/bsc_intervention_design.py` is the stdlib-only exact checker.
- `../../tests/test_bsc_intervention_design.py` supplies positive, mutation,
  malformed-input, metric, coverage, and deterministic-output tests.

## Exact checks

For every one of the eight intervention families, one checker cross-checks two
separately coded criteria:

1. the target is constant on each fiber of the joint report;
2. the chosen reports cover every target-separated state pair.

The general checker rejects inputs above fixed ceilings: 2,000,000 input
bytes, JSON depth 32, 200,000 JSON items, 256 states, 16 interventions, 32
points per metric, 256 oscillation queries, 1,000,000 metric-validation
operations, 10,000,000 exhaustive-family operations, 4,096 reported
minimizers, 4,000,000 report bytes, 18 decimal digits per JSON integer, and
1,000,000,000,000 in absolute rational components. Failures are typed and
sent to standard error without echoing local paths.

It also computes, from the declared finite metrics and tolerances,

$$
\omega_q(J,\varepsilon)
=\max\lbrace d_Z(q(x),q(x')):
d_i(r_i(x),r_i(x'))\leq\varepsilon_i\ \forall i\in J\rbrace.
$$

For example, the empty family has oscillation `7/2`, while the exact
`[column, row]` design has oscillation 0. The tolerant `direct` report has
oscillation `3/2` even though it is exactly injective; this separates exact
identifiability from tolerance-robust identifiability.

## Replay

From the repository root, use the configured Python 3 interpreter:

```text
python fixtures/F14_intervention_identifiability/check_fixture.py
python -m unittest tests.test_bsc_intervention_design
```

## Authority boundary

The retained report establishes exact conclusions only for the finite deterministic
model encoded in `input.json`. It does not show that the model is causally
valid, empirically adequate, stochastic, continuous, externally identifiable,
novel, or representative of a scientific domain. SHA-256 values bind bytes;
they do not confer semantic truth or priority, and a public hash is not a
confidentiality control for guessable private material.
