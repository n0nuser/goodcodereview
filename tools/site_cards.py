"""The cards JSON files: cards.json and cards-drafts.json, one file per level, one per concern, and the slim cards-index.json."""
import json
from collections.abc import Sequence
from typing import Any

import orgs
import schema
import site_concerns
import strength
from card_fields import concerns, lacks, level_of, markdown_url, page_name, topics
from config import BASE, LICENCE_URL, SITE_NAME
from context import BuildInput
from errors import BuildError
from markdown import rule, section
from models import CONCERNS, LEVELS, Card, LacksReason
from prose import INPUT, LEVEL_DESC, NAME
from shell import page_url


def _card_model(card: Card) -> schema.Card:
    fm = card.fm
    found = orgs.split(fm["borrowed_from"])
    draft_lack = lacks(card)
    return schema.Card(
        id=fm["id"], level=fm["level"], status=fm["status"], severity=fm["severity"], concerns=concerns(card),
        topics=topics(card), lang=fm["lang"], applies_when=fm["applies_when"], context=fm.get("context", []),
        tool_gate=None if fm["tool_gate"] == "none" else fm["tool_gate"], note=fm.get("note"),
        lacks=schema.Lacks(LacksReason(draft_lack.reason), draft_lack.note) if draft_lack else None,
        rule=rule(card.body), why=section(card.body, "Why"), counterpoint=section(card.body, "Counterpoint"),
        fail=schema.example(card.body, "FAIL"), pass_=schema.example(card.body, "PASS"), sources=fm["borrowed_from"],
        orgs=[schema.Org(g.id, orgs.ORGS[g.id], g.urls, strength.of_org(fm["id"], g.urls)) for g in found.organisations],
        people=[schema.Org(g.id, orgs.ORGS[g.id], g.urls, strength.of_org(fm["id"], g.urls)) for g in found.people],
        backing=strength.backing(fm["id"], [g.urls for g in found.organisations]),
        url=f"{page_url(page_name(card))}#{fm['id']}", markdown_url=markdown_url(card))


def corpus(kind: schema.Kind, cards: Sequence[Card], b: BuildInput) -> schema.Corpus:
    """The cards.json model: kind "stable" for the vetted cards, "drafts" for every other card."""
    levels = [schema.LevelInfo(
        id=lv, name=NAME[lv], input=INPUT[lv], description=LEVEL_DESC[lv], stable_count=b.counts[lv].stable, draft_count=b.counts[lv].draft,
        gives_verdict=bool(b.counts[lv].stable), url=page_url(lv), markdown_url=f"{BASE}/{lv}.md") for lv in LEVELS]
    return schema.Corpus(schema.SCHEMA_VERSION, kind, SITE_NAME, f"{BASE}/", LICENCE_URL, b.date, list(CONCERNS), levels,
                         [_card_model(c) for c in cards])


def check_union(merged: list[str], by_file: dict[str, list[str]]) -> None:
    """Raise BuildError unless the per-level files together hold exactly the cards of the merged file (which has no repeated id), so each card is in one file."""
    union = [i for ids in by_file.values() for i in ids]
    if sorted(union) != sorted(merged):
        missing = sorted(set(merged) - set(union))
        extra = sorted(set(union) - set(merged))
        raise BuildError(f"level files hold {len(union)} cards, the merged file {len(merged)}; missing {missing[:5]}, extra {extra[:5]}")


def check_concern_files(merged: list[dict[str, Any]], by_file: dict[str, list[str]]) -> None:
    """Raise BuildError unless each concern file holds the ids of the merged cards that list the concern, in the merged order."""
    for concern in CONCERNS:
        name = f"cards/concern-{concern}.json"
        expected = [c["id"] for c in merged if concern in c["concerns"]]
        if by_file.get(name, []) != expected:
            raise BuildError(f"{name} holds {len(by_file.get(name, []))} cards, the merged file has {len(expected)} that list {concern}")


def index_model(cards: Sequence[Card]) -> schema.CardsIndex:
    """The slim index: one short record per card."""
    return schema.CardsIndex(
        schema.SCHEMA_VERSION, [str(c) for c in CONCERNS], list(LEVELS),
        [schema.IndexCard(c.fm["id"], c.fm["level"], c.fm["severity"], concerns(c), topics(c), rule(c.body), f"{page_url(page_name(c))}#{c.fm['id']}") for c in cards])


def check_index(index: dict[str, Any], merged: list[dict[str, Any]]) -> None:
    """Raise BuildError unless the slim index holds the merged cards, in order, with the same slim fields."""
    slim = ("id", "level", "severity", "concerns", "topics", "rule", "url")
    expected = [{k: c[k] for k in slim} for c in merged]
    if index["cards"] != expected:
        raise BuildError("cards-index.json differs from cards.json in its ids or slim fields")


def _emit(files: dict[str, str], name: str, data: dict[str, Any], sch: dict[str, Any]) -> None:
    """Validate one file against its schema, then add its text to `files`."""
    if problems := schema.check(sch, data):
        raise BuildError(f"{name} does not match its schema:\n" + "\n".join(problems[:10]))
    files[name] = json.dumps(data, indent=1, ensure_ascii=False) + "\n"


def cards_files(b: BuildInput) -> dict[str, str]:
    """Every cards file, as text keyed by path under site/.

    - `cards.json` and `cards-drafts.json` hold every card of their kind.
    - `cards/<level>.json` and `cards/drafts-<level>.json` hold one level (a pack card goes with its own level); they exist for levels with cards.
    - `cards/concern-<concern>.json` holds the stable cards that list the concern, so a card appears under each of its concerns.
    - `cards-index.json` is the slim index of the stable cards, `concerns/<concern>.md` and `concerns/level-<level>.md` the Markdown lists.

    All of them come from the same card lists. The cards files share cards.schema.json and the index has cards-index.schema.json.
    Raises BuildError when a file breaks its schema, or when the files disagree with the merged file.
    """
    sch = schema.json_schema(BASE)
    index_sch = schema.index_json_schema(BASE)
    files = {"cards.schema.json": json.dumps(sch, indent=2) + "\n", "cards-index.schema.json": json.dumps(index_sch, indent=2) + "\n"}
    merged_stable: list[dict[str, Any]] = []
    for kind, merged_name, prefix, cards in ((schema.Kind.STABLE, "cards.json", "", b.stable), (schema.Kind.DRAFTS, "cards-drafts.json", "drafts-", b.draft)):
        parts = {merged_name: cards}
        parts.update({f"cards/{prefix}{lv}.json": cs for lv in LEVELS if (cs := [c for c in cards if level_of(c) == lv])})
        if kind == schema.Kind.STABLE:
            parts.update({f"cards/concern-{cn}.json": cs for cn in CONCERNS if (cs := [c for c in cards if cn in concerns(c)])})
        ids: dict[str, list[str]] = {}
        for name, part in parts.items():
            data = schema.to_dict(corpus(kind, part, b))
            _emit(files, name, data, sch)
            ids[name] = [c["id"] for c in data["cards"]]
            if name == merged_name and kind == schema.Kind.STABLE:
                merged_stable = data["cards"]
        merged_ids = ids.pop(merged_name)
        concern_ids = {n: i for n, i in ids.items() if n.startswith("cards/concern-")}
        check_union(merged_ids, {n: i for n, i in ids.items() if n not in concern_ids})
        if kind == schema.Kind.STABLE:
            check_concern_files(merged_stable, concern_ids)
    index = schema.to_dict(index_model(b.stable))
    _emit(files, "cards-index.json", index, index_sch)
    check_index(index, merged_stable)
    files.update(site_concerns.files(index))
    return files
