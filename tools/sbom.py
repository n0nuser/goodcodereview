#!/usr/bin/env python3
"""Write or check sbom.cdx.json, a CycloneDX 1.6 SBOM of the dev dependencies and the bundled Simple Icons data.

    python3 tools/sbom.py            write sbom.cdx.json
    python3 tools/sbom.py --check    fail if it is stale, or if any component has no licence

The deployed site has no runtime dependency: the build uses only the standard library. The SBOM lists what the repository
installs to test and check it (Python from uv.lock, Node from package-lock.json) and the third-party data it ships
(tools/org_icons.json, Simple Icons, CC0). Python licences come from the installed package metadata, so run `uv sync --locked` first.
Standard library only.
"""
import argparse
import json
import sys
import tomllib
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, metadata
from pathlib import Path
from typing import Any

from config import ROOT, SBOM_FILE, SIMPLE_ICONS_VERSION

SPEC_VERSION = "1.6"
LICENCE_PREFIX = "License :: OSI Approved :: "
LICENCE_FIELD_MAX = 100  # a longer License field is licence text, not a name


@dataclass(frozen=True, slots=True)
class Licence:
    """An SPDX expression, or a free-text name when the package gives no SPDX identifier."""

    expression: str | None = None
    name: str | None = None


@dataclass(frozen=True, slots=True)
class Component:
    name: str
    version: str
    purl: str
    kind: str  # CycloneDX component type: "library" or "data"
    licence: Licence | None


# Packages that uv.lock pins but a Linux install skips, so their metadata is not there to read. Each entry names why.
LICENCE_OVERRIDES = {
    "colorama": Licence(expression="BSD-3-Clause"),  # Windows-only dependency of pytest; BSD license on its PyPI page
}


def python_licence(name: str) -> Licence | None:
    """The licence of an installed Python package: its SPDX expression, else a licence classifier, else a short License field."""
    if name in LICENCE_OVERRIDES:
        return LICENCE_OVERRIDES[name]
    try:
        meta = metadata(name)
    except PackageNotFoundError:
        return None
    if expression := meta.get("License-Expression"):
        return Licence(expression=expression)
    classifiers = [c.removeprefix(LICENCE_PREFIX) for c in meta.get_all("Classifier", []) if c.startswith(LICENCE_PREFIX)]
    if classifiers:
        return Licence(name=classifiers[0])
    field = (meta.get("License") or "").strip()
    return Licence(name=field) if field and "\n" not in field and len(field) <= LICENCE_FIELD_MAX else None


def python_components(lock: Path) -> list[Component]:
    """Every package in uv.lock except the project itself."""
    packages = tomllib.loads(lock.read_text())["package"]
    return [
        Component(p["name"], p["version"], f"pkg:pypi/{p['name']}@{p['version']}", "library", python_licence(p["name"]))
        for p in packages
        if "registry" in p.get("source", {})
    ]


def node_components(lock: Path) -> list[Component]:
    """Every package in package-lock.json except the project itself."""
    packages: dict[str, Any] = json.loads(lock.read_text())["packages"]
    out = []
    for path, p in packages.items():
        if not path:
            continue
        name = path.rsplit("node_modules/", 1)[-1]
        licence = p.get("license")
        out.append(Component(name, p["version"], f"pkg:npm/{name.replace('@', '%40', 1)}@{p['version']}", "library", Licence(expression=licence) if licence else None))
    return out


def data_components(icons: Path) -> list[Component]:
    """The third-party data the repository ships: the Simple Icons paths in tools/org_icons.json."""
    if not icons.is_file():
        return []
    return [Component("simple-icons", SIMPLE_ICONS_VERSION, f"pkg:npm/simple-icons@{SIMPLE_ICONS_VERSION}", "data", Licence(expression="CC0-1.0"))]


def render(components: list[Component]) -> str:
    """The SBOM as CycloneDX JSON. It has no timestamp or serial number, so the same inputs give the same file."""
    entries = []
    for c in sorted(components, key=lambda c: (c.kind, c.name, c.version)):
        entry: dict[str, Any] = {"type": c.kind, "name": c.name, "version": c.version, "purl": c.purl}
        if c.licence:
            entry["licenses"] = [{"expression": c.licence.expression}] if c.licence.expression else [{"license": {"name": c.licence.name}}]
        entries.append(entry)
    bom = {"bomFormat": "CycloneDX", "specVersion": SPEC_VERSION, "version": 1,
           "metadata": {"component": {"type": "application", "name": "goodcodereview"}}, "components": entries}
    return json.dumps(bom, indent=2, ensure_ascii=False) + "\n"


def collect(root: Path) -> list[Component]:
    return python_components(root / "uv.lock") + node_components(root / "package-lock.json") + data_components(root / "tools" / "org_icons.json")


def problems(components: list[Component], committed: Path, rendered: str) -> list[str]:
    """Return the reasons the SBOM fails: components without a licence, a missing file, or a stale file."""
    errors = [f"no licence found for {c.name} {c.version} (run `uv sync --locked` and `npm ci` so the metadata is installed)" for c in components if c.licence is None]
    if not committed.is_file():
        errors.append(f"{committed.name} is missing; run `python3 tools/sbom.py` and commit it")
    elif committed.read_text() != rendered:
        errors.append(f"{committed.name} is stale; run `python3 tools/sbom.py` and commit it")
    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="write nothing; fail if the file is stale or a component has no licence")
    args = parser.parse_args(argv)
    components = collect(ROOT)
    rendered = render(components)
    errors = problems(components, SBOM_FILE, rendered)
    if args.check:
        print("\n".join(errors) if errors else f"{SBOM_FILE.name}: {len(components)} components, every one has a licence, and the file is current")
        return 1 if errors else 0
    missing = [e for e in errors if e.startswith("no licence")]
    if missing:
        print("\n".join(missing))
        return 1
    SBOM_FILE.write_text(rendered)
    print(f"wrote {SBOM_FILE.name}: {len(components)} components")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
