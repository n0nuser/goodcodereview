"""How strongly each source backs its card's Rule, read from docs/research/source-strength.tsv.

The file has one row per (card, URL): `supports`, `partial`, `weak` or `off`, as judged against the card's Rule. A URL with no row is
`unjudged`. The count of organisations in borrowed_from says who backs a card; this says how well.
"""
import csv
from functools import cache

from config import ROOT
from schema import Backing, Strength

STRENGTH_FILE = ROOT / "docs" / "research" / "source-strength.tsv"
RANK = {Strength.SUPPORTS: 4, Strength.PARTIAL: 3, Strength.WEAK: 2, Strength.OFF: 1, Strength.UNJUDGED: 0}
STRONG_ORGS = 3  # supporting organisations that make a card "strong": the same floor as a stable card


@cache
def _rows() -> dict[tuple[str, str], Strength]:
    if not STRENGTH_FILE.is_file():
        return {}
    with STRENGTH_FILE.open(newline="") as f:
        return {(r["card"], r["url"]): Strength(r["verdict"]) for r in csv.DictReader(f, delimiter="\t")}


def of_url(card_id: str, url: str) -> Strength:
    return _rows().get((card_id, url), Strength.UNJUDGED)


def of_org(card_id: str, urls: list[str]) -> Strength:
    """An organisation is as strong as its best source for this card."""
    return max((of_url(card_id, u) for u in urls), key=RANK.__getitem__, default=Strength.UNJUDGED)


def backing(card_id: str, org_urls: list[list[str]]) -> Backing:
    """`strong` when at least three organisations support the Rule, `unjudged` when no source was judged, else `mixed`."""
    levels = [of_org(card_id, urls) for urls in org_urls]
    if sum(s is Strength.SUPPORTS for s in levels) >= STRONG_ORGS:
        return Backing.STRONG
    if all(s is Strength.UNJUDGED for s in levels):
        return Backing.UNJUDGED
    return Backing.MIXED
