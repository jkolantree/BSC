import Mathlib

/-!
# The finite Q26 profile closure

This file contains only the finite integer arithmetic at the end of the
Q26 grid-annihilator argument.  It does not assume the board-theoretic
Weakley bridge or the polynomial moment lemmas.  Instead, it exposes the two
integer contradictions to which those earlier layers reduce the five cases.

All finite classifications below are evaluated by the kernel with `decide`;
no external table is imported into the proof.
-/

namespace Q26GridAnnihilator

/-- The three possible occupied-row/occupied-column inventories, after using
transpose to orient the one-duplicate case. -/
inductive Inventory where
  | W0
  | W1
  | W2
  deriving DecidableEq, Repr

abbrev Pair := Nat × Nat

def occupiedRows : Inventory → Nat
  | .W0 => 13
  | .W1 => 12
  | .W2 => 12

def occupiedColumns : Inventory → Nat
  | .W0 => 13
  | .W1 => 13
  | .W2 => 12

/-- The four parity-refined empty-line counts `(x0,x1,y0,y1)`.  The input
pair records the numbers of occupied even rows and occupied even columns. -/
structure EmptyCounts where
  x0 : Nat
  x1 : Nat
  y0 : Nat
  y1 : Nat
  deriving DecidableEq, Repr

def emptyCounts (kind : Inventory) (pair : Pair) : EmptyCounts where
  x0 := 13 - pair.1
  x1 := 13 - occupiedRows kind + pair.1
  y0 := 13 - pair.2
  y1 := 13 - occupiedColumns kind + pair.2

/-- The queen parity-incidence table `(q00,q01,q10,q11)`. -/
structure QTable where
  q00 : Nat
  q01 : Nat
  q10 : Nat
  q11 : Nat
  deriving DecidableEq, Repr

/-- Check all four margins of the normalized `6/7` color split. -/
def QTable.validFor (table : QTable)
    (evenRowIncidence evenColumnIncidence : Nat) : Bool :=
  decide (
    table.q00 + table.q01 + table.q10 + table.q11 = 13 ∧
    table.q00 + table.q11 = 6 ∧
    table.q01 + table.q10 = 7 ∧
    table.q00 + table.q01 = evenRowIncidence ∧
    table.q00 + table.q10 = evenColumnIncidence)

/-- Enumerate `q00 = 0,...,6`; the row, column, and color-0 margins then
determine the other entries.  The final filter checks the color-1 and total
margins as well as guarding all truncated natural-number subtractions. -/
def feasibleTables (evenRowIncidence evenColumnIncidence : Nat) : List QTable :=
  ((List.range 7).map fun q00 =>
      { q00 := q00
        q01 := evenRowIncidence - q00
        q10 := evenColumnIncidence - q00
        q11 := 6 - q00 }).filter fun table =>
    table.validFor evenRowIncidence evenColumnIncidence

def tableFeasible (evenRowIncidence evenColumnIncidence : Nat) : Bool :=
  !(feasibleTables evenRowIncidence evenColumnIncidence).isEmpty

/-- Whether a repeated occupied line, if there is one, may have even index.
`false` means either that there is no repeated line or that the repeated line
has odd index. -/
def duplicateAllowed (occupied occupiedEven : Nat) (duplicateEven : Bool) : Bool :=
  if occupied = 13 then
    !duplicateEven
  else if occupied = 12 then
    if duplicateEven then decide (0 < occupiedEven)
    else decide (occupiedEven < occupied)
  else
    false

def boolNat : Bool → Nat
  | false => 0
  | true => 1

structure DuplicateChoice where
  rowEven : Bool
  columnEven : Bool
  deriving DecidableEq, Repr

structure Lift where
  duplicate : DuplicateChoice
  table : QTable
  deriving DecidableEq, Repr

def duplicateChoiceUniverse : List DuplicateChoice :=
  [⟨false, false⟩, ⟨false, true⟩, ⟨true, false⟩, ⟨true, true⟩]

def duplicateSupported (kind : Inventory) (pair : Pair)
    (choice : DuplicateChoice) : Bool :=
  duplicateAllowed (occupiedRows kind) pair.1 choice.rowEven &&
  duplicateAllowed (occupiedColumns kind) pair.2 choice.columnEven

def feasibleLifts (kind : Inventory) (pair : Pair) : List Lift :=
  (duplicateChoiceUniverse.filter fun choice =>
      duplicateSupported kind pair choice).flatMap fun choice =>
    (feasibleTables (pair.1 + boolNat choice.rowEven)
      (pair.2 + boolNat choice.columnEven)).map fun table =>
      ⟨choice, table⟩

def allPairs (kind : Inventory) : List Pair :=
  (List.range (occupiedRows kind + 1)).flatMap fun a =>
    (List.range (occupiedColumns kind + 1)).map fun b => (a, b)

/-- Before the grid-cardinality inequalities, W0 already has its unique
no-duplicate parity table.  W1 and W2 retain all possible occupied-even-line
counts because the duplicate parities have not yet been selected. -/
def coarseDomain : Inventory → List Pair
  | .W0 => (allPairs .W0).filter fun pair => tableFeasible pair.1 pair.2
  | .W1 => allPairs .W1
  | .W2 => allPairs .W2

def pairLE (left right : Pair) : Bool :=
  decide (left.1 < right.1 ∨ (left.1 = right.1 ∧ left.2 ≤ right.2))

def orbit (kind : Inventory) (pair : Pair) : List Pair :=
  let a := pair.1
  let b := pair.2
  match kind with
  | .W0 => [(a, b), (b, a), (13 - a, 13 - b), (13 - b, 13 - a)]
  | .W1 => [(a, b), (12 - a, 13 - b)]
  | .W2 => [(a, b), (b, a), (12 - a, 12 - b), (12 - b, 12 - a)]

def isOrbitRepresentative (kind : Inventory) (pair : Pair) : Bool :=
  (orbit kind pair).all (pairLE pair)

def orbitRepresentatives (kind : Inventory) (domain : List Pair) : List Pair :=
  domain.filter (isOrbitRepresentative kind)

def cnGridOK (rowCount columnCount queenCount : Nat) : Bool :=
  (List.range (queenCount + 1)).all fun j =>
    decide (rowCount ≤ 2 * (queenCount - j) ∨ columnCount ≤ 2 * j)

def countsPositive (counts : EmptyCounts) : Bool :=
  decide (0 < counts.x0 ∧ 0 < counts.x1 ∧ 0 < counts.y0 ∧ 0 < counts.y1)

def cnProfileOK (kind : Inventory) (pair : Pair) : Bool :=
  let counts := emptyCounts kind pair
  countsPositive counts &&
  cnGridOK counts.x0 counts.y0 6 &&
  cnGridOK counts.x1 counts.y1 6 &&
  cnGridOK counts.x0 counts.y1 7 &&
  cnGridOK counts.x1 counts.y0 7

def survivorDomain (kind : Inventory) : List Pair :=
  (coarseDomain kind).filter fun pair =>
    cnProfileOK kind pair && !(feasibleLifts kind pair).isEmpty

def survivorRepresentatives (kind : Inventory) : List Pair :=
  orbitRepresentatives kind (survivorDomain kind)

set_option maxRecDepth 100000 in
theorem coarse_domain_cardinalities :
    (coarseDomain .W0).length = 56 ∧
    (coarseDomain .W1).length = 182 ∧
    (coarseDomain .W2).length = 169 := by
  decide

set_option maxRecDepth 100000 in
theorem coarse_orbit_cardinalities :
    (orbitRepresentatives .W0 (coarseDomain .W0)).length = 16 ∧
    (orbitRepresentatives .W1 (coarseDomain .W1)).length = 91 ∧
    (orbitRepresentatives .W2 (coarseDomain .W2)).length = 49 := by
  decide

set_option maxRecDepth 100000 in
theorem raw_survivors_W0 :
    survivorDomain .W0 = [(5, 8), (6, 7), (7, 6), (8, 5)] := by
  decide

set_option maxRecDepth 100000 in
theorem raw_survivors_W1 :
    survivorDomain .W1 = [(5, 7), (5, 8), (7, 5), (7, 6)] := by
  decide

set_option maxRecDepth 100000 in
theorem raw_survivors_W2 :
    survivorDomain .W2 = [(5, 7), (7, 5)] := by
  decide

set_option maxRecDepth 100000 in
theorem five_orbit_representatives :
    survivorRepresentatives .W0 = [(5, 8), (6, 7)] ∧
    survivorRepresentatives .W1 = [(5, 7), (5, 8)] ∧
    survivorRepresentatives .W2 = [(5, 7)] := by
  decide

def table3253 : QTable := ⟨3, 2, 5, 3⟩
def table3343 : QTable := ⟨3, 3, 4, 3⟩

theorem supported_lifts_W0_5_8 :
    feasibleLifts .W0 (5, 8) = [⟨⟨false, false⟩, table3253⟩] := by
  decide

theorem supported_lifts_W0_6_7 :
    feasibleLifts .W0 (6, 7) = [⟨⟨false, false⟩, table3343⟩] := by
  decide

theorem supported_lifts_W1_5_7 :
    feasibleLifts .W1 (5, 7) = [⟨⟨true, false⟩, table3343⟩] := by
  decide

theorem supported_lifts_W1_5_8 :
    feasibleLifts .W1 (5, 8) = [⟨⟨false, false⟩, table3253⟩] := by
  decide

theorem supported_lifts_W2_5_7 :
    feasibleLifts .W2 (5, 7) =
      [⟨⟨false, true⟩, table3253⟩, ⟨⟨true, false⟩, table3343⟩] := by
  decide

structure Profile where
  inventory : Inventory
  pair : Pair
  deriving DecidableEq, Repr

def canonicalProfiles : List Profile :=
  [ ⟨.W0, (5, 8)⟩
  , ⟨.W0, (6, 7)⟩
  , ⟨.W1, (5, 7)⟩
  , ⟨.W1, (5, 8)⟩
  , ⟨.W2, (5, 7)⟩
  ]

def canonicalLifts : List Lift :=
  canonicalProfiles.flatMap fun profile =>
    feasibleLifts profile.inventory profile.pair

theorem canonical_lifts_exact :
    canonicalLifts =
      [ ⟨⟨false, false⟩, table3253⟩
      , ⟨⟨false, false⟩, table3343⟩
      , ⟨⟨true, false⟩, table3343⟩
      , ⟨⟨false, false⟩, table3253⟩
      , ⟨⟨false, true⟩, table3253⟩
      , ⟨⟨true, false⟩, table3343⟩
      ] := by
  decide

/-- Every supported lift of every canonical profile has `q11 = 3`. -/
theorem q11_eq_three_of_mem_canonical_lifts
    (lift : Lift) (membership : lift ∈ canonicalLifts) : lift.table.q11 = 3 := by
  rw [canonical_lifts_exact] at membership
  simp only [List.mem_cons, List.not_mem_nil, or_false] at membership
  rcases membership with h | h | h | h | h | h
  all_goals
    subst lift
    rfl

/-- The four cases with a six-element odd empty-row class close as soon as the
moment equation and the two parity facts have been supplied by the preceding
formal layers.  `q11 = 3` is kept explicit in the statement. -/
theorem six_odd_row_profile_contradiction
    (q11 : Nat) (R A : Int)
    (hq11 : q11 = 3)
    (queenRowParity : R % 2 = (q11 : Int) % 2)
    (sixOddRowsParity : A % 2 = 0)
    (moment : 6 * R = 6 * A) : False := by
  omega

/-- The remaining W0(5,8) case: the 8-by-5 and 8-by-8 moment equations force
the six-queen row sum to be even, contradicting `q11 = 3`. -/
theorem W0_5_8_divisibility_contradiction
    (q11 : Nat) (R0 R1 A0 : Int)
    (hq11 : q11 = 3)
    (queenRowParity : R0 % 2 = (q11 : Int) % 2)
    (color0Moment : 8 * R0 = 6 * A0)
    (color1Moment : 8 * R1 = 7 * A0) : False := by
  omega

end Q26GridAnnihilator
