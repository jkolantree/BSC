# F10: coupled-surrogate host dependence

This executable fixture proves one bounded computational claim:

> The same exact standalone surrogate interface error stays within the
> declared host-state tolerance in one stable host and produces an exact
> tolerance violation in another stable host.

The reference component emits $z_k=0$, while the surrogate emits
$\widehat z_k=1/100$. For each host,

$$
e_{k+1}=a e_k+\left|\widehat z_k-z_k\right|,
\qquad e_0=0.
$$

The canonical input binds both the initial reference state $x_0=0$ and the
initial surrogate state $\widehat x_0=0$. The initial error is therefore
derived as $e_0=|\widehat x_0-x_0|=0$. The horizon is 10 steps and the
host-state tolerance is $1/20$.

| Host | $a$ | Exact step-10 error | First violation | Tolerance disposition |
|---|---:|---:|---:|---|
| `HOST-A` | $1/2$ | $1023/51200$ | none | within tolerance |
| `HOST-B` | $9/10$ | $6513215599/100000000000$ | 7 | tolerance violated |

Both hosts satisfy $|a|<1$. The `HOST-B` result is an exact actual
violation, not merely an upper enclosure above tolerance.

## Files

- `input.json` is the canonical fixture specification.
- `verify_coupled_surrogate.py` computes a deterministic receipt with
  `fractions.Fraction`.
- `check_fixture.py` independently validates the schema, identities, exact
  state paths, tolerance dispositions, and byte-for-byte regeneration.
- `receipt.schema.json` is the receipt contract.
- `verification_receipt.json` is the retained deterministic receipt.

The receipt binds stable claim identifier `BSC-FIX-10`, both exact initial
states, their derived initial error, every exact reference and surrogate
host-state path, and a five-factor
`evidence_identity`:

- candidate: reference, surrogate, recurrence, both initial states, and both
  hosts;
- data: typed `not_applicable`, because this exact fixture uses no training,
  calibration, validation, or empirical data;
- analysis: generator, checker, schema, and serialization identity;
- environment: the declared CPython exact-arithmetic runtime; and
- contract: claim, fixture, and canonical-input identity.

The receipt deliberately does not hash itself. The release manifest must bind
its bytes externally in `MANIFEST.sha256`, avoiding recursive self-hash
semantics.

From the repository root, run:

```text
python3 fixtures/F10_coupled_surrogate/check_fixture.py
```

This is code-verification evidence for the declared finite recurrence only.
It is one loss-coordinate tolerance disposition, not full BSC
claim-relative admissibility, physical validation, a general surrogate
guarantee, or evidence about the Riemann hypothesis or a quantum
implementation.
