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
LEGEND = ('<ul class="legend">'
          '<li><span class="b block">block</span><span>must be fixed before merge or release.</span></li>'
          '<li><span class="b should-fix">should-fix</span><span>fix it, but it need not block.</span></li>'
          '<li><span class="b discuss">discuss</span><span>raise it and decide together.</span></li>'
          '<li><span class="b stable">stable</span><span>vetted; use for verdicts.</span></li>'
          '<li><span class="b draft">draft</span><span>not vetted; do not use for a verdict.</span></li>'
          '<li class="tg">Tool gate: what a linter or CI check could enforce instead of a reviewer.</li></ul>')
SEVERITY = ["## Severity", "", "- `block`: must be fixed before merge or release.", "- `should-fix`: fix it, but it need not block.",
            "- `discuss`: raise it and decide together.", ""]
BASE = "https://goodcodereview.com"
NAME = {lv: "Change review" if lv == "change" else f"{lv.capitalize()} audit" for lv in LEVELS}
VERDICT = "Report each check as <code>PASS</code>, <code>FAIL</code>, or <code>N/A</code> with <code>file:line</code> evidence. A <code>FAIL</code> carries the card's severity."
DRAFT_NOTE = "A draft card is not vetted. Read it for ideas, but do not use it for a verdict."
CSS = """*,*::before,*::after{box-sizing:border-box;min-width:0}
:root{color-scheme:light dark;
--bg:light-dark(oklch(.985 0 none),oklch(.18 0 none));--fg:light-dark(oklch(.2 0 none),oklch(.93 0 none));
--mut:light-dark(oklch(.45 0 none),oklch(.76 0 none));--line:light-dark(oklch(.88 0 none),oklch(.32 0 none));
--edge:light-dark(oklch(.58 0 none),oklch(.58 0 none));
--acc:light-dark(oklch(.45 .09 190),oklch(.8 .08 180));--bad:light-dark(oklch(.48 .17 27),oklch(.78 .13 25));
--warn:light-dark(oklch(.47 .1 70),oklch(.8 .12 80));--good:light-dark(oklch(.45 .11 150),oklch(.78 .12 150));
--code:color-mix(in oklch,var(--fg) 6%,var(--bg));
--text:Charter,"Bitstream Charter","Sitka Text",Cambria,"Iowan Old Style","Palatino Linotype","Noto Serif",serif;
--ui:Seravek,"Gill Sans Nova",Ubuntu,Calibri,"DejaVu Sans","Noto Sans",sans-serif;
--mono:ui-monospace,"Cascadia Code","SF Mono",Menlo,Consolas,"DejaVu Sans Mono",monospace;
--narrow:20;--wide:77.5;--size-narrow:1;--size-wide:1.125;--ratio-narrow:1.2;--ratio-wide:1.25;
--fluid:clamp(0rem,(100vw - var(--narrow)*1rem)/(var(--wide) - var(--narrow)),1rem);
--at-narrow:calc(var(--size-narrow)*(1rem - var(--fluid)));--at-wide:calc(var(--size-wide)*var(--fluid));
--step-0:calc(var(--at-narrow) + var(--at-wide));--step--1:calc(var(--step-0)/var(--ratio-narrow));
--step-1:calc(var(--at-narrow)*var(--ratio-narrow) + var(--at-wide)*var(--ratio-wide));
--step-3:calc(var(--at-narrow)*pow(var(--ratio-narrow),3) + var(--at-wide)*pow(var(--ratio-wide),3));
--space-s:var(--step-0);--space-m:calc(1.5*var(--step-0));--space-l:calc(2*var(--step-0));--gutter:clamp(1rem,4vw,2rem);
--ease-out:cubic-bezier(.23,1,.32,1);
scrollbar-gutter:stable;scroll-padding-block-start:var(--space-m);text-wrap:pretty;overflow-wrap:break-word;font-synthesis:none;
-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}
[hidden]{display:none!important}
h1,h2,h3,h4{text-wrap:balance}
input,textarea,select{font-size:max(16px,1rem)}
button,a,summary{touch-action:manipulation}button{user-select:none;-webkit-user-select:none}
body{margin:0;min-block-size:100svh;display:grid;grid-template-rows:auto 1fr auto;align-content:start;
grid-template-columns:minmax(var(--gutter),1fr) minmax(0,62rem) minmax(var(--gutter),1fr);
background:var(--bg);color:var(--fg);font:var(--step-0)/1.55 var(--text)}
body>*{grid-column:2}
:where(h1,h2,h3,p,ul,pre,figure){margin:0}
:is(main,article)>*+*{margin-block-start:var(--space-s)}
p{max-inline-size:68ch}ul:not([class]){padding-inline-start:1.25em;max-inline-size:68ch}
h1,h2,h3{font-family:var(--ui);line-height:1.2}
main>h1{margin-block-start:var(--space-l);font-size:var(--step-3);font-weight:700;letter-spacing:-.01em}
main>h2{margin-block-start:var(--space-l);padding-block-start:var(--space-s);border-block-start:2px solid var(--fg);font-size:var(--step-1)}
article>h2{font-size:var(--step-1)}
h3{font:600 var(--step-0)/1.2 var(--mono)}
a{color:var(--acc);text-decoration-thickness:.07em;text-underline-offset:.2em}
:focus-visible{outline:max(2px,.08em) solid var(--acc);outline-offset:.2em}
nav{display:flex;flex-wrap:wrap;gap:0 var(--space-m);padding-block:var(--space-s);border-block-end:1px solid var(--line);font:var(--step--1)/1.3 var(--ui)}
nav a{padding-block:.5rem;color:var(--fg);text-decoration:none}
nav a[aria-current]{font-weight:700;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:.35em}
code{font:.9em var(--mono);padding:.08em .3em;background:var(--code);border-radius:2px;overflow-wrap:anywhere}
pre{padding:var(--space-s);overflow-x:auto;background:var(--code);border-radius:2px;font:var(--step--1)/1.5 var(--mono);tab-size:4}
pre code{padding:0;background:none;font:inherit;overflow-wrap:normal}
pre.wrap{max-inline-size:68ch;white-space:pre-wrap;overflow-wrap:anywhere}pre.wrap code{overflow-wrap:anywhere}
.b{display:inline-block;padding:.05em .45em;border:1px solid currentColor;border-radius:2px;color:var(--mut);font:600 var(--step--1)/1.3 var(--ui);white-space:nowrap}
.block{color:var(--bad)}.should-fix{color:var(--warn)}.stable{color:var(--fg)}.draft{border-style:dashed}
.tags{display:flex;flex-wrap:wrap;gap:0 .7em;color:var(--mut);font:var(--step--1)/1.4 var(--ui)}
.note{color:var(--mut);font:var(--step--1)/1.5 var(--ui)}
.legend{display:grid;grid-template-columns:max-content 1fr;gap:.4rem var(--space-s);padding:0;list-style:none;font:var(--step--1)/1.4 var(--ui)}
.legend li{grid-column:1/-1;display:grid;grid-template-columns:subgrid;align-items:baseline}.legend .b{justify-self:start}.legend li.tg{display:block}
.flt{display:flex;flex-wrap:wrap;align-items:center;gap:.75rem .5rem}
.lab{flex:none;inline-size:6.5rem;color:var(--mut);font:600 var(--step--1)/1.3 var(--ui)}
button{position:relative;padding:.4rem .7rem;color:var(--fg);background:none;border:1px solid var(--edge);border-radius:3px;font:500 var(--step--1)/1.2 var(--ui);cursor:pointer;transition:background-color .15s,border-color .15s}
button::after{content:"";position:absolute;inset:min(0px,(100% - 44px)/2)}
button[aria-pressed=true]{font-weight:700;background:var(--acc);border-color:var(--acc);color:var(--bg)}
button:active{transform:scale(.97)}
details{border-block-start:1px solid var(--line)}
summary{padding-block:.75rem;cursor:pointer;font:600 var(--step--1)/1.3 var(--ui)}
details[open]>summary{border-block-end:1px solid var(--line)}
#dsum,#empty{font-variant-numeric:tabular-nums}
.ckw{container-type:inline-size}
ul.ck{padding:0;list-style:none}
ul.ck li{display:flex;flex-wrap:wrap;align-items:baseline;gap:.2rem var(--space-s);padding-block:.6rem;border-block-start:1px solid var(--line)}
ul.ck a{font:600 var(--step--1)/1.4 var(--mono)}
ul.ck .r{flex:1 0 100%;max-inline-size:68ch}
ul.ck .th{display:none}
@container (min-width:46rem){
ul.ck{display:grid;grid-template-columns:max-content max-content fit-content(11rem) minmax(0,1fr);column-gap:var(--space-m)}
ul.ck li{grid-column:1/-1;display:grid;grid-template-columns:subgrid}
ul.ck .r{flex:none}
ul.ck .th{display:grid;border-block-start:0;border-block-end:1px solid var(--edge);padding-block:.25rem;color:var(--mut);font:600 var(--step--1)/1.3 var(--ui)}
}
ul.idx{padding:0;list-style:none}
ul.idx li{display:flex;flex-wrap:wrap;gap:0 var(--space-s);padding-block:.55rem;border-block-start:1px solid var(--line)}
ul.idx a{flex:1 1 10rem;font:600 var(--step-0)/1.5 var(--ui)}ul.idx span{flex:3 1 22rem}
article{padding-block:var(--space-m);border-block-start:1px solid var(--line)}
h2+article{border-block-start:0}
.ch{display:flex;flex-wrap:wrap;align-items:baseline;gap:.3rem var(--space-s)}
.ex{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,24rem),1fr));gap:var(--space-s)}
figure{--tone:var(--mut);border-block-start:2px solid var(--tone)}
figure.fail{--tone:var(--bad)}figure.pass{--tone:var(--good)}
figcaption{padding-block:.3rem;color:var(--tone);font:700 var(--step--1)/1.3 var(--ui)}
figure pre{background:color-mix(in oklch,var(--tone) 7%,var(--bg));border-radius:0;white-space:pre-wrap;overflow-wrap:anywhere}figure pre code{overflow-wrap:anywhere}
article:target>.ch h3{text-decoration:underline;text-decoration-color:var(--acc);text-decoration-thickness:.15em;text-underline-offset:.2em}
footer{margin-block-start:var(--space-l);padding-block:var(--space-s) var(--space-m);border-block-start:1px solid var(--line);color:var(--mut);font:var(--step--1)/1.5 var(--ui)}
@media(hover:hover) and (pointer:fine){
a:hover{text-decoration-thickness:.16em}nav a:hover,summary:hover{color:var(--acc)}
button:hover{border-color:var(--fg)}ul.ck li:not(.th):hover{background:color-mix(in oklch,var(--fg) 4%,transparent)}
}
@media(prefers-reduced-motion:no-preference){
html{scroll-behavior:smooth}button{transition:transform 140ms var(--ease-out),background-color .15s,border-color .15s}
}"""
JS = """const q=s=>[...document.querySelectorAll(s)],S={c:new Set(),t:new Set(),l:new Set()},E=document.getElementById('empty'),D=document.getElementById('dsum');
function go(){q('[data-tags]').forEach(a=>{const g=a.dataset.tags.split(' ');
a.hidden=(S.c.size>0&&![...S.c].some(x=>g.includes(x)))||[...S.t].some(x=>!g.includes(x))||(S.l.size>0&&!S.l.has(a.dataset.level))});
const on=S.c.size+S.t.size+S.l.size>0,s=q('article[data-tags]:not([hidden])').filter(a=>!a.closest('details')).length,d=q('details article[data-tags]:not([hidden])').length;
if(E){E.hidden=!on||s>0;E.textContent='No stable cards match.'+(d?' '+d+' draft '+(d>1?'cards match':'card matches')+' below.':'')}
if(D)D.textContent=D.dataset.n+' draft cards'+(on?' ('+d+' match)':'')}
q('button[data-k]').forEach(b=>b.onclick=()=>{const s=S[b.dataset.k],v=b.dataset.v;
s.has(v)?s.delete(v):s.add(v);b.setAttribute('aria-pressed',s.has(v));go()});
const op=()=>{const e=document.getElementById(location.hash.slice(1)),d=e&&e.closest('details');if(d){d.open=true;e.scrollIntoView()}};
addEventListener('hashchange',op);op()"""
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3' fill='%23006469'/%3E%3Cpath d='M3.5 8.5l3 3 6-6' fill='none' stroke='%23fff' stroke-width='2'/%3E%3C/svg%3E"
# Markdown features md() cannot render. The build fails if a source file uses one outside a code fence.
UNSUPPORTED = {"numbered list": r"\s*\d+[.)] ", "table": r"\s*\|", "quote": r"\s*>", "nested bullet": r"\s{2,}[-*] ", "rule": r"-{3,}\s*$"}


def check_md(path, text):
    """Return an error per source line md() would render wrongly."""
    prose = re.sub(r"^```[^\n]*\n.*?^```[ \t]*$", "", text, flags=re.S | re.M)
    return ([f"{path}: unsupported markdown ({k}): {l.strip()[:50]}"
             for l in prose.split("\n") for k, r in UNSUPPORTED.items() if re.match(r, l)]
            + [f"{path}: heading with text on the next line: {b.strip()[:50]}"
               for b in re.split(r"\n\s*\n", prose) if re.match(r"#+ ", b) and "\n" in b.strip()])


def inline(s, ids):
    s = html.escape(s)
    codes = []
    s = re.sub(r"`([^`]+)`", lambda m: codes.append(m.group(1)) or f"\0{len(codes) - 1}\0", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\[\[([^\]]+)\]\]", lambda m: f'<a href="{ids.get(m.group(1), "#")}">{m.group(1)}</a>', s)
    return re.sub(r"\0(\d+)\0", lambda m: f"<code>{codes[int(m.group(1))]}</code>", s)


def md(text, ids):
    out, mark = [], ""
    for i, part in enumerate(re.split(r"^```[^\n]*\n(.*?)^```[ \t]*$", text, flags=re.S | re.M)):
        if i % 2:
            pre = f"<pre><code>{html.escape(part)}</code></pre>"
            out.append(f'<figure class="{mark}"><figcaption>{inline(f"**{mark.upper()}**", ids)}</figcaption>{pre}</figure>' if mark else pre)
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
            else:
                out.append(f"<p>{inline(' '.join(lines), ids)}</p>")
    fig = lambda c: rf'(<figure class="{c}">(?:(?!</figure>).)*</figure>)'
    return re.sub(fig("fail") + "\n" + fig("pass"), r'<div class="ex">\1\2</div>', "\n".join(out), flags=re.S)


def page(title, body, script=False, links=(), cur=""):
    nav = '<header><nav aria-label="Site">' + "".join(f'<a href="{h}"{" aria-current=page" if h == cur else ""}>{html.escape(t)}</a>' for h, t in links) + "</nav></header>"
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark">'
            f'<link rel="icon" href="{FAVICON}">'
            f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>{nav}<main><h1>{html.escape(title)}</h1>{body}</main>"
            f'<footer>Created and edited by <a href="https://pablogonzalez.me">Pablo González</a> · Content CC BY 4.0 · Code MIT · <a href="https://github.com/n0nuser/goodcodereview">Source</a> · Styled with <a href="https://good-css.com">good-css.com</a></footer>'
            f"{'<script>' + JS + '</script>' if script else ''}</body></html>")


def concerns(fm):
    return [t for t in fm["tags"] if t in CONCERNS]


def chips(fm):
    return '<span class="tags">' + "".join(f"<span>{c}</span>" for c in concerns(fm)) + "</span>"


def sources(fm):
    urls = fm["borrowed_from"]
    return ('<p class="note">Sources: ' + ", ".join(f'<a href="{html.escape(u)}">{html.escape(urlparse(u).netloc)}</a>' for u in urls) + "</p>") if urls else ""


def card_html(fm, body, ids):
    b = f'<span class="b {fm["severity"]}">{fm["severity"]}</span><span class="b {fm["status"]}">{fm["status"]}</span>{chips(fm)}'
    gate = "" if fm["tool_gate"] == "none" else f'<p class="note">Tool gate: {inline(fm["tool_gate"], ids)}</p>'
    return (f'<article id="{html.escape(fm["id"])}" data-tags="{html.escape(" ".join(fm["tags"]))}" data-level="{fm["level"]}"><div class="ch"><h3>{html.escape(fm["id"])}</h3>{b}</div>'
            f'<p><strong>Applies when:</strong> {inline(fm["applies_when"], ids)}</p>{md(body, ids)}{gate}{sources(fm)}</article>')


def row(fm, body, ids):
    return (f'<li data-tags="{html.escape(" ".join(fm["tags"]))}" data-level="{fm["level"]}"><a href="#{html.escape(fm["id"])}">{html.escape(fm["id"])}</a> '
            f'<span class="b {fm["severity"]}">{fm["severity"]}</span>{chips(fm)}<span class="r">{inline(rule(body), ids)}</span></li>')


def buttons(label, key, values):
    return (f'<div class="flt" role="group" aria-label="{label}"><span class="lab">{label}</span>'
            + "".join(f'<button type="button" data-k="{key}" data-v="{html.escape(v)}" aria-pressed="false">{html.escape(v)}</button>' for v in values) + "</div>")


def listing(title, intro, cards, ids, links, cur):
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
    drafts = (f'<h2>Draft cards</h2>{"" if stable else "<p>No stable cards yet.</p>"}<details><summary id="dsum" data-n="{len(draft)}">{len(draft)} draft cards</summary>'
              f"<p>{DRAFT_NOTE}</p>" + "".join(card_html(fm, b, ids) for _, fm, b in draft) + "</details>") if draft else ""
    if not stable:
        return page(title, intro + LEGEND + drafts, True, links, cur)
    th = '<li class="th" aria-hidden="true"><span>Card</span><span>Severity</span><span>Concerns</span><span>Rule</span></li>'
    ck = '<div class="ckw"><ul class="ck">' + th + "".join(row(fm, b, ids) for _, fm, b in stable) + "</ul></div>"
    body = (intro + LEGEND + f'<h2>Filters</h2>{flt}<p id="empty" hidden></p>'
            f"<h2>Checklist</h2>{ck}<h2>Cards</h2>" + "".join(card_html(fm, b, ids) for _, fm, b in stable) + drafts)
    return page(title, body, True, links, cur)


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
    links = ([("index.html", "Home"), ("concerns.html", "Concerns")] + [(f"{lv}.html", NAME[lv]) for lv in LEVELS]
             + [(f"pack-{pk}.html", f"{pk.capitalize()} pack") for pk in packs] + [("glossary.html", "Glossary")])

    shutil.rmtree(SITE, ignore_errors=True)
    SITE.mkdir()
    pages = []  # (file, title, intro, cards)
    for lv in LEVELS:
        pages.append((f"{lv}.html", NAME[lv],
                      f"<p>{LEVEL_DESC[lv]} Use it for this input: {INPUT[lv]}. {VERDICT}</p>",
                      [c for c in cards if c[1]["level"] == lv and c[1]["lang"] == "core"]))
    for pk in packs:
        pages.append((f"pack-{pk}.html", f"{pk.capitalize()} pack",
                      f"<p>Cards specific to {pk}. Use them with the level page that matches your input. {VERDICT}</p>",
                      [c for c in cards if c[1]["lang"] == pk]))
    pages.append(("concerns.html", "Concerns",
                  f"<p>Every card on one page. Pick one or more concerns to scope a review, such as performance only. A card matches when it lists any picked concern. {VERDICT}</p>",
                  cards))
    for f, title, intro, cs in pages:
        out = listing(title, intro, cs, ids, links, f)
        if "<code></code>" in out or out.count("<strong>PASS</strong>") != len(cs):
            sys.exit(f"{f}: a card lost its FAIL or PASS code block in rendering")
        (SITE / f).write_text(out)
    g = "".join(f'<article id="{p.stem}">{md(p.read_text(), ids)}</article>' for p in gloss)
    (SITE / "glossary.html").write_text(page("Glossary", g, links=links, cur="glossary.html"))
    (SITE / "robots.txt").write_text("User-agent: *\nAllow: /\n")
    (SITE / "404.html").write_text(page("Not found", '<p><a href="index.html">Back to the start</a></p>', links=links))
    npx = "npx skills add n0nuser/goodcodereview"
    plugin = "/plugin marketplace add n0nuser/goodcodereview\n/plugin install goodcodereview@goodcodereview"
    rows = lambda lvs: '<ul class="idx">' + "".join(f'<li><a href="{lv}.html">{NAME[lv]}</a><span>{LEVEL_DESC[lv]} Input: {INPUT[lv]}.</span></li>' for lv in lvs) + "</ul>"
    (SITE / "index.html").write_text(page("Good Code Review", (
        "<p>A checklist for reviewing code, for people and for agents. A card is one rule that a reviewer marks <code>PASS</code>, <code>FAIL</code>, or <code>N/A</code>. Each card has a FAIL example and a PASS example.</p>"
        "<p>" + VERDICT + "</p>"
        "<h2>Start a review</h2>"
        "<p>Paste this to your agent:</p>"
        "<pre class='wrap'><code>Read https://goodcodereview.com/llms.txt and use it to review my code.</code></pre>"
        "<p>To install it as a skill (Claude Code, Codex, Cursor, and other tools that read <code>skills/&lt;name&gt;/SKILL.md</code>), run:</p>"
        f"<pre class='wrap'><code>{npx}</code></pre>"
        "<p>To install it as a Claude Code plugin, run:</p>"
        f"<pre class='wrap'><code>{plugin}</code></pre>"
        "<p>To review by hand, pick a level below and work through its checklist.</p>"
        f"<h2>Choose a review</h2>{rows(LEVELS)}"
        "<h2>Scope a review</h2><p>To review only some concerns, such as performance, use the <a href=\"concerns.html\">Concerns</a> page.</p>"
        "<h2>Packs</h2><p>A pack adds language-specific cards on top of the levels. Use one with the level that matches your input.</p>"
        "<p>" + (", ".join(f'<a href="pack-{p}.html">{p.capitalize()} pack</a>' for p in packs) or "No packs yet.") + "</p>"
        '<p class="note">Writing CSS? <a href="https://good-css.com">good-css.com</a> has the rules this site\'s CSS follows.</p>'), links=links, cur="index.html"))

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
    # llms.txt = SKILL.md body (same routing, verdict, scope, stable cards), opened by the SKILL description, with a Severity
    # section and a full-text URL per level added. Then the glossary, then drafts last, never mixed into the vetted sections.
    url = lambda fm: f"{BASE}/pack-{fm['lang']}.html" if fm["lang"] != "core" else f"{BASE}/{fm['level']}.html"
    body = list(sk[5:])
    k = next(i for i, l in enumerate(body) if l.startswith("The full text"))
    del body[k:k + 2]
    llms = [body[0], "", sk[2][len("description: "):], ""]
    seen_level = False
    for l in body[2:]:
        if l.startswith("## ") and l[3:] in LEVELS:
            if not seen_level:
                llms += SEVERITY
                seen_level = True
            llms += [l, "", f"Full text: {BASE}/{l[3:]}.html"]
        else:
            llms.append(l)
    llms += ["## Glossary", "", f"Terms the cards link to: {BASE}/glossary.html", ""]
    llms += ["## Draft cards (not vetted; do not use for a verdict)", ""]
    for lv in LEVELS:
        cs = [c for c in draft if c[1]["level"] == lv and c[1]["lang"] == "core"]
        if cs:
            llms += [f"### {lv}", "", f"Full text: {url(cs[0][1])}", ""] + [line(fm, b) for _, fm, b in cs] + [""]
    for pk in packs:
        cs = [c for c in draft if c[1]["lang"] == pk]
        llms += [f"### pack {pk}", "", f"Full text: {url(cs[0][1])}", ""] + [line(fm, b) for _, fm, b in cs] + [""]
    text = "\n".join(llms)
    vetted, _, drafts = text.partition("## Draft cards")
    idre = lambda t: re.findall(r"^- `([^`]+)` \[", t, re.M)
    if idre(vetted) != idre("\n".join(sk)) or {fm["id"] for _, fm, _ in draft} & set(idre(vetted)) or "\n## " in drafts:
        sys.exit("llms.txt: stable ids before the draft heading differ from SKILL.md, or a draft sits before it")
    (SITE / "llms.txt").write_text(text)
    print(f"site: {len(pages) + 3} pages; SKILL.md: {len(sk)} lines; stable cards: {len(stable)}")


if __name__ == "__main__":
    main()
