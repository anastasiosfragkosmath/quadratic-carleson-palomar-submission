#!/usr/bin/env python3
"""Enforce local source/config policy and validate the explicit Lean axiom audit.

This guard is not Comparator, an independent kernel, or an adversarial sandbox.
Dependency sources/generated files in .lake are excluded from the source scan;
the Lean audit checks transitive axioms of the explicitly audited declarations.
"""

import argparse
import fnmatch
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
CHALLENGE = ROOT / "Challenge.lean"
SOLUTION = ROOT / "Solution.lean"
COMPARATOR_CONFIG = ROOT / "comparator.json"
CHALLENGE_THEOREMS = (
    "QuadraticCarleson.PaperTheorems.lacunary_sub_log2_modular_failure",
    "QuadraticCarleson.PaperTheorems.full_sub_log2_modular_failure",
    "QuadraticCarleson.PaperTheorems.full_LlogL_endpoint",
    "QuadraticCarleson.PaperTheorems.lacunary_log2_squared_log4_endpoint",
)
FORBIDDEN_SOURCE = (
    r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|extern|native_decide|"
    r"trustCompiler|run_tac|run_cmd|run_elab|elab|macro|opaque)\b|"
    r"debug\.skipKernelTC|kernel\.trust|Lean\.ofReduce|^\s*#eval\b"
)
HEADLINES = frozenset(
    "QuadraticCarleson.PaperTheorems." + name
    for name in (
        "lacunary_sub_log2_modular_failure",
        "full_sub_log2_modular_failure",
        "lacunary_counterexample_at_unit_height",
        "full_counterexample_at_unit_height",
        "full_LlogL_endpoint",
        "lacunary_log2_squared_log4_endpoint",
        "lacunary_not_weakOneOne",
        "full_not_weakOneOne",
        "principalValueMaxima_aemeasurable",
        "finite_modulation_blocks_weakOneOne",
    )
)
REQUIRED_AUDIT = HEADLINES | frozenset(
    "QuadraticCarleson." + name
    for name in (
        "PositiveEndpointsAERepresentative.full_principalValue_endpoint_aemeasurable",
        "PositiveEndpointsAERepresentative.lacunary_principalValue_endpoint_aemeasurable",
        "fourier_principalValueOneDiv",
        "principalValueOneDiv_eq_FourierCandidate",
        "offSupportPaperLemma",
        "bohrSet_volume_real_comparable",
        "bohrSet_inter_volume_le",
        "dyadicBohrLogUnion_volume_real_ge",
        "dyadicBohrLogUnion_volume_real_ge_uniform",
        "weak11sparseStatement_proof",
        "paperFixedHeightQuadraticMaximal_eLpNorm_decay",
        "KaltonEndpoint.hasWeakL1Bound_tsum_paperLog",
        "LacunaryFrozenBlockDirectResolved.hasUniformL0LogSquaredFrozenBlockWeakBounds",
        "YoungFunction.bijOn_nonneg",
        "YoungFunction.apply_nonnegOrderIso_symm",
        "YoungFunction.nonnegOrderIso_symm_apply",
        "hasSum_dyadicPsi",
        "tsum_dyadicPsi",
        "torusNorm_eq_abs_of_mem_Ico",
        "torusNorm_isLeast_integerDistances",
        "torusNorm_eq_iInf_abs_sub_int",
    )
)
REPORT = re.compile(
    r"^'([^'\n]+)' (?:depends on axioms:\s*\[([^\]]*)\]|"
    r"does not depend on any axioms)\s*$",
    re.MULTILINE,
)
CHALLENGE_PLACEHOLDER = re.compile(r"^\s*sorry\s*$", re.MULTILINE)


def inventory(pattern):
    if shutil.which("rg") is None:
        files = []
        for directory, directories, filenames in os.walk(ROOT):
            directories[:] = [name for name in directories if name not in {".lake", ".git"}]
            files.extend(
                Path(directory) / name for name in filenames if fnmatch.fnmatch(name, pattern)
            )
        return sorted(files)

    result = subprocess.run(
        ["rg", "--no-config", "--files", "--hidden", "--no-ignore", "-0", "-g", pattern,
         "-g", "!**/.lake/**", "-g", "!**/.git/**", "."],
        cwd=ROOT, capture_output=True,
    )
    if result.returncode not in (0, 1):
        raise ValueError("Source inventory failed: " + result.stderr.decode())
    return [ROOT / part.decode() for part in result.stdout.split(b"\0") if part]


def fallback_forbidden_source_matches(sources):
    forbidden = re.compile(FORBIDDEN_SOURCE, re.MULTILINE)
    matches = []
    for source in sources:
        lines = source.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            if forbidden.search(line):
                matches.append(f"./{source.relative_to(ROOT)}:{line_number}:{line}")
    return matches


def validate_challenge_source(challenge):
    placeholders = CHALLENGE_PLACEHOLDER.findall(challenge)
    if len(placeholders) != len(CHALLENGE_THEOREMS):
        raise ValueError("Challenge.lean must contain exactly one intentional placeholder per target.")
    challenge_without_placeholders = CHALLENGE_PLACEHOLDER.sub("", challenge)
    forbidden = re.compile(FORBIDDEN_SOURCE, re.MULTILINE)
    if forbidden.search(challenge_without_placeholders):
        raise ValueError("Challenge.lean contains a forbidden declaration outside its placeholders.")
    for theorem in CHALLENGE_THEOREMS:
        name = theorem.rsplit(".", maxsplit=1)[1]
        placeholder_body = re.compile(
            rf"^theorem {re.escape(name)}\b(?:(?!^theorem\b).)*?"
            r":=\s*by\s*\n[ \t]*sorry[ \t]*$",
            re.MULTILINE | re.DOTALL,
        )
        if not placeholder_body.search(challenge):
            raise ValueError(
                f"Challenge.lean must use its intentional placeholder as the body of {theorem}."
            )


def validate_challenge():
    if not CHALLENGE.is_file() or not SOLUTION.is_file() or not COMPARATOR_CONFIG.is_file():
        raise ValueError("Comparator challenge, solution, and configuration must all be present.")

    challenge = CHALLENGE.read_text(encoding="utf-8")
    validate_challenge_source(challenge)

    solution = SOLUTION.read_text(encoding="utf-8")
    if "import QuadraticCarleson.PaperTheorems" not in solution:
        raise ValueError("Solution.lean must import the paper-facing formalization module.")

    config = json.loads(COMPARATOR_CONFIG.read_text(encoding="utf-8"),
                        object_pairs_hook=unique_object)
    validate_config(config)
    if (config.get("challenge_module") != "Challenge"
            or config.get("solution_module") != "Solution"
            or config.get("theorem_names") != list(CHALLENGE_THEOREMS)):
        raise ValueError("Comparator configuration must name the four approved challenge targets.")


def reject_unscanned_symlinks():
    def fail_walk(error):
        raise error

    for directory, directories, files in os.walk(ROOT, onerror=fail_walk):
        directories[:] = [name for name in directories if name not in {".lake", ".git"}]
        for name in directories + [name for name in files if name.endswith((".lean", ".json"))]:
            path = Path(directory) / name
            if path.is_symlink():
                raise ValueError(f"Symlink could evade the source/config scan: {path}")


def check_sources():
    reject_unscanned_symlinks()
    sources = inventory("*.lean")
    if not sources:
        raise ValueError("No project Lean sources found; refusing an empty scan.")
    validate_challenge()
    implementation_sources = [source for source in sources if source != CHALLENGE]
    if shutil.which("rg") is None:
        matches = fallback_forbidden_source_matches(implementation_sources)
        if matches:
            raise ValueError("Forbidden project source tokens:\n" + "\n".join(matches))
    else:
        result = subprocess.run(
            ["rg", "--no-config", "--text", "-n", "--hidden", "--no-ignore", "-g", "*.lean",
             "-g", "!Challenge.lean", "-g", "!**/.lake/**", "-g", "!**/.git/**",
             FORBIDDEN_SOURCE, "."],
            cwd=ROOT, capture_output=True, text=True,
        )
        if result.returncode == 0:
            raise ValueError("Forbidden project source tokens:\n" + result.stdout)
        if result.returncode != 1:
            raise ValueError("Source scan failed:\n" + result.stderr)
    print("PASS: source policy "
          f"({len(implementation_sources)} non-challenge Lean files; "
          f"{len(CHALLENGE_THEOREMS)} approved challenge placeholders).", flush=True)


def validate_config(config):
    if not isinstance(config, dict):
        raise ValueError("Comparator configuration must be a JSON object.")
    permitted = config.get("permitted_axioms")
    if (not isinstance(permitted, list)
            or not all(isinstance(name, str) for name in permitted)
            or not set(permitted) <= ALLOWED_AXIOMS):
        raise ValueError("Comparator permitted_axioms must be a subset of "
                         "propext, Classical.choice, Quot.sound.")
    if config.get("enable_nanoda") is not True:
        raise ValueError("Project Comparator configs must explicitly enable NanoDa.")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key is not permitted: {key}")
        result[key] = value
    return result


def check_configs():
    count = 0
    for path in inventory("*.json"):
        # Inspect keys rather than depending on one conventional filename.
        config = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        if ("comparator" in path.name.lower()
                or isinstance(config, dict) and any(
                    key in config for key in
                    ("challenge_module", "solution_module", "permitted_axioms")
                )):
            validate_config(config)
            count += 1
    validate_challenge()
    print(f"PASS: config policy ({count} Comparator configurations present).", flush=True)
    if count == 0:
        print("NOTE: no Comparator configuration; Comparator has NOT run.", flush=True)


def validate_reports(output, expected):
    reports = list(REPORT.finditer(output))
    names = [report.group(1) for report in reports]
    if len(names) != len(expected) or set(names) != set(expected):
        raise ValueError("Missing, duplicate, or unexpected Lean axiom reports.")
    for report in reports:
        dependencies = {name.strip() for name in (report.group(2) or "").split(",")
                        if name.strip()}
        forbidden = dependencies - ALLOWED_AXIOMS
        if forbidden:
            raise ValueError(f"Forbidden axioms for {report.group(1)}: {sorted(forbidden)}")


def check_axioms():
    audit = (ROOT / "Verification.lean").read_text(encoding="utf-8")
    expected = re.findall(r"^#print axioms (\S+)\s*$", audit, re.MULTILINE)
    if len(set(expected)) != len(expected) or not REQUIRED_AUDIT <= set(expected):
        raise ValueError("Verification.lean must retain all 31 required declarations exactly once.")
    print("Running Lean's explicit transitive-axiom audit...", flush=True)
    result = subprocess.run(
        ["lake", "env", "lean", "Verification.lean"], cwd=ROOT,
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise ValueError("Lean axiom audit failed:\n" + result.stdout + result.stderr)
    validate_reports(result.stdout, expected)
    print(f"PASS: all {len(expected)} explicit reports use only permitted axioms.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-only", action="store_true",
                        help="Scan source/configs only; do not claim an axiom-audit pass.")
    args = parser.parse_args()
    check_sources()
    check_configs()
    if args.source_only:
        print("NOTE: axiom audit was not run (--source-only).")
    else:
        check_axioms()


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
