import Q26GridAnnihilator.OccurrenceAlgebra

/-!
# Arbitrary-cardinality occurrence-polynomial grid bounds

This module removes the hard-coded cardinalities `6` and `7` from the leading
coefficient and Combinatorial Nullstellensatz layer.  In particular, its public
theorems include the empty queen set: the occurrence polynomial is then `1`,
and vanishing on a Cartesian grid forces at least one side of that grid to be
empty.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

private theorem quadratic_binomial_term
    (k m : Nat) :
    (U ^ 2) ^ m * (- (V ^ 2)) ^ (k - m) * (k.choose m : Bivariate) =
      MvPolynomial.monomial (pairExponent (2 * m) (2 * (k - m)))
        ((-1 : ℚ) ^ (k - m) * k.choose m) := by
  rw [monomial_pairExponent]
  have negPower :
      (- (V ^ 2)) ^ (k - m) =
        (-1 : Bivariate) ^ (k - m) * (V ^ 2) ^ (k - m) := by
    rw [neg_pow]
  rw [negPower]
  rw [← pow_mul, ← pow_mul]
  have signCast :
      (-1 : Bivariate) ^ (k - m) =
        MvPolynomial.C ((-1 : ℚ) ^ (k - m)) := by
    simp
  have chooseCast :
      (k.choose m : Bivariate) = MvPolynomial.C (k.choose m : ℚ) := by
    exact (MvPolynomial.C_eq_coe_nat (R := ℚ) (k.choose m)).symm
  rw [signCast, chooseCast, map_mul]
  ring

/-- The leading coefficient of `(U²-V²)^k`, uniformly for every natural
cardinality `k`, including `k = 0`. -/
theorem quadratic_pow_top_coefficient
    (k j : Nat) (hj : j ≤ k) :
    MvPolynomial.coeff (pairExponent (2 * (k - j)) (2 * j))
        (quadraticPart ^ k) =
      (-1 : ℚ) ^ j * Nat.choose k j := by
  rw [quadraticPart, sub_eq_add_neg, add_pow]
  simp_rw [quadratic_binomial_term]
  rw [MvPolynomial.coeff_sum]
  rw [Finset.sum_eq_single (k - j)]
  · rw [MvPolynomial.coeff_monomial]
    rw [if_pos]
    · rw [Nat.sub_sub_self hj, Nat.choose_symm hj]
    · apply congrArg₂ pairExponent
      · rfl
      · rw [Nat.sub_sub_self hj]
  · intro m hm hne
    rw [MvPolynomial.coeff_monomial, if_neg]
    intro exponentEqual
    have uEqual := congrArg (fun exponent : Fin 2 →₀ Nat => exponent 0) exponentEqual
    norm_num [pairExponent, Finsupp.single_apply] at uEqual
    have : m = k - j := by omega
    exact hne this
  · intro hnot
    exact False.elim (hnot (Finset.mem_range.mpr (by omega)))

/-- Every top-slice coefficient of an occurrence polynomial has its uniform
binomial value.  Unlike `coeff_occurrence_eq_top`, this statement includes the
empty queen set. -/
theorem occurrence_top_coefficient
    (queens : Finset Square) (j : Nat) (hj : j ≤ queens.card) :
    MvPolynomial.coeff
        (pairExponent (2 * (queens.card - j)) (2 * j))
        (occurrencePolynomial queens) =
      (-1 : ℚ) ^ j * Nat.choose queens.card j := by
  by_cases queensEmpty : queens = ∅
  · subst queens
    have jZero : j = 0 := by simpa using hj
    subst j
    simp [occurrencePolynomial, pairExponent]
  · calc
      MvPolynomial.coeff
          (pairExponent (2 * (queens.card - j)) (2 * j))
          (occurrencePolynomial queens) =
          MvPolynomial.coeff
            (pairExponent (2 * (queens.card - j)) (2 * j))
            (topApproximation queens) := by
        apply coeff_occurrence_eq_top queens
          (Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr queensEmpty))
        rw [pairExponent_degree]
        omega
      _ = MvPolynomial.coeff
            (pairExponent (2 * (queens.card - j)) (2 * j))
            (quadraticPart ^ queens.card) := by
        simp [topApproximation]
      _ = (-1 : ℚ) ^ j * Nat.choose queens.card j :=
        quadratic_pow_top_coefficient queens.card j hj

/-- The occurrence polynomial always has its expected total degree, including
degree zero for the empty product. -/
theorem occurrence_totalDegree (queens : Finset Square) :
    (occurrencePolynomial queens).totalDegree = 2 * queens.card := by
  apply le_antisymm
  · exact occurrencePolynomial_totalDegree_le queens
  · have coefficientNonzero :
        MvPolynomial.coeff (pairExponent (2 * queens.card) 0)
            (occurrencePolynomial queens) ≠ 0 := by
      have coefficient := occurrence_top_coefficient queens 0 (Nat.zero_le _)
      norm_num at coefficient
      rw [coefficient]
      norm_num
    have inSupport :
        pairExponent (2 * queens.card) 0 ∈
          (occurrencePolynomial queens).support :=
      MvPolynomial.mem_support_iff.mpr coefficientNonzero
    have lower := MvPolynomial.le_totalDegree inSupport
    change (pairExponent (2 * queens.card) 0).degree ≤
      (occurrencePolynomial queens).totalDegree at lower
    simpa [pairExponent_degree] using lower

/-- The arbitrary-cardinality color-grid obstruction `G_k(a,b)`.  For `k = 0`
the sole case `j = 0` says that at least one grid side has cardinality zero. -/
theorem occurrence_grid_alternatives_card
    (queens : Finset Square) (rows columns : Finset ℚ)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column)
        (occurrencePolynomial queens) = 0) :
    ∀ j ≤ queens.card,
      rows.card ≤ 2 * (queens.card - j) ∨ columns.card ≤ 2 * j := by
  apply occurrence_grid_alternatives
      (occurrencePolynomial queens) queens.card
  · exact occurrence_totalDegree queens
  · intro j hj
    rw [occurrence_top_coefficient queens j hj]
    apply mul_ne_zero
    · exact pow_ne_zero _ (by norm_num)
    · exact_mod_cast (Nat.choose_pos hj).ne'
  · exact vanishes

end

end Q26GridAnnihilator
