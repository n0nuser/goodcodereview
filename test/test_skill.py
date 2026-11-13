import json
import re

import pytest

from config import ROOT, SKILL
from models import CONTEXTS
from prose import LLMS_HEAD_MAX, LLMS_IMPERATIVE
from validate import load_cards

SKILL_MD = SKILL / "SKILL.md"
SKILL_BODY_MAX = 16_000  # about 4,000 tokens; the Agent Skills spec recommends under 5,000
LLMS_MAX = 12_000
INDEX_MAX = 12_000
DESCRIPTION_MAX = 1024
COMPATIBILITY_MAX = 500
SKILL_LINES_MAX = 500


@pytest.fixture(scope="module")
def frontmatter() -> str:
    text = SKILL_MD.read_text()
    assert text.startswith("---\n"), "SKILL.md must open with frontmatter"
    return text.split("---\n")[1]


def test_parses_as_yaml_when_pyyaml_is_installed(frontmatter: str) -> None:
    yaml = pytest.importorskip("yaml", reason="PyYAML is optional; test_plain_scalars_hold_no_yaml_syntax covers the same ground")
    data = yaml.safe_load(frontmatter)
    assert data["name"] == "good-code-review"
    assert all(isinstance(v, str) for v in data["metadata"].values())


def test_plain_scalars_hold_no_yaml_syntax(frontmatter: str) -> None:
    # A plain scalar that contains ": " or " #" is not valid YAML. Quote it (JSON strings are valid YAML).
    for line in frontmatter.splitlines():
        m = re.match(r"^\s*[a-z-]+:\s+(\S.*)$", line)
        if m and not m[1].startswith(('"', "'")):
            assert not re.search(r": | #", m[1]), line[:60]


def test_fields_meet_the_spec_limits(frontmatter: str) -> None:
    assert re.search(r"(?m)^name: good-code-review$", frontmatter)
    description = re.search(r'(?m)^description: (".*")$', frontmatter)
    compat = re.search(r'(?m)^compatibility: (".*")$', frontmatter)
    assert description
    assert compat
    assert 0 < len(json.loads(description[1])) <= DESCRIPTION_MAX
    assert 0 < len(json.loads(compat[1])) <= COMPATIBILITY_MAX
    assert SKILL.name == "good-code-review"


def test_body_stays_small() -> None:
    assert len(SKILL_MD.read_text().splitlines()) < SKILL_LINES_MAX


def test_skill_has_the_audit_section_and_report_shape() -> None:
    skill = SKILL_MD.read_text()
    assert "## Audit a repo, service, or release" in skill
    assert "references/audit.md" in skill
    text = (SKILL / "references" / "audit.md").read_text()
    for needle in ("absent in <paths>", "Proposed changes", "Not examined", "accepted by <owner> until <date>",
                   "not a SOC 2, ISO 27001, or other compliance attestation"):
        assert needle in text


def test_drafts_ship_inside_the_skill() -> None:
    assert (SKILL / "references" / "drafts.md").is_file()
    assert "references/drafts.md" in SKILL_MD.read_text()


def test_no_draft_is_block_and_context_uses_the_closed_list() -> None:
    for c in load_cards(ROOT):
        assert not (c.fm["status"] == "draft" and c.fm["severity"] == "block"), c.path.name
        assert set(c.fm.get("context", [])) <= set(CONTEXTS), c.path.name


def test_skill_body_and_llms_stay_in_budget(site_text: dict[str, str]) -> None:
    assert len(SKILL_MD.read_text().split("\n---\n", 1)[1]) <= SKILL_BODY_MAX
    assert len(site_text["llms.txt"]) <= LLMS_MAX


def test_indexes_stay_in_budget(site_text: dict[str, str]) -> None:
    indexes = {name: text for name, text in site_text.items() if re.fullmatch(r".*-index.*\.md", name)}
    assert indexes
    for name, text in indexes.items():
        assert len(text) <= INDEX_MAX, name


def test_llms_txt_lists_files_and_no_card_lines(site_text: dict[str, str]) -> None:
    text = site_text["llms.txt"]
    assert text.startswith("# ")
    assert re.search(r"(?m)^> ", text)
    assert not re.search(r"(?m)^- \[[a-z0-9-]+\]\(\S+#", text)  # a card line belongs in a level index, not in llms.txt
    assert text.rstrip().split("\n## ")[-1].startswith("Optional")




def test_skill_names_every_depth_and_llms_points_to_them(site_text: dict[str, str]) -> None:
    skill = SKILL_MD.read_text()
    assert "## Depth" in skill
    for depth in ("quick", "default", "deep", "audit"):
        assert f"| `{depth}` |" in skill
        assert f"`{depth}`" in site_text["llms.txt"]


def test_references_show_the_tool_gate_of_a_gated_card() -> None:
    text = (SKILL / "references" / "function.md").read_text()
    assert "\ntool gate: " in text


def test_llms_head_is_short_descriptive_and_not_copied_from_skill(site_text: dict[str, str]) -> None:
    head = site_text["llms.txt"].split("\n## ", 1)[0]
    assert len(head) <= LLMS_HEAD_MAX
    assert not re.search(LLMS_IMPERATIVE, head)
    skill_paragraphs = {p for p in SKILL_MD.read_text().split("\n\n") if len(p) > 80}
    assert not [p for p in head.split("\n\n") if p in skill_paragraphs]


def test_index_places_point_at_the_card_sections() -> None:
    refs = SKILL / "references"
    checked = 0
    for index in [*refs.glob("index-*.md"), *refs.glob("concern-*.md")]:
        for m in re.finditer(r"^- `([^`]+)` .*?(?:(\w+)\.md:)?L(\d+)\+(\d+): ", index.read_text(), re.M):
            card, name, first, count = m[1], m[2], int(m[3]), int(m[4])
            target = refs / (f"{name}.md" if name else "drafts.md" if index.name == "index-drafts.md" else index.name.replace("index-", ""))
            lines = target.read_text().split("\n")
            assert lines[first - 1] == f"## {card}", (index.name, card)
            assert count > 1 and lines[first - 1 + count - 1].strip(), (index.name, card)
            checked += 1
    assert checked > 237  # every stable card is in its level index and in at least one concern index
