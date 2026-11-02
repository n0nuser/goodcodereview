import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from validate import CONTEXTS, load_cards  # noqa: E402

SKILL = ROOT / "skills" / "good-code-review" / "SKILL.md"
if not (ROOT / "site" / "llms.txt").is_file():  # site/ is generated and untracked; a fresh clone needs one build
    subprocess.run([sys.executable, str(ROOT / "tools" / "build.py")], check=True)


def frontmatter():
    text = SKILL.read_text()
    assert text.startswith("---\n"), "SKILL.md must open with frontmatter"
    return text.split("---\n")[1]


class Frontmatter(unittest.TestCase):
    """The Agent Skills spec (agentskills.io/specification) requires YAML frontmatter that parses."""

    def test_parses_as_yaml_when_pyyaml_is_installed(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML is not installed; test_plain_scalars_hold_no_yaml_syntax covers it")
        data = yaml.safe_load(frontmatter())
        self.assertEqual(data["name"], "good-code-review")
        self.assertTrue(all(isinstance(v, str) for v in data["metadata"].values()))

    def test_plain_scalars_hold_no_yaml_syntax(self):
        # A plain scalar that contains ": " or " #" is not valid YAML. Quote it (JSON strings are valid YAML).
        for line in frontmatter().splitlines():
            m = re.match(r"^\s*[a-z-]+:\s+(\S.*)$", line)
            if m and not m[1].startswith(('"', "'")):
                self.assertNotRegex(m[1], r": | #", line[:60])

    def test_fields_meet_the_spec_limits(self):
        fm = frontmatter()
        self.assertRegex(fm, r"(?m)^name: good-code-review$")
        desc = json.loads(re.search(r'(?m)^description: (".*")$', fm)[1])
        self.assertTrue(0 < len(desc) <= 1024, len(desc))
        comp = json.loads(re.search(r'(?m)^compatibility: (".*")$', fm)[1])
        self.assertTrue(0 < len(comp) <= 500, len(comp))
        self.assertEqual(SKILL.parent.name, "good-code-review")

    def test_body_stays_small(self):
        self.assertLess(len(SKILL.read_text().splitlines()), 500)


class Audit(unittest.TestCase):
    """The audit section, the draft cap, and the context tags that real audits asked for."""

    def test_skill_has_the_audit_section_and_report_shape(self):
        skill = SKILL.read_text()
        self.assertIn("## Audit a repo, service, or release", skill)
        self.assertIn("references/audit.md", skill)
        text = (SKILL.parent / "references" / "audit.md").read_text()
        for needle in ("absent in <paths>", "Proposed changes", "Not examined", "accepted by <owner> until <date>",
                       "not a SOC 2, ISO 27001, or other compliance attestation"):
            self.assertIn(needle, text)

    def test_drafts_ship_inside_the_skill(self):
        refs = SKILL.parent / "references"
        self.assertTrue((refs / "drafts.md").is_file())
        self.assertIn("references/drafts.md", SKILL.read_text())

    def test_no_draft_is_block_and_context_uses_the_closed_list(self):
        for p, fm, _ in load_cards(SKILL.parents[2]):
            self.assertFalse(fm["status"] == "draft" and fm["severity"] == "block", p.name)
            self.assertTrue(set(fm.get("context", [])) <= set(CONTEXTS), p.name)


class Budgets(unittest.TestCase):
    """The first read stays small as cards and audit advice grow: each layer has a budget, and build.py fails past it."""

    ROOT = SKILL.parents[2]

    def test_skill_body_llms_and_indexes_stay_in_budget(self):
        body = SKILL.read_text().split("\n---\n", 1)[1]
        self.assertLessEqual(len(body), 16_000)  # about 4,000 tokens; the Agent Skills spec recommends under 5,000
        self.assertLessEqual(len((self.ROOT / "site" / "llms.txt").read_text()), 12_000)
        for p in (self.ROOT / "site").glob("*-index*.md"):
            self.assertLessEqual(len(p.read_text()), 12_000, p.name)
        for p in (SKILL.parent / "references").glob("*.md"):
            self.assertLessEqual(len(p.read_text()), 70_000, p.name)

    def test_llms_txt_lists_files_and_no_card_lines(self):
        text = (self.ROOT / "site" / "llms.txt").read_text()
        self.assertTrue(text.startswith("# "))
        self.assertRegex(text, r"(?m)^> ")
        self.assertNotRegex(text, r"(?m)^- \[[a-z0-9-]+\]\(\S+#")  # a card line belongs in a level index, not in llms.txt
        self.assertTrue(text.rstrip().split("\n## ")[-1].startswith("Optional"))


if __name__ == "__main__":
    unittest.main()
