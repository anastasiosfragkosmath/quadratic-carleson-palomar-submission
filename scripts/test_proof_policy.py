"""In-memory rejection tests; no placeholder-containing Lean file is created."""

import unittest
import json

from check_proof_policy import (
    CHALLENGE_THEOREMS,
    HEADLINES,
    REQUIRED_AUDIT,
    unique_object,
    validate_challenge_source,
    validate_config,
    validate_reports,
)


class PolicyTests(unittest.TestCase):
    @staticmethod
    def challenge_source():
        return "\n\n".join(
            f"theorem {name.rsplit('.', maxsplit=1)[1]} : True := by\n  sorry"
            for name in CHALLENGE_THEOREMS
        )

    def test_permitted_config(self):
        validate_config({"permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
                         "enable_nanoda": True})

    def test_forbidden_configs(self):
        for value in (["sorryAx"], ["Lean.ofReduceBool"], ["NewAxiom"],
                      "propext", None, [None]):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_config({"permitted_axioms": value, "enable_nanoda": True})

    def test_disabled_second_kernel(self):
        with self.assertRaises(ValueError):
            validate_config({"permitted_axioms": [], "enable_nanoda": False})

    def test_missing_second_kernel_setting(self):
        with self.assertRaises(ValueError):
            validate_config({"permitted_axioms": []})

    def test_duplicate_json_key(self):
        with self.assertRaises(ValueError):
            json.loads('{"permitted_axioms": ["sorryAx"], "permitted_axioms": []}',
                       object_pairs_hook=unique_object)

    def test_standard_reports(self):
        validate_reports("'a' depends on axioms: [propext,\n Classical.choice, Quot.sound]\n"
                         "'b' does not depend on any axioms\n", ["a", "b"])

    def test_missing_and_duplicate_reports(self):
        for output in ("", "'a' depends on axioms: []\n" * 2,
                       "'unexpected' depends on axioms: []\n", "unrecognized output"):
            with self.subTest(output=output), self.assertRaises(ValueError):
                validate_reports(output, ["a"])

    def test_forbidden_dependencies(self):
        for name in ("sorryAx", "CustomAxiom", "Lean.trustCompiler"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                validate_reports(f"'a' depends on axioms: [propext, {name}]\n", ["a"])

    def test_headline_inventory(self):
        self.assertEqual(len(HEADLINES), 10)
        self.assertEqual(len(REQUIRED_AUDIT), 31)

    def test_challenge_placeholders_belong_to_the_target_bodies(self):
        source = self.challenge_source()
        validate_challenge_source(source)

        first_name = CHALLENGE_THEOREMS[0].rsplit(".", maxsplit=1)[1]
        malformed = source.replace(
            f"theorem {first_name} : True := by\n  sorry",
            f"theorem {first_name} : True := by\n  trivial\n\nsorry",
        )
        with self.assertRaises(ValueError):
            validate_challenge_source(malformed)


if __name__ == "__main__":
    unittest.main()
