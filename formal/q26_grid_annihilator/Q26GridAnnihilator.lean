import Q26GridAnnihilator.Basic
import Q26GridAnnihilator.Polynomial
import Q26GridAnnihilator.OccurrenceAlgebra
import Q26GridAnnihilator.MomentAlgebra
import Q26GridAnnihilator.CoordinateSets
import Q26GridAnnihilator.ColorBridge
import Q26GridAnnihilator.GridMoment
import Q26GridAnnihilator.Profiles
import Q26GridAnnihilator.Conditional
import Q26GridAnnihilator.Unconditional
import Q26GridAnnihilator.Definitive

/-!
# Q26 color-split grid-annihilator formalization

This root module collects both the earlier five-profile conditional theorem
and the unrestricted theorem `no_thirteen_queen_dominator`.  The latter maps
an arbitrary thirteen-queen dominator to the exact 36-entry parity-shadow
roster, closes the 32 bichromatic entries with occurrence-polynomial moments,
and closes the four monochromatic entries with the normalized diagonal shell.

The definitive theorem `q26_domination_exact` combines that obstruction with
an explicit, kernel-checked fourteen-queen dominating set and a finite-padding
argument.  It states directly that a fourteen-queen dominator exists and that
every dominator has cardinality at least fourteen.

The unrestricted root-CNF certificate status is a separate evidentiary track
and remains `UNKNOWN` unless that exact CNF receives an independently replayed
proof certificate.
-/
