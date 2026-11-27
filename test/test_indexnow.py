"""IndexNow submits only the pages that changed (tools/indexnow.py)."""
from pathlib import Path

import indexnow
from build import Plan
from config import INDEXNOW_KEY


def test_changed_ignores_dates_and_reports_new_and_removed_pages(tmp_path: Path) -> None:
    old, new = tmp_path / "old", tmp_path / "new"
    for site, files in ((old, {"index": "a 2026-01-01", "gone": "x", "edit": "one"}), (new, {"index": "a 2026-02-02", "added": "y", "edit": "two", "404": "z"})):
        site.mkdir()
        for name, text in files.items():
            (site / f"{name}.html").write_text(text)
    assert indexnow.changed(indexnow.pages(old), indexnow.pages(new)) == ["added", "edit", "gone"]


def test_the_key_file_is_served(plan: Plan) -> None:
    assert plan.site[f"{INDEXNOW_KEY}.txt"].decode() == INDEXNOW_KEY
