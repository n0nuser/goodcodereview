import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import orgs  # noqa: E402
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
		return validate(root)


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

	def test_a_stable_card_needs_three_orgs(self):
		two = ["https://www.w3.org/a", "https://web.dev/a", "https://developer.chrome.com/a"]
		self.assertIn("has 2 organisation(s)", " ".join(errors_for(two)))
		self.assertEqual(errors_for(two + ["https://owasp.org/a"]), [])


if __name__ == "__main__":
	unittest.main()
