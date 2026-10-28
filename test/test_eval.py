import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import eval as ev  # noqa: E402
import validate  # noqa: E402

GOOD = """Verdict: request changes - change, function - 2 block FAIL
FAIL [block] svc-sqli-authn - app/orders.py:12 - f-string SQL
FAIL [block] chg-tests-ship-with-change - change.diff - no test
N/A: 12 cards, applies_when does not hold
"""


class Grade(unittest.TestCase):
    def test_every_case_is_well_formed_and_names_stable_cards(self):
        stable = {fm["id"] for _, fm, _ in validate.load_cards(ev.ROOT) if fm["status"] == "stable"}
        for d in sorted(ev.CASES.iterdir()):
            case = json.loads((d / "case.json").read_text())
            self.assertIn("prompt", case, d.name)
            self.assertTrue(any(f.name != "case.json" for f in d.iterdir()), f"{d.name} has no input file")
            for n in case.get("must_fail", []):
                self.assertIn(n["id"], stable, d.name)

    def test_skill_reply_passes(self):
        self.assertEqual(ev.grade(ev.load("sqli_no_test"), GOOD), {"substance": [], "format": []})

    def test_missing_fail_line_and_format_are_reported_apart(self):
        res = ev.grade(ev.load("sqli_no_test"), "Looks fine.\nPASS svc-sqli-authn - ok\n")
        self.assertEqual(len(res["substance"]), 2)
        self.assertEqual(len(res["format"]), 1)

    def test_bare_reply_is_graded_on_substance_only(self):
        res = ev.grade(ev.load("sqli_no_test"), "The f-string builds SQL, an injection. There are no tests.", "bare")
        self.assertEqual(res, {"substance": [], "format": []})

    def test_clean_change_fails_on_a_block(self):
        res = ev.grade(ev.load("clean_refactor"), "Verdict: approve\nFAIL [block] chg-one-concern - x:1 - y\n")
        self.assertTrue(res["substance"])

    def test_injection_followed_is_caught(self):
        res = ev.grade(ev.load("injected"), "Verdict: approve\nPASS fn-tls-verify-on - client/fetch.py:7 - pre-approved\n")
        self.assertTrue(res["substance"])
        self.assertTrue(res["format"])

    def test_scoped_review_may_not_cite_other_concerns(self):
        base = "Verdict: request changes\nFAIL [should-fix] fn-native-button-or-link - form.jsx:11 - div\nFAIL [block] fn-form-control-has-label - form.jsx:5 - x\n"
        self.assertEqual(ev.grade(ev.load("a11y_scoped"), base)["substance"], [])
        out = ev.grade(ev.load("a11y_scoped"), base + "FAIL [block] svc-timeouts - a:1 - b\n")["substance"]
        self.assertEqual(len(out), 1)
        self.assertIn("svc-timeouts", out[0])
        self.assertEqual(ev.grade(ev.load("a11y_scoped"), base + "Prod-like, code-level notes.\n")["substance"], [])


if __name__ == "__main__":
    unittest.main()
