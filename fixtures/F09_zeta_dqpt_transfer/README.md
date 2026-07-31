# F09: finite Riemann--DQPT accumulated-phase identity

## Status

- **Claim:** BSC-ZDQ-01.
- **Kind:** exact documentary fixture.
- **Computational readiness:** unexecuted.
- **Empirical readiness:** N/A.
- **Receipt:** none.

This directory specifies an exact finite arithmetic check for the identity

$$
  L_N(\beta_{\mathrm{eff}},t)
  =-\frac{S_N(\beta_{\mathrm{eff}}+it)}
          {Z_N(\beta_{\mathrm{eff}})}.
$$

Here $S_N=\eta_N=\sum_{n=1}^N(-1)^{n-1}n^{-s}$.
It does not claim to reproduce the Nature Communications experiment, locate a
Riemann zero, exhibit a DQPT, or verify RH.

It exercises BSC-ZDQ-01 only. The core framework proves the general
normalized-scale, decision, and analytic-transfer theorems, while the
surrounding application proves their eta/zeta-specific hypotheses. These JSON
files execute neither layer: they do not execute the fixed $s$ scaling limit,
the real-time slice, a contour census, or a stochastic decision test. In
particular, the fixture supplies no evidence for the comparator-local resource
claim BSC-ZDQ-06.

## Input

[`input.json`](input.json) declares

$$
  N=4,\qquad\beta_{\mathrm{eff}}=1,\qquad t=0,
$$

with the source phase convention

$$
  (-1)^n=(-1,+1,-1,+1).
$$

At $t=0$, all evolution factors are $1$, so every expected result is a
rational number. No floating-point approximation or convention for
$\log(1)$ is needed.

## Expected exact derivation

The partition function is

$$
  Z_4(1)=1+\frac12+\frac13+\frac14=\frac{25}{12}.
$$

The truncated eta value $S_4=\eta_4$ is

$$
  \eta_4(1)=1-\frac12+\frac13-\frac14=\frac{7}{12}.
$$

The source-convention signed numerator is

$$
  -1+\frac12-\frac13+\frac14=-\frac{7}{12}
  =-\eta_4(1).
$$

Therefore

$$
  L_4(1,0)
  =\frac{-7/12}{25/12}
  =-\frac{7}{25}.
$$

[`expected_output.json`](expected_output.json) records those reduced
fractions as numerator/denominator pairs.

## Nearby invalid control

The input also declares a negative control in which only the fourth phase is
flipped:

$$
  (-1,+1,-1,-1).
$$

Its signed numerator and normalized coherence are

$$
  -1+\frac12-\frac13-\frac14=-\frac{13}{12},
  \qquad L_{\rm control}=-\frac{13}{25}.
$$

This differs from $-7/25$ by $6/25$ in absolute value. Any future checker
must reject the control as an implementation of BSC-ZDQ-01 even though it is
internally arithmetically consistent.

## Future checker contract

A future exact checker may promote the fixture from `unexecuted` only if it:

1. parses the input and expected output without binary floating-point;
2. constructs all fractions from integer numerator/denominator pairs;
3. verifies denominators are positive and fractions are reduced;
4. recomputes $Z_4$, $\eta_4$, the signed numerator, and $L_4$;
5. verifies $Z_4L_4=-\eta_4$;
6. runs the one-phase-flip control and confirms the identity gate rejects it;
7. writes a deterministic receipt containing tool version, command, input and
   output hashes, checks performed, and final status; and
8. is itself checked with at least one semantic mutant.

Until such code is executed and its receipt retained, the permanent status is
`unexecuted`. Merely copying the values in `expected_output.json` is not an
execution.

## Source and scope

- Primary publication:
  [Wei et al., *Nature Communications* (2026)](https://doi.org/10.1038/s41467-026-74935-8).
- Version-pinned primary manuscript:
  [arXiv:2511.11199v1](https://arxiv.org/abs/2511.11199v1).
- BSC application record:
  [`applications/Riemann_DQPT_Transfer.md`](../../applications/Riemann_DQPT_Transfer.md).
- Reusable BSC framework:
  [`framework/Normalized_Scale_Profiles.md`](../../framework/Normalized_Scale_Profiles.md).
