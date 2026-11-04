"""The HTML pages of the site: level, pack, and concerns listings, the glossary, the text pages, the home page, and the 404."""
import html
import re

from card_fields import lacks
from config import REPO, SITE_DESC
from context import BuildInput, pack_name
from errors import BuildError
from guides import GUIDES, guide_text, guides_index_text
from listing import copy_pre, listing
from markdown import inline, md
from models import LEVELS, LacksReason, Level, PageSpec
from prose import (
    ABOUT,
    ABOUT_DESC,
    AUDIT_DESC,
    AUDIT_INTRO,
    AUDIT_NOTE,
    AUDIT_STEPS,
    BACKING,
    CONCERNS_DESC,
    DRAFTS_DESC,
    EMPTY_MARK,
    EXAMPLE,
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
from seo import home_ld
from shell import page

INSTALL_SKILL = "npx skills add n0nuser/goodcodereview"
INSTALL_PLUGIN = "/plugin marketplace add n0nuser/goodcodereview\n/plugin install goodcodereview@goodcodereview"
CONCERNS_INTRO = ("<p>Every card's rule on one page, and each row links to the full card. Pick one or more concerns to scope a review, such as performance only. "
                  "A card matches when it lists any picked concern, topic, or level. The picks go in the address, for example "
                  "<code>?concern=security,performance&amp;level=function</code>, so you can share the view. "
                  "Add <code>.md</code> or use <code>cards.json</code> for the same view as text or JSON.</p>")


def page_specs(b: BuildInput) -> list[PageSpec]:
    """Level pages, pack pages, then the concerns page."""
    specs = []
    for lv in LEVELS:
        intro = f"<p>{LEVEL_DESC[lv]} Use it for this input: {INPUT[lv]}.{'' if lv in b.no_stable else ' ' + VERDICT}</p>"
        if lv == Level.INCIDENT:
            intro += f"<p>{inline(INCIDENT_RULE, {})}</p><p>An example:</p><pre class=\"wrap\"><code>{html.escape(INCIDENT_EXAMPLE)}</code></pre>"
        specs.append(PageSpec(f"{lv}.html", NAME[lv], intro, tuple(b.core_at(lv)), LEVEL_DESC[lv]))
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
    for spec in page_specs(b):
        compact = spec.file == "concerns.html"
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
    specs = (("about", "About", ABOUT, ABOUT_DESC), ("privacy", "Privacy", PRIVACY, PRIVACY_DESC),
             ("audit", "Audit", AUDIT_INTRO + "\n\n" + "\n".join(AUDIT_STEPS), AUDIT_DESC),
             ("drafts", "Drafts by what they lack", drafts_md, DRAFTS_DESC))
    pages = {f"{slug}.html": page(title, md(text, b.ids), links=b.links, desc=desc, slug=slug) for slug, title, text, desc in specs}
    articles = "".join(f'<article id="{p.stem}">{md(p.read_text(), b.ids)}</article>' for p in b.glossary)
    pages["glossary.html"] = page("Glossary", articles, links=b.links, cur="glossary.html", desc=GLOSSARY_DESC, slug="glossary")
    return pages


def sample_verdict() -> str:
    """The sample verdict with each FAIL and PASS tag coloured. The words stay, so colour is never the only signal."""
    def tint(line: str) -> str:
        for tag, cls in (("FAIL [block]", "block"), ("FAIL [should-fix]", "should-fix"), ("PASS", "ok")):
            if line.startswith(tag):
                return f'<span class="{cls}">{tag}</span>' + html.escape(line[len(tag):])
        return html.escape(line)

    return '<pre class="wrap"><code>' + "\n".join(tint(x) for x in EXAMPLE.splitlines()) + "</code></pre>"


def home_page(b: BuildInput) -> str:
    rows = '<ul class="idx">' + "".join(
        f'<li><a href="{lv}.html">{NAME[lv]}</a><span>{LEVEL_DESC[lv]} Input: {INPUT[lv]}.</span>'
        f'<span class="n">{b.counts[lv].stable} stable, {b.counts[lv].draft} draft{f" · {EMPTY_MARK}" if lv in b.no_stable else ""}</span></li>' for lv in LEVELS) + "</ul>"
    ld = home_ld(b.date)
    agent = ("<h2>Start a review</h2>"
             "<p>Paste this to your agent:</p>"
             + copy_pre("Read https://goodcodereview.com/llms.txt and use it to review my code.", "Copy prompt") +
             f'<p>Free and open source. <a href="{REPO}">Star it on GitHub</a> to follow new cards.</p>'
             "<details><summary>Install it as a skill or a Claude Code plugin</summary>"
             "<p>To install it as a skill (Claude Code, Codex, Cursor, and other tools that read <code>skills/&lt;name&gt;/SKILL.md</code>), run:</p>"
             + copy_pre(INSTALL_SKILL, "Copy install command") +
             f"<p>{inline(INVOKE, {})}</p>"
             "<p>To install it as a Claude Code plugin, run:</p>"
             + copy_pre(INSTALL_PLUGIN, "Copy plugin commands") + "</details>")
    body = (
        f"<p>{HERO}</p>"
        "<h2>What a review looks like</h2>" + sample_verdict() + '<p class="note">The card ids are real. The paths and line numbers are made up.</p>' + agent +
        "<h2>Choose a review</h2>"
        "<p>To review by hand, pick the level that matches your input and work through its checklist. Only stable cards are vetted.</p>"
        f"<p>{b.tally}</p>{rows}"
        "<h2>Where the rules come from</h2><p>" + BACKING + ' Open a stable card, such as <a href="service.html#svc-sqli-authn">svc-sqli-authn</a>, '
        "to see the organisations and the sources behind it.</p>"
        "<h2>Scope a review</h2><p>To review only some concerns, such as performance, use the <a href=\"concerns.html\">Concerns</a> page. "
        "Its filters live in the address, so <a href=\"concerns.html?concern=security,performance\">concerns.html?concern=security,performance</a> opens the security and performance cards.</p>"
        "<h2>Report format</h2><p>" + VERDICT + "</p>"
        "<h2>Audit a repo, service, or release</h2><p>" + inline(AUDIT_NOTE, {}) + "</p>"
        "<h2>Feedback</h2><p>" + inline(FEEDBACK, {}) + "</p>"
        "<h2>Guides</h2><p>Short explainers: " + ", ".join(f'<a href="guides/{g.slug}.html">{g.title.lower()}</a>' for g in GUIDES) + ".</p>"
        "<h2>Packs</h2><p>A pack adds language-specific cards on top of the levels. Use one with the level that matches your input.</p>"
        "<p>" + (", ".join(f'<a href="pack-{p}.html">{pack_name(p)} pack</a>' for p in b.packs) or "No packs yet.") + "</p>"
        '<p class="note">Writing CSS? <a href="https://good-css.com">good-css.com</a> has rules for reviewing CSS.</p>')
    return page("Good Code Review", body, links=b.links, cur="index.html", desc=SITE_DESC, slug="index", ld=ld, script=True, updated=b.date)


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
        return re.sub(r'href="(?![a-z]+:|#|/)', 'href="/', page(title, md(text, b.ids), links=b.links, desc=desc, slug=slug, updated=b.date, crumbs=crumbs))

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

