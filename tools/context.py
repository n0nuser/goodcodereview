"""Everything the writers share, derived once from the cards: the build input."""
from __future__ import annotations

import datetime
import subprocess
from dataclasses import dataclass, field, replace
from pathlib import Path

from card_fields import context_group, href, is_core, is_stable, level_of, page_name
from config import ROOT
from errors import BuildError
from markdown import check_md
from models import LEVELS, Card, Level, LevelCount, NavLink
from prose import ABOUT, AUDIT_MD, EMPTY_MARK, FAQ, NAME, PRIVACY
from validate import load_cards, validate


def pack_name(pk: str) -> str:
    """A pack's display name."""
    return {"typescript": "TypeScript"}.get(pk, pk.capitalize())


def build_date() -> str:
    """One date for every lastmod and `updated`: the HEAD commit date in UTC, or today's date outside a git checkout.

    UTC keeps a commit made just after local midnight from dating the site a day ahead of a CI runner, which checks lastmod against its own UTC today.
    """
    try:
        stamp = subprocess.run(["git", "log", "-1", "--format=%ct"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        return datetime.datetime.fromtimestamp(int(stamp), datetime.UTC).date().isoformat()
    except (OSError, subprocess.CalledProcessError, ValueError):
        return datetime.date.today().isoformat()


@dataclass(frozen=True, slots=True)
class BuildInput:
    """The cards, glossary, and derived tables the writers read. Built by `read_input`."""

    cards: tuple[Card, ...]
    packs: tuple[str, ...]
    glossary: tuple[Path, ...]
    date: str
    ids: dict[str, str]  # card id or glossary term -> site-relative link
    counts: dict[Level, LevelCount]  # core cards only
    no_stable: frozenset[Level]  # levels whose core cards include no stable one
    links: tuple[NavLink, ...]
    split: frozenset[Level] = field(default_factory=frozenset)  # levels whose HTML page is one hub plus a page per `context`
    plan: dict[str, str] = field(default_factory=dict)  # card id -> part name, for a context part that was split again (docs/adr/0002)

    def part_of(self, card: Card) -> str:
        """The part of a split level that holds the card: its context, or the sub-part the planner gave it."""
        return self.plan.get(card.fm["id"], context_group(card))

    def page_of(self, card: Card) -> str:
        """The page slug that holds the card in full: its pack page, its level page, or its context part of a split level."""
        return f"{level_of(card)}-{self.part_of(card)}" if is_core(card) and level_of(card) in self.split else page_name(card)

    def parts(self, level: Level) -> dict[str, list[Card]]:
        """The parts of a split level, each with its cards (stable and draft), in card order."""
        groups: dict[str, list[Card]] = {}
        for c in self.core_at(level):
            groups.setdefault(self.part_of(c), []).append(c)
        return groups

    def hubs(self, level: Level) -> dict[str, list[Card]]:
        """Each context of a split level that was split again, with its cards. It keeps a hub page: a published URL must not disappear (docs/adr/0002)."""
        if level not in self.split:
            return {}
        cards = self.core_at(level)
        resplit = {context_group(c) for c in cards if c.fm["id"] in self.plan}
        return {g: [c for c in cards if context_group(c) == g] for g in dict.fromkeys(map(context_group, cards)) if g in resplit}

    def with_split(self, split: frozenset[Level], plan: dict[str, str] | None = None) -> BuildInput:
        """The same input with `split` levels set and every card link pointing at the page that holds the card."""
        moved = replace(self, split=split, plan=plan or {})
        return replace(moved, ids={**self.ids, **{c.fm["id"]: f"{moved.page_of(c)}.html#{c.fm['id']}" for c in self.cards}})

    @property
    def stable(self) -> list[Card]:
        return [c for c in self.cards if is_stable(c)]

    @property
    def draft(self) -> list[Card]:
        return [c for c in self.cards if not is_stable(c)]

    def core_at(self, level: Level) -> list[Card]:
        return [c for c in self.cards if level_of(c) == level and is_core(c)]

    @property
    def tally(self) -> str:
        """The headline count, printed from the build so it cannot drift from the cards."""
        core = sum(n.stable for n in self.counts.values())
        pack = len(self.stable) - core
        return f"{len(self.stable)} stable checks: {core} across the eight levels and {pack} in the language packs."


def source_errors(cards: list[Card], glossary: list[Path], root: Path) -> list[str]:
    """Markdown the renderer cannot draw, in the cards, the glossary, and the page texts."""
    errors = [e for c in cards for e in check_md(c.path.relative_to(root), c.body)]
    errors += [e for g in glossary for e in check_md(g.relative_to(root), g.read_text())]
    errors += [e for name, text in (("ABOUT", ABOUT), ("FAQ", FAQ), ("PRIVACY", PRIVACY), ("AUDIT", AUDIT_MD)) for e in check_md(name, text)]
    return errors


def read_input(root: Path, date: str) -> BuildInput:
    """Read the cards under `root`. Raises BuildError listing every problem in the cards or in Markdown the renderer cannot draw."""
    errors = validate(root)
    if errors:
        raise BuildError("\n".join(errors))
    cards = load_cards(root)
    glossary = sorted((root / "glossary").glob("*.md"))
    errors = source_errors(cards, glossary, root)
    if errors:
        raise BuildError("\n".join(errors))
    packs = tuple(sorted({c.fm["lang"] for c in cards if not is_core(c)}))
    ids = {c.fm["id"]: href(c) for c in cards}
    ids.update({g.stem: f"glossary.html#{g.stem}" for g in glossary})
    counts = {
        lv: LevelCount(
            stable=sum(level_of(c) == lv and is_core(c) and is_stable(c) for c in cards),
            draft=sum(level_of(c) == lv and is_core(c) and not is_stable(c) for c in cards),
        )
        for lv in LEVELS
    }
    no_stable = frozenset(lv for lv in LEVELS if not counts[lv].stable)
    links = (
        [NavLink("index.html", "Home"), NavLink("concerns.html", "Concerns")]
        + [NavLink(f"{lv}.html", NAME[lv] + (f" ({EMPTY_MARK})" if lv in no_stable else "")) for lv in LEVELS]
        + [NavLink(f"pack-{pk}.html", f"{pack_name(pk)} pack") for pk in packs]
        + [NavLink("glossary.html", "Glossary")]
    )
    return BuildInput(tuple(cards), packs, tuple(glossary), date, ids, counts, no_stable, tuple(links))
