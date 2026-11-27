"""Every page but the home page has its own share image, rendered from the title it has now (tools/og_images.py)."""
import html
import json
import re

from build import Plan
from config import TOOLS

RERUN = "run: python3 tools/build.py && python3 tools/og_images.py && python3 tools/build.py"


def test_every_page_has_a_current_share_image(plan: Plan) -> None:
    titles = json.loads((TOOLS / "og" / "titles.json").read_text())
    slugs = re.findall(r"<loc>https://goodcodereview\.com/([^<]+)</loc>", plan.site["sitemap.xml"].decode())
    stale = []
    for slug in slugs:
        page = plan.site[f"{slug}.html"].decode()
        title = html.unescape(re.findall(r"<title>(.*?)</title>", page)[0]).removesuffix(" | Good Code Review")
        image = f"og/{slug.replace('/', '--')}.png"
        if titles.get(slug) != title or image not in plan.site or f'content="https://goodcodereview.com/{image}"' not in page:
            stale.append(slug)
    assert stale == [], RERUN
