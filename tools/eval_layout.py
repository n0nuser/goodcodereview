#!/usr/bin/env python3
"""Whole file or parts? Run the same `service` review with the checklist laid out three ways and count the card ids each reply reports.

    python3 tools/eval_layout.py run [--runs N] [--model M] [--save DIR] [LAYOUT ...]

Layouts, each in a scratch copy with the case files from test/evals/cases/audit_repo under repo/:
  whole   only service.md, the whole level in one file
  parts   only the five service-<context>.md parts, which name each other
  llms    the site's llms.txt (links made local) plus every file, so the agent picks, as it would on the site

The score is the share of the level's card ids that appear in the reply as FAIL, PASS, or on an N/A line. A reply that skips a part leaves a gap of
ids. It spends tokens (`claude -p`), so CI runs only the unit test of `coverage`. Background: docs/research/context-splitting.md.
"""
import argparse
import re
import shutil
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path

from config import BASE, SITE
from errors import HarnessError
from eval import ANSI, CASES, _run_cli

LEVEL = "service"
LAYOUTS = ("whole", "parts", "llms")
ID = re.compile(r"^## ([a-z0-9-]+)$", re.M)
PROMPT = (
    "Review the code in ./repo against the Good Code Review `service` level. {entry} "
    "Open with `Verdict: request changes` or `Verdict: approve`. Then report every card of the level exactly once: "
    "`FAIL [severity] id - file:line - why`, `PASS id - file:line`, and every card whose applies_when does not hold on one line, "
    "`N/A (applies_when does not hold): id, id, ...`. Use only the cards in the files you were given."
)
ENTRY = {
    "whole": "The checklist is the file ./service.md.",
    "parts": "The checklist starts at ./service-server.md.",
    "llms": "Start from ./llms.txt, which says where the checklist is.",
}


def part_files(site: Path = SITE) -> list[Path]:
    return sorted(p for p in site.glob(f"{LEVEL}-*.md") if "-index" not in p.name)


def expected_ids(site: Path = SITE) -> list[str]:
    """The card ids in the parts: every core stable card of the level, in file order."""
    return [i for p in part_files(site) for i in ID.findall(p.read_text())]


def coverage(reply: str, ids: Sequence[str]) -> list[str]:
    """The ids that appear nowhere in the reply, as a word on its own."""
    return [i for i in ids if not re.search(rf"(?<![a-z0-9-]){re.escape(i)}(?![a-z0-9-])", reply)]


def stage(layout: str, work: Path, site: Path = SITE) -> None:
    shutil.copytree(CASES / "audit_repo", work / "repo", ignore=shutil.ignore_patterns("case.json"))
    files = ([site / f"{LEVEL}.md"] if layout in ("whole", "llms") else []) + (part_files(site) if layout in ("parts", "llms") else [])
    files += [site / "llms.txt"] if layout == "llms" else []
    for f in files:  # links point at the files beside it, as they point at the site online
        (work / f.name).write_text(f.read_text().replace(f"{BASE}/", "./"))


def run_one(layout: str, model: str | None) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        stage(layout, work)
        cmd = ["claude", "-p", PROMPT.format(entry=ENTRY[layout]), "--allowedTools", "Read,Grep,Glob", "--output-format", "text"]
        out = _run_cli(cmd + (["--model", model] if model else []), work, f"{layout}: ")
    return ANSI.sub("", out)


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["run"])
    ap.add_argument("layouts", nargs="*", default=list(LAYOUTS))
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--model")
    ap.add_argument("--save", metavar="DIR")
    a = ap.parse_args(argv)
    ids = expected_ids()
    print(f"{len(ids)} card ids expected\n{'layout':<8}{'run':>4}{'reported':>10}  missing")
    for layout in a.layouts:
        for n in range(1, a.runs + 1):
            try:
                reply = run_one(layout, a.model)
            except HarnessError as e:
                print(f"{layout:<8}{n:>4}  harness error: {e}", file=sys.stderr)
                continue
            if a.save:
                Path(a.save).mkdir(parents=True, exist_ok=True)
                (Path(a.save) / f"{layout}-{n}.txt").write_text(reply)
            gap = coverage(reply, ids)
            print(f"{layout:<8}{n:>4}{len(ids) - len(gap):>7}/{len(ids)}  {', '.join(gap[:6])}{' ...' if len(gap) > 6 else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
