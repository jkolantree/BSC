# Exact attack on the $26\times26$ queen-domination decision problem

## Status and authority

This post-v1.4.0 application is a bounded **independent reconstruction** of a
finite combinatorial decision problem. It is an attack package, not a solved
case, a fixture, a release result, or a priority claim.

As checked on 6 August 2026, the public record gives

$$
13\leq\gamma(Q_{26})\leq14,
$$

where $\gamma(Q_n)$ is the minimum number of queens that occupy or attack all
squares of an $n\times n$ board. Weakley's general bound

$$
\gamma(Q_{m\times n})\geq
\min\left\lbrace m,n,\left\lceil\frac{m+n-2}{4}\right\rceil\right\rbrace
$$

gives the lower value 13. The retained external witness gives the upper value
14. The exact unresolved decision is therefore:

**Question:** Does a set of thirteen queens dominate the 26 by 26 board?

The current source boundary is:

- OEIS A075458: <https://oeis.org/A075458>;
- public 14-queen witness: <https://oeis.org/A075458/a075458.txt>;
- W. D. Weakley, *Queen Domination of Even Square Boards*, EJC 29(2),
  P2.50 (2022), <https://doi.org/10.37236/10617>; and
- T. Rostami and C. Bright, *Queen Domination by SAT Solving*,
  arXiv:2508.11945v2 (29 July 2026),
  <https://arxiv.org/abs/2508.11945>.

The SAT paper and public implementation informed the verification boundary.
No source code from that implementation is copied here. The public Gamma
repository showed no license file when checked, and these BSC encodings were
independently implemented from the mathematical definitions and papers.

## Exact witness semantics

Coordinates are one-based pairs $(r,c)$ with $1\leq r,c\leq n$. A queen at
$(r,c)$ dominates $(u,v)$ exactly when

$$
r=u,\qquad c=v,\qquad r-c=u-v,\qquad\text{or}\qquad r+c=u+v.
$$

The definition includes the occupied square. A positive result consists of
thirteen distinct coordinates for which this predicate holds for every one of
the 676 squares. The dependency-free checker in
[`tools/q26_queen_domination.py`](../tools/q26_queen_domination.py) recomputes
that statement directly using integer arithmetic. A second checker uses only
the four occupied-line sets.

## Three independent decision lanes

### Lane A: direct CNF

Let $x_{r,c}$ state that $(r,c)$ contains a queen. For every target $(u,v)$,
the direct encoding contains

$$
\bigvee_{(r,c)\in N[u,v]}x_{r,c},
$$

where $N[u,v]$ is its inclusive queen neighbourhood. An independently written
unary prefix counter enforces $\sum x_{r,c}\leq13$.

### Lane B: line CNF

The line encoding introduces variables for every row $R_r$, column $C_c$,
difference diagonal $D_{r-c}$, and sum diagonal $A_{r+c}$. Every square has the
four-literal clause

$$
R_r\vee C_c\vee D_{r-c}\vee A_{r+c}.
$$

Two modes are available:

- `exact` uses $L\leftrightarrow\bigvee_{q\in L}x_q$;
- `supported`, matching the paper's search construction, uses only
  $L\rightarrow\bigvee_{q\in L}x_q$.

The supported mode is still equisatisfiable. In any model, a selected line is
supported by a queen and each domination clause selects such a line. Conversely,
given a dominating queen set, selecting exactly its occupied lines satisfies the
formula. Because each queen occupies four labelled lines, the redundant bound

$$
\sum_L L\leq4\cdot13=52
$$

is sound and enabled by default. A separately implemented balanced totalizer
encodes both cardinality bounds.

### Lane C: direct OPB

The direct pseudo-Boolean artifact contains 676 primary variables, 676
independently reconstructed coverage inequalities, and one cardinality
inequality. It does not call either CNF geometry builder. The writer uses the
restricted OPB header, ASCII, `>=` only, and represents the upper bound as

$$
-\sum_{r,c}x_{r,c}\geq-13.
$$

This is the preferred semantic-audit input for an Exact/VeriPB/CakePB lane.
The local suite checks its strict surface grammar and exhaustively compares its
semantics on small boards. No Exact, VeriPB, or CakePB parser was available on
this Windows host, so target-tool parsing and proof replay remain `NOT_RUN`.

## Sound reductions

### Hilbert ordering and $D_4$

Cardinality inputs and the optional lexicographic symmetry vectors use a
deterministic Hilbert order by default; row-major and domination-degree orders
remain explicit alternatives. Seven lex-leaders require the primary vector to
be no greater than each nonidentity $D_4$ image, with $0<1$. Every finite orbit
has a least representative. Exhaustive tests check arbitrary lex vectors, group
closure, attack preservation, and complete small-board semantics.

Symmetry breaking is only a search optimization. A positive model is checked on
the unsymmetrized board definition.

### Q26-only theorem strengthening

The optional `--q26-structural` mode is deliberately scoped to the line CNF at
$(n,k)=(26,13)$. It adds the following necessary conditions:

1. Weakley's lower bound makes an at-most-13 witness exactly 13; an exact unary
   lower-bound circuit asserts this explicitly.
2. A monochromatic 13-queen witness would require odd $d,e\leq13$ satisfying
   $d^2+12e^2=741$. Only $e=1,3,5,7$ can occur. They give
   $d^2=729,633,441,153$;
   the two squares have $d=27,21>13$, and the other two are nonsquares. Thus a
   witness must be bichromatic.
3. Weakley's Proposition 11 then limits the checkerboard-color imbalance to two;
   thirteen queens therefore split $6/7$. The encoding imposes at most seven of
   each color.
4. The equality-case argument used in that proposition leaves at most one
   repeated queen in the row inventory and, independently, in the column
   inventory. Hence 12 or 13 distinct rows and 12 or 13 distinct columns are
   occupied. Supported row/column variables encode the corresponding lower
   bounds.

This mode is a **discovery accelerator**, not automatically the promotion
formula. An UNSAT claim from it additionally requires an independently reviewed
theorem-to-CNF bridge. The conservative negative path is an unstrengthened CNF
proof plus the direct OPB cross-check.

The companion
[`Q26_Symmetry_Parity_Profile_Reduction.md`](Q26_Symmetry_Parity_Profile_Reduction.md)
makes the occupied-line quotient explicit: 156 coarse parity-profile shells,
tightened to 142 by Weakley's Lemma 6. These shells form an exhaustive
structural over-cover, not a list of queen placements or solved SAT instances.

## Decisive evidence

### Positive branch

A SAT model is discovery output. Promotion requires:

1. decode only primary square variables;
2. reject duplicates, out-of-range coordinates, or more than thirteen queens;
3. recompute domination of all 676 squares without consulting the formula; and
4. obtain identical normalized coordinates and coverage results from both
   independent witness checkers.

A valid thirteen-queen list and the established lower bound prove
$\gamma(Q_{26})=13$. No SAT proof trace is needed once the finite coordinate
witness passes direct checking.

### Negative branch

`UNSAT` text, a timeout, a conflict count, or agreement between solvers is not a
nonexistence proof. Promotion requires:

1. frozen formula bytes, byte size, and SHA-256;
2. a complete LRAT or equivalently strong retained proof from a pinned solver;
3. successful replay by an independent proof checker;
4. a checked encoding-to-board bridge;
5. preferably a separately generated direct OPB proof replay; and
6. the independently checked fourteen-queen witness.

For cube-and-conquer, every cube and leaf proof must bind the base-formula hash.
A checked cover proof must reject missing, duplicate, contradictory, or altered
cubes. Solver logs and counts do not establish coverage.

The current host has no executable CakeLPR, LRAT-Catcher, VeriPB, CakePB, or
standalone proof-producing solver stack. A negative campaign therefore requires
a pinned Linux, WSL, container, or HPC environment. Discovery-only Python SAT
bindings cannot close this branch.

## Reproductions and bounded search observations

The local direct formulation reproduced the known SAT/UNSAT boundary for every
board from $n=4$ through $n=12$. Complete brute-force semantics, rather than a
solver, cover the smallest regression boards in the retained unit suite.

Several $Q_{26}$ direct, exact-line, and supported-line formulations were then
run with Hilbert, domination-degree, line-bound, symmetry, and theorem-derived
variants. Bounded CaDiCaL runs reached 500,000 or 1,000,000 conflicts without a
model or an UNSAT result. A MapleChrono probe reached its wall-time cap, and the
available Windows Kissat binding exited before returning a status. Every one of
these outcomes is `UNKNOWN`; none is evidence that thirteen queens do not exist.
These are unretained engineering observations, not mechanically replayed runs.

This establishes a genuine engineering boundary: the next serious negative run
is a proof-producing, hash-frozen cube-and-conquer campaign, not a longer
uncertified retry. The positive branch remains open to exact or heuristic
discovery because any candidate is cheap to verify.

## Locally normalized fourteen-queen upper-bound witness

[`Q26_queen_domination_known_14.json`](Q26_queen_domination_known_14.json) is a
normalized JSON transcription of the coordinates in Dmitry Kamenetsky's linked
OEIS companion file; it is not claimed to preserve the source text's bytes. Its
coordinates are

$$
\begin{aligned}
&(2,6),(4,20),(6,10),(8,4),(10,16),(10,18),(12,24),\\
&(14,8),(16,14),(18,2),(20,12),(22,22),(24,26),(26,14).
\end{aligned}
$$

Both independent checkers confirm all 676 squares are dominated. The witness
proves only the upper bound; it is not evidence against thirteen queens.

## Required fail-closed checks

- A one-square witness mutation, duplicate, out-of-board coordinate, and a
  fourteenth queen under a thirteen-queen claim are rejected.
- `UNSAT`, `UNKNOWN`, contradictory literals, malformed records, and content
  after a DIMACS model terminator cannot be decoded as witnesses.
- Free line variables cannot satisfy either line mode without supporting queens.
- Separate cardinality circuits are exhaustive on small inputs, including the
  bidirectional lower-bound circuit.
- Direct CNF, both line modes, and direct OPB agree with brute-force board
  semantics on complete small cases.
- Symmetry and the line bound preserve those semantics.
- The monochromatic equation has no admissible Q26 solution.
- A solver timeout or unverified status remains `NOT_PROVED`.

## Scope boundary

This attack allocates no BSC claim identifier or fixture identifier. It does not
change the existing Collatz, electrostatic, electromagnetic, formal-kernel, or
release sequence. Search timings are hardware- and solver-dependent engineering
observations, not mathematical evidence. Public status must be rechecked before
any novelty or priority statement because this is an active computational
frontier.
