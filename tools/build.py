#!/usr/bin/env python3
"""Validate, then emit site/ and skills/good-code-review/. Run from anywhere."""
import datetime
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent))
from validate import CONCERNS, LEVELS, load_cards, validate  # noqa: E402
import schema  # noqa: E402

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
LEGEND = f'<details><summary>What the badges mean</summary>{LEGEND}</details>'
NONE_NOTE = (f'<p><strong>No vetted cards for this level yet.</strong> It gives no verdict. '
             'For the code fix, use <a href="change.html">Change review</a>.</p>')
SEVERITY = ["## Severity", "", "- `block`: must be fixed before merge or release.", "- `should-fix`: fix it, but it need not block.",
            "- `discuss`: raise it and decide together.", ""]
BASE = "https://goodcodereview.com"
REPO = "https://github.com/n0nuser/goodcodereview"
SITE_NAME = "Good Code Review"
SITE_DESC = "A checklist for reviewing code, for people and for agents. Every check ends in PASS, FAIL, or N/A with file:line evidence."
LICENCE_URL = "https://creativecommons.org/licenses/by/4.0/"
NAME = {lv: "Change review" if lv == "change" else f"{lv.capitalize()} audit" for lv in LEVELS}
VERDICT = ("Report each check as <code>PASS</code>, <code>FAIL</code>, or <code>N/A</code> with <code>file:line</code> evidence. A <code>FAIL</code> carries the card's severity. "
           "Any <code>block</code> <code>FAIL</code> means request changes. A <code>should-fix</code> or <code>discuss</code> <code>FAIL</code> goes in the review but does not block.")
EXAMPLE = """FAIL [block] chg-expand-contract - src/a.py:42 - renames the column and drops the old one in one migration
FAIL [should-fix] chg-one-concern - src/b.py:7 - a logging rewrite rides along with the bug fix
PASS chg-breaking-change-taxonomy - src/c.py:15 - no signature or return shape changes
N/A chg-perf-claim-evidence - the description makes no performance claim"""
EXAMPLE_HTML = f'<pre class="wrap"><code>{html.escape(EXAMPLE)}</code></pre>'
INCIDENT_RULE = ("An incident review also checks the stable cards of the level where the cause lived: `change` for a bad release or migration, "
                 "`function`, `module`, `service`, or `system` for code and design, and `production` for rollout, alerting, and capacity. "
                 "Quote the incident text as evidence in place of `file:line`. "
                 "Those `FAIL` and `PASS` lines are real verdicts, and any `block` `FAIL` still means request changes.")
INCIDENT_EXAMPLE = "\n".join([
    'FAIL [block] chg-expand-contract - postmortem, Cause: "the deploy renamed the column and dropped the old one in one migration"',
    'PASS inc-perf-fix-has-profile-evidence - postmortem, Fix: "CPU profile: 61% in json.Marshal; after the fix, p99 1.9 s -> 240 ms under the same load"'])
EMPTY_MARK = "no vetted cards yet"
EMPTY_RULE = (f'A level marked "{EMPTY_MARK}" has no stable cards. Give no verdict for it. Say that there are no vetted cards for that level yet. '
              "You may list its draft cards as notes, never as `PASS` or `FAIL`.")
DRAFT_RULE = "Draft cards are never verdicts."
# One closing prompt for design-level reviews. It sits outside the PASS/FAIL ledger.
DESIGN_NOTE = "For a system or codebase review, end with one note outside the ledger: name the decision you would most want written down and what its alternative costs. Cite file:line for the decision. Give no verdict and no severity for it."
DRAFT_NOTE = "A draft card is not vetted. Read it for ideas, but do not use it for a verdict."
PACK_DESC = "Draft cards specific to {pk}, not vetted. Use them with the level page that matches your input."
CONCERNS_DESC = "Every card's rule on one page. Pick a concern, such as performance or security, to scope a review."
GLOSSARY_DESC = "Terms that the cards link to, with a note on why a reviewer cares."
ABOUT_DESC = "Who makes Good Code Review, what stable and draft cards mean, and the licences."
PRIVACY_DESC = "Good Code Review collects nothing: no cookies, no analytics, no accounts."
WHEN_TO_USE = ("Use this site when you are asked to review, audit, or check code: a diff or pull request, a file or function, a package, a service, "
               "a design document that spans services, a repository, a release, or an incident. Match the input to a level in the routing table, "
               "then check every stable card for that level and report each as `PASS`, `FAIL`, or `N/A` with evidence. "
               "To review only some concerns, such as performance, check only the cards that list them. "
               "Do not use it to write code or to run tests, and never turn a draft card into a verdict.")
ABOUT = """Good Code Review is a checklist for reviewing code, for people and for agents. Each check is a card: one rule that a reviewer marks `PASS`, `FAIL`, or `N/A`, with a FAIL example and a PASS example. The cards are grouped into eight levels, from a single diff up to an incident, so a reviewer picks the level that matches the input.

# Who makes it

[Pablo González](https://pablogonzalez.me) created and edits the site and the cards. The cards, the build script, and the skill files are in the [GitHub repository](https://github.com/n0nuser/goodcodereview).

# What stable and draft mean

A stable card is vetted, and its FAIL and PASS lines are real verdicts. A draft card is not vetted. Read it for ideas, but do not use it for a verdict. The home page shows how many cards of each kind every level has.

# How the site is built

`python3 tools/build.py` reads the cards in the repository and writes this site as plain static files, plus the Markdown, `llms.txt`, and skill files that agents read. Cloudflare Pages hosts the result. There is no database and no server code.

# Cost and licence

The site and the cards are free to read and use. The content is under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) and the code is under the MIT licence.

# Contact

To report a wrong card, propose a card, or ask a question, open an issue on [GitHub Issues](https://github.com/n0nuser/goodcodereview/issues)."""
PRIVACY = """This site collects nothing about you. It sets no cookies, runs no analytics or tracking scripts, has no accounts or forms, and stores nothing in your browser.

# What runs in your browser

The filter buttons and the copy buttons use a small script that is part of each page. It runs only in your browser, makes no network requests, and sends nothing anywhere. Every page reads fine with JavaScript turned off. Without it, the filter buttons do nothing and the copy buttons stay hidden.

# What loads from other sites

Nothing. Pages load no fonts, images, scripts, or styles from other sites. Links to other sites, such as the author's website and GitHub, load only when you follow them, and those sites have their own policies.

# Hosting

Cloudflare Pages hosts the site. Like any web host, it handles each request and may keep standard server logs under its own privacy policy. That is outside this site's code.

# Contact

Questions about this page go through [GitHub Issues](https://github.com/n0nuser/goodcodereview/issues)."""
INDEX_MD = """# Good Code Review

A checklist for reviewing code, for people and for agents. A card is one rule that a reviewer marks `PASS`, `FAIL`, or `N/A`. Each card has a FAIL example and a PASS example.

## Choose a review

Pick the level that matches your input and work through its checklist. Only stable cards are vetted.

{levels}

## Scope a review

To review only some concerns, such as performance, use the [Concerns page](https://goodcodereview.com/concerns.md).

## Start a review with an agent

Paste this to your agent:

```text
Read https://goodcodereview.com/llms.txt and use it to review my code.
```

To install it as a skill, run:

```text
{npx}
```

To install it as a Claude Code plugin, run:

```text
{plugin}
```

## Report format

{verdict}

```text
{example}
```

## Packs

{packs}
"""
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
nav{display:flex;flex-wrap:wrap;align-items:center;gap:0 var(--space-m);padding-block:var(--space-s);border-block-end:1px solid var(--line);font:var(--step--1)/1.3 var(--ui)}
nav a,nav summary{display:flex;align-items:center;min-block-size:44px;padding-block:0;color:var(--fg);text-decoration:none}
nav a[aria-current]{font-weight:700;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:.35em}
nav details{border:0}nav details[open]{flex:1 0 100%}nav details[open]>summary{border:0}
nav details:has([aria-current])>summary{font-weight:700}
nav details>div{display:flex;flex-wrap:wrap;gap:0 var(--space-m);padding-inline-start:var(--space-s)}
.skip{position:absolute;inset-block-start:-100px;inset-inline-start:var(--space-s);z-index:1;display:flex;align-items:center;min-block-size:44px;padding-inline:var(--space-s);background:var(--bg);color:var(--fg);border:2px solid var(--acc);font:600 var(--step--1)/1.3 var(--ui)}
.skip:focus{inset-block-start:var(--space-s)}
main:focus{outline:none}
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
#dsum,#empty,#count{font-variant-numeric:tabular-nums}
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
ul.idx a{flex:1 1 10rem;font:600 var(--step-0)/1.5 var(--ui)}ul.idx span{flex:3 1 22rem}ul.idx span.n{flex:1 1 10rem;color:var(--mut);font:var(--step--1)/1.5 var(--ui);font-variant-numeric:tabular-nums}
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
.fl{display:flex;flex-wrap:wrap;gap:0 var(--space-m);margin:0;padding:0;list-style:none}.fl a{display:flex;align-items:center;min-block-size:44px}
@media(hover:hover) and (pointer:fine){
a:hover{text-decoration-thickness:.16em}nav a:hover,summary:hover{color:var(--acc)}
button:hover{border-color:var(--fg)}ul.ck li:not(.th):hover{background:color-mix(in oklch,var(--fg) 4%,transparent)}
}
@media(prefers-reduced-motion:no-preference){
html{scroll-behavior:smooth}button{transition:transform 140ms var(--ease-out),background-color .15s,border-color .15s}
}"""
JS = """const q=s=>[...document.querySelectorAll(s)],S={c:new Set(),t:new Set(),l:new Set()},E=document.getElementById('empty'),D=document.getElementById('dsum'),C=document.getElementById('count');
function go(){q('[data-tags]').forEach(a=>{const g=a.dataset.tags.split(' ');
a.hidden=(S.c.size>0&&![...S.c].some(x=>g.includes(x)))||[...S.t].some(x=>!g.includes(x))||(S.l.size>0&&!S.l.has(a.dataset.level))});
const on=S.c.size+S.t.size+S.l.size>0,s=q('li[data-tags]:not([hidden])').filter(a=>!a.closest('details')).length,d=q('details [data-tags]:not([hidden])').length;
if(E){E.hidden=!on||s>0;E.textContent='No stable cards match.'+(d?' '+d+' draft '+(d>1?'cards match':'card matches')+' below.':'')}
if(D)D.textContent=D.dataset.n+' draft cards'+(on?' ('+d+' match)':'')
if(C)C.textContent=on?s+' stable and '+d+' draft '+(s+d==1?'card matches.':'cards match.'):''}
q('button[data-k]').forEach(b=>b.onclick=()=>{const s=S[b.dataset.k],v=b.dataset.v;
s.has(v)?s.delete(v):s.add(v);b.setAttribute('aria-pressed',s.has(v));go()});
q('button[data-copy]').forEach(b=>{const l=b.textContent;b.hidden=false;b.onclick=()=>{
const t=b.dataset.copy=='ck'?q('ul.ck li[data-tags]:not([hidden])').filter(r=>!r.closest('details')).map(r=>'- `'+r.querySelector('a').textContent+'` ['+r.querySelector('.b').textContent+'] '+r.querySelector('.r').textContent+' PASS/FAIL/N/A: ').join('\\n'):b.previousElementSibling.textContent;
(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>b.textContent='Copied',()=>b.textContent='Copy failed');setTimeout(()=>b.textContent=l,1500)}});
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
    lang = ""
    for i, part in enumerate(re.split(r"^```([^\n]*)\n(.*?)^```[ \t]*$", text, flags=re.S | re.M)):
        if i % 3 == 1:
            lang = part.strip()
            continue
        if i % 3 == 2:
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            pre = f"<pre><code{cls}>{html.escape(part)}</code></pre>"
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


def page_url(slug):
    """The URL Cloudflare Pages serves: it redirects /x.html to /x and /index.html to /."""
    return BASE + "/" if slug == "index" else f"{BASE}/{slug}"


def head_tags(title, desc, slug):
    """Canonical, description, Open Graph, discovery links, and the site-type declaration. The 404 page gets none."""
    if not slug:
        return ""
    q = lambda t: html.escape(t, quote=True)
    og = {"title": title, "description": desc, "type": "website", "url": page_url(slug), "site_name": SITE_NAME,
          "image": f"{BASE}/og.png", "image:alt": f"{SITE_NAME}: {SITE_DESC}", "image:width": "1200", "image:height": "630"}
    return (f'<meta name="description" content="{q(desc)}"><link rel="canonical" href="{page_url(slug)}">'
            + "".join(f'<meta property="og:{k}" content="{q(v)}">' for k, v in og.items())
            + f'<link rel="alternate" type="text/markdown" href="/{slug}.md"><link rel="alternate" type="text/plain" href="/llms.txt" title="llms.txt">'
            '<link rel="sitemap" type="application/xml" href="/sitemap.xml"><meta name="is-agentic-site-type" content="content">')


FOOTER = (f'<footer><p>Created and edited by <a href="https://pablogonzalez.me">Pablo González</a> · Content CC BY 4.0 · Code MIT · <a href="{REPO}">Source</a></p>'
          '<ul class="fl"><li><a href="about.html">About</a></li><li><a href="privacy.html">Privacy</a></li>'
          f'<li><a href="{REPO}/issues">Contact (GitHub Issues)</a></li><li><a href="llms.txt">llms.txt</a></li><li><a href="sitemap.xml">Sitemap</a></li>'
          f'<li><a href="{REPO}/blob/main/AGENTS.md">AGENTS.md</a></li><li><a href="{REPO}/tree/main/skills/good-code-review">Skill folder</a></li></ul></footer>')


def page(title, body, script=False, links=(), cur="", desc="", slug="", ld=None):
    aud = {f"{lv}.html" for lv in AUDIT}
    a = lambda h, t: f'<a href="{h}"{" aria-current=page" if h == cur else ""}>{html.escape(t)}</a>'
    items = [a(h, t) for h, t in links if h not in aud]
    menu = "".join(a(h, t) for h, t in links if h in aud)
    if menu:
        items.insert(next(i for i, (h, _) in enumerate(links) if h in aud), f'<details><summary>Audits</summary><div>{menu}</div></details>')
    nav = '<header><nav aria-label="Site">' + "".join(items) + "</nav></header>"
    full = title if slug == "index" else f"{title} | {SITE_NAME}"
    jsonld = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>" if ld else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark">'
            f'<link rel="icon" href="{FAVICON}">'
            f"<title>{html.escape(full)}</title>{head_tags(full, desc, slug)}<style>{CSS}</style>{jsonld}</head><body><a class=skip href=#main>Skip to content</a>{nav}<main id=main tabindex=-1><h1>{html.escape(title)}</h1>{body}</main>"
            f"{FOOTER}{'<script>' + JS + '</script>' if script else ''}</body></html>")


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


def row(fm, body, ids, href=""):
    return (f'<li data-tags="{html.escape(" ".join(fm["tags"]))}" data-level="{fm["level"]}"><a href="{href}#{html.escape(fm["id"])}">{html.escape(fm["id"])}</a> '
            f'<span class="b {fm["severity"]}">{fm["severity"]}</span>{chips(fm)}<span class="r">{inline(rule(body), ids)}</span></li>')


def buttons(label, key, values):
    return (f'<div class="flt" role="group" aria-label="{label}"><span class="lab">{label}</span>'
            + "".join(f'<button type="button" data-k="{key}" data-v="{html.escape(v)}" aria-pressed="false">{html.escape(v)}</button>' for v in values) + "</div>")


def copy_pre(text, label):
    return f"<pre class='wrap'><code>{text}</code></pre>" + f'<button type="button" data-copy="pre" hidden>{label}</button>'


def listing(title, intro, cards, ids, links, cur, desc, empty=False, compact=False):
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
    th = '<li class="th" aria-hidden="true"><span>Card</span><span>Severity</span><span>Concerns</span><span>Rule</span></li>'
    # compact: one row per draft, linked to the page that holds the full card
    home_page = lambda fm: f"pack-{fm['lang']}.html" if fm["lang"] != "core" else f"{fm['level']}.html"
    dbody = ('<div class="ckw"><ul class="ck">' + th + "".join(row(fm, b, ids, home_page(fm)) for _, fm, b in draft) + "</ul></div>"
             if compact else "".join(card_html(fm, b, ids) for _, fm, b in draft))
    drafts = (f'<h2>Draft cards</h2>{"" if stable or empty else "<p>No stable cards yet.</p>"}<details><summary id="dsum" data-n="{len(draft)}">{len(draft)} draft cards</summary>'
              f"<p>{DRAFT_NOTE}{' Each row links to the full card.' if compact else ''}</p>" + dbody + "</details>") if draft else ""
    if empty:
        return page(title, NONE_NOTE + intro + LEGEND + drafts, True, links, cur, desc, cur[:-5])
    intro += EXAMPLE_HTML
    if not stable:
        return page(title, intro + LEGEND + drafts, True, links, cur, desc, cur[:-5])
    ck = ('<button type="button" data-copy="ck" hidden>Copy checklist as markdown</button><div class="ckw"><ul class="ck">' + th
          + "".join(row(fm, b, ids, home_page(fm) if compact else "") for _, fm, b in stable) + "</ul></div>")
    body = (intro + f"<h2>Checklist</h2>{ck}" + LEGEND + f'<h2>Filters</h2>{"<noscript><p>The filters need JavaScript. Without it, the page lists every card.</p></noscript>" if compact else ""}{flt}<p id="count" class="note" role="status"></p><p id="empty" hidden></p>'
            + ("" if compact else "<h2>Cards</h2>" + "".join(card_html(fm, b, ids) for _, fm, b in stable)) + drafts)
    return page(title, body, True, links, cur, desc, cur[:-5])


def rule(body):
    m = re.search(r"\*\*Rule\.\*\*\s*(.*?)(?:\n\s*\n|$)", body, re.S)
    return " ".join(m.group(1).split()) if m else ""


def section(body, label):
    m = re.search(rf"\*\*{label}\.\*\*\s*(.*?)(?:\n\s*\n|$)", body, re.S)
    return " ".join(m.group(1).split()) if m else ""


def corpus(kind, cs, cnt, date):
    """The cards.json model: kind "stable" for the vetted core cards, "drafts" for every other card."""
    def card(fm, body):
        where = f"pack-{fm['lang']}" if fm["lang"] != "core" else fm["level"]
        return schema.Card(
            id=fm["id"], level=fm["level"], status=fm["status"], severity=fm["severity"], concerns=concerns(fm),
            topics=[t for t in fm["tags"] if t not in CONCERNS], lang=fm["lang"], applies_when=fm["applies_when"],
            tool_gate=None if fm["tool_gate"] == "none" else fm["tool_gate"], note=fm.get("note"),
            rule=rule(body), why=section(body, "Why"), counterpoint=section(body, "Counterpoint"),
            fail=schema.example(body, "FAIL"), pass_=schema.example(body, "PASS"), sources=fm["borrowed_from"],
            url=f"{page_url(where)}#{fm['id']}", markdown_url=f"{BASE}/{where}.md")
    levels = [schema.LevelInfo(id=lv, name=NAME[lv], input=INPUT[lv], description=LEVEL_DESC[lv], stable_count=cnt[lv][0], draft_count=cnt[lv][1],
                               gives_verdict=bool(cnt[lv][0]), url=page_url(lv), markdown_url=f"{BASE}/{lv}.md") for lv in LEVELS]
    return schema.Corpus(schema.SCHEMA_VERSION, kind, SITE_NAME, f"{BASE}/", LICENCE_URL, date, list(CONCERNS), levels,
                         [card(fm, b) for _, fm, b in cs])


def check_routes(by_lv, refs, skill_text, stable_ids):
    """Return an error per routed level whose stable cards, reference file, or empty-level text disagree."""
    errs = []
    for _, lv in ROUTES:
        row = f"| {lv} ({EMPTY_MARK}) |" in skill_text
        if by_lv[lv] and not (refs / f"{lv}.md").is_file():
            errs.append(f"routed level '{lv}' has stable cards but no references/{lv}.md")
        if by_lv[lv] and row:
            errs.append(f"routed level '{lv}' has stable cards but is marked '{EMPTY_MARK}'")
        if not by_lv[lv] and not (row and EMPTY_RULE in skill_text):
            errs.append(f"routed level '{lv}' has no stable cards and the routing text lacks the empty-level rule")
    if INCIDENT_RULE not in skill_text:
        errs.append("the routing text lacks the incident rule")
    errs += [f"EXAMPLE names '{i}', which is not a stable card" for i in re.findall(r"^(?:FAIL \[[a-z-]+\]|PASS|N/A) ([a-z0-9-]+)", EXAMPLE + "\n" + INCIDENT_EXAMPLE, re.M) if i not in stable_ids]
    return errs


def build_date():
    """One date for every lastmod and `updated`: the HEAD commit date, or today's date outside a git checkout."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        out = ""
    return out or datetime.date.today().isoformat()


def front(title, desc, slug, date):
    """YAML frontmatter for a served Markdown file. JSON strings are valid YAML."""
    return "---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in
                               {"title": title, "description": desc, "canonical": page_url(slug), "updated": date}.items()) + "\n---\n\n"


def headers_file(slugs):
    """Cloudflare Pages `_headers`: https://developers.cloudflare.com/pages/configuration/headers/"""
    md = lambda s: f'</{s}.md>; rel="alternate"; type="text/markdown"'
    out = ["# Generated by tools/build.py. Format: https://developers.cloudflare.com/pages/configuration/headers/",
           "/*", '  Link: </sitemap.xml>; rel="sitemap", </llms.txt>; rel="describedby"',
           "  Strict-Transport-Security: max-age=31536000",
           "  X-Content-Type-Options: nosniff",
           "  Referrer-Policy: strict-origin-when-cross-origin",
           # frame-ancestors only: the pages carry an inline script and inline styles, so a script-src policy would block them.
           "  Content-Security-Policy: frame-ancestors 'none'"]
    for s in slugs:
        out += ["/" if s == "index" else f"/{s}", f"  Link: {md(s)}"]
    out += ["/*.md", "  Content-Type: text/markdown; charset=utf-8", "/*.txt", "  Content-Type: text/plain; charset=utf-8",
            "/sitemap.xml", "  Content-Type: application/xml; charset=utf-8",
            "/.well-known/agent-skills/index.json", "  Content-Type: application/json; charset=utf-8"]
    return "\n".join(out) + "\n"


def main():
    errs = validate(ROOT)
    if errs:
        print("\n".join(errs))
        sys.exit(1)
    cards = [(p, fm, b) for p, fm, b in load_cards(ROOT)]
    packs = sorted({fm["lang"] for _, fm, _ in cards if fm["lang"] != "core"})
    gloss = sorted((ROOT / "glossary").glob("*.md"))
    bad = [e for p, _, b in cards for e in check_md(p.relative_to(ROOT), b)] + [e for g in gloss for e in check_md(g.relative_to(ROOT), g.read_text())]
    bad += [f"{n}: {e}" for n, t in (("ABOUT", ABOUT), ("PRIVACY", PRIVACY)) for e in check_md(n, t)]
    if bad:
        sys.exit("\n".join(bad))
    date = build_date()
    ids = {fm["id"]: (f"pack-{fm['lang']}.html" if fm["lang"] != "core" else f"{fm['level']}.html") + f"#{fm['id']}"
           for _, fm, _ in cards}
    ids.update({g.stem: f"glossary.html#{g.stem}" for g in gloss})
    cnt = {lv: [sum(c[1]["level"] == lv and c[1]["lang"] == "core" and (c[1]["status"] == "stable") == st for c in cards) for st in (True, False)] for lv in LEVELS}
    none = {lv for lv in LEVELS if not cnt[lv][0]}
    label = lambda lv: NAME[lv] + (f" ({EMPTY_MARK})" if lv in none else "")
    links = ([("index.html", "Home"), ("concerns.html", "Concerns")] + [(f"{lv}.html", label(lv)) for lv in LEVELS]
             + [(f"pack-{pk}.html", f"{pk.capitalize()} pack") for pk in packs] + [("glossary.html", "Glossary")])

    shutil.rmtree(SITE, ignore_errors=True)
    SITE.mkdir()
    pages = []  # (file, title, intro, cards, description)
    for lv in LEVELS:
        pages.append((f"{lv}.html", NAME[lv],
                      f"<p>{LEVEL_DESC[lv]} Use it for this input: {INPUT[lv]}.{'' if lv in none else ' ' + VERDICT}</p>",
                      [c for c in cards if c[1]["level"] == lv and c[1]["lang"] == "core"], LEVEL_DESC[lv]))
    inc = next(i for i, pg in enumerate(pages) if pg[0] == "incident.html")
    pages[inc] = (*pages[inc][:2], pages[inc][2] + f"<p>{inline(INCIDENT_RULE, {})}</p><p>An example:</p>"
                  f'<pre class="wrap"><code>{html.escape(INCIDENT_EXAMPLE)}</code></pre>', *pages[inc][3:])
    for pk in packs:
        pages.append((f"pack-{pk}.html", f"{pk.capitalize()} pack",
                      f"<p>Cards specific to {pk}. Use them with the level page that matches your input. {VERDICT}</p>",
                      [c for c in cards if c[1]["lang"] == pk], PACK_DESC.format(pk=pk)))
    pages.append(("concerns.html", "Concerns",
                  f"<p>Every card's rule on one page, and each row links to the full card. Pick one or more concerns to scope a review, such as performance only. A card matches when it lists any picked concern. {VERDICT}</p>",
                  cards, CONCERNS_DESC))
    for f, title, intro, cs, desc in pages:
        out = listing(title, intro, cs, ids, links, f, desc, f[:-5] in none, f == "concerns.html")
        if "<code></code>" in out or out.count("<strong>PASS</strong>") != (0 if f == "concerns.html" else len(cs)):
            sys.exit(f"{f}: a card lost its FAIL or PASS code block in rendering")
        (SITE / f).write_text(out)
    g = "".join(f'<article id="{p.stem}">{md(p.read_text(), ids)}</article>' for p in gloss)
    (SITE / "glossary.html").write_text(page("Glossary", g, links=links, cur="glossary.html", desc=GLOSSARY_DESC, slug="glossary"))
    for slug, title, text, desc in (("about", "About", ABOUT, ABOUT_DESC), ("privacy", "Privacy", PRIVACY, PRIVACY_DESC)):
        (SITE / f"{slug}.html").write_text(page(title, md(text, ids), links=links, desc=desc, slug=slug))
    npx = "npx skills add n0nuser/goodcodereview"
    plugin = "/plugin marketplace add n0nuser/goodcodereview\n/plugin install goodcodereview@goodcodereview"
    rows = '<ul class="idx">' + "".join(
        f'<li><a href="{lv}.html">{NAME[lv]}</a><span>{LEVEL_DESC[lv]} Input: {INPUT[lv]}.</span>'
        f'<span class="n">{cnt[lv][0]} stable, {cnt[lv][1]} draft{f" · {EMPTY_MARK}" if lv in none else ""}</span></li>' for lv in LEVELS) + "</ul>"
    person = {"@type": "Person", "name": "Pablo González", "url": "https://pablogonzalez.me",
              "description": "Maintainer of Good Code Review.", "sameAs": ["https://github.com/n0nuser"]}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": SITE_NAME, "description": SITE_DESC, "inLanguage": "en",
         "license": LICENCE_URL, "author": person, "dateModified": date,
         "sameAs": ["https://github.com/n0nuser/goodcodereview"]},
        {"@type": "CreativeWork", "@id": f"{BASE}/#checklist", "url": f"{BASE}/", "name": "Good Code Review checklist",
         "description": "Rules for reviewing code, one card per rule, each with a FAIL example and a PASS example.", "inLanguage": "en",
         "isPartOf": {"@id": f"{BASE}/#website"}, "license": LICENCE_URL, "author": person, "dateModified": date}]}
    (SITE / "index.html").write_text(page("Good Code Review", (
        "<p>A checklist for reviewing code, for people and for agents. A card is one rule that a reviewer marks <code>PASS</code>, <code>FAIL</code>, or <code>N/A</code>. Each card has a FAIL example and a PASS example.</p>"
        "<h2>Choose a review</h2>"
        "<p>To review by hand, pick the level that matches your input and work through its checklist. Only stable cards are vetted.</p>"
        f"{rows}"
        "<h2>Scope a review</h2><p>To review only some concerns, such as performance, use the <a href=\"concerns.html\">Concerns</a> page.</p>"
        "<h2>Start a review with an agent</h2>"
        "<p>Paste this to your agent:</p>"
        + copy_pre("Read https://goodcodereview.com/llms.txt and use it to review my code.", "Copy prompt") +
        "<p>To install it as a skill (Claude Code, Codex, Cursor, and other tools that read <code>skills/&lt;name&gt;/SKILL.md</code>), run:</p>"
        + copy_pre(npx, "Copy install command") +
        "<p>To install it as a Claude Code plugin, run:</p>"
        + copy_pre(plugin, "Copy plugin commands") +
        "<h2>Report format</h2><p>" + VERDICT + "</p>" + EXAMPLE_HTML +
        "<h2>Packs</h2><p>A pack adds language-specific cards on top of the levels. Use one with the level that matches your input.</p>"
        "<p>" + (", ".join(f'<a href="pack-{p}.html">{p.capitalize()} pack</a>' for p in packs) or "No packs yet.") + "</p>"
        '<p class="note">Writing CSS? <a href="https://good-css.com">good-css.com</a> has rules for reviewing CSS.</p>'), True, links, "index.html", SITE_DESC, "index", ld))

    stable = [c for c in cards if c[1]["status"] == "stable"]
    draft = [c for c in cards if c[1]["status"] != "stable"]
    (SKILL / "references").mkdir(parents=True, exist_ok=True)
    for f in (SKILL / "references").glob("*.md"):
        f.unlink()
    by_lv = {lv: [c for c in stable if c[1]["level"] == lv] for lv in LEVELS}
    empty = [lv for _, lv in ROUTES if not by_lv[lv]]
    home = {fm["id"]: fm["level"] for _, fm, _ in stable}
    # A stable card links only to another stable card, as a relative path inside references/. Any other target is plain text.
    link = lambda t: re.sub(r"\[\[([^\]]+)\]\]", lambda m: f"[{m[1]}]({home[m[1]]}.md#{m[1]})" if m[1] in home else m[1], t)
    plain = VERDICT.replace("<code>", "`").replace("</code>", "`")
    sk = ["---", "name: good-code-review",
          "description: Review code against stable cards, from a diff up to an incident. Use when asked to review, audit, or check code.",
          "---", "", "# Good Code Review", "", "## Routing", "", "| Input | Entry point |", "|---|---|"]
    sk += [f"| {i} | {lv}{f' ({EMPTY_MARK})' if lv in empty else ''} |" for i, lv in ROUTES]
    sk += ["", INCIDENT_RULE, ""] + ([EMPTY_RULE, ""] if empty else [])
    sk += ["## Verdict format", ""] + plain.replace(". ", ".\n").split("\n") + ["", "```", EXAMPLE, "```", "", DRAFT_RULE, "", DESIGN_NOTE, "",
           "The full text for each level is in `references/<level>.md`.",
           *[f"{pk.capitalize()} pack (draft cards, not vetted): {BASE}/pack-{pk}.html" for pk in packs],
           f"Glossary: {BASE}/glossary.html",
           f"Draft cards (not vetted): {BASE}/llms-drafts.txt", "",
           "## Scope by concern", "",
           "Each card lists its concerns in braces: " + ", ".join(f"`{c}`" for c in CONCERNS) + ".",
           "To review only some concerns, such as a performance-only review, check only the cards that list them.", ""]
    line = lambda fm, b: f"- `{fm['id']}` [{fm['severity']}] {{{', '.join(concerns(fm))}}}: {rule(b)}"
    section = lambda fm, b: f"## {fm['id']}\n\nseverity: {fm['severity']}  \nconcerns: {', '.join(concerns(fm))}  \napplies_when: {fm['applies_when']}\n\n{b.strip()}"
    refs = {}
    twins = {}  # slug -> (title, description, markdown body). Each gets frontmatter and is written to site/<slug>.md.
    for lv in LEVELS:
        cs = by_lv[lv]
        if not cs:
            twins[lv] = (NAME[lv], LEVEL_DESC[lv], f"# {lv}\n\nNo vetted cards for this level yet. It gives no verdict.\n")
            continue
        sk += [f"## {lv}", ""] + [line(fm, b) for _, fm, b in cs] + [""]
        refs[lv] = link(f"# {lv}\n\n" + "\n\n".join(section(fm, b) for _, fm, b in cs) + "\n")
        (SKILL / "references" / f"{lv}.md").write_text(refs[lv])
        twins[lv] = (NAME[lv], LEVEL_DESC[lv], refs[lv])
    if "incident" in twins:
        t = twins["incident"]
        twins["incident"] = (*t[:2], t[2].replace("# incident\n\n", f"# incident\n\n{INCIDENT_RULE}\n\n", 1))
    bad = check_routes(by_lv, SKILL / "references", "\n".join(sk), set(home))
    if bad:
        sys.exit("\n".join(bad))
    (SKILL / "SKILL.md").write_text("\n".join(sk))
    n = len("\n".join(sk).split("\n"))
    if n > SKILL_BUDGET:
        sys.exit(f"SKILL.md is {n} lines, budget {SKILL_BUDGET}")
    # llms.txt = SKILL.md body (same routing, verdict, scope, stable cards), opened by the SKILL description as the summary, with a
    # "when to use" paragraph, a Severity section and a described link to each level's Markdown file added.
    # Drafts live in llms-drafts.txt, never mixed into the vetted file.
    url = lambda fm: f"{BASE}/pack-{fm['lang']}.html" if fm["lang"] != "core" else f"{BASE}/{fm['level']}.html"
    body = list(sk[5:])
    k = next(i for i, l in enumerate(body) if l.startswith("The full text"))
    del body[k:body.index("", k) + 1]  # the shared pointer lines; llms.txt has its own Glossary and Draft sections
    llms = [body[0], "", "> " + sk[2][len("description: "):], "", "## When to use this site", "", WHEN_TO_USE, ""]
    seen_level = False
    for l in body[2:]:
        if l.startswith("## ") and l[3:] in LEVELS:
            if not seen_level:
                llms += SEVERITY
                seen_level = True
            llms += [l, "", f"- [{NAME[l[3:]]}, full text]({BASE}/{l[3:]}.md): every stable {l[3:]} card with its FAIL and PASS examples."]
        else:
            llms.append(l)
    llms += ["## Glossary", "", f"- [Glossary]({BASE}/glossary.md): terms the cards link to.", "",
             "## Draft cards", "", f"- [Draft cards]({BASE}/llms-drafts.txt): not vetted. {DRAFT_RULE}", "",
             "## Site", "",
             f"- [About]({BASE}/about.html): who makes this and under which licence.",
             f"- [Privacy]({BASE}/privacy.html): the site collects nothing.",
             f"- [Sitemap]({BASE}/sitemap.xml): every page.",
             f"- [cards.json]({BASE}/cards.json): every stable card as JSON; the shape is in [cards.schema.json]({BASE}/cards.schema.json).",
             f"- [Agent Skills index]({BASE}/.well-known/agent-skills/index.json): the skill, with a sha256 digest.",
             f"- [AGENTS.md]({REPO}/blob/main/AGENTS.md): how to review code with this repo and how to contribute a card.",
             f"- [Skill folder]({REPO}/tree/main/skills/good-code-review): `SKILL.md` and `references/` in the repository.",
             f"- [Contact]({REPO}/issues): GitHub Issues.", ""]
    dr = ["# Draft cards", "", f"Not vetted. {DRAFT_RULE} Use them as notes only, never as `PASS` or `FAIL`.", ""]
    for lv in LEVELS:
        cs = [c for c in draft if c[1]["level"] == lv and c[1]["lang"] == "core"]
        if cs:
            dr += [f"## {lv}", "", f"Full text: {url(cs[0][1])}", ""] + [line(fm, b) for _, fm, b in cs] + [""]
    for pk in packs:
        cs = [c for c in draft if c[1]["lang"] == pk]
        dr += [f"## pack {pk}", "", f"Full text: {url(cs[0][1])}", ""] + [line(fm, b) for _, fm, b in cs] + [""]
    text, dtext = "\n".join(llms), "\n".join(dr)
    idre = lambda t: re.findall(r"^- `([^`]+)` \[", t, re.M)
    if idre(text) != idre("\n".join(sk)) or {fm["id"] for _, fm, _ in draft} & set(idre(text)):
        sys.exit("llms.txt: stable ids differ from SKILL.md, or a draft id sits in it")
    if sorted(idre(dtext)) != sorted(fm["id"] for _, fm, _ in draft):
        sys.exit("llms-drafts.txt: ids differ from the draft cards")
    (SITE / "llms.txt").write_text(text)
    (SITE / "llms-drafts.txt").write_text(dtext)

    # Markdown twins of the pages that have no level file, for agents that prefer Markdown (checklist items 22 and 23).
    xlink = lambda t: re.sub(r"\[\[([^\]]+)\]\]", lambda m: f"[{m[1]}]({BASE}/{home[m[1]]}.md#{m[1]})" if m[1] in home
                             else f"[{m[1]}]({BASE}/{ids[m[1]]})" if m[1] in ids else m[1], t)
    twins["index"] = ("Good Code Review", SITE_DESC, INDEX_MD.format(
        verdict=plain, example=EXAMPLE, npx=npx, plugin=plugin,
        levels="\n".join(f"- [{NAME[lv]}]({BASE}/{lv}.md): {LEVEL_DESC[lv]} Input: {INPUT[lv]}. {cnt[lv][0]} stable, {cnt[lv][1]} draft." for lv in LEVELS if lv not in none)
        + "".join(f"\n- {NAME[lv]}: {LEVEL_DESC[lv]} Input: {INPUT[lv]}. {EMPTY_MARK.capitalize()}." for lv in LEVELS if lv in none),
        packs="\n".join(f"- [{pk.capitalize()} pack]({BASE}/pack-{pk}.md)" for pk in packs) or "No packs yet."))
    by_concern = "\n\n".join(f"## {c}\n\n" + "\n".join(f"- [`{fm['id']}`]({BASE}/{fm['level']}.md#{fm['id']}) [{fm['severity']}]: {rule(b)}"
                                                       for _, fm, b in stable if c in fm["tags"]) for c in CONCERNS if any(c in fm["tags"] for _, fm, _ in stable))
    twins["concerns"] = ("Concerns", CONCERNS_DESC, f"# Concerns\n\nStable cards grouped by concern. A card appears under each concern it lists. {plain}\n\n{by_concern}\n\n"
                         f"Draft cards are not vetted and are not listed here. See {BASE}/llms-drafts.txt.\n")
    for pk in packs:
        twins[f"pack-{pk}"] = (f"{pk.capitalize()} pack", PACK_DESC.format(pk=pk), xlink(
            f"# {pk.capitalize()} pack\n\n{DRAFT_NOTE} {DRAFT_RULE}\n\n" + "\n\n".join(section(fm, b) for _, fm, b in cards if fm["lang"] == pk) + "\n"))
    twins["glossary"] = ("Glossary", GLOSSARY_DESC, "# Glossary\n\n" + "\n\n".join(xlink(re.sub(r"^# ", "## ", p.read_text(), count=1).strip()) for p in gloss) + "\n")
    twins["about"] = ("About", ABOUT_DESC, "# About\n\n" + ABOUT)
    twins["privacy"] = ("Privacy", PRIVACY_DESC, "# Privacy\n\n" + PRIVACY)
    for slug, (title, desc, md_text) in twins.items():
        (SITE / f"{slug}.md").write_text(front(title, desc, slug, date) + md_text)

    # 404: plain text a missing-page visitor or agent can act on. Root-relative links, because the host serves this file at any missing path.
    nf = ("<p>No page exists at this address, and the server answered with status 404. The link may be old or mistyped.</p>"
          "<p>These pages exist:</p><ul>" + "".join(f'<li><a href="{h}">{html.escape(t)}</a>: {d}</li>' for h, t, d in [
              ("index.html", "Home", "choose a review level."), ("llms.txt", "llms.txt", "the entry point for agents: routing, verdict format, and every stable card."),
              ("sitemap.xml", "Sitemap", "every page.")] + [(f"{lv}.html", NAME[lv], LEVEL_DESC[lv]) for lv in LEVELS]) + "</ul>")
    (SITE / "404.html").write_text(re.sub(r'href="(?![a-z]+:|#|/)', 'href="/', page("Not found", nf, links=links)))

    slugs = ["index", "concerns", *LEVELS, *[f"pack-{pk}" for pk in packs], "glossary", "about", "privacy"]
    (SITE / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + "".join(f"<url><loc>{page_url(s)}</loc><lastmod>{date}</lastmod></url>\n" for s in slugs) + "</urlset>\n")
    shutil.copy(ROOT / "tools" / "og.png", SITE / "og.png")
    # cards.json is the one machine-readable source for the CLI and any other tool. Both files must match cards.schema.json.
    sch = schema.json_schema(BASE)
    (SITE / "cards.schema.json").write_text(json.dumps(sch, indent=2) + "\n")
    for name, kind, cs in (("cards.json", "stable", stable), ("cards-drafts.json", "drafts", draft)):
        data = schema.to_dict(corpus(kind, cs, cnt, date))
        if problems := schema.check(sch, data):
            sys.exit(f"{name} does not match cards.schema.json:\n" + "\n".join(problems[:10]))
        (SITE / name).write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    (SITE / "_headers").write_text(headers_file(slugs))

    # Agent Skills discovery: serve the skill and its references, and list it with the sha256 digest of the served SKILL.md.
    wk = SITE / ".well-known" / "agent-skills"
    shutil.copytree(SKILL, wk / "good-code-review")
    digest = hashlib.sha256((wk / "good-code-review" / "SKILL.md").read_bytes()).hexdigest()
    (wk / "index.json").write_text(json.dumps({
        "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
        "skills": [{"name": "good-code-review", "type": "skill-md", "description": sk[2][len("description: "):],
                    "url": f"{BASE}/.well-known/agent-skills/good-code-review/SKILL.md", "digest": f"sha256:{digest}"}]}, indent=2) + "\n")
    print(f"site: {len(slugs) + 1} pages; SKILL.md: {n} lines; stable cards: {len(stable)}; llms.txt: {len(text)} chars; lastmod: {date}")


if __name__ == "__main__":
    main()
