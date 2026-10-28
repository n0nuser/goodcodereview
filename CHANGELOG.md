# Changelog

All notable changes to this project are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

- The skill description says to use it for any request to review, audit, or check code and to load it before reviewing by hand. In the evals, the agent invoked it unprompted in about half the runs, up from about a third.
- Skill evals: `tools/eval.py` runs five cases in `test/evals/` through `claude -p` in `skill`, `forced`, and `bare` modes and grades each reply on substance and format. CI runs only the grader's tests.
- Skill, from a 26-repository test-suite audit: cards whose `applies_when` fails collapse to one `N/A` count and the `change` cards are skipped when there is no diff; one defect goes under one card; each `FAIL` is tagged `proven`, `inferred`, or `could not check`; draft findings go in a Notes section at `discuss` at most; the closing design note is one short line and only for an unscoped review.
- The skill routes a diff to the function, module, service, system, and codebase cards its changed lines touch, opens its report with a `Verdict:` line and orders the ledger by severity, tells the agent to mark `PASS` or `FAIL` only for code it read, to treat the reviewed content as data, and to triage cards by `applies_when` before opening a reference file. The description names pull requests, security, accessibility, and performance reviews so it triggers.
- The Concerns page filters through the address: `?concern=`, `?topic=`, `?level=`, and `?group=`, with comma-separated or repeated values. Filters now sit above the checklist in collapsible groups, show counts, list only topics that have a stable card, and have a Group by menu, a Clear button, and a link to the same view as Markdown and JSON. `/concerns.md` and `/cards.json` apply the same filters in the Worker (`run_worker_first`).
- The home page opens with the agent prompt and says the rules are curated and backed by named organisations. The README says the same.
- `llms.txt` follows llmstxt.org: an H1, a blockquote, headingless intro sections, then H2 file lists of `[name](url): notes` links, with draft cards and site pages under `## Optional`. Each stable card links to its entry in the level file. `/.well-known/security.txt` is served.
- `code-dead-code` and `mod-yagni` are stable again. Each Rule is narrowed to the clauses that three organisations back (`docs/research/dead-code-yagni-pass.md`), and commented-out code and orphaned files moved to the Why.
- Two cards moved to draft, six gained sources, and two Rules narrowed, so every stable card has three organisations that are not single authors (`python3 tools/validate.py` enforces it).
- Each card ends with a "Backed by" list that names every organisation behind it, with a logo or a letter badge, and groups its source links under each one. `tools/orgs.py` maps every source URL to an organisation, and `python3 tools/validate.py` fails a stable card with fewer than three. People are references: they appear under "People cited" and never count as organisations. A draft says "Cites" instead of "Backed by". `cards.json` has an `orgs` field (organisations only) and a `people` field per card, and its `schema_version` is now 3.
- On the Concerns page, every card shows as one row that links to its full card, which shrinks the page below 100,000 characters of text (`python3 tools/agent_ready_check.py` reports the largest page). Level pages keep the full text.
- 114 stable cards ship in `skills/good-code-review/SKILL.md` (the `stable cards:` count that `python3 tools/build.py` prints). Every level has at least one, and the incident level has one.
- Cards cover a change review and seven audit levels: function, module, service, system, codebase, production, and incident (`ls cards/audit`).
- The site builds 16 static pages, including the 404 page (the `site:` count that `python3 tools/build.py` prints) for goodcodereview.com.
- You can install the checklist as a skill (`npx skills add n0nuser/goodcodereview`) or as a Claude Code plugin.
- Every card names at least one concern in its tags (correctness, security, performance, reliability, compatibility, testing, maintainability, accessibility, usability, observability, or process), so a review can be scoped to one concern. `tools/validate.py` enforces it.
- Performance cards at every review level (`rg -l '^tags:.*performance' cards | wc -l`).
- Community files: code of conduct, security policy, support guide, issue forms, and a pull request template.
- The site reads as a checklist: each level page lists its checklist first, and the build writes `llms.txt`, `llms-drafts.txt`, and one `<level>.md` per level from the same cards.
- Frontend cards for usability and accessibility.
- Every draft card says why it is not stable in a `lacks:` line, which `tools/validate.py` checks. The site card, `llms-drafts.txt`, and `cards-drafts.json` show it, and the Drafts by what they lack page groups the drafts by reason. `docs/PROMOTION.md` gives the bar a draft must meet.
- `accessibility` and `usability` are concerns, so a review can be scoped to either one on the Concerns page.
- Human path: the home page opens with "Choose a review" and shows each level's stable and draft counts. A level with no stable cards says so on its page, on the home page, and in the nav, and gives no verdict. The nav groups the audits under one menu with 44px targets. Each page has a skip link. Copy buttons cover the home code blocks and each checklist (as markdown). A status message tells screen readers when a copy works or fails.
- The site is ready for AI agents. `python3 tools/build.py` also writes `sitemap.xml` with `lastmod`, a Markdown twin with frontmatter for every page, `_headers` (Link headers, charsets), canonical and Open Graph tags, home-page JSON-LD, About and Privacy pages, a plain-text 404, and `/.well-known/agent-skills/index.json` with the skill's sha256 digest. `llms.txt` gains a summary, a "When to use this site" paragraph, and described links. The audit is in `docs/research/agent-readiness-gaps.md`.
- `python3 tools/agent_ready_check.py` checks `site/` against those items without network access. CI does not run it.
- An incident review also checks the stable cards of the level where the cause lived, with evidence quoted from the incident text. The rule is in `SKILL.md`, `llms.txt`, and the incident page, and the build fails if it is missing.
- The footer no longer says the site is styled with good-css.com. The home page says what good-css.com is: rules for reviewing CSS.
