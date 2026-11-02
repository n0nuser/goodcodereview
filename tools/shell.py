"""The page shell shared by every HTML page: head tags, navigation, footer, and the org icon sprite."""
import html
import json
import re
from collections.abc import Sequence
from typing import Any

import orgs
from assets import CSS, FAVICON, JS
from config import BASE, MONOGRAM_FONT_SIZES, OG_IMAGE_HEIGHT, OG_IMAGE_WIDTH, REPO, SITE_DESC, SITE_NAME
from models import AUDIT_LEVELS, NavLink

FOOTER = (f'<footer><p>Created and edited by <a href="https://pablogonzalez.me">Pablo Jesús González Rubio</a> · Content CC BY 4.0 · Code MIT · <a href="{REPO}">Source</a></p>'
          '<ul class="fl"><li><a href="drafts.html">Drafts by what they lack</a></li><li><a href="about.html">About</a></li><li><a href="privacy.html">Privacy</a></li>'
          f'<li><a href="{REPO}/issues">Contact (GitHub Issues)</a></li><li><a href="llms.txt">llms.txt</a></li><li><a href="sitemap.xml">Sitemap</a></li>'
          f'<li><a href="{REPO}/blob/main/AGENTS.md">AGENTS.md</a></li><li><a href="{REPO}/tree/main/skills/good-code-review">Skill folder</a></li></ul></footer>')


def page_url(slug: str) -> str:
    """The URL Cloudflare serves: it redirects /x.html to /x and /index.html to /."""
    return BASE + "/" if slug == "index" else f"{BASE}/{slug}"


def head_tags(title: str, desc: str, slug: str) -> str:
    """Canonical, description, Open Graph, discovery links, and the site-type declaration. The 404 page gets none."""
    if not slug:
        return ""

    def quote(t: str) -> str:
        return html.escape(t, quote=True)

    og = {"title": title, "description": desc, "type": "website", "url": page_url(slug), "site_name": SITE_NAME,
          "image": f"{BASE}/og.png", "image:alt": f"{SITE_NAME}: {SITE_DESC}", "image:width": str(OG_IMAGE_WIDTH), "image:height": str(OG_IMAGE_HEIGHT)}
    return (f'<meta name="description" content="{quote(desc)}"><link rel="canonical" href="{page_url(slug)}">'
            + "".join(f'<meta property="og:{k}" content="{quote(v)}">' for k, v in og.items())
            + f'<link rel="alternate" type="text/markdown" href="/{slug}.md"><link rel="alternate" type="text/plain" href="/llms.txt" title="llms.txt">'
            '<link rel="sitemap" type="application/xml" href="/sitemap.xml"><meta name="is-agentic-site-type" content="content">')


def sprite(body: str) -> str:
    """One hidden SVG with a symbol for each org icon the page uses: the logo, or a monogram badge."""
    def symbol(o: str) -> str:
        if o in orgs.ICONS:
            return f'<symbol id="o-{o}" viewBox="0 0 24 24"><path fill="currentColor" d="{orgs.ICONS[o]}"/></symbol>'
        m = orgs.monogram(o)
        return (f'<symbol id="o-{o}" viewBox="0 0 24 24"><rect x="1" y="1" width="22" height="22" rx="5" fill="none" stroke="currentColor" stroke-width="1.5"/>'
                f'<text x="12" y="12" dy=".35em" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-weight="700" font-size="{MONOGRAM_FONT_SIZES[len(m)]}">'
                f'{html.escape(m)}</text></symbol>')
    used = sorted(set(re.findall(r'<use href="#o-([a-z0-9-]+)"/>', body)))
    return f'<svg class="sprite" aria-hidden="true">{"".join(symbol(o) for o in used)}</svg>' if used else ""


def _nav(links: Sequence[NavLink], cur: str) -> str:
    audit_files = {f"{lv}.html" for lv in AUDIT_LEVELS}

    def anchor(link: NavLink) -> str:
        return f'<a href="{link.href}"{" aria-current=page" if link.href == cur else ""}>{html.escape(link.label)}</a>'

    items = [anchor(link) for link in links if link.href not in audit_files]
    menu = "".join(anchor(link) for link in links if link.href in audit_files)
    if menu:
        first = next(i for i, link in enumerate(links) if link.href in audit_files)
        items.insert(first, f'<details><summary>Audits</summary><div>{menu}</div></details>')
    return '<header><nav aria-label="Site">' + "".join(items) + "</nav></header>"


def page(title: str, body: str, *, links: Sequence[NavLink] = (), cur: str = "", desc: str = "", slug: str = "",
         ld: dict[str, Any] | None = None, script: bool = False) -> str:
    """One complete HTML page. `script` adds the inline filter script; `slug` turns on the head tags; `ld` is JSON-LD."""
    full = title if slug == "index" else f"{title} | {SITE_NAME}"
    jsonld = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>" if ld else ""
    tail = '<p id=said class=vh role=status></p><script>' + JS + '</script>' if script else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark">'
            f'<link rel="icon" href="{FAVICON}">'
            f"<title>{html.escape(full)}</title>{head_tags(full, desc, slug)}<style>{CSS}</style>{jsonld}</head>"
            f"<body><a class=skip href=#main>Skip to content</a>{_nav(links, cur)}<main id=main tabindex=-1>"
            f"<h1>{html.escape(title)}</h1>{body}</main>{sprite(body)}"
            f"{FOOTER}{tail}</body></html>")
