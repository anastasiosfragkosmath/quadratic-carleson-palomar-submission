# Endpoint estimates for Stein's purely quadratic Carleson operator

This repository is a substantive Lean 4 + Mathlib formalization of principal
endpoint results from Anastasios Fragkos, Ben Krause, and Michael Lacey,
[*Endpoint Estimates for Stein's Purely Quadratic Carleson
Operator*](https://arxiv.org/abs/2609.04101v1).

## Main results

The project formalizes:

- failure of modular estimates below `t log₂ t` for the lacunary quadratic
  Carleson operator and the corresponding full-modulation result;
- the full-modulation `L log L` endpoint estimate; and
- the lacunary `L (log₂ L)² log₄ L` endpoint estimate.

The paper-facing source declarations are in
[`QuadraticCarleson/PaperTheorems.lean`](QuadraticCarleson/PaperTheorems.lean).
The mathematical correspondence is described in
[`semantic-audit.md`](semantic-audit.md).

## Palomar verification surface

[`Challenge.lean`](Challenge.lean) is an independent, Mathlib-only statement
surface for four headline declarations. Its four deliberate statement holes are
not proof-development gaps: [`Solution.lean`](Solution.lean) supplies completed
declarations with matching types, and [`comparator.json`](comparator.json)
configures Comparator with NanoDa enabled.

The submission metadata is in [`formalization.yaml`](formalization.yaml). The
repository is licensed under [Apache-2.0](LICENSE).

## Build and local checks

With the toolchain selected by `lean-toolchain`, obtain the pinned dependency
cache and run:

```sh
lake exe cache get
lake build
python3 -B scripts/test_proof_policy.py
python3 -B scripts/check_proof_policy.py
```

`lake build` includes the substantive development and the separate
Challenge/Solution libraries. The policy script rejects unfinished proof
development, prohibited proof-bypass mechanisms, and unsupported Comparator
configuration; it also runs the explicit axiom audit in
[`Verification.lean`](Verification.lean).

The private CI includes a pinned Comparator/NanoDa preflight. It checks the
same statement-comparison toolchain family as Palomar, while the official
registry remains the final independent verifier of a public pinned commit.
See [`verification-report.md`](verification-report.md) for the verification
boundary and reproducible checks.
