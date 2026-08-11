import Q26GridAnnihilator.OccurrenceAlgebra

/-!
# Coordinate sums in the next homogeneous layer

The next-to-leading part of the occurrence product depends only on the sums
of the row and column coordinates of the indexed queen occurrences.  This
module records that identity without any distinct-diagonal hypothesis.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

def queenRowSum (queens : Finset Square) : ℚ :=
  ∑ queen ∈ queens, rationalCoord queen.1

def queenColumnSum (queens : Finset Square) : ℚ :=
  ∑ queen ∈ queens, rationalCoord queen.2

theorem linearSum_eq_coordinate_sums (queens : Finset Square) :
    linearSum queens =
      MvPolynomial.C (-2 * queenRowSum queens) * U +
        MvPolynomial.C (2 * queenColumnSum queens) * V := by
  classical
  induction queens using Finset.induction_on with
  | empty =>
      simp [linearSum, queenRowSum, queenColumnSum]
  | @insert queen queens queenNotIn tail =>
      rw [linearSum, Finset.sum_insert queenNotIn]
      change linearPart queen + linearSum queens = _
      rw [tail]
      simp only [queenRowSum, queenColumnSum, Finset.sum_insert queenNotIn]
      simp [linearPart, rowLinearPart, columnLinearPart]
      have c2 : MvPolynomial.C (2 : ℚ) = (2 : Bivariate) := by
        change MvPolynomial.C ((2 : Nat) : ℚ) = (2 : Bivariate)
        exact MvPolynomial.C_eq_coe_nat 2
      rw [c2]
      ring

theorem topTwoApproximation_eq_coordinate_sums (queens : Finset Square) :
    topTwoApproximation queens =
      quadraticPart ^ queens.card +
        (MvPolynomial.C (-2 * queenRowSum queens) * U +
          MvPolynomial.C (2 * queenColumnSum queens) * V) *
            quadraticPart ^ (queens.card - 1) := by
  simp [topTwoApproximation, linearSum_eq_coordinate_sums]

end

end Q26GridAnnihilator
