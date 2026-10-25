#!/usr/bin/env python3
"""Check site/ against the agent-readiness items in docs/research/agent-readiness-gaps.md. Run tools/build.py first.
No network: it reads files only. Prints one PASS or FAIL line per check, names the checklist item, and exits 1 on any FAIL."""
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BASE = "https://goodcodereview.com"
LLMS_MAX = 30_000
PAGE_MAX = 100_000
FAILS = []


def check(item, ok, msg):
    print(f"{'PASS' if ok else 'FAIL'}  item {item}: {msg}")
    if not ok:
        FAILS.append(item)


class Page(HTMLParser):
    """Collects what the checks read: text, headings, head tags, links, and landmark tags."""

    def __init__(self, src):
        super().__init__()
        self.text, self.heads, self.metas, self.links, self.hrefs, self.tags = [], [], [], [], [], set()
        self.ld, self.js, self.css, self.scripts, self.title, self._skip, self._in = [], [], [], [], "", 0, ""
        self.feed(src)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.add(tag)
        if tag in ("script", "style"):
            self._skip += 1
            self._in = tag + (":ld" if a.get("type") == "application/ld+json" else ":js" if "src" not in a else ":ext")
            if self._in == "script:ext":
                self.scripts.append(a)
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        elif tag == "title":
            self._in = "title"
        elif re.fullmatch(r"h[1-6]", tag):
            self.heads.append(int(tag[1]))

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1
        if tag in ("script", "style", "title"):
            self._in = ""

    def handle_data(self, data):
        if self._in == "script:ld":
            self.ld.append(data)
        elif self._in == "script:js":
            self.js.append(data)
        elif self._in == "style:js":
            self.css.append(data)
        elif self._in == "title":
            self.title += data
        elif not self._skip:
            self.text.append(data)

    def chars(self):
        return len(re.sub(r"\s+", " ", " ".join(self.text)).strip())

    def meta(self, key, val):
        return [m.get("content", "") for m in self.metas if m.get(key) == val]

    def link(self, rel):
        return [l for l in self.links if l.get("rel") == rel]


def resolve(url):
    """Map a goodcodereview.com URL to the file the host serves, or None. Cloudflare Pages drops .html from page URLs."""
    p = urlparse(url).path
    if p in ("", "/"):
        return SITE / "index.html"
    f = SITE / p.lstrip("/")
    return f if f.is_file() else (SITE / (p.lstrip("/") + ".html") if (SITE / (p.lstrip("/") + ".html")).is_file() else None)


def parse_headers(text):
    """Parse a Cloudflare Pages _headers file: unindented URL lines, then indented `Name: value` lines. Return (rules, errors)."""
    rules, errs, cur = {}, [], None
    for n, line in enumerate(text.split("\n"), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if len(line) > 2000:
            errs.append(f"line {n} is over 2,000 characters")
        if line[0] not in " \t":
            cur = rules.setdefault(line.strip(), [])
        elif cur is None:
            errs.append(f"line {n}: header before any URL")
        elif not re.fullmatch(r"\s+!?\s*[A-Za-z0-9-]+(:\s*.+)?", line):
            errs.append(f"line {n}: not `Name: value`")
        else:
            cur.append(line.strip())
    return rules, errs


def main():
    if not (SITE / "index.html").is_file():
        sys.exit("site/ is empty. Run python3 tools/build.py first.")
    pages = {f.name: Page(f.read_text()) for f in sorted(SITE.glob("*.html"))}
    content = {n: p for n, p in pages.items() if n != "404.html"}

    # 1, 12, 30: content in the raw HTML, landmarks, heading order
    idx = pages["index.html"]
    check(1, idx.heads.count(1) == 1 and idx.chars() >= 500, f"index.html has one h1 and {idx.chars()} characters of text without JavaScript")
    bad = [n for n, p in pages.items() if p.heads.count(1) != 1 or any(b > a + 1 for a, b in zip(p.heads, p.heads[1:]))
           or not {"header", "nav", "main", "footer"} <= p.tags]
    check(30, not bad, f"every page has header, nav, main, footer, one h1, and no skipped heading level{': ' + ', '.join(bad) if bad else ''}")

    # 2, 3, 4: robots.txt
    robots = (SITE / "robots.txt").read_text()
    groups = re.findall(r"(?im)^user-agent:\s*(.+)$", robots)
    check(2, groups == ["*"] and not re.search(r"(?im)^disallow:\s*\S", robots), "robots.txt has one `User-agent: *` group and no Disallow rule")
    check(3, groups == ["*"] and re.search(r"(?im)^allow:\s*/\s*$", robots) is not None, "robots.txt allows everything and names no crawler")
    check(4, f"Sitemap: {BASE}/sitemap.xml" in robots, "robots.txt has a Sitemap line")

    # 5, 6: sitemap
    try:
        root = ET.fromstring((SITE / "sitemap.xml").read_text())
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [u.findtext("s:loc", "", ns) for u in root.findall("s:url", ns)]
        mods = [u.findtext("s:lastmod", "", ns) for u in root.findall("s:url", ns)]
    except (OSError, ET.ParseError) as e:
        locs, mods = [], []
        print(f"      sitemap.xml unreadable: {e}")
    served = {resolve(l) for l in locs}
    missing = [n for n in content if SITE / n not in served]
    check(5, locs and not missing and None not in served, f"sitemap.xml lists {len(locs)} URLs, one per HTML page except 404.html{': missing ' + ', '.join(missing) if missing else ''}")
    try:
        ok = mods and all(date.fromisoformat(m) <= date.today() for m in mods)
    except ValueError:
        ok = False
    check(6, bool(ok), f"every sitemap URL has a lastmod date ({mods[0] if mods else 'none'})")

    # 7, 8, 9: error page, redirects
    nf = pages["404.html"]
    check(9, nf.chars() >= 20 and len(nf.hrefs) >= 5, f"404.html has {nf.chars()} characters of text and {len(nf.hrefs)} links")
    check(8, not (SITE / "_redirects").exists() and not any(m.get("http-equiv") == "refresh" for p in pages.values() for m in p.metas),
          "no _redirects file and no meta-refresh stubs")

    # 15, 16, 17, 19: llms.txt
    llms = (SITE / "llms.txt").read_text()
    check(16, 100 <= len(llms) < LLMS_MAX and re.match(r"# \S", llms) and re.search(r"(?m)^> \S", llms) and re.search(r"(?m)^## \S", llms),
          f"llms.txt is {len(llms)} characters (limit {LLMS_MAX}) with an H1, a blockquote summary, and H2 sections")
    own = [u.rstrip(".,)") for u in re.findall(r"\]\((https?://[^)\s]+)\)", llms) if urlparse(u).netloc == "goodcodereview.com"]
    dead = [u for u in own if resolve(u) is None]
    check(17, own and not dead, f"{len(own)} own-site links in llms.txt resolve to files in site/{': dead ' + ', '.join(dead) if dead else ''}")
    check(19, re.search(r"(?m)^## When to use", llms) is not None, "llms.txt has a `When to use` section")
    unbalanced = [f.name for f in [*SITE.glob("*.md"), SITE / "llms.txt", SITE / "llms-drafts.txt"] if len(re.findall(r"(?m)^```", f.read_text())) % 2]
    check(15, not unbalanced and all('<code class="language-' in (SITE / f"{lv}.html").read_text() for lv in ("change", "function")),
          f"code fences are balanced in served Markdown and tagged with a language class in HTML{': ' + ', '.join(unbalanced) if unbalanced else ''}")

    # 14, 29, 37, 42: head tags
    problems = []
    for n, p in content.items():
        slug = n[:-5]
        want = BASE + "/" if slug == "index" else f"{BASE}/{slug}"
        canon = [l["href"] for l in p.link("canonical")]
        og = {m.get("property"): m.get("content", "") for m in p.metas if str(m.get("property", "")).startswith("og:")}
        if canon != [want]:
            problems.append(f"{n}: canonical {canon}")
        if not (p.meta("name", "description") or [""])[0]:
            problems.append(f"{n}: description")
        if not all(og.get(k) for k in ("og:title", "og:description", "og:type", "og:url", "og:site_name", "og:image")):
            problems.append(f"{n}: og tags")
        if p.meta("name", "is-agentic-site-type") != ["content"]:
            problems.append(f"{n}: is-agentic-site-type")
        if "Good Code Review" not in p.title or p.title.strip() == "":
            problems.append(f"{n}: title")
    check(14, not any("canonical" in x for x in problems), "every page has one canonical URL, the extensionless URL in the sitemap")
    check(29, not any(k in x for x in problems for k in ("description", "og tags")) and all(re.search(r'<html lang="en"', f.read_text()) for f in SITE.glob("*.html")),
          "every page has lang, description, and the Open Graph tags, including og:image")
    check(29, (SITE / "og.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", "og.png is a PNG file")
    check(37, not any("title" in x for x in problems), "every page title names Good Code Review")
    check(42, not any("is-agentic-site-type" in x for x in problems), 'every page has <meta name="is-agentic-site-type" content="content">')

    # 20, 38: discovery links in footer and head
    foot = ["llms.txt", "sitemap.xml", "about.html", "privacy.html", "/AGENTS.md", "/skills/good-code-review", "/issues"]
    gaps = [n for n, p in pages.items() if not all(any(h.endswith(f) for h in p.hrefs) for f in foot)]
    check(20, not gaps, f"footer links About, Privacy, Contact, llms.txt, sitemap, AGENTS.md, and the skill folder on every page{': ' + ', '.join(gaps) if gaps else ''}")
    head_gaps = [n for n, p in content.items() if not (p.link("sitemap") and any(l.get("href") == "/llms.txt" for l in p.link("alternate")))]
    check(20, not head_gaps, f"head links the sitemap and llms.txt on every content page{': ' + ', '.join(head_gaps) if head_gaps else ''}")

    # 22, 23: Markdown twins and frontmatter
    twin_gaps, fm_gaps = [], []
    for n, p in content.items():
        slug = n[:-5]
        alt = [l["href"] for l in p.link("alternate") if l.get("type") == "text/markdown"]
        if alt != [f"/{slug}.md"] or not (SITE / f"{slug}.md").is_file():
            twin_gaps.append(n)
    for f in sorted(SITE.glob("*.md")):
        m = re.match(r"---\n(.*?)\n---\n", f.read_text(), re.S)
        keys = {l.split(":", 1)[0] for l in m.group(1).split("\n")} if m else set()
        if not {"title", "description", "canonical", "updated"} <= keys:
            fm_gaps.append(f.name)
    check(22, not twin_gaps, f"every content page has a Markdown twin and a rel=alternate link to it{': ' + ', '.join(twin_gaps) if twin_gaps else ''}")
    check(23, not fm_gaps, f"every served .md starts with frontmatter (title, description, canonical, updated){': ' + ', '.join(fm_gaps) if fm_gaps else ''}")

    # 21, 33: _headers
    rules, errs = parse_headers((SITE / "_headers").read_text())
    flat = " ".join(" ".join(v) for v in rules.values())
    check(21, not errs and len(rules) <= 100 and "rel=\"sitemap\"" in flat and "rel=\"alternate\"; type=\"text/markdown\"" in flat
          and "/*.md" in rules and "charset=utf-8" in " ".join(rules.get("/*.md", [])) and "charset=utf-8" in " ".join(rules.get("/*.txt", [])),
          f"_headers parses ({len(rules)} rules): Link for sitemap and Markdown twins, charset for .md and .txt{'; ' + '; '.join(errs) if errs else ''}")
    check(33, "x-robots-tag" not in flat.lower() and not any(m.get("name") == "robots" and "noindex" in m.get("content", "") for p in pages.values() for m in p.metas),
          "no noindex meta tag and no X-Robots-Tag header")

    # 25, 28: JSON-LD
    try:
        ld = json.loads("".join(idx.ld))
        types = {n.get("@type") for n in ld.get("@graph", [])}
        ok = {"WebSite", "CreativeWork"} <= types and all(n.get(k) for n in ld["@graph"] for k in ("name", "description", "url"))
    except (ValueError, AttributeError):
        ok, types = False, set()
    check(25, ok, f"index.html JSON-LD parses; types {sorted(types)}; each has name, description, url")
    check(28, ok and types <= {"WebSite", "CreativeWork"}, "JSON-LD types match visible content (WebSite, CreativeWork only)")

    # 34: trust pages, and the privacy claim
    for n in ("about.html", "privacy.html"):
        check(34, pages[n].chars() >= 500, f"{n} has {pages[n].chars()} characters of text (at least 500)")
    code = "".join(x for p in pages.values() for x in p.js)
    css = "".join(x for p in pages.values() for x in p.css)
    leaks = [t for t in ("document.cookie", "localStorage", "sessionStorage", "fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket") if t in code]
    leaks += [t for t in ("@import", "http") if t in css] + [f"<{t}>" for p in pages.values() for t in ("img", "iframe", "form", "input", "video", "audio") if t in p.tags]
    ext = [x for p in pages.values() for x in p.scripts] + [l for p in pages.values() for l in p.links if l.get("rel") in ("stylesheet", "preload", "preconnect")]
    check(34, not leaks and not ext, f"page scripts and styles use no cookie, storage, or network call, and no page loads external or form content, as privacy.html says{': found ' + ', '.join(leaks) if leaks else ''}")

    # 36: page size
    big = {n: p.chars() for n, p in pages.items() if p.chars() >= PAGE_MAX}
    top = max(pages.items(), key=lambda kv: kv[1].chars())
    check(36, not big, f"every page is under {PAGE_MAX:,} characters of text; largest is {top[0]} at {top[1].chars():,}")

    # 39: Agent Skills index
    try:
        idx_json = json.loads((SITE / ".well-known/agent-skills/index.json").read_text())
        sk = idx_json["skills"]
        want = "sha256:" + hashlib.sha256((ROOT / "skills/good-code-review/SKILL.md").read_bytes()).hexdigest()
        ok = (idx_json["$schema"].endswith("/0.2.0/schema.json") and len(sk) == 1 and sk[0]["name"] == "good-code-review" and sk[0]["type"] == "skill-md"
              and sk[0]["description"] and sk[0]["digest"] == want and resolve(sk[0]["url"]) is not None
              and "sha256:" + hashlib.sha256(resolve(sk[0]["url"]).read_bytes()).hexdigest() == want)
    except (OSError, ValueError, KeyError, IndexError):
        ok = False
    check(39, ok, "agent-skills/index.json lists the skill, and its sha256 digest matches skills/good-code-review/SKILL.md and the served copy")

    print(f"\n{len(FAILS)} failing check(s)" if FAILS else "\nall checks pass")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
