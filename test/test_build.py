import subprocess
from pathlib import Path

import pytest
from freezegun import freeze_time

import build
import context
import skill_files
from build import Plan
from errors import BuildError
from markdown import check_md, inline, rule
from site_meta import security_txt, sitemap


def tree(path: Path) -> dict[str, bytes]:
    return {str(p.relative_to(path)): p.read_bytes() for p in sorted(path.rglob("*")) if p.is_file()}


def test_dry_run_writes_nothing(tmp_path: Path, plan: Plan) -> None:
    site, skill = tmp_path / "site", tmp_path / "skill"
    (site).mkdir()
    (site / "old.html").write_text("old")
    (skill / "references").mkdir(parents=True)
    (skill / "references" / "gone.md").write_text("stale")
    report = build.describe(plan, site, skill)
    assert "would remove" in report
    assert str(skill / "references" / "gone.md") in report
    assert tree(site) == {"old.html": b"old"}
    assert tree(skill) == {"references/gone.md": b"stale"}


def test_swap_site_replaces_the_old_site(tmp_path: Path) -> None:
    site = tmp_path / "site"
    site.mkdir()
    (site / "old.html").write_text("old")
    build.swap_site({"index.html": b"new", ".well-known/security.txt": b"x"}, site)
    assert tree(site) == {"index.html": b"new", ".well-known/security.txt": b"x"}
    assert not (tmp_path / "site.new").exists()
    assert not (tmp_path / "site.old").exists()


def test_write_skill_removes_stale_references(tmp_path: Path) -> None:
    (tmp_path / "references").mkdir()
    (tmp_path / "references" / "gone.md").write_text("stale")
    build.write_skill({"SKILL.md": b"s", "references/a.md": b"a"}, tmp_path)
    assert tree(tmp_path) == {"SKILL.md": b"s", "references/a.md": b"a"}


def test_a_failed_budget_leaves_the_skill_untouched(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(skill_files, "REF_BUDGET", 10)
    before = tree(build.SKILL)
    with pytest.raises(BuildError, match="budget 10"):
        build.plan_build(build.ROOT)
    assert tree(build.SKILL) == before


def test_the_plan_is_deterministic(plan: Plan) -> None:
    assert build.plan_build(build.ROOT).site == plan.site


@freeze_time("2026-01-02")
def test_build_date_falls_back_to_today_outside_git(monkeypatch: pytest.MonkeyPatch) -> None:
    def no_git(*args: object, **kwargs: object) -> None:
        raise subprocess.CalledProcessError(128, "git")

    monkeypatch.setattr(context.subprocess, "run", no_git)
    assert context.build_date() == "2026-01-02"


def test_security_txt_expires_180_days_after_the_build_date() -> None:
    assert "Expires: 2026-06-30T00:00:00Z" in security_txt("2026-01-01")


def test_sitemap_lists_each_slug_with_the_build_date() -> None:
    xml = sitemap(["index", "audit"], "2026-01-01")
    assert "<loc>https://goodcodereview.com/</loc><lastmod>2026-01-01</lastmod>" in xml
    assert "<loc>https://goodcodereview.com/audit</loc>" in xml


@pytest.mark.parametrize(
    ("text", "kind"),
    [("1. one", "numbered list"), ("| a | b |", "table"), ("> quote", "quote"), ("  - nested", "nested bullet"), ("---", "rule")],
)
def test_check_md_flags_unsupported_markdown(text: str, kind: str) -> None:
    assert f"({kind})" in " ".join(check_md("x.md", text))


def test_check_md_ignores_code_fences() -> None:
    assert check_md("x.md", "```text\n1. one\n| a |\n```\n") == []


def test_inline_renders_code_bold_and_card_links() -> None:
    assert inline("**b** `<x>` [[fn-a]]", {"fn-a": "function.html#fn-a"}) == '<strong>b</strong> <code>&lt;x&gt;</code> <a href="function.html#fn-a">fn-a</a>'


def test_rule_reads_the_first_paragraph() -> None:
    assert rule("**Rule.** One\ntwo.\n\n**Why.** x") == "One two."


@pytest.mark.parametrize("name", ["index.html", "function.html", "pack-python.html", "concerns.html"])
def test_page_shows_last_updated(site_text: dict[str, str], name: str) -> None:
    assert 'Last updated <time datetime="' in site_text[name]
