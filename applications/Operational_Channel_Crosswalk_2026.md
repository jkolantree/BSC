# Operational-channel crosswalk: four July 2026 experiments

## Status

This is a source-bound application note for the `1.3.0` mathematical
framework. It applies
[the operational channel core](../framework/Operational_Channel_Core.md) to
four recent publications. It is not an independent laboratory replay, raw-data
reanalysis, device simulation, or physical unification claim.

The scientific papers remain authoritative for their experiments. BSC adds
only a typed claim crosswalk and mathematical consequences that follow from
declared channel hypotheses.

## Primary-source register

| Code | Primary publication | Source state inspected |
|---|---|---|
| QPH | K.-Y. Kim et al., [Two-photon interference between independent atomic and quantum dot single-photon sources for hybrid quantum network](https://doi.org/10.1038/s41377-026-02399-y), *Light: Science & Applications* 15, 320 (2026) | Peer-reviewed open article, published 15 July 2026 |
| PTC | T. Guo et al., [Plasmonic metamaterial time crystal](https://doi.org/10.1038/s41586-026-10825-9), *Nature* (2026); open author preprint [arXiv:2510.02845v2](https://arxiv.org/abs/2510.02845) | Peer-reviewed publication, published 29 July 2026; preprint used for method detail |
| HIR | L. Bindi et al., [Discovery of a multicomponent alloy forged by the Hiroshima atomic blast](https://doi.org/10.1126/sciadv.aeg8299), *Science Advances* 12(31) (2026) | Peer-reviewed publication, published 29 July 2026 |
| MWN | B. Govind, P. Raigoza, and A. Apsel, [Broadband encoding and high-speed probabilistic bit generation with integrated microwave neurons](https://doi.org/10.1038/s41467-026-75783-2), *Nature Communications* (2026); [data and code](https://doi.org/10.5281/zenodo.17906138) | Accepted peer-reviewed early-access article in unedited form, published 29 July 2026 |

News reports motivated the comparison, but quantitative rows below are bound
to these primary sources.

## 1. The common structure

All four studies can be represented at the report boundary as

$$
\theta
\longrightarrow
\mathsf{Prep}_\theta
\longrightarrow
\mathsf{Drive}_\theta
\longrightarrow
\mathsf{Measure}_\theta
\longrightarrow
\mathsf{Report}_\theta
\longrightarrow
c_\theta.
$$

That diagram does not identify the underlying physics. It exposes the same
five questions in each field:

1. What state or specimen was prepared?
2. What uncontrolled or driven transformation occurred?
3. Which observable was actually measured?
4. Which post-selection, fit, compression, or label produced the report?
5. Which physical claim really descends through that report?

| Study | Preparation and evolution | Measurement and report | Licensed local claim | Non-inherited promotion |
|---|---|---|---|---|
| QPH | Warm cesium SFWM photon and tuned InAs/GaAs quantum-dot photon; interference at a beamsplitter | Herald-conditioned time-resolved coincidences, spectral fits, and HOM/TPI visibility | The tested sources exhibit the reported spectral compatibility and post-selected two-photon interference | Bell-state measurement, entanglement swapping, teleportation, memory integration, or scalable network |
| PTC | Optically driven plasmonic metamaterial with time-dependent carrier response | THz reflectivity and phase spectroscopy interpreted through a Floquet model | The driven device enters the reported PTC regime and exhibits the reported loss reduction | Spontaneous many-body time-crystal order, observed plasmonic lasing, measured entangled plasmons, or energy without a pump ledger |
| HIR | Blast-affected multicomponent material followed by rapid cooling, with the detailed history unobserved | Single-crystal X-ray diffraction and electron-microprobe composition on extracted micrometre grains | One grain has the reported ordered phase, lattice, and multicomponent chemistry | A unique pressure-temperature-time history, bulk prevalence, mechanical properties, or a device-ready material |
| MWN | CMOS microwave network driven by analog tokens or 8-bit input streams | Mixed spectral features or thresholded stochastic bits, followed by classifiers and cached image reconstruction | The tested chip produces the reported features and input-dependent stochastic outputs | Lossless 8:1 coding, independent samples, intrinsic semantics, cryptographic security, or an end-to-end live image pipeline |

## 2. Hybrid atom-quantum-dot photons

### Source-bound record

The atomic source uses spontaneous four-wave mixing in a warm
$^{133}\mathrm{Cs}$ ensemble at $105\,^\circ\mathrm C$. The reported signal
and idler wavelengths are $917.48\,\mathrm{nm}$ and $852.35\,\mathrm{nm}$.
The InAs/GaAs quantum-dot emission is thermally tuned to the atomic transition
at $12.4\,\mathrm K$. The article's phrase “without spectral modification”
therefore means no post-emission narrowband filter or frequency converter; it
does not mean that emitter tuning, heralding, or temporal selection was absent.

The measured high-resolution spectra give overlap

$$
A=0.88\pm0.01.
$$

The paper explicitly treats this as an upper bound on full photon
indistinguishability because polarization, temporal, spatial, and other
degrees of freedom must also match. In the heterogeneous-source TPI
measurement, the reported raw visibility is $0.41$, the threefold rate is
$1.07\pm0.14\,\mathrm{Hz}$, and a detector-resolution deconvolution gives
$0.65\pm0.14$.

### BSC interpretation

The relevant quantum state is not certified by one spectral scalar. The
actual report channel includes heralding, an $80\,\mathrm{ps}$ selection
window, detector jitter, $40\,\mathrm{ps}$ bins, source-rate imbalance,
multi-photon contamination, and a deconvolution model. Accordingly:

- spectral overlap is one observable coordinate, not equality of quantum
  states;
- raw and corrected visibility are different reports with different model
  dependencies;
- post-selection is part of the experiment and its success probability cannot
  be omitted from an end-to-end network claim;
- the complete heralding instrument, including failure, is contractive, while
  renormalization on success is nonlinear and can amplify distinguishability;
- Theorem BSC-CHN-01 may propagate a declared trace-distance defect through a
  fixed source-channel-measurement chain, but this paper does not supply every
  local reachable-set bound needed for such a certificate.

The result is an important heterogeneous-interface demonstration. It does not
close BSC-QOP-03 and does not by itself execute a hybrid network protocol.

The exact BSC-QPH-02 counterexample makes the marginal boundary sharp. For
orthogonal frequency modes, define

$$
|\psi\rangle
=
\frac{|\omega_1\rangle+|\omega_2\rangle}{\sqrt2},
\qquad
|\phi\rangle
=
\frac{|\omega_1\rangle-|\omega_2\rangle}{\sqrt2}.
$$

The spectral intensities are identical, so their intensity-overlap score is
$1$, while $\langle\psi|\phi\rangle=0$ and the pure-state trace distance is
$1$. Spectral phase and every other unmeasured mode must therefore remain in
the completion ledger.

## 3. Driven plasmonic photonic time crystal

### Source-bound record

The reported device is an Au/$\mathrm{Si_3N_4}$/InSb plasmonic cavity array
with $41\,\mu\mathrm m$ stripes, $16\,\mu\mathrm m$ gaps, $57\,\mu\mathrm m$
period, and an equilibrium resonance near $0.77\,\mathrm{THz}$. The open
preprint reports a drive near $0.69\,\mathrm{THz}$ at roughly
$40\,\mathrm{kV\,cm^{-1}}$ at room temperature. The publication reports
near-unity coherent sub-cycle modulation, a transition through an exceptional
point at which two Floquet modes coalesce, and more than $50\%$ reduction of
plasmonic loss in the driven regime.

The source's roughly $80\%$ effective-mass modulation is model-inferred, using
a fitted coupling fraction and leading-order Kane-band approximation. It
concerns the driven carrier effective mass relative to its material baseline.
It must not be rewritten as an unqualified claim that an electron acquired
$0.8$ times the vacuum electron rest mass.
Plasmonic lasing is predicted to be experimentally reachable; it is not
reported as observed. Correlated or entangled plasmon production belongs to
theoretical modeling, not the reported measurement.

### Energy ledger

For a reduced driven open-system model,

$$
\dot\rho
=
-\frac{i}{\hbar}[H(t),\rho]
+\mathcal D_t(\rho),
$$

BSC-ENE-01 requires

$$
\frac{d}{dt}\operatorname{Tr}[\rho H]
=
\operatorname{Tr}[\rho\dot H]
+
\operatorname{Tr}[H\mathcal D_t(\rho)].
$$

Within the declared reduced model, the first term is the modulation-power
term. Equality to laboratory pump power requires a calibrated bridge among
the fitted Hamiltonian, incident pump field, switching work, material
absorption, and unobserved output ports. Emergent gain and
reduced loss are therefore not conservation paradoxes. A complete energy
claim would additionally bind pump energy, reflected and transmitted fields,
material absorption, bath exchange, and any switching work on a common
interval.

BSC-ENE-01 is finite-dimensional. Direct application to the full bosonic
cavity therefore requires either a controlled finite-dimensional truncation
or trace-class and operator-domain hypotheses sufficient to justify
differentiation and cyclicity. The identity alone is not a first or second
law, an entropy-production theorem, or validation of the fitted Floquet model.

This is an externally driven Floquet photonic time crystal. It is not, by that
name alone, spontaneous breaking of continuous time-translation symmetry in
an autonomous many-body system.

## 4. Hiroshima blast-forged multicomponent alloy

### Source-bound record

The study inspected 34 roughly equal-sized, author-supplied Hiroshima debris
specimens. One contained several Fe-Cr grains; four promising grains of
roughly $8$--$10\,\mu\mathrm m$ were purposively selected for single-crystal
X-ray diffraction. Three were ordinary body-centered-cubic $\alpha$-Fe. The
fourth was assigned an ordered AlAu4-type derivative of $\beta$-Mn (also
rendered AuAl4-type in the article) with space group $P2_13$ and lattice
parameter $6.2666(5)\,\text{\AA}$.

Four electron-microprobe points on that grain give the reported mean weight
percentages

| Element | Fe | Cr | Si | Ni | Mo | Mn | Al | P |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Mean wt% | 62.69 | 14.71 | 7.02 | 8.95 | 3.70 | 2.09 | 0.56 | 0.02 |

This supports the local composition and structure claim. Formation by mixed
vapor condensation and ultrafast quenching is a physically motivated
historical inference using context and microstructure.

The $34\to1$ host $\to4$ selected grains $\to1$ unusual phase funnel is not a
probability sample and supports no debris-population prevalence estimate.

### Inverse boundary

Let $\theta$ encode a candidate pressure-temperature-composition-time history
and let $F(\theta)$ be the predicted terminal grain record. For measured
record $y$ and declared discrepancy $\varepsilon$,

$$
\mathcal I_\varepsilon(y)
=
\{\theta:d(F(\theta),y)\le\varepsilon\}.
$$

The observations establish a unique history only if the target historical
property is constant on this identified set. The source does not provide an
injectivity theorem, a complete kinetic forward map, or a certified
uncertainty set for all admissible histories. BSC therefore retains the
formation interpretation as source-supported and plausible while blocking
promotion to one uniquely reconstructed trajectory.

The same boundary blocks inference from one grain to abundance throughout the
debris, mechanical or electronic performance, or deliberate materials
manufacturing.

## 5. Integrated microwave neurons and probabilistic bits

### Source-bound record

The reported chip was fabricated in $45\,\mathrm{nm}$ GlobalFoundries RFSOI
CMOS. Its coupled microwave paths transform low-frequency token controls into
features spanning approximately $10$--$13\,\mathrm{GHz}$, mixed to a
$0$--$3\,\mathrm{GHz}$ measurement band.

For the token-association demonstration, 125 physical tokens generate
15,500 ordered distinct pairs. A supervised linear classifier acts on 34
measured features. The resulting association matrix is therefore conditional
on the feature construction, training split, labels, and classifier.

In the probabilistic-bit mode, each of the 256 8-bit input patterns was
repeated 300 times. Two thresholded samples at $625\,\mathrm{MS\,s^{-1}}$
produce the reported Static and Dynamic bits. Relative phase against a
free-running oscillator contributes variability. The source does not by this
fact establish a deployment law of independent uniform phases or
conditionally iid bits.

The image demonstration samples pixels from a cache of 300 measured outcomes
per input pattern. It is not a live end-to-end acquisition-to-transmission
pipeline. A one-bit draw per 8-bit pixel gives a nominal one-eighth raw bit
rate with visible distortion; averaging multiple draws improves PSNR while
spending additional bits.

### Conditional channel theorem

If the repeated output is genuinely

$$
Y_i\mid X=x
\mathrel{\overset{\mathrm{iid}}{\sim}}
\operatorname{Bernoulli}(q_x),
$$

then BSC-ENC-01 gives

$$
I(X;Y^N)=I(X;K)\le\log_2(N+1),
\qquad K=\sum_iY_i.
$$

For a uniform 8-bit $X$, $N\ge255$ is necessary for eight bits of mutual
information. It is not sufficient: BSC-ENC-02 proves that 256 scalar Bernoulli
laws cannot have pairwise disjoint finite-sample supports, so zero-error
recovery is impossible at every finite $N$ under this model.

The honest raw-bit compression factor is

$$
\mathcal C_N=\frac8N.
$$

Thus $N=1$ is nominal 8:1 lossy coding, $N=8$ is no raw-bit compression, and
$N>8$ is expansion. PSNR improvement at 10, 100, or 1000 draws must be
reported with the corresponding raw output count and, when outputs are
actually sent, the wire rate as a separate coordinate.

### What 300 repeats establish

Under independent sampling, with $\widehat q_x$ the observed frequency,

$$
\Pr\left\{
\max_x|\widehat q_x-q_x|>\varepsilon
\right\}
\le512e^{-600\varepsilon^2}.
$$

At simultaneous 95% coverage this gives
$\varepsilon\approx0.1241$. Two symmetric empirical confidence intervals
supplied by this bound are disjoint only when the estimated biases differ by
more than approximately $0.2482$. This is conservative, but it shows why 300
repetitions do not make all 256 biases precisely known. The physical
independence and stationarity assumptions still require diagnostics.

The same inequality makes a separate point: a finite table of input-dependent
biases is learnable by repeated queries. The article itself does not present
the device as a formal cryptographic primitive. Hardware specificity or
analog phase sensitivity therefore supplies neither a secret nor a security
game.

### Semantic alignment

If both axes of an association matrix represent the same entities, use the
permutation convention $P_{\phi(i),i}=1$. One identity map then requires

$$
S=PCP^{\mathsf T}.
$$

Fitting independent row and column permutations establishes only
$S=PCQ^{\mathsf T}$. The latter is appropriate for two separately typed
entity sets, but not as proof that one token identity preserves an
endorelation. Approximate same-identity alignment is a graph-matching or
quadratic-assignment problem; a linear assignment alone does not solve it in
general.

## 6. The actual synthesis

The four studies support a unification of **evidentiary form**:

1. **Heterogeneous source compatibility is operational.** It is established
   through specified observables and post-selection, not resemblance.
2. **Temporal order requires an energy and drive ledger.** A periodic
   response may be real while the pump remains the source of useful energy.
3. **A terminal material record does not uniquely reconstruct a history.**
   Identified sets, not narrative uniqueness, are the correct inverse object.
4. **Compression, semantics, and security are different claims.** Each has a
   different channel, loss function, and falsifier.
5. **Every downstream result is report-relative.** Post-processing cannot
   resurrect distinctions already erased by preparation, dynamics, or
   measurement.

This synthesis is useful because the same theorems expose different causal
failure modes without conflating the systems. It is not a unified field
theory.

## 7. Why 1/137 does not emerge here

The low-energy electromagnetic coupling has 2022 CODATA value

$$
\alpha^{-1}=137.035\,999\,177(21).
$$

None of the four studies derives that value, and the operational-channel core
cannot do so: its diagrams remain valid for physical completions with
different coupling constants. Cesium and quantum-dot transitions of course
depend on electromagnetic physics, and the plasmonic device depends on
electromagnetic material response, but participation in QED is not a
derivation of $\alpha$.

A serious bridge to 1/137 would require a physical action or Hamiltonian,
normalization and renormalization-scale conventions, a dimensionless
prediction, and metrological comparison. Numerological recurrence of 137 in a
frequency ratio, graph size, fit, or boundary count is not evidence of such a
bridge.

## 8. Highest-value next experiments

| Domain | Smallest decisive next record |
|---|---|
| Hybrid photons | A frozen end-to-end Bell-state or entanglement-swapping protocol with success probability, loss, visibility, and memory/interface defects in one certificate |
| PTC | A common-interval pump/device/output energy budget with calibrated uncertainty, followed by a predeclared lasing or nonclassical-correlation test |
| Hiroshima alloy | A kinetic forward family and uncertainty-calibrated inverse identified set tested against multiple grains and independent synthesis/quench controls |
| Microwave neuron | Fresh-stream rather than cached image trials; dependence/stationarity tests; rate-distortion curves charged by raw output bits and, separately, any bits actually transmitted; same-permutation semantic alignment; a separate security evaluation only if a security claim is made |

These tests would raise local evidence readiness. None would automatically
promote the other domains or the BSC framework as a whole.
