#!/usr/bin/env python3
"""Run and grade the skill evals in test/evals/cases.

    python3 tools/eval.py grade CASE OUTPUT_FILE [--mode skill|bare]
    python3 tools/eval.py run [--mode skill|bare|both] [--runs N] [--model M] [CASE ...]

`run` starts `claude -p` in a scratch copy of each case and grades the reply. Modes: `skill` installs the skill and leaves it
to the agent to invoke (measures triggering and adherence), `forced` installs it and starts the prompt with `/good-code-review`
(measures adherence alone), `bare` installs nothing. It spends tokens and needs the `claude` CLI, so CI runs only the grader's unit tests (test/test_eval.py).

A case.json holds:
  prompt            what the user asks
  first_line        regex for the first non-empty line of the reply (format; skill and forced modes)
  must_fail         [{"id", "alt"}]: skill mode needs a FAIL line naming the id; bare mode needs the `alt` regex anywhere
  must_not_fail_severity  severities that may not appear as `FAIL [sev]` (skill mode)
  must_contain / must_not_contain  regexes over the whole reply
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
FAIL_LINE = re.compile(r"^\s*(?:[-*]\s*)?(?:`)?FAIL\s*(?:\[([a-z-]+)\])?\s*(?:`)?\s*([a-z0-9-]+)?", re.M)


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


def load(name):
    return json.loads((CASES / name / "case.json").read_text())


def run_one(name, mode, model):
    case = load(name)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for f in (CASES / name).iterdir():
            if f.name != "case.json":
                shutil.copy(f, work / f.name)
        if mode in ("skill", "forced"):
            shutil.copytree(SKILL, work / ".claude" / "skills" / "good-code-review")
        prompt = ("/good-code-review " if mode == "forced" else "") + case["prompt"]
        cmd = ["claude", "-p", prompt, "--allowedTools", "Read,Grep,Glob,Skill", "--output-format", "text"]
        if model:
            cmd += ["--model", model]
        out = subprocess.run(cmd, cwd=work, capture_output=True, text=True, timeout=600)
    return out.stdout


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
    a = ap.parse_args()
    if a.cmd == "grade":
        res = grade(load(a.case), Path(a.output).read_text(), a.mode)
        print(json.dumps(res, indent=2))
        sys.exit(any(res.values()))
    names = a.cases or sorted(p.name for p in CASES.iterdir() if (p / "case.json").is_file())
    modes = ["skill", "forced", "bare"] if a.mode == "all" else [a.mode]
    print(f"{'case':<16}{'mode':<7}{'substance':>10}{'format':>8}")
    for n in names:
        for m in modes:
            res = [grade(load(n), run_one(n, m, a.model), m) for _ in range(a.runs)]
            ok = lambda t: sum(not x[t] for x in res)
            print(f"{n:<16}{m:<7}{ok('substance'):>7}/{a.runs}{(str(ok('format')) + '/' + str(a.runs)) if m != 'bare' else '-':>8}")


if __name__ == "__main__":
    main()
