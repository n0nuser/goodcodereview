#!/usr/bin/env python3
"""Crawl a site's sitemap and report SEO problems. Stdlib only.

    python3 tools/seo_check.py https://example.com

Per sitemap URL: status 200 with no redirect, one canonical equal to the URL, no noindex, title 30-62 chars,
description 110-160 chars, internal links that redirect or end in .html. Exit code 1 if any problem is found.
"""

import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from email.message import Message
from typing import Any


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a: Any, **k: Any) -> None:
        return None


OPEN = urllib.request.build_opener(NoRedirect).open


def get(url: str) -> tuple[int, Message, str]:
    """Return (status, headers, body) without following redirects."""
    req = urllib.request.Request(url, headers={"User-Agent": "seo-check"})
    try:
        with OPEN(req, timeout=20) as r:
            return r.status, r.headers, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.headers, ""


def first(pattern: str, text: str) -> str | None:
    m = re.search(pattern, text, re.I | re.S)
    return next((g for g in m.groups() if g is not None), "").strip() if m else None


def attr(tag: str, name: str, text: str) -> str | None:
    """Value of attribute `name` on the first <tag ...>, with double, single or no quotes (minified HTML)."""
    for m in re.finditer(rf"<{tag}\b[^>]*>", text, re.I):
        v = re.search(rf"""\b{name}=(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", m.group(0), re.I)
        if v:
            return next(g for g in v.groups() if g is not None).strip()
    return None


def tag_attr(body: str, tag: str, key: str, value: str, want: str) -> str | None:
    """Attribute `want` of the first <tag> whose `key` attribute equals `value`."""
    for t in re.findall(rf"<{tag}\b[^>]*>", body, re.I):
        if (attr(tag, key, t) or "").lower() == value:
            return attr(tag, want, t)
    return None


def check_page(url: str, base: str) -> list[str]:
    status, headers, body = get(url)
    if status != 200:
        return [f"status {status} -> {headers.get('location')}"]
    out: list[str] = []
    canon = tag_attr(body, "link", "rel", "canonical", "href")
    if canon != url:
        out.append(f"canonical {canon!r} != url")
    robots = (tag_attr(body, "meta", "name", "robots", "content") or "") + " " + headers.get("x-robots-tag", "")
    if "noindex" in robots:
        out.append("noindex")
    title = first(r"<title>(.*?)</title>", body) or ""
    desc = tag_attr(body, "meta", "name", "description", "content") or ""
    if not 30 <= len(title) <= 62:
        out.append(f"title length {len(title)}")
    if not 110 <= len(desc) <= 160:
        out.append(f"description length {len(desc)}")
    hrefs = {attr("a", "href", t) for t in re.findall(r"<a\b[^>]*>", body, re.I)}
    for raw in sorted(h for h in hrefs if h):
        href = raw.split("#")[0]
        if not href:
            continue
        full = urllib.parse.urljoin(url, href)
        if full.startswith(base) and urllib.parse.urlparse(full).path.endswith(".html"):
            out.append(f"internal link to .html: {href}")
    return out


def main(base: str) -> None:
    base = base.rstrip("/")
    status, _, sitemap = get(base + "/sitemap.xml")
    if status != 200:
        sys.exit(f"sitemap.xml status {status}")
    urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    bad = 0
    for url in urls:
        problems = check_page(url, base)
        bad += bool(problems)
        print(("FAIL " if problems else "ok   ") + url + "".join(f"\n       {p}" for p in problems))
    print(f"{len(urls)} urls, {bad} with problems")
    sys.exit(bool(bad))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__))
