import json
from typing import Any

import pytest

import schema
from config import BASE, CARDS_JSON_BUDGET
from errors import BuildError
from models import LEVELS
from site_meta import check_union

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
