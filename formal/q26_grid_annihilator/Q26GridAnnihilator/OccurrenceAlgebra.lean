import Q26GridAnnihilator.Polynomial

/-!
# The top two homogeneous layers of the occurrence product

The paired factor belonging to `(r,c)` is

`U² - V² + (-2r U + 2c V) + (r² - c²)`.

This file isolates that exact algebra.  The factors are indexed by queen
occurrences, so no diagonal-label distinctness is present or needed.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

def quadraticPart : Bivariate := U ^ 2 - V ^ 2

def rowLinearPart (queen : Square) : Bivariate :=
  -(MvPolynomial.C (rationalCoord queen.1) * U) -
    MvPolynomial.C (rationalCoord queen.1) * U

def columnLinearPart (queen : Square) : Bivariate :=
  MvPolynomial.C (rationalCoord queen.2) * V +
    MvPolynomial.C (rationalCoord queen.2) * V

def linearPart (queen : Square) : Bivariate :=
  rowLinearPart queen + columnLinearPart queen

def constantPart (queen : Square) : Bivariate :=
  MvPolynomial.C
    (rationalCoord queen.1 ^ 2 - rationalCoord queen.2 ^ 2)

def lowerPart (queen : Square) : Bivariate :=
  linearPart queen + constantPart queen

theorem occurrenceFactor_decomposition (queen : Square) :
    occurrenceFactor queen = quadraticPart + linearPart queen + constantPart queen := by
  simp [occurrenceFactor, quadraticPart, linearPart, rowLinearPart,
    columnLinearPart, constantPart, U, V]
  ring

theorem occurrenceFactor_eq_quadratic_add_lower (queen : Square) :
    occurrenceFactor queen = quadraticPart + lowerPart queen := by
  rw [occurrenceFactor_decomposition]
  simp [lowerPart, add_assoc]

theorem quadraticPart_totalDegree_le : quadraticPart.totalDegree ≤ 2 := by
  calc
    quadraticPart.totalDegree ≤
        max (U ^ 2).totalDegree (V ^ 2).totalDegree := by
      exact MvPolynomial.totalDegree_sub _ _
    _ = 2 := by simp [U, V]

theorem linearPart_totalDegree_le (queen : Square) :
    (linearPart queen).totalDegree ≤ 1 := by
  have rowTerm :
      (MvPolynomial.C (rationalCoord queen.1) * U : Bivariate).totalDegree ≤ 1 := by
    calc
      (MvPolynomial.C (rationalCoord queen.1) * U : Bivariate).totalDegree ≤
          (MvPolynomial.C (rationalCoord queen.1) : Bivariate).totalDegree +
            U.totalDegree := MvPolynomial.totalDegree_mul _ _
      _ = 1 := by simp [U]
  have columnTerm :
      (MvPolynomial.C (rationalCoord queen.2) * V : Bivariate).totalDegree ≤ 1 := by
    calc
      (MvPolynomial.C (rationalCoord queen.2) * V : Bivariate).totalDegree ≤
          (MvPolynomial.C (rationalCoord queen.2) : Bivariate).totalDegree +
            V.totalDegree := MvPolynomial.totalDegree_mul _ _
      _ = 1 := by simp [V]
  have rowPart : (rowLinearPart queen).totalDegree ≤ 1 := by
    unfold rowLinearPart
    exact (MvPolynomial.totalDegree_sub _ _).trans
      (max_le ((MvPolynomial.totalDegree_neg _).le.trans rowTerm) rowTerm)
  have columnPart : (columnLinearPart queen).totalDegree ≤ 1 := by
    unfold columnLinearPart
    exact (MvPolynomial.totalDegree_add _ _).trans (max_le columnTerm columnTerm)
  calc
    (linearPart queen).totalDegree ≤
        max (rowLinearPart queen).totalDegree
          (columnLinearPart queen).totalDegree := by
      exact MvPolynomial.totalDegree_add _ _
    _ ≤ 1 := max_le rowPart columnPart

theorem constantPart_totalDegree_le (queen : Square) :
    (constantPart queen).totalDegree ≤ 0 := by
  unfold constantPart
  exact (MvPolynomial.totalDegree_C _).le

theorem lowerPart_totalDegree_le (queen : Square) :
    (lowerPart queen).totalDegree ≤ 1 := by
  calc
    (lowerPart queen).totalDegree ≤
        max (linearPart queen).totalDegree (constantPart queen).totalDegree := by
      exact MvPolynomial.totalDegree_add _ _
    _ ≤ 1 := by
      exact max_le (linearPart_totalDegree_le queen)
        ((constantPart_totalDegree_le queen).trans (by omega))

theorem occurrenceFactor_totalDegree_le (queen : Square) :
    (occurrenceFactor queen).totalDegree ≤ 2 := by
  rw [occurrenceFactor_eq_quadratic_add_lower]
  exact (MvPolynomial.totalDegree_add _ _).trans
    (max_le quadraticPart_totalDegree_le
      ((lowerPart_totalDegree_le queen).trans (by omega)))

theorem occurrencePolynomial_totalDegree_le (queens : Finset Square) :
    (occurrencePolynomial queens).totalDegree ≤ 2 * queens.card := by
  rw [occurrencePolynomial]
  calc
    (∏ queen ∈ queens, occurrenceFactor queen).totalDegree ≤
        ∑ queen ∈ queens, (occurrenceFactor queen).totalDegree := by
      exact MvPolynomial.totalDegree_finsetProd queens occurrenceFactor
    _ ≤ ∑ _queen ∈ queens, 2 := by
      exact Finset.sum_le_sum fun queen _ => occurrenceFactor_totalDegree_le queen
    _ = 2 * queens.card := by simp [mul_comm]

def linearSum (queens : Finset Square) : Bivariate :=
  ∑ queen ∈ queens, linearPart queen

def topApproximation (queens : Finset Square) : Bivariate :=
  quadraticPart ^ queens.card

def topTwoApproximation (queens : Finset Square) : Bivariate :=
  quadraticPart ^ queens.card +
    linearSum queens * quadraticPart ^ (queens.card - 1)

/-- All monomials omitted by the leading homogeneous approximation have
total degree at most `2|Q|-1`. -/
theorem top_error_totalDegree_le (queens : Finset Square) :
    (occurrencePolynomial queens - topApproximation queens).totalDegree ≤
      2 * queens.card - 1 := by
  classical
  induction queens using Finset.induction_on with
  | empty => simp [occurrencePolynomial, topApproximation]
  | @insert queen queens hqueen ih =>
      by_cases hqueensEmpty : queens = ∅
      · subst queens
        have identity :
            occurrencePolynomial (insert queen ∅) -
                topApproximation (insert queen ∅) =
              lowerPart queen := by
          simp [occurrencePolynomial, topApproximation,
            occurrenceFactor_eq_quadratic_add_lower]
        rw [identity]
        simpa using lowerPart_totalDegree_le queen
      · have cardPositive : 0 < queens.card :=
          Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hqueensEmpty)
        have identity :
            occurrencePolynomial (insert queen queens) -
                topApproximation (insert queen queens) =
              (occurrencePolynomial queens - topApproximation queens) * quadraticPart +
                occurrencePolynomial queens * lowerPart queen := by
          simp only [occurrencePolynomial, topApproximation,
            Finset.prod_insert hqueen, Finset.card_insert_of_notMem hqueen,
            occurrenceFactor_eq_quadratic_add_lower, pow_succ]
          ring
        rw [identity]
        apply (MvPolynomial.totalDegree_add _ _).trans
        apply max_le
        · calc
            ((occurrencePolynomial queens - topApproximation queens) *
                quadraticPart).totalDegree ≤
                (occurrencePolynomial queens - topApproximation queens).totalDegree +
                  quadraticPart.totalDegree := MvPolynomial.totalDegree_mul _ _
            _ ≤ (2 * queens.card - 1) + 2 :=
              Nat.add_le_add ih quadraticPart_totalDegree_le
            _ ≤ 2 * (insert queen queens).card - 1 := by
              rw [Finset.card_insert_of_notMem hqueen]
              omega
        · calc
            (occurrencePolynomial queens * lowerPart queen).totalDegree ≤
                (occurrencePolynomial queens).totalDegree +
                  (lowerPart queen).totalDegree := MvPolynomial.totalDegree_mul _ _
            _ ≤ 2 * queens.card + 1 :=
              Nat.add_le_add (occurrencePolynomial_totalDegree_le queens)
                (lowerPart_totalDegree_le queen)
            _ ≤ 2 * (insert queen queens).card - 1 := by
              rw [Finset.card_insert_of_notMem hqueen]
              omega

/-- After subtracting both displayed homogeneous layers, only total degree
`2|Q|-2` or lower remains. -/
theorem topTwo_error_totalDegree_le (queens : Finset Square) :
    (occurrencePolynomial queens - topTwoApproximation queens).totalDegree ≤
      2 * queens.card - 2 := by
  classical
  induction queens using Finset.induction_on with
  | empty => simp [occurrencePolynomial, topTwoApproximation, linearSum]
  | @insert queen queens hqueen ih =>
      by_cases hqueensEmpty : queens = ∅
      · subst queens
        have identity :
            occurrencePolynomial (insert queen ∅) -
                topTwoApproximation (insert queen ∅) =
              constantPart queen := by
          simp [occurrencePolynomial, topTwoApproximation, linearSum,
            occurrenceFactor_decomposition]
        rw [identity]
        simpa using constantPart_totalDegree_le queen
      · have cardPositive : 0 < queens.card :=
          Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hqueensEmpty)
        have powerRelation :
            quadraticPart ^ (queens.card - 1) * quadraticPart =
              quadraticPart ^ queens.card := by
          calc
            quadraticPart ^ (queens.card - 1) * quadraticPart =
                quadraticPart ^ ((queens.card - 1) + 1) := by
              rw [pow_succ]
            _ = quadraticPart ^ queens.card := by
              congr
              omega
        have powerRelationLeft :
            quadraticPart * quadraticPart ^ (queens.card - 1) =
              quadraticPart ^ queens.card := by
          rw [mul_comm, powerRelation]
        have identity :
            occurrencePolynomial (insert queen queens) -
                topTwoApproximation (insert queen queens) =
              (occurrencePolynomial queens - topTwoApproximation queens) * quadraticPart +
                (occurrencePolynomial queens - topApproximation queens) * linearPart queen +
                occurrencePolynomial queens * constantPart queen := by
          simp only [occurrencePolynomial, topTwoApproximation, topApproximation,
            linearSum, Finset.prod_insert hqueen, Finset.sum_insert hqueen,
            Finset.card_insert_of_notMem hqueen, occurrenceFactor_decomposition,
            pow_succ, Nat.add_sub_cancel]
          ring_nf
          rw [powerRelationLeft]
          ring
        rw [identity]
        apply (MvPolynomial.totalDegree_add _ _).trans
        apply max_le
        · apply (MvPolynomial.totalDegree_add _ _).trans
          apply max_le
          · calc
              ((occurrencePolynomial queens - topTwoApproximation queens) *
                  quadraticPart).totalDegree ≤
                  (occurrencePolynomial queens - topTwoApproximation queens).totalDegree +
                    quadraticPart.totalDegree := MvPolynomial.totalDegree_mul _ _
              _ ≤ (2 * queens.card - 2) + 2 :=
                Nat.add_le_add ih quadraticPart_totalDegree_le
              _ ≤ 2 * (insert queen queens).card - 2 := by
                rw [Finset.card_insert_of_notMem hqueen]
                omega
          · calc
              ((occurrencePolynomial queens - topApproximation queens) *
                  linearPart queen).totalDegree ≤
                  (occurrencePolynomial queens - topApproximation queens).totalDegree +
                    (linearPart queen).totalDegree := MvPolynomial.totalDegree_mul _ _
              _ ≤ (2 * queens.card - 1) + 1 :=
                Nat.add_le_add (top_error_totalDegree_le queens)
                  (linearPart_totalDegree_le queen)
              _ ≤ 2 * (insert queen queens).card - 2 := by
                rw [Finset.card_insert_of_notMem hqueen]
                omega
        · calc
            (occurrencePolynomial queens * constantPart queen).totalDegree ≤
                (occurrencePolynomial queens).totalDegree +
                  (constantPart queen).totalDegree := MvPolynomial.totalDegree_mul _ _
            _ ≤ 2 * queens.card + 0 :=
              Nat.add_le_add (occurrencePolynomial_totalDegree_le queens)
                (constantPart_totalDegree_le queen)
            _ ≤ 2 * (insert queen queens).card - 2 := by
              rw [Finset.card_insert_of_notMem hqueen]
              omega

/-- Every coefficient on the top total-degree slice is exactly the
corresponding coefficient of `(U²-V²)^|Q|`. -/
theorem coeff_occurrence_eq_top
    (queens : Finset Square) (cardPositive : 0 < queens.card)
    (exponent : Fin 2 →₀ Nat)
    (exponentDegree : exponent.degree = 2 * queens.card) :
    MvPolynomial.coeff exponent (occurrencePolynomial queens) =
      MvPolynomial.coeff exponent (topApproximation queens) := by
  have errorCoefficientZero :
    MvPolynomial.coeff exponent
          (occurrencePolynomial queens - topApproximation queens) = 0 := by
    apply MvPolynomial.coeff_eq_zero_of_totalDegree_lt
    change (occurrencePolynomial queens - topApproximation queens).totalDegree <
      exponent.degree
    rw [exponentDegree]
    exact (top_error_totalDegree_le queens).trans_lt (by omega)
  simpa only [MvPolynomial.coeff_sub, sub_eq_zero] using errorCoefficientZero

/-- Every coefficient on the next total-degree slice is exactly the
corresponding coefficient of the displayed top-two approximation. -/
theorem coeff_occurrence_eq_topTwo
    (queens : Finset Square) (cardPositive : 0 < queens.card)
    (exponent : Fin 2 →₀ Nat)
    (exponentDegree : exponent.degree = 2 * queens.card - 1) :
    MvPolynomial.coeff exponent (occurrencePolynomial queens) =
      MvPolynomial.coeff exponent (topTwoApproximation queens) := by
  have errorCoefficientZero :
    MvPolynomial.coeff exponent
          (occurrencePolynomial queens - topTwoApproximation queens) = 0 := by
    apply MvPolynomial.coeff_eq_zero_of_totalDegree_lt
    change (occurrencePolynomial queens - topTwoApproximation queens).totalDegree <
      exponent.degree
    rw [exponentDegree]
    exact (topTwo_error_totalDegree_le queens).trans_lt (by omega)
  simpa only [MvPolynomial.coeff_sub, sub_eq_zero] using errorCoefficientZero

theorem monomial_pairExponent (uDegree vDegree : Nat) (coefficient : ℚ) :
    MvPolynomial.monomial (pairExponent uDegree vDegree) coefficient =
      MvPolynomial.C coefficient * U ^ uDegree * V ^ vDegree := by
  rw [pairExponent, MvPolynomial.monomial_add_single,
    ← MvPolynomial.C_mul_X_pow_eq_monomial]
  rfl

theorem quadratic_pow_six_top_coefficient (j : Nat) (hj : j ≤ 6) :
    MvPolynomial.coeff (pairExponent (2 * (6 - j)) (2 * j))
        (quadraticPart ^ 6) =
      (-1 : ℚ) ^ j * Nat.choose 6 j := by
  have expansion :
      quadraticPart ^ 6 =
        MvPolynomial.monomial (pairExponent 12 0) (1 : ℚ) +
        MvPolynomial.monomial (pairExponent 10 2) (-6 : ℚ) +
        MvPolynomial.monomial (pairExponent 8 4) (15 : ℚ) +
        MvPolynomial.monomial (pairExponent 6 6) (-20 : ℚ) +
        MvPolynomial.monomial (pairExponent 4 8) (15 : ℚ) +
        MvPolynomial.monomial (pairExponent 2 10) (-6 : ℚ) +
        MvPolynomial.monomial (pairExponent 0 12) (1 : ℚ) := by
    have c6 : MvPolynomial.C (6 : ℚ) = (6 : Bivariate) := by
      change MvPolynomial.C ((6 : Nat) : ℚ) = (6 : Bivariate)
      exact MvPolynomial.C_eq_coe_nat 6
    have c15 : MvPolynomial.C (15 : ℚ) = (15 : Bivariate) := by
      change MvPolynomial.C ((15 : Nat) : ℚ) = (15 : Bivariate)
      exact MvPolynomial.C_eq_coe_nat 15
    have c20 : MvPolynomial.C (20 : ℚ) = (20 : Bivariate) := by
      change MvPolynomial.C ((20 : Nat) : ℚ) = (20 : Bivariate)
      exact MvPolynomial.C_eq_coe_nat 20
    simp only [quadraticPart, monomial_pairExponent, pow_zero, mul_one]
    simp only [map_neg]
    rw [MvPolynomial.C_1, c6, c15, c20]
    ring
  rw [expansion]
  have cases : j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 ∨ j = 5 ∨ j = 6 := by
    omega
  rcases cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    norm_num [pairExponent, MvPolynomial.coeff_add,
      MvPolynomial.coeff_monomial, Finsupp.ext_iff, Fin.forall_fin_two,
      Nat.choose]

theorem quadratic_pow_seven_top_coefficient (j : Nat) (hj : j ≤ 7) :
    MvPolynomial.coeff (pairExponent (2 * (7 - j)) (2 * j))
        (quadraticPart ^ 7) =
      (-1 : ℚ) ^ j * Nat.choose 7 j := by
  have expansion :
      quadraticPart ^ 7 =
        MvPolynomial.monomial (pairExponent 14 0) (1 : ℚ) +
        MvPolynomial.monomial (pairExponent 12 2) (-7 : ℚ) +
        MvPolynomial.monomial (pairExponent 10 4) (21 : ℚ) +
        MvPolynomial.monomial (pairExponent 8 6) (-35 : ℚ) +
        MvPolynomial.monomial (pairExponent 6 8) (35 : ℚ) +
        MvPolynomial.monomial (pairExponent 4 10) (-21 : ℚ) +
        MvPolynomial.monomial (pairExponent 2 12) (7 : ℚ) +
        MvPolynomial.monomial (pairExponent 0 14) (-1 : ℚ) := by
    have c7 : MvPolynomial.C (7 : ℚ) = (7 : Bivariate) := by
      change MvPolynomial.C ((7 : Nat) : ℚ) = (7 : Bivariate)
      exact MvPolynomial.C_eq_coe_nat 7
    have c21 : MvPolynomial.C (21 : ℚ) = (21 : Bivariate) := by
      change MvPolynomial.C ((21 : Nat) : ℚ) = (21 : Bivariate)
      exact MvPolynomial.C_eq_coe_nat 21
    have c35 : MvPolynomial.C (35 : ℚ) = (35 : Bivariate) := by
      change MvPolynomial.C ((35 : Nat) : ℚ) = (35 : Bivariate)
      exact MvPolynomial.C_eq_coe_nat 35
    simp only [quadraticPart, monomial_pairExponent, pow_zero, mul_one]
    simp only [map_neg]
    rw [MvPolynomial.C_1, c7, c21, c35]
    ring
  rw [expansion]
  have cases :
      j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 ∨ j = 5 ∨ j = 6 ∨ j = 7 := by
    omega
  rcases cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    norm_num [pairExponent, MvPolynomial.coeff_add,
      MvPolynomial.coeff_monomial, Finsupp.ext_iff, Fin.forall_fin_two,
      Nat.choose]

theorem occurrence_six_top_coefficient
    (queens : Finset Square) (cardExact : queens.card = 6)
    (j : Nat) (hj : j ≤ 6) :
    MvPolynomial.coeff (pairExponent (2 * (6 - j)) (2 * j))
        (occurrencePolynomial queens) =
      (-1 : ℚ) ^ j * Nat.choose 6 j := by
  calc
    MvPolynomial.coeff (pairExponent (2 * (6 - j)) (2 * j))
        (occurrencePolynomial queens) =
        MvPolynomial.coeff (pairExponent (2 * (6 - j)) (2 * j))
          (topApproximation queens) := by
            apply coeff_occurrence_eq_top queens (by omega)
            rw [pairExponent_degree, cardExact]
            omega
    _ = MvPolynomial.coeff (pairExponent (2 * (6 - j)) (2 * j))
          (quadraticPart ^ 6) := by simp [topApproximation, cardExact]
    _ = (-1 : ℚ) ^ j * Nat.choose 6 j :=
      quadratic_pow_six_top_coefficient j hj

theorem occurrence_seven_top_coefficient
    (queens : Finset Square) (cardExact : queens.card = 7)
    (j : Nat) (hj : j ≤ 7) :
    MvPolynomial.coeff (pairExponent (2 * (7 - j)) (2 * j))
        (occurrencePolynomial queens) =
      (-1 : ℚ) ^ j * Nat.choose 7 j := by
  calc
    MvPolynomial.coeff (pairExponent (2 * (7 - j)) (2 * j))
        (occurrencePolynomial queens) =
        MvPolynomial.coeff (pairExponent (2 * (7 - j)) (2 * j))
          (topApproximation queens) := by
            apply coeff_occurrence_eq_top queens (by omega)
            rw [pairExponent_degree, cardExact]
            omega
    _ = MvPolynomial.coeff (pairExponent (2 * (7 - j)) (2 * j))
          (quadraticPart ^ 7) := by simp [topApproximation, cardExact]
    _ = (-1 : ℚ) ^ j * Nat.choose 7 j :=
      quadratic_pow_seven_top_coefficient j hj

theorem occurrence_six_totalDegree
    (queens : Finset Square) (cardExact : queens.card = 6) :
    (occurrencePolynomial queens).totalDegree = 12 := by
  apply le_antisymm
  · simpa [cardExact] using occurrencePolynomial_totalDegree_le queens
  · have coefficientNonzero :
        MvPolynomial.coeff (pairExponent 12 0)
            (occurrencePolynomial queens) ≠ 0 := by
      have coefficient := occurrence_six_top_coefficient queens cardExact 0 (by omega)
      norm_num at coefficient
      rw [coefficient]
      norm_num
    have inSupport :
        pairExponent 12 0 ∈ (occurrencePolynomial queens).support :=
      MvPolynomial.mem_support_iff.mpr coefficientNonzero
    have lower := MvPolynomial.le_totalDegree inSupport
    change (pairExponent 12 0).degree ≤
      (occurrencePolynomial queens).totalDegree at lower
    simpa [pairExponent_degree] using lower

theorem occurrence_seven_totalDegree
    (queens : Finset Square) (cardExact : queens.card = 7) :
    (occurrencePolynomial queens).totalDegree = 14 := by
  apply le_antisymm
  · simpa [cardExact] using occurrencePolynomial_totalDegree_le queens
  · have coefficientNonzero :
        MvPolynomial.coeff (pairExponent 14 0)
            (occurrencePolynomial queens) ≠ 0 := by
      have coefficient := occurrence_seven_top_coefficient queens cardExact 0 (by omega)
      norm_num at coefficient
      rw [coefficient]
      norm_num
    have inSupport :
        pairExponent 14 0 ∈ (occurrencePolynomial queens).support :=
      MvPolynomial.mem_support_iff.mpr coefficientNonzero
    have lower := MvPolynomial.le_totalDegree inSupport
    change (pairExponent 14 0).degree ≤
      (occurrencePolynomial queens).totalDegree at lower
    simpa [pairExponent_degree] using lower

theorem occurrence_six_grid_alternatives
    (queens : Finset Square) (cardExact : queens.card = 6)
    (rows columns : Finset ℚ)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column)
        (occurrencePolynomial queens) = 0) :
    ∀ j ≤ 6, rows.card ≤ 2 * (6 - j) ∨ columns.card ≤ 2 * j := by
  apply occurrence_grid_alternatives (occurrencePolynomial queens) 6
  · simpa using occurrence_six_totalDegree queens cardExact
  · intro j hj
    rw [occurrence_six_top_coefficient queens cardExact j hj]
    apply mul_ne_zero
    · exact pow_ne_zero _ (by norm_num)
    · exact_mod_cast (Nat.choose_pos hj).ne'
  · exact vanishes

theorem occurrence_seven_grid_alternatives
    (queens : Finset Square) (cardExact : queens.card = 7)
    (rows columns : Finset ℚ)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column)
        (occurrencePolynomial queens) = 0) :
    ∀ j ≤ 7, rows.card ≤ 2 * (7 - j) ∨ columns.card ≤ 2 * j := by
  apply occurrence_grid_alternatives (occurrencePolynomial queens) 7
  · simpa using occurrence_seven_totalDegree queens cardExact
  · intro j hj
    rw [occurrence_seven_top_coefficient queens cardExact j hj]
    apply mul_ne_zero
    · exact pow_ne_zero _ (by norm_num)
    · exact_mod_cast (Nat.choose_pos hj).ne'
  · exact vanishes

end

end Q26GridAnnihilator
