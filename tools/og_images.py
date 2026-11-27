#!/usr/bin/env python3
"""Render one share image per page into tools/og/. Run after tools/build.py; needs rsvg-convert and magick. Standard library only.

    python3 tools/build.py && python3 tools/og_images.py && python3 tools/build.py

The home page keeps tools/og.png. test/test_og.py fails when a page has no image or its title changed since the render.
"""
import html
import json
import re
import subprocess
import textwrap

from config import OG_IMAGE_HEIGHT, OG_IMAGE_WIDTH, SITE, TOOLS

OUT = TOOLS / "og"
TITLES = OUT / "titles.json"


def name(slug: str) -> str:
    return slug.replace("/", "--")


def page_titles() -> dict[str, tuple[str, str]]:
    """The (title, description) of every sitemap page except the home page, read from the built site."""
    slugs = re.findall(r"<loc>https://goodcodereview\.com/([^<]+)</loc>", (SITE / "sitemap.xml").read_text())
    out = {}
    for slug in slugs:
        page = (SITE / f"{slug}.html").read_text()
        title = html.unescape(re.findall(r"<title>(.*?)</title>", page)[0]).removesuffix(" | Good Code Review")
        out[slug] = (title, html.unescape(re.findall(r'<meta name="description" content="([^"]*)"', page)[0]))
    return out


def svg(title: str, desc: str) -> str:
    def lines(text: str, width: int, y: int, step: int, size: int, fill: str, weight: int) -> str:
        return "".join(f'<text x="70" y="{y + i * step}" font-family="Liberation Sans, Arial" font-size="{size}" font-weight="{weight}" fill="{fill}">{html.escape(s)}</text>'
                       for i, s in enumerate(textwrap.wrap(text, width)[:3]))

    top = 140
    below = top + len(textwrap.wrap(title, 28)[:3]) * 78 + 20
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{OG_IMAGE_WIDTH}" height="{OG_IMAGE_HEIGHT}">'
            f'<rect width="100%" height="100%" fill="#11131a"/><rect width="18" height="100%" fill="#3dba7f"/>'
            + lines(title, 28, top, 78, 64, "#f3f5f8", 700) + lines(desc, 62, below, 44, 32, "#c3c9d4", 400)
            + '<text x="70" y="582" font-family="Liberation Sans, Arial" font-size="30" font-weight="700" fill="#3dba7f">goodcodereview.com</text>'
            + '<text x="1130" y="582" text-anchor="end" font-family="Liberation Sans, Arial" font-size="26" fill="#8c93a0">Free. For people and agents.</text></svg>')


def main() -> None:
    OUT.mkdir(exist_ok=True)
    pages = page_titles()
    for old in OUT.glob("*.png"):
        old.unlink()
    for slug, (title, desc) in pages.items():
        png = subprocess.run(["rsvg-convert"], input=svg(title, desc).encode(), capture_output=True, check=True).stdout
        subprocess.run(["magick", "png:-", "-strip", "-colors", "64", f"PNG8:{OUT / name(slug)}.png"], input=png, check=True)  # a flat design needs few colours
    TITLES.write_text(json.dumps({s: t for s, (t, _) in sorted(pages.items())}, indent=1) + "\n")
    print(f"{len(pages)} share images in {OUT}")


if __name__ == "__main__":
    main()
