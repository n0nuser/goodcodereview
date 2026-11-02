"""goodcodereview: read the public, static files of goodcodereview.com. No account, no key, one dependency-free module.

    goodcodereview levels
    goodcodereview cards [--level L] [--concern C] [--topic T] [--json]
    goodcodereview card ID
    goodcodereview prompt
    goodcodereview manifest
    goodcodereview install            # prints the install commands for the skills

--base points at another origin or a local folder (file:///path/to/site) for testing or a mirror.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

BASE = "https://goodcodereview.com"
UA = "goodcodereview-cli/0.1 (+https://goodcodereview.com/agent.json)"


def fetch(base: str, path: str) -> bytes:
    req = urllib.request.Request(f"{base.rstrip('/')}/{path.lstrip('/')}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310 - the scheme is http(s) or file, chosen by --base
        return r.read()


def cards(base: str, level: str = "", concern: str = "", topic: str = "") -> list[dict]:
    """Stable cards. A single level or concern is one static file; any combination is filtered here, so the host runs no code."""
    path = f"cards/{level}.json" if level and not concern else f"cards/concern-{concern}.json" if concern and not level else "cards.json"
    got = json.loads(fetch(base, path))["cards"]
    return [c for c in got if (not level or c["level"] == level) and (not concern or concern in c["concerns"]) and (not topic or topic in c["topics"])]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="goodcodereview", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base", default=BASE, help=f"origin to read (default {BASE})")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("levels", help="list the review levels")
    c = sub.add_parser("cards", help="list stable cards")
    for f in ("level", "concern", "topic"):
        c.add_argument(f"--{f}", default="")
    c.add_argument("--json", action="store_true", help="print JSON")
    one = sub.add_parser("card", help="print one card's rule and URL")
    one.add_argument("id")
    sub.add_parser("prompt", help="print the prompt that starts a review")
    sub.add_parser("manifest", help="print agent.json")
    sub.add_parser("install", help="print the install commands")
    a = p.parse_args(argv)
    try:
        if a.cmd == "levels":
            for lv in json.loads(fetch(a.base, "agent.json"))["levels"]:
                print(f"{lv['level']:<11} {lv['page']}")
        elif a.cmd == "cards":
            got = cards(a.base, a.level, a.concern, a.topic)
            if a.json:
                print(json.dumps(got, indent=2))
            else:
                for x in got:
                    print(f"{x['id']} [{x['severity']}] {{{', '.join(x['concerns'])}}}: {x['rule']}")
                print(f"{len(got)} cards", file=sys.stderr)
        elif a.cmd == "card":
            hit = [x for x in cards(a.base) if x["id"] == a.id]
            if not hit:
                print(f"no stable card '{a.id}'", file=sys.stderr)
                return 1
            print(json.dumps(hit[0], indent=2))
        elif a.cmd == "prompt":
            print(f"Read {BASE}/llms.txt and use it to review my code.")
        elif a.cmd == "manifest":
            sys.stdout.write(fetch(a.base, "agent.json").decode())
        else:
            m = json.loads(fetch(a.base, "agent.json"))["install"]
            print(f"{m['skill']}\n{m['plugin']}")
    except (urllib.error.URLError, OSError, ValueError, KeyError) as e:
        print(f"goodcodereview: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
