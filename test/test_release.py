"""One version string everywhere, and a frozen release never changes (docs/versioning.md)."""
import re

import pytest

import release
from build import Plan
from config import ADOPTION_LINE, ROOT, VERSION
from errors import BuildError


def test_every_version_string_is_the_same(plan: Plan) -> None:
    assert f'version = "{VERSION}"' in (ROOT / "pyproject.toml").read_text()
    assert f"\nversion: {VERSION}\n" in (ROOT / "CITATION.cff").read_text()
    assert f'version: "{VERSION}"' in plan.skill["SKILL.md"].decode()
    released = re.search(r"^## \[(\d+\.\d+\.\d+)\]", (ROOT / "CHANGELOG.md").read_text(), re.M)
    assert released and released[1] == VERSION, "the newest released heading in CHANGELOG.md names VERSION"


def test_the_readme_carries_the_current_adoption_line(plan: Plan) -> None:
    readme = (ROOT / "README.md").read_text()
    assert ADOPTION_LINE in readme and f"/v/{VERSION}/badge.svg" in readme
    assert ADOPTION_LINE in plan.site["guides/code-review-with-ai-agents.md"].decode()


def test_frozen_releases_do_not_change(plan: Plan) -> None:
    assert release.digests() == release.SUMS.read_text(), "a file in releases/ changed; releases are frozen"
    assert f"v/{VERSION}/cards.json" in plan.site, "run: python3 tools/build.py && python3 tools/release.py"


def cards(*pairs: tuple[str, str], schema: int = 5) -> dict[str, object]:
    return {"schema_version": schema, "cards": [{"id": i, "severity": s} for i, s in pairs]}


@pytest.mark.parametrize(("new", "bump"), [
    (cards(("a", "block")), release.Bump.PATCH),
    (cards(("a", "block"), ("b", "discuss")), release.Bump.MINOR),
    (cards(("a", "should-fix")), release.Bump.MINOR),
    (cards(), release.Bump.MAJOR),
    (cards(("a", "block"), schema=6), release.Bump.MAJOR),
])
def test_required_bump(new: dict[str, object], bump: release.Bump) -> None:
    assert release.required_bump(cards(("a", "block")), new) == bump


def test_check_bump() -> None:
    release.check_bump("0.2.0", "0.3.0", release.Bump.MAJOR)  # while MAJOR is 0, breaking changes bump MINOR
    release.check_bump("1.0.0", "1.1.0", release.Bump.MINOR)
    for previous, new, needed in (("0.2.0", "0.2.1", release.Bump.MINOR), ("1.0.0", "1.1.0", release.Bump.MAJOR), ("0.2.0", "0.2.0", release.Bump.PATCH)):
        with pytest.raises(BuildError):
            release.check_bump(previous, new, needed)
