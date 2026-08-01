# F13: Lorentz auxiliary-state passivity over Q

## Identity

- mathematical claim: `BSC-EM-12`;
- fixture-ledger claim: `BSC-FIX-13`;
- runtime fixture: `F13-LORENTZ-AUXILIARY-PASSIVITY`;
- evidence status: `independent_reconstruction`;
- historical replay: `NOT_REPLAYED`.

This is a post-v1.4.0 development fixture. It does not modify the immutable
v1.4.0 paper, its `BSC-EM-01` through `BSC-EM-11` roster, or its eleven-fixture
release record.

## Contract

The retained input uses reduced rational pairs only. The generator checks
$a>0$, $b>0$, $\gamma\ge0$, the fixed/lossless/dissipative classification,
the full coefficient-modulation pump term, a direct chain-rule storage rate
against the balance-side rate, pointwise material arithmetic, the integrated
Maxwell ledger, and both outward-flux and inward-port forms.

Every retained case uses the locked profile convention
`uniform_normalized_cell`: the supplied scalar fields and coefficients are
constant density representatives on a cell with the declared rational spatial
measure. Multiplication by that measure is not asserted for arbitrary profiles
or for separately averaged products.

The checker independently reconstructs the same obligations without importing
the generator. It also verifies denominator-cleared sparse-polynomial
cancellation over $\mathbb Q$ for the fixed and time-varying identities. No
time samples or numerical tolerances are used.

Run:

```bash
python3 fixtures/F13_lorentz_auxiliary_passivity/check_fixture.py
```

Expected terminal line:

```text
F13-LORENTZ-AUXILIARY-PASSIVITY: PASS: 4 exact ledgers
```

The checker regenerates the receipt twice in temporary directories, requires
byte-identical canonical JSON, and confirms that the generator refuses to
overwrite a retained output.

## Retained cases

- `fixed_dissipative`: positive storage with $\gamma=1$ and exact damping;
- `fixed_lossless`: $\gamma=0$ with a nontrivial port-orientation check;
- `varying_b_pump`: isolates the $\dot bP^2/(2a)$ contribution; and
- `varying_a_pump`: isolates the
  $-\dot a(V^2+bP^2)/(2a^2)$ contribution.

The rational ledgers are finite algebraic witnesses, not Maxwell PDE
solutions. The analytic theorem remains conditional on differentiability,
the declared background-field balance, fixed-domain regularity, and the
stated scalar oscillator model.

## Provenance boundary

No external paper, data, code, figure, or historical receipt is an input.
The fixture is not mechanically replayed or kernel verified and supplies no
absolute-energy, device-efficiency, switching, memory, empirical, novelty, or
priority authority.
