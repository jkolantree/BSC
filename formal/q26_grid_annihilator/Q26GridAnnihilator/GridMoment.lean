import Q26GridAnnihilator.MomentAlgebra
import Mathlib.LinearAlgebra.Lagrange

/-!
# The tensor Lagrange functional and equality moments

This file formalizes the coefficient-descent step behind the Q26 moment
equalities.  It uses exact rational arithmetic throughout.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

noncomputable section

def powerFunctional (nodes : Finset ℚ) (power : Nat) : ℚ :=
  ∑ node ∈ nodes,
    node ^ power / ∏ other ∈ nodes.erase node, (node - other)

theorem powerFunctional_of_lt_card
    (nodes : Finset ℚ) (power : Nat) (powerSmall : power < nodes.card) :
    powerFunctional nodes power = if power = nodes.card - 1 then 1 else 0 := by
  have degreeSmall :
      ((Polynomial.X : Polynomial ℚ) ^ power).degree < nodes.card := by
    rw [Polynomial.degree_X_pow]
    exact_mod_cast powerSmall
  have coefficientFormula :=
    Lagrange.coeff_eq_sum
      (s := nodes) (v := fun value : ℚ => value)
      (P := (Polynomial.X : Polynomial ℚ) ^ power)
      Function.injective_id.injOn degreeSmall
  calc
    powerFunctional nodes power =
        ((Polynomial.X : Polynomial ℚ) ^ power).coeff (nodes.card - 1) := by
      rw [coefficientFormula]
      simp [powerFunctional]
    _ = if power = nodes.card - 1 then 1 else 0 := by
      simp [Polynomial.coeff_X_pow, eq_comm]

theorem nodal_nextCoeff_eq_neg_sum (nodes : Finset ℚ) :
    (Lagrange.nodal nodes (fun value : ℚ => value)).nextCoeff =
      -(∑ value ∈ nodes, value) := by
  rw [Lagrange.nodal_eq]
  rw [Polynomial.Monic.nextCoeff_prod nodes
    (fun value : ℚ => Polynomial.X - Polynomial.C value)]
  · simp only [Polynomial.nextCoeff_X_sub_C]
    rw [Finset.sum_neg_distrib]
  · intro value _
    exact Polynomial.monic_X_sub_C value

theorem powerFunctional_card (nodes : Finset ℚ) (nodesNonempty : nodes.Nonempty) :
    powerFunctional nodes nodes.card = ∑ value ∈ nodes, value := by
  let nodal : Polynomial ℚ := Lagrange.nodal nodes (fun value : ℚ => value)
  let reduced : Polynomial ℚ := Polynomial.X ^ nodes.card - nodal
  have cardPositive : 0 < nodes.card := Finset.card_pos.mpr nodesNonempty
  have degreePower :
      ((Polynomial.X : Polynomial ℚ) ^ nodes.card).degree = nodes.card := by
    rw [Polynomial.degree_X_pow]
  have degreeNodal : nodal.degree = nodes.card := by
    simp [nodal]
  have leadingCoefficientEqual :
      ((Polynomial.X : Polynomial ℚ) ^ nodes.card).leadingCoeff =
        nodal.leadingCoeff := by
    have nodalMonic : nodal.Monic := by
      simpa [nodal] using
        (Lagrange.nodal_monic (s := nodes) (v := fun value : ℚ => value))
    rw [Polynomial.leadingCoeff_X_pow, nodalMonic.leadingCoeff]
  have powerNonzero :
      (Polynomial.X : Polynomial ℚ) ^ nodes.card ≠ 0 :=
    pow_ne_zero _ Polynomial.X_ne_zero
  have reducedDegreeSmall : reduced.degree < nodes.card := by
    unfold reduced
    have strict := Polynomial.degree_sub_lt
      (degreePower.trans degreeNodal.symm) powerNonzero leadingCoefficientEqual
    rw [degreePower] at strict
    exact strict
  have coefficientFormula :=
    Lagrange.coeff_eq_sum
      (s := nodes) (v := fun value : ℚ => value)
      (P := reduced) Function.injective_id.injOn reducedDegreeSmall
  have functionalEqualsCoefficient :
      powerFunctional nodes nodes.card = reduced.coeff (nodes.card - 1) := by
    rw [coefficientFormula]
    unfold powerFunctional
    apply Finset.sum_congr rfl
    intro value valueInNodes
    have nodalEval : nodal.eval value = 0 := by
      unfold nodal
      exact Lagrange.eval_nodal_at_node
        (s := nodes) (v := fun node : ℚ => node) (i := value) valueInNodes
    rw [show reduced.eval value = value ^ nodes.card by
      simp [reduced, nodalEval]]
  rw [functionalEqualsCoefficient]
  have nodalNatDegree : nodal.natDegree = nodes.card := by
    simp [nodal]
  have nodalCoefficient :
      nodal.coeff (nodes.card - 1) = -(∑ value ∈ nodes, value) := by
    rw [← nodalNatDegree, ← Polynomial.nextCoeff_of_natDegree_pos]
    · simpa [nodal] using nodal_nextCoeff_eq_neg_sum nodes
    · rw [nodalNatDegree]
      exact cardPositive
  unfold reduced
  rw [Polynomial.coeff_sub, nodalCoefficient]
  have precedingNe : nodes.card - 1 ≠ nodes.card := by omega
  simp [Polynomial.coeff_X_pow, precedingNe]

def nodeWeight (nodes : Finset ℚ) (node : ℚ) : ℚ :=
  (∏ other ∈ nodes.erase node, (node - other))⁻¹

def gridFunctional (rows columns : Finset ℚ) (polynomial : Bivariate) : ℚ :=
  ∑ row ∈ rows, ∑ column ∈ columns,
    nodeWeight rows row * nodeWeight columns column *
      MvPolynomial.eval (rationalPairPoint row column) polynomial

theorem finTwoExponent_eq_pairExponent (exponent : Fin 2 →₀ Nat) :
    exponent = pairExponent (exponent 0) (exponent 1) := by
  ext index
  fin_cases index <;> simp

theorem gridFunctional_monomial
    (rows columns : Finset ℚ) (exponent : Fin 2 →₀ Nat)
    (coefficient : ℚ) :
    gridFunctional rows columns (MvPolynomial.monomial exponent coefficient) =
      coefficient * powerFunctional rows (exponent 0) *
        powerFunctional columns (exponent 1) := by
  have monomialIdentity :
      MvPolynomial.monomial exponent coefficient =
        MvPolynomial.C coefficient * U ^ exponent 0 * V ^ exponent 1 := by
    calc
      MvPolynomial.monomial exponent coefficient =
          MvPolynomial.monomial
            (pairExponent (exponent 0) (exponent 1)) coefficient := by
        exact congrArg (fun powers => MvPolynomial.monomial powers coefficient)
          (finTwoExponent_eq_pairExponent exponent)
      _ = MvPolynomial.C coefficient * U ^ exponent 0 * V ^ exponent 1 :=
        monomial_pairExponent (exponent 0) (exponent 1) coefficient
  rw [monomialIdentity]
  unfold gridFunctional powerFunctional nodeWeight
  simp only [MvPolynomial.eval_mul, MvPolynomial.eval_C, MvPolynomial.eval_pow,
    U, V, MvPolynomial.eval_X, rationalPairPoint_zero, rationalPairPoint_one,
    div_eq_mul_inv]
  symm
  calc
    coefficient *
          (∑ row ∈ rows,
            row ^ exponent 0 *
              (∏ other ∈ rows.erase row, (row - other))⁻¹) *
        (∑ column ∈ columns,
          column ^ exponent 1 *
            (∏ other ∈ columns.erase column, (column - other))⁻¹) =
        coefficient *
          (∑ row ∈ rows, ∑ column ∈ columns,
            (row ^ exponent 0 *
                (∏ other ∈ rows.erase row, (row - other))⁻¹) *
              (column ^ exponent 1 *
                (∏ other ∈ columns.erase column, (column - other))⁻¹)) := by
      rw [mul_assoc, Finset.sum_mul_sum]
    _ = ∑ row ∈ rows, ∑ column ∈ columns,
          (∏ other ∈ rows.erase row, (row - other))⁻¹ *
            (∏ other ∈ columns.erase column, (column - other))⁻¹ *
              (coefficient * row ^ exponent 0 * column ^ exponent 1) := by
      simp_rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro row _
      apply Finset.sum_congr rfl
      intro column _
      ring

theorem pairExponent_eq_iff
    {uDegree vDegree uDegree' vDegree' : Nat} :
    pairExponent uDegree vDegree = pairExponent uDegree' vDegree' ↔
      uDegree = uDegree' ∧ vDegree = vDegree' := by
  constructor
  · intro equality
    constructor
    · simpa only [pairExponent_zero] using
        congrArg (fun exponent : Fin 2 →₀ Nat => exponent 0) equality
    · simpa only [pairExponent_one] using
        congrArg (fun exponent : Fin 2 →₀ Nat => exponent 1) equality
  · rintro ⟨rfl, rfl⟩
    rfl

def gridFunctionalAddHom (rows columns : Finset ℚ) : Bivariate →+ ℚ where
  toFun := gridFunctional rows columns
  map_zero' := by
    simp [gridFunctional]
  map_add' left right := by
    simp only [gridFunctional, MvPolynomial.eval_add, mul_add,
      Finset.sum_add_distrib]

theorem gridFunctional_eq_support_sum
    (rows columns : Finset ℚ) (polynomial : Bivariate) :
    gridFunctional rows columns polynomial =
      ∑ exponent ∈ polynomial.support,
        MvPolynomial.coeff exponent polynomial *
          powerFunctional rows (exponent 0) *
          powerFunctional columns (exponent 1) := by
  calc
    gridFunctional rows columns polynomial =
        gridFunctional rows columns
          (∑ exponent ∈ polynomial.support,
            MvPolynomial.monomial exponent
              (MvPolynomial.coeff exponent polynomial)) := by
      exact congrArg (gridFunctional rows columns) (MvPolynomial.as_sum polynomial)
    _ = ∑ exponent ∈ polynomial.support,
          gridFunctional rows columns
            (MvPolynomial.monomial exponent
              (MvPolynomial.coeff exponent polynomial)) := by
      change gridFunctionalAddHom rows columns
          (∑ exponent ∈ polynomial.support,
            MvPolynomial.monomial exponent
              (MvPolynomial.coeff exponent polynomial)) =
        ∑ exponent ∈ polynomial.support,
          gridFunctionalAddHom rows columns
            (MvPolynomial.monomial exponent
              (MvPolynomial.coeff exponent polynomial))
      exact map_sum (gridFunctionalAddHom rows columns)
        (fun exponent => MvPolynomial.monomial exponent
          (MvPolynomial.coeff exponent polynomial)) polynomial.support
    _ = ∑ exponent ∈ polynomial.support,
          MvPolynomial.coeff exponent polynomial *
            powerFunctional rows (exponent 0) *
            powerFunctional columns (exponent 1) := by
      apply Finset.sum_congr rfl
      intro exponent _
      exact gridFunctional_monomial rows columns exponent
        (MvPolynomial.coeff exponent polynomial)

theorem gridFunctional_eq_zero_of_vanishes
    (rows columns : Finset ℚ) (polynomial : Bivariate)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column) polynomial = 0) :
    gridFunctional rows columns polynomial = 0 := by
  unfold gridFunctional
  apply Finset.sum_eq_zero
  intro row rowIn
  apply Finset.sum_eq_zero
  intro column columnIn
  rw [vanishes row rowIn column columnIn]
  ring

private theorem gridFunctional_pair_monomial_ledger
    (rows columns : Finset ℚ)
    (rowsNonempty : rows.Nonempty) (columnsNonempty : columns.Nonempty)
    (uDegree vDegree : Nat) (coefficient : ℚ)
    (degreeBound : uDegree + vDegree ≤ rows.card + columns.card - 1) :
    gridFunctional rows columns
        (MvPolynomial.monomial (pairExponent uDegree vDegree) coefficient) =
      MvPolynomial.coeff
          (pairExponent (rows.card - 1) (columns.card - 1))
          (MvPolynomial.monomial (pairExponent uDegree vDegree) coefficient) +
        (∑ row ∈ rows, row) *
          MvPolynomial.coeff (pairExponent rows.card (columns.card - 1))
            (MvPolynomial.monomial (pairExponent uDegree vDegree) coefficient) +
        (∑ column ∈ columns, column) *
          MvPolynomial.coeff (pairExponent (rows.card - 1) columns.card)
            (MvPolynomial.monomial (pairExponent uDegree vDegree) coefficient) := by
  rw [gridFunctional_monomial]
  simp only [pairExponent_zero, pairExponent_one, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]
  have rowsPositive : 0 < rows.card := Finset.card_pos.mpr rowsNonempty
  have columnsPositive : 0 < columns.card := Finset.card_pos.mpr columnsNonempty
  by_cases rowLow : uDegree < rows.card - 1
  · have rowBelowCard : uDegree < rows.card := by omega
    rw [powerFunctional_of_lt_card rows uDegree rowBelowCard]
    have firstFalse :
        ¬(uDegree = rows.card - 1 ∧ vDegree = columns.card - 1) := by omega
    have secondFalse :
        ¬(uDegree = rows.card ∧ vDegree = columns.card - 1) := by omega
    have thirdFalse :
        ¬(uDegree = rows.card - 1 ∧ vDegree = columns.card) := by omega
    simp [if_neg (by omega : uDegree ≠ rows.card - 1), firstFalse,
      secondFalse, thirdFalse]
  by_cases columnLow : vDegree < columns.card - 1
  · have columnBelowCard : vDegree < columns.card := by omega
    rw [powerFunctional_of_lt_card columns vDegree columnBelowCard]
    have firstFalse :
        ¬(uDegree = rows.card - 1 ∧ vDegree = columns.card - 1) := by omega
    have secondFalse :
        ¬(uDegree = rows.card ∧ vDegree = columns.card - 1) := by omega
    have thirdFalse :
        ¬(uDegree = rows.card - 1 ∧ vDegree = columns.card) := by omega
    simp [if_neg (by omega : vDegree ≠ columns.card - 1), firstFalse,
      secondFalse, thirdFalse]
  have cases :
      (uDegree = rows.card - 1 ∧ vDegree = columns.card - 1) ∨
      (uDegree = rows.card ∧ vDegree = columns.card - 1) ∨
      (uDegree = rows.card - 1 ∧ vDegree = columns.card) := by
    omega
  rcases cases with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · rw [powerFunctional_of_lt_card rows (rows.card - 1) (by omega),
      powerFunctional_of_lt_card columns (columns.card - 1) (by omega)]
    simp [show rows.card - 1 ≠ rows.card by omega,
      show columns.card - 1 ≠ columns.card by omega]
  · rw [powerFunctional_card rows rowsNonempty,
      powerFunctional_of_lt_card columns (columns.card - 1) (by omega)]
    simp [show rows.card ≠ rows.card - 1 by omega,
      show columns.card - 1 ≠ columns.card by omega]
    ring
  · rw [powerFunctional_of_lt_card rows (rows.card - 1) (by omega),
      powerFunctional_card columns columnsNonempty]
    simp [show rows.card - 1 ≠ rows.card by omega,
      show columns.card ≠ columns.card - 1 by omega]
    ring

/-- Tensor-Lagrange coefficient ledger through total degree `a+b-1`. -/
theorem gridFunctional_coefficient_ledger
    (rows columns : Finset ℚ)
    (rowsNonempty : rows.Nonempty) (columnsNonempty : columns.Nonempty)
    (polynomial : Bivariate)
    (degreeBound : polynomial.totalDegree ≤ rows.card + columns.card - 1) :
    gridFunctional rows columns polynomial =
      MvPolynomial.coeff
          (pairExponent (rows.card - 1) (columns.card - 1)) polynomial +
        (∑ row ∈ rows, row) *
          MvPolynomial.coeff (pairExponent rows.card (columns.card - 1)) polynomial +
        (∑ column ∈ columns, column) *
          MvPolynomial.coeff (pairExponent (rows.card - 1) columns.card) polynomial := by
  rw [gridFunctional_eq_support_sum]
  calc
    (∑ exponent ∈ polynomial.support,
        MvPolynomial.coeff exponent polynomial *
          powerFunctional rows (exponent 0) *
          powerFunctional columns (exponent 1)) =
        ∑ exponent ∈ polynomial.support,
          (MvPolynomial.coeff
              (pairExponent (rows.card - 1) (columns.card - 1))
              (MvPolynomial.monomial exponent
                (MvPolynomial.coeff exponent polynomial)) +
            (∑ row ∈ rows, row) *
              MvPolynomial.coeff (pairExponent rows.card (columns.card - 1))
                (MvPolynomial.monomial exponent
                  (MvPolynomial.coeff exponent polynomial)) +
            (∑ column ∈ columns, column) *
              MvPolynomial.coeff (pairExponent (rows.card - 1) columns.card)
                (MvPolynomial.monomial exponent
                  (MvPolynomial.coeff exponent polynomial))) := by
      apply Finset.sum_congr rfl
      intro exponent exponentIn
      have exponentDegree : exponent.degree = exponent 0 + exponent 1 := by
        calc
          exponent.degree =
              (pairExponent (exponent 0) (exponent 1)).degree :=
            congrArg Finsupp.degree (finTwoExponent_eq_pairExponent exponent)
          _ = exponent 0 + exponent 1 := pairExponent_degree _ _
      have exponentBound : exponent 0 + exponent 1 ≤
          rows.card + columns.card - 1 := by
        rw [← exponentDegree]
        exact (MvPolynomial.le_totalDegree exponentIn).trans degreeBound
      have ledger := gridFunctional_pair_monomial_ledger rows columns rowsNonempty
        columnsNonempty (exponent 0) (exponent 1)
        (MvPolynomial.coeff exponent polynomial) exponentBound
      rw [gridFunctional_monomial] at ledger
      simpa only [← finTwoExponent_eq_pairExponent exponent] using ledger
    _ = MvPolynomial.coeff
          (pairExponent (rows.card - 1) (columns.card - 1)) polynomial +
        (∑ row ∈ rows, row) *
          MvPolynomial.coeff (pairExponent rows.card (columns.card - 1)) polynomial +
        (∑ column ∈ columns, column) *
          MvPolynomial.coeff (pairExponent (rows.card - 1) columns.card) polynomial := by
      rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
      simp_rw [← Finset.mul_sum]
      rw [← MvPolynomial.coeff_sum, ← MvPolynomial.coeff_sum,
        ← MvPolynomial.coeff_sum, MvPolynomial.support_sum_monomial_coeff]

private theorem quadraticPart_pow_five_expansion :
    quadraticPart ^ 5 =
      MvPolynomial.monomial (pairExponent 10 0) (1 : ℚ) +
      MvPolynomial.monomial (pairExponent 8 2) (-5 : ℚ) +
      MvPolynomial.monomial (pairExponent 6 4) (10 : ℚ) +
      MvPolynomial.monomial (pairExponent 4 6) (-10 : ℚ) +
      MvPolynomial.monomial (pairExponent 2 8) (5 : ℚ) +
      MvPolynomial.monomial (pairExponent 0 10) (-1 : ℚ) := by
  have c5 : MvPolynomial.C (5 : ℚ) = (5 : Bivariate) := by
    change MvPolynomial.C ((5 : Nat) : ℚ) = (5 : Bivariate)
    exact MvPolynomial.C_eq_coe_nat 5
  have c10 : MvPolynomial.C (10 : ℚ) = (10 : Bivariate) := by
    change MvPolynomial.C ((10 : Nat) : ℚ) = (10 : Bivariate)
    exact MvPolynomial.C_eq_coe_nat 10
  simp only [quadraticPart, monomial_pairExponent, pow_zero, mul_one]
  simp only [map_neg]
  rw [MvPolynomial.C_1, c5, c10]
  ring

private theorem quadraticPart_pow_six_expansion :
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

private theorem quadraticPart_pow_seven_expansion :
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

private theorem coeff_quadraticPart_pow_five_4_6 :
    MvPolynomial.coeff (pairExponent 4 6) (quadraticPart ^ 5) = -10 := by
  rw [quadraticPart_pow_five_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem coeff_quadraticPart_pow_five_6_4 :
    MvPolynomial.coeff (pairExponent 6 4) (quadraticPart ^ 5) = 10 := by
  rw [quadraticPart_pow_five_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem coeff_quadraticPart_pow_five_5_5 :
    MvPolynomial.coeff (pairExponent 5 5) (quadraticPart ^ 5) = 0 := by
  rw [quadraticPart_pow_five_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem coeff_quadraticPart_pow_five_7_3 :
    MvPolynomial.coeff (pairExponent 7 3) (quadraticPart ^ 5) = 0 := by
  rw [quadraticPart_pow_five_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem coeff_quadraticPart_pow_six_5_7 :
    MvPolynomial.coeff (pairExponent 5 7) (quadraticPart ^ 6) = 0 := by
  rw [quadraticPart_pow_six_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem coeff_quadraticPart_pow_six_6_6 :
    MvPolynomial.coeff (pairExponent 6 6) (quadraticPart ^ 6) = -20 := by
  rw [quadraticPart_pow_six_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem coeff_quadraticPart_pow_six_5_6 :
    MvPolynomial.coeff (pairExponent 5 6) (quadraticPart ^ 6) = 0 := by
  rw [quadraticPart_pow_six_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem coeff_quadraticPart_pow_six_7_4 :
    MvPolynomial.coeff (pairExponent 7 4) (quadraticPart ^ 6) = 0 := by
  rw [quadraticPart_pow_six_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem coeff_quadraticPart_pow_six_8_4 :
    MvPolynomial.coeff (pairExponent 8 4) (quadraticPart ^ 6) = 15 := by
  rw [quadraticPart_pow_six_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem coeff_quadraticPart_pow_six_7_5 :
    MvPolynomial.coeff (pairExponent 7 5) (quadraticPart ^ 6) = 0 := by
  rw [quadraticPart_pow_six_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem coeff_quadraticPart_pow_seven_7_6 :
    MvPolynomial.coeff (pairExponent 7 6) (quadraticPart ^ 7) = 0 := by
  rw [quadraticPart_pow_seven_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem coeff_quadraticPart_pow_seven_8_6 :
    MvPolynomial.coeff (pairExponent 8 6) (quadraticPart ^ 7) = -35 := by
  rw [quadraticPart_pow_seven_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem coeff_quadraticPart_pow_seven_7_7 :
    MvPolynomial.coeff (pairExponent 7 7) (quadraticPart ^ 7) = 0 := by
  rw [quadraticPart_pow_seven_expansion]
  norm_num [MvPolynomial.coeff_add, MvPolynomial.coeff_monomial,
    pairExponent_eq_iff]

private theorem pairExponent_sub_zero_succ (uDegree vDegree : Nat) :
    pairExponent (uDegree + 1) vDegree - Finsupp.single 0 1 =
      pairExponent uDegree vDegree := by
  ext index
  fin_cases index <;> simp [pairExponent]

private theorem pairExponent_sub_one_succ (uDegree vDegree : Nat) :
    pairExponent uDegree (vDegree + 1) - Finsupp.single 1 1 =
      pairExponent uDegree vDegree := by
  ext index
  fin_cases index <;> simp [pairExponent]

private theorem coeff_rowTerm_pow_five_5_6 (scalar : ℚ) :
    MvPolynomial.coeff (pairExponent 5 6)
        (MvPolynomial.C scalar * U * quadraticPart ^ 5) = -10 * scalar := by
  rw [mul_assoc, MvPolynomial.coeff_C_mul]
  unfold U
  rw [MvPolynomial.coeff_X_mul']
  rw [if_pos (by simp : (0 : Fin 2) ∈ (pairExponent 5 6).support)]
  rw [show pairExponent 5 6 - Finsupp.single 0 1 = pairExponent 4 6 by
    simpa using pairExponent_sub_zero_succ 4 6]
  rw [coeff_quadraticPart_pow_five_4_6]
  ring

private theorem coeff_columnTerm_pow_five_5_6 (scalar : ℚ) :
    MvPolynomial.coeff (pairExponent 5 6)
        (MvPolynomial.C scalar * V * quadraticPart ^ 5) = 0 := by
  rw [mul_assoc, MvPolynomial.coeff_C_mul]
  unfold V
  rw [MvPolynomial.coeff_X_mul']
  rw [if_pos (by simp : (1 : Fin 2) ∈ (pairExponent 5 6).support)]
  rw [show pairExponent 5 6 - Finsupp.single 1 1 = pairExponent 5 5 by
    simpa using pairExponent_sub_one_succ 5 5]
  rw [coeff_quadraticPart_pow_five_5_5]
  ring

private theorem coeff_rowTerm_pow_five_7_4 (scalar : ℚ) :
    MvPolynomial.coeff (pairExponent 7 4)
        (MvPolynomial.C scalar * U * quadraticPart ^ 5) = 10 * scalar := by
  rw [mul_assoc, MvPolynomial.coeff_C_mul]
  unfold U
  rw [MvPolynomial.coeff_X_mul']
  rw [if_pos (by simp : (0 : Fin 2) ∈ (pairExponent 7 4).support)]
  rw [show pairExponent 7 4 - Finsupp.single 0 1 = pairExponent 6 4 by
    simpa using pairExponent_sub_zero_succ 6 4]
  rw [coeff_quadraticPart_pow_five_6_4]
  ring

private theorem coeff_columnTerm_pow_five_7_4 (scalar : ℚ) :
    MvPolynomial.coeff (pairExponent 7 4)
        (MvPolynomial.C scalar * V * quadraticPart ^ 5) = 0 := by
  rw [mul_assoc, MvPolynomial.coeff_C_mul]
  unfold V
  rw [MvPolynomial.coeff_X_mul']
  rw [if_pos (by simp : (1 : Fin 2) ∈ (pairExponent 7 4).support)]
  rw [show pairExponent 7 4 - Finsupp.single 1 1 = pairExponent 7 3 by
    simpa using pairExponent_sub_one_succ 7 3]
  rw [coeff_quadraticPart_pow_five_7_3]
  ring

private theorem coeff_rowTerm_pow_six_7_6 (scalar : ℚ) :
    MvPolynomial.coeff (pairExponent 7 6)
        (MvPolynomial.C scalar * U * quadraticPart ^ 6) = -20 * scalar := by
  rw [mul_assoc, MvPolynomial.coeff_C_mul]
  unfold U
  rw [MvPolynomial.coeff_X_mul']
  rw [if_pos (by simp : (0 : Fin 2) ∈ (pairExponent 7 6).support)]
  rw [show pairExponent 7 6 - Finsupp.single 0 1 = pairExponent 6 6 by
    simpa using pairExponent_sub_zero_succ 6 6]
  rw [coeff_quadraticPart_pow_six_6_6]
  ring

private theorem coeff_columnTerm_pow_six_7_6 (scalar : ℚ) :
    MvPolynomial.coeff (pairExponent 7 6)
        (MvPolynomial.C scalar * V * quadraticPart ^ 6) = 0 := by
  rw [mul_assoc, MvPolynomial.coeff_C_mul]
  unfold V
  rw [MvPolynomial.coeff_X_mul']
  rw [if_pos (by simp : (1 : Fin 2) ∈ (pairExponent 7 6).support)]
  rw [show pairExponent 7 6 - Finsupp.single 1 1 = pairExponent 7 5 by
    simpa using pairExponent_sub_one_succ 7 5]
  rw [coeff_quadraticPart_pow_six_7_5]
  ring

private theorem occurrence_six_coeff_5_6
    (queens : Finset Square) (cardExact : queens.card = 6) :
    MvPolynomial.coeff (pairExponent 5 6) (occurrencePolynomial queens) =
      20 * queenRowSum queens := by
  calc
    MvPolynomial.coeff (pairExponent 5 6) (occurrencePolynomial queens) =
        MvPolynomial.coeff (pairExponent 5 6) (topTwoApproximation queens) := by
      apply coeff_occurrence_eq_topTwo queens (by omega)
      rw [pairExponent_degree, cardExact]
    _ = 20 * queenRowSum queens := by
      rw [topTwoApproximation_eq_coordinate_sums, cardExact]
      norm_num only [Nat.reduceSub]
      rw [MvPolynomial.coeff_add, coeff_quadraticPart_pow_six_5_6,
        add_mul, MvPolynomial.coeff_add,
        coeff_rowTerm_pow_five_5_6, coeff_columnTerm_pow_five_5_6]
      ring

private theorem occurrence_six_coeff_7_4
    (queens : Finset Square) (cardExact : queens.card = 6) :
    MvPolynomial.coeff (pairExponent 7 4) (occurrencePolynomial queens) =
      -20 * queenRowSum queens := by
  calc
    MvPolynomial.coeff (pairExponent 7 4) (occurrencePolynomial queens) =
        MvPolynomial.coeff (pairExponent 7 4) (topTwoApproximation queens) := by
      apply coeff_occurrence_eq_topTwo queens (by omega)
      rw [pairExponent_degree, cardExact]
    _ = -20 * queenRowSum queens := by
      rw [topTwoApproximation_eq_coordinate_sums, cardExact]
      norm_num only [Nat.reduceSub]
      rw [MvPolynomial.coeff_add, coeff_quadraticPart_pow_six_7_4,
        add_mul, MvPolynomial.coeff_add,
        coeff_rowTerm_pow_five_7_4, coeff_columnTerm_pow_five_7_4]
      ring

private theorem occurrence_seven_coeff_7_6
    (queens : Finset Square) (cardExact : queens.card = 7) :
    MvPolynomial.coeff (pairExponent 7 6) (occurrencePolynomial queens) =
      40 * queenRowSum queens := by
  calc
    MvPolynomial.coeff (pairExponent 7 6) (occurrencePolynomial queens) =
        MvPolynomial.coeff (pairExponent 7 6) (topTwoApproximation queens) := by
      apply coeff_occurrence_eq_topTwo queens (by omega)
      rw [pairExponent_degree, cardExact]
    _ = 40 * queenRowSum queens := by
      rw [topTwoApproximation_eq_coordinate_sums, cardExact]
      norm_num only [Nat.reduceSub]
      rw [MvPolynomial.coeff_add, coeff_quadraticPart_pow_seven_7_6,
        add_mul, MvPolynomial.coeff_add,
        coeff_rowTerm_pow_six_7_6, coeff_columnTerm_pow_six_7_6]
      ring

private theorem occurrence_six_coeff_6_6
    (queens : Finset Square) (cardExact : queens.card = 6) :
    MvPolynomial.coeff (pairExponent 6 6) (occurrencePolynomial queens) = -20 := by
  calc
    MvPolynomial.coeff (pairExponent 6 6) (occurrencePolynomial queens) =
        MvPolynomial.coeff (pairExponent 6 6) (topApproximation queens) := by
      apply coeff_occurrence_eq_top queens (by omega)
      rw [pairExponent_degree, cardExact]
    _ = -20 := by
      simp [topApproximation, cardExact, coeff_quadraticPart_pow_six_6_6]

private theorem occurrence_six_coeff_8_4
    (queens : Finset Square) (cardExact : queens.card = 6) :
    MvPolynomial.coeff (pairExponent 8 4) (occurrencePolynomial queens) = 15 := by
  calc
    MvPolynomial.coeff (pairExponent 8 4) (occurrencePolynomial queens) =
        MvPolynomial.coeff (pairExponent 8 4) (topApproximation queens) := by
      apply coeff_occurrence_eq_top queens (by omega)
      rw [pairExponent_degree, cardExact]
    _ = 15 := by
      simp [topApproximation, cardExact, coeff_quadraticPart_pow_six_8_4]

private theorem occurrence_seven_coeff_8_6
    (queens : Finset Square) (cardExact : queens.card = 7) :
    MvPolynomial.coeff (pairExponent 8 6) (occurrencePolynomial queens) = -35 := by
  calc
    MvPolynomial.coeff (pairExponent 8 6) (occurrencePolynomial queens) =
        MvPolynomial.coeff (pairExponent 8 6) (topApproximation queens) := by
      apply coeff_occurrence_eq_top queens (by omega)
      rw [pairExponent_degree, cardExact]
    _ = -35 := by
      simp [topApproximation, cardExact, coeff_quadraticPart_pow_seven_8_6]

private theorem occurrence_six_coeff_5_7
    (queens : Finset Square) (cardExact : queens.card = 6) :
    MvPolynomial.coeff (pairExponent 5 7) (occurrencePolynomial queens) = 0 := by
  calc
    MvPolynomial.coeff (pairExponent 5 7) (occurrencePolynomial queens) =
        MvPolynomial.coeff (pairExponent 5 7) (topApproximation queens) := by
      apply coeff_occurrence_eq_top queens (by omega)
      rw [pairExponent_degree, cardExact]
    _ = 0 := by
      simp [topApproximation, cardExact, coeff_quadraticPart_pow_six_5_7]

private theorem occurrence_six_coeff_7_5
    (queens : Finset Square) (cardExact : queens.card = 6) :
    MvPolynomial.coeff (pairExponent 7 5) (occurrencePolynomial queens) = 0 := by
  calc
    MvPolynomial.coeff (pairExponent 7 5) (occurrencePolynomial queens) =
        MvPolynomial.coeff (pairExponent 7 5) (topApproximation queens) := by
      apply coeff_occurrence_eq_top queens (by omega)
      rw [pairExponent_degree, cardExact]
    _ = 0 := by
      simp [topApproximation, cardExact, coeff_quadraticPart_pow_six_7_5]

private theorem occurrence_seven_coeff_7_7
    (queens : Finset Square) (cardExact : queens.card = 7) :
    MvPolynomial.coeff (pairExponent 7 7) (occurrencePolynomial queens) = 0 := by
  calc
    MvPolynomial.coeff (pairExponent 7 7) (occurrencePolynomial queens) =
        MvPolynomial.coeff (pairExponent 7 7) (topApproximation queens) := by
      apply coeff_occurrence_eq_top queens (by omega)
      rw [pairExponent_degree, cardExact]
    _ = 0 := by
      simp [topApproximation, cardExact, coeff_quadraticPart_pow_seven_7_7]

/-- The exact row moment for the tight `6 × 7` grid covered by six queens. -/
theorem occurrence_six_row_moment_6_7
    (queens : Finset Square) (queenCard : queens.card = 6)
    (rows columns : Finset ℚ) (rowCard : rows.card = 6)
    (columnCard : columns.card = 7)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column)
        (occurrencePolynomial queens) = 0) :
    6 * queenRowSum queens = 6 * ∑ row ∈ rows, row := by
  have rowsNonempty : rows.Nonempty := Finset.card_pos.mp (by omega)
  have columnsNonempty : columns.Nonempty := Finset.card_pos.mp (by omega)
  have degreeBound :
      (occurrencePolynomial queens).totalDegree ≤
        rows.card + columns.card - 1 := by
    rw [occurrence_six_totalDegree queens queenCard, rowCard, columnCard]
  have ledger := gridFunctional_coefficient_ledger rows columns rowsNonempty
    columnsNonempty (occurrencePolynomial queens) degreeBound
  have functionalZero := gridFunctional_eq_zero_of_vanishes rows columns
    (occurrencePolynomial queens) vanishes
  rw [functionalZero, rowCard, columnCard] at ledger
  norm_num only [Nat.reduceSub] at ledger
  rw [occurrence_six_coeff_5_6 queens queenCard,
    occurrence_six_coeff_6_6 queens queenCard,
    occurrence_six_coeff_5_7 queens queenCard] at ledger
  linarith

/-- The exact row moment for the tight `8 × 5` grid covered by six queens. -/
theorem occurrence_six_row_moment_8_5
    (queens : Finset Square) (queenCard : queens.card = 6)
    (rows columns : Finset ℚ) (rowCard : rows.card = 8)
    (columnCard : columns.card = 5)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column)
        (occurrencePolynomial queens) = 0) :
    8 * queenRowSum queens = 6 * ∑ row ∈ rows, row := by
  have rowsNonempty : rows.Nonempty := Finset.card_pos.mp (by omega)
  have columnsNonempty : columns.Nonempty := Finset.card_pos.mp (by omega)
  have degreeBound :
      (occurrencePolynomial queens).totalDegree ≤
        rows.card + columns.card - 1 := by
    rw [occurrence_six_totalDegree queens queenCard, rowCard, columnCard]
  have ledger := gridFunctional_coefficient_ledger rows columns rowsNonempty
    columnsNonempty (occurrencePolynomial queens) degreeBound
  have functionalZero := gridFunctional_eq_zero_of_vanishes rows columns
    (occurrencePolynomial queens) vanishes
  rw [functionalZero, rowCard, columnCard] at ledger
  norm_num only [Nat.reduceSub] at ledger
  rw [occurrence_six_coeff_7_4 queens queenCard,
    occurrence_six_coeff_8_4 queens queenCard,
    occurrence_six_coeff_7_5 queens queenCard] at ledger
  linarith

private theorem coeff_V_mul_pairExponent_succ
    (polynomial : Bivariate) (uDegree vDegree : Nat) :
    MvPolynomial.coeff (pairExponent uDegree (vDegree + 1))
        (V * polynomial) =
      MvPolynomial.coeff (pairExponent uDegree vDegree) polynomial := by
  unfold V
  rw [MvPolynomial.coeff_X_mul']
  rw [if_pos (by simp :
    (1 : Fin 2) ∈ (pairExponent uDegree (vDegree + 1)).support)]
  rw [pairExponent_sub_one_succ]

/-- The even-even `8 × 6` row moment, obtained by applying the ledger to
`V` times the six-queen occurrence polynomial. -/
theorem occurrence_six_row_moment_8_6
    (queens : Finset Square) (queenCard : queens.card = 6)
    (rows columns : Finset ℚ) (rowCard : rows.card = 8)
    (columnCard : columns.card = 6)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column)
        (occurrencePolynomial queens) = 0) :
    8 * queenRowSum queens = 6 * ∑ row ∈ rows, row := by
  have rowsNonempty : rows.Nonempty := Finset.card_pos.mp (by omega)
  have columnsNonempty : columns.Nonempty := Finset.card_pos.mp (by omega)
  have occurrenceDegree :
      (occurrencePolynomial queens).totalDegree = 12 :=
    occurrence_six_totalDegree queens queenCard
  have degreeBound :
      (V * occurrencePolynomial queens).totalDegree ≤
        rows.card + columns.card - 1 := by
    calc
      (V * occurrencePolynomial queens).totalDegree ≤
          V.totalDegree + (occurrencePolynomial queens).totalDegree :=
        MvPolynomial.totalDegree_mul _ _
      _ = 13 := by simp [V, occurrenceDegree]
      _ = rows.card + columns.card - 1 := by rw [rowCard, columnCard]
  have productVanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column)
        (V * occurrencePolynomial queens) = 0 := by
    intro row rowIn column columnIn
    rw [MvPolynomial.eval_mul, vanishes row rowIn column columnIn]
    ring
  have ledger := gridFunctional_coefficient_ledger rows columns rowsNonempty
    columnsNonempty (V * occurrencePolynomial queens) degreeBound
  have functionalZero := gridFunctional_eq_zero_of_vanishes rows columns
    (V * occurrencePolynomial queens) productVanishes
  rw [functionalZero, rowCard, columnCard] at ledger
  norm_num only [Nat.reduceSub] at ledger
  rw [coeff_V_mul_pairExponent_succ (occurrencePolynomial queens) 7 4,
    coeff_V_mul_pairExponent_succ (occurrencePolynomial queens) 8 4,
    coeff_V_mul_pairExponent_succ (occurrencePolynomial queens) 7 5,
    occurrence_six_coeff_7_4 queens queenCard,
    occurrence_six_coeff_8_4 queens queenCard,
    occurrence_six_coeff_7_5 queens queenCard] at ledger
  linarith

/-- The even-even `6 × 8` row moment, obtained by applying the ledger to
`V` times the six-queen occurrence polynomial. -/
theorem occurrence_six_row_moment_6_8
    (queens : Finset Square) (queenCard : queens.card = 6)
    (rows columns : Finset ℚ) (rowCard : rows.card = 6)
    (columnCard : columns.card = 8)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column)
        (occurrencePolynomial queens) = 0) :
    6 * queenRowSum queens = 6 * ∑ row ∈ rows, row := by
  have rowsNonempty : rows.Nonempty := Finset.card_pos.mp (by omega)
  have columnsNonempty : columns.Nonempty := Finset.card_pos.mp (by omega)
  have occurrenceDegree :
      (occurrencePolynomial queens).totalDegree = 12 :=
    occurrence_six_totalDegree queens queenCard
  have degreeBound :
      (V * occurrencePolynomial queens).totalDegree ≤
        rows.card + columns.card - 1 := by
    calc
      (V * occurrencePolynomial queens).totalDegree ≤
          V.totalDegree + (occurrencePolynomial queens).totalDegree :=
        MvPolynomial.totalDegree_mul _ _
      _ = 13 := by simp [V, occurrenceDegree]
      _ = rows.card + columns.card - 1 := by rw [rowCard, columnCard]
  have productVanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column)
        (V * occurrencePolynomial queens) = 0 := by
    intro row rowIn column columnIn
    rw [MvPolynomial.eval_mul, vanishes row rowIn column columnIn]
    ring
  have ledger := gridFunctional_coefficient_ledger rows columns rowsNonempty
    columnsNonempty (V * occurrencePolynomial queens) degreeBound
  have functionalZero := gridFunctional_eq_zero_of_vanishes rows columns
    (V * occurrencePolynomial queens) productVanishes
  rw [functionalZero, rowCard, columnCard] at ledger
  norm_num only [Nat.reduceSub] at ledger
  rw [coeff_V_mul_pairExponent_succ (occurrencePolynomial queens) 5 6,
    coeff_V_mul_pairExponent_succ (occurrencePolynomial queens) 6 6,
    coeff_V_mul_pairExponent_succ (occurrencePolynomial queens) 5 7,
    occurrence_six_coeff_5_6 queens queenCard,
    occurrence_six_coeff_6_6 queens queenCard,
    occurrence_six_coeff_5_7 queens queenCard] at ledger
  linarith

/-- The even-even `8 × 8` row moment, obtained by applying the ledger to
`V` times the seven-queen occurrence polynomial. -/
theorem occurrence_seven_row_moment_8_8
    (queens : Finset Square) (queenCard : queens.card = 7)
    (rows columns : Finset ℚ) (rowCard : rows.card = 8)
    (columnCard : columns.card = 8)
    (vanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column)
        (occurrencePolynomial queens) = 0) :
    8 * queenRowSum queens = 7 * ∑ row ∈ rows, row := by
  have rowsNonempty : rows.Nonempty := Finset.card_pos.mp (by omega)
  have columnsNonempty : columns.Nonempty := Finset.card_pos.mp (by omega)
  have occurrenceDegree :
      (occurrencePolynomial queens).totalDegree = 14 :=
    occurrence_seven_totalDegree queens queenCard
  have degreeBound :
      (V * occurrencePolynomial queens).totalDegree ≤
        rows.card + columns.card - 1 := by
    calc
      (V * occurrencePolynomial queens).totalDegree ≤
          V.totalDegree + (occurrencePolynomial queens).totalDegree :=
        MvPolynomial.totalDegree_mul _ _
      _ = 15 := by simp [V, occurrenceDegree]
      _ = rows.card + columns.card - 1 := by rw [rowCard, columnCard]
  have productVanishes : ∀ row ∈ rows, ∀ column ∈ columns,
      MvPolynomial.eval (rationalPairPoint row column)
        (V * occurrencePolynomial queens) = 0 := by
    intro row rowIn column columnIn
    rw [MvPolynomial.eval_mul, vanishes row rowIn column columnIn]
    ring
  have ledger := gridFunctional_coefficient_ledger rows columns rowsNonempty
    columnsNonempty (V * occurrencePolynomial queens) degreeBound
  have functionalZero := gridFunctional_eq_zero_of_vanishes rows columns
    (V * occurrencePolynomial queens) productVanishes
  rw [functionalZero, rowCard, columnCard] at ledger
  norm_num only [Nat.reduceSub] at ledger
  rw [coeff_V_mul_pairExponent_succ (occurrencePolynomial queens) 7 6,
    coeff_V_mul_pairExponent_succ (occurrencePolynomial queens) 8 6,
    coeff_V_mul_pairExponent_succ (occurrencePolynomial queens) 7 7,
    occurrence_seven_coeff_7_6 queens queenCard,
    occurrence_seven_coeff_8_6 queens queenCard,
    occurrence_seven_coeff_7_7 queens queenCard] at ledger
  linarith

end

end Q26GridAnnihilator
