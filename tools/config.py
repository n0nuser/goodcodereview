"""Paths, site constants, and the size budgets that tools/build.py enforces."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SKILL = ROOT / "skills" / "good-code-review"
TOOLS = ROOT / "tools"

BASE = "https://goodcodereview.com"
REPO = "https://github.com/n0nuser/goodcodereview"
SITE_NAME = "Good Code Review"
SITE_DESC = "A code review checklist for people and agents. Each vetted rule cites at least three independent organisations, and every check ends in PASS, FAIL, or N/A with file:line evidence."
LICENCE_URL = "https://creativecommons.org/licenses/by/4.0/"
SKILL_NAME = "good-code-review"
SIMPLE_ICONS_VERSION = "15.22.0"  # the release that tools/org_icons.json was taken from (CC0, https://simpleicons.org)
SBOM_FILE = ROOT / "sbom.cdx.json"

# Size budgets. The build fails past them, so the first read stays small as cards and audit advice grow.
# llms.txt and SKILL.md hold routing and links; per-card text lives in the level indexes and references.
SKILL_BUDGET = 400  # max lines in SKILL.md
LLMS_BUDGET = 12_000  # characters in llms.txt (llmstxt.org asks for a concise summary)
SKILL_BODY_BUDGET = 16_000  # characters in SKILL.md after the frontmatter, about 4,000 tokens (the Agent Skills spec recommends under 5,000)
INDEX_BUDGET = 12_000  # characters in one level index; past it the index splits by `context`

SECURITY_TXT_DAYS = 180  # RFC 9116 Expires, counted from the build date so each rebuild renews it
HSTS_MAX_AGE = 31_536_000  # one year, in seconds
OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630
# Monogram font size by letter count (index 0 is unused): a longer monogram needs smaller type inside the 24-unit badge.
MONOGRAM_FONT_SIZES = (0, 12, 10, 8, 6.5)
