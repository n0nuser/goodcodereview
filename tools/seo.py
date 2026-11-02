"""Search and agent metadata: per-page titles and descriptions for search results, JSON-LD for every page, agent.json, and the ARD manifest.

The visible H1 and the short level blurbs stay as they are; the strings here are written for a results page (titles 50 to 62 characters
with the brand, descriptions 110 to 160) and feed only <title>, the meta description, and the Open Graph and Twitter tags.
"""
from collections.abc import Sequence
from typing import Any

from config import BASE, LICENCE_URL, REPO, SITE_DESC, SITE_NAME
from models import CONCERNS, LEVELS

AUTHOR_URL = "https://pablogonzalez.me"
AUTHOR_GITHUB = "https://github.com/n0nuser"
# Only profiles that exist and that we can check. [NEED: owner URL] for X, Bluesky, LinkedIn. Wikipedia and Wikidata entries do not exist yet; add them here the day they do.
SAME_AS = [REPO, AUTHOR_GITHUB, AUTHOR_URL]
KEYWORDS = ("code review checklist, pull request review checklist, code review rules, AI code review, agent skill for code review, "
            "security code review, code audit checklist, PASS FAIL review verdict")
MAX_TITLE, MIN_TITLE, MIN_DESC, MAX_DESC = 62, 30, 110, 160

# slug -> (title, description). The brand is part of every title.
META: dict[str, tuple[str, str]] = {
    "index": ("Good Code Review: Checklist for People and AI Agents",
              "Free, open code review checklist with rules vetted against Google, OWASP and Microsoft. Each check ends in PASS, FAIL, or N/A with file:line evidence."),
    "concerns": ("Review Rules by Concern | Good Code Review",
                 "Filter every code review rule by concern, topic, or level. Scope a review to security, performance, accessibility, or any other concern."),
    "change": ("Pull Request Review Checklist | Good Code Review",
               "Checklist for reviewing a diff or pull request: scope, size, compatibility, tests, and the description. Every rule is vetted and ends in PASS, FAIL, or N/A."),
    "function": ("Function-Level Code Review Checklist | Good Code Review",
                 "Checklist for reviewing one file or function: names, error handling, concurrency, and call-level security. Each check ends in PASS, FAIL, or N/A."),
    "module": ("Module and Package Code Review Checklist | Good Code Review",
               "Checklist for reviewing a package or directory: boundaries, shared state, dependencies, and the public surface. Each check ends in PASS, FAIL, or N/A."),
    "service": ("Service Code Review Checklist | Good Code Review",
                "Checklist for reviewing a running service: its API, failure handling, limits, and security. Each check ends in PASS, FAIL, or N/A with evidence."),
    "system": ("System Design Review Checklist | Good Code Review",
               "Checklist for reviewing a design that spans services: shared data, caches, migrations, and failure modes. Each check ends in PASS, FAIL, or N/A."),
    "codebase": ("Repository Audit Checklist | Good Code Review",
                 "Checklist for auditing a whole repository: CI gates, dependencies, secrets, setup, and conventions. Each check ends in PASS, FAIL, or N/A with evidence."),
    "production": ("Production Readiness Review Checklist | Good Code Review",
                   "Checklist for reviewing a release or launch: rollout, rollback, alerts, and load. Each check ends in PASS, FAIL, or N/A with evidence."),
    "incident": ("Incident Postmortem Review Checklist | Good Code Review",
                 "Checklist for reviewing an incident and its follow-up: evidence, guards, and owned actions. Each check ends in PASS, FAIL, or N/A with quoted evidence."),
    "pack-go": ("Go Code Review Checklist: Go Pack | Good Code Review",
                "Go-specific code review rules for errors, goroutines, contexts, and the standard library. Use them with the level page that matches your input."),
    "pack-python": ("Python Code Review Checklist: Python Pack | Good Code Review",
                    "Python-specific code review rules for typing, exceptions, async, packaging, and security. Use them with the level page that matches your input."),
    "pack-typescript": ("TypeScript Code Review Checklist: TS Pack | Good Code Review",
                        "TypeScript-specific code review rules for types, async code, and runtime validation. Use them with the level page that matches your input."),
    "glossary": ("Code Review Glossary and Terms | Good Code Review",
                 "Definitions of the terms that the code review cards link to, with a note on why a reviewer cares about each one, from race conditions to idempotency."),
    "drafts": ("Draft Code Review Rules | Good Code Review",
               "Every draft code review card grouped by what keeps it from stable, and what each draft needs to be promoted. Drafts never change a verdict."),
    "guides": ("Code Review Guides: Pull Requests, Security | Good Code Review",
               "Short guides to common review questions, such as how to review a pull request and what to check in a migration. Each lists vetted checks."),
    "about": ("About Good Code Review: Authorship, Method, Licences",
              "Who makes Good Code Review, how a rule becomes stable, what stable and draft cards mean, and the licences for the content and the code."),
    "privacy": ("Privacy: Good Code Review Collects Nothing",
                "Good Code Review sets no cookies, runs no analytics, asks for no accounts, and loads nothing from other sites. Here is what the host logs."),
    "audit": ("Audit a Repo or Release | Good Code Review",
              "How to audit a whole repo, service, or release with the same cards: scope, read order, missing controls, accepted risk, and the report shape."),
}

PAGE_TYPE: dict[str, str] = {**{k: "CollectionPage" for k in ("concerns", "glossary", "drafts", "guides", *map(str, LEVELS))}, "about": "AboutPage"}


def meta(slug: str, title: str, desc: str) -> tuple[str, str]:
    """The <title> and description for a slug. A page with no entry keeps the plain title plus the brand."""
    return META.get(slug, (title if slug == "index" else f"{title} | {SITE_NAME}", desc))


def person() -> dict[str, Any]:
    return {"@type": "Person", "@id": f"{AUTHOR_URL}/#person", "name": "Pablo Jesús González Rubio", "url": AUTHOR_URL,
            "description": "Maintainer of Good Code Review.", "sameAs": [AUTHOR_GITHUB, AUTHOR_URL]}


def page_ld(slug: str, title: str, desc: str, date: str, crumbs: Sequence[tuple[str, str]] = ()) -> dict[str, Any]:
    """JSON-LD for an inner page: the page, its breadcrumb, and a pointer to the site. The home page builds its own graph."""
    url = f"{BASE}/{slug}"
    trail = [(t, f"{BASE}/" if c == "index" else f"{BASE}/{c}") for t, c in crumbs] or [("Home", f"{BASE}/")] + ([] if slug == "index" else [(title, url)])
    return {"@context": "https://schema.org", "@graph": [
        {"@type": PAGE_TYPE.get(slug, "WebPage"), "@id": f"{url}#page", "url": url, "name": title, "description": desc, "inLanguage": "en",
         "isPartOf": {"@id": f"{BASE}/#website"}, "breadcrumb": {"@id": f"{url}#breadcrumb"}, "dateModified": date, "license": LICENCE_URL},
        {"@type": "BreadcrumbList", "@id": f"{url}#breadcrumb",
         "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "item": u} for i, (n, u) in enumerate(trail, 1)]}]}


def home_ld(date: str) -> dict[str, Any]:
    """The home graph: the site, the checklist, the open-source project, and the maintainer, with the profiles that disambiguate the brand."""
    author = person()
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": SITE_NAME, "alternateName": ["goodcodereview.com", "GCR"],
         "description": SITE_DESC, "inLanguage": "en", "keywords": KEYWORDS, "license": LICENCE_URL, "author": {"@id": author["@id"]},
         "dateModified": date, "sameAs": SAME_AS},
        {"@type": "CreativeWork", "@id": f"{BASE}/#checklist", "url": f"{BASE}/", "name": "Good Code Review checklist",
         "description": "Rules for reviewing code, one card per rule, each with a FAIL example and a PASS example.", "inLanguage": "en", "keywords": KEYWORDS,
         "isPartOf": {"@id": f"{BASE}/#website"}, "license": LICENCE_URL, "author": {"@id": author["@id"]}, "dateModified": date, "sameAs": [REPO]},
        {"@type": "SoftwareSourceCode", "@id": f"{REPO}#source", "name": "goodcodereview", "url": REPO, "description": "Cards and build tools of goodcodereview.com.",
         "codeRepository": REPO, "license": "https://opensource.org/license/mit",
         "author": {"@id": author["@id"]}, "isPartOf": {"@id": f"{BASE}/#website"}, "sameAs": [REPO]},
        author]}


def _levels() -> list[dict[str, str]]:
    return [{"level": lv, "page": f"{BASE}/{lv}", "markdown": f"{BASE}/{lv}.md", "cards": f"{BASE}/cards/{lv}.json"} for lv in LEVELS]


def agent_manifest(date: str, counts: dict[str, int], skills: list[str]) -> dict[str, Any]:
    """agent.json: what the site is, what an agent can fetch, how (no authentication), and which skills and CLI to install.

    Served at /agent.json. A Cloudflare rule can also serve it for /?mode=agent (docs/deploy.md).
    """
    return {
        "name": SITE_NAME, "url": f"{BASE}/", "description": SITE_DESC, "updated": date, "mode": "agent",
        "human_page": f"{BASE}/", "license": {"content": LICENCE_URL, "code": "https://opensource.org/license/mit"},
        "authentication": {"type": "none", "note": "Every endpoint is a public, read-only static file. No key, no cookie, no account."},
        "rate_limits": "None set by the site. Files sit behind a CDN cache; fetch the single-level or single-concern files instead of a filtered query.",
        "capabilities": [
            {"id": "review-code", "summary": "Check code against vetted cards and report each as PASS, FAIL, or N/A with file:line evidence.", "entry": f"{BASE}/llms.txt"},
            {"id": "list-cards", "summary": "List stable cards as JSON, all at once or per level or concern.", "entry": f"{BASE}/cards.json"},
            {"id": "scope-by-concern", "summary": "Get the cards for one concern as Markdown.", "entry": f"{BASE}/concerns/{{concern}}.md"},
            {"id": "audit", "summary": "Audit a repo, service, or release: scope, read order, report shape.", "entry": f"{BASE}/audit.md"}],
        "endpoints": {
            "llms_txt": f"{BASE}/llms.txt", "sitemap": f"{BASE}/sitemap.xml", "agent_manifest": f"{BASE}/agent.json",
            "ard": f"{BASE}/.well-known/ard.json", "agent_skills": f"{BASE}/.well-known/agent-skills/index.json",
            "cards": f"{BASE}/cards.json", "cards_index": f"{BASE}/cards-index.json", "cards_schema": f"{BASE}/cards.schema.json",
            "cards_by_level": f"{BASE}/cards/{{level}}.json", "cards_by_concern": f"{BASE}/cards/concern-{{concern}}.json",
            "concern_markdown": f"{BASE}/concerns/{{concern}}.md", "level_markdown": f"{BASE}/concerns/level-{{level}}.md",
            "page_markdown": f"{BASE}/{{page}}.md", "drafts": f"{BASE}/cards-drafts.json"},
        "levels": _levels(), "concerns": list(CONCERNS), "stable_cards": counts,
        "skills": [{"name": n, "path": f"{REPO}/tree/main/skills/{n}"} for n in skills],
        "install": {"skill": "npx skills add n0nuser/goodcodereview", "plugin": "/plugin marketplace add n0nuser/goodcodereview",
                    "cli": f"not published yet; source in {REPO}/tree/main/cli"},
        "webmcp": "Pages register read-only tools on document.modelContext when the browser supports it: start_review, list_levels, list_cards.",
        "repository": REPO, "sameAs": SAME_AS}


def ard_manifest(skills: list[tuple[str, str, list[str]]]) -> dict[str, Any]:
    """/.well-known/ard.json, ARD publisher spec v0.91: https://agenticresourcediscovery.org/spec/. `skills` holds (name, description, example queries)."""
    pub = "goodcodereview.com"
    entries: list[dict[str, Any]] = [
        {"identifier": f"urn:air:{pub}:data:review-cards", "displayName": "Good Code Review cards", "type": "application/json", "url": f"{BASE}/cards.json",
         "description": "Every vetted code review rule as JSON, one card each, with severity, concerns, and sources.", "capabilities": ["CodeReviewRules"],
         "representativeQueries": ["what should I check when reviewing a pull request", "list security code review rules", "code review checklist as JSON"]},
        {"identifier": f"urn:air:{pub}:data:agent-manifest", "displayName": "Good Code Review agent manifest", "type": "application/json", "url": f"{BASE}/agent.json",
         "description": "Endpoints, capabilities, and authentication (none) for agents using Good Code Review.", "capabilities": ["Discovery"],
         "representativeQueries": ["how do I use goodcodereview.com from an agent", "which endpoints does Good Code Review offer"]}]
    entries += [
        {"identifier": f"urn:air:{pub}:skill:{n}", "displayName": n, "type": "application/agent-skills+md", "url": f"{BASE}/.well-known/agent-skills/{n}/SKILL.md",
         "description": d, "capabilities": ["CodeReview"], "representativeQueries": q}
        for n, d, q in skills]
    return {"entries": entries}
