"""Readers for the front matter of a card, shared by the HTML, Markdown, and JSON writers."""
from collections.abc import Iterable

import orgs
import strength
from config import BASE
from models import CONCERNS, CORE, Card, DraftLack, Level, Status


def concerns(card: Card) -> list[str]:
    """The card's tags that name a concern."""
    return [t for t in card.fm["tags"] if t in CONCERNS]


def topics(card: Card) -> list[str]:
    """The card's tags that are not concerns."""
    return [t for t in card.fm["tags"] if t not in CONCERNS]


def lacks(card: Card) -> DraftLack | None:
    """A draft's `lacks:` line as a reason and a note, or None on a stable card."""
    if "lacks" not in card.fm:
        return None
    reason, note = card.fm["lacks"].split(", ", 1)
    return DraftLack(reason, note)


def is_stable(card: Card) -> bool:
    return bool(card.fm["status"] == Status.STABLE)


def is_core(card: Card) -> bool:
    """True for a card that belongs to a level, not to a language pack."""
    return bool(card.fm["lang"] == CORE)


def level_of(card: Card) -> Level:
    return Level(card.fm["level"])


def page_name(card: Card) -> str:
    """The page that holds the card: its pack page, or its level page."""
    return f"pack-{card.fm['lang']}" if not is_core(card) else str(card.fm["level"])


def href(card: Card) -> str:
    """Site-relative link to the card on its page."""
    return f"{page_name(card)}.html#{card.fm['id']}"


def context(card: Card) -> list[str]:
    return list(card.fm.get("context", []))


def context_group(card: Card) -> str:
    """The context group a card is filed under: its first `context`, or "any"."""
    return (context(card) or ["any"])[0]


def group_by_context(cards: Iterable[Card]) -> dict[str, list[Card]]:
    """The cards by context group, in card order. The level index and the split level pages both use it."""
    groups: dict[str, list[Card]] = {}
    for c in cards:
        groups.setdefault(context_group(c), []).append(c)
    return groups


def backers(card: Card) -> str:
    """The organisation and people lines for the Markdown and text outputs. A draft says "Cites", a stable card "Backed by"."""
    found = orgs.split(card.fm["borrowed_from"])
    organisations, people = found.organisations, found.people

    cid = card.fm["id"]

    def names(group: list[orgs.OrgUrls]) -> str:
        return ", ".join(f"{orgs.ORGS[g.id]} ({strength.of_org(cid, g.urls)})" for g in group)

    head = "Backed by" if is_stable(card) else "Cites"
    return (f"{head}: {names(organisations) or 'no organisation yet'}." + (f" Backing: {strength.backing(cid, [g.urls for g in organisations])}." if organisations else "")
            + (f" People cited: {names(people)}." if people else ""))


def markdown_url(card: Card) -> str:
    return f"{BASE}/{page_name(card)}.md"
