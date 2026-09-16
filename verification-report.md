# Verification boundary and reproducible checks

This file intentionally does not claim a successful registry verification for
an earlier or different revision. Verification evidence applies to the exact
commit that was checked.

## Local Lean checks

With the pinned `lean-toolchain` and committed `lake-manifest.json`, run:

```sh
lake exe cache get
lake build
python3 -B scripts/test_proof_policy.py
python3 -B scripts/check_proof_policy.py
```

The final command scans project sources, checks the Challenge/Solution and
Comparator configuration, and asks Lean to report the transitive axioms of the
audited declarations in `Verification.lean`. The intended allowlist is
`propext`, `Classical.choice`, and `Quot.sound`.

## Comparator and NanoDa preflight

The private CI workflow `.github/workflows/run-comparator.yml` builds the
independent Challenge/Solution pair and runs Comparator with NanoDa using a
pinned verifier toolchain. Its result is useful preflight evidence for the
commit that triggered it.

The official Palomar registry performs the final, independent verification of
the public repository and selected immutable commit. Its checks include its own
fresh checkout and protected Challenge handling, so a local or private CI run
is not described here as a registry acceptance.
