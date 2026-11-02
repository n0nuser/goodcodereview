#!/usr/bin/env python3
"""Validate, then emit site/ and skills/good-code-review/. Run from anywhere.

    python3 tools/build.py [--dry-run]

--dry-run builds everything in memory, runs every check and budget, prints what it would remove and write, and writes nothing.
A real run writes the new site and skill into temporary folders first and swaps them in only after every check has passed,
so a failed budget never leaves skills/ half regenerated.
"""
import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from config import ROOT, SITE, SKILL, TOOLS
from context import BuildInput, build_date, read_input
from errors import ToolError
from site_cards import cards_files
from site_meta import agent_files, headers_file, page_slugs, robots, security_txt, sitemap, skill_discovery
from site_pages import html_pages
from site_twins import markdown_twins
from skill_files import SkillOutput, skill_output
from skills_extra import extra_files

Files = dict[str, bytes]  # path relative to the output folder -> content


@dataclass(frozen=True, slots=True)
class Plan:
    """Everything one build produces: the site and skill files, ready to write, and the summary line."""

    site: Files
    skill: Files
    summary: str
    extra: Files  # skills/<name>/SKILL.md for the focused skills


def _encode(texts: dict[str, str]) -> Files:
    return {name: text.encode() for name, text in texts.items()}


def site_files(b: BuildInput, skill: SkillOutput) -> Files:
    """Every file of site/, from the pages and twins to the discovery files."""
    slugs = page_slugs(b)
    texts: dict[str, str] = {}
    texts.update(html_pages(b))
    texts.update(markdown_twins(b, skill))
    texts["llms.txt"] = skill.llms
    texts["llms-drafts.txt"] = skill.llms_drafts
    texts["sitemap.xml"] = sitemap(slugs, b.date)
    texts["robots.txt"] = robots()
    texts["_headers"] = headers_file(slugs)
    texts[".well-known/security.txt"] = security_txt(b.date)
    texts.update(cards_files(b))
    texts.update(skill_discovery(skill.files))
    texts.update(agent_files(b))
    files = _encode(texts)
    files["og.png"] = (TOOLS / "og.png").read_bytes()
    return files


def plan_build(root: Path) -> Plan:
    """Read the cards and produce every output in memory. Raises ToolError before anything is written."""
    b = read_input(root, build_date())
    skill = skill_output(b)
    site = site_files(b, skill)
    pages = len(page_slugs(b)) + 1
    skill_lines = skill.files["SKILL.md"].count("\n") + 1
    summary = (f"site: {pages} pages; SKILL.md: {skill_lines} lines; stable cards: {len(b.stable)}; "
               f"llms.txt: {len(skill.llms)} chars; lastmod: {b.date}")
    return Plan(site, _encode(skill.files), summary, _encode(extra_files()))


def _write_tree(base: Path, files: Files) -> None:
    for name, data in files.items():
        target = base / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def _stale(base: Path, files: Files) -> list[str]:
    """Files under base/references that the new skill no longer has."""
    return sorted(str(p.relative_to(base)) for p in (base / "references").glob("*.md") if str(p.relative_to(base)) not in files)


def swap_site(files: Files, site: Path = SITE) -> None:
    """Write the new site next to the old one, then replace it, so a failed write leaves the old site whole."""
    staged, previous = site.with_name(site.name + ".new"), site.with_name(site.name + ".old")
    shutil.rmtree(staged, ignore_errors=True)
    shutil.rmtree(previous, ignore_errors=True)
    _write_tree(staged, files)
    if site.exists():
        site.rename(previous)
    staged.rename(site)
    shutil.rmtree(previous, ignore_errors=True)


def write_skill(files: Files, skill: Path = SKILL) -> None:
    """Replace SKILL.md and references/*.md. The files are in memory and checked, so only disk errors can fail now."""
    for name in _stale(skill, files):
        (skill / name).unlink()
    _write_tree(skill, files)


def write_extra(files: Files, skills: Path = SKILL.parent) -> None:
    """Write skills/<name>/SKILL.md for each focused skill."""
    _write_tree(skills, files)


def describe(plan: Plan, site: Path = SITE, skill: Path = SKILL) -> str:
    """The dry-run report: what would be removed and what would be written."""
    old_site = sum(1 for p in site.rglob("*") if p.is_file()) if site.exists() else 0
    lines = [f"would remove: {site} ({old_site} files)"]
    lines += [f"would remove: {skill / name}" for name in _stale(skill, plan.skill)]
    lines += [f"would write: {len(plan.extra)} focused skills under {skill.parent}", f"would write: {len(plan.site)} files under {site}", f"would write: {len(plan.skill)} files under {skill}"]
    lines += [f"  {skill / name}" for name in sorted(plan.skill)]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="run every check and print what would change; write nothing")
    args = parser.parse_args(argv)
    try:
        plan = plan_build(ROOT)
    except ToolError as e:
        print(e)
        return 1
    if args.dry_run:
        print(describe(plan))
        print(plan.summary)
        return 0
    write_skill(plan.skill)
    write_extra(plan.extra)
    swap_site(plan.site)
    print(plan.summary)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
