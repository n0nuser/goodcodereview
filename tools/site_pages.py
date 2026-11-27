"""The HTML pages of the site: level, pack, and concerns listings, the glossary, the text pages, the home page, and the 404."""
import html
import re
from collections.abc import Callable

from agent_ready_check import Page
from card_fields import concerns, is_stable, lacks, topics
from config import MIN_PART, PAGE_MAX, REPO, SITE_DESC
from context import BuildInput, pack_name
from errors import BuildError
from guides import GUIDES, guide_text, guides_index_text
from listing import copy_pre, listing
from markdown import inline, md
from models import LEVELS, Card, LacksReason, Level, PageSpec
from prose import (
    ABOUT,
    ABOUT_DESC,
    AGENTIC_NOTE,
    AUDIT_DESC,
    AUDIT_INTRO,
    AUDIT_NOTE,
    AUDIT_STEPS,
    BACKING,
    CONCERNS_DESC,
    DRAFTS_DESC,
    EMPTY_MARK,
    EXAMPLE,
    FAQ,
    FAQ_DESC,
    FEEDBACK,
    GLOSSARY_DESC,
    GUIDES_DESC,
    HERO,
    INCIDENT_EXAMPLE,
    INCIDENT_RULE,
    INPUT,
    INVOKE,
    LACKS_LABEL,
    LEVEL_DESC,
    NAME,
    PACK_DESC,
    PRIVACY,
    PRIVACY_DESC,
    VERDICT,
)
from seo import MAX_DESC, MIN_DESC, PARTS, home_ld
from shell import page

INSTALL_SKILL = "npx skills add n0nuser/goodcodereview"
INSTALL_PLUGIN = "/plugin marketplace add n0nuser/goodcodereview\n/plugin install goodcodereview@goodcodereview"
CONCERNS_INTRO = ("<p>Every card's rule on one page, and each row links to the full card. Pick one or more concerns to scope a review, such as performance only. "
                  "A card matches when it lists any picked concern, topic, or level. The picks go in the address, for example "
                  "<code>?concern=security,performance&amp;level=function</code>, so you can share the view. "
                  "Add <code>.md</code> or use <code>cards.json</code> for the same view as text or JSON.</p>")


def part_name(lv: Level, g: str, cards: list[Card]) -> tuple[str, str]:
    """The title and description of one part. The description counts stable cards only: a draft is not vetted."""
    title, covers = PARTS.get(f"{lv}-{g}", (f"{NAME[lv]}, {g} cards", f"the {g} part of the {lv} level"))
    n = sum(is_stable(c) for c in cards)
    return title, f"Review {covers}. {n} vetted check{'' if n == 1 else 's'} with FAIL and PASS examples and sources."


def part_spec(lv: Level, g: str, cards: list[Card]) -> PageSpec:
    """The page for one context of a split level. Raises BuildError when its description breaks the search-snippet length."""
    title, desc = part_name(lv, g, cards)
    if not MIN_DESC <= len(desc) <= MAX_DESC:
        raise BuildError(f"{lv}-{g}.html: description is {len(desc)} characters, want {MIN_DESC} to {MAX_DESC}")
    intro = f"<p>{LEVEL_DESC[lv]} This page holds the cards for the <code>{g}</code> {'part' if '-' in g else 'context'}. The <a href=\"{lv}.html\">{NAME[lv]}</a> page lists every card. {VERDICT}</p>"
    return PageSpec(f"{lv}-{g}.html", title, intro, tuple(cards), desc, parent=str(lv))


def hub_spec(b: BuildInput, lv: Level, g: str, cards: list[Card]) -> PageSpec:
    """The page for a context that was split again: it links each of its parts, and its rows keep the old `page#card-id` links alive."""
    parts = {b.part_of(c): sum(b.part_of(x) == b.part_of(c) for x in cards) for c in cards}
    title, desc = part_name(lv, g, cards)
    if not MIN_DESC <= len(desc) <= MAX_DESC:
        raise BuildError(f"{lv}-{g}.html: description is {len(desc)} characters, want {MIN_DESC} to {MAX_DESC}")
    links = ", ".join(f'<a href="{lv}-{p}.html">{p}</a> ({n})' for p, n in parts.items())
    intro = f"<p>{LEVEL_DESC[lv]} The <code>{g}</code> context is split into {len(parts)} pages so each stays small: {links}. Every row links to its card.</p>"
    return PageSpec(f"{lv}-{g}.html", title, intro, tuple(cards), desc, parent=str(lv))


def _regroup(cards: list[Card], key: Callable[[Card], list[str]], fallback: str) -> dict[str, list[Card]]:
    """The cards by the first value `key` gives (or `fallback`); a group under MIN_PART cards joins "other"."""
    groups: dict[str, list[Card]] = {}
    for c in cards:
        groups.setdefault((key(c) or [fallback])[0], []).append(c)
    small = [g for g, cs in groups.items() if len(cs) < MIN_PART and g != "other"]
    if len(small) > 1 or (small and "other" in groups):
        groups["other"] = groups.get("other", []) + [c for g in small for c in groups.pop(g)]
    return groups


def split_levels(b: BuildInput) -> BuildInput:
    """Split every level whose one-page HTML would reach PAGE_MAX characters of text into a hub plus parts.

    A level splits by `context`. A context part that is still too big splits by its cards' first concern, and a concern part
    that is still too big by the first topic tag (docs/adr/0002). The measure is the one tools/agent_ready_check.py applies
    (`Page.chars()`). Raises BuildError when a part is still too big after that.
    """
    def size(spec: PageSpec) -> int:
        return Page.parse(listing(spec, b.ids, b.links, empty=False, compact=False)).chars()

    over = frozenset(lv for lv in LEVELS if lv not in b.no_stable and size(PageSpec(f"{lv}.html", NAME[lv], "", tuple(b.core_at(lv)), "")) >= PAGE_MAX)
    split = b.with_split(over)
    plan: dict[str, str] = {}

    def fits(lv: Level, g: str, cs: list[Card]) -> bool:
        return size(part_spec(lv, g, cs)) < PAGE_MAX

    for lv in over:
        for g, cs in split.parts(lv).items():
            if fits(lv, g, cs):
                continue
            for sub, by_concern in _regroup(cs, concerns, "general").items():
                if fits(lv, f"{g}-{sub}", by_concern):
                    plan.update({c.fm["id"]: f"{g}-{sub}" for c in by_concern})
                    continue
                for tag, by_topic in _regroup(by_concern, topics, "general").items():
                    if not fits(lv, f"{g}-{sub}-{tag}", by_topic):
                        raise BuildError(f"{lv}-{g}-{sub}-{tag}.html is over {PAGE_MAX:,} characters of text; add a context or a tag that splits it")
                    plan.update({c.fm["id"]: f"{g}-{sub}-{tag}" for c in by_topic})
    return b.with_split(over, plan)


def page_specs(b: BuildInput) -> list[PageSpec]:
    """Level pages, pack pages, then the concerns page."""
    specs = []
    for lv in LEVELS:
        intro = f"<p>{LEVEL_DESC[lv]} Use it for this input: {INPUT[lv]}.{'' if lv in b.no_stable else ' ' + VERDICT}</p>"
        if lv == Level.INCIDENT:
            intro += f"<p>{inline(INCIDENT_RULE, {})}</p><p>An example:</p><pre class=\"wrap\"><code>{html.escape(INCIDENT_EXAMPLE)}</code></pre>"
        if lv in b.split:
            parts = b.parts(lv)
            intro += ("<p>This level is split by context so each page stays small. Every row links to its card on the page for its context: "
                      + ", ".join(f'<a href="{lv}-{g}.html">{g}</a> ({len(cs)})' for g, cs in parts.items()) + ".</p>")
        specs.append(PageSpec(f"{lv}.html", NAME[lv], intro, tuple(b.core_at(lv)), LEVEL_DESC[lv]))
        for g, cs in (b.parts(lv) if lv in b.split else {}).items():
            specs.append(part_spec(lv, g, cs))
        for g, cs in b.hubs(lv).items():
            specs.append(hub_spec(b, lv, g, cs))
    for pk in b.packs:
        specs.append(PageSpec(
            f"pack-{pk}.html", f"{pack_name(pk)} pack",
            f"<p>Cards specific to {pk}. Use them with the level page that matches your input. {VERDICT}</p>",
            tuple(c for c in b.cards if c.fm["lang"] == pk), PACK_DESC.format(pk=pk)))
    specs.append(PageSpec("concerns.html", "Concerns", CONCERNS_INTRO, b.cards, CONCERNS_DESC))
    return specs


def listing_pages(b: BuildInput) -> dict[str, str]:
    """The listing pages by file name. Raises BuildError when a card lost its FAIL or PASS block in rendering."""
    pages = {}
    hubs = {f"{lv}-{g}" for lv in b.split for g in b.hubs(lv)}
    for spec in page_specs(b):
        compact = spec.file == "concerns.html" or spec.file[:-5] in b.split | hubs
        out = listing(spec, b.ids, b.links, empty=spec.file[:-5] in b.no_stable, compact=compact, date=b.date)
        if "<code></code>" in out or out.count("<strong>PASS</strong>") != (0 if compact else len(spec.cards)):
            raise BuildError(f"{spec.file}: a card lost its FAIL or PASS block in rendering")
        pages[spec.file] = out
    return pages


def drafts_markdown(b: BuildInput) -> str:
    """The Drafts by what they lack page, as Markdown with [[card-id]] links."""
    if set(LACKS_LABEL) != set(LacksReason):
        raise BuildError("LACKS_LABEL must name every reason in LacksReason")
    drafts = [(c, d) for c in b.cards if (d := lacks(c))]
    by_lack = {r: [(c, d.note) for c, d in drafts if d.reason == r] for r in LACKS_LABEL}
    sections = [
        f"# {LACKS_LABEL[r][0].upper() + LACKS_LABEL[r][1:]} ({len(cs)})\n\n" + "\n".join(f"- [[{c.fm['id']}]] ({c.fm['level']}): {note}" for c, note in cs)
        for r, cs in by_lack.items() if cs
    ]
    return (f"Each draft card names what keeps it from stable in a `lacks:` line. This page groups the {len(drafts)} drafts by that reason. "
            f"[How a draft becomes stable]({REPO}/blob/main/docs/PROMOTION.md) gives the bar. "
            f"To promote one, open a [Promote a draft issue]({REPO}/issues/new?template=promote-draft.yml).\n\n" + "\n\n".join(sections))


def text_pages(b: BuildInput, drafts_md: str) -> dict[str, str]:
    """About, Privacy, Audit, Drafts, and the glossary."""
    specs = (("about", "About", ABOUT, ABOUT_DESC), ("faq", "FAQ", FAQ.replace("TALLY", b.tally), FAQ_DESC), ("privacy", "Privacy", PRIVACY, PRIVACY_DESC),
             ("audit", "Audit", AUDIT_INTRO + "\n\n" + "\n".join(AUDIT_STEPS), AUDIT_DESC),
             ("drafts", "Drafts by what they lack", drafts_md, DRAFTS_DESC))
    pages = {f"{slug}.html": page(title, md(text, b.ids), links=b.links, desc=desc, slug=slug) for slug, title, text, desc in specs}
    articles = "".join(f'<article id="{p.stem}">{md(p.read_text(), b.ids)}</article>' for p in b.glossary)
    pages["glossary.html"] = page("Glossary", articles, links=b.links, cur="glossary.html", desc=GLOSSARY_DESC, slug="glossary")
    return pages


def sample_verdict() -> str:
    """The sample verdict with each FAIL and PASS tag coloured. The words stay, so colour is never the only signal.

    Each line is a block with a hanging indent, so a wrapped line reads as a continuation.
    """
    def tint(line: str) -> str:
        for tag, cls in (("FAIL [block]", "block"), ("FAIL [should-fix]", "should-fix"), ("PASS", "ok")):
            if line.startswith(tag):
                return f'<span class="{cls}">{tag}</span>' + html.escape(line[len(tag):])
        return html.escape(line)

    return '<pre class="wrap v"><code>' + "".join(f'<span class="l">{tint(x)}\n</span>' for x in EXAMPLE.splitlines()) + "</code></pre>"


def home_page(b: BuildInput) -> str:
    rows = '<ul class="idx">' + "".join(
        f'<li><a href="{lv}.html">{NAME[lv]}</a><span>{LEVEL_DESC[lv]} Input: {INPUT[lv]}.</span>'
        f'<span class="n">{b.counts[lv].stable} stable, {b.counts[lv].draft} draft{f" · {EMPTY_MARK}" if lv in b.no_stable else ""}</span></li>' for lv in LEVELS) + "</ul>"
    ld = home_ld(b.date)
    agent = ("<h3 class=lane>With an agent</h3>"
             "<p>Paste this to your agent:</p>"
             + copy_pre("Read https://goodcodereview.com/llms.txt and use it to review my code.", "Copy prompt") +
             f'<p class="note">{inline(AGENTIC_NOTE, {})}</p>'
             '<p>Free and open source: code under MIT, content under CC BY 4.0.</p>'
             "<details><summary>Install it as a skill or a Claude Code plugin</summary>"
             "<p>To install it as a skill (Claude Code, Codex, Cursor, and other tools that read <code>skills/&lt;name&gt;/SKILL.md</code>), run:</p>"
             + copy_pre(INSTALL_SKILL, "Copy install command") +
             f"<p>{inline(INVOKE, {})}</p>"
             "<p>To install it as a Claude Code plugin, run:</p>"
             + copy_pre(INSTALL_PLUGIN, "Copy plugin commands") + "</details>")
    by_hand = ("<h3 class=lane>By hand</h3>"
               "<p>Pick the level that matches your input and work through its checklist. Only stable cards are vetted.</p>"
               f"<p>{b.tally}</p>{rows}")
    body = (
        f"<p class=lede>{HERO}</p>"
        "<h2>What a review looks like</h2>" + sample_verdict() + '<p class="note">The card ids are real. The paths and line numbers are made up.</p>'
        "<p>" + VERDICT + "</p>"
        "<h2>Start a review</h2>" + agent + by_hand +
        "<h2>Where the rules come from</h2><p>" + BACKING + ' Open a stable card, such as <a href="' + b.ids["svc-sqli-authn"] + '">svc-sqli-authn</a>, '
        "to see the organisations and the sources behind it.</p>"
        "<h2 class=s>Scope a review</h2><p>To review only some concerns, such as performance, use the <a href=\"concerns.html\">Concerns</a> page. "
        "Its filters live in the address, so <a href=\"concerns.html?concern=security,performance\">/concerns?concern=security,performance</a> opens the security and performance cards.</p>"
        "<h2 class=s>Audit a repo, service, or release</h2><p>" + inline(AUDIT_NOTE, {}) + "</p>"
        "<h2 class=s>Guides, packs, and feedback</h2>"
        "<p>Short explainers: " + ", ".join(f'<a href="guides/{g.slug}.html">{g.title.lower()}</a>' for g in GUIDES) + ".</p>"
        "<p>A pack adds language-specific cards on top of the levels. Use one with the level that matches your input: "
        + (", ".join(f'<a href="pack-{p}.html">{pack_name(p)} pack</a>' for p in b.packs) or "no packs yet") + ".</p>"
        "<p>" + inline(FEEDBACK, {}) + "</p>"
        '<p class="note">Writing CSS? <a href="https://good-css.com">good-css.com</a> has rules for reviewing CSS.</p>')
    return page("Good Code Review", body, links=b.links, cur="index.html", desc=SITE_DESC, slug="index", ld=ld, script=True, updated=b.date, stamp_in_footer=True)


def not_found_page(b: BuildInput) -> str:
    """Plain text a missing-page visitor or agent can act on. Root-relative links, because the host serves this file at any missing path."""
    entries = [("index.html", "Home", "choose a review level."), ("llms.txt", "llms.txt", "the entry point for agents: routing, verdict format, and every stable card."),
               ("sitemap.xml", "Sitemap", "every page.")] + [(f"{lv}.html", NAME[lv], LEVEL_DESC[lv]) for lv in LEVELS]
    body = ("<p>No page exists at this address, and the server answered with status 404. The link may be old or mistyped.</p>"
            "<p>These pages exist:</p><ul>" + "".join(f'<li><a href="{h}">{html.escape(t)}</a>: {d}</li>' for h, t, d in entries) + "</ul>")
    return re.sub(r'href="(?![a-z]+:|#|/)', 'href="/', page("Not found", body, links=b.links))


def guide_pages(b: BuildInput) -> dict[str, str]:
    """The guides index and each guide. They sit one folder down, so relative links become site-absolute, as on the 404 page."""
    def build(slug: str, title: str, text: str, desc: str, crumbs: tuple[tuple[str, str], ...]) -> str:
        return re.sub(r'href="(?![a-z]+:|#|/)', 'href="/', page(title, md(text, b.ids), links=b.links, cur="guides.html", desc=desc, slug=slug, updated=b.date, crumbs=crumbs))

    pages = {"guides.html": build("guides", "Guides", guides_index_text(html=True), GUIDES_DESC, (("Home", "index"), ("Guides", "guides")))}
    for g in GUIDES:
        pages[f"guides/{g.slug}.html"] = build(f"guides/{g.slug}", g.title, guide_text(b, g, html=True), g.desc,
                                                 (("Home", "index"), ("Guides", "guides"), (g.title, f"guides/{g.slug}")))
    return pages


def html_pages(b: BuildInput) -> dict[str, str]:
    """Every HTML file by name, in the order the original build wrote them."""
    pages = listing_pages(b)
    pages.update(text_pages(b, drafts_markdown(b)))
    pages["index.html"] = home_page(b)
    pages["404.html"] = not_found_page(b)
    pages.update(guide_pages(b))
    return pages

