# Exact-rational Lorentz auxiliary-state passivity

## Status and authority

This post-v1.4.0 note is an independent reconstruction under roadmap item 9.
It allocates `BSC-EM-12` without modifying the immutable v1.4.0 paper or the
released `BSC-EM-01` through `BSC-EM-11` roster.

The theorem below is an analytic scalar identity for differentiable
real-valued fields. Fixture F13 checks its denominator-cleared algebra over
$\mathbb Q$ and four finite exact energy ledgers. Exact rational fixture
arithmetic is not a claim that a nonconstant physical trajectory is
$\mathbb Q$-valued, a Maxwell PDE execution, a material calibration, a
historical replay, or a trusted-kernel proof.

## 1. Declared model

Work on a fixed spatial region with enough regularity for the local Poynting
identity and, when the integrated form is used, the divergence theorem. The
result is scalar, local, and isotropic. Tensor coefficients, multiple poles,
spatial nonlocality, nonlinear response, magnetic dispersion, moving
boundaries, and distributional coefficient jumps require separate theorems.

Let $P$ be one polarization coordinate, let $V=\dot P$, and let $E$ be the
electric-field component paired with that polarization. For fixed real
parameters

```math
a=\varepsilon_0\omega_p^2>0,
\qquad
b=\omega_0^2>0,
\qquad
\gamma\ge 0,
```

assume

```math
\dot P=V,
\qquad
\dot V=aE-\gamma V-bP.
```

The symbol $a$ is a local oscillator coefficient, not a BSC scale label, and
$b$ is not a scattering amplitude. The rational examples below are normalized
algebraic ledgers; no SI parameter bridge is supplied.

The background electromagnetic storage $u_{\mathrm{EM}}$ must exclude the
polarization storage introduced below. Equivalently, if
$D=D_{\mathrm b}+P$, the background field law belongs to $D_{\mathrm b}$ and
the polarization current $V$ remains explicit. The declared Maxwell balance
is

```math
\partial_tu_{\mathrm{EM}}+\nabla\mkern3mu\cdot S
=-EJ_{\mathrm{free}}-EV.
```

Using total $D$ inside an instantaneous field-energy formula and then adding
the auxiliary storage again would double count polarization energy.

## 2. Fixed-parameter storage theorem

### Theorem 2.1 (BSC-EM-12)

Under the declared fixed-parameter hypotheses, define

```math
W(P,V)=\frac{V^2+bP^2}{2a},
\qquad
D_{\mathrm{loss}}=\frac{\gamma V^2}{a}.
```

Then $W$ is positive definite in $(P,V)$ and

```math
\dot W=EV-\frac{\gamma V^2}{a}.
```

Together with the declared Maxwell balance,

```math
\partial_t(u_{\mathrm{EM}}+W)+\nabla\mkern3mu\cdot S
=-EJ_{\mathrm{free}}-\frac{\gamma V^2}{a}.
```

#### Proof

Direct differentiation and the two state equations give

```math
\begin{aligned}
\dot W
&=\frac{V\dot V+bP\dot P}{a}\\
&=\frac{V(aE-\gamma V-bP)+bPV}{a}\\
&=EV-\frac{\gamma V^2}{a}.
\end{aligned}
```

The coefficients of $V^2$ and $P^2$ in $W$ are positive because $a,b>0$.
Adding the material identity to the Maxwell premise cancels the internal
exchange $EV$ and gives the coupled identity. $\square$

The corresponding material-port inequality is

```math
W(t_1)-W(t_0)
=\int_{t_0}^{t_1}EV\,dt
-\int_{t_0}^{t_1}\frac{\gamma V^2}{a}\,dt
\le\int_{t_0}^{t_1}EV\,dt.
```

For $\gamma=0$ the material channel is lossless. For $\gamma>0$ it is in a
dissipative parameter regime, but the instantaneous loss still vanishes at
$V=0$; no strict pointwise decay is claimed. For $\gamma<0$, zero-input
antidamping can increase $W$, so that regime is not passive.

## 3. Integrated energy and port orientation

For a fixed region $\Omega$ with outward unit normal $n$, define the typed
integrated quantities

```math
U_{\mathrm{total}}
=\int_\Omega(u_{\mathrm{EM}}+W)\,dx,
\qquad
P_{\mathrm{free}}=\int_\Omega EJ_{\mathrm{free}}\,dx,
\qquad
D_{\mathrm{loss},\Omega}
=\int_\Omega\frac{\gamma V^2}{a}\,dx.
```

Then

```math
\frac d{dt}\int_\Omega(u_{\mathrm{EM}}+W)\,dx
+\int_{\partial\Omega}S\mathbin{\cdot}n\,dA
=-\int_\Omega EJ_{\mathrm{free}}\,dx
-\int_\Omega\frac{\gamma V^2}{a}\,dx.
```

Outward flux is positive in this convention. If

```math
p_{\mathrm{in}}
=-\int_{\partial\Omega}S\mathbin{\cdot}n\,dA,
```

then

```math
\dot U_{\mathrm{total}}
=p_{\mathrm{in}}-P_{\mathrm{free}}-D_{\mathrm{loss},\Omega}.
```

Positive $EJ_{\mathrm{free}}$ is work by the field on the declared free
current. It need not be irreversible loss: a negative value represents
source injection. Pointwise balance, volume integration, boundary flux, and
inward port power remain separate typed statements.

## 4. Time-varying coefficients and pump accounting

If differentiable $a(t)>0$ or $b(t)>0$ varies while the same oscillator
equation is retained, then

```math
q_{\mathrm{pump}}
=\frac{\dot b\,P^2}{2a}
-\frac{\dot a\,(V^2+bP^2)}{2a^2}
```

and

```math
\dot W
=EV-\frac{\gamma V^2}{a}+q_{\mathrm{pump}}.
```

Thus

```math
\partial_t(u_{\mathrm{EM}}+W)+\nabla\mkern3mu\cdot S
=-EJ_{\mathrm{free}}
-\frac{\gamma V^2}{a}
+q_{\mathrm{pump}}.
```

The pump term is signed exchange. A positive value supplies energy and a
negative value extracts it. It appears with a plus sign on the right-hand
side above; moving it to the left reverses the sign. Including the pump gives
a dissipation inequality with augmented supply $EV+q_{\mathrm{pump}}$.
Passivity relative to $EV$ alone requires an additional pointwise or
integrated bound, such as $q_{\mathrm{pump}}\le0$; recording the pump term
alone is insufficient.
Even when one sampled state makes the numerical pump value zero, time-varying
coefficients still require the structural pump term.

For the fixed-domain integrated form, set

```math
Q_{\mathrm{pump},\Omega}=\int_\Omega q_{\mathrm{pump}}\,dx.
```

The corresponding port balance is

```math
\dot U_{\mathrm{total}}
=p_{\mathrm{in}}-P_{\mathrm{free}}-D_{\mathrm{loss},\Omega}
+Q_{\mathrm{pump},\Omega}.
```

The formula assumes classical differentiability. Jumps require
distributional or interface bookkeeping. It is conditional on the displayed
time-dependent oscillator equation and is not a universal microscopic law.

## 5. Exact certificate factorization

The F13 checker works in the sparse polynomial ring

```math
\mathbb Q[
a,b,\gamma,\dot a,\dot b,P,V,E,J_{\mathrm{free}},
\dot u_{\mathrm{EM}},\nabla\mkern3mu\cdot S
].
```

For fixed coefficients it clears the positive denominator $a$. For varying
coefficients it clears $2a^2$. The scaled pump numerator is

```math
a\dot bP^2-\dot a(V^2+bP^2).
```

After substituting $\dot P=V$, $\dot V=aE-\gamma V-bP$, and the declared
Maxwell premise, the material and coupled residuals cancel coefficient by
coefficient. No time samples or floating-point tolerances are used.

The factorization keeps three obligations visible:

```math
\begin{aligned}
M&=\partial_tu_{\mathrm{EM}}+\nabla\mkern3mu\cdot S
   +EJ_{\mathrm{free}}+EV,\\
L&=\dot W-EV+\frac{\gamma V^2}{a}-q_{\mathrm{pump}},\\
T&=\partial_tu_{\mathrm{EM}}+\dot W+\nabla\mkern3mu\cdot S
   +EJ_{\mathrm{free}}+\frac{\gamma V^2}{a}-q_{\mathrm{pump}},
\end{aligned}
```

with $T=M+L$. This exposes a polarization-current sign error instead of
hiding it inside the total residual.

## 6. Fixture F13 and evidence boundary

`F13-LORENTZ-AUXILIARY-PASSIVITY` retains four exact ledgers:

1. a fixed dissipative case;
2. a fixed lossless case with a nontrivial inward/outward port conversion;
3. a $\dot b$-only pump case; and
4. a $\dot a$-only pump case.

Separate modulation cases prevent the two pump terms from accidentally
cancelling. The receipt binds the input, this framework note, generator,
independent checker, schema, and provenance bytes. It contains no commit or
tree hash and is outside every released fixture record.

Each finite ledger declares a spatially uniform normalized cell: its supplied
$a,b,\gamma,\dot a,\dot b,P,V,E,$ and $J_{\mathrm{free}}$ values are constant
density representatives on a cell of the stated rational measure. This is why
the fixture may multiply pointwise densities by that measure. It is a fixture
convention only, not a claim about arbitrary spatial profiles or averages.
The finite checker also differentiates $W$ directly through $P,V,a,b$ and
compares that chain-rule rate with the balance-side rate.

The fixture is `independent_reconstruction` evidence and remains
`NOT_REPLAYED`, not mechanically replayed and not kernel verified. It proves
no Maxwell existence or regularity theorem, causal completeness for a general
dispersive medium, calibrated physical energy, device efficiency, switching
or memory performance, empirical validation, novelty, or priority.

No external paper, data set, script, figure, table, or historical receipt is
an input to this construction.
