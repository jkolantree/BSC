# ASTRA dual-rent source-admission crosswalk

## Status and authority

This post-v1.4.0 note is a **citation-only crosswalk and independent
reconstruction**. It does not import the ASTRA package, certify the package as
a whole, replay any cited experiment, or claim that the package's authors or
sources endorse BSC. No ASTRA prose, figure, executable, or data file is
redistributed here.

The admitted contribution is narrow: ASTRA's distinction between physical
change and diagnostic gain is rewritten as a pair of typed statistical
comparisons, checked against the existing BSC operational-channel boundary,
and illustrated by exact finite countermodels. The name "dual rent" is useful
terminology, not a BSC novelty claim. The result allocates no new BSC claim or
fixture identifier and changes no release record.

## Frozen source identity

The supplied source family has six separately delivered byte records.

| Source record | SHA-256 | Admission |
|---|---|---|
| `ASTRA_Dual_Rent_Local_to_Global_Audit_Form_v0.3.0.pdf` | `62ee91f1d855fba12781e44aed8a5958b159508459bce53e5dc9eaefe48936ef` | inspected source; not redistributed |
| `ASTRA_v0.3.0_Public_Ground_Reading.pdf` | `cc722b73741049440caaf307d0fbeee7b543755c53f8114a114b7adcef0e7c28` | inspected source; not redistributed |
| `ASTRA_v0.3.0_Verification_Report.pdf` | `a7c0f9b9b979ec6bc5aeb685aa3165a5d1c89a60f712573a5a1871cf2831b35e` | source-asserted report; not independent verification |
| `ASTRA_Framework_v0.3.0_Dual_Rent_Arithmetic_Seams.zip` | `2f8c26c92826c0464ae88048d9c3e68a4404ee5d9b8f46a660a0733ccddd75ab` | inspected package; not redistributed |
| archive checksum sidecar | `9a6cd6158024df295000da160af73451676313602700e9aac9749a0adb13d9a4` | identity sidecar; not independent evidence |
| archive verification note | `14d9452b3f092a8497e61cafa4ce24fedbf4afdd41e59692150babafa8979594` | source-asserted note; not independent evidence |

The archive hash matches its checksum sidecar. Independent inventory checks
found 333 safe, case-distinct regular-file members, a complete 331-file
payload manifest, and a complete 332-row checksum inventory with no mismatch.
The three separately supplied PDFs are byte-identical aliases of the copies
inside the archive and therefore are not counted as independent evidence. The
archive's 171-page main PDF has inner SHA-256
`39c722bb8ace94a28b08aa92d0596cc5342b156d8da05ff00737f5f23b8319e1`.
The outer PDFs identify themselves as ASTRA v0.3.0 records; only the
verification report embeds an author field (`ASTRA release verification`).
The inner main PDF embeds `Jacko T.; ASTRA multidisciplinary synthesis`.

Fresh execution of the bundled test suite produced 27 passing tests in a
disposable current Python environment. That environment was not pinned by the
package, and the tests, generators, ledgers, report, and retained logs share
one source root. The result is harness-local execution, not independent
validation of the package's 80 claims.

## 1. Typed dual-rent comparison

Fix a finite candidate set $\mathcal K$, one prior $p(k)>0$, and a common
finite report-label space $Y$. In the classical case also fix a common finite
physical outcome space $W$. Two declared protocols $\Gamma_0$ and $\Gamma_1$
induce joint mass functions

```math
P_i(k,w,y)=p(k)\,\mu_i^k(w)\,M_i(y\mid w,k),
\qquad i\in\{0,1\}.
```

The dependence of $M_i$ on $k$ is part of the declared physical model. The
controller follows one fixed declared intervention and has no oracle access to
the unknown $k$; candidate dependence may enter only through the modeled
physical response.

For a finite-dimensional quantum experiment, use a common Hilbert space,
candidate-conditioned states $\rho_i^k$, and a declared quantum-to-classical
measurement/report channel. For a POVM
$\lbrace E_{i,y}\rbrace_{y\in Y}$, the induced
report law is

```math
\nu_i^k(y)=\mathrm{Tr}(\rho_i^kE_{i,y}),
\qquad
P_i(k,y)=p(k)\nu_i^k(y).
```

A general instrument must retain every classical outcome and its
post-measurement branch. Density operators are not substituted into the
classical joint-law formula.

Let $d_{\mathrm{phys}}$ be total variation classically and trace distance
quantum mechanically. Define, with $\sigma_i^k=\mu_i^k$ classically and
$\sigma_i^k=\rho_i^k$ quantum mechanically,

```math
R_{\mathrm{dyn}}
=
\sum_{k\in\mathcal K}p(k)
d_{\mathrm{phys}}\!\left(\sigma_1^k,\sigma_0^k\right),
```

```math
R_{\mathrm{epi}}
=
I_{P_1}(K;Y)-I_{P_0}(K;Y).
```

Mutual information is measured in a declared log base; this note uses bits.
Both quantities are protocol contrasts, not intrinsic properties of a seam.
$R_{\mathrm{epi}}$ can be negative. Comparing values obtained with different
candidate labels, priors, report codings, horizons, or decision tasks requires
a separately justified transport; otherwise the subtraction is not admitted.

This definition repairs two ambiguities in the supplied presentation.

1. Dynamical change is compared candidate by candidate before averaging, so
   opposite candidate-specific changes cannot disappear by mixing.
2. Physical future $W$ is distinct from observed report $Y$. A changed report
   can expose a pre-existing distinction without changing the physical future,
   while a physical intervention can change every future without making the
   candidate more identifiable.

Energy, elapsed time, sample count, bandwidth, discarded outcomes, and other
resources are separate ledger coordinates. Neither scalar above is an
efficiency until its denominator and boundary are declared.

## 2. Seam information is a standard experiment quantity

For one protocol, write $\nu^k=P(Y\in\cdot\mid K=k)$ and
$\bar\nu=\sum_kp(k)\nu^k$. On a finite report space,

```math
I(K;Y)
=
\sum_k p(k)D_{\mathrm{KL}}(\nu^k\Vert\bar\nu).
```

Thus seam information is the prior-weighted Jensen--Shannon divergence of the
terminal report laws. Nonnegativity and the equality condition for relative
entropy give

```math
I(K;Y)=0
\quad\Longleftrightarrow\quad
\nu^k=\nu^{k'}
\ \text{for all positive-prior }k,k'.
```

This is a finite statistical-experiment identity. It does not prove structural
identifiability outside the declared candidate family, validate the physical
model, or license an exact decoder from a merely positive mutual information.
The exact finite-label boundary remains BSC-QUO-03.

## 3. No passive information amplification

Suppose a common Markov report kernel $R$ is appended to every candidate law.
The data-processing inequality gives

```math
I(K;R(Y))\le I(K;Y).
```

The corresponding total-variation statement, and its common fixed
CPTP/trace-distance, POVM, and report-kernel forms, are already recorded by
BSC-CHN-02. A changed POVM is a changed experiment rather than downstream
processing of the same report. Consequently, a common passive downstream seam
cannot resurrect information erased upstream.
Positive epistemic rent must be attributed to a changed experiment, such as:

- access to a previously unreported observable;
- one fixed intervention whose physical response depends on the candidate;
- an active measurement or intervention with its resources charged; or
- conditioning whose complete success/failure instrument, success
  probability, yield, and throughput remain visible.

A normalized successful branch can be more distinguishable because
conditioning is nonlinear. Calling that an amplification while omitting the
failure branch is not admitted. Likewise, numerical separation of fitted
curves is not proof of candidate identifiability or physical adequacy.

## 4. Two exact independence countermodels

Let $K$ be a fair bit.

### Diagnostic access without dynamical rent

Under both protocols set $W=K$. Protocol $\Gamma_0$ discards $W$ and always
reports $Y=0$; protocol $\Gamma_1$ reports $Y=W$. The candidate-conditioned
physical laws are unchanged, so

```math
R_{\mathrm{dyn}}=0.
```

But $I_{P_0}(K;Y)=0$ and $I_{P_1}(K;Y)=1$ bit, hence
$R_{\mathrm{epi}}=1$ bit. The gain comes from changed access, not from a
common downstream channel.

### Dynamical rent without diagnostic access

Under $\Gamma_0$ set $W=0$ for every candidate; under $\Gamma_1$ set $W=1$
for every candidate. Both protocols always report $Y=0$. Candidate-wise total
variation is one, so $R_{\mathrm{dyn}}=1$, while both mutual informations and
$R_{\mathrm{epi}}$ are zero. Physical change alone need not discriminate the
candidate.

These examples prevent either rent from being used as a proxy for the other.

## 5. Exact static reservoir degeneracy

One narrow local-to-global example from the package admits a direct exact
derivation. Let $L=L^T\succeq0$ be the nonnegatively weighted Laplacian of a
finite connected undirected graph, so
$\ker L=\mathrm{span}\lbrace\mathbf1\rbrace$ and $\mathbf1^TL=0$. Let $C$ have
positive diagonal entries, and let node $s$ be the sole external linear sink
with coefficient $\lambda>0$. For source vector $b$, the model is

```math
C\dot T
=
-LT-\lambda e_se_s^TT+b.
```

Every equilibrium satisfies

```math
(L+\lambda e_se_s^T)T=b.
```

Left multiplication by $\mathbf1^T$ gives the exact identity

```math
\boxed{T_s=\frac{\mathbf1^Tb}{\lambda}}.
```

For nonzero $v$,
$v^T(L+\lambda e_se_s^T)v=v^TLv+\lambda v_s^2>0$: equality would force $v$
to be constant and $v_s=0$, hence $v=0$. The equilibrium is therefore unique.
Its static surface value depends on total input and the sole-sink coefficient,
not on the internal topology or capacities. This proves model-local static
degeneracy; it does not prove that frequency-domain data identify topology.
That stronger numerical lane is withheld below.

## 6. Source-admission findings

| Package lane | Evidence observed | BSC disposition |
|---|---|---|
| Dual-rent vocabulary | source-asserted definitions plus the exact reconstruction above | citation-only crosswalk to BSC-CHN-02 and BSC-QUO-03 |
| Sole-sink static identity | exact hand derivation and independent rational examples | admitted only under the displayed finite linear hypotheses |
| Three-variable Keller map | determinant $-2$ and an exact rational three-point collision independently reproduced; 14 odd-prime reductions also checked | strong later independent-reconstruction candidate; no identifier or fixture allocated here |
| Prime-difference arithmetic | symbolic identities and a bounded seven-prime, 34,993-case scan with zero hits were independently checked | deferred; finite scan is not an unrestricted proof |
| SPPT frequency/topology benchmark | bundled tests execute, but narrative optima conflict with canonical JSON | `NOT_ADMITTED` pending one corrected authority and fresh independent replay |
| Experimental and quantum case studies | citations and same-package summaries; no raw-data or apparatus replay | citation-only; no empirical promotion |
| Archaeological, origin, panspermia, and hidden-history material | analogies and hypotheses outside this repository's declared program | not integrated |
| Verification report | polished same-package report | source asserted; not independent or fail-closed verification |

The exact Keller result is consistent with the current higher-dimensional
counterexample record, including
[arXiv:2608.00222v1](https://arxiv.org/abs/2608.00222v1). It supplies no conclusion
about the still-open two-dimensional case. The cited record is a recent
preprint, not a peer-review boundary. Any executable BSC treatment must follow
the already reserved electromagnetic fixture sequence, use fresh identifiers,
and independently validate exact domains and serialization.

## 7. Preserved defects and negative gates

The audit found defects that are intentionally not averaged into an overall
PASS.

1. `verification/verify_v030.py` writes overall and gate-level PASS values
   without turning failed booleans into assertions or a nonzero exit.
2. Its source-support gate checks self-entered PASS labels and citation-key
   presence, not whether a source entails a claim.
3. A retained `27 passed` log is treated as evidence by the verifier instead
   of invoking the test runner.
4. The technical supplement reports frequency-grid optima
   `(16.0319, 0.271916)` and `(20.1111, 0.201304)`, while canonical JSON
   reports `(42.340425531914896, 0.16627084041143314)` and
   `(20.079787234042556, 0.1975524418167117)`.
5. The package supplies no dependency lock or complete frozen environment.
6. Several arithmetic entry points do not fail closed on composite or invalid
   moduli; one valuation interface can fail to terminate at base one.
7. Claim `C054` says the plane Jacobian case is settled while assigning it an
   open status. The higher-dimensional result does not settle dimension two.
8. The v0.3 package's text-and-figures notice still names v0.2, so no license
   inference is made for newly added material.
9. Reports, ledgers, checksums, duplicate PDFs, generated figures, tests, and
   logs descending from the same package are not independent evidence.
10. The topology-recovery benchmark is not blind in evaluation-integrity
    terms: its generator and truth are in the script, the true graph is in the
    closed candidate family, each candidate receives a parameter-dependent
    equilibrium initial state, and held-out error is scored against noiseless
    simulator truth.
11. The seam-information illustration boxcar-averages the signal while holding
    complex-noise standard deviation fixed. No continuous/discrete noise
    process or post-averaging covariance is supplied for a cadence claim.
12. The mutual-information spectrum uses fitted point estimates, equal priors,
    circular Gaussian noise, no parameter uncertainty or error bars, and clips
    negative estimates to zero. It is a synthetic illustration, not calibrated
    model selection.
13. Several one-program empirical reports are labeled `Established` even
    though replication and apparatus transfer were not supplied.
14. The evidence-independence graph covers six grouped nodes and omits the
    seven added calibration cases; it is illustrative rather than complete.

The following conditions therefore fail closed:

- a source-hash mismatch or one-byte mutation;
- a changed candidate prior, label map, outcome space, or horizon presented as
  the same dual-rent comparison;
- passive common processing presented as positive information gain;
- postselection without the complete instrument and success probability;
- narrative/JSON disagreement promoted to a numerical result;
- same-package tests or a retained log promoted to independent verification;
- finite or numerical agreement promoted to a universal proof;
- a higher-dimensional counterexample promoted to the plane case;
- a stale license notice treated as permission to copy the package; or
- any fixture, release, empirical, novelty, or priority promotion from this
  citation-only note.

## 8. Sequencing boundary

This note adds no fixture and reuses no existing claim namespace. The strongest
later candidate is an independently reconstructed exact Keller local-to-global
certificate using the next available identifiers only after the existing
electromagnetic executable milestone. The prime-difference, SPPT, broad
empirical, and historical lanes remain separate deferred work.
