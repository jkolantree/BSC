import BscCore

/-!
# Axiom audit

Run this file directly after `lake build`.  Lean prints the transitive axioms of
the public boundary theorems.  The README records the expected standard Lean
axioms; any project-specific axiom is a release blocker.
-/

#print axioms BscCore.Readiness.refines_antisymm
#print axioms BscCore.ActiveReadiness.le_meet
#print axioms BscCore.Axis.notApplicable_not_refines_applicable
#print axioms BscCore.HomogeneousCapSystem.greatestFeasible_fixed
#print axioms BscCore.HomogeneousCapSystem.greatestFeasible_isGreatest
#print axioms BscCore.HomogeneousCapSystem.descendingSequence_stabilizes
#print axioms BscCore.HomogeneousCapSystem.exists_descendingSequence_eq_greatestFeasible
#print axioms BscCore.identifies_iff_factors_through_attainable
#print axioms BscCore.identifies_iff_existsUnique_factors_through_attainable
#print axioms BscCore.identifiesFrom_iff_finset_cover
#print axioms BscCore.Approximate.oscillation_mono
#print axioms BscCore.Approximate.oscillation_mono_tolerance
#print axioms BscCore.Examples.exactBoolReport_identifies
