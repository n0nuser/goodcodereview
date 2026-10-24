# Changelog

All notable changes to this project are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

- 26 stable cards ship in `skills/good-code-review/SKILL.md` (`python3 tools/build.py`).
- Cards cover a change review and seven audit levels: function, module, service, system, codebase, production, and incident (`ls cards/audit`).
- The site builds 11 static pages (`python3 tools/build.py`) for goodcodereview.com.
- You can install the checklist as a skill (`npx skills add n0nuser/goodcodereview`) or as a Claude Code plugin.
- Every card names at least one concern in its tags (correctness, security, performance, reliability, compatibility, testing, maintainability, accessibility, usability, observability, or process), so a review can be scoped to one concern. `tools/validate.py` enforces it.
- Performance cards at every review level (`rg -l '^tags:.*performance' cards | wc -l`).
- Community files: code of conduct, security policy, support guide, issue forms, and a pull request template.
- The site reads as a checklist: each level page lists its checklist first, and the build writes `llms.txt`, `llms-drafts.txt`, and one `<level>.md` per level from the same cards.
- Frontend cards for usability and accessibility.
- `accessibility` and `usability` are concerns, so a review can be scoped to either one on the Concerns page.
- Human path: the home page opens with "Choose a review" and shows each level's stable and draft counts. A level with no stable cards, such as incident, says so on its page, on the home page, and in the nav, and gives no verdict. The nav groups the audits under one menu with 44px targets. Each page has a skip link. Copy buttons cover the home code blocks and each checklist (as markdown).
