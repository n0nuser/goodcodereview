"""Readers for the front matter of a card, shared by the HTML, Markdown, and JSON writers."""
import orgs
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


def backers(card: Card) -> str:
    """The organisation and people lines for the Markdown and text outputs. A draft says "Cites", a stable card "Backed by"."""
    found = orgs.split(card.fm["borrowed_from"])
    organisations, people = found.organisations, found.people

    def names(group: list[orgs.OrgUrls]) -> str:
        return ", ".join(orgs.ORGS[g.id] for g in group)

    head = "Backed by" if is_stable(card) else "Cites"
    return f"{head}: {names(organisations) or 'no organisation yet'}." + (f" People cited: {names(people)}." if people else "")


def markdown_url(card: Card) -> str:
    return f"{BASE}/{page_name(card)}.md"
