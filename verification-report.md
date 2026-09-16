# Verification report

## Recorded source verification

The most recent recorded end-to-end GitHub Actions verification was run at
revision `1a79ef9` (2026-09-13). The revision is recorded because verification
evidence applies to the exact source and configuration checked. Its successor
`22efe5a` changed only `README.md`; it did not alter the Lean source, toolchain,
Comparator files, or proof-policy script.

| Check | Recorded result |
| --- | --- |
| GitHub Actions: Lean Action CI #8 | Passed at `1a79ef9`. It built every `QuadraticCarleson.*` module with the pinned toolchain, then ran the source-policy checks and explicit axiom audit. |
| GitHub Actions: Run Comparator #2 | Passed at `1a79ef9`. The manual Comparator workflow checked the four declarations listed in `comparator.json`; NanoDa checking was enabled. |
| Source policy | Every project Lean file other than `Challenge.lean` is checked for forbidden placeholders and proof-bypass mechanisms. `Challenge.lean` is separately checked to contain exactly four approved statement placeholders, each as the body of its named Comparator target. |
| Explicit axiom audit | The 31 declarations listed in `Verification.lean` depend only on `propext`, `Classical.choice`, and `Quot.sound`. |

The regular CI builds every `QuadraticCarleson.*` module. `Challenge.lean` and
`Solution.lean` are built separately by the manual Comparator workflow.

## Reproduce the Lean checks locally

With the toolchain selected by `lean-toolchain`, use the committed
`lake-manifest.json` and run:

```sh
lake exe cache get
lake build
python3 -B scripts/test_proof_policy.py
python3 -B scripts/check_proof_policy.py
```

The cache command is optional but substantially reduces the initial build time.
The first build can require roughly 10 GB of free disk space, depending on the
platform and cache state. Do not run `lake update` merely to reproduce this
checkout: it is a maintainer operation that changes the dependency lockfile.
The final command performs the project source and configuration checks, then
runs the explicit transitive-axiom audit.

To display the axiom reports for all audited declarations directly, run:

```sh
lake env lean Verification.lean
```

## Comparator check

`Challenge.lean` fixes these four statement declarations:

- `lacunary_sub_log2_modular_failure`
- `full_sub_log2_modular_failure`
- `full_LlogL_endpoint`
- `lacunary_log2_squared_log4_endpoint`

`Solution.lean` exposes the corresponding completed proofs from
`QuadraticCarleson.PaperTheorems`. The manual workflow builds these separate
modules and then runs Comparator against that exact pair. It is intentionally
manual because it is an additional long-running check; the regular Lean CI is
the check that runs on every push. Comparator checks these
four written Lean statement/proof pairs; the statement-level comparison with
the article is documented separately in `semantic-audit.md`.

## Scope

This report records build, source-policy, axiom-audit, and Comparator evidence
for `1a79ef9`. The paper-facing declarations are collected in
`QuadraticCarleson/PaperTheorems.lean`; the current statement correspondence is
documented in `semantic-audit.md`. This report does not replace inspection of
the theorem types or an applicable workflow run after a later change to Lean
source, the toolchain, Comparator files, the proof-policy script, or workflows.
