import json
from pathlib import Path

import pytest

import sbom
from sbom import Component, Licence

MIT = Licence(expression="MIT")


def component(name: str = "x", licence: Licence | None = MIT) -> Component:
    return Component(name, "1.0", f"pkg:pypi/{name}@1.0", "library", licence)


def test_render_is_deterministic_and_sorted() -> None:
    a, b = component("b"), component("a")
    assert sbom.render([a, b]) == sbom.render([b, a])
    assert [c["name"] for c in json.loads(sbom.render([a, b]))["components"]] == ["a", "b"]


@pytest.mark.parametrize(
    ("licence", "expected"),
    [(Licence(expression="MIT"), [{"expression": "MIT"}]), (Licence(name="Some Licence"), [{"license": {"name": "Some Licence"}}])],
    ids=["spdx-expression", "free-text-name"],
)
def test_render_writes_the_licence(licence: Licence, expected: list[dict[str, object]]) -> None:
    assert json.loads(sbom.render([component(licence=licence)]))["components"][0]["licenses"] == expected


def test_a_missing_licence_fails(tmp_path: Path) -> None:
    components = [component("ok"), component("bare", licence=None)]
    rendered = sbom.render(components)
    committed = tmp_path / "sbom.cdx.json"
    committed.write_text(rendered)
    assert sbom.problems(components, committed, rendered) == ["no licence found for bare 1.0 (run `uv sync --locked` and `npm ci` so the metadata is installed)"]


@pytest.mark.parametrize(("on_disk", "fragment"), [(None, "is missing"), ("{}\n", "is stale")], ids=["missing-file", "stale-file"])
def test_a_missing_or_stale_file_fails(tmp_path: Path, on_disk: str | None, fragment: str) -> None:
    committed = tmp_path / "sbom.cdx.json"
    if on_disk is not None:
        committed.write_text(on_disk)
    errors = sbom.problems([component()], committed, sbom.render([component()]))
    assert len(errors) == 1
    assert fragment in errors[0]


def test_current_file_passes(tmp_path: Path) -> None:
    committed = tmp_path / "sbom.cdx.json"
    committed.write_text(sbom.render([component()]))
    assert sbom.problems([component()], committed, committed.read_text()) == []


def test_node_components_read_name_version_and_licence(tmp_path: Path) -> None:
    lock = tmp_path / "package-lock.json"
    lock.write_text(json.dumps({"packages": {"": {"name": "root"}, "node_modules/a": {"version": "1.0.0", "license": "MIT"},
                                             "node_modules/@s/b": {"version": "2.0.0"}}}))
    a, b = sbom.node_components(lock)
    assert (a.name, a.licence) == ("a", Licence(expression="MIT"))
    assert (b.name, b.purl, b.licence) == ("@s/b", "pkg:npm/%40s/b@2.0.0", None)


def test_the_committed_sbom_is_current() -> None:
    components = sbom.collect(sbom.ROOT)
    assert sbom.problems(components, sbom.SBOM_FILE, sbom.render(components)) == []
