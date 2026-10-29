#!/usr/bin/env python3
"""Run and grade the skill evals in test/evals/cases.

    python3 tools/eval.py grade CASE OUTPUT_FILE [--mode skill|bare]
    python3 tools/eval.py run [--agent claude|opencode] [--mode skill|forced|bare|all] [--runs N] [--model M] [CASE ...]
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
skill. That adapter has not been run against a real opencode install; start with one case and `--runs 1`.

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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "test" / "evals" / "cases"
SKILL = ROOT / "skills" / "good-code-review"
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
FAIL_LINE = re.compile(r"^\s*(?:[-*]\s*)?(?:`)?FAIL\s*(?:\[([a-z-]+)\])?\s*(?:`)?\s*([a-z0-9-]+)?", re.M)


LEDGER_LINE = re.compile(r"^\s*(?:[-*]\s*)?`?(?:FAIL(?:\s*\[[a-z-]+\])?|PASS)\s+`?([a-z0-9-]+)", re.M)
_tags = {}


def stable_tags():
    """Concern tags of every stable card, by id."""
    if not _tags:
        sys.path.insert(0, str(ROOT / "tools"))
        import validate
        for _, fm, _ in validate.load_cards(ROOT):
            if fm["status"] == "stable":
                _tags[fm["id"]] = set(fm["tags"])
    return _tags


def grade(case, text, mode="skill"):
    """Return {"substance": [problems], "format": [problems]}. An empty list means that tier passed."""
    sub, fmt = [], []
    fails = [(m.group(1), m.group(2)) for m in FAIL_LINE.finditer(text)]
    for need in case.get("must_fail", []):
        if mode != "bare":
            if not any(i == need["id"] for _, i in fails):
                sub.append(f"no FAIL line for {need['id']}")
        elif not re.search(need["alt"], text):
            sub.append(f"reply does not mention {need['alt']}")
    for sev in case.get("must_not_fail_severity", []):
        if any(s == sev for s, _ in fails):
            sub.append(f"FAIL [{sev}] present")
    if case.get("scope") and mode != "bare":
        for m in LEDGER_LINE.finditer(text):
            tags = stable_tags().get(m.group(1))
            if tags is not None and not tags & set(case["scope"]):
                sub.append(f"{m.group(1)} is outside the scope {case['scope']}")
    for rx in case.get("must_contain", []):
        if not re.search(rx, text):
            sub.append(f"missing /{rx}/")
    for rx in case.get("must_not_contain", []):
        if m := re.search(rx, text):
            sub.append(f"forbidden /{rx}/ matched {m.group(0)!r}")
    if mode != "bare" and case.get("first_line"):
        first = next((l for l in text.splitlines() if l.strip()), "")
        if not re.search(case["first_line"], first.strip().lstrip("`*# ")):
            fmt.append(f"first line {first[:60]!r} does not match /{case['first_line']}/")
    return {"substance": sub, "format": fmt}


class HarnessError(Exception):
    """The CLI failed, which says nothing about the skill."""


def triggered(stream):
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


def trigger_run(query, model):
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copytree(SKILL, work / ".claude/skills/good-code-review")
        cmd = ["claude", "-p", query, "--allowedTools", "Read,Grep,Glob,Skill", "--output-format", "stream-json", "--verbose"]
        try:
            out = subprocess.run(cmd + (["--model", model] if model else []), cwd=work, capture_output=True, text=True, timeout=600)
        except FileNotFoundError:
            raise HarnessError("claude is not installed or not on PATH")
        except subprocess.TimeoutExpired:
            raise HarnessError("claude timed out after 600 s")
    if out.returncode or not out.stdout.strip():
        raise HarnessError(f"claude exited {out.returncode}: {out.stderr.strip()[:200]}")
    return triggered(out.stdout)


def load(name):
    return json.loads((CASES / name / "case.json").read_text())


def command(agent, prompt, model, mode):
    """The argv for one run, and where the agent looks for skills under the scratch copy."""
    if agent == "opencode":
        if mode == "forced":
            prompt = "Load and follow the good-code-review skill. " + prompt
        return ["opencode", "run", prompt] + (["--model", model] if model else []), ".opencode/skills"
    if mode == "forced":
        prompt = "/good-code-review " + prompt
    cmd = ["claude", "-p", prompt, "--allowedTools", "Read,Grep,Glob,Skill", "--output-format", "text"]
    return cmd + (["--model", model] if model else []), ".claude/skills"


def run_one(name, mode, model, agent="claude"):
    case = load(name)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for f in (CASES / name).iterdir():
            if f.name != "case.json":
                shutil.copy(f, work / f.name)
        cmd, skills = command(agent, case["prompt"], model, mode)
        if mode in ("skill", "forced"):
            shutil.copytree(SKILL, work / skills / "good-code-review")
        try:
            out = subprocess.run(cmd, cwd=work, capture_output=True, text=True, timeout=600)
        except FileNotFoundError:
            raise HarnessError(f"{name} {mode}: {cmd[0]} is not installed or not on PATH")
        except subprocess.TimeoutExpired:
            raise HarnessError(f"{name} {mode}: {cmd[0]} timed out after 600 s")
    if out.returncode or not out.stdout.strip():
        raise HarnessError(f"{name} {mode}: {cmd[0]} exited {out.returncode}: {out.stderr.strip()[:200]}")
    return ANSI.sub("", out.stdout)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("grade")
    g.add_argument("case")
    g.add_argument("output")
    g.add_argument("--mode", choices=["skill", "forced", "bare"], default="skill")
    r = sub.add_parser("run")
    r.add_argument("cases", nargs="*")
    r.add_argument("--mode", choices=["skill", "forced", "bare", "all"], default="all")
    r.add_argument("--runs", type=int, default=3)
    r.add_argument("--model")
    r.add_argument("--save", metavar="DIR", help="write each raw reply to DIR/<case>-<mode>-<n>.txt")
    r.add_argument("--agent", choices=["claude", "opencode"], default="claude")
    t = sub.add_parser("triggers")
    t.add_argument("--split", choices=["train", "validation", "all"], default="all")
    t.add_argument("--runs", type=int, default=3)
    t.add_argument("--model")
    a = ap.parse_args()
    if a.cmd == "triggers":
        queries = json.loads((CASES.parent / "triggers.json").read_text())["queries"]
        passed = {"train": [0, 0], "validation": [0, 0]}
        for q in queries:
            if a.split not in ("all", q["split"]):
                continue
            try:
                hits = sum(trigger_run(q["query"], a.model) for _ in range(a.runs))
            except HarnessError as e:
                sys.exit(f"harness error: {e}")
            rate = hits / a.runs
            ok = (rate > 0.5) == q["should_trigger"]
            passed[q["split"]][0] += ok
            passed[q["split"]][1] += 1
            print(f"{'ok  ' if ok else 'FAIL'} {q['split']:<11}{'want' if q['should_trigger'] else 'skip'} rate {rate:.2f}  {q['query'][:70]}")
        for k, (n, d) in passed.items():
            if d:
                print(f"{k}: {n}/{d} pass")
        return
    if a.cmd == "grade":
        res = grade(load(a.case), Path(a.output).read_text(), a.mode)
        print(json.dumps(res, indent=2))
        sys.exit(any(res.values()))
    names = a.cases or sorted(p.name for p in CASES.iterdir() if (p / "case.json").is_file())
    modes = ["skill", "forced", "bare"] if a.mode == "all" else [a.mode]
    print(f"{'case':<16}{'mode':<7}{'substance':>10}{'format':>8}")
    for n in names:
        for m in modes:
            try:
                res = []
                for i in range(a.runs):
                    reply = run_one(n, m, a.model, a.agent)
                    res.append(grade(load(n), reply, m))
                    if a.save:
                        Path(a.save).mkdir(parents=True, exist_ok=True)
                        (Path(a.save) / f"{n}-{m}-{i + 1}.txt").write_text(reply)
                    for tier, problems in res[-1].items():
                        for pr in problems:
                            print(f"    run {i + 1} {tier}: {pr}")
            except HarnessError as e:
                print(f"{n:<16}{m:<7} harness error: {e}")
                continue
            ok = lambda t: sum(not x[t] for x in res)
            print(f"{n:<16}{m:<7}{ok('substance'):>7}/{a.runs}{(str(ok('format')) + '/' + str(a.runs)) if m != 'bare' else '-':>8}")


if __name__ == "__main__":
    main()
