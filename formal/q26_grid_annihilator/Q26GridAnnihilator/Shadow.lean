import Mathlib

/-!
# The unrestricted finite Q26 parity shadow

This module contains only finite arithmetic.  It deliberately admits zero
empty-line parity classes and does not claim that an arbitrary dominating
queen set has been connected to one of these records.

The four entries of `ShadowQTable` count queens by row/column parity.  A
`CoarseShadow` records the color-0 total and the numbers of distinct occupied
lines of both parities.  The raw enumeration imposes only:

* thirteen queen occurrences;
* support sizes compatible with the four occurrence margins; and
* every exact top-coefficient CN alternative on the four empty grids.

Kernel reduction classifies the resulting over-approximation into four rigid
monochromatic records and thirty-two bichromatic records.  In every
bichromatic record the color split is `6/7`, every empty-line parity class is
nonempty, and the row and column repetition excesses are at most one.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

def shadowBoardHalf : Nat := 13

/-- Numbers of distinct occupied even and odd lines in one direction. -/
structure ShadowSupport where
  even : Nat
  odd : Nat
  deriving DecidableEq, Repr

/-- Every physically possible support-size pair for thirteen occurrences. -/
def shadowSupportPairs : List ShadowSupport :=
  (List.range (shadowBoardHalf + 1)).flatMap fun even =>
    (List.range (shadowBoardHalf + 1 - even)).map fun odd =>
      { even := even, odd := odd }

/-- Membership form used by the later actual-board bridge. -/
theorem mem_shadowSupportPairs_iff (support : ShadowSupport) :
    support ∈ shadowSupportPairs ↔
      support.even + support.odd ≤ shadowBoardHalf := by
  constructor
  · intro member
    rw [shadowSupportPairs, List.mem_flatMap] at member
    rcases member with ⟨even, evenRange, member⟩
    rw [List.mem_map] at member
    rcases member with ⟨odd, oddRange, definition⟩
    simp only [List.mem_range] at evenRange oddRange
    rw [← definition]
    simp only
    omega
  · intro supportBound
    rw [shadowSupportPairs, List.mem_flatMap]
    refine ⟨support.even, ?_, ?_⟩
    · simp only [List.mem_range]
      omega
    · rw [List.mem_map]
      refine ⟨support.odd, ?_, ?_⟩
      · simp only [List.mem_range]
        omega
      · cases support
        rfl

def ShadowSupport.emptyEven (support : ShadowSupport) : Nat :=
  shadowBoardHalf - support.even

def ShadowSupport.emptyOdd (support : ShadowSupport) : Nat :=
  shadowBoardHalf - support.odd

def ShadowSupport.excess (support : ShadowSupport) : Nat :=
  shadowBoardHalf - (support.even + support.odd)

/-- The numerical shadow before choosing the four-cell incidence table. -/
structure CoarseShadow where
  color0 : Nat
  rows : ShadowSupport
  columns : ShadowSupport
  deriving DecidableEq, Repr

def CoarseShadow.color1 (shadow : CoarseShadow) : Nat :=
  shadowBoardHalf - shadow.color0

/-- The literal family of exact top-coefficient CN alternatives for a grid. -/
def shadowCNGridAlternatives (rowCount columnCount queenCount : Nat) : Bool :=
  (List.range (queenCount + 1)).all fun j =>
    decide
      (rowCount <= 2 * (queenCount - j) \/
        columnCount <= 2 * j)

def shadowCeilHalf (count : Nat) : Nat :=
  (count + 1) / 2

/-- Closed form of `shadowCNGridAlternatives`.  Empty grids are retained as
vacuous; on a positive grid this is the exact ceiling-sum inequality. -/
def shadowCNGridOK (rowCount columnCount queenCount : Nat) : Bool :=
  if rowCount = 0 || columnCount = 0 then
    true
  else
    decide
      (shadowCeilHalf rowCount + shadowCeilHalf columnCount <= queenCount + 1)

/-- Exhaustive Q26-range check that the closed form used by the shadow
enumeration is exactly the literal CN family. -/
def shadowCNFormsAgree : Bool :=
  (List.range (shadowBoardHalf + 1)).all fun rowCount =>
    (List.range (shadowBoardHalf + 1)).all fun columnCount =>
      (List.range (shadowBoardHalf + 1)).all fun queenCount =>
        shadowCNGridOK rowCount columnCount queenCount =
          shadowCNGridAlternatives rowCount columnCount queenCount

/-- All four same-color empty-grid alternatives, with zero grids retained. -/
def coarseShadowCNOK (shadow : CoarseShadow) : Bool :=
  shadowCNGridOK shadow.rows.emptyEven shadow.columns.emptyEven
      shadow.color0 &&
    shadowCNGridOK shadow.rows.emptyOdd shadow.columns.emptyOdd
      shadow.color0 &&
    shadowCNGridOK shadow.rows.emptyEven shadow.columns.emptyOdd
      shadow.color1 &&
    shadowCNGridOK shadow.rows.emptyOdd shadow.columns.emptyEven
      shadow.color1

def coarseShadowSurvivors : List CoarseShadow :=
  (List.range (shadowBoardHalf + 1)).flatMap fun color0 =>
    shadowSupportPairs.flatMap fun rows =>
      (shadowSupportPairs.filter fun columns =>
        coarseShadowCNOK { color0 := color0, rows := rows, columns := columns }).map
          fun columns => { color0 := color0, rows := rows, columns := columns }

/-- Queen incidences in the four row/column parity cells. -/
structure ShadowQTable where
  q00 : Nat
  q01 : Nat
  q10 : Nat
  q11 : Nat
  deriving DecidableEq, Repr

/-- All four-part compositions of thirteen, generated without a sum filter. -/
def shadowQTables : List ShadowQTable :=
  (List.range (shadowBoardHalf + 1)).flatMap fun q00 =>
    (List.range (shadowBoardHalf + 1 - q00)).flatMap fun q01 =>
      (List.range (shadowBoardHalf + 1 - q00 - q01)).map fun q10 =>
        { q00 := q00
          q01 := q01
          q10 := q10
          q11 := shadowBoardHalf - q00 - q01 - q10 }

/-- Membership form used by the later actual-board bridge. -/
theorem mem_shadowQTables_iff (table : ShadowQTable) :
    table ∈ shadowQTables ↔
      table.q00 + table.q01 + table.q10 + table.q11 = shadowBoardHalf := by
  constructor
  · intro member
    rw [shadowQTables, List.mem_flatMap] at member
    rcases member with ⟨q00, q00Range, member⟩
    rw [List.mem_flatMap] at member
    rcases member with ⟨q01, q01Range, member⟩
    rw [List.mem_map] at member
    rcases member with ⟨q10, q10Range, definition⟩
    simp only [List.mem_range] at q00Range q01Range q10Range
    rw [← definition]
    simp only
    omega
  · intro tableSum
    rw [shadowQTables, List.mem_flatMap]
    refine ⟨table.q00, ?_, ?_⟩
    · simp only [List.mem_range]
      omega
    · rw [List.mem_flatMap]
      refine ⟨table.q01, ?_, ?_⟩
      · simp only [List.mem_range]
        omega
      · rw [List.mem_map]
        refine ⟨table.q10, ?_, ?_⟩
        · simp only [List.mem_range]
          omega
        · cases table
          congr 1
          rw [Nat.sub_sub, Nat.sub_sub]
          exact (Nat.eq_sub_of_add_eq'
            (by simpa [Nat.add_assoc] using tableSum)).symm

def ShadowQTable.color0 (table : ShadowQTable) : Nat :=
  table.q00 + table.q11

def ShadowQTable.rowEven (table : ShadowQTable) : Nat :=
  table.q00 + table.q01

def ShadowQTable.rowOdd (table : ShadowQTable) : Nat :=
  table.q10 + table.q11

def ShadowQTable.columnEven (table : ShadowQTable) : Nat :=
  table.q00 + table.q10

def ShadowQTable.columnOdd (table : ShadowQTable) : Nat :=
  table.q01 + table.q11

/-- A support is empty exactly when its occurrence margin is empty; otherwise
it contains between one and all of the occurrences. -/
def shadowSupportValid (support occurrences : Nat) : Bool :=
  decide
    ((occurrences = 0 /\ support = 0) \/
      (0 < occurrences /\ 0 < support /\ support <= occurrences))

def shadowTableFits (coarse : CoarseShadow) (table : ShadowQTable) : Bool :=
  decide (table.color0 = coarse.color0) &&
    shadowSupportValid coarse.rows.even table.rowEven &&
    shadowSupportValid coarse.rows.odd table.rowOdd &&
    shadowSupportValid coarse.columns.even table.columnEven &&
    shadowSupportValid coarse.columns.odd table.columnOdd

/-- A complete numerical parity shadow.  No board realization is asserted. -/
structure Shadow where
  coarse : CoarseShadow
  table : ShadowQTable
  deriving DecidableEq, Repr

def shadowsFor (coarse : CoarseShadow) : List Shadow :=
  (shadowQTables.filter (shadowTableFits coarse)).map fun table =>
    { coarse := coarse, table := table }

def rawShadows : List Shadow :=
  coarseShadowSurvivors.flatMap shadowsFor

def CoarseShadow.emptyParitiesPositive (shadow : CoarseShadow) : Bool :=
  decide
    (0 < shadow.rows.emptyEven /\ 0 < shadow.rows.emptyOdd /\
      0 < shadow.columns.emptyEven /\ 0 < shadow.columns.emptyOdd)

def CoarseShadow.monochromatic (shadow : CoarseShadow) : Bool :=
  decide (shadow.color0 = 0 \/ shadow.color0 = shadowBoardHalf)

def CoarseShadow.bichromaticCore (shadow : CoarseShadow) : Bool :=
  decide
    ((shadow.color0 = 6 \/ shadow.color0 = 7) /\
      shadow.emptyParitiesPositive = true /\
      shadow.rows.excess <= 1 /\ shadow.columns.excess <= 1)

/-- The four zero-grid survivors have one occupied parity in each direction,
with all thirteen incidences in the corresponding table cell. -/
def Shadow.monochromaticStandard (shadow : Shadow) : Bool :=
  shadow.coarse.monochromatic &&
    decide
      (shadow.coarse.rows.excess = 0 /\
        shadow.coarse.columns.excess = 0 /\
        shadow.coarse.rows.even = shadow.table.rowEven /\
        shadow.coarse.rows.odd = shadow.table.rowOdd /\
        shadow.coarse.columns.even = shadow.table.columnEven /\
        shadow.coarse.columns.odd = shadow.table.columnOdd)

def Shadow.bichromaticCore (shadow : Shadow) : Bool :=
  shadow.coarse.bichromaticCore

def Shadow.hasClassifiedRecipe (shadow : Shadow) : Bool :=
  shadow.monochromaticStandard || shadow.bichromaticCore

def monochromaticShadows : List Shadow :=
  rawShadows.filter Shadow.monochromaticStandard

def bichromaticShadows : List Shadow :=
  rawShadows.filter Shadow.bichromaticCore

structure CoarseShadowStats where
  survivors : Nat
  zeroParity : Nat
  deriving DecidableEq, Repr

def addCoarseShadow (stats : CoarseShadowStats)
    (shadow : CoarseShadow) : CoarseShadowStats where
  survivors := stats.survivors + 1
  zeroParity := stats.zeroParity + if shadow.emptyParitiesPositive then 0 else 1

def coarseShadowStats : CoarseShadowStats :=
  coarseShadowSurvivors.foldl addCoarseShadow
    { survivors := 0, zeroParity := 0 }

/-- One traversal records the exact raw classification and excess histogram. -/
structure RawShadowStats where
  survivors : Nat
  monochromatic : Nat
  bichromatic : Nat
  excess00 : Nat
  excess10 : Nat
  excess01 : Nat
  excess11 : Nat
  everyRecordClassified : Bool
  deriving DecidableEq, Repr

def addRawShadow (stats : RawShadowStats) (shadow : Shadow) : RawShadowStats :=
  let monochromatic := shadow.monochromaticStandard
  let bichromatic := shadow.bichromaticCore
  let classified := shadow.hasClassifiedRecipe
  let rowExcess := shadow.coarse.rows.excess
  let columnExcess := shadow.coarse.columns.excess
  { survivors := stats.survivors + 1
    monochromatic := stats.monochromatic + if monochromatic then 1 else 0
    bichromatic := stats.bichromatic + if bichromatic then 1 else 0
    excess00 := stats.excess00 + if rowExcess = 0 && columnExcess = 0 then 1 else 0
    excess10 := stats.excess10 + if rowExcess = 1 && columnExcess = 0 then 1 else 0
    excess01 := stats.excess01 + if rowExcess = 0 && columnExcess = 1 then 1 else 0
    excess11 := stats.excess11 + if rowExcess = 1 && columnExcess = 1 then 1 else 0
    everyRecordClassified :=
      stats.everyRecordClassified && classified }

theorem foldl_addRawShadow_every (records : List Shadow)
    (stats : RawShadowStats) :
    (records.foldl addRawShadow stats).everyRecordClassified =
      (stats.everyRecordClassified &&
        records.all Shadow.hasClassifiedRecipe) := by
  induction records generalizing stats with
  | nil => simp
  | cons head tail inductionHypothesis =>
      rw [List.foldl_cons, inductionHypothesis]
      simp [addRawShadow, Bool.and_assoc]

def rawShadowStats : RawShadowStats :=
  rawShadows.foldl addRawShadow
    { survivors := 0
      monochromatic := 0
      bichromatic := 0
      excess00 := 0
      excess10 := 0
      excess01 := 0
      excess11 := 0
      everyRecordClassified := true }

/-- Combined traversal: the coarse CN enumeration is reduced only once while
also accumulating all supported incidence-table lifts. -/
structure ExactShadowStats where
  coarse : CoarseShadowStats
  raw : RawShadowStats
  deriving DecidableEq, Repr

def addCoarseAndRaw (stats : ExactShadowStats)
    (coarse : CoarseShadow) : ExactShadowStats where
  coarse := addCoarseShadow stats.coarse coarse
  raw := (shadowsFor coarse).foldl addRawShadow stats.raw

def exactShadowStats : ExactShadowStats :=
  coarseShadowSurvivors.foldl addCoarseAndRaw
    { coarse := { survivors := 0, zeroParity := 0 }
      raw :=
        { survivors := 0
          monochromatic := 0
          bichromatic := 0
          excess00 := 0
          excess10 := 0
          excess01 := 0
          excess11 := 0
          everyRecordClassified := true } }

theorem foldl_addCoarseAndRaw_every (records : List CoarseShadow)
    (stats : ExactShadowStats) :
    (records.foldl addCoarseAndRaw stats).raw.everyRecordClassified =
      (stats.raw.everyRecordClassified &&
        records.all fun coarse =>
          (shadowsFor coarse).all Shadow.hasClassifiedRecipe) := by
  induction records generalizing stats with
  | nil => simp
  | cons head tail inductionHypothesis =>
      rw [List.foldl_cons, inductionHypothesis]
      simp only [addCoarseAndRaw, foldl_addRawShadow_every]
      simp [Bool.and_assoc]

set_option maxRecDepth 100000 in
theorem shadow_cn_forms_agree : shadowCNFormsAgree = true := by
  decide

theorem shadow_support_pair_count : shadowSupportPairs.length = 105 := by
  decide

set_option maxRecDepth 100000 in
theorem shadow_qtable_count : shadowQTables.length = 560 := by
  decide

set_option maxRecDepth 1000000 in
set_option maxHeartbeats 1000000000 in
/-- Exact kernel-reduced audit: 32 bichromatic plus four monochromatic raw
records, with no positivity premise built into the enumeration. -/
theorem exact_shadow_stats :
    exactShadowStats =
      { coarse := { survivors := 40, zeroParity := 4 }
        raw :=
          { survivors := 36
            monochromatic := 4
            bichromatic := 32
            excess00 := 12
            excess10 := 8
            excess01 := 8
            excess11 := 8
            everyRecordClassified := true } } := by
  decide

/-- Membership-friendly form of the exact classification. -/
theorem mem_rawShadows_recipe {shadow : Shadow}
    (member : shadow ∈ rawShadows) :
    shadow.monochromaticStandard = true \/
      shadow.bichromaticCore = true := by
  have finalEvery :
      exactShadowStats.raw.everyRecordClassified = true := by
    rw [exact_shadow_stats]
  rw [exactShadowStats, foldl_addCoarseAndRaw_every] at finalEvery
  have allCoarse :
      coarseShadowSurvivors.all (fun coarse =>
        (shadowsFor coarse).all Shadow.hasClassifiedRecipe) = true := by
    simpa using finalEvery
  rw [rawShadows, List.mem_flatMap] at member
  rcases member with ⟨coarse, coarseMember, shadowMember⟩
  have allForCoarse :=
    (List.all_eq_true.mp allCoarse) coarse coarseMember
  have recipe :=
    (List.all_eq_true.mp allForCoarse) shadow shadowMember
  simpa only [Shadow.hasClassifiedRecipe, Bool.or_eq_true] using recipe

end Q26GridAnnihilator
