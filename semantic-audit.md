# Semantic correspondence with the article

This document records the current statement-level correspondence between the
Lean development and [*Endpoint Estimates for Stein's Purely Quadratic
Carleson Operator*](https://arxiv.org/abs/2609.04101v1). It is a guide to the
written Lean theorem types, not a substitute for reading those types or for the
build and axiom evidence in [the verification report](verification-report.md).

## Headline results

The public review entry point is
[`QuadraticCarleson/PaperTheorems.lean`](../QuadraticCarleson/PaperTheorems.lean).
Its headline declarations have the following correspondence.

| Article result | Lean declarations | Scope of the written Lean statements |
| --- | --- | --- |
| Failure below `t log₂ t` | `lacunary_sub_log2_modular_failure`, `full_sub_log2_modular_failure` | For every `YoungFunction` with the stated little-o growth condition, the relevant principal-value maximal operator has no corresponding modular estimate. The full-modulation conclusion is a separate theorem for the full operator. |
| Unit-height counterexamples | `lacunary_counterexample_at_unit_height`, `full_counterexample_at_unit_height` | For every `0 < κ < 1`, each declaration provides an input whose modular mass is strictly below `κ` times the strict unit-height level-set measure. |
| Full-modulation positive endpoint | `full_LlogL_endpoint` | One finite constant works for every `L0Infinity` input and every positive threshold, with the `L log₁ L` modular. The statement includes almost-everywhere existence of the principal values for every real modulation. |
| Lacunary positive endpoint | `lacunary_log2_squared_log4_endpoint` | One finite constant works for every `L0Infinity` input and every positive threshold, with the `L (log₂ L)² log₄ L` modular. The statement includes almost-everywhere existence of the principal values for every dyadic modulation. |

The first, third, and fourth rows are the three principal results highlighted
in the README. The full-modulation negative result is the consequence paired
with the lacunary negative theorem in the first row.

## Other article-facing declarations

The development also exposes the following reviewable declarations.

| Article-facing item | Lean declaration | Written scope |
| --- | --- | --- |
| Weak-`(1,1)` failures | `lacunary_not_weakOneOne`, `full_not_weakOneOne` | Consequences of the negative modular results for the same principal-value maximal operators. |
| Measurability | `principalValueMaxima_aemeasurable` | Almost-everywhere measurability of both headline maximal operators. |
| Finite-modulation weak estimate | `finite_modulation_blocks_weakOneOne` | A weak bound for an arbitrary finite family of signed nonzero real modulations; the finite-family cardinality remains outside the operator. |
| Off-support estimate | `offSupportPaperLemma` | The two paper-facing off-support bounds, including the displayed maximum error and the stated modulation restrictions. |
| Bohr-set intersection | `bohrSet_inter_volume_real_le` | The stated positive-frequency, small-radius intersection estimate. |
| Dyadic Bohr-union estimate | `dyadicBohrLogUnion_volume_real_ge`, `dyadicBohrLogUnion_volume_real_ge_uniform` | The real logarithmic-window lower bounds used in the development. |
| Finite sparse maximal estimate | `weak11sparseStatement_proof`, `finiteSparseMaximal_hasWeakOneOneBound` | The finite sublinear-family estimate under its explicit sparse-growth hypothesis. |

## Verification boundary

The source-policy audit and the explicit axiom audit are described in the
[verification report](verification-report.md). The manual Comparator workflow
checks exactly four declarations: the two negative endpoint declarations and
the two positive endpoint declarations listed in the headline table. Its
statement specifications are intentionally isolated in `Challenge.lean`; their
four placeholders are not completed proofs and are built separately by the
manual Comparator workflow.

The development formalizes the quadratic estimates and constructions used for
these declarations. It does not claim to formalize every auxiliary result in
the article's historical survey or every result cited from other work. In
particular, an auxiliary declaration with an explicit hypothesis should be read
according to that hypothesis; it is not evidence that the hypothesis has been
proved elsewhere in this repository.

For the exact Lean types and their imports, inspect
[`QuadraticCarleson/PaperTheorems.lean`](../QuadraticCarleson/PaperTheorems.lean).
For reproducible build and audit commands, see the
[verification report](verification-report.md).
