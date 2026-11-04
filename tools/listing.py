"""HTML for cards: the full card, a checklist row, the filter buttons, and the listing pages built from them."""
import html
from collections.abc import Iterable, Sequence
from urllib.parse import urlparse

import orgs
import strength
from card_fields import concerns, is_stable, lacks, page_name
from config import REPO
from markdown import inline, md, rule
from models import CONCERNS, LEVELS, Card, NavLink, PageSpec
from prose import DRAFT_NOTE, EXAMPLE_HTML, LACKS_LABEL, LEGEND, NONE_NOTE, VERDICT
from shell import page


def chips(card: Card) -> str:
    return '<span class="tags">' + "".join(f"<span>{c}</span>" for c in concerns(card)) + "</span>"


def link_text(u: str) -> str:
    """A short, distinct label for a source link: the host and the last path segment, such as "w3.org/…/target-size-minimum"."""
    p = urlparse(u)
    host, parts = p.netloc.removeprefix("www."), [s for s in p.path.split("/") if s]
    return host + ("/" + "/".join(parts) if len(parts) < 2 else "/…/" + parts[-1]) + (f"#{p.fragment}" if p.fragment else "")


def icon(oid: str) -> str:
    return f'<svg class="oi" aria-hidden="true" focusable="false"><use href="#o-{oid}"/></svg>'


def _org_list(group: list[orgs.OrgUrls], card_id: str) -> str:
    return '<ul class="orgs">' + "".join(
        f'<li>{icon(g.id)}<span class="on">{html.escape(orgs.ORGS[g.id])}</span> '
        f'<span class="str" title="How well this organisation\'s sources back the Rule">({strength.of_org(card_id, g.urls)})</span>: '
        + ", ".join(f'<a href="{html.escape(u)}">{html.escape(link_text(u))}</a>' for u in g.urls) + "</li>" for g in group) + "</ul>"


def sources(card: Card) -> str:
    """The "Backed by" or "Cites" block: organisations first, then people."""
    found = orgs.split(card.fm["borrowed_from"])
    organisations, people = found.organisations, found.people
    head = "Backed by" if is_stable(card) else "Cites"
    if not organisations and not people:
        return f'<div class="by"><p class="note"><strong>{head}</strong> no organisation yet. This draft cites no source.</p></div>'
    cid = card.fm["id"]
    backing = strength.backing(cid, [g.urls for g in organisations])
    out = (f'<p class="note"><strong>{head}</strong> {len(organisations)} organisation{"s" * (len(organisations) != 1)}, backing {backing}:</p>{_org_list(organisations, cid)}'
           if organisations else f'<p class="note"><strong>{head}</strong> no organisation yet.</p>')
    if people:
        out += f'<p class="note"><strong>People cited:</strong></p>{_org_list(people, cid)}'
    return f'<div class="by">{out}</div>'


def lacks_html(card: Card, ids: dict[str, str]) -> str:
    draft_lack = lacks(card)
    if not draft_lack:
        return ""
    note = draft_lack.note
    return (f'<p class="note"><strong>Why it is a draft:</strong> {LACKS_LABEL[draft_lack.reason]}. {inline(note[:1].upper() + note[1:], ids)} '
            f'<a href="{REPO}/blob/main/docs/PROMOTION.md">How a draft becomes stable</a></p>')


def card_html(card: Card, ids: dict[str, str]) -> str:
    fm = card.fm
    badges = f'<span class="b {fm["severity"]}">{fm["severity"]}</span><span class="b {fm["status"]}">{fm["status"]}</span>{chips(card)}'
    gate = "" if fm["tool_gate"] == "none" else f'<p class="note">Tool gate: {inline(fm["tool_gate"], ids)}</p>'
    return (f'<article id="{html.escape(fm["id"])}" data-tags="{html.escape(" ".join(fm["tags"]))}" data-level="{fm["level"]}"><div class="ch"><h3>{html.escape(fm["id"])}</h3>{badges}</div>'
            f'<p><strong>Applies when:</strong> {inline(fm["applies_when"], ids)}</p>{md(card.body, ids)}{lacks_html(card, ids)}{gate}{sources(card)}</article>')


def row(card: Card, ids: dict[str, str], page_href: str = "") -> str:
    fm = card.fm
    return (f'<li data-tags="{html.escape(" ".join(fm["tags"]))}" data-level="{fm["level"]}"><a href="{page_href}#{html.escape(fm["id"])}">{html.escape(fm["id"])}</a> '
            f'<span class="b {fm["severity"]}">{fm["severity"]}</span>{chips(card)}<span class="r">{inline(rule(card.body), ids)}</span></li>')


def buttons(label: str, key: str, values: Iterable[str], count: dict[str, int], *, is_open: bool = True) -> str:
    """One collapsible filter group. The summary shows how many picks it holds; the script fills it in."""
    return (f'<details class="fg" data-k="{key}"{" open" if is_open else ""}><summary>{label} <span class="sel"></span></summary>'
            f'<div class="flt" role="group" aria-label="{label}">'
            + "".join(f'<button type="button" data-k="{key}" data-v="{html.escape(v)}" aria-pressed="false">{html.escape(v)} <span class="n">{count[v]}</span></button>' for v in values)
            + "</div></details>")


def copy_pre(text: str, label: str) -> str:
    return f"<pre class='wrap'><code>{text}</code></pre>" + f'<button type="button" data-copy="pre" hidden>{label}</button>'


_TABLE_HEAD = '<li class="th" aria-hidden="true"><span>Card</span><span>Severity</span><span>Concerns</span><span>Rule</span></li>'


def _filters(cards: Sequence[Card], stable: Sequence[Card], *, compact: bool) -> str:
    """The filter buttons, the group-by select, and the clear button."""
    seen = {t for c in cards for t in c.fm["tags"]}
    levels = [lv for lv in LEVELS if any(c.fm["level"] == lv for c in cards)]
    tally = {t: sum(t in c.fm["tags"] for c in stable) for t in seen}
    flt = buttons("Concerns", "c", [c for c in CONCERNS if c in seen and (not compact or tally[c])], {c: tally.get(c, 0) for c in CONCERNS})
    if len(levels) > 1:
        flt += buttons("Levels", "l", levels, {lv: sum(c.fm["level"] == lv for c in stable) for lv in levels})
    topics = sorted(t for t in seen - set(CONCERNS) if not compact or tally[t])
    if topics:
        flt += buttons("Topics", "t", topics, tally, is_open=False)
    groups = [g for g, on in (("concern", True), ("level", len(levels) > 1), ("topic", bool(topics))) if on]
    flt += ('<div class="flt"><label class="lab" for="grp">Group by</label><select id="grp" hidden><option value="">Nothing</option>'
            + "".join(f'<option value="{g}">{g.capitalize()}</option>' for g in groups) + "</select>"
            '<button type="button" id="clr" hidden>Clear filters</button></div>'
            '<p id="gnote" class="note" hidden>A card appears under each concern or topic it lists, so a group view can repeat a card.</p>')
    return flt


def listing(spec: PageSpec, ids: dict[str, str], links: Sequence[NavLink], *, empty: bool, compact: bool, date: str = "") -> str:
    """A level, pack, or concerns page. `empty` marks a level with no stable cards; `compact` shows rows that link to the full cards."""
    cards = spec.cards
    stable = [c for c in cards if is_stable(c)]
    draft = [c for c in cards if not is_stable(c)]
    flt = _filters(cards, stable, compact=compact)
    share = f'<p id="share" class="note" data-md="{"concerns" if compact else ""}" hidden></p>'
    # compact: one row per draft, linked to the page that holds the full card
    dbody = ('<div class="ckw"><ul class="ck">' + _TABLE_HEAD + "".join(row(c, ids, f"{page_name(c)}.html") for c in draft) + "</ul></div>"
             if compact else "".join(card_html(c, ids) for c in draft))
    drafts = (f'<h2>Draft cards</h2>{"" if stable or empty else "<p>No stable cards yet.</p>"}<details><summary id="dsum" data-n="{len(draft)}">{len(draft)} draft cards</summary>'
              f"<p>{inline(DRAFT_NOTE, {})}{' Each row links to the full card.' if compact else ''} "
              f'<a href="{REPO}/blob/main/docs/PROMOTION.md">How a draft becomes stable</a></p>' + dbody + "</details>") if draft else ""
    slug = spec.file[:-5]

    def render(body: str) -> str:
        return page(spec.title, body, links=links, cur=spec.file, desc=spec.desc, slug=slug, script=True, updated=date, crumbs=(("Home", "index"), (spec.title, slug)))

    if empty:
        return render(NONE_NOTE + spec.intro + LEGEND + drafts)
    intro = spec.intro + (f"<details><summary>How to report each check</summary><p>{VERDICT}</p>{EXAMPLE_HTML}</details>" if compact else EXAMPLE_HTML)
    if not stable:
        return render(intro + LEGEND + drafts)
    checklist = ('<button type="button" data-copy="ck" hidden>Copy checklist as markdown</button><div class="ckw" id="flat"><ul class="ck">' + _TABLE_HEAD
                 + "".join(row(c, ids, f"{page_name(c)}.html" if compact else "") for c in stable) + '</ul></div><div id="grouped" hidden></div>'
                 '<p class="note"><a href="#filters">Back to filters</a></p>')
    nojs = ("<noscript><p>The filters need JavaScript. Without it, the page lists every card. "
            "Add <code>?concern=security</code> to the Markdown or JSON address for a filtered list.</p></noscript>") if compact else ""
    body = (intro + f'<h2 id="filters">Filters</h2>{nojs}{flt}<p id="count" class="note" role="status"></p>{share}<p id="empty" hidden></p>'
            + f"<h2>Checklist</h2>{checklist}" + LEGEND
            + ("" if compact else "<h2>Cards</h2>" + "".join(card_html(c, ids) for c in stable)) + drafts)
    return render(body)
