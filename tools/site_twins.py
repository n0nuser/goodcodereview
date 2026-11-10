"""The Markdown twins of the site pages: each page that agents may need has a clean .md file with frontmatter."""
import json
import re

from card_fields import is_core, is_stable, level_of
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


LLMS_NOTE = f"> For the complete documentation index, see [llms.txt]({BASE}/llms.txt).\n\n"


def _absolute(text: str) -> str:
    """Make site-relative links (`service.md#id`, `/x.md`) absolute, so a twin read off-site still resolves. Code fences stay as written."""
    link = re.compile(r"\]\((?!https?:|mailto:|#)/?([^)\s]+)\)")
    # re.split with a capturing group keeps the fences at the odd indexes.
    chunks = re.split(r"(?ms)(^```.*?^```)", text)
    return "".join(c if i % 2 else link.sub(lambda m: f"]({BASE}/{m[1]})", c) for i, c in enumerate(chunks))


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


FULL_SLUGS = (*LEVELS, "audit", "glossary", "guides", "about")


def llms_full(texts: dict[str, str], b: BuildInput) -> str:
    """llms-full.txt: the full-text pages in one file. Each is its served .md without the frontmatter; the context parts and packs repeat or extend them, so they stay out."""
    guides = [f"guides/{g.slug}" for g in GUIDES]
    parts = [texts[f"{s}.md"].split("\n---\n\n", 1)[1].replace(LLMS_NOTE, "", 1) for s in (*FULL_SLUGS, *guides) if f"{s}.md" in texts]
    return f"# Good Code Review: full text\n\n> {SITE_DESC}\n\nThe index is {BASE}/llms.txt. Each section below is one page, as served at its .md URL.\n\n" + "\n\n".join(parts)


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
        by_ctx = b.parts(lv)
        total = sum(sum(is_stable(c) for c in cs) for cs in by_ctx.values())
        done = 0
        packs = sum(1 for c in b.stable if level_of(c) == lv and not is_core(c))
        pack_note = f" The {packs} stable language-pack cards at this level are on the pack pages ({', '.join(f'[{pk}]({BASE}/pack-{pk}.md)' for pk in b.packs)})." if packs else ""
        for n, (ctx, cs) in enumerate(by_ctx.items(), 1):
            stable = [card_section(c) for c in cs if is_stable(c)] or ["No vetted cards for this context yet."]
            first, done = done + 1, done + sum(is_stable(c) for c in cs)
            others = ", ".join(f"[{o}]({BASE}/{lv}-{o}.md)" for o in by_ctx if o != ctx)
            head = (f"# {lv}, {ctx}\n\nPart {n} of {len(by_ctx)} of the {lv} level: stable cards {first} to {done} of {total}, the `{ctx}` context. "
                    f"A review of this level needs every part: read the others ({others}) too, and name the parts you read in your report.{pack_note} "
                    f"The whole level is one file at {BASE}/{lv}.md, about {skill.level_chars[lv] // 1000}K characters; a fetch tool may truncate it, so use it only if you can download it.\n\n")
            text = link_stable(head + "\n\n".join(stable) + "\n", skill.stable_home)
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
    return {f"{slug}.md": front(t.title, t.description, slug, b.date) + LLMS_NOTE + _absolute(t.markdown) for slug, t in twins.items()}
