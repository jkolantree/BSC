import Q26GridAnnihilator.Shadow

/-!
# Finite obstruction recipes for the bichromatic Q26 shadows

This module refines the exact 32-record bichromatic classification.  It does
not mention a chessboard: each recipe is only a proposition about one raw
numerical shadow.  The board-level module must still turn the selected recipe
into the corresponding checked polynomial moment and parity contradiction.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

def sevenOrEight (count : Nat) : Prop := count = 7 ∨ count = 8

instance (count : Nat) : Decidable (sevenOrEight count) := by
  unfold sevenOrEight
  infer_instance

/-- A six-queen color has a six-line row set and a tight seven- or eight-line
column set.  The recorded incidence is exactly the odd row count used later. -/
def Shadow.standardRowRecipe (shadow : Shadow) : Prop :=
  (shadow.coarse.color0 = 6 ∧ shadow.table.q11 = 3 ∧
      ((shadow.coarse.rows.emptyEven = 6 ∧
          sevenOrEight shadow.coarse.columns.emptyEven) ∨
        (shadow.coarse.rows.emptyOdd = 6 ∧
          sevenOrEight shadow.coarse.columns.emptyOdd))) ∨
    (shadow.coarse.color0 = 7 ∧ shadow.table.q10 = 3 ∧
      ((shadow.coarse.rows.emptyEven = 6 ∧
          sevenOrEight shadow.coarse.columns.emptyOdd) ∨
        (shadow.coarse.rows.emptyOdd = 6 ∧
          sevenOrEight shadow.coarse.columns.emptyEven)))

def fiveOrSix (count : Nat) : Prop := count = 5 ∨ count = 6

instance (count : Nat) : Decidable (fiveOrSix count) := by
  unfold fiveOrSix
  infer_instance

/-- The shared-eight-line exception: the same row set supports a tight
`8 × (5 or 6)` six-queen grid and a tight `8 × 8` seven-queen grid. -/
def Shadow.exceptionalRowRecipe (shadow : Shadow) : Prop :=
  (shadow.coarse.color0 = 6 ∧ shadow.table.q11 = 3 ∧
      ((shadow.coarse.rows.emptyEven = 8 ∧
          fiveOrSix shadow.coarse.columns.emptyEven ∧
          shadow.coarse.columns.emptyOdd = 8) ∨
        (shadow.coarse.rows.emptyOdd = 8 ∧
          fiveOrSix shadow.coarse.columns.emptyOdd ∧
          shadow.coarse.columns.emptyEven = 8))) ∨
    (shadow.coarse.color0 = 7 ∧ shadow.table.q10 = 3 ∧
      ((shadow.coarse.rows.emptyEven = 8 ∧
          fiveOrSix shadow.coarse.columns.emptyOdd ∧
          shadow.coarse.columns.emptyEven = 8) ∨
        (shadow.coarse.rows.emptyOdd = 8 ∧
          fiveOrSix shadow.coarse.columns.emptyEven ∧
          shadow.coarse.columns.emptyOdd = 8)))

def Shadow.hasBichromaticObstruction (shadow : Shadow) : Prop :=
  shadow.standardRowRecipe ∨ shadow.exceptionalRowRecipe

instance (shadow : Shadow) : Decidable shadow.standardRowRecipe := by
  unfold Shadow.standardRowRecipe sevenOrEight
  infer_instance

instance (shadow : Shadow) : Decidable shadow.exceptionalRowRecipe := by
  unfold Shadow.exceptionalRowRecipe fiveOrSix
  infer_instance

instance (shadow : Shadow) : Decidable shadow.hasBichromaticObstruction := by
  unfold Shadow.hasBichromaticObstruction
  infer_instance

def rawBichromaticRecipesHold : Bool :=
  rawShadows.all fun shadow =>
    !shadow.bichromaticCore || decide shadow.hasBichromaticObstruction

set_option maxRecDepth 1000000 in
set_option maxHeartbeats 1000000000 in
/-- Exact kernel reduction of all 32 bichromatic raw records to one of the
three obstruction forms above. -/
theorem raw_bichromatic_recipes_hold : rawBichromaticRecipesHold = true := by
  decide

theorem mem_rawShadows_bichromatic_obstruction
    {shadow : Shadow} (member : shadow ∈ rawShadows)
    (bichromatic : shadow.bichromaticCore = true) :
    shadow.hasBichromaticObstruction := by
  have checked :=
    (List.all_eq_true.mp raw_bichromatic_recipes_hold) shadow member
  have decided : decide shadow.hasBichromaticObstruction = true := by
    simpa [bichromatic] using checked
  exact of_decide_eq_true decided

end Q26GridAnnihilator
