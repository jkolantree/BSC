import Q26GridAnnihilator.Basic

set_option autoImplicit false

namespace Q26GridAnnihilator

/-- Verifier-controlled statement for the external Q26 proof replay. -/
theorem no_thirteen_queen_dominator :
    ¬ ∃ queens : Finset Square, Dominates queens ∧ queens.card = 13 := by
  sorry

end Q26GridAnnihilator
