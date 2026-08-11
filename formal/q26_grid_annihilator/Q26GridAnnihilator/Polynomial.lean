import Q26GridAnnihilator.Basic
import Mathlib.LinearAlgebra.Lagrange

/-!
# Exact polynomial consequences on a two-dimensional grid

The first theorem below is the precise two-variable Combinatorial
Nullstellensatz step used in the Q26 argument.  It is stated independently of
the occurrence polynomial so that the coefficient calculation and the grid
logic have separate trust boundaries.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

def pairExponent (uDegree vDegree : Nat) : Fin 2 →₀ Nat :=
  Finsupp.single 0 uDegree + Finsupp.single 1 vDegree

@[simp] theorem pairExponent_zero (uDegree vDegree : Nat) :
    pairExponent uDegree vDegree 0 = uDegree := by
  simp [pairExponent]

@[simp] theorem pairExponent_one (uDegree vDegree : Nat) :
    pairExponent uDegree vDegree 1 = vDegree := by
  simp [pairExponent]

theorem pairExponent_degree (uDegree vDegree : Nat) :
    (pairExponent uDegree vDegree).degree = uDegree + vDegree := by
  rw [Finsupp.degree_eq_sum]
  simp [pairExponent, Fin.sum_univ_two]

def rationalPairPoint (u v : ℚ) : Fin 2 → ℚ :=
  fun index => if index = 0 then u else v

@[simp] theorem rationalPairPoint_zero (u v : ℚ) :
    rationalPairPoint u v 0 = u := by
  simp [rationalPairPoint]

@[simp] theorem rationalPairPoint_one (u v : ℚ) :
    rationalPairPoint u v 1 = v := by
  simp [rationalPairPoint]

/-- If a total-degree coefficient at `(m,n)` is nonzero, a polynomial that
vanishes on `A × B` cannot have both `|A| > m` and `|B| > n`. -/
theorem grid_cardinality_alternative
    (polynomial : Bivariate) (uDegree vDegree : Nat)
    (coefficientNonzero :
      MvPolynomial.coeff (pairExponent uDegree vDegree) polynomial ≠ 0)
    (totalDegreeExact : polynomial.totalDegree = uDegree + vDegree)
    (rows columns : Finset ℚ)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column) polynomial = 0) :
    rows.card ≤ uDegree ∨ columns.card ≤ vDegree := by
  by_contra bothTooLarge
  rw [not_or] at bothTooLarge
  have rowDegreeSmall : uDegree < rows.card := Nat.lt_of_not_ge bothTooLarge.1
  have columnDegreeSmall : vDegree < columns.card := Nat.lt_of_not_ge bothTooLarge.2
  let grid : Fin 2 → Finset ℚ :=
    fun index => if index = 0 then rows else columns
  have exponentSmall :
      ∀ index, pairExponent uDegree vDegree index < (grid index).card := by
    intro index
    fin_cases index
    · simpa [grid] using rowDegreeSmall
    · simpa [grid] using columnDegreeSmall
  have degreeExact :
      polynomial.totalDegree = (pairExponent uDegree vDegree).degree := by
    rw [pairExponent_degree]
    exact totalDegreeExact
  obtain ⟨point, pointInGrid, pointNonzero⟩ :=
    MvPolynomial.combinatorial_nullstellensatz_exists_eval_nonzero
      polynomial (pairExponent uDegree vDegree) coefficientNonzero degreeExact
      grid exponentSmall
  have pointRow : point 0 ∈ rows := by
    simpa [grid] using pointInGrid 0
  have pointColumn : point 1 ∈ columns := by
    simpa [grid] using pointInGrid 1
  apply pointNonzero
  have pointExt : rationalPairPoint (point 0) (point 1) = point := by
    funext index
    fin_cases index <;> simp
  rw [← pointExt]
  exact vanishes (point 0) pointRow (point 1) pointColumn

/-- The exact family of alternatives used for an occurrence polynomial with
`k` paired diagonal factors.  The algebraic caller supplies the standard
top coefficient and total-degree identities. -/
theorem occurrence_grid_alternatives
    (polynomial : Bivariate) (queenCount : Nat)
    (totalDegreeExact : polynomial.totalDegree = 2 * queenCount)
    (topCoefficients : ∀ j ≤ queenCount,
      MvPolynomial.coeff
          (pairExponent (2 * (queenCount - j)) (2 * j)) polynomial ≠ 0)
    (rows columns : Finset ℚ)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column) polynomial = 0) :
    ∀ j ≤ queenCount,
      rows.card ≤ 2 * (queenCount - j) ∨ columns.card ≤ 2 * j := by
  intro j hj
  apply grid_cardinality_alternative polynomial
      (2 * (queenCount - j)) (2 * j) (topCoefficients j hj)
  · omega
  · exact vanishes

end

end Q26GridAnnihilator
