#!/usr/bin/env python3
"""Validate, then emit site/ and skills/good-code-review/. Run from anywhere."""
import html
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent))
from validate import CONCERNS, LEVELS, load_cards, validate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SKILL = ROOT / "skills" / "good-code-review"
SKILL_BUDGET = 400  # max lines in SKILL.md
AUDIT = LEVELS[1:]
ROUTES = [
    ("diff / PR", "change"), ("file / function", "function"), ("package / path", "module"),
    ("service", "service"), ("cross-service design doc", "system"), ("repo", "codebase"),
    ("release / launch", "production"), ("incident", "incident"),
]
LEVEL_DESC = {
    "change": "Checks a diff or pull request: scope, size, compatibility, tests, and the description.",
    "function": "Checks one file or function: names, errors, concurrency, and security at the call level.",
    "module": "Checks a package or path: boundaries, state, dependencies, and the public surface.",
    "service": "Checks one running service: its API, failure handling, limits, and security.",
    "system": "Checks a design that spans services: shared data, caches, migrations, and failure modes.",
    "codebase": "Checks a whole repository: CI gates, dependencies, setup, and conventions.",
    "production": "Checks a release or launch: rollout, rollback, alerts, and load.",
    "incident": "Checks an incident and its follow-up: evidence, guards, and owned actions.",
}
INPUT = {lv: i for i, lv in ROUTES}
LEGEND = ('<p class="legend">Severity: <span class="b block">block</span> a FAIL blocks the change or release; '
          '<span class="b should-fix">should-fix</span> fix it, but it need not block; '
          '<span class="b discuss">discuss</span> raise it with the author. '
          'Status: <span class="b stable">stable</span> vetted, used for verdicts; '
          '<span class="b draft">draft</span> not vetted yet.</p>')
VERDICT = "Report each check as <code>PASS</code>, <code>FAIL</code>, or <code>N/A</code> with <code>file:line</code> evidence. A <code>FAIL</code> carries the card's severity."
DRAFT_NOTE = "A draft card is not vetted. Read it for ideas, but do not use it for a verdict."
CSS = """:root{--bg:#fff;--fg:#1a1a1a;--mut:#666;--line:#ddd;--acc:#0b5fff;--red:#c22;--grn:#1a7f1a;--amb:#a60}
@media(prefers-color-scheme:dark){:root{--bg:#121212;--fg:#e8e8e8;--mut:#9a9a9a;--line:#333;--acc:#6ea0ff;--red:#f06a6a;--grn:#5cc85c;--amb:#e0a040}}
[hidden]{display:none!important}
body{margin:0 auto;max-width:48rem;padding:1rem;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif;overflow-wrap:anywhere}
a{color:var(--acc)}nav{display:flex;flex-wrap:wrap;gap:.2rem .8rem;padding-bottom:.5rem;border-bottom:1px solid var(--line)}
pre{overflow-x:auto;background:var(--line);padding:.6rem;border-radius:4px}
code{font-family:ui-monospace,monospace;font-size:.9em}article{border-top:1px solid var(--line);padding:.5rem 0}
.b{display:inline-block;font-size:.75rem;padding:0 .5rem;border:1px solid var(--mut);border-radius:1rem;margin:0 .3rem .2rem 0}
.block{border-color:var(--red);color:var(--red)}.should-fix{border-color:var(--amb);color:var(--amb)}.stable{border-color:var(--grn);color:var(--grn)}
p.fail{border-left:4px solid var(--red);padding-left:.6rem;margin-bottom:0}p.pass{border-left:4px solid var(--grn);padding-left:.6rem;margin-bottom:0}
pre.fail{border-left:4px solid var(--red)}pre.pass{border-left:4px solid var(--grn)}
.flt{margin:.4rem 0}.flt b{margin-right:.4rem}
button{font:inherit;font-size:.85rem;cursor:pointer;color:var(--acc);background:none;border:1px solid var(--line);border-radius:1rem;padding:.1rem .6rem;margin:0 .3rem .3rem 0}
button[aria-pressed=true]{background:var(--acc);color:var(--bg);font-weight:bold}
ul.ck{list-style:none;padding:0}ul.ck li{border-top:1px solid var(--line);padding:.4rem 0}
.doors a{display:block;border:1px solid var(--line);padding:1rem;margin:.6rem 0;border-radius:6px}footer{color:var(--mut);margin-top:2rem}"""
JS = """const q=s=>[...document.querySelectorAll(s)],S={c:new Set(),t:new Set(),l:new Set()};
function go(){q('[data-tags]').forEach(a=>{const g=a.dataset.tags.split(' ');
a.hidden=(S.c.size>0&&![...S.c].some(x=>g.includes(x)))||[...S.t].some(x=>!g.includes(x))||(S.l.size>0&&!S.l.has(a.dataset.level))});
document.getElementById('empty').hidden=q('article[data-tags]:not([hidden])').length>0}
q('button[data-k]').forEach(b=>b.onclick=()=>{const s=S[b.dataset.k],v=b.dataset.v;
s.has(v)?s.delete(v):s.add(v);b.setAttribute('aria-pressed',s.has(v));go()});
const op=()=>{const e=document.getElementById(location.hash.slice(1)),d=e&&e.closest('details');if(d){d.open=true;e.scrollIntoView()}};
addEventListener('hashchange',op);op()"""
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3' fill='%230b5fff'/%3E%3Cpath d='M3.5 8.5l3 3 6-6' fill='none' stroke='%23fff' stroke-width='2'/%3E%3C/svg%3E"
# Markdown features md() cannot render. The build fails if a source file uses one outside a code fence.
UNSUPPORTED = {"numbered list": r"\s*\d+[.)] ", "table": r"\s*\|", "quote": r"\s*>", "nested bullet": r"\s{2,}[-*] ", "rule": r"-{3,}\s*$"}


def check_md(path, text):
    """Return an error per source line md() would render wrongly."""
    prose = re.sub(r"^```[^\n]*\n.*?^```[ \t]*$", "", text, flags=re.S | re.M)
    return [f"{path}: unsupported markdown ({k}): {l.strip()[:50]}"
            for l in prose.split("\n") for k, r in UNSUPPORTED.items() if re.match(r, l)]


def inline(s, ids):
    s = html.escape(s)
    codes = []
    s = re.sub(r"`([^`]+)`", lambda m: codes.append(m.group(1)) or f"\0{len(codes) - 1}\0", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\[\[([^\]]+)\]\]", lambda m: f'<a href="{ids.get(m.group(1), "#")}">{m.group(1)}</a>', s)
    return re.sub(r"\0(\d+)\0", lambda m: f"<code>{codes[int(m.group(1))]}</code>", s)


def md(text, ids):
    out, mark = [], ""
    for i, part in enumerate(re.split(r"^```[^\n]*\n(.*?)^```[ \t]*$", text, flags=re.S | re.M)):
        if i % 2:
            out.append(f'<pre class="{mark}"><code>{html.escape(part)}</code></pre>')
            mark = ""
            continue
        for blk in re.split(r"\n\s*\n", part.strip()):
            lines = blk.split("\n")
            if not blk.strip():
                continue
            if all(re.match(r"\s*[-*] ", l) for l in lines):
                out.append("<ul>" + "".join("<li>" + inline(re.sub(r"^\s*[-*] ", "", l), ids) + "</li>" for l in lines) + "</ul>")
            elif m := re.match(r"(#+) (.*)", blk):
                out.append(f"<h{len(m[1]) + 1}>{inline(m[2], ids)}</h{len(m[1]) + 1}>")
            elif blk.strip() in ("**FAIL**", "**PASS**"):
                mark = blk.strip()[2:-2].lower()
                out.append(f'<p class="{mark}">{inline(blk.strip(), ids)}</p>')
            else:
                out.append(f"<p>{inline(' '.join(lines), ids)}</p>")
    return "\n".join(out)


def page(title, body, script=False, links=()):
    nav = "<nav>" + "".join(f'<a href="{h}">{html.escape(t)}</a>' for h, t in links) + "</nav>"
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<link rel="icon" href="{FAVICON}">'
            f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>{nav}<h1>{html.escape(title)}</h1>{body}"
            f'<footer>Created and edited by <a href="https://pablogonzalez.me">Pablo González</a> · Content CC BY 4.0 · Code MIT · <a href="https://github.com/n0nuser/goodcodereview">Source</a></footer>'
            f"{'<script>' + JS + '</script>' if script else ''}</body></html>")


def concerns(fm):
    return [t for t in fm["tags"] if t in CONCERNS]


def chips(fm):
    return "".join(f'<span class="b">{c}</span>' for c in concerns(fm))


def sources(fm):
    urls = fm["borrowed_from"]
    return ("<p>Sources: " + ", ".join(f'<a href="{html.escape(u)}">{html.escape(urlparse(u).netloc)}</a>' for u in urls) + "</p>") if urls else ""


def card_html(fm, body, ids):
    b = f'<span class="b {fm["severity"]}">{fm["severity"]}</span><span class="b {fm["status"]}">{fm["status"]}</span>{chips(fm)}'
    gate = "" if fm["tool_gate"] == "none" else f'<p>Tool gate: {inline(fm["tool_gate"], ids)}</p>'
    return (f'<article id="{fm["id"]}" data-tags="{html.escape(" ".join(fm["tags"]))}" data-level="{fm["level"]}"><h3>{fm["id"]}</h3>{b}'
            f'<p><strong>Applies when:</strong> {inline(fm["applies_when"], ids)}</p>{md(body, ids)}{gate}{sources(fm)}</article>')


def row(fm, body, ids):
    return (f'<li data-tags="{html.escape(" ".join(fm["tags"]))}" data-level="{fm["level"]}"><a href="#{fm["id"]}">{fm["id"]}</a> '
            f'<span class="b {fm["severity"]}">{fm["severity"]}</span>{chips(fm)}<br>{inline(rule(body), ids)}</li>')


def buttons(label, key, values):
    return (f'<div class="flt" role="group" aria-label="{label}"><b>{label}</b>'
            + "".join(f'<button type="button" data-k="{key}" data-v="{html.escape(v)}" aria-pressed="false">{html.escape(v)}</button>' for v in values) + "</div>")


def listing(title, intro, cards, ids, links):
    stable = [c for c in cards if c[1]["status"] == "stable"]
    draft = [c for c in cards if c[1]["status"] != "stable"]
    seen = {t for _, fm, _ in cards for t in fm["tags"]}
    levels = [lv for lv in LEVELS if any(c[1]["level"] == lv for c in cards)]
    flt = buttons("Concerns", "c", [c for c in CONCERNS if c in seen])
    if len(levels) > 1:
        flt += buttons("Levels", "l", levels)
    topics = sorted(seen - set(CONCERNS))
    if topics:
        flt += "<details><summary>Topic tags</summary>" + buttons("Topics", "t", topics) + "</details>"
    ck = ('<ul class="ck">' + "".join(row(fm, b, ids) for _, fm, b in stable) + "</ul>") if stable else "<p>No stable cards yet. Draft cards are below.</p>"
    body = (intro + LEGEND + f"<h2>Filters</h2>{flt}<p id=\"empty\" hidden>No cards match these filters.</p>"
            f"<h2>Checklist</h2>{ck}<h2>Cards</h2>"
            + ("".join(card_html(fm, b, ids) for _, fm, b in stable) or "<p>No stable cards yet.</p>")
            + (f"<h2>Draft cards</h2><details><summary>{len(draft)} draft cards</summary><p>{DRAFT_NOTE}</p>"
               + "".join(card_html(fm, b, ids) for _, fm, b in draft) + "</details>" if draft else ""))
    return page(title, body, True, links)


def rule(body):
    m = re.search(r"\*\*Rule\.\*\*\s*(.*?)(?:\n\s*\n|$)", body, re.S)
    return " ".join(m.group(1).split()) if m else ""


def main():
    errs = validate(ROOT)
    if errs:
        print("\n".join(errs))
        sys.exit(1)
    cards = [(p, fm, b) for p, fm, b in load_cards(ROOT)]
    packs = sorted({fm["lang"] for _, fm, _ in cards if fm["lang"] != "core"})
    gloss = sorted((ROOT / "glossary").glob("*.md"))
    bad = [e for p, _, b in cards for e in check_md(p.relative_to(ROOT), b)] + [e for g in gloss for e in check_md(g.relative_to(ROOT), g.read_text())]
    if bad:
        sys.exit("\n".join(bad))
    ids = {fm["id"]: (f"pack-{fm['lang']}.html" if fm["lang"] != "core" else f"{fm['level']}.html") + f"#{fm['id']}"
           for _, fm, _ in cards}
    ids.update({g.stem: f"glossary.html#{g.stem}" for g in gloss})
    links = ([("index.html", "Home"), ("concerns.html", "Concerns")] + [(f"{lv}.html", lv) for lv in LEVELS]
             + [(f"pack-{pk}.html", f"pack: {pk}") for pk in packs] + [("glossary.html", "Glossary")])

    shutil.rmtree(SITE, ignore_errors=True)
    SITE.mkdir()
    pages = []  # (file, title, intro, cards)
    for lv in LEVELS:
        pages.append((f"{lv}.html", f"Level: {lv}",
                      f"<p>{LEVEL_DESC[lv]} Use it for this input: {INPUT[lv]}. {VERDICT}</p>",
                      [c for c in cards if c[1]["level"] == lv and c[1]["lang"] == "core"]))
    for pk in packs:
        pages.append((f"pack-{pk}.html", f"Pack: {pk}",
                      f"<p>Cards specific to {pk}. Use them with the level page that matches your input. {VERDICT}</p>",
                      [c for c in cards if c[1]["lang"] == pk]))
    pages.append(("concerns.html", "Concerns",
                  f"<p>Every card on one page. Pick one or more concerns to scope a review, such as performance only. A card matches when it lists any picked concern. {VERDICT}</p>",
                  cards))
    for f, title, intro, cs in pages:
        out = listing(title, intro, cs, ids, links)
        if "<code></code>" in out or out.count("<strong>PASS</strong>") != len(cs):
            sys.exit(f"{f}: a card lost its FAIL or PASS code block in rendering")
        (SITE / f).write_text(out)
    g = "".join(f'<article id="{p.stem}">{md(p.read_text(), ids)}</article>' for p in gloss)
    (SITE / "glossary.html").write_text(page("Glossary", g, links=links))
    (SITE / "robots.txt").write_text("User-agent: *\nAllow: /\n")
    (SITE / "404.html").write_text(page("Not found", '<p><a href="index.html">Back to the start</a></p>', links=links))
    npx = "npx skills add n0nuser/goodcodereview"
    plugin = "/plugin marketplace add n0nuser/goodcodereview\n/plugin install goodcodereview@goodcodereview"
    rows = lambda lvs: "<ul>" + "".join(f'<li><a href="{lv}.html">{lv}</a>: {LEVEL_DESC[lv]} Input: {INPUT[lv]}.</li>' for lv in lvs) + "</ul>"
    (SITE / "index.html").write_text(page("Good Code Review", (
        "<p>A checklist for reviewing code, for people and for agents. " + VERDICT + "</p>"
        "<h2>Start a review</h2>"
        "<p>Paste this to your agent:</p>"
        "<pre><code>Read https://goodcodereview.com/llms.txt and use it to review my code.</code></pre>"
        "<p>To install it as a skill (Claude Code, Codex, Cursor, and other tools that read <code>skills/&lt;name&gt;/SKILL.md</code>), run:</p>"
        f"<pre><code>{npx}</code></pre>"
        "<p>To install it as a Claude Code plugin, run:</p>"
        f"<pre><code>{plugin}</code></pre>"
        "<p>To review by hand, pick a level below and work through its checklist.</p>"
        f"<h2>Review a change</h2>{rows(['change'])}<h2>Audit existing code</h2>{rows(AUDIT)}"
        "<h2>Scope a review</h2><p>To review only some concerns, such as performance, use the <a href=\"concerns.html\">Concerns</a> page.</p>"
        "<h2>Packs</h2><p>A pack adds language-specific cards on top of the levels. Use one with the level that matches your input.</p>"
        "<p>" + (", ".join(f'<a href="pack-{p}.html">{p}</a>' for p in packs) or "No packs yet.") + "</p>"), links=links))

    stable = [c for c in cards if c[1]["status"] == "stable"]
    draft = [c for c in cards if c[1]["status"] != "stable"]
    (SKILL / "references").mkdir(parents=True, exist_ok=True)
    for f in (SKILL / "references").glob("*.md"):
        f.unlink()
    sk = ["---", "name: good-code-review",
          "description: Review code against stable cards, from a diff up to an incident. Use when asked to review, audit, or check code.",
          "---", "", "# Good Code Review", "", "## Routing", "", "| Input | Entry point |", "|---|---|"]
    sk += [f"| {i} | {lv} |" for i, lv in ROUTES]
    sk += ["", "## Verdict format", "", "Each check gets `PASS`, `FAIL`, or `N/A`, with `file:line` evidence.",
           "A `FAIL` carries the card's severity: `block`, `should-fix`, or `discuss`.", "",
           "The full text for each level is in `references/<level>.md`.", "",
           "## Scope by concern", "",
           "Each card lists its concerns in braces: " + ", ".join(f"`{c}`" for c in CONCERNS) + ".",
           "To review only some concerns, such as a performance-only review, check only the cards that list them.", ""]
    line = lambda fm, b: f"- `{fm['id']}` [{fm['severity']}] {{{', '.join(concerns(fm))}}}: {rule(b)}"
    for lv in LEVELS:
        cs = [c for c in stable if c[1]["level"] == lv]
        if not cs:
            continue
        sk += [f"## {lv}", ""] + [line(fm, b) for _, fm, b in cs] + [""]
        (SKILL / "references" / f"{lv}.md").write_text(
            f"# {lv}\n\n" + "\n\n".join(f"## {fm['id']}\n\nseverity: {fm['severity']}  \nconcerns: {', '.join(concerns(fm))}  \napplies_when: {fm['applies_when']}\n\n{b.strip()}"
                                        for _, fm, b in cs) + "\n")
    (SKILL / "SKILL.md").write_text("\n".join(sk))
    if len(sk) > SKILL_BUDGET:
        sys.exit(f"SKILL.md is {len(sk)} lines, budget {SKILL_BUDGET}")
    # llms.txt = SKILL.md body (same routing, verdict, scope, stable cards) with the reference pointer aimed at the site,
    # then the glossary, then drafts last. Drafts are never mixed into the vetted sections.
    llms = [("The full text of each card is at https://goodcodereview.com/<level>.html." if l.startswith("The full text") else l)
            for l in sk[5:]]
    llms += ["## Glossary (glossary.html)", ""] + [f"- {p.stem}" for p in gloss] + [""]
    llms += ["## Draft cards (not vetted; do not use for a verdict)", ""]
    for lv in LEVELS:
        cs = [c for c in draft if c[1]["level"] == lv and c[1]["lang"] == "core"]
        if cs:
            llms += [f"### {lv}", ""] + [line(fm, b) for _, fm, b in cs] + [""]
    for pk in packs:
        llms += [f"### pack {pk}", ""] + [line(fm, b) for _, fm, b in draft if fm["lang"] == pk] + [""]
    (SITE / "llms.txt").write_text("\n".join(llms))
    print(f"site: {len(pages) + 3} pages; SKILL.md: {len(sk)} lines; stable cards: {len(stable)}")


if __name__ == "__main__":
    main()
