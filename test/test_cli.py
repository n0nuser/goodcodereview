import json
import sys

import pytest

from config import ROOT, SITE

sys.path.insert(0, str(ROOT / "cli" / "src"))
from goodcodereview import cli  # noqa: E402

BASE = SITE.as_uri()


def test_levels_and_filters(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["--base", BASE, "levels"]) == 0
    assert "function" in capsys.readouterr().out
    assert cli.main(["--base", BASE, "cards", "--level", "function", "--concern", "security", "--json"]) == 0
    got = json.loads(capsys.readouterr().out)
    assert got
    assert all(c["level"] == "function" and "security" in c["concerns"] for c in got)


def test_unknown_card_fails(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["--base", BASE, "card", "no-such-card"]) == 1
