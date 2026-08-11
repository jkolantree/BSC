import Mathlib

/-!
# Q26 monochromatic endpoint arithmetic

This module isolates the final integer calculation in the proposed
monochromatic-support argument.  It deliberately does not assume that the
support thresholds or the two residual difference labels arise from a board;
that geometric bridge belongs in a separate module.

For the normalized Q26 monochromatic configuration, the support calculation
has an even threshold `h` with `0 < h <= 12` and a residual label `a` with
`a <= 13`.  The second-moment identity is equivalent to

`(2*a - 13)^2 + 12*(2*h - 13)^2 = 741`.

The theorem below checks, in the kernel, that this equation has no admissible
solution.  No solver, native evaluator, or project-defined axiom is used.
-/

set_option autoImplicit false

namespace Q26GridAnnihilator

/-- The expanded shell moment and the compact Diophantine form are exactly
equivalent.  All variables are integers so there is no truncated subtraction.
-/
theorem monochromatic_moment_normalization (a h : ℤ) :
    24 * h ^ 2 - 312 * h + 3859 + (a - 1) ^ 2 + (12 - a) ^ 2 = 3276 ↔
      (2 * a - 13) ^ 2 + 12 * (2 * h - 13) ^ 2 = 741 := by
  constructor <;> intro equality <;> nlinarith

/-- The separate zero-threshold shell already violates the fixed second
moment (`4004` instead of `3276`). -/
theorem monochromatic_zero_threshold_contradiction
    (moment : (4004 : ℤ) = 3276) : False := by
  norm_num at moment

/-- There is no admissible Q26 solution of the monochromatic endpoint
equation.  The finite cases are small enough for ordinary kernel reduction;
`native_decide` and `bv_decide` are intentionally not used. -/
theorem no_q26_monochromatic_endpoint
    (a h : ℤ)
    (aLower : 0 ≤ a) (aUpper : a ≤ 13)
    (hPositive : 0 < h) (hUpper : h ≤ 12)
    (equation : (2 * a - 13) ^ 2 + 12 * (2 * h - 13) ^ 2 = 741) : False := by
  interval_cases h <;> interval_cases a <;> norm_num at equation

end Q26GridAnnihilator
