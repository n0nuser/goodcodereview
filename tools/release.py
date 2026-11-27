#!/usr/bin/env python3
"""Freeze the card set of this version into releases/<version>/: cards.json, its schema, and a badge. Run after tools/build.py.

    python3 tools/build.py && python3 tools/release.py && python3 tools/build.py

It refuses a version that is already tagged, and a version number smaller than the change since the last release needs (docs/versioning.md).
Standard library only.
"""
import hashlib
import json
import subprocess
from enum import IntEnum
from typing import Any

from config import ROOT, SITE, VERSION
from errors import BuildError

RELEASES = ROOT / "releases"
SUMS = RELEASES / "SHA256SUMS"
FILES = ("cards.json", "cards.schema.json")


class Bump(IntEnum):
    PATCH = 0
    MINOR = 1
    MAJOR = 2


def parse(version: str) -> tuple[int, int, int]:
    major, minor, patch = (int(x) for x in version.split("."))
    return major, minor, patch


def required_bump(old: dict[str, Any], new: dict[str, Any]) -> Bump:
    """The smallest bump the change between two cards.json files needs."""
    before = {c["id"]: c["severity"] for c in old["cards"]}
    after = {c["id"]: c["severity"] for c in new["cards"]}
    if old["schema_version"] != new["schema_version"] or set(before) - set(after):
        return Bump.MAJOR
    if set(after) - set(before) or any(after[i] != s for i, s in before.items()):
        return Bump.MINOR
    return Bump.PATCH


def check_bump(previous: str, version: str, needed: Bump) -> None:
    """Raise BuildError unless `version` is at least `needed` above `previous`. While MAJOR is 0, a breaking change bumps MINOR."""
    a, b = parse(previous), parse(version)
    if b <= a:
        raise BuildError(f"{version} is not above the last release, {previous}")
    got = Bump.MAJOR if b[0] > a[0] else Bump.MINOR if b[1] > a[1] else Bump.PATCH
    if got < (min(needed, Bump.MINOR) if b[0] == 0 else needed):
        raise BuildError(f"the cards changed enough to need a {needed.name} release; {previous} to {version} is only {got.name}")


def badge(version: str) -> str:
    label, value = "reviewed against", f"Good Code Review v{version}"
    left, right = 110, 175
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{left + right}" height="20" role="img" aria-label="{label} {value}">'
            f'<rect width="{left}" height="20" fill="#555"/><rect x="{left}" width="{right}" height="20" fill="#006469"/>'
            '<g fill="#fff" font-family="Verdana,DejaVu Sans,sans-serif" font-size="11" text-anchor="middle">'
            f'<text x="{left // 2}" y="14">{label}</text><text x="{left + right // 2}" y="14">{value}</text></g></svg>\n')


def digests() -> str:
    """One `sha256  path` line per frozen file."""
    return "".join(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(RELEASES)}\n" for f in sorted(RELEASES.glob("*/*")))


def main() -> None:
    if subprocess.run(["git", "rev-parse", "-q", "--verify", f"refs/tags/v{VERSION}"], cwd=ROOT, capture_output=True).returncode == 0:
        raise BuildError(f"v{VERSION} is already tagged; a release is frozen, so raise VERSION in tools/config.py")
    current = json.loads((SITE / "cards.json").read_text())
    older = sorted((p.name for p in RELEASES.glob("*.*.*") if p.name != VERSION), key=parse)
    if older:
        check_bump(older[-1], VERSION, required_bump(json.loads((RELEASES / older[-1] / "cards.json").read_text()), current))
    out = RELEASES / VERSION
    out.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        (out / name).write_bytes((SITE / name).read_bytes())
    (out / "badge.svg").write_text(badge(VERSION))
    SUMS.write_text(digests())
    print(f"froze {len(current['cards'])} cards into {out}")


if __name__ == "__main__":
    main()
