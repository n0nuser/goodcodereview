"""The Markdown twins of the site pages: each page that agents may need has a clean .md file with frontmatter."""
import json
import re

from card_fields import is_stable
from config import BASE, SITE_DESC
from context import BuildInput, pack_name
from guides import GUIDES, guide_text, guides_index_text
from markdown import rule
from models import CONCERNS, LEVELS, Twin
from prose import (
    ABOUT,
    ABOUT_DESC,
    AUDIT_NOTE,
    BACKING,
    CONCERNS_DESC,
    DRAFT_NOTE,
    DRAFT_RULE,
    DRAFTS_DESC,
    EMPTY_MARK,
    EXAMPLE,
    FEEDBACK,
    GLOSSARY_DESC,
    GUIDES_DESC,
    HERO,
    INDEX_MD,
    INPUT,
    INVOKE,
    LEVEL_DESC,
    NAME,
    PACK_DESC,
    PRIVACY,
    PRIVACY_DESC,
)
from shell import page_url
from site_pages import INSTALL_PLUGIN, INSTALL_SKILL, drafts_markdown, part_spec
from skill_files import SkillOutput, audit_twin, card_section, link_stable


def front(title: str, desc: str, slug: str, date: str) -> str:
    """YAML frontmatter for a served Markdown file. JSON strings are valid YAML."""
    fields = {"title": title, "description": desc, "canonical": page_url(slug), "updated": date}
    return "---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fields.items()) + "\n---\n\n"


def _xlink(text: str, home: dict[str, str], ids: dict[str, str]) -> str:
    """Turn [[card-id]] into an absolute link: a stable card to its level file, any other known id to its page."""
    def link(m: re.Match[str]) -> str:
        name = m[1]
        if name in home:
            return f"[{name}]({BASE}/{home[name]}.md#{name})"
        return f"[{name}]({BASE}/{ids[name]})" if name in ids else name

    return re.sub(r"\[\[([^\]]+)\]\]", link, text)


def _index_page(b: BuildInput, plain: str) -> Twin:
    levels = "\n".join(f"- [{NAME[lv]}]({BASE}/{lv}.md): {LEVEL_DESC[lv]} Input: {INPUT[lv]}. {b.counts[lv].stable} stable, {b.counts[lv].draft} draft."
                       for lv in LEVELS if lv not in b.no_stable)
    levels += "".join(f"\n- {NAME[lv]}: {LEVEL_DESC[lv]} Input: {INPUT[lv]}. {EMPTY_MARK.capitalize()}." for lv in LEVELS if lv in b.no_stable)
    packs = "\n".join(f"- [{pack_name(pk)} pack]({BASE}/pack-{pk}.md)" for pk in b.packs) or "No packs yet."
    text = INDEX_MD.format(hero=HERO, verdict=plain, example=EXAMPLE, audit=AUDIT_NOTE, backing=BACKING, invoke=INVOKE, feedback=FEEDBACK,
                           npx=INSTALL_SKILL, plugin=INSTALL_PLUGIN, levels=levels, packs=packs, tally=b.tally,
                           guides="Short explainers: " + ", ".join(f"[{g.title.lower()}]({BASE}/guides/{g.slug}.md)" for g in GUIDES) + ".")
    return Twin("Good Code Review", SITE_DESC, text)


def _concerns_page(b: BuildInput, plain: str) -> Twin:
    by_concern = "\n\n".join(
        f"## {c}\n\n" + "\n".join(f"- [`{x.fm['id']}`]({BASE}/{x.fm['level']}.md#{x.fm['id']}) [{x.fm['severity']}]: {rule(x.body)}" for x in b.stable if c in x.fm["tags"])
        for c in CONCERNS if any(c in x.fm["tags"] for x in b.stable))
    return Twin("Concerns", CONCERNS_DESC, f"# Concerns\n\nStable cards grouped by concern. A card appears under each concern it lists. {plain}\n\n{by_concern}\n\n"
                f"Draft cards are not vetted and are not listed here. See {BASE}/llms-drafts.txt.\n")


def markdown_twins(b: BuildInput, skill: SkillOutput) -> dict[str, str]:
    """Every site/<slug>.md file: the level files and indexes, then the pages that have no level file."""
    twins = dict(skill.level_twins)
    for parts in skill.level_index.values():
        for part in parts:
            level = part.slug.split("-index")[0]
            twins[part.slug] = Twin(part.title, f"One line per stable {level} card.", part.text)
    twins["audit"] = audit_twin()
    twins["guides"] = Twin("Guides", GUIDES_DESC, "# Guides\n\n" + guides_index_text(html=False))
    for g in GUIDES:
        twins[f"guides/{g.slug}"] = Twin(g.title, g.desc, f"# {g.title}\n\n" + guide_text(b, g, html=False))
    twins["index"] = _index_page(b, skill.plain_verdict)
    twins["concerns"] = _concerns_page(b, skill.plain_verdict)
    for lv in b.split:
        for ctx, cs in b.parts(lv).items():
            stable = [card_section(c) for c in cs if is_stable(c)] or ["No vetted cards for this context yet."]
            text = link_stable(f"# {lv}, {ctx}\n\nThe stable {lv} cards for the `{ctx}` context. The whole level is at {BASE}/{lv}.md.\n\n" + "\n\n".join(stable) + "\n", skill.stable_home)
            twins[f"{lv}-{ctx}"] = Twin(f"{NAME[lv]}, {ctx} cards", part_spec(lv, ctx, cs).desc, text)
    for pk in b.packs:
        text = (f"# {pack_name(pk)} pack\n\nEach card says whether it is stable or draft. Stable cards are vetted and also appear in their level file. {DRAFT_NOTE} {DRAFT_RULE}\n\n"
                + "\n\n".join(card_section(c) for c in b.cards if c.fm["lang"] == pk) + "\n")
        twins[f"pack-{pk}"] = Twin(f"{pack_name(pk)} pack", PACK_DESC.format(pk=pk), _xlink(text, skill.stable_home, b.ids))
    glossary = "\n\n".join(_xlink(re.sub(r"^# ", "## ", p.read_text(), count=1).strip(), skill.stable_home, b.ids) for p in b.glossary)
    twins["glossary"] = Twin("Glossary", GLOSSARY_DESC, "# Glossary\n\n" + glossary + "\n")
    twins["about"] = Twin("About", ABOUT_DESC, "# About\n\n" + ABOUT)
    twins["privacy"] = Twin("Privacy", PRIVACY_DESC, "# Privacy\n\n" + PRIVACY)
    drafts = _xlink(re.sub(r"^# ", "## ", drafts_markdown(b), flags=re.M), skill.stable_home, b.ids)
    twins["drafts"] = Twin("Drafts by what they lack", DRAFTS_DESC, "# Drafts by what they lack\n\n" + drafts + "\n")
    return {f"{slug}.md": front(t.title, t.description, slug, b.date) + t.markdown for slug, t in twins.items()}
