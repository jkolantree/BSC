import Q26GridAnnihilator.BoardShadow
import Q26GridAnnihilator.BichromaticClosure
import Q26GridAnnihilator.MonochromaticBoardBridge
import Q26GridAnnihilator.MonochromaticShell

/-!
# Unconditional thirteen-queen obstruction

This module composes the exact shadow classification with the independently
closed bichromatic and monochromatic branches.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

theorem no_thirteen_queen_dominator :
    ¬ ∃ queens : Finset Square, Dominates queens ∧ queens.card = 13 := by
  rintro ⟨queens, dominates, cardThirteen⟩
  rcases actualShadow_recipe queens dominates cardThirteen with
    monochromatic | bichromatic
  · obtain ⟨permutation, covered⟩ :=
      monochromatic_actualShadow_monoCoreCovered
        queens dominates cardThirteen monochromatic
    exact no_mono_core_covered permutation covered
  · exact no_bichromatic_actual_shadow
      queens dominates cardThirteen bichromatic

end Q26GridAnnihilator
