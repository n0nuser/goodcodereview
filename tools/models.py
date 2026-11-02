"""The closed lists of the card format, and the records the build passes around."""
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any


class Level(StrEnum):
    CHANGE = "change"
    FUNCTION = "function"
    MODULE = "module"
    SERVICE = "service"
    SYSTEM = "system"
    CODEBASE = "codebase"
    PRODUCTION = "production"
    INCIDENT = "incident"


class Severity(StrEnum):
    BLOCK = "block"
    SHOULD_FIX = "should-fix"
    DISCUSS = "discuss"


class Status(StrEnum):
    STABLE = "stable"
    DRAFT = "draft"


class Context(StrEnum):
    """A part of an input. A card without `context` applies to any input."""

    UI = "ui"
    SERVER = "server"
    DATA = "data"
    CLI = "cli"


class Concern(StrEnum):
    """Every card's tags include one or more of these, so a review can be scoped to one concern."""

    CORRECTNESS = "correctness"
    SECURITY = "security"
    PERFORMANCE = "performance"
    RELIABILITY = "reliability"
    COMPATIBILITY = "compatibility"
    TESTING = "testing"
    MAINTAINABILITY = "maintainability"
    ACCESSIBILITY = "accessibility"
    USABILITY = "usability"
    OBSERVABILITY = "observability"
    PROCESS = "process"


class LacksReason(StrEnum):
    """Every draft names its main blocker as the first word of `lacks:`. docs/PROMOTION.md defines each one."""

    ORGS = "orgs"
    EVIDENCE = "evidence"
    FAILABLE = "failable"
    DUPLICATE = "duplicate"
    CONTRADICTION = "contradiction"
    HELD = "held"
    UNREVIEWED = "unreviewed"


CONTEXTS = tuple(Context)
LEVELS = tuple(Level)
AUDIT_LEVELS = LEVELS[1:]  # every level except `change`
CONCERNS = tuple(Concern)
CORE = "core"  # the `lang` of a card that belongs to no language pack


@dataclass(frozen=True, slots=True)
class ParsedFront:
    """A card file split into front matter and body. `fm` is None when the file has no front matter."""

    fm: dict[str, Any] | None
    body: str


@dataclass(frozen=True, slots=True)
class RawCard:
    """A card file as read: `fm` is None when the file has no front matter."""

    path: Path
    fm: dict[str, Any] | None
    body: str


@dataclass(frozen=True, slots=True)
class Card:
    """A card with front matter. `fm` holds the parsed front matter keys."""

    path: Path
    fm: dict[str, Any]
    body: str


@dataclass(frozen=True, slots=True)
class DraftLack:
    """A draft's `lacks:` line split into its reason word and its note."""

    reason: str
    note: str


@dataclass(frozen=True, slots=True)
class Route:
    """One row of the routing table: the input a reviewer has and the level that handles it."""

    input: str
    level: Level


@dataclass(frozen=True, slots=True)
class NavLink:
    href: str
    label: str


@dataclass(frozen=True, slots=True)
class PageSpec:
    """A listing page: its file, title, intro HTML, the cards it lists, and its description."""

    file: str
    title: str
    intro: str
    cards: tuple[Card, ...]
    desc: str


@dataclass(frozen=True, slots=True)
class Twin:
    """A Markdown twin of a page: it is written to site/<slug>.md with frontmatter."""

    title: str
    description: str
    markdown: str


@dataclass(frozen=True, slots=True)
class IndexPart:
    """One level index file, or one context slice of it."""

    slug: str
    title: str
    text: str
    count: int


@dataclass(frozen=True, slots=True)
class LevelCount:
    stable: int
    draft: int
