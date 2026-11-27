#!/usr/bin/env python3
"""Tell IndexNow search engines (Bing and others) which pages a deploy changed. Standard library only.

    python3 tools/indexnow.py OLD_SITE NEW_SITE [--dry-run]

OLD_SITE and NEW_SITE are two built site/ folders. A page counts as changed when its HTML differs once dates are removed, or when it appeared or
disappeared. Before it submits, it waits until the live site serves the new build.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from config import BASE, INDEXNOW_KEY

ENDPOINT = "https://api.indexnow.org/indexnow"
WAIT_SECONDS, STEP = 900, 30


def normalise(page: str) -> str:
    """The page without ISO dates, which change on every build."""
    return re.sub(r"\d{4}-\d{2}-\d{2}", "", page)


def pages(site: Path) -> dict[str, str]:
    """URL path to normalised HTML, for every page but the 404 page."""
    out = {}
    for f in site.rglob("*.html"):
        slug = f.relative_to(site).with_suffix("").as_posix()
        if slug != "404":
            out["" if slug == "index" else slug] = normalise(f.read_text())
    return out


def changed(old: dict[str, str], new: dict[str, str]) -> list[str]:
    return sorted(p for p in old.keys() | new.keys() if old.get(p) != new.get(p))


def live(path: str) -> str | None:
    request = urllib.request.Request(f"{BASE}/{path}", headers={"User-Agent": "goodcodereview-indexnow", "Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return normalise(response.read().decode("utf-8", "replace"))
    except urllib.error.URLError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("old", type=Path)
    ap.add_argument("new", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    new = pages(a.new)
    paths = changed(pages(a.old), new)
    if not paths:
        print("no page changed")
        return 0
    urls = [f"{BASE}/{p}" for p in paths]
    print("\n".join(urls))
    if a.dry_run:
        return 0
    probe = next((p for p in paths if p in new), None)
    deadline = time.monotonic() + WAIT_SECONDS
    while probe is not None and live(probe) != new[probe]:
        if time.monotonic() > deadline:
            print(f"the live site did not serve the new {probe!r} within {WAIT_SECONDS} s; nothing submitted", file=sys.stderr)
            return 1
        time.sleep(STEP)
    body = {"host": BASE.split("//")[1], "key": INDEXNOW_KEY, "keyLocation": f"{BASE}/{INDEXNOW_KEY}.txt", "urlList": urls}
    request = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(), headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(request, timeout=30) as response:  # an error status raises, which fails the job
        print(f"IndexNow answered {response.status} for {len(urls)} URLs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
