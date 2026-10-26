#!/usr/bin/env python3
"""Lint every card under cards/** and packs/**. Usage: validate.py [--root PATH]"""
import re
import sys
from pathlib import Path

import orgs

KEYS = ["id", "level", "tags", "severity", "status", "lang", "applies_when", "tool_gate", "borrowed_from"]
LEVELS = ["change", "function", "module", "service", "system", "codebase", "production", "incident"]
LEVEL_PREFIX = dict(zip(LEVELS, ["chg", "fn", "mod", "svc", "sys", "code", "prod", "inc"]))
PACK_PREFIX = {"python": "py"}  # other packs: prefix = lang name
SEVERITIES = ["block", "should-fix", "discuss"]
STATUSES = ["draft", "stable"]
# Closed list. Every card's tags include one or more of these, so a review can be scoped to one concern.
CONCERNS = ["correctness", "security", "performance", "reliability", "compatibility",
            "testing", "maintainability", "accessibility", "usability", "observability", "process"]
# Closed list. Every draft names its main blocker as the first word of `lacks:`. docs/PROMOTION.md defines each one.
LACKS = ["orgs", "evidence", "failable", "duplicate", "contradiction", "held", "unreviewed"]
BODY_MARKS = ["**Rule.**", "**Why.**", "**FAIL**", "**PASS**", "**Counterpoint.**"]


def strip_comment(s):
    return re.sub(r"\s+#.*$", "", s).strip()


def parse_front(text):
    """Return (dict, body) or (None, text). YAML subset: scalars, [a, b], block lists."""
    m = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    if not m:
        return None, text
    fm, key = {}, None
    for line in m.group(1).split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.match(r"\s+-\s+(.*)", line)
        if item and key and isinstance(fm.get(key), list):
            fm[key].append(strip_comment(item.group(1)))
            continue
        kv = re.match(r"([A-Za-z_]+):\s*(.*)", line)
        if not kv:
            continue
        key, val = kv.group(1), strip_comment(kv.group(2))
        if val.startswith("["):
            fm[key] = [x.strip() for x in val.strip("[]").split(",") if x.strip()]
        elif val == "":
            fm[key] = []  # block list follows
        else:
            fm[key] = val
    return fm, m.group(2)


def load_cards(root):
    cards = []
    files = sorted(list((root / "cards").rglob("*.md")) + list((root / "packs").rglob("*.md")))
    for p in files:
        if p.name == "_template.md":
            continue
        fm, body = parse_front(p.read_text())
        cards.append((p, fm, body))
    return cards


def validate(root):
    errors = []
    cards = load_cards(root)
    research = "\n".join(p.read_text() for p in (root / "docs" / "research").glob("*.md"))
    glossary = {p.stem for p in (root / "glossary").glob("*.md")}
    ids = {}
    for p, fm, _ in cards:
        if fm and "id" in fm:
            ids.setdefault(fm["id"], []).append(p)
    drafts = {fm["id"] for _, fm, _ in cards if fm and fm.get("status") == "draft" and "id" in fm}
    for p, fm, body in cards:
        rel = p.relative_to(root)

        def err(msg):
            errors.append(f"{rel}: {msg}")

        if fm is None:
            err("no front matter")
            continue
        for k in KEYS:
            if k not in fm:
                err(f"missing key '{k}'")
        cid, level, lang = fm.get("id", ""), fm.get("level"), fm.get("lang")
        if level is not None and level not in LEVELS:
            err(f"bad level '{level}'")
        if fm.get("severity") is not None and fm["severity"] not in SEVERITIES:
            err(f"bad severity '{fm['severity']}'")
        if fm.get("status") is not None and fm["status"] not in STATUSES:
            err(f"bad status '{fm['status']}'")
        tags = fm.get("tags", [])
        if not any(t in CONCERNS for t in tags):
            err(f"tags need at least one concern: {', '.join(CONCERNS)}")
        if cid and not re.fullmatch(r"[a-z0-9-]+", cid):
            err(f"id '{cid}' must match [a-z0-9-]+")
        if len(ids.get(cid, [])) > 1:
            err(f"duplicate id '{cid}'")
        if lang == "core" and level in LEVEL_PREFIX and not cid.startswith(LEVEL_PREFIX[level] + "-"):
            err(f"core id '{cid}' needs prefix '{LEVEL_PREFIX[level]}-' for level {level}")
        elif lang and lang != "core":
            if p.parent != root / "packs" / lang:
                err(f"lang '{lang}' card must live in packs/{lang}/")
            pre = PACK_PREFIX.get(lang, lang)
            if not cid.startswith(pre + "-"):
                err(f"id '{cid}' needs prefix '{pre}-' for pack {lang}")
        urls = fm.get("borrowed_from", [])
        if not isinstance(urls, list):
            err("borrowed_from must be a list")
            urls = []
        for u in urls:
            if u not in research:
                err(f"borrowed_from URL not in docs/research: {u}")
            if orgs.org_of(u) is None:
                err(f"borrowed_from URL has no organisation in tools/orgs.py: {u}")
        # A floor for rule 1 of docs/PROMOTION.md: it counts per Rule clause, so three orgs per card is necessary, not sufficient.
        found = {orgs.org_of(u) for u in urls} - {None}
        if fm.get("status") == "stable" and len(found) < 3:
            err(f"stable card has {len(found)} organisation(s) in borrowed_from; it needs at least 3")
        lacks = fm.get("lacks")
        if fm.get("status") == "stable" and lacks is not None:
            err("stable card has 'lacks:'; remove it on promotion")
        if fm.get("status") == "draft":
            m = re.fullmatch(r"([a-z]+), ((?!.*\[\[).{1,160})", lacks) if isinstance(lacks, str) else None
            if not m or m.group(1) not in LACKS:
                err(f"draft needs 'lacks: <word>, <note of at most 160 characters>' with a word from: {', '.join(LACKS)}")
        if fm.get("status") == "stable" and not urls:
            err("stable card needs >=1 borrowed_from URL")
        for mark in BODY_MARKS:
            if mark not in body:
                err(f"body missing {mark}")
        for ref in sorted(set(re.findall(r"\[\[([^\]]+)\]\]", body))):
            if ref not in ids and ref not in glossary:
                err(f"unresolved cross-ref [[{ref}]]")
        if fm.get("status") == "stable":
            text = p.read_text()
            for d in sorted(drafts):
                if re.search(rf"(?<![a-z0-9-]){re.escape(d)}(?![a-z0-9-])", text):
                    err(f"stable card names draft id '{d}'")
    for g in sorted((root / "glossary").glob("*.md")):
        text = g.read_text()
        for d in sorted(drafts):
            if re.search(rf"(?<![a-z0-9-]){re.escape(d)}(?![a-z0-9-])", text):
                errors.append(f"{g.relative_to(root)}: glossary entry names draft id '{d}'")
    return errors


if __name__ == "__main__":
    root = Path(sys.argv[sys.argv.index("--root") + 1] if "--root" in sys.argv else ".").resolve()
    errs = validate(root)
    print("\n".join(errs))
    sys.exit(1 if errs else 0)
