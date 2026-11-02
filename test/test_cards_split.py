import json
from typing import Any

import pytest

import schema
from config import BASE, CARDS_JSON_BUDGET, LLMS_BUDGET
from errors import BuildError
from models import CONCERNS, LEVELS
from site_cards import check_concern_files, check_index, check_union

KINDS = [("cards.json", "cards/"), ("cards-drafts.json", "cards/drafts-")]


def level_files(site_text: dict[str, str], prefix: str) -> dict[str, dict[str, Any]]:
    return {lv: json.loads(site_text[f"{prefix}{lv}.json"]) for lv in LEVELS if f"{prefix}{lv}.json" in site_text}


@pytest.mark.parametrize(("merged", "prefix"), KINDS)
def test_the_level_files_hold_exactly_the_merged_cards(site_text: dict[str, str], merged: str, prefix: str) -> None:
    ids = [c["id"] for part in level_files(site_text, prefix).values() for c in part["cards"]]
    merged_ids = [c["id"] for c in json.loads(site_text[merged])["cards"]]
    assert merged_ids
    assert len(ids) == len(set(ids)) == len(merged_ids)
    assert sorted(ids) == sorted(merged_ids)


@pytest.mark.parametrize(("merged", "prefix"), KINDS)
def test_each_card_is_in_the_file_of_its_own_level(site_text: dict[str, str], merged: str, prefix: str) -> None:
    for lv, part in level_files(site_text, prefix).items():
        assert part["cards"]
        assert {c["level"] for c in part["cards"]} == {lv}


@pytest.mark.parametrize(("merged", "prefix"), KINDS)
def test_each_level_file_keeps_the_merged_top_level_keys_and_card_order(site_text: dict[str, str], merged: str, prefix: str) -> None:
    whole = json.loads(site_text[merged])
    order = {c["id"]: i for i, c in enumerate(whole["cards"])}
    for part in level_files(site_text, prefix).values():
        assert list(part) == list(whole)
        assert {k: v for k, v in part.items() if k != "cards"} == {k: v for k, v in whole.items() if k != "cards"}
        positions = [order[c["id"]] for c in part["cards"]]
        assert positions == sorted(positions)


def test_every_emitted_file_passes_the_schema_and_the_budget(site_text: dict[str, str]) -> None:
    sch = schema.json_schema(BASE)
    names = [n for n in site_text if n.startswith("cards/") or n in {"cards.json", "cards-drafts.json"}]
    assert len(names) > 2
    for name in names:
        assert schema.check(sch, json.loads(site_text[name])) == [], name
        assert len(site_text[name].encode()) <= CARDS_JSON_BUDGET, name


def test_llms_txt_advertises_a_level_file(site_text: dict[str, str]) -> None:
    assert f"{BASE}/cards/function.json" in site_text["llms.txt"]
    assert "cards/function.json" in site_text


@pytest.mark.parametrize(
    ("by_file", "fragment"),
    [
        ({"a": ["x"], "b": ["y"]}, ""),
        ({"a": ["x"]}, "level files hold 1 cards, the merged file 2"),
        ({"a": ["x"], "b": ["y", "z"]}, "level files hold 3 cards, the merged file 2"),
        ({"a": ["x", "y"], "b": ["y"]}, "level files hold 3 cards"),
        ({"a": ["x", "x"]}, "missing ['y']"),
    ],
    ids=["equal", "card-missing", "card-extra", "card-in-two-files", "same-count-wrong-ids"],
)
def test_check_union(by_file: dict[str, list[str]], fragment: str) -> None:
    if not fragment:
        check_union(["x", "y"], by_file)
        return
    with pytest.raises(BuildError, match=fragment.replace("[", r"\[").replace("]", r"\]")):
        check_union(["x", "y"], by_file)


CONCERN_PREFIX = "cards/concern-"


def test_each_concern_file_holds_the_stable_cards_that_list_the_concern(site_text: dict[str, str]) -> None:
    merged = json.loads(site_text["cards.json"])["cards"]
    files = {n: json.loads(t) for n, t in site_text.items() if n.startswith(CONCERN_PREFIX)}
    assert files
    for concern in CONCERNS:
        expected = [c["id"] for c in merged if concern in c["concerns"]]
        name = f"{CONCERN_PREFIX}{concern}.json"
        if expected:
            assert [c["id"] for c in files[name]["cards"]] == expected, concern
            assert all(concern in c["concerns"] for c in files[name]["cards"])
        else:
            assert name not in files
    assert any(len([c for c in merged if cn in c["concerns"]]) > 1 for cn in CONCERNS)
    assert len(merged) < sum(len(f["cards"]) for f in files.values()), "a card with two concerns appears under each"


def test_the_slim_index_matches_cards_json(site_text: dict[str, str]) -> None:
    merged = json.loads(site_text["cards.json"])
    index = json.loads(site_text["cards-index.json"])
    assert [c["id"] for c in index["cards"]] == [c["id"] for c in merged["cards"]]
    for slim, full in zip(index["cards"], merged["cards"], strict=True):
        assert slim == {k: full[k] for k in slim}
    assert index["concerns"] == merged["concerns"]
    assert index["levels"] == [lv["id"] for lv in merged["levels"]]
    assert index["schema_version"] == merged["schema_version"]


def test_the_slim_index_is_small(site_text: dict[str, str]) -> None:
    assert len(site_text["cards-index.json"]) < len(site_text["cards.json"]) / 4


def test_the_slim_index_passes_its_own_schema_and_not_the_cards_schema(site_text: dict[str, str]) -> None:
    index = json.loads(site_text["cards-index.json"])
    assert schema.check(schema.index_json_schema(BASE), index) == []
    assert schema.check(schema.json_schema(BASE), index)
    assert json.loads(site_text["cards-index.schema.json"]) == schema.index_json_schema(BASE)


def test_the_index_schema_rejects_a_missing_or_extra_key() -> None:
    sch = schema.index_json_schema(BASE)
    card = {"id": "x", "level": "change", "severity": "block", "concerns": [], "topics": [], "rule": "r", "url": "u"}
    good = {"schema_version": 4, "concerns": [], "levels": ["change"], "cards": [card]}
    assert schema.check(sch, good) == []
    assert "missing 'url'" in " ".join(schema.check(sch, {**good, "cards": [{k: v for k, v in card.items() if k != "url"}]}))
    assert "unexpected 'sources'" in " ".join(schema.check(sch, {**good, "cards": [{**card, "sources": []}]}))


@pytest.mark.parametrize(
    ("merged", "files", "fragment"),
    [
        ([{"id": "a", "concerns": ["security"]}], {"cards/concern-security.json": ["a"]}, ""),
        ([{"id": "a", "concerns": ["security"]}], {}, "holds 0 cards, the merged file has 1"),
        ([{"id": "a", "concerns": ["security"]}, {"id": "b", "concerns": ["security"]}], {"cards/concern-security.json": ["b", "a"]}, "holds 2 cards"),
        ([{"id": "a", "concerns": ["testing"]}], {"cards/concern-security.json": ["a"]}, "cards/concern-security.json holds 1 cards, the merged file has 0"),
    ],
    ids=["equal", "file-missing", "wrong-order", "wrong-concern"],
)
def test_check_concern_files(merged: list[dict[str, Any]], files: dict[str, list[str]], fragment: str) -> None:
    if not fragment:
        check_concern_files(merged, files)
        return
    with pytest.raises(BuildError, match=fragment):
        check_concern_files(merged, files)


def test_check_index_fails_on_a_changed_rule() -> None:
    full = {"id": "a", "level": "change", "severity": "block", "concerns": [], "topics": [], "rule": "r", "url": "u", "why": "w"}
    slim = {k: full[k] for k in ("id", "level", "severity", "concerns", "topics", "rule", "url")}
    check_index({"cards": [slim]}, [full])
    with pytest.raises(BuildError, match="differs"):
        check_index({"cards": [{**slim, "rule": "other"}]}, [full])


def test_markdown_files_exist_for_each_concern_and_level(site_text: dict[str, str]) -> None:
    concern_files = {n for n in site_text if n.startswith("concerns/")}
    assert {f"concerns/{c}.md" for c in CONCERNS if f"{CONCERN_PREFIX}{c}.json" in site_text} <= concern_files
    assert {f"concerns/level-{lv}.md" for lv in LEVELS if f"cards/{lv}.json" in site_text} <= concern_files
    body = site_text["concerns/security.md"]
    assert body.startswith("# Concerns\n\nStable cards that match concern: security.")
    assert body.endswith("\n")


def test_llms_txt_advertises_the_static_routes(site_text: dict[str, str]) -> None:
    for path in ("cards/concern-security.json", "concerns/security.md", "cards-index.json", "cards-index.schema.json"):
        assert f"{BASE}/{path}" in site_text["llms.txt"]
        assert path in site_text
    assert len(site_text["llms.txt"]) <= LLMS_BUDGET
