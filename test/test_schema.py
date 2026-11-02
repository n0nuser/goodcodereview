import json
from typing import Any

import pytest

import orgs
import schema
from config import BASE


@pytest.fixture
def json_schema() -> dict[str, Any]:
    return schema.json_schema(BASE)


@pytest.mark.parametrize("name", ["cards.json", "cards-drafts.json"])
def test_built_files_match_the_schema(site_text: dict[str, str], json_schema: dict[str, Any], name: str) -> None:
    assert schema.check(json_schema, json.loads(site_text[name])) == []


def test_a_missing_key_fails(cards_json: dict[str, Any], json_schema: dict[str, Any]) -> None:
    del cards_json["cards"][0]["rule"]
    assert "missing 'rule'" in " ".join(schema.check(json_schema, cards_json))


def test_a_value_outside_the_enum_fails(cards_json: dict[str, Any], json_schema: dict[str, Any]) -> None:
    cards_json["cards"][0]["severity"] = "urgent"
    assert schema.check(json_schema, cards_json)


def test_an_unknown_key_fails(cards_json: dict[str, Any], json_schema: dict[str, Any]) -> None:
    cards_json["cards"][0]["extra"] = 1
    assert "unexpected 'extra'" in " ".join(schema.check(json_schema, cards_json))


def test_only_drafts_say_what_they_lack(cards_json: dict[str, Any], site_text: dict[str, str]) -> None:
    assert {c["lacks"] for c in cards_json["cards"]} == {None}
    drafts = json.loads(site_text["cards-drafts.json"])["cards"]
    assert all(c["lacks"]["reason"] and c["lacks"]["note"] for c in drafts)


def test_a_reason_outside_the_list_fails(site_text: dict[str, str], json_schema: dict[str, Any]) -> None:
    drafts = json.loads(site_text["cards-drafts.json"])
    drafts["cards"][0]["lacks"] = {"reason": "vibes", "note": "x"}
    assert schema.check(json_schema, drafts)


def test_orgs_and_people_together_cover_every_source(cards_json: dict[str, Any]) -> None:
    # No three-organisation assertion here: validate.py errors on a stable card below the floor.
    for c in cards_json["cards"]:
        assert sorted(u for o in c["orgs"] + c["people"] for u in o["sources"]) == sorted(c["sources"]), c["id"]


def test_people_never_count_as_orgs(cards_json: dict[str, Any]) -> None:
    for c in cards_json["cards"]:
        assert [o["id"] for o in c["orgs"] if o["id"] in orgs.PERSONS] == [], c["id"]


def test_a_card_without_orgs_fails(cards_json: dict[str, Any], json_schema: dict[str, Any]) -> None:
    del cards_json["cards"][0]["orgs"]
    assert "missing 'orgs'" in " ".join(schema.check(json_schema, cards_json))


def test_pass_is_a_json_key_not_pass_underscore(cards_json: dict[str, Any]) -> None:
    assert "pass" in cards_json["cards"][0]
    assert "pass_" not in cards_json["cards"][0]
