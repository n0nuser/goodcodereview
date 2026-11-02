from pathlib import Path

import pytest

import orgs
from validate import validate

CARD = """---
id: fn-x
level: function
tags: [correctness]
severity: block
status: stable
lang: core
applies_when: Always.
tool_gate: none
borrowed_from:
{urls}
---

**Rule.** R.

**Why.** W.

**FAIL**

```text
f
```

**PASS**

```text
p
```

**Counterpoint.** C.
"""
TWO_ORGS_PLUS_ONE = ["https://www.w3.org/a", "https://web.dev/a", "https://developer.chrome.com/a"]


def errors_for(root: Path, urls: list[str]) -> list[str]:
    (root / "cards" / "audit" / "function").mkdir(parents=True)
    (root / "docs" / "research").mkdir(parents=True)
    (root / "glossary").mkdir()
    (root / "cards" / "audit" / "function" / "fn-x.md").write_text(CARD.format(urls="\n".join(f"  - {u}" for u in urls)))
    (root / "docs" / "research" / "n.md").write_text("\n".join(urls))
    return validate(root)


@pytest.mark.parametrize(
    ("url", "org"),
    [
        ("https://raw.githubusercontent.com/OWASP/ASVS/master/x.md", "owasp"),
        ("https://github.com/cursor/plugins/blob/main/x.md", "cursor"),
        ("https://github.com/someone-new/repo", None),
        ("https://cheatsheetseries.owasp.org/x.html", "owasp"),
        ("https://www.w3.org/TR/WCAG22/", "w3c"),
        ("https://www.ncsc.gov.uk/x", "ncsc"),
    ],
    ids=["raw-host-to-owner", "code-host-owner", "unknown-owner", "subdomain", "www", "gov-uk-subdomain"],
)
def test_org_of(url: str, org: str | None) -> None:
    assert orgs.org_of(url) == org


def test_every_org_has_a_name() -> None:
    assert set(orgs.PREFIXES.values()) - set(orgs.ORGS) == set()
    assert set(orgs.ICONS) - set(orgs.ORGS) == set()


def test_an_unmapped_url_fails_validation(tmp_path: Path) -> None:
    errs = errors_for(tmp_path, ["https://example.com/a", "https://www.w3.org/a", "https://web.dev/a", "https://owasp.org/a"])
    assert "no organisation in tools/orgs.py: https://example.com/a" in " ".join(errs)


def test_split_puts_people_apart_from_orgs() -> None:
    urls = ["https://testdesiderata.com/", "https://web.dev/a", "https://kentcdodds.com/blog/x", "https://owasp.org/a", "https://newsletter.kentbeck.com/p"]
    found = orgs.split(urls)
    assert found.organisations == [orgs.OrgUrls("google", ["https://web.dev/a"]), orgs.OrgUrls("owasp", ["https://owasp.org/a"])]
    assert found.people == [orgs.OrgUrls("kent-beck", ["https://testdesiderata.com/", "https://newsletter.kentbeck.com/p"]), orgs.OrgUrls("kent-c-dodds", ["https://kentcdodds.com/blog/x"])]


def test_persons_are_known_ids_and_orgs_are_not_persons() -> None:
    assert set(orgs.ORGS) >= orgs.PERSONS
    assert {"kent-beck", "kent-c-dodds"} <= orgs.PERSONS
    assert "google" not in orgs.PERSONS


@pytest.mark.parametrize(
    "urls",
    [
        ["https://web.dev/a", "https://testdesiderata.com/", "https://kentcdodds.com/b", "https://owasp.org/a"],
        TWO_ORGS_PLUS_ONE,
        ["https://www.w3.org/a", "https://web.dev/a", "https://martin.kleppmann.com/a"],
    ],
    ids=["people-do-not-count", "two-orgs", "a-person-is-not-an-org"],
)
def test_a_stable_card_below_the_floor_fails(tmp_path: Path, urls: list[str]) -> None:
    assert "has 2 organisation(s)" in " ".join(errors_for(tmp_path, urls))


def test_three_orgs_pass(tmp_path: Path) -> None:
    assert errors_for(tmp_path, [*TWO_ORGS_PLUS_ONE, "https://owasp.org/a"]) == []


def test_a_creator_source_satisfies_the_floor(tmp_path: Path) -> None:
    assert errors_for(tmp_path, ["https://pablogonzalez.me/posts/python-code-review-guide/"]) == []
