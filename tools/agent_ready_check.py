#!/usr/bin/env python3
"""Check site/ against the agent-readiness items in docs/research/agent-readiness-gaps.md. Run tools/build.py first.

No network: it reads files only. Prints one PASS or FAIL line per check, names the checklist item, and exits 1 on any FAIL.
"""
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from config import BASE, LLMS_BUDGET, PAGE_MAX, ROOT, SITE

MIN_INDEX_CHARS = 500
MIN_TRUST_PAGE_CHARS = 500
MIN_404_CHARS = 20
MIN_404_LINKS = 5
HEADERS_MAX_RULES = 100
HEADERS_MAX_LINE = 2_000
LLMS_MIN = 100  # characters; a shorter llms.txt is empty in practice
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
FEATURE_TAGS = ("img", "iframe", "form", "input", "video", "audio")
FOOTER_LINKS = ["llms.txt", "sitemap.xml", "about.html", "privacy.html", "/AGENTS.md", "/skills/good-code-review", "/issues"]
Attrs = dict[str, str | None]


@dataclass(slots=True)
class Report:
    """Prints one line per check and remembers the items that failed."""

    failures: list[int] = field(default_factory=list)

    def check(self, item: int, ok: object, msg: str) -> None:
        print(f"{'PASS' if ok else 'FAIL'}  item {item}: {msg}")
        if not ok:
            self.failures.append(item)


class Page(HTMLParser):
    """Collects what the checks read: text, headings, head tags, links, and landmark tags. Build one with `Page.parse`."""

    def __init__(self) -> None:
        super().__init__()
        self.text: list[str] = []
        self.heads: list[int] = []
        self.metas: list[Attrs] = []
        self.links: list[Attrs] = []
        self.hrefs: list[str] = []
        self.tags: set[str] = set()
        self.ld: list[str] = []
        self.js: list[str] = []
        self.css: list[str] = []
        self.scripts: list[Attrs] = []
        self.title = ""
        self._skip = 0
        self._in = ""

    @classmethod
    def parse(cls, src: str) -> "Page":
        page = cls()
        page.feed(src)
        return page

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
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
            self.hrefs.append(a["href"] or "")
        elif tag == "title":
            self._in = "title"
        elif re.fullmatch(r"h[1-6]", tag):
            self.heads.append(int(tag[1]))

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self._skip -= 1
        if tag in ("script", "style", "title"):
            self._in = ""

    def handle_data(self, data: str) -> None:
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

    def chars(self) -> int:
        return len(re.sub(r"\s+", " ", " ".join(self.text)).strip())

    def meta(self, key: str, val: str) -> list[str]:
        return [m.get("content") or "" for m in self.metas if m.get(key) == val]

    def link(self, rel: str) -> list[Attrs]:
        return [lk for lk in self.links if lk.get("rel") == rel]


def resolve(url: str) -> Path | None:
    """Map a goodcodereview.com URL to the file the host serves, or None. Cloudflare Pages drops .html from page URLs."""
    p = urlparse(url).path
    if p in ("", "/"):
        return SITE / "index.html"
    f = SITE / p.lstrip("/")
    return f if f.is_file() else (SITE / (p.lstrip("/") + ".html") if (SITE / (p.lstrip("/") + ".html")).is_file() else None)


@dataclass(frozen=True, slots=True)
class ParsedHeaders:
    """The rules of a `_headers` file by URL pattern, and the format errors found."""

    rules: dict[str, list[str]]
    errors: list[str]


def parse_headers(text: str) -> ParsedHeaders:
    """Parse a Cloudflare Pages _headers file: unindented URL lines, then indented `Name: value` lines. Return (rules, errors)."""
    rules: dict[str, list[str]] = {}
    errs: list[str] = []
    cur: list[str] | None = None
    for n, line in enumerate(text.split("\n"), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if len(line) > HEADERS_MAX_LINE:
            errs.append(f"line {n} is over {HEADERS_MAX_LINE:,} characters")
        if line[0] not in " \t":
            cur = rules.setdefault(line.strip(), [])
        elif cur is None:
            errs.append(f"line {n}: header before any URL")
        elif not re.fullmatch(r"\s+!?\s*[A-Za-z0-9-]+(:\s*.+)?", line):
            errs.append(f"line {n}: not `Name: value`")
        else:
            cur.append(line.strip())
    return ParsedHeaders(rules, errs)


def _items_1_12_30(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """1, 12, 30: content in the raw HTML, landmarks, heading order."""
    idx = pages["index.html"]
    r.check(1, idx.heads.count(1) == 1 and idx.chars() >= MIN_INDEX_CHARS, f"index.html has one h1 and {idx.chars()} characters of text without JavaScript")
    bad = [n for n, p in pages.items() if p.heads.count(1) != 1 or any(b > a + 1 for a, b in zip(p.heads, p.heads[1:], strict=False))
           or not {"header", "nav", "main", "footer"} <= p.tags]
    r.check(30, not bad, f"every page has header, nav, main, footer, one h1, and no skipped heading level{': ' + ', '.join(bad) if bad else ''}")


def _items_2_3_4(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """2, 3, 4: robots.txt."""
    robots = (SITE / "robots.txt").read_text()
    groups = re.findall(r"(?im)^user-agent:\s*(.+)$", robots)
    r.check(2, groups == ["*"] and not re.search(r"(?im)^disallow:\s*\S", robots), "robots.txt has one `User-agent: *` group and no Disallow rule")
    r.check(3, groups == ["*"] and re.search(r"(?im)^allow:\s*/\s*$", robots) is not None, "robots.txt allows everything and names no crawler")
    r.check(4, f"Sitemap: {BASE}/sitemap.xml" in robots, "robots.txt has a Sitemap line")


def _items_5_6(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """5, 6: sitemap."""
    try:
        root = ET.fromstring((SITE / "sitemap.xml").read_text())
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [u.findtext("s:loc", "", ns) for u in root.findall("s:url", ns)]
        mods = [u.findtext("s:lastmod", "", ns) for u in root.findall("s:url", ns)]
    except (OSError, ET.ParseError) as e:
        locs, mods = [], []
        print(f"      sitemap.xml unreadable: {e}")
    served = {resolve(ln) for ln in locs}
    missing = [n for n in content if SITE / n not in served]
    r.check(5, locs and not missing and None not in served, f"sitemap.xml lists {len(locs)} URLs, one per HTML page except 404.html{': missing ' + ', '.join(missing) if missing else ''}")
    try:
        ok = mods and all(date.fromisoformat(m) <= date.today() for m in mods)
    except ValueError:
        ok = False
    r.check(6, bool(ok), f"every sitemap URL has a lastmod date ({mods[0] if mods else 'none'})")


def _items_7_8_9(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """7, 8, 9: error page, redirects."""
    nf = pages["404.html"]
    r.check(9, nf.chars() >= MIN_404_CHARS and len(nf.hrefs) >= MIN_404_LINKS, f"404.html has {nf.chars()} characters of text and {len(nf.hrefs)} links")
    r.check(8, not (SITE / "_redirects").exists() and not any(m.get("http-equiv") == "refresh" for p in pages.values() for m in p.metas),
          "no _redirects file and no meta-refresh stubs")


def _items_15_16_17_19(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """15, 16, 17, 19: llms.txt."""
    llms = (SITE / "llms.txt").read_text()
    # llmstxt.org: H1, then a blockquote, then headingless sections, then H2 file lists of `- [name](url): notes`; "Optional" last.
    lines = llms.split("\n")
    first_h2 = next((i for i, ln in enumerate(lines) if ln.startswith("## ")), len(lines))
    fence = False
    bad_items: list[str] = []
    for ln in lines[first_h2:]:
        if ln.startswith("```"):
            fence = not fence
        elif not fence and ln.strip() and not ln.startswith("## ") and not re.match(r"- \[[^\]]+\]\(\S+\)(: .*)?$", ln):
            bad_items.append(ln[:50])
    h2s = [ln for ln in lines if ln.startswith("## ")]
    shape = (re.match(r"# \S", llms) and re.match(r"(?s)# [^\n]+\n\n> \S", llms) and not any(ln.startswith("#") for ln in lines[1:first_h2])
             and not bad_items and h2s and h2s[-1] == "## Optional")
    detail = f"; not a file-list line: {bad_items[0]}" if bad_items else ""
    r.check(16, LLMS_MIN <= len(llms) < LLMS_BUDGET and shape,
            f"llms.txt follows llmstxt.org ({len(llms)} characters, limit {LLMS_BUDGET}): H1, blockquote, headingless intro, H2 file lists, Optional last{detail}")
    own = [u.rstrip(".,)") for u in re.findall(r"\]\((https?://[^)\s]+)\)", llms) if urlparse(u).netloc == "goodcodereview.com"]
    dead = [u for u in own if resolve(u) is None]
    r.check(17, own and not dead, f"{len(own)} own-site links in llms.txt resolve to files in site/{': dead ' + ', '.join(dead) if dead else ''}")
    r.check(19, "Use this site when you are asked to review" in llms, "llms.txt opens with a `When to use` paragraph")
    unbalanced = [f.name for f in [*SITE.glob("*.md"), SITE / "llms.txt", SITE / "llms-drafts.txt"] if len(re.findall(r"(?m)^```", f.read_text())) % 2]
    r.check(15, not unbalanced and all('<code class="language-' in (SITE / f"{lv}.html").read_text() for lv in ("change", "function")),
          f"code fences are balanced in served Markdown and tagged with a language class in HTML{': ' + ', '.join(unbalanced) if unbalanced else ''}")


def _items_14_29_37_42(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """14, 29, 37, 42: head tags."""
    problems = []
    for n, p in content.items():
        slug = n[:-5]
        want = BASE + "/" if slug == "index" else f"{BASE}/{slug}"
        canon = [ln["href"] for ln in p.link("canonical")]
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
    r.check(14, not any("canonical" in x for x in problems), "every page has one canonical URL, the extensionless URL in the sitemap")
    r.check(29, not any(k in x for x in problems for k in ("description", "og tags")) and all(re.search(r'<html lang="en"', f.read_text()) for f in SITE.glob("*.html")),
          "every page has lang, description, and the Open Graph tags, including og:image")
    r.check(29, (SITE / "og.png").read_bytes()[:8] == PNG_MAGIC, "og.png is a PNG file")
    r.check(37, not any("title" in x for x in problems), "every page title names Good Code Review")
    r.check(42, not any("is-agentic-site-type" in x for x in problems), 'every page has <meta name="is-agentic-site-type" content="content">')


def _items_20_38(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """20, 38: discovery links in footer and head."""
    foot = ["llms.txt", "sitemap.xml", "about.html", "privacy.html", "/AGENTS.md", "/skills/good-code-review", "/issues"]
    gaps = [n for n, p in pages.items() if not all(any(h.endswith(f) for h in p.hrefs) for f in foot)]
    r.check(20, not gaps, f"footer links About, Privacy, Contact, llms.txt, sitemap, AGENTS.md, and the skill folder on every page{': ' + ', '.join(gaps) if gaps else ''}")
    head_gaps = [n for n, p in content.items() if not (p.link("sitemap") and any(ln.get("href") == "/llms.txt" for ln in p.link("alternate")))]
    r.check(20, not head_gaps, f"head links the sitemap and llms.txt on every content page{': ' + ', '.join(head_gaps) if head_gaps else ''}")


def _items_22_23(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """22, 23: Markdown twins and frontmatter."""
    twin_gaps, fm_gaps = [], []
    for n, p in content.items():
        slug = n[:-5]
        alt = [ln["href"] for ln in p.link("alternate") if ln.get("type") == "text/markdown"]
        if alt != [f"/{slug}.md"] or not (SITE / f"{slug}.md").is_file():
            twin_gaps.append(n)
    for f in sorted(SITE.glob("*.md")):
        m = re.match(r"---\n(.*?)\n---\n", f.read_text(), re.S)
        keys = {ln.split(":", 1)[0] for ln in m.group(1).split("\n")} if m else set()
        if not {"title", "description", "canonical", "updated"} <= keys:
            fm_gaps.append(f.name)
    r.check(22, not twin_gaps, f"every content page has a Markdown twin and a rel=alternate link to it{': ' + ', '.join(twin_gaps) if twin_gaps else ''}")
    r.check(23, not fm_gaps, f"every served .md starts with frontmatter (title, description, canonical, updated){': ' + ', '.join(fm_gaps) if fm_gaps else ''}")


def _items_21_33(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """21, 33: _headers."""
    parsed = parse_headers((SITE / "_headers").read_text())
    rules, errs = parsed.rules, parsed.errors
    flat = " ".join(" ".join(v) for v in rules.values())
    r.check(21, not errs and len(rules) <= HEADERS_MAX_RULES and "rel=\"sitemap\"" in flat and "rel=\"alternate\"; type=\"text/markdown\"" in flat
          and "/*.md" in rules and "charset=utf-8" in " ".join(rules.get("/*.md", [])) and "charset=utf-8" in " ".join(rules.get("/*.txt", [])),
          f"_headers parses ({len(rules)} rules): Link for sitemap and Markdown twins, charset for .md and .txt{'; ' + '; '.join(errs) if errs else ''}")
    r.check(33, "x-robots-tag" not in flat.lower() and not any(m.get("name") == "robots" and "noindex" in (m.get("content") or "") for p in pages.values() for m in p.metas),
          "no noindex meta tag and no X-Robots-Tag header")


def _items_25_28(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """25, 28: JSON-LD."""
    idx = pages["index.html"]
    try:
        ld = json.loads("".join(idx.ld))
        types = {n.get("@type") for n in ld.get("@graph", [])}
        ok = {"WebSite", "CreativeWork"} <= types and all(n.get(k) for n in ld["@graph"] for k in ("name", "description", "url"))
    except (ValueError, AttributeError):
        ok, types = False, set()
    r.check(25, ok, f"index.html JSON-LD parses; types {sorted(types)}; each has name, description, url")
    allowed = {"WebSite", "CreativeWork", "Person", "SoftwareSourceCode"}
    r.check(28, ok and types <= allowed, f"home JSON-LD types match visible content ({', '.join(sorted(allowed))} only)")
    same = [n for n in ld.get("@graph", []) if n.get("@type") == "WebSite"] if ok else []
    r.check(28, same and len(same[0].get("sameAs", [])) >= 2 and same[0].get("keywords"), "home WebSite declares keywords and sameAs profiles")
    inner = {"WebPage", "CollectionPage", "AboutPage", "BreadcrumbList"}
    bad = []
    for n, p in content.items():
        if n == "index.html":
            continue
        try:
            kinds = {x.get("@type") for x in json.loads("".join(p.ld))["@graph"]}
        except (ValueError, KeyError, AttributeError):
            kinds = set()
        if "BreadcrumbList" not in kinds or not kinds <= inner:
            bad.append(n)
    r.check(28, not bad, f"every inner page has a page node and a BreadcrumbList in JSON-LD{': ' + ', '.join(bad) if bad else ''}")


def _items_34(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """34: trust pages, and the privacy claim."""
    for n in ("about.html", "privacy.html"):
        r.check(34, pages[n].chars() >= MIN_TRUST_PAGE_CHARS, f"{n} has {pages[n].chars()} characters of text (at least {MIN_TRUST_PAGE_CHARS})")
    code = "".join(x for p in pages.values() for x in p.js)
    css = "".join(x for p in pages.values() for x in p.css)
    leaks = [t for t in ("document.cookie", "localStorage", "sessionStorage", "fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket") if t in code]
    leaks += [t for t in ("@import", "http") if t in css] + [f"<{t}>" for p in pages.values() for t in ("img", "iframe", "form", "input", "video", "audio") if t in p.tags]
    ext = [x for p in pages.values() for x in p.scripts] + [ln for p in pages.values() for ln in p.links if ln.get("rel") in ("stylesheet", "preload", "preconnect")]
    r.check(34, not leaks and not ext, "page scripts and styles use no cookie, storage, or network call, and no page loads external or form content, as privacy.html says"
            + (f": found {', '.join(leaks)}" if leaks else ""))


def _items_36(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """36: page size."""
    big = {n: p.chars() for n, p in pages.items() if p.chars() >= PAGE_MAX}
    top = max(pages.items(), key=lambda kv: kv[1].chars())
    r.check(36, not big, f"every page is under {PAGE_MAX:,} characters of text; largest is {top[0]} at {top[1].chars():,}")


def _items_39(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """39: Agent Skills index; every listed skill's digest matches its source and its served copy."""
    bad = []
    try:
        idx_json = json.loads((SITE / ".well-known/agent-skills/index.json").read_text())
        sk = idx_json["skills"]
        if not idx_json["$schema"].endswith("/0.2.0/schema.json") or sk[0]["name"] != "good-code-review" or len(sk) != 3:
            bad.append("index shape")
        for e in sk:
            src = ROOT / "skills" / e["name"] / "SKILL.md"
            served = resolve(e["url"])
            want = "sha256:" + hashlib.sha256(src.read_bytes()).hexdigest()
            if not (e["type"] == "skill-md" and 0 < len(e["description"]) <= 1024 and e["digest"] == want and served is not None
                    and "sha256:" + hashlib.sha256(served.read_bytes()).hexdigest() == want
                    and re.search(rf"(?m)^name: {re.escape(e['name'])}$", src.read_text())):
                bad.append(e["name"])
    except (OSError, ValueError, KeyError, IndexError):
        bad.append("index unreadable")
    r.check(39, not bad, f"agent-skills/index.json lists every skill, and each digest matches skills/<name>/SKILL.md and the served copy{': ' + ', '.join(bad) if bad else ''}")


def _items_43_46(r: Report, pages: dict[str, Page], content: dict[str, Page]) -> None:
    """43 ARD, 44 agent.json, 45 WebMCP, 46 search snippets."""
    try:
        ard = json.loads((SITE / ".well-known/ard.json").read_text())["entries"]
        keys = [("url" in e) != ("data" in e) for e in ard]
        ok = (bool(ard) and all(keys) and all(re.fullmatch(r"urn:air:goodcodereview\.com:(?:[a-z-]+:)?[a-z0-9-]+", e["identifier"]) and e["displayName"] and e["type"] for e in ard)
              and all(2 <= len(e.get("representativeQueries", [])) <= 5 for e in ard) and len({e["identifier"] for e in ard}) == len(ard)
              and all(resolve(e["url"]) is not None for e in ard))
    except (OSError, ValueError, KeyError):
        ok = False
    robots = (SITE / "robots.txt").read_text()
    rel = all(any(ln.get("href") == "/.well-known/ard.json" for ln in p.link("ard")) for p in content.values())
    agentmap = f"Agentmap: {BASE}/.well-known/ard.json" in robots
    r.check(43, ok and rel and agentmap, "ARD spec v0.91 (agenticresourcediscovery.org/spec): entries valid, urls resolve, rel=ard on each page, Agentmap in robots.txt")
    try:
        am = json.loads((SITE / "agent.json").read_text())
        ok = (am["authentication"]["type"] == "none" and am["capabilities"] and am["endpoints"]["llms_txt"].startswith(BASE)
              and all(resolve(am["endpoints"][k]) is not None for k in ("llms_txt", "sitemap", "cards", "cards_index", "agent_skills", "ard")))
    except (OSError, ValueError, KeyError):
        ok = False
    r.check(44, ok, "agent.json states the authentication (none), the capabilities, and endpoints that resolve")
    code = "".join(pages["index.html"].js)
    r.check(45, "modelContext" in code and "registerTool" in code and all(t in code for t in ("start_review", "list_levels", "list_cards")),
            "WebMCP: the page script registers start_review, list_levels, and list_cards on document.modelContext when it exists")
    ico, svg = SITE / "favicon.ico", SITE / "favicon.svg"
    icons = [(ln.get("href"), ln.get("sizes") or ln.get("type")) for p in pages.values() for ln in p.links if ln.get("rel") == "icon"]
    r.check(47, ico.is_file() and ico.read_bytes()[:4] == b"\x00\x00\x01\x00" and svg.is_file() and svg.read_text().lstrip().startswith("<svg")
            and all(("/favicon.svg", "image/svg+xml") in icons[i:i + 2] and ("/favicon.ico", "32x32") in icons[i:i + 2] for i in range(0, len(icons), 2)) and len(icons) == 2 * len(pages),
            "/favicon.svg and /favicon.ico are served files and every page's <link rel=icon> points at them, with no data: URI")
    snippet = []
    for n, p in content.items():
        t, d = p.title, (p.meta("name", "description") or [""])[0]
        if not (40 <= len(t) <= 62 and 110 <= len(d) <= 160):
            snippet.append(f"{n} ({len(t)}/{len(d)})")
        if p.meta("name", "twitter:card") != ["summary_large_image"]:
            snippet.append(f"{n}: twitter:card")
    r.check(46, not snippet, f"titles are 40 to 62 characters and descriptions 110 to 160, and every page has twitter:card{': ' + ', '.join(snippet) if snippet else ''}")


def main() -> int:
    """Run every check against site/ and return the exit code."""
    if not (SITE / "index.html").is_file():
        print("site/ is empty. Run python3 tools/build.py first.")
        return 1
    pages = {f.name: Page.parse(f.read_text()) for f in sorted(SITE.glob("*.html"))}
    content = {n: p for n, p in pages.items() if n != "404.html"}
    r = Report()
    _items_1_12_30(r, pages, content)
    _items_2_3_4(r, pages, content)
    _items_5_6(r, pages, content)
    _items_7_8_9(r, pages, content)
    _items_15_16_17_19(r, pages, content)
    _items_14_29_37_42(r, pages, content)
    _items_20_38(r, pages, content)
    _items_22_23(r, pages, content)
    _items_21_33(r, pages, content)
    _items_25_28(r, pages, content)
    _items_34(r, pages, content)
    _items_36(r, pages, content)
    _items_39(r, pages, content)
    _items_43_46(r, pages, content)
    print(f"\n{len(r.failures)} failing check(s)" if r.failures else "\nall checks pass")
    return 1 if r.failures else 0


if __name__ == "__main__":
    sys.exit(main())
