import json
from pathlib import Path
from typing import Any

import pytest
from goodcodereview_lint import cli, gates

REPO = Path(__file__).resolve().parent.parent


def test_every_mapped_card_exists_and_scope_is_known(cards_json: dict[str, Any]) -> None:
    ids = {c["id"] for c in cards_json["cards"]}
    for g in gates.load_gates():
        assert g.card in ids, g
        assert g.scope in {"full", "partial"}, g
        assert g.tool == "ruff", g


def test_the_snapshot_matches_the_built_cards(cards_json: dict[str, Any]) -> None:
    snap = gates.load_snapshot()["cards"]
    built = {c["id"]: {k: c[k] for k in ("level", "severity", "backing", "rule", "url", "tool_gate")} for c in cards_json["cards"]}
    assert snap == built, "run python3 tools/build.py, then python3 lint/scripts/snapshot.py"


def test_coverage_line_counts_cards_and_is_never_a_pass() -> None:
    line = cli.coverage_line(gates.load_gates(), gates.load_snapshot())
    assert "stable cards" in line
    assert "A clean run is not a review." in line


def test_a_code_with_two_cards_reports_the_full_one_first_and_names_the_other() -> None:
    raw = [{"code": "BLE001", "message": "Do not catch blind exception", "filename": "a.py", "location": {"row": 3, "column": 1}}]
    out = cli.findings(raw, gates.load_gates(), gates.load_snapshot())
    assert [f["card"] for f in out] == ["fn-specific-exceptions-only"]
    assert out[0]["also"] == ["py-cancellation"]
    assert out[0]["severity"] in {"block", "should-fix", "discuss"}


def test_a_code_the_map_does_not_know_is_dropped() -> None:
    raw = [{"code": "E501", "message": "long", "filename": "a.py", "location": {"row": 1, "column": 1}}]
    assert cli.findings(raw, gates.load_gates(), gates.load_snapshot()) == []


@pytest.mark.parametrize(("source", "card"), [
    ("def f(o):\n    return getattr(o, 'total')\n", "fn-no-getattr-for-known-names"),
    ("def f():\n    try:\n        g()\n    except Exception:\n        return None\n", "fn-specific-exceptions-only"),
    ("def f(x):\n    return x == 4242\n", "fn-no-magic-values"),
])
def test_ruff_findings_come_back_as_the_card(tmp_path: Path, capsys: pytest.CaptureFixture[str], source: str, card: str) -> None:
    (tmp_path / "bad.py").write_text(source)
    assert cli.main(["check", str(tmp_path), "--json", "--fail-on", "never"]) == 0
    got = json.loads(capsys.readouterr().out)
    assert card in {f["card"] for f in got["findings"]}
    assert "A clean run is not a review." in got["coverage"]


def test_clean_code_has_no_finding_and_exit_zero(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / "ok.py").write_text("def f(o):\n    return o.total\n")
    assert cli.main(["check", str(tmp_path)]) == 0
    assert capsys.readouterr().out.startswith("0 findings.")


def test_a_should_fix_finding_fails_the_run_by_default(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / "bad.py").write_text("def f():\n    try:\n        g()\n    except Exception:\n        return None\n")
    code = cli.main(["check", str(tmp_path)])
    out = capsys.readouterr().out
    sev = gates.load_snapshot()["cards"]["fn-specific-exceptions-only"]["severity"]
    assert code == (0 if sev == "discuss" else 1), out
