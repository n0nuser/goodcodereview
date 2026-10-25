# Changelog

All notable changes to this project are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

- On the Concerns page, every card shows as one row that links to its full card, which shrinks the page below 100,000 characters of text (`python3 tools/agent_ready_check.py` reports the largest page). Level pages keep the full text.
- 103 stable cards ship in `skills/good-code-review/SKILL.md` (the `stable cards:` count that `python3 tools/build.py` prints). Every level has at least one, and the incident level has one.
- Cards cover a change review and seven audit levels: function, module, service, system, codebase, production, and incident (`ls cards/audit`).
- The site builds 15 static pages, including the 404 page (the `site:` count that `python3 tools/build.py` prints) for goodcodereview.com.
- You can install the checklist as a skill (`npx skills add n0nuser/goodcodereview`) or as a Claude Code plugin.
- Every card names at least one concern in its tags (correctness, security, performance, reliability, compatibility, testing, maintainability, accessibility, usability, observability, or process), so a review can be scoped to one concern. `tools/validate.py` enforces it.
- Performance cards at every review level (`rg -l '^tags:.*performance' cards | wc -l`).
- Community files: code of conduct, security policy, support guide, issue forms, and a pull request template.
- The site reads as a checklist: each level page lists its checklist first, and the build writes `llms.txt`, `llms-drafts.txt`, and one `<level>.md` per level from the same cards.
- Frontend cards for usability and accessibility.
- `accessibility` and `usability` are concerns, so a review can be scoped to either one on the Concerns page.
- Human path: the home page opens with "Choose a review" and shows each level's stable and draft counts. A level with no stable cards says so on its page, on the home page, and in the nav, and gives no verdict. The nav groups the audits under one menu with 44px targets. Each page has a skip link. Copy buttons cover the home code blocks and each checklist (as markdown). A status message tells screen readers when a copy works or fails.
- The site is ready for AI agents. `python3 tools/build.py` also writes `sitemap.xml` with `lastmod`, a Markdown twin with frontmatter for every page, `_headers` (Link headers, charsets), canonical and Open Graph tags, home-page JSON-LD, About and Privacy pages, a plain-text 404, and `/.well-known/agent-skills/index.json` with the skill's sha256 digest. `llms.txt` gains a summary, a "When to use this site" paragraph, and described links. The audit is in `docs/research/agent-readiness-gaps.md`.
- `python3 tools/agent_ready_check.py` checks `site/` against those items without network access. CI does not run it.
- An incident review also checks the stable cards of the level where the cause lived, with evidence quoted from the incident text. The rule is in `SKILL.md`, `llms.txt`, and the incident page, and the build fails if it is missing.
- The footer no longer says the site is styled with good-css.com. The home page says what good-css.com is: rules for reviewing CSS.
