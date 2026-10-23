#!/usr/bin/env python3
"""Validate, then emit site/ and skills/good-code-review/. Run from anywhere."""
import html
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import LEVELS, load_cards, validate  # noqa: E402

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
CSS = """:root{--bg:#fff;--fg:#1a1a1a;--mut:#666;--line:#ddd;--acc:#0b5fff}
@media(prefers-color-scheme:dark){:root{--bg:#121212;--fg:#e8e8e8;--mut:#9a9a9a;--line:#333;--acc:#6ea0ff}}
body{margin:0 auto;max-width:48rem;padding:1rem;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif}
a{color:var(--acc)}nav a{margin-right:.8rem}pre{overflow-x:auto;background:var(--line);padding:.6rem;border-radius:4px}
code{font-family:ui-monospace,monospace;font-size:.9em}article{border-top:1px solid var(--line);padding:.5rem 0}
.b{display:inline-block;font-size:.75rem;padding:0 .5rem;border:1px solid var(--mut);border-radius:1rem;margin-right:.3rem}
.block{border-color:#d33;color:#d33}.should-fix{border-color:#c80;color:#c80}.stable{border-color:#2a2;color:#2a2}
.tag{cursor:pointer;color:var(--acc);margin-right:.5rem}.tag.on{font-weight:bold}
.doors a{display:block;border:1px solid var(--line);padding:1rem;margin:.6rem 0;border-radius:6px}footer{color:var(--mut);margin-top:2rem}"""
JS = """const on=new Set();document.querySelectorAll('.tag').forEach(t=>t.onclick=()=>{
t.classList.toggle('on');on.has(t.dataset.t)?on.delete(t.dataset.t):on.add(t.dataset.t);
document.querySelectorAll('article[data-tags]').forEach(a=>{const g=a.dataset.tags.split(' ');
a.hidden=[...on].some(x=>!g.includes(x))})})"""


def inline(s, ids):
    s = html.escape(s)
    codes = []
    s = re.sub(r"`([^`]+)`", lambda m: codes.append(m.group(1)) or f"\0{len(codes) - 1}\0", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\[\[([^\]]+)\]\]", lambda m: f'<a href="{ids.get(m.group(1), "#")}">{m.group(1)}</a>', s)
    return re.sub(r"\0(\d+)\0", lambda m: f"<code>{codes[int(m.group(1))]}</code>", s)


def md(text, ids):
    out = []
    for i, part in enumerate(re.split(r"^```.*\n(.*?)^```\s*$", text, flags=re.S | re.M)):
        if i % 2:
            out.append(f"<pre><code>{html.escape(part)}</code></pre>")
            continue
        for blk in re.split(r"\n\s*\n", part.strip()):
            lines = blk.split("\n")
            if not blk.strip():
                continue
            if all(re.match(r"\s*[-*] ", l) for l in lines):
                out.append("<ul>" + "".join(f"<li>{inline(re.sub(r'^\s*[-*] ', '', l), ids)}</li>" for l in lines) + "</ul>")
            elif m := re.match(r"(#+) (.*)", blk):
                out.append(f"<h{len(m[1]) + 1}>{inline(m[2], ids)}</h{len(m[1]) + 1}>")
            else:
                out.append(f"<p>{inline(' '.join(lines), ids)}</p>")
    return "\n".join(out)


def page(title, body, script=False):
    nav = '<nav><a href="index.html">Home</a><a href="change.html">Change</a><a href="glossary.html">Glossary</a></nav>'
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>{nav}<h1>{html.escape(title)}</h1>{body}"
            f"<footer>created and edited by Pablo</footer>{'<script>' + JS + '</script>' if script else ''}</body></html>")


def card_html(fm, body, ids):
    b = f'<span class="b {fm["severity"]}">{fm["severity"]}</span><span class="b {fm["status"]}">{fm["status"]}</span>'
    tags = " ".join(fm["tags"])
    return (f'<article id="{fm["id"]}" data-tags="{html.escape(tags)}"><h3>{fm["id"]}</h3>{b}'
            f'<p><em>{inline(fm["applies_when"], ids)}</em></p>{md(body, ids)}</article>')


def listing(title, intro, cards, ids):
    tags = sorted({t for _, fm, _ in cards for t in fm["tags"]})
    bar = "<p>" + "".join(f'<span class="tag" data-t="{html.escape(t)}">#{html.escape(t)}</span>' for t in tags) + "</p>"
    return page(title, intro + bar + "".join(card_html(fm, b, ids) for _, fm, b in cards) or "<p>No cards yet.</p>", True)


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
    ids = {fm["id"]: (f"pack-{fm['lang']}.html" if fm["lang"] != "core" else f"{fm['level']}.html") + f"#{fm['id']}"
           for _, fm, _ in cards}
    ids.update({g.stem: f"glossary.html#{g.stem}" for g in gloss})

    shutil.rmtree(SITE, ignore_errors=True)
    SITE.mkdir()
    llms = ["# Good Code Review", ""]
    pages = []  # (file, title, cards)
    for lv in LEVELS:
        pages.append((f"{lv}.html", f"Level: {lv}", [c for c in cards if c[1]["level"] == lv and c[1]["lang"] == "core"]))
    for pk in packs:
        pages.append((f"pack-{pk}.html", f"Pack: {pk}", [c for c in cards if c[1]["lang"] == pk]))
    for f, title, cs in pages:
        (SITE / f).write_text(listing(title, "", cs, ids))
        llms += [f"## {title} ({f})"] + [f"- {fm['id']}: {rule(b)}" for _, fm, b in cs] + [""]
    g = "".join(f'<article id="{p.stem}">{md(p.read_text(), ids)}</article>' for p in gloss)
    (SITE / "glossary.html").write_text(page("Glossary", g))
    llms += [f"## Glossary (glossary.html)"] + [f"- {p.stem}" for p in gloss]
    (SITE / "llms.txt").write_text("\n".join(llms) + "\n")
    links = lambda ls: "".join(f'<a href="{l}.html">{l}</a>' for l in ls)
    (SITE / "index.html").write_text(page("Good Code Review", (
        "<p>What to check when reviewing code. Every check ends in PASS, FAIL or N/A with file:line evidence.</p>"
        f'<div class="doors"><div><a href="change.html"><strong>Review a change</strong><br>A diff or PR.</a></div>'
        f'<div><strong>Audit what exists</strong>{links(AUDIT)}</div></div>'
        f"<p>Packs: {links('pack-' + p for p in packs) or 'none'}</p>")))

    stable = [c for c in cards if c[1]["status"] == "stable"]
    (SKILL / "references").mkdir(parents=True, exist_ok=True)
    for f in (SKILL / "references").glob("*.md"):
        f.unlink()
    sk = ["---", "name: good-code-review",
          "description: Review code against stable cards, from a diff up to an incident. Use when asked to review, audit or check code.",
          "---", "", "# Good Code Review", "", "## Routing", "", "| Input | Entry point |", "|---|---|"]
    sk += [f"| {i} | {lv} |" for i, lv in ROUTES]
    sk += ["", "## Verdict format", "", "Per check: `PASS`, `FAIL` or `N/A`, with `file:line` evidence.",
           "A `FAIL` carries the card severity: block, should-fix or discuss.", "",
           "Full text per level: `references/<level>.md`.", ""]
    for lv in LEVELS:
        cs = [c for c in stable if c[1]["level"] == lv]
        if not cs:
            continue
        sk += [f"## {lv}", ""] + [f"- `{fm['id']}` [{fm['severity']}]: {rule(b)}" for _, fm, b in cs] + [""]
        (SKILL / "references" / f"{lv}.md").write_text(
            f"# {lv}\n\n" + "\n\n".join(f"## {fm['id']}\n\nseverity: {fm['severity']}  \napplies_when: {fm['applies_when']}\n\n{b.strip()}"
                                        for _, fm, b in cs) + "\n")
    (SKILL / "SKILL.md").write_text("\n".join(sk))
    if len(sk) > SKILL_BUDGET:
        sys.exit(f"SKILL.md is {len(sk)} lines, budget {SKILL_BUDGET}")
    print(f"site: {len(pages) + 2} pages; SKILL.md: {len(sk)} lines; stable cards: {len(stable)}")


if __name__ == "__main__":
    main()
