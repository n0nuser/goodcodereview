#!/usr/bin/env python3
"""Lint every card under cards/** and packs/**. Usage: validate.py [--root PATH]."""
import re
import sys
from pathlib import Path
from typing import Any

import orgs
from config import ROOT
from errors import ToolError
from models import (
    CONCERNS,
    CORE,
    LEVELS,
    Card,
    Context,
    LacksReason,
    ParsedFront,
    RawCard,
    Severity,
    Status,
)

KEYS = ["id", "level", "tags", "severity", "status", "lang", "applies_when", "tool_gate", "borrowed_from"]
LEVEL_PREFIX = dict(zip(LEVELS, ["chg", "fn", "mod", "svc", "sys", "code", "prod", "inc"], strict=True))
PACK_PREFIX = {"python": "py"}  # other packs: prefix = lang name
BODY_MARKS = ["**Rule.**", "**Why.**", "**FAIL**", "**PASS**", "**Counterpoint.**"]
LACKS_NOTE_MAX = 160  # characters in the note after the reason word of `lacks:`
STABLE_ORG_FLOOR = 3  # independent organisations a stable card needs in borrowed_from


def strip_comment(s: str) -> str:
    """Drop a trailing ` # comment` and surrounding space."""
    return re.sub(r"\s+#.*$", "", s).strip()


def parse_front(text: str) -> ParsedFront:
    """Split a card file into front matter and body. YAML subset: scalars, [a, b], block lists."""
    m = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    if not m:
        return ParsedFront(None, text)
    fm: dict[str, Any] = {}
    key: str | None = None
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
    return ParsedFront(fm, m.group(2))


def load_raw_cards(root: Path) -> list[RawCard]:
    """Every card file under cards/ and packs/, in path order. A file may lack front matter."""
    files = sorted(list((root / "cards").rglob("*.md")) + list((root / "packs").rglob("*.md")))
    cards = []
    for p in files:
        if p.name == "_template.md":
            continue
        parsed = parse_front(p.read_text())
        cards.append(RawCard(p, parsed.fm, parsed.body))
    return cards


def load_cards(root: Path) -> list[Card]:
    """Every card, for code that runs after validate() passed. Raises ToolError on a file without front matter."""
    cards = []
    for raw in load_raw_cards(root):
        if raw.fm is None:
            raise ToolError(f"{raw.path}: no front matter")
        cards.append(Card(raw.path, raw.fm, raw.body))
    return cards


def _check_card(card: RawCard, root: Path, ids: dict[str, list[Path]], research: str, glossary: set[str]) -> list[str]:
    """Return the errors of one card, each prefixed with its path."""
    fm = card.fm
    rel = card.path.relative_to(root)
    errors: list[str] = []

    def err(msg: str) -> None:
        errors.append(f"{rel}: {msg}")

    if fm is None:
        err("no front matter")
        return errors
    for k in KEYS:
        if k not in fm:
            err(f"missing key '{k}'")
    cid, level, lang = fm.get("id", ""), fm.get("level"), fm.get("lang")
    if level is not None and level not in LEVELS:
        err(f"bad level '{level}'")
    if fm.get("severity") is not None and fm["severity"] not in set(Severity):
        err(f"bad severity '{fm['severity']}'")
    if fm.get("status") is not None and fm["status"] not in set(Status):
        err(f"bad status '{fm['status']}'")
    for c in fm.get("context", []):
        if c not in set(Context):
            err(f"bad context '{c}'; use: {', '.join(Context)}")
    tags = fm.get("tags", [])
    if not any(t in CONCERNS for t in tags):
        err(f"tags need at least one concern: {', '.join(CONCERNS)}")
    if cid and not re.fullmatch(r"[a-z0-9-]+", cid):
        err(f"id '{cid}' must match [a-z0-9-]+")
    if len(ids.get(cid, [])) > 1:
        err(f"duplicate id '{cid}'")
    if lang == CORE and level in LEVEL_PREFIX and not cid.startswith(LEVEL_PREFIX[level] + "-"):
        err(f"core id '{cid}' needs prefix '{LEVEL_PREFIX[level]}-' for level {level}")
    elif lang and lang != CORE:
        if card.path.parent != root / "packs" / lang:
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
    found = {orgs.org_of(u) for u in urls} - {None} - orgs.PERSONS  # people are references, not organisations
    stable = fm.get("status") == Status.STABLE
    if stable and len(found) < STABLE_ORG_FLOOR and not {orgs.org_of(u) for u in urls} & orgs.CREATORS:
        err(f"stable card has {len(found)} organisation(s) in borrowed_from; it needs at least 3, or one source by the creator (docs/adr/0001)")
    lacks = fm.get("lacks")
    if stable and lacks is not None:
        err("stable card has 'lacks:'; remove it on promotion")
    if fm.get("status") == Status.DRAFT:
        m = re.fullmatch(rf"([a-z]+), ((?!.*\[\[).{{1,{LACKS_NOTE_MAX}}})", lacks) if isinstance(lacks, str) else None
        if not m or m.group(1) not in set(LacksReason):
            err(f"draft needs 'lacks: <word>, <note of at most {LACKS_NOTE_MAX} characters>' with a word from: {', '.join(LacksReason)}")
        if fm.get("severity") == Severity.BLOCK:
            err("a draft card is capped at should-fix; set the card's own severity when you promote it")
    if stable and not urls:
        err("stable card needs >=1 borrowed_from URL")
    for mark in BODY_MARKS:
        if mark not in card.body:
            err(f"body missing {mark}")
    for ref in sorted(set(re.findall(r"\[\[([^\]]+)\]\]", card.body))):
        if ref not in ids and ref not in glossary:
            err(f"unresolved cross-ref [[{ref}]]")
    return errors


def validate(root: Path) -> list[str]:
    """Return one message per problem in the cards and glossary under `root`."""
    errors: list[str] = []
    cards = load_raw_cards(root)
    research = "\n".join(p.read_text() for p in (root / "docs" / "research").glob("*.md"))
    glossary = {p.stem for p in (root / "glossary").glob("*.md")}
    ids: dict[str, list[Path]] = {}
    for c in cards:
        if c.fm and "id" in c.fm:
            ids.setdefault(c.fm["id"], []).append(c.path)
    drafts = {c.fm["id"] for c in cards if c.fm and c.fm.get("status") == Status.DRAFT and "id" in c.fm}
    # One alternation matches every draft id in a text, so each stable card costs one scan.
    draft_re = re.compile(r"(?<![a-z0-9-])(" + "|".join(map(re.escape, sorted(drafts, key=len, reverse=True))) + r")(?![a-z0-9-])") if drafts else None

    def names_in(text: str) -> list[str]:
        return sorted(set(draft_re.findall(text))) if draft_re else []

    for card in cards:
        errors += _check_card(card, root, ids, research, glossary)
        if card.fm and card.fm.get("status") == Status.STABLE:
            errors += [f"{card.path.relative_to(root)}: stable card names draft id '{d}'" for d in names_in(card.path.read_text())]
    for g in sorted((root / "glossary").glob("*.md")):
        errors += [f"{g.relative_to(root)}: glossary entry names draft id '{d}'" for d in names_in(g.read_text())]
    return errors


def main(argv: list[str]) -> int:
    """Lint the cards under --root (default: the repository) and print the problems. Return the exit code."""
    root = Path(argv[argv.index("--root") + 1]).resolve() if "--root" in argv else ROOT
    errs = validate(root)
    print("\n".join(errs))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
