#!/usr/bin/env python3
"""Check that every relative link and anchor in the tracked Markdown files resolves.

    python3 tools/check_links.py

Skips external links (a scheme such as https: or mailto:), the literal `(url)` placeholder, fenced code, and inline code.
Reads files only; no network. Exits 1 and prints `file:line: message` for each broken link.
"""
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from config import ROOT

LINK = re.compile(r"(?<!!)\[(?:[^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`\n]*`")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
PLACEHOLDERS = {"url"}


@dataclass(frozen=True, slots=True)
class Link:
    file: Path
    line: int
    target: str


def tracked_markdown(root: Path) -> list[Path]:
    """The Markdown files git tracks, or every *.md under root when git is not available."""
    try:
        out = subprocess.run(["git", "ls-files", "*.md"], cwd=root, capture_output=True, text=True, check=True).stdout
        return [root / line for line in out.splitlines() if line]
    except (OSError, subprocess.CalledProcessError):
        return sorted(root.rglob("*.md"))


def slugs(text: str) -> set[str]:
    """GitHub heading anchors for a Markdown file: lower case, punctuation dropped, spaces to hyphens, repeats numbered."""
    seen: dict[str, int] = {}
    out = set()
    in_fence = False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
        m = None if in_fence else re.match(r"#{1,6}\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        base = re.sub(r"[^\w\- ]", "", re.sub(r"`|\*|_(?=\w)", "", m.group(1)).lower()).replace(" ", "-")
        n = seen.get(base, 0)
        seen[base] = n + 1
        out.add(base if n == 0 else f"{base}-{n}")
    return out


def links_in(path: Path) -> list[Link]:
    """Every link in a file outside fenced and inline code."""
    found = []
    in_fence = False
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        found += [Link(path, n, m.group(1)) for m in LINK.finditer(INLINE_CODE.sub("", line))]
    return found


def problem(link: Link, root: Path, anchors: dict[Path, set[str]]) -> str | None:
    """Return why a link is broken, or None when it resolves or is out of scope."""
    target = link.target
    if SCHEME.match(target) or target in PLACEHOLDERS:
        return None
    path_part, _, fragment = target.partition("#")
    path_part = unquote(path_part.split("?")[0])
    if not path_part:
        dest = link.file
    elif path_part.startswith("/"):
        dest = root / path_part.lstrip("/")
    else:
        dest = link.file.parent / path_part
    if not dest.exists():
        return f"{target}: no such file {dest.relative_to(root) if dest.is_relative_to(root) else dest}"
    if fragment and dest.suffix == ".md":
        if dest not in anchors:
            anchors[dest] = slugs(dest.read_text())
        if unquote(fragment).lower() not in anchors[dest]:
            return f"{target}: no heading with that anchor in {dest.relative_to(root)}"
    return None


def check(root: Path, files: list[Path]) -> list[str]:
    """Return one `file:line: message` per broken link."""
    anchors: dict[Path, set[str]] = {}
    errors = []
    for f in files:
        for link in links_in(f):
            if msg := problem(link, root, anchors):
                errors.append(f"{f.relative_to(root)}:{link.line}: {msg}")
    return errors


def main() -> int:
    files = tracked_markdown(ROOT)
    errors = check(ROOT, files)
    print("\n".join(errors) if errors else f"{len(files)} Markdown files: every relative link and anchor resolves")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
