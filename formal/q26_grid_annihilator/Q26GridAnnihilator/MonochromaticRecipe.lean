import Q26GridAnnihilator.Shadow

/-!
# Exact finite recipes for the monochromatic Q26 shadows

This module contains only a finite classification of the four monochromatic
records produced by `rawShadows`.  It introduces no board geometry and makes
no claim that an arbitrary queen placement realizes one of those records.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

/-- The four possible cells containing all thirteen occurrences in a
monochromatic raw shadow. -/
inductive MonochromaticOrientation where
  | q01
  | q10
  | q11
  | q00
  deriving DecidableEq, Repr

/-- The exact raw shadow represented by an orientation.  The support pairs
also record the complementary empty-line counts: `(0, 13)` for support
`(13, 0)` and `(13, 0)` for support `(0, 13)`. -/
def MonochromaticOrientation.shadow : MonochromaticOrientation → Shadow
  | .q01 =>
      { coarse :=
          { color0 := 0
            rows := { even := 13, odd := 0 }
            columns := { even := 0, odd := 13 } }
        table := { q00 := 0, q01 := 13, q10 := 0, q11 := 0 } }
  | .q10 =>
      { coarse :=
          { color0 := 0
            rows := { even := 0, odd := 13 }
            columns := { even := 13, odd := 0 } }
        table := { q00 := 0, q01 := 0, q10 := 13, q11 := 0 } }
  | .q11 =>
      { coarse :=
          { color0 := 13
            rows := { even := 0, odd := 13 }
            columns := { even := 0, odd := 13 } }
        table := { q00 := 0, q01 := 0, q10 := 0, q11 := 13 } }
  | .q00 =>
      { coarse :=
          { color0 := 13
            rows := { even := 13, odd := 0 }
            columns := { even := 13, odd := 0 } }
        table := { q00 := 13, q01 := 0, q10 := 0, q11 := 0 } }

/-- The requested `q01`, `q10`, `q11`, `q00` orientation roster. -/
def monochromaticOrientations : List MonochromaticOrientation :=
  [.q01, .q10, .q11, .q00]

/-- All roster entries whose complete numerical shadow equals `candidate`. -/
def monochromaticOrientationMatches
    (candidate : Shadow) : List MonochromaticOrientation :=
  monochromaticOrientations.filter fun orientation =>
    decide (orientation.shadow = candidate)

/-- Finite audit predicate: every monochromatic-standard entry of the raw
enumeration has exactly one matching orientation. -/
def rawMonochromaticOrientationsExact : Bool :=
  rawShadows.all fun candidate =>
    if candidate.monochromaticStandard then
      decide ((monochromaticOrientationMatches candidate).length = 1)
    else
      true

theorem monochromatic_orientation_count :
    monochromaticOrientations.length = 4 := by
  decide

set_option maxRecDepth 1000000 in
set_option maxHeartbeats 1000000000 in
/-- Kernel reduction of the raw finite enumeration against the explicit
four-orientation roster. -/
theorem raw_monochromatic_orientations_exact :
    rawMonochromaticOrientationsExact = true := by
  decide

/-- A raw monochromatic-standard shadow has exactly one matching roster
entry. -/
theorem mem_rawShadows_monochromatic_match_count
    {candidate : Shadow} (member : candidate ∈ rawShadows)
    (monochromatic : candidate.monochromaticStandard = true) :
    (monochromaticOrientationMatches candidate).length = 1 := by
  have checked :=
    (List.all_eq_true.mp raw_monochromatic_orientations_exact) candidate member
  have decided :
      decide ((monochromaticOrientationMatches candidate).length = 1) = true := by
    simpa [monochromatic] using checked
  exact of_decide_eq_true decided

/-- Membership form of the finite classification, returning the explicit
orientation witness as well as its membership in the four-entry roster. -/
theorem mem_rawShadows_monochromatic_orientation
    {candidate : Shadow} (member : candidate ∈ rawShadows)
    (monochromatic : candidate.monochromaticStandard = true) :
    ∃ orientation,
      orientation ∈ monochromaticOrientations ∧
        orientation.shadow = candidate := by
  have matchCount :=
    mem_rawShadows_monochromatic_match_count member monochromatic
  cases matchesEquation : monochromaticOrientationMatches candidate with
  | nil =>
      rw [matchesEquation] at matchCount
      simp at matchCount
  | cons orientation tail =>
      have orientationMember :
          orientation ∈ monochromaticOrientationMatches candidate := by
        rw [matchesEquation]
        simp
      have filtered := List.mem_filter.mp orientationMember
      exact ⟨orientation, filtered.1, of_decide_eq_true filtered.2⟩

end Q26GridAnnihilator
