"""gcr-lint: run the lint rules that cards name, report findings by card, and say how much of the card set a run covers."""
import argparse
import json
import subprocess
import sys
from collections.abc import Sequence
from typing import Any

from goodcodereview_lint import __version__
from goodcodereview_lint.gates import Gate, by_code, load_gates, load_snapshot

SEVERITY_RANK = {"discuss": 1, "should-fix": 2, "block": 3}


def coverage_line(gates: list[Gate], snapshot: dict[str, Any], tool: str = "ruff") -> str:
    """The sentence every run ends with, so a clean result is never read as a finished review."""
    total = len(snapshot["cards"])
    covered = {g.card for g in gates if g.tool == tool}
    full = {g.card for g in gates if g.tool == tool and g.scope == "full"}
    return (f"{tool} rules here cover {len(covered)} of {total} stable cards ({len(full)} in full, {len(covered) - len(full)} in part). "
            f"The other {total - len(covered)} need a reviewer or another tool. A clean run is not a review.")


def ruff_command(select: Sequence[str], paths: Sequence[str]) -> list[str]:
    return [sys.executable, "-m", "ruff", "check", "--output-format", "json", "--no-cache", "--select", ",".join(select), *paths]


def findings(raw: list[dict[str, Any]], gates: list[Gate], snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    """Ruff findings as card findings: the first card for the code, the severity and backing from the snapshot."""
    mapping = by_code(gates)
    out = []
    for r in raw:
        cards = mapping.get(r["code"], [])
        if not cards:
            continue
        card = snapshot["cards"][cards[0].card]
        out.append({
            "path": r["filename"], "line": r["location"]["row"], "column": r["location"]["column"], "code": r["code"], "message": r["message"],
            "card": cards[0].card, "severity": card["severity"], "backing": card["backing"], "scope": cards[0].scope,
            "also": [g.card for g in cards[1:]], "url": card["url"],
        })
    return sorted(out, key=lambda f: (-SEVERITY_RANK[f["severity"]], f["path"], f["line"]))


def render(f: dict[str, Any]) -> str:
    also = f" also {', '.join(f['also'])}" if f["also"] else ""
    return (f"{f['path']}:{f['line']}:{f['column']}: [{f['severity']}] {f['card']} - {f['message']} "
            f"(ruff {f['code']}, {f['scope']} gate, backing {f['backing']}{also})")


def cmd_coverage(args: argparse.Namespace) -> int:
    gates, snapshot = load_gates(), load_snapshot()
    rows = sorted({(g.card, g.scope) for g in gates if g.tool == "ruff"} - {(g.card, "partial") for g in gates if g.scope == "full" and g.tool == "ruff"})
    if args.json:
        print(json.dumps({"snapshot": snapshot["generated"], "total": len(snapshot["cards"]), "covered": [{"card": c, "scope": s} for c, s in rows]}, indent=1))
        return 0
    print(f"Cards as of {snapshot['generated']}.")
    for card, scope in rows:
        info = snapshot["cards"][card]
        print(f"  {card} [{info['severity']}] {scope}: {info['rule']}")
    print(coverage_line(gates, snapshot))
    return 0


def cmd_config(_: argparse.Namespace) -> int:
    codes = sorted({g.code for g in load_gates() if g.tool == "ruff"})
    print("# Rules the Good Code Review cards name as gates. Paste into pyproject.toml.\n[tool.ruff.lint]\nextend-select = [" + ", ".join(f'"{c}"' for c in codes) + "]")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    gates, snapshot = load_gates(), load_snapshot()
    codes = sorted(by_code(gates))
    proc = subprocess.run(ruff_command(codes, args.paths or ["."]), capture_output=True, text=True, check=False)
    if proc.returncode not in (0, 1):
        print(proc.stderr.strip() or "ruff failed", file=sys.stderr)
        return 2
    found = findings(json.loads(proc.stdout or "[]"), gates, snapshot)
    if args.json:
        print(json.dumps({"findings": found, "coverage": coverage_line(gates, snapshot)}, indent=1))
    else:
        for f in found:
            print(render(f))
        print(f"{len(found)} finding{'s' * (len(found) != 1)}. {coverage_line(gates, snapshot)}")
    if args.fail_on == "never":
        return 0
    return int(any(SEVERITY_RANK[f["severity"]] >= SEVERITY_RANK[args.fail_on] for f in found))


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="gcr-lint", description=__doc__)
    p.add_argument("--version", action="version", version=f"gcr-lint {__version__}")
    sub = p.add_subparsers(dest="command", required=True)
    c = sub.add_parser("coverage", help="list the cards these rules cover and how many they leave out")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_coverage)
    sub.add_parser("config", help="print a ruff config that selects the rules the cards name").set_defaults(func=cmd_config)
    k = sub.add_parser("check", help="run the rules and report findings by card")
    k.add_argument("paths", nargs="*")
    k.add_argument("--json", action="store_true")
    k.add_argument("--fail-on", choices=["never", "discuss", "should-fix", "block"], default="should-fix", help="lowest severity that makes the exit code 1")
    k.set_defaults(func=cmd_check)
    args = p.parse_args(argv)
    code: int = args.func(args)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
