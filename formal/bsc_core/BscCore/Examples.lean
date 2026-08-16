import BscCore.Readiness
import BscCore.CapSystem
import BscCore.PairSeparation
import BscCore.Oscillation

/-!
# Small kernel-checked examples

These examples exercise all four theorem families without external solvers.
-/

namespace BscCore.Examples

def lowerReadiness : Readiness Nat Nat Nat Nat :=
  ⟨.applicable 1, .applicable 1, .applicable 0, .notApplicable⟩

def upperReadiness : Readiness Nat Nat Nat Nat :=
  ⟨.applicable 2, .applicable 3, .applicable 1, .notApplicable⟩

example : Readiness.Refines lowerReadiness upperReadiness := by
  simp [Readiness.Refines, Axis.Refines, lowerReadiness, upperReadiness]

example : ¬ Axis.Refines (Axis.notApplicable : Axis Nat) (.applicable 0) := by
  simp

/-- One intervention reports the Boolean completion exactly. -/
def exactBoolReport : Unit → Bool → Bool :=
  fun _ x => x

theorem exactBoolReport_covers :
    PairCover exactBoolReport id {()} := by
  intro x x' hdiff
  exact ⟨(), by simp, by simpa [exactBoolReport] using hdiff⟩

theorem exactBoolReport_identifies :
    IdentifiesFrom exactBoolReport id {()} :=
  (identifiesFrom_iff_pairCover exactBoolReport id {()}).2
    exactBoolReport_covers

/-- Discrete Boolean distance, used for the exact oscillation example. -/
def boolDistance (x x' : Bool) : Nat :=
  if x = x' then 0 else 1

def boolReportDistance : Unit → Bool → Bool → Nat :=
  fun _ => boolDistance

def zeroTolerance : Unit → Nat :=
  fun _ => 0

example :
    Approximate.oscillation boolDistance boolReportDistance zeroTolerance
      ({()} : Finset Unit) = 0 := by
  decide

example :
    Approximate.oscillation boolDistance boolReportDistance zeroTolerance
      ({()} : Finset Unit) ≤
    Approximate.oscillation boolDistance boolReportDistance zeroTolerance
      (∅ : Finset Unit) := by
  exact Approximate.oscillation_mono
    boolDistance boolReportDistance zeroTolerance (by simp)

end BscCore.Examples
