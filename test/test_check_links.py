from pathlib import Path

import pytest

import check_links


def write(root: Path, files: dict[str, str]) -> list[Path]:
    paths = []
    for name, text in files.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        paths.append(p)
    return paths


@pytest.mark.parametrize(
    ("link", "ok"),
    [
        ("[a](b.md)", True),
        ("[a](missing.md)", False),
        ("[a](b.md#setup-notes)", True),
        ("[a](b.md#renamed)", False),
        ("[a](sub/c.md)", True),
        ("[a](/b.md)", True),
        ("[a](#top)", True),
        ("[a](#nope)", False),
        ("[a](https://example.com/gone)", True),
        ("[a](mailto:x@y.z)", True),
        ("[a](url)", True),
        ("`[a](missing.md)`", True),
    ],
    ids=["file", "missing-file", "anchor", "bad-anchor", "subdir", "root-relative", "same-file", "bad-same-file", "external", "mailto", "placeholder", "inline-code"],
)
def test_links(tmp_path: Path, link: str, ok: bool) -> None:
    files = write(tmp_path, {"a.md": f"# Top\n\n{link}\n", "b.md": "# Setup notes\n", "sub/c.md": "x\n"})
    assert (check_links.check(tmp_path, files) == []) is ok


def test_fenced_code_is_skipped(tmp_path: Path) -> None:
    files = write(tmp_path, {"a.md": "```text\n[a](missing.md)\n```\n"})
    assert check_links.check(tmp_path, files) == []


def test_the_message_names_file_and_line(tmp_path: Path) -> None:
    files = write(tmp_path, {"a.md": "ok\n\nsee [x](gone.md)\n"})
    assert check_links.check(tmp_path, files) == ["a.md:3: gone.md: no such file gone.md"]


def test_repeated_headings_get_numbered_anchors() -> None:
    assert check_links.slugs("# A\n\n## A\n") == {"a", "a-1"}


def test_the_repository_docs_resolve() -> None:
    assert check_links.check(check_links.ROOT, check_links.tracked_markdown(check_links.ROOT)) == []
