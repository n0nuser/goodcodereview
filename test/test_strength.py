from pathlib import Path
from typing import Any

import pytest

import strength
from schema import Backing, Strength


@pytest.fixture
def judged(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    f = tmp_path / "s.tsv"
    f.write_text("card\turl\tverdict\tjudged\n"
                 "c\thttps://a/1\tsupports\t2026-11-04\nc\thttps://b/1\tpartial\t2026-11-04\nc\thttps://b/2\tsupports\t2026-11-04\n"
                 "c\thttps://c/1\tsupports\t2026-11-04\nc\thttps://d/1\tweak\t2026-11-04\n")
    monkeypatch.setattr(strength, "STRENGTH_FILE", f)
    strength._rows.cache_clear()
    yield
    strength._rows.cache_clear()


def test_an_organisation_is_as_strong_as_its_best_source(judged: None) -> None:
    assert strength.of_org("c", ["https://b/1", "https://b/2"]) is Strength.SUPPORTS
    assert strength.of_org("c", ["https://d/1"]) is Strength.WEAK


def test_a_source_with_no_row_is_unjudged_and_is_per_card(judged: None) -> None:
    assert strength.of_org("c", ["https://z/1"]) is Strength.UNJUDGED
    assert strength.of_org("other", ["https://a/1"]) is Strength.UNJUDGED


def test_backing_is_strong_mixed_or_unjudged(judged: None) -> None:
    assert strength.backing("c", [["https://a/1"], ["https://b/2"], ["https://c/1"]]) is Backing.STRONG
    assert strength.backing("c", [["https://a/1"], ["https://b/1"], ["https://z/1"]]) is Backing.MIXED
    assert strength.backing("c", [["https://z/1"], ["https://y/1"]]) is Backing.UNJUDGED


def test_every_row_names_a_known_verdict_and_a_stable_or_draft_card(cards_json: dict[str, Any]) -> None:
    ids = {c["id"] for c in cards_json["cards"]}
    rows = [line.split("\t") for line in strength.STRENGTH_FILE.read_text().splitlines()[1:]]
    assert rows
    assert {r[2] for r in rows} <= {s.value for s in Strength}
    assert all(r[0] for r in rows)
    assert len(ids) > 100
