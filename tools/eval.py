#!/usr/bin/env python3
"""Run and grade the skill evals in test/evals/cases.

    python3 tools/eval.py grade CASE OUTPUT_FILE [--mode skill|bare]
    python3 tools/eval.py run [--agent claude|opencode|codex|cursor] [--mode skill|forced|bare|all] [--runs N] [--model M] [CASE ...]
    python3 tools/eval.py triggers [--split train|validation|all] [--runs N] [--model M]

`run` starts `claude -p` in a scratch copy of each case and grades the reply. Modes: `skill` installs the skill and leaves it
to the agent to invoke (measures triggering and adherence), `forced` installs it and starts the prompt with `/good-code-review`
(measures adherence alone), `bare` installs nothing. It spends tokens and needs the `claude` CLI, so CI runs only the grader's unit tests (test/test_eval.py).

A case.json holds:
  prompt            what the user asks
  first_line        regex for the first non-empty line of the reply (format; skill and forced modes)
  must_fail         [{"id", "alt"}]: skill mode needs a FAIL line naming the id; bare mode needs the `alt` regex anywhere
  must_not_fail_severity  severities that may not appear as `FAIL [sev]` (skill mode)
  scope             concerns the review is limited to: a FAIL or PASS line for a card with none of them is a problem
  must_contain / must_not_contain  regexes over the whole reply
`--agent opencode` drives `opencode run` instead (model as `provider/model`, such as `opencode-go/deepseek-v4.1-flash`), with the skill
copied to `.opencode/skills/`. In forced mode, which has no slash command there, the prompt starts with an instruction to load the
skill. `--agent codex` drives `codex exec` (skills in `.agents/skills`, forced mode starts with `$good-code-review`), and `--agent cursor` drives `agent -p`
(skills in `.agents/skills`). None of the three adapters has been run against a real install, and Cursor's docs do not say that its CLI loads skills; start with one case and `--runs 1`.

`triggers --focused` also installs the other skills under `skills/`, so a drop in the main skill's rate shows the focused skills taking its queries.
`triggers --isolate` adds `--setting-sources project`, so only the skill under test is loaded: it measures the description without the user's other skills competing.
`triggers` runs the queries in test/evals/triggers.json with the skill installed and reports how often the agent loaded it
(`claude -p --output-format stream-json`; the skill counts as loaded on a `Skill` call for it or a read of its SKILL.md). A query passes when
its trigger rate is above 0.5 for a should-trigger query and at or below 0.5 for the rest. Tune the description on `train`, confirm on `validation`.

Each result has two tiers: `substance` (did it find what a reviewer must find) and `format` (did it follow the report format).
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

import validate
from config import ROOT, SKILL
from errors import HarnessError

CASES = ROOT / "test" / "evals" / "cases"
TRIGGERS = ROOT / "test" / "evals" / "triggers.json"
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
FAIL_LINE = re.compile(r"^\s*(?:[-*]\s*)?(?:`)?FAIL\s*(?:\[([a-z-]+)\])?\s*(?:`)?\s*([a-z0-9-]+)?", re.M)
LEDGER_LINE = re.compile(r"^\s*(?:[-*]\s*)?`?(?:FAIL(?:\s*\[[a-z-]+\])?|PASS)\s+`?([a-z0-9-]+)", re.M)
RUN_TIMEOUT_S = 600
TRIGGER_MIN_RATE = 0.5  # a query "triggers" when the skill loads in more than this share of runs
ERROR_PREVIEW = 200  # characters of CLI stderr shown in a harness error
FIRST_LINE_PREVIEW = 60
QUERY_PREVIEW = 70
ALLOWED_TOOLS = "Read,Grep,Glob,Skill"

Case = dict[str, Any]
Problems = dict[str, list[str]]


class Mode(StrEnum):
    SKILL = "skill"
    FORCED = "forced"
    BARE = "bare"
    ALL = "all"


class Agent(StrEnum):
    CLAUDE = "claude"
    OPENCODE = "opencode"
    CODEX = "codex"
    CURSOR = "cursor"


class Split(StrEnum):
    TRAIN = "train"
    VALIDATION = "validation"
    ALL = "all"


@dataclass(frozen=True, slots=True)
class Command:
    """The argv for one run, and where the agent looks for skills under the scratch copy."""

    argv: list[str]
    skills_dir: str


def stable_tags(root: Path = ROOT) -> dict[str, set[str]]:
    """Concern tags of every stable card, by id."""
    return {c.fm["id"]: set(c.fm["tags"]) for c in validate.load_cards(root) if c.fm["status"] == "stable"}


def grade(case: Case, text: str, mode: Mode = Mode.SKILL, *, tags: dict[str, set[str]] | None = None) -> Problems:
    """Return {"substance": [problems], "format": [problems]}. An empty list means that tier passed.

    `tags` maps a stable card id to its concern tags; it defaults to the cards in the repository.
    """
    sub: list[str] = []
    fmt: list[str] = []
    fails = [(m.group(1), m.group(2)) for m in FAIL_LINE.finditer(text)]
    for need in case.get("must_fail", []):
        if mode != Mode.BARE:
            if not any(i == need["id"] for _, i in fails):
                sub.append(f"no FAIL line for {need['id']}")
        elif not re.search(need["alt"], text):
            sub.append(f"reply does not mention {need['alt']}")
    for sev in case.get("must_not_fail_severity", []):
        if any(s == sev for s, _ in fails):
            sub.append(f"FAIL [{sev}] present")
    if case.get("scope") and mode != Mode.BARE:
        known = stable_tags() if tags is None else tags
        for m in LEDGER_LINE.finditer(text):
            card_tags = known.get(m.group(1))
            if card_tags is not None and not card_tags & set(case["scope"]):
                sub.append(f"{m.group(1)} is outside the scope {case['scope']}")
    for rx in case.get("must_contain", []):
        if not re.search(rx, text):
            sub.append(f"missing /{rx}/")
    for rx in case.get("must_not_contain", []):
        if hit := re.search(rx, text):
            sub.append(f"forbidden /{rx}/ matched {hit.group(0)!r}")
    if mode != Mode.BARE and case.get("first_line"):
        first = next((line for line in text.splitlines() if line.strip()), "")
        if not re.search(case["first_line"], first.strip().lstrip("`*# ")):
            fmt.append(f"first line {first[:FIRST_LINE_PREVIEW]!r} does not match /{case['first_line']}/")
    return {"substance": sub, "format": fmt}


def triggered(stream: str) -> bool:
    """True if a stream-json transcript shows the agent loading the skill: a Skill call for it, or a read of its SKILL.md."""
    for raw in stream.splitlines():
        try:
            ev = json.loads(raw)
        except ValueError:
            continue
        content = (ev.get("message") or {}).get("content") if ev.get("type") == "assistant" else None
        for block in content if isinstance(content, list) else []:
            if block.get("type") != "tool_use":
                continue
            inp = block.get("input") or {}
            if block.get("name") == "Skill" and inp.get("skill", "").endswith("good-code-review"):
                return True
            if block.get("name") == "Read" and "good-code-review/SKILL.md" in inp.get("file_path", ""):
                return True
    return False


def _run_cli(cmd: list[str], cwd: Path, label: str) -> str:
    """Run a CLI and return its stdout. Raises HarnessError when it is missing, times out, or exits non-zero."""
    try:
        out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=RUN_TIMEOUT_S, check=False)
    except FileNotFoundError as e:
        raise HarnessError(f"{label}{cmd[0]} is not installed or not on PATH") from e
    except subprocess.TimeoutExpired as e:
        raise HarnessError(f"{label}{cmd[0]} timed out after {RUN_TIMEOUT_S} s") from e
    if out.returncode or not out.stdout.strip():
        raise HarnessError(f"{label}{cmd[0]} exited {out.returncode}: {out.stderr.strip()[:ERROR_PREVIEW]}")
    return out.stdout


def trigger_run(query: str, model: str | None, *, isolate: bool = False, focused: bool = False) -> bool:
    """Run one query with the skill installed and say whether the agent loaded it."""
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copytree(SKILL, work / ".claude/skills/good-code-review")
        if focused:  # also install the focused skills, to see whether they take the main skill's queries
            for other in sorted(SKILL.parent.iterdir()):
                if other != SKILL and (other / "SKILL.md").is_file():
                    shutil.copytree(other, work / ".claude/skills" / other.name)
        cmd = ["claude", "-p", query, "--allowedTools", ALLOWED_TOOLS, "--output-format", "stream-json", "--verbose"]
        if isolate:  # no user-level skills or plugins compete with the skill under test
            cmd += ["--setting-sources", "project"]
        stdout = _run_cli(cmd + (["--model", model] if model else []), work, "")
    return triggered(stdout)


def load(name: str) -> Case:
    case: Case = json.loads((CASES / name / "case.json").read_text())
    return case


def command(agent: Agent, prompt: str, model: str | None, mode: Mode) -> Command:
    """The argv for one run, and where the agent looks for skills under the scratch copy."""
    forced = "Load and follow the good-code-review skill. " + prompt
    if agent == Agent.OPENCODE:
        return Command(["opencode", "run", forced if mode == Mode.FORCED else prompt] + (["--model", model] if model else []), ".opencode/skills")
    if agent == Agent.CODEX:  # read-only sandbox is the default; the scratch dir is not a git repo
        argv = ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only"] + (["--model", model] if model else [])
        return Command(argv + ["$good-code-review " + prompt if mode == Mode.FORCED else prompt], ".agents/skills")
    if agent == Agent.CURSOR:  # no --force: the review only reads
        argv = ["agent", "-p", "--trust", "--output-format", "text"] + (["--model", model] if model else [])
        return Command(argv + [forced if mode == Mode.FORCED else prompt], ".agents/skills")
    if mode == Mode.FORCED:
        prompt = "/good-code-review " + prompt
    cmd = ["claude", "-p", prompt, "--allowedTools", ALLOWED_TOOLS, "--output-format", "text"]
    return Command(cmd + (["--model", model] if model else []), ".claude/skills")


def run_one(name: str, mode: Mode, model: str | None, agent: Agent = Agent.CLAUDE) -> str:
    """Run one case in a scratch copy and return the reply with terminal colour codes removed."""
    case = load(name)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for f in (CASES / name).iterdir():
            if f.name != "case.json":
                shutil.copy(f, work / f.name)
        cmd = command(agent, case["prompt"], model, mode)
        if mode in (Mode.SKILL, Mode.FORCED):
            shutil.copytree(SKILL, work / cmd.skills_dir / "good-code-review")
        stdout = _run_cli(cmd.argv, work, f"{name} {mode}: ")
    return ANSI.sub("", stdout)


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("grade")
    g.add_argument("case")
    g.add_argument("output")
    g.add_argument("--mode", type=Mode, choices=[Mode.SKILL, Mode.FORCED, Mode.BARE], default=Mode.SKILL)
    r = sub.add_parser("run")
    r.add_argument("cases", nargs="*")
    r.add_argument("--mode", type=Mode, choices=list(Mode), default=Mode.ALL)
    r.add_argument("--runs", type=int, default=3)
    r.add_argument("--model")
    r.add_argument("--save", metavar="DIR", help="write each raw reply to DIR/<case>-<mode>-<n>.txt")
    r.add_argument("--agent", type=Agent, choices=list(Agent), default=Agent.CLAUDE)
    t = sub.add_parser("triggers")
    t.add_argument("--split", type=Split, choices=list(Split), default=Split.ALL)
    t.add_argument("--runs", type=int, default=3)
    t.add_argument("--model")
    t.add_argument("--focused", action="store_true", help="also install the focused skills under skills/, to measure whether they take the main skill's queries")
    t.add_argument("--isolate", action="store_true", help="load only the project's skills, so the description is measured without the user's other skills competing")
    return ap


def _triggers(split: Split, runs: int, model: str | None, *, isolate: bool, focused: bool = False) -> int:
    queries = json.loads(TRIGGERS.read_text())["queries"]
    passed = {"train": [0, 0], "validation": [0, 0]}
    for q in queries:
        if split not in (Split.ALL, q["split"]):
            continue
        try:
            hits = sum(trigger_run(q["query"], model, isolate=isolate, focused=focused) for _ in range(runs))
        except HarnessError as e:
            print(f"harness error: {e}")
            return 1
        rate = hits / runs
        ok = (rate > TRIGGER_MIN_RATE) == q["should_trigger"]
        passed[q["split"]][0] += ok
        passed[q["split"]][1] += 1
        print(f"{'ok  ' if ok else 'FAIL'} {q['split']:<11}{'want' if q['should_trigger'] else 'skip'} rate {rate:.2f}  {q['query'][:QUERY_PREVIEW]}")
    for k, (n, d) in passed.items():
        if d:
            print(f"{k}: {n}/{d} pass")
    return 0


def _run_cases(names: Sequence[str], modes: Sequence[Mode], runs: int, model: str | None, agent: Agent, save: str | None) -> int:
    print(f"{'case':<16}{'mode':<7}{'substance':>10}{'format':>8}")
    failed = False  # a harness error, or a missed substance check in a mode that has the skill (bare is the baseline and may miss)
    for n in names:
        for m in modes:
            try:
                res: list[Problems] = []
                for i in range(runs):
                    reply = run_one(n, m, model, agent)
                    res.append(grade(load(n), reply, m))
                    if save:
                        Path(save).mkdir(parents=True, exist_ok=True)
                        (Path(save) / f"{n}-{m}-{i + 1}.txt").write_text(reply)
                    for tier, problems in res[-1].items():
                        for pr in problems:
                            print(f"    run {i + 1} {tier}: {pr}")
            except HarnessError as e:
                print(f"{n:<16}{m:<7} harness error: {e}", file=sys.stderr)
                failed = True
                continue
            substance = sum(not x["substance"] for x in res)
            fmt = sum(not x["format"] for x in res)
            failed |= m != Mode.BARE and substance < runs
            print(f"{n:<16}{m:<7}{substance:>7}/{runs}{(str(fmt) + '/' + str(runs)) if m != Mode.BARE else '-':>8}")
    return 1 if failed else 0


def main(argv: Sequence[str]) -> int:
    a = _parser().parse_args(argv)
    if a.cmd == "triggers":
        return _triggers(a.split, a.runs, a.model, isolate=a.isolate, focused=a.focused)
    if a.cmd == "grade":
        res = grade(load(a.case), Path(a.output).read_text(), a.mode)
        print(json.dumps(res, indent=2))
        return int(any(res.values()))
    names = a.cases or sorted(p.name for p in CASES.iterdir() if (p / "case.json").is_file())
    modes = [Mode.SKILL, Mode.FORCED, Mode.BARE] if a.mode == Mode.ALL else [a.mode]
    return _run_cases(names, modes, a.runs, a.model, a.agent, a.save)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
