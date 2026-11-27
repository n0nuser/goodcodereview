"""A page that was published keeps its URL. test/published_urls.txt is the record: add a line for a new page, never delete one."""
from pathlib import Path

from build import Plan

RECORD = Path(__file__).with_name("published_urls.txt")


def test_every_published_page_is_still_built(plan: Plan) -> None:
    built = {name.removesuffix(".html") for name in plan.site if name.endswith(".html")}
    published = set(RECORD.read_text().split())
    assert sorted(published - built) == [], "these published pages are no longer built; keep them as a page, such as a hub"


def test_every_built_page_is_recorded(plan: Plan) -> None:
    pages = {u.split("goodcodereview.com/")[1].split("<")[0] or "index" for u in plan.site["sitemap.xml"].decode().split("<loc>")[1:]}
    assert sorted(pages - set(RECORD.read_text().split())) == [], "add the new pages to test/published_urls.txt"
