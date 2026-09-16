/-
Copyright (c) 2026 Quadratic Carleson formalization contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.

This file is the compact Challenge statement surface. Its four deliberate
statement holes are used only for Comparator's independent comparison.
-/

import Mathlib

/-!
# Exact endpoint claims for Stein's purely quadratic Carleson operator

This Mathlib-only file records four endpoint claims from Fragkos--Krause--
Lacey, *Endpoint Estimates for Stein's Purely Quadratic Carleson Operator*,
arXiv:2609.04101v1. The definitions in
`QuadraticCarleson.StatementSurface` give the operator and endpoint statements
being audited; `Solution.lean` proves the same declarations from the
substantive development.
-/

open Filter MeasureTheory Set
open scoped ENNReal Topology

namespace QuadraticCarleson

/-- A Young function with the regularity and growth alternatives used here. -/
structure YoungFunction where
  toFun : ℝ → ℝ
  continuousOn_nonneg : ContinuousOn toFun (Ici 0)
  convexOn_nonneg : ConvexOn ℝ (Ici 0) toFun
  strictMonoOn_nonneg : StrictMonoOn toFun (Ici 0)
  map_zero : toFun 0 = 0
  identity_or_superlinear :
    (∀ t ∈ Ici (0 : ℝ), toFun t = t) ∨
      Tendsto (fun t : ℝ => toFun t / t) atTop atTop

instance : CoeFun YoungFunction (fun _ => ℝ → ℝ) := ⟨YoungFunction.toFun⟩

/-- A bounded, measurable, compactly supported complex-valued function. -/
structure L0Infinity where
  toFun : ℝ → ℂ
  measurable_toFun : Measurable toFun
  bounded_toFun : ∃ C : ℝ, ∀ x, ‖toFun x‖ ≤ C
  hasCompactSupport_toFun : HasCompactSupport toFun

instance : CoeFun L0Infinity (fun _ => ℝ → ℂ) := ⟨L0Infinity.toFun⟩

namespace StatementSurface

/-- The quadratic oscillatory phase `exp(2π i s)`. -/
noncomputable def phase (s : ℝ) : ℂ :=
  Complex.exp (((2 * Real.pi * s : ℝ) : ℂ) * Complex.I)

/-- The iterated logarithm convention used in the endpoint estimates. -/
noncomputable def paperLog : ℕ → ℝ → ℝ
  | 0 => id
  | n + 1 => fun t => Real.log (10 + paperLog n t)

/-- Growth strictly below the endpoint Young function `t log₂ t`. -/
def GrowsSlowerThanEndpoint (Phi : YoungFunction) : Prop :=
  (fun t : ℝ => Phi t) =o[atTop] (fun t : ℝ => t * paperLog 2 t)

/-- The symmetrically truncated oscillatory quadratic Hilbert integral. -/
noncomputable def quadraticHilbertTrunc
    (modulation epsilon : ℝ) (f : ℝ → ℂ) (x : ℝ) : ℂ :=
  ∫ t in {t : ℝ | epsilon < |t|}, f (x - t) * phase (modulation * t ^ 2) / (t : ℂ)

/-- The existence of the symmetric principal value of the truncated integral. -/
def HasQuadraticPrincipalValue (modulation : ℝ) (f : ℝ → ℂ) (x : ℝ) (z : ℂ) : Prop :=
  Tendsto (fun epsilon : ℝ => quadraticHilbertTrunc modulation epsilon f x)
    (nhdsWithin 0 (Ioi 0)) (nhds z)

/-- The dyadic modulation `2^n` for an integer exponent. -/
noncomputable def dyadicModulation (n : ℤ) : ℝ :=
  (2 : ℝ) ^ n

/-- The principal-value value where it exists, and zero otherwise. -/
noncomputable def principalValueRepresentative (lam : ℝ) (f : L0Infinity) (x : ℝ) : ℂ := by
  classical
  exact if h : ∃ z : ℂ, HasQuadraticPrincipalValue lam f x z then h.choose else 0

/-- The full-modulation principal-value maximal operator. -/
noncomputable def fullPrincipalValueMaximal (f : L0Infinity) (x : ℝ) : ℝ≥0∞ :=
  ⨆ lam : ℝ, ENNReal.ofReal ‖principalValueRepresentative lam f x‖

/-- The dyadically lacunary principal-value maximal operator. -/
noncomputable def lacunaryPrincipalValueMaximal (f : L0Infinity) (x : ℝ) : ℝ≥0∞ :=
  ⨆ m : ℤ, ENNReal.ofReal ‖principalValueRepresentative (dyadicModulation m) f x‖

/-- The strict level set of an operator applied to a function. -/
def functionOperatorLevelSet
    (T : L0Infinity → ℝ → ℝ≥0∞) (f : L0Infinity) (alpha : ℝ) : Set ℝ :=
  {x | ENNReal.ofReal alpha < T f x}

/-- The weak modular estimate with Young function `Phi` for an operator `T`. -/
def HasFunctionPhiModularEstimate
    (Phi : YoungFunction) (T : L0Infinity → ℝ → ℝ≥0∞) : Prop :=
  ∃ C : ℝ, 0 < C ∧ ∀ (f : L0Infinity) (alpha : ℝ), 0 < alpha →
    volume (functionOperatorLevelSet T f alpha) ≤
      ENNReal.ofReal C * ∫⁻ x : ℝ, ENNReal.ofReal (Phi (‖f x‖ / alpha))

namespace PaperTheorems

set_option autoImplicit false

/-- Failure of a lacunary modular estimate below `t log₂ t`. -/
theorem lacunary_sub_log2_modular_failure
    (Phi : YoungFunction) (hPhi : GrowsSlowerThanEndpoint Phi) :
    ¬HasFunctionPhiModularEstimate Phi lacunaryPrincipalValueMaximal := by
  sorry

/-- Failure of a full-modulation modular estimate below `t log₂ t`. -/
theorem full_sub_log2_modular_failure
    (Phi : YoungFunction) (hPhi : GrowsSlowerThanEndpoint Phi) :
    ¬HasFunctionPhiModularEstimate Phi fullPrincipalValueMaximal := by
  sorry

/-- The full-modulation `L log L` endpoint estimate. -/
theorem full_LlogL_endpoint :
    ∃ K : ℝ≥0∞, K < ∞ ∧ ∀ f : L0Infinity,
      (∀ᵐ x, ∀ lam : ℝ,
        HasQuadraticPrincipalValue lam f x (principalValueRepresentative lam f x)) ∧
      ∀ α : ℝ, 0 < α →
        volume {x | ENNReal.ofReal α < fullPrincipalValueMaximal f x} ≤
          K * ∫⁻ x, ENNReal.ofReal ((‖f x‖ / α) * paperLog 1 (‖f x‖ / α)) := by
  sorry

/-- The lacunary `L (log₂ L)² log₄ L` endpoint estimate. -/
theorem lacunary_log2_squared_log4_endpoint :
    ∃ K : ℝ≥0∞, K < ∞ ∧ ∀ f : L0Infinity,
      (∀ᵐ x, ∀ m : ℤ, HasQuadraticPrincipalValue (dyadicModulation m) f x
        (principalValueRepresentative (dyadicModulation m) f x)) ∧
      ∀ α : ℝ, 0 < α →
        volume {x | ENNReal.ofReal α < lacunaryPrincipalValueMaximal f x} ≤
          K * ∫⁻ x, ENNReal.ofReal
            ((‖f x‖ / α) * paperLog 2 (‖f x‖ / α) ^ 2 * paperLog 4 (‖f x‖ / α)) := by
  sorry

end PaperTheorems
end StatementSurface
end QuadraticCarleson
