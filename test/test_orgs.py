import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import orgs  # noqa: E402
import validate as validate_mod  # noqa: E402
from validate import validate  # noqa: E402

CARD = """---
id: fn-x
level: function
tags: [correctness]
severity: block
status: stable
lang: core
applies_when: Always.
tool_gate: none
borrowed_from:
{urls}
---

**Rule.** R.

**Why.** W.

**FAIL**

```text
f
```

**PASS**

```text
p
```

**Counterpoint.** C.
"""


def errors_for(urls):
	with tempfile.TemporaryDirectory() as d:
		root = Path(d)
		(root / "cards" / "audit" / "function").mkdir(parents=True)
		(root / "docs" / "research").mkdir(parents=True)
		(root / "glossary").mkdir()
		(root / "cards" / "audit" / "function" / "fn-x.md").write_text(CARD.format(urls="\n".join(f"  - {u}" for u in urls)))
		(root / "docs" / "research" / "n.md").write_text("\n".join(urls))
		old, validate_mod.ORG_FLOOR_STRICT = validate_mod.ORG_FLOOR_STRICT, True  # the floor is a warning in the repo; test it as an error
		try:
			return validate(root)
		finally:
			validate_mod.ORG_FLOOR_STRICT = old


class OrgsTest(unittest.TestCase):
	def test_a_code_host_maps_to_the_repository_owner(self):
		self.assertEqual(orgs.org_of("https://raw.githubusercontent.com/OWASP/ASVS/master/x.md"), "owasp")
		self.assertEqual(orgs.org_of("https://github.com/cursor/plugins/blob/main/x.md"), "cursor")
		self.assertIsNone(orgs.org_of("https://github.com/someone-new/repo"))

	def test_a_bare_host_covers_its_subdomains_and_www(self):
		self.assertEqual(orgs.org_of("https://cheatsheetseries.owasp.org/x.html"), "owasp")
		self.assertEqual(orgs.org_of("https://www.w3.org/TR/WCAG22/"), "w3c")
		self.assertEqual(orgs.org_of("https://www.ncsc.gov.uk/x"), "ncsc")

	def test_every_org_has_a_name(self):
		self.assertEqual(set(orgs.PREFIXES.values()) - set(orgs.ORGS), set())
		self.assertEqual(set(orgs.ICONS) - set(orgs.ORGS), set())

	def test_an_unmapped_url_fails_validation(self):
		errs = errors_for(["https://example.com/a", "https://www.w3.org/a", "https://web.dev/a", "https://owasp.org/a"])
		self.assertIn("no organisation in tools/orgs.py: https://example.com/a", " ".join(errs))

	def test_split_puts_people_apart_from_orgs(self):
		urls = ["https://testdesiderata.com/", "https://web.dev/a", "https://kentcdodds.com/blog/x", "https://owasp.org/a", "https://newsletter.kentbeck.com/p"]
		o, p = orgs.split(urls)
		self.assertEqual(o, [("google", ["https://web.dev/a"]), ("owasp", ["https://owasp.org/a"])])
		self.assertEqual(p, [("kent-beck", ["https://testdesiderata.com/", "https://newsletter.kentbeck.com/p"]), ("kent-c-dodds", ["https://kentcdodds.com/blog/x"])])

	def test_persons_are_known_ids_and_orgs_are_not_persons(self):
		self.assertLessEqual(orgs.PERSONS, set(orgs.ORGS))
		self.assertEqual(len(orgs.PERSONS), 26)
		self.assertTrue({"kent-beck", "kent-c-dodds"} <= orgs.PERSONS)
		self.assertNotIn("google", orgs.PERSONS)

	def test_people_do_not_count_toward_the_floor(self):
		errs = errors_for(["https://web.dev/a", "https://testdesiderata.com/", "https://kentcdodds.com/b", "https://owasp.org/a"])
		self.assertIn("has 2 organisation(s)", " ".join(errs))

	def test_a_stable_card_needs_three_orgs(self):
		two = ["https://www.w3.org/a", "https://web.dev/a", "https://developer.chrome.com/a"]
		self.assertIn("has 2 organisation(s)", " ".join(errors_for(two)))
		self.assertEqual(errors_for(two + ["https://owasp.org/a"]), [])

	def test_a_person_does_not_count_as_an_org(self):
		urls = ["https://www.w3.org/a", "https://web.dev/a", "https://martin.kleppmann.com/a"]
		self.assertIn("has 2 organisation(s)", " ".join(errors_for(urls)))


if __name__ == "__main__":
	unittest.main()
