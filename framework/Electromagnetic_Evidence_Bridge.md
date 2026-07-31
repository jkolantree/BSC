# On Electromagnetism: an operational evidence bridge

## Status and scope

This is a development module for version `1.3.0-dev`. The latest immutable
release remains v1.2.0.

The purpose of this module is to supply the electromagnetic completion that
the operational-channel core deliberately left open. It separates six layers:

$$
\text{bundle and gauge}
\longrightarrow
\text{field equations}
\longrightarrow
\text{constitutive response}
\longrightarrow
\text{boundary ports}
\longrightarrow
\text{instrument report}
\longrightarrow
\text{inference}.
$$

The common language does not make every electromagnetic system microscopically
identical. Vacuum electrodynamics, a dispersive material, a waveguide, an
atomic spectrum, and a quantum interference experiment can share a typed
evidence route while having different state spaces, controls, material laws,
and measurement maps.

Maxwell equations, gauge theory, Poynting balance, passive scattering,
electromagnetic inverse problems, quantum holonomy, and precision metrology
are prior art. The BSC contribution here is narrower: a joint record of which
layer licenses a claim, exact descent and nonidentifiability tests, and
claim-local demotion when a required bridge is absent.

This module does **not** derive the fine-structure constant, quantize the full
electromagnetic field, prove an unknown material model, or establish a
unified field theory.

## 1. Typed electromagnetic completions

### Definition 1.1 (Electromagnetic completion)

An electromagnetic completion of an operational report envelope is a record

$$
\mathsf{EMC}
=
\left(
M,g,P,[\mathcal A],\mathcal F,\mathcal H,\mathcal J,
\mathcal C,\mathcal B,\mathcal M,\mathcal R,
\mathsf{Cert}_{\mathrm{EM}}
\right).
$$

Its coordinates are:

1. an oriented, time-oriented spacetime region $(M,g)$, or a declared
   nonrelativistic spacetime slab;
2. a principal $U(1)$ bundle $P\to M$;
3. a connection $\mathcal A$ modulo its declared gauge group and curvature
   $\mathcal F$;
4. an excitation two-form $\mathcal H$ and electric-current three-form
   $\mathcal J$;
5. a constitutive record $\mathcal C$ relating $\mathcal H$ to $\mathcal F$
   and any material state;
6. initial, boundary, interface, and port data $\mathcal B$;
7. an instrument map $\mathcal M$ and report map $\mathcal R$; and
8. a certificate binding domains, regularity, units, conventions, sources,
   calibration, uncertainty, proof or execution identity, and open
   obligations.

In local connection coordinates the Maxwell equations are

$$
d\mathcal F=0,
\qquad
d\mathcal H=\mathcal J.
$$

The first equation is geometric. The second is sourced. Neither equation
selects a constitutive law. In vacuum one may have a convention-dependent
multiple of

$$
\mathcal H=\star_g\mathcal F,
$$

whereas a material may require a tensorial, nonlinear, history-dependent,
spatially nonlocal, or temporally dispersive map

$$
\mathcal H(t)
=
\mathcal C\!\left[
\{\mathcal F(s):s\le t\},
\xi(t)
\right].
$$

Here $\xi$ is a declared material state. Suppressing $\xi$ or the history
while invoking a memoryless material theorem is a type error.

The terminal electromagnetic report law is

$$
P_\theta^Z
=
\mathcal R_\#
\mathcal M_\#
\operatorname{Sol}_{\mathsf{EMC}}
\bigl(\mathsf{Prep}(\theta),\mathsf{Control}(\theta)\bigr).
$$

This map, not a diagram of field lines by itself, is the object that enters
the operational report envelope.

## 2. Gauge descent and global observables

Let $\mathscr A(P)$ be the space of admissible connections and
$\mathscr G(P)$ the declared gauge group.

### Proposition 2.1 (Gauge-descent criterion)

A deterministic report

$$
R:\mathscr A(P)\longrightarrow Z
$$

defines a physical report on gauge classes if and only if it is constant on
gauge orbits:

$$
R(A^u)=R(A)
\qquad
\text{for every admissible }A\text{ and }u\in\mathscr G(P).
$$

Equivalently, there is a unique map

$$
\overline R:\mathscr A(P)/\mathscr G(P)\longrightarrow Z
$$

such that $R=\overline R\circ\pi$, where $\pi$ is the quotient map.

#### Proof

If $R=\overline R\circ\pi$, gauge-related connections have the same quotient
class and therefore the same report. Conversely, orbit constancy makes
$\overline R([A])=R(A)$ independent of the representative. Uniqueness follows
from surjectivity of $\pi$. $\square$

This is BSC-EM-01. A gauge condition can select a computational
representative, but a representative-dependent number does not become a
physical observable merely because the gauge was convenient.

Curvature and closed-loop holonomy are gauge invariant:

$$
\mathcal F_A
\longmapsto
\mathcal F_A,
\qquad
\operatorname{Hol}_\gamma(A)
=
\exp\!\left(i\oint_\gamma A\right)
\quad
\text{for closed }\gamma.
$$

An open-path phase is not gauge invariant without endpoint matter states or
another compensating boundary record.

For a global base-space potential $A$, the curvature $F=dA$ is exact.
Conversely, a closed two-form has some global one-form potential exactly when
its de Rham class vanishes. For a $U(1)$ bundle, the real cohomology class
$[F/(2\pi)]$ is the image of its first Chern class (in the dimensionless
connection convention). A nonzero class therefore forbids a single global
potential, and a torsion bundle can retain global information invisible to
de Rham curvature. Patchwise potentials and transition functions are then
part of the completion rather than optional notation.

### Proposition 2.2 (Curvature does not determine global holonomy)

If

$$
H^1(M;\mathbb R)/(2\pi H^1(M;\mathbb Z))
$$

is nontrivial, there are gauge-inequivalent $U(1)$ connections with the same
curvature and different closed-loop holonomy.

#### Proof

Choose a closed one-form $h$ whose period class is not in
$2\pi H^1(M;\mathbb Z)$. Then $A$ and $A+h$ have the same curvature because
$dh=0$. They are not related by a single-valued $U(1)$ gauge transformation,
and some closed loop $\gamma$ satisfies

$$
\exp\!\left(i\oint_\gamma(A+h)\right)
\ne
\exp\!\left(i\oint_\gamma A\right).
$$

For the explicit cylinder factor $M=S^1\times N$, the flat connections
$A_\vartheta=\vartheta\,d\phi$ all have zero curvature, while their holonomy
around $S^1$ is $\exp(2\pi i\vartheta)$; only integer shifts of $\vartheta$
are gauge equivalent. $\square$

This is BSC-EM-02. A local field-strength report can therefore be complete for
one classical target and incomplete for a quantum phase or global-topology
target. The Aharonov--Bohm effect is a physical instance of this distinction,
not a license to treat a gauge-dependent local potential value as an
observable.

## 3. Sources, conservation, and flux

### Proposition 3.1 (Source compatibility)

Every smooth solution of

$$
d\mathcal H=\mathcal J
$$

satisfies

$$
d\mathcal J=0.
$$

If $\mathcal H$ is a global smooth two-form, then $\mathcal J$ is exact, so
$[\mathcal J]=0$ in de Rham cohomology. A proposed smooth global source with
$d\mathcal J\ne0$, or with a nonzero cohomology class incompatible with the
declared domain and boundary model, admits no such global solution.

#### Proof

Apply $d$ and use $d^2=0$. Exactness follows directly from
$\mathcal J=d\mathcal H$. $\square$

This is BSC-EM-03. Singular sources, excised world lines, interfaces, and open
boundaries require the corresponding distributional or relative-cohomology
version; they may not be hidden inside a smooth theorem.

In an oriented $3+1$ split, write the spatial charge and current forms as
$\rho$ and $j$. The same equation becomes

$$
\partial_t\rho+d_\Omega j=0,
$$

and every fixed spatial region $V$ obeys

$$
\frac d{dt}\int_V\rho
=
-\int_{\partial V}j.
$$

For every admissible three-chain $V$, Stokes' theorem gives

$$
\int_{\partial V}\mathcal H
=
\int_V\mathcal J.
$$

This is a typed Gauss-law bridge from a declared boundary flux to the enclosed
charge represented by $\mathcal J$. It does not reconstruct the interior
current density from one scalar flux.

### Proposition 3.2 (Total-flux nonidentifiability)

Let the report be only

$$
R(\mathcal J)=\int_V\mathcal J.
$$

Any two admissible current forms with equal integrals give the same report.
Consequently, an interior source property $q(\mathcal J)$ descends from this
report only if it is constant on every equal-total-flux fiber.

#### Proof

Equality of the two integrals is exactly equality of the reports. The descent
condition is Proposition 6.4 of the main paper applied to this report map.
$\square$

The statement is intentionally report-local. A complete, calibrated
boundary-response operator can contain much more information than a total
flux.

### Proposition 3.3 (Local source-free laws do not select a flux sector)

Let

$$
\Omega=\{x\in\mathbb R^3:a<|x|<b\}.
$$

For every $q\in\mathbb R$, the static field

$$
E_q=0,
\qquad
B_q=\frac{q}{4\pi|x|^3}x,
\qquad
H_q=\mu^{-1}B_q
$$

satisfies the source-free local Maxwell equations on $\Omega$, while

$$
\int_{S_r^2}B_q\mathbin{\cdot}n\,dA=q
\qquad
(a<r<b).
$$

For $q\ne0$, the associated magnetic two-form is closed but not exact on the
shell. Moreover, every member has zero tangential electric trace and zero
tangential magnetic trace at the spherical boundaries, even though the normal
flux sectors differ.

#### Proof

Direct differentiation gives
$\nabla\mathbin{\cdot}B_q=0$ and
$\nabla\times H_q=0$ on the shell. The flux integral is elementary. If the
magnetic two-form were exact, Stokes' theorem would make its integral over
every closed two-cycle vanish. Radial $H_q$ and zero $E_q$ have the stated
tangential traces. $\square$

Thus local source-free equations and a tangential power-port report do not
determine a normal topological-flux sector. This sharpens BSC-EM-02 and
BSC-EM-03 without introducing magnetic monopole evidence inside the excised
domain.

## 4. Energy and boundary power

Consider a fixed bounded spatial region $\Omega\subset\mathbb R^3$. Let the
fields be regular enough for the following integrations by parts, and suppose

$$
\nabla\times H=J+\partial_tD,
\qquad
\nabla\times E=-\partial_tB,
\qquad
D=\varepsilon E,
\qquad
B=\mu H,
$$

where $\varepsilon$ and $\mu$ are time-independent, symmetric, and positive.

### Theorem 4.1 (Electromagnetic energy balance)

With

$$
u
=
\frac12(E\mathbin{\cdot}D+H\mathbin{\cdot}B),
\qquad
S=E\times H,
$$

one has

$$
\partial_tu+\nabla\mathbin{\cdot}S=-J\mathbin{\cdot}E
$$

and therefore

$$
\frac{d}{dt}\int_\Omega u\,dx
=
-\int_{\partial\Omega}S\mathbin{\cdot}n\,dA
-\int_\Omega J\mathbin{\cdot}E\,dx.
$$

#### Proof

Use

$$
\nabla\mathbin{\cdot}(E\times H)
=
H\mathbin{\cdot}(\nabla\times E)
-E\mathbin{\cdot}(\nabla\times H)
$$

and substitute Maxwell's equations. Symmetry and time independence of
$\varepsilon,\mu$ identify the two field terms with $\partial_tu$. Integrate
and apply the divergence theorem. $\square$

This is BSC-EM-04. The boundary term is delivered electromagnetic power, not
a decorative edge variable. The volume term is work on the declared current.
The signs reverse if a different outward-power convention is adopted, and
that convention belongs in the certificate.

If $\varepsilon(t)$ or $\mu(t)$ is externally modulated, the same calculation
using the instantaneous expression for $u$ gives

$$
\partial_tu+\nabla\mathbin{\cdot}S
=
-J\mathbin{\cdot}E
-\frac12E\mathbin{\cdot}\dot\varepsilon E
-\frac12H\mathbin{\cdot}\dot\mu H.
$$

The last two terms are exchange with the modulated material or pump. Omitting
them can manufacture apparent gain. For temporally dispersive media,
$D(t)$ and $B(t)$ depend on field history; a positive instantaneous quadratic
$u$ is not automatic. A material-state realization, passivity theorem, or
other stored-energy construction is then required.

## 5. Calibrated ports and scattering reports

Let $a(\omega)$ and $b(\omega)$ be incident and outgoing mode amplitudes at a
declared frequency, port basis, reference plane, and normalization:

$$
b(\omega)=S(\omega)a(\omega).
$$

### Proposition 5.1 (Passive port contraction)

If the amplitudes are power normalized, all relevant propagating ports are
included, and the linear time-invariant device is passive with no unreported
initial stored-energy release, then

$$
\lVert S(\omega)a\rVert_2^2
\le
\lVert a\rVert_2^2
\qquad
\text{for every }a.
$$

Equivalently,

$$
S(\omega)^\dagger S(\omega)\preceq I.
$$

Equality requires losslessness at that frequency and a complete port
accounting. With a non-Euclidean power metric $W\succ0$, the correct statement
is

$$
S^\dagger W S\preceq W,
$$

not an unqualified Euclidean norm inequality.

#### Proof

Passivity says outgoing time-averaged port power cannot exceed incident
power. Under power normalization these are the two squared norms. The
quadratic inequality for every $a$ is equivalent to
$I-S^\dagger S\succeq0$. The weighted statement is identical in the
$W$-metric. $\square$

This is BSC-EM-05. Reference impedance, mode normalization, de-embedding,
frequency, bandwidth, dynamic range, calibration standards, uncertainty, and
hidden radiation or material-loss ports are part of the report identity.

If a complete lossless scattering operator is partitioned into observed and
hidden ports,

$$
U=
\begin{pmatrix}
S_{oo}&S_{oh}\\
S_{ho}&S_{hh}
\end{pmatrix},
\qquad
U^\dagger U=I,
$$

then the observed-input block satisfies

$$
I-S_{oo}^\dagger S_{oo}=S_{ho}^\dagger S_{ho}.
$$

An observed power deficit therefore proves only transfer out of the retained
output ports. It does not by itself distinguish absorption, radiation,
higher modes, termination loss, or another hidden channel.

Suppose a simultaneous calibration certificate gives

$$
\lVert\widehat S-S\rVert_2\le\varepsilon.
$$

Singular-value perturbation yields

$$
\left|
\sigma_{\max}(\widehat S)-\sigma_{\max}(S)
\right|
\le\varepsilon.
$$

Consequently:

1. if $\sigma_{\max}(\widehat S)-\varepsilon>1$, the declared passive
   closed-port model is falsified;
2. if $\sigma_{\max}(\widehat S)+\varepsilon\le1$, contractivity is certified
   on the declared configuration and band; and
3. otherwise the passivity disposition is inconclusive.

For every incident amplitude,

$$
\left|
\lVert\widehat Sa\rVert_2^2-\lVert Sa\rVert_2^2
\right|
\le
\left(2\lVert S\rVert_2\varepsilon+\varepsilon^2\right)
\lVert a\rVert_2^2.
$$

Under the passive model this is at most
$(2\varepsilon+\varepsilon^2)\lVert a\rVert_2^2$. Pointwise error bars do not
automatically provide the simultaneous operator-norm event used here.

Reciprocity can additionally imply

$$
CS=(CS)^{\mathsf T},
$$

where $C$ is the modal orthogonality matrix. This reduces to $S=S^{\mathsf T}$
only for consistently paired, orthonormal, power-normalized modes with common
reference conventions. It requires a reciprocal linear medium and no
reciprocity-breaking bias, time modulation, or active control. Passivity does
not imply reciprocity.

### Proposition 5.2 (Power-only scattering does not identify phase)

Fix $0<r\le1$ and $\tau>0$. Under a fixed Fourier convention, the two causal
passive one-port responses

$$
S_0(\omega)=r,
\qquad
S_\tau(\omega)=r e^{-i\omega\tau}
$$

have the same power response at every frequency,

$$
|S_0(\omega)|^2=|S_\tau(\omega)|^2=r^2,
$$

but different phase, delay, and impulse response.

#### Proof

Multiplication by $e^{-i\omega\tau}$ is a pure delay in the stated Fourier
convention and does not change magnitude. The two responses differ whenever
$\omega\tau$ is not an integer multiple of $2\pi$. Attenuation by
$r\le1$ is passive. $\square$

This is BSC-EM-06. Magnitude-only spectra cannot license a phase, group-delay,
time-domain waveform, or coherent-interference claim without an additional
minimum-phase theorem or phase measurement. Finite-band complex data also
leave behavior outside the measured band unidentified.

Connected scattering systems generally compose through a Redheffer star
product, not ordinary matrix multiplication. Internal feedback introduces
factors such as

$$
\left(I-S_{22}^{A}S_{11}^{B}\right)^{-1}.
$$

The composite is undefined if the inverse does not exist and can be highly
sensitive near an internal resonance. Energy contractivity of the completed
passive channel does not supply a universal contraction constant for the map
from component S-parameter defects to the composite defect.

## 6. Boundary inversion is theorem local

For a fixed frequency and a declared coefficient class, a Maxwell boundary
operator may be written schematically as

$$
\Lambda_{\varepsilon,\mu}:
\operatorname{tr}_{\!t}E
\longmapsto
\operatorname{tr}_{\!t}H.
$$

For finite-energy fields on a Lipschitz domain, these tangential traces are
generally elements of the appropriate $H(\operatorname{curl})$ trace spaces
(commonly represented by $H^{-1/2}(\operatorname{div}_\Gamma,\Gamma)$ and
its paired companion), not pointwise boundary vectors. Boundary power is then
a continuous dual pairing. Replacing that pairing by an $L^2$ surface
integral requires the extra regularity that makes the replacement valid.

Its definition requires a well-posed forward problem, admissible frequency,
boundary spaces, coefficient regularity, geometry, gauge quotient, and a
choice of full or partial data. A measured finite-dimensional S-parameter
matrix is not automatically the full operator
$\Lambda_{\varepsilon,\mu}$.

Published uniqueness results determine material parameters from boundary
measurements in specific isotropic or anisotropic regimes. They do not imply

$$
\text{every finite-band boundary report}
\Longrightarrow
\text{every interior constitutive law}.
$$

That universal statement is false by the already retained finite-system
counterexamples and by the report restrictions above. This binds the existing
BSC-BND-03 row rather than replacing it.

Two exact obstructions show why the admissible class matters.

First, if that class permits a perfectly conducting closed shield surrounding
an interior subdomain $D\Subset\Omega$, fields driven and observed only at
the exterior boundary do not enter $D$. Two constitutive records that agree
on the accessible exterior but differ arbitrarily inside $D$ therefore have
the same exterior boundary operator. No improvement in exterior measurement
precision removes this noninjectivity; the target or coefficient class must
change.

Second, in anisotropic transformation-optics formulations, a
boundary-fixing diffeomorphism can push forward the material tensors while
leaving the boundary data invariant. The identified object is then an
equivalence class under that coordinate gauge, unless the theorem supplies
additional structure that fixes it. Neither obstruction says that all Maxwell
inverse problems are nonunique. They locate two exact quotients that a claimed
uniqueness theorem must exclude or retain.

A valid inverse promotion must identify:

1. the exact forward Maxwell problem;
2. the coefficient and geometry class;
3. the gauge or diffeomorphism quotient;
4. full versus partial boundary access;
5. frequency and time regime;
6. uniqueness and stability theorems;
7. instrument-to-boundary-map calibration; and
8. the target property that is constant on the resulting identified set.

## 7. Coupling normalization and topology

### Proposition 7.1 (Field normalization and invariant couplings)

In rationalized natural units, consider the local action family

$$
\mathcal S_{Z,\{q_i\}}[A,\{\psi_i\},J]
=
-\frac Z4\int F_{\mu\nu}F^{\mu\nu}\,dV
+\sum_i
\mathcal S_i\!\left[\psi_i,d+iq_iA\right]
-\int J^\mu A_\mu\,dV,
$$

with $Z>0$. For every $\lambda>0$, the coordinate change

$$
A'=\lambda A
$$

rewrites the same action with

$$
Z'=\frac{Z}{\lambda^2},
\qquad
q_i'=\frac {q_i}\lambda,
\qquad
J'=\frac J\lambda.
$$

Thus $Z$, the $q_i$, and the components of the external current separately
depend on field normalization, while

$$
\frac{q_i'}{\sqrt{Z'}}
=
\frac{q_i}{\sqrt Z},
\qquad
\frac{q_i'}{q_j'}
=
\frac{q_i}{q_j},
\qquad
\alpha_i
:=
\frac{q_i^2}{4\pi Z}
$$

are invariant whenever the displayed ratios are defined.

#### Proof

Since $F'=\lambda F$, substitute $A=A'/\lambda$ and
$F=F'/\lambda$ into the action. Each covariant derivative satisfies
$q_iA=q_i'A'$, and the external pairing satisfies
$J\mathbin{\cdot}A=J'\mathbin{\cdot}A'$. The displayed coefficients and
invariants follow. $\square$

This is BSC-EM-07. It does not say that electric charge is physically
arbitrary after a representation, charge unit, kinetic normalization, and
matter content have been fixed. It says that a bare symbol attached to an
unnormalized potential is not yet a dimensionless interaction strength. The
normalization orbit leaves every $\alpha_i$ invariant; it does **not** make a
fully normalized, experimentally connected $\alpha_i$ unidentifiable.

Gauge covariance and topology alone contain no equation selecting the
remaining invariant $q_i^2/Z$. They admit electromagnetic theories with
different interaction strengths.

### Proposition 7.2 (Flux quantization constrains a product)

In a convention where a charged world line acquires the phase

$$
\exp\!\left(
\frac{iq}{\hbar}\int A_{\mathrm{phys}}
\right),
$$

let the dimensionless connection seen by that matter representation be

$$
\mathcal A=\frac q\hbar A_{\mathrm{phys}}.
$$

For a closed oriented two-cycle $\Sigma$, the first-Chern integrality
condition is

$$
\frac1{2\pi}\int_\Sigma d\mathcal A\in\mathbb Z,
$$

or equivalently

$$
\frac q{2\pi\hbar}
\int_\Sigma F_{\mathrm{phys}}
\in\mathbb Z.
$$

This condition quantizes the normalized holonomy or the product of charge
normalization and physical flux. It does not determine $q$, $Z$, or
$q^2/Z$ separately.

#### Proof

The first statement is the integral-period condition for the curvature of a
$U(1)$ connection. Substitution of the physical normalization gives the
second. Rescaling $q$ and $A_{\mathrm{phys}}$ inversely preserves
$\mathcal A$ and its integral periods. $\square$

This is BSC-EM-08. Dirac-type quantization is a genuine topology-to-physics
bridge once the matter representation and normalization are supplied, but it
does not by itself derive the fine-structure constant.

## 8. The metrological bridge to the fine-structure constant

At low energy in SI units,

$$
\alpha
=
\frac{e^2}{4\pi\varepsilon_0\hbar c}
=
\frac{\mu_0ce^2}{2h}
=
\frac{Z_0}{2R_{\mathrm K}},
$$

where $Z_0=\mu_0c$ is the vacuum impedance and
$R_{\mathrm K}=h/e^2$ is the von Klitzing constant. Since the 2019 SI fixes
the numerical values of $e$, $h$, and $c$, the exact relation is

$$
\mu_0=\alpha\frac{2h}{ce^2}.
$$

The numerical value of $\mu_0$ is therefore no longer fixed exactly; its
relative standard uncertainty is inherited from $\alpha$. Substituting the
pre-2019 exact value

$$
\mu_0=4\pi\times10^{-7}\ {\rm N\,A^{-2}}
$$

to claim a derivation of $\alpha$ would reuse an obsolete definitional
constraint as if it were independent evidence.

This is BSC-EM-09. A change of units can move uncertainty among dimensional
constants, but it cannot manufacture a value for the dimensionless
$\alpha$.

One real experimental bridge uses atom recoil. For an atom $X$, the declared
relation is

$$
\alpha^2
=
\frac{2R_\infty}{c}
\frac{A_{\mathrm r}(X)}{A_{\mathrm r}(e)}
\frac h{m_X}.
$$

An atom-interferometric estimate of $h/m_X$, together with mass ratios,
$R_\infty$, calibration, corrections, and a joint uncertainty model, induces
an identified set for $\alpha$. This is a measurement equation, not a
topological identity.

A second route compares a measured electron magnetic moment with the QED
series and its electroweak, hadronic, mass-ratio, and numerical inputs. In
that route, solving for $\alpha$ is conditional on the stated QED calculation.
Conversely, inserting an independently measured $\alpha$ turns the same
comparison into a QED test. Evidence authority depends on which quantities
are inputs and which are targets.

The 2026 atomic-hydrogen $2S$--$6P$ result is an example of the latter
direction: it uses independently determined $\alpha$ and mass ratios among
the inputs to a bound-state-QED prediction. Agreement does not become an
independent derivation of $\alpha$ merely because the spectrum is
electromagnetic.

The current low-energy value recorded by the 2022 CODATA adjustment remains

$$
\alpha^{-1}=137.035\,999\,177(21).
$$

No theorem in this module predicts that number.

### 8.1 Renormalization transports a boundary value

The symbol $\alpha$ is incomplete unless the report declares which coupling
it means. Examples include:

1. the on-shell or Thomson-limit coupling $\alpha(0)$;
2. a scheme coupling such as
   $\overline{\alpha}_{\overline{\mathrm{MS}}}(\mu)$; and
3. an effective charge inferred from a specified observable at momentum
   transfer $q^2$.

These are connected by matching and vacuum-polarization calculations, not by
silently identifying their numerical values. The Ward--Takahashi identity
enforces the gauge-compatible relation between the vertex and charged-field
renormalizations. It constrains how charge renormalization is represented; it
does not provide a numerical boundary condition for the coupling.

Likewise, a renormalization-group equation

$$
\mu\frac{d\alpha}{d\mu}=\beta(\alpha)
$$

determines a trajectory only after a value such as
$\alpha(\mu_0)=\alpha_0$ and the active particle content, masses, matching
conditions, and scheme are supplied. The exact special case
$\beta\equiv0$ already admits every constant trajectory
$\alpha(\mu)\equiv\alpha_0$; the differential equation does not select one.
For example, in a mass-independent perturbative regime with $N_f$ active
unit-charge Dirac fermions,

$$
\mu\frac{d\alpha}{d\mu}
=
\frac{2N_f}{3\pi}\alpha^2+O(\alpha^3),
$$

so the leading-order solution contains the undetermined integration constant

$$
\frac1{\alpha(\mu)}
=
\frac1{\alpha(\mu_0)}
-\frac{2N_f}{3\pi}\log\frac{\mu}{\mu_0}.
$$

This last display is the solution of the stated one-loop truncation.
Higher-order terms, thresholds, and scheme changes modify the flow and
matching, but not this logical boundary: running transports and tests a
supplied coupling value; it does not derive the infrared value from gauge
symmetry.

This is BSC-EM-10. A report that computes high-energy running from an
experimentally supplied $\alpha(0)$ is a conditional prediction of the
declared quantum field theory. Reversing a measured high-energy observable
through the same model can estimate $\alpha(0)$, but that estimate inherits
the model, matching, nuisance, and calibration obligations.

### 8.2 A binary and constructibility screen for 137

Several striking integers share an exact base-two origin:

$$
\begin{aligned}
2^{31}-1&=2\,147\,483\,647,\\
2^{32}-1&=4\,294\,967\,295\\
&=3\cdot5\cdot17\cdot257\cdot65\,537,\\
65\,537&=2^{16}+1.
\end{aligned}
$$

The first is a Mersenne prime and the maximum positive signed 32-bit integer.
Legacy signed 32-bit Unix timestamps reach that representation boundary in
2038. The second is the maximum unsigned 32-bit integer and is the product of
the five known Fermat primes. The last is the fifth known Fermat prime. These
facts explain both the computing cutoffs and the straightedge-and-compass
constructibility of the regular $65\,537$-gon and of the regular
$(2^{32}-1)$-gon.

There is one exact base-two fact about the integer $137$. Repeated squaring
modulo $137$ gives

$$
2^{16}\equiv50,
\qquad
2^{17}\equiv100,
\qquad
2^{34}\equiv-1
\pmod{137}.
$$

Also $2^4\not\equiv1\pmod{137}$. It follows that

$$
\operatorname{ord}_{137}(2)=68.
$$

Therefore the base-two expansion of the rational number $1/137$ has period
$68$, and $137$ divides $2^{68}-1$ (indeed, it divides $2^{34}+1$). This is
a genuine arithmetic relation to powers of two. It is not a relation to the
specific 16-, 31-, or 32-bit cutoffs:

$$
\begin{aligned}
2^{31}-1&\equiv16\pmod{137},\\
2^{32}-1&\equiv33\pmod{137},\\
65\,537&\equiv51\pmod{137}.
\end{aligned}
$$

The geometric comparison points in the same direction. A regular prime
$p$-gon is constructible only when $p-1$ is a power of two. For $p=65\,537$,
the real cyclotomic degree is

$$
\frac{65\,537-1}{2}=2^{15},
$$

whereas for $p=137$ it is

$$
\frac{137-1}{2}=68=4\cdot17,
$$

which is not a power of two. Thus the regular $137$-gon is not constructible
by straightedge and compass.

Most importantly, the low-energy electromagnetic constant is not exactly
$1/137$. The CODATA value

$$
\alpha^{-1}=137.035\,999\,177(21)
$$

differs from $137$ by about $263$ parts per million in the corresponding
coupling, vastly more than its reported uncertainty. The periodicity result
belongs to the rational number $1/137$, while $\alpha$ is a measured physical
parameter. Promoting one to the other would require a physical map from the
integer construction to $q_i^2/(4\pi Z)$ and then to the metrological report.
No such map is supplied by bit width, timestamp convention, polygon
constructibility, Maxwell's equations, gauge descent, or renormalization-group
flow.

### 8.3 Aperiodic geometry-to-field descent

The Einstein monotile result supplies an unusually clean local-to-global
example, but its mathematical conclusion and an electromagnetic conclusion
have different types. Smith, Myers, Kaplan, and Goodman-Strauss prove that
the Hat is an aperiodic monotile: it tiles the plane, while no admitted tiling
has a nonzero translational symmetry. The Hat itself is the union of eight
kites in the Laves tiling $[3.4.6.4]$, the dual of the
$(3.4.6.4)$ rhombitrihexagonal Archimedean tiling. This is the periodic
deltoidal-trihexagonal kite framework highlighted by the geometric
construction. The periodicity of the elementary kite framework therefore
does not transfer to the global arrangement of Hats. Conversely, the
aperiodicity of that arrangement does not by itself transfer to every
observable constructed from it.

The later chiral theorem sharpens the isometry boundary. Every Hat tiling
mixes reflected and unreflected copies. The equilateral relative
$\operatorname{Tile}(1,1)$ is weakly chiral when reflections are forbidden,
and suitable edge modifications give Spectres whose admitted tilings are
strictly chiral and nonperiodic even when reflections are allowed. Thus
``one tile'', ``one orientation class'', ``no translation'', and ``no mirror
symmetry'' are four different predicates.

To promote one of these predicates to a field or scattering claim, record the
full materialization chain

$$
\mathscr T_{\mathrm{ap}}
\xrightarrow{\,C_{\mathrm{sel}}\,}
X_N
\xrightarrow{\,\Phi_{\mathrm{mat}}\,}
(\varepsilon,\mu,\sigma,\Omega,\mathcal B)
\xrightarrow{\,\mathcal P_{\lambda,p}\,}
Y.
$$

Here $\mathscr T_{\mathrm{ap}}$ is an abstract infinite tiling,
$C_{\mathrm{sel}}$ chooses tile interiors, edges, vertices, centroids, or a
finite approximant $X_N$; $\Phi_{\mathrm{mat}}$ supplies physical scale,
thickness, constitutive dispersion, loss, substrate, interfaces, and
fabrication; and $\mathcal P_{\lambda,p}$ supplies illumination wavelength,
polarization, ports, Maxwell model, calibration, and report map. A finite
fabricated patch is evidence about that declared approximant and experiment,
not an experimental proof that every infinite tiling is aperiodic.

This chain gives an exact descent test. Let $\mathcal M(\mathscr T)$ be the
admissible materializations of a tiling and let
$R(\mathscr T,m)$ be the resulting report. A report predicate $Q$ descends
from the tiling alone only if

$$
Q\!\left(R(\mathscr T,m_1)\right)
=
Q\!\left(R(\mathscr T,m_2)\right)
\qquad
\text{for all }m_1,m_2\in\mathcal M(\mathscr T).
$$

The condition fails in the unconstrained class. One admissible map can erase
the tiling by assigning the same homogeneous $(\varepsilon,\mu,\sigma)$
everywhere, while another can pattern a nonzero contrast on selected
centroids or boundaries. These two maps share the abstract tiling but need
not share a spectrum, band gap, diffraction pattern, polarization response,
or scattering matrix. Therefore no such physical property follows from
aperiodicity alone.

There is a useful sufficient condition for transferring only the
translation-symmetry statement. Let $P$ be the tiling partition and let
$\kappa=(\varepsilon,\mu,\sigma,\ldots)$ be the coefficient field. Call the
encoding translation-faithful when

$$
\tau_v\kappa=\kappa
\quad\Longrightarrow\quad
\tau_vP=P.
$$

Then, immediately,

$$
\operatorname{Stab}_{\mathrm{tr}}(\kappa)
\subseteq
\operatorname{Stab}_{\mathrm{tr}}(P).
$$

If $P$ is aperiodic, a translation-faithful $\kappa$ has no nonzero
translation symmetry. Constant coefficient fields and lattice-periodic
coefficient fields materializing only the unlabeled carrier kite grid violate
faithfulness and give exact counterexamples. Even a faithfully aperiodic
coefficient field establishes
only the absence of an ordinary lattice Bloch decomposition. It does not by
itself establish a band gap, localization, a critical state, a topological
phase, optical activity, circular dichroism, nonreciprocity, or device
performance.

For a declared finite set of identical point scatterers
$X_N=\{(x_j,y_j)\}_{j=1}^N$, the scalar kinematic model is

$$
F_N(k_x,k_y)
=
\sum_{j=1}^N
\exp\!\left(2\pi i(k_xx_j+k_yy_j)\right),
\qquad
I_N=|F_N|^2.
$$

This formula is a conditional structure-factor model, not the full Maxwell
solution for finite holes in a dispersive slab. It already shows that the
selector matters: $I_N(0)=N^2$, changing weights or selected points changes
$F_N$, and intensity discards its phase. In a concrete peer-reviewed
counterexample, Hat-vertex point diffraction is two-periodic because those
vertices lie in an underlying periodic hexagonal net even though the Hat
tiling is aperiodic. The related Spectre vertex and centroid patterns instead
have nonperiodic diffraction with chiral sixfold point symmetry. Real-space
aperiodicity and reciprocal-space periodicity are therefore not logical
negations of one another.

Moritake, Takiguchi, Aihara, and Notomi provide the corresponding 2026
experimental bridge. They selected the centroids of an $H_6$ Hat approximant,
fabricated $372\,100$ circular holes in a $350\,\mathrm{nm}$ SiN film, and
reported sharp Bragg peaks whose positions were insensitive to illumination
position, mirror-reversing pinwheel diffraction, and helicity-dependent
intensity. Their point model uses the displayed $F_N$, while finite hole size
explains a reported high-wavevector envelope absent from the delta-scatterer
calculation. For their golden-ratio/Fibonacci inflation geometry,

$$
\phi=\frac{1+\sqrt5}{2},
\qquad
\theta_{\mathrm{chiral}}
=
\arccos\!\left(\frac{3\phi-1}{4}\right)
\approx15.52^\circ.
$$

This supplies measured-and-modelled evidence along a
geometry-to-fabricated-sample-to-report chain for the stated selector,
approximant, material, wavelength, polarization, and instrument. It does not
close the full constitutive, Maxwell, calibration, or uncertainty obligations
and does not establish a universal photonic band gap, a unique bulk
constitutive law, or the electromagnetic response of every Hat or Spectre
realization. The source-local observation record is BSC-EM-OBS-01; it is not
the proof authority for BSC-EM-11.

This is BSC-EM-11. It is also another exact screen against a proposed
$1/137$ route. The integers eight and three, the golden-ratio/Fibonacci
inflation geometry, the sixfold intensity symmetry, and the angle
$\theta_{\mathrm{chiral}}$ arise from the declared tiling, selector, and
Fourier geometry. None supplies a map to $q_i^2/(4\pi Z)$, a renormalization
boundary value, or a metrological equation for $\alpha$.

## 9. Electromagnetic certificate obligations

A claim-ready electromagnetic certificate records at least:

1. spacetime, orientation, metric, domain, and regularity;
2. bundle, gauge group, matter representation, and quotient;
3. local potentials only when patching data are supplied;
4. field strength, excitation, current, and source compatibility;
5. constitutive law, material state, causality, dispersion, nonlinearity, and
   passivity regime;
6. initial, boundary, interface, radiation, and port conditions;
7. energy density, power orientation, pump, material, loss, and hidden-port
   accounting;
8. port basis, reference plane, impedance, normalization, calibration,
   de-embedding, bandwidth, dynamic range, and uncertainty;
9. exact measured observable and report post-processing;
10. inverse theorem, gauge quotient, stability class, and identified set;
11. coupling convention, renormalization scale or scheme, and charge
    normalization when a coupling is claimed;
12. metrological equations, nuisance quantities, covariance, model
    corrections, and evidence identity; and
13. for patterned-geometry claims, the infinite tiling or finite approximant,
    point/edge/interior selector, materialization map, physical scale,
    structure-factor or full-wave model, illumination, polarization, and
    instrument.

Failure of one coordinate demotes only the claims that depend on it. For
example, absent phase blocks coherent-delay reconstruction but need not block
a calibrated power-absorption claim.

## 10. Claim bindings

| ID | Mathematical content | Boundary |
|---|---|---|
| BSC-EM-01 | A connection-level report is physical exactly when it descends through the declared gauge quotient. | Gauge fixing alone does not establish descent. |
| BSC-EM-02 | On suitable nontrivial topology, equal curvature can coexist with different gauge-invariant holonomy. | Field strength can still be sufficient for a narrower classical target. |
| BSC-EM-03 | Maxwell source compatibility gives $d\mathcal J=0$; a global smooth excitation additionally makes $\mathcal J$ exact. | Singularities, interfaces, and open boundaries need relative or distributional treatment. |
| BSC-EM-04 | Poynting balance separates stored field energy, boundary power, and work on current. | Modulated or dispersive media require pump or material-state terms. |
| BSC-EM-05 | A passive power-normalized scattering map is contractive. | Weight, reference impedance, hidden ports, and stored-energy release must be declared. |
| BSC-EM-06 | Power-only scattering data do not identify phase or delay. | A valid minimum-phase theorem or direct phase measurement changes the report. |
| BSC-EM-07 | Field rescaling changes bare kinetic and current coefficients while preserving $q^2/Z$. | A fixed representation and canonical normalization may remove this coordinate freedom. |
| BSC-EM-08 | Chern/Dirac flux quantization constrains normalized holonomy or a charge-flux product, not $\alpha$. | Matter representation and global bundle data are indispensable. |
| BSC-EM-09 | In the revised SI, fixed $e,h,c$ do not fix $\alpha$; $\mu_0$ inherits its uncertainty through an exact relation. | Metrological definitions are not independent physical measurements. |
| BSC-EM-10 | Ward identities and renormalization-group flow constrain transport and matching of a declared coupling but require a boundary value. | Scheme, scale, thresholds, particle content, and the input measurement remain part of the claim. |
| BSC-EM-11 | A tiling-level predicate transfers to a field or scattering report only when it is constant over the declared selector-and-materialization fiber. | Aperiodicity alone fixes neither diffraction periodicity, chirality, band gaps, nor a coupling. |

The earlier BSC-UNI-01 no-go is therefore sharpened rather than reversed:
gauge structure, topology, Maxwell form, and channel form still do not
determine $\alpha$. They now expose the precise locations where a physical
interaction parameter and a metrological report must enter.

## 11. Prior-art and novelty boundary

The physical and mathematical ingredients are established. Primary or
authoritative sources include:

- J. H. Poynting,
  [On the transfer of energy in the electromagnetic field](https://doi.org/10.1098/rstl.1884.0016),
  *Philosophical Transactions of the Royal Society of London* 175,
  343--361 (1884).
- P. A. M. Dirac,
  [Quantised singularities in the electromagnetic field](https://doi.org/10.1098/rspa.1931.0130),
  *Proceedings of the Royal Society A* 133, 60--72 (1931).
- Y. Aharonov and D. Bohm,
  [Significance of electromagnetic potentials in the quantum theory](https://doi.org/10.1103/PhysRev.115.485),
  *Physical Review* 115, 485--491 (1959).
- J. C. Ward,
  [An identity in quantum electrodynamics](https://doi.org/10.1103/PhysRev.78.182),
  *Physical Review* 78, 182 (1950).
- Y. Takahashi,
  [On the generalized Ward identity](https://doi.org/10.1007/BF02832514),
  *Il Nuovo Cimento* 6, 371--375 (1957).
- M. Gell-Mann and F. E. Low,
  [Quantum electrodynamics at small distances](https://doi.org/10.1103/PhysRev.95.1300),
  *Physical Review* 95, 1300--1312 (1954).
- L. Wantzel,
  [Recherches sur les moyens de reconnaître si un problème de géométrie peut se résoudre avec la règle et le compas](https://www.numdam.org/item/JMPA_1837_1_2__366_0/),
  *Journal de Mathématiques Pures et Appliquées*, first series 2,
  366--372 (1837).
- The Open Group,
  [Rationale for Base Definitions: seconds since the Epoch](https://pubs.opengroup.org/onlinepubs/9799919799/xrat/V4_xbd_chap01.html),
  *The Open Group Base Specifications*, Issue 8.
- D. Smith, J. S. Myers, C. S. Kaplan, and C. Goodman-Strauss,
  [An aperiodic monotile](https://doi.org/10.5070/C64163843),
  *Combinatorial Theory* 4(1), article 6 (2024).
- D. Smith, J. S. Myers, C. S. Kaplan, and C. Goodman-Strauss,
  [A chiral aperiodic monotile](https://doi.org/10.5070/C64264241),
  *Combinatorial Theory* 4(2), article 13 (2024).
- C. S. Kaplan, M. O'Keeffe, and M. M. J. Treacy,
  [Periodic diffraction from an aperiodic monohedral tiling](https://doi.org/10.1107/S2053273323009506),
  *Acta Crystallographica A* 80, 72--78 (2024), with the
  [Spectre addendum](https://doi.org/10.1107/S2053273324008945),
  80, 460--463 (2024).
- Y. Moritake, M. Takiguchi, T. Aihara, and M. Notomi,
  [Chiral diffraction from aperiodic monotile structure](https://doi.org/10.1038/s41467-026-75023-7),
  *Nature Communications* 17, 6085 (2026), with
  [open data](https://doi.org/10.6084/m9.figshare.29313743).
- K. Kurokawa,
  [Power waves and the scattering matrix](https://doi.org/10.1109/TMTT.1965.1125964),
  *IEEE Transactions on Microwave Theory and Techniques* 13, 194--202
  (1965).
- R. B. Marks and D. F. Williams,
  [A general waveguide circuit theory](https://doi.org/10.6028/jres.097.024),
  *Journal of Research of the National Institute of Standards and Technology*
  97, 533--562 (1992).
- A. Buffa, M. Costabel, and D. Sheen,
  [On traces for $H(\operatorname{curl},\Omega)$ in Lipschitz domains](https://doi.org/10.1016/S0022-247X(02)00455-9),
  *Journal of Mathematical Analysis and Applications* 276, 845--867
  (2002).
- C. E. Kenig, M. Salo, and G. Uhlmann,
  [Inverse problems for the anisotropic Maxwell equations](https://doi.org/10.1215/00127094-1272903),
  *Duke Mathematical Journal* 157, 369--419 (2011).
- L. Morel, Z. Yao, P. Clade, and S. Guellati-Khelifa,
  [Determination of the fine-structure constant with an accuracy of 81 parts per trillion](https://doi.org/10.1038/s41586-020-2964-7),
  *Nature* 588, 61--65 (2020).
- X. Fan, T. G. Myers, B. A. D. Sukra, and G. Gabrielse,
  [Measurement of the electron magnetic moment](https://doi.org/10.1103/PhysRevLett.130.071801),
  *Physical Review Letters* 130, 071801 (2023).
- L. Maisenbacher et al.,
  [Sub-part-per-trillion test of the Standard Model with atomic hydrogen](https://doi.org/10.1038/s41586-026-10124-3),
  *Nature* 650, 845--851 (2026).
- Bureau International des Poids et Mesures,
  [SI Brochure, ninth edition, Appendix 2: ampere](https://www.bipm.org/documents/20126/41489676/SI-App2-ampere.pdf/0987a90e-051b-dd7f-827d-3f7b32751a61).
- P. J. Mohr et al.,
  [CODATA recommended values of the fundamental physical constants: 2022](https://doi.org/10.1103/RevModPhys.97.025002),
  *Reviews of Modern Physics* 97, 025002 (2025).

BSC does not claim these results as new. Its added object is the typed
electromagnetic evidence bridge, the exact location of each promotion, and the
falsifiable statement of what remains unidentified when a bridge coordinate
is missing.

## 12. Highest-leverage next proofs

1. Prove a time-domain passive-material theorem with an explicit auxiliary
   material state and storage functional.
2. Bind a calibrated vector-network-analyzer fixture to the weighted
   scattering inequality, including reference-plane transformations.
3. Construct one partial-boundary Maxwell inverse example with an explicit
   identified set and stability radius.
4. Formalize the $U(1)$ bundle, gauge quotient, holonomy, and flux-product
   propositions in a proof assistant.
5. Build two independent metrological evidence graphs for $\alpha$ and
   propagate their correlated input uncertainties without treating theory
   inputs as independent measurements.
6. Extend the finite-dimensional quantum energy ledger to a controlled
   electromagnetic field truncation without hiding cutoff dependence.
7. Freeze a Hat or Spectre approximant, selector, mirrored control,
   fabrication map, scalar structure-factor prediction, full-wave model, and
   calibrated diffraction record, then compare only observables shared by
   those layers.
