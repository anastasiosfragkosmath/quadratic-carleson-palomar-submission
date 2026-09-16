import QuadraticCarleson.NegativePrincipalValueEndpoints
import QuadraticCarleson.LacunaryEndpointDirectResolved
import QuadraticCarleson.PositiveFullMaximalMeasurability

/-!
# Comparator challenge statements

This module contains the four paper-facing statements checked by Comparator.
Its four theorem bodies are intentional specification placeholders. The
corresponding completed proofs are supplied by `Solution.lean`, which imports
the formalization itself.
-/

open MeasureTheory
open scoped ENNReal

namespace QuadraticCarleson.PaperTheorems

open PositivePrincipalValueEndpoints

set_option autoImplicit false

/-- Lacunary failure below `t log₂ t`. -/
theorem lacunary_sub_log2_modular_failure
    (Phi : YoungFunction) (hPhi : GrowsSlowerThanEndpoint Phi) :
    ¬HasFunctionPhiModularEstimate Phi lacunaryPrincipalValueMaximal := by
  sorry

/-- The resulting full-modulation failure below `t log₂ t`. -/
theorem full_sub_log2_modular_failure
    (Phi : YoungFunction) (hPhi : GrowsSlowerThanEndpoint Phi) :
    ¬HasFunctionPhiModularEstimate Phi fullPrincipalValueMaximal := by
  sorry

/-- Full-modulation `L log L` endpoint. -/
theorem full_LlogL_endpoint :
    ∃ K : ℝ≥0∞, K < ∞ ∧ ∀ f : L0Infinity,
      (∀ᵐ x, ∀ lam : ℝ,
        HasQuadraticPrincipalValue lam f x (principalValueRepresentative lam f x)) ∧
      ∀ α : ℝ, 0 < α →
        volume {x | ENNReal.ofReal α < fullPrincipalValueMaximal f x} ≤
          K * ∫⁻ x, ENNReal.ofReal ((‖f x‖ / α) * paperLog 1 (‖f x‖ / α)) := by
  sorry

/-- Lacunary `L (log₂ L)² log₄ L` endpoint. -/
theorem lacunary_log2_squared_log4_endpoint :
    ∃ K : ℝ≥0∞, K < ∞ ∧ ∀ f : L0Infinity,
      (∀ᵐ x, ∀ m : ℤ, HasQuadraticPrincipalValue (dyadicModulation m) f x
        (principalValueRepresentative (dyadicModulation m) f x)) ∧
      ∀ α : ℝ, 0 < α →
        volume {x | ENNReal.ofReal α < lacunaryPrincipalValueMaximal f x} ≤
          K * ∫⁻ x, ENNReal.ofReal
            ((‖f x‖ / α) * paperLog 2 (‖f x‖ / α) ^ 2 * paperLog 4 (‖f x‖ / α)) := by
  sorry

end QuadraticCarleson.PaperTheorems
