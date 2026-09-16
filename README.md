# Lean verification for *Endpoint Estimates for Stein's Purely Quadratic Carleson Operator*

A Lean 4 + Mathlib formalization of the principal endpoint results in
Anastasios Fragkos, Ben Krause, and Michael Lacey, [*Endpoint Estimates for
Stein's Purely Quadratic Carleson Operator*](https://arxiv.org/abs/2609.04101v1).

## Main results

The following main results have been formally verified in Lean:

- failure of modular estimates below $t\log_2 t$ for
  $\mathcal{C}_{2,\mathsf{lac}}$ and the resulting consequence for
  $\mathcal{C}_2$;
- the $L\log_1 L$ modular estimate for $\mathcal{C}_2$;
- the $L(\log_2 L)^2\log_4 L$ modular estimate for
  $\mathcal{C}_{2,\mathsf{lac}}$.

`lake build` compiles the core formalization with the pinned toolchain.
The source-policy checks prohibit placeholders and proof-bypass mechanisms in
the completed formalization sources. The explicit axiom audit reports only Lean
and Mathlib's standard logical axioms for the audited declarations:
`propext`, `Classical.choice`, and `Quot.sound`.

The four headline declarations are also checked by the manual
[Comparator workflow](.github/workflows/run-comparator.yml), which compares
the fixed statements in [`Challenge.lean`](Challenge.lean) with the completed
proof development made available through [`Solution.lean`](Solution.lean).
`Challenge.lean` is an isolated statement specification with four intentional
placeholders and is built separately by that workflow. Comparator checks those
four statement/proof pairs, while the regular Lean CI verifies the core build
and source-policy checks.

This repository reports local Lean verification: the included proofs are
checked by Lean's kernel with the pinned toolchain. The
[verification report](docs/verification-report.md) records the scope and
reproducible evidence for that claim.

## Main Lean declarations

The review-facing statements are collected in
[`QuadraticCarleson.PaperTheorems`](QuadraticCarleson/PaperTheorems.lean). The
three principal exports are:

- `QuadraticCarleson.PaperTheorems.full_LlogL_endpoint`
- `QuadraticCarleson.PaperTheorems.lacunary_log2_squared_log4_endpoint`
- `QuadraticCarleson.PaperTheorems.lacunary_sub_log2_modular_failure`

The module also exports the full-modulation negative consequence, the explicit
counterexamples, weak-`(1,1)` corollaries, measurability, and the finite
modulation block estimate. The [semantic audit](docs/semantic-audit.md)
documents the precise correspondence and any Lean-level formulation details.

## Build and verify

Install the Lean toolchain selected by `lean-toolchain` (via
[elan](https://github.com/leanprover/elan)). Dependencies are pinned in the
committed `lake-manifest.json`; obtain the cache and then build:

```sh
lake exe cache get
lake build
python3 -B scripts/test_proof_policy.py
python3 -B scripts/check_proof_policy.py
```

The cache command is optional but makes the initial build substantially faster.
An initial build can require roughly 10 GB of free disk space, depending on the
platform and cache state. Do not run `lake update` merely to verify this
checkout: it is a maintainer operation that changes the dependency lockfile.
The final policy command scans the Lean sources and checks the transitive axioms
of the 31 explicitly audited declarations.

To inspect the axiom report for all audited declarations directly, run:

```sh
lake env lean Verification.lean
```

Each printed declaration depends only on `propext`, `Classical.choice`, and
`Quot.sound`.

## Navigation

- [Paper-facing theorem statements](QuadraticCarleson/PaperTheorems.lean)
- [Local verification report](docs/verification-report.md)
- [Semantic comparison with the paper](docs/semantic-audit.md)

## License

The Lean source code and repository documentation are licensed under
[Apache-2.0](LICENSE).

## Acknowledgement

The organization and verification workflow of this formalization were informed
by [Joris Roos's public Lean repositories](https://github.com/roos-j). Codex
was explicitly instructed to use the general structure and workflow of those
repositories as a model.
