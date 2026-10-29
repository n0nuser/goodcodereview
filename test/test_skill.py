import json
import re
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "good-code-review" / "SKILL.md"


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


if __name__ == "__main__":
    unittest.main()
