# Changelog

All notable changes to this project are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

- 26 stable cards ship in `skills/good-code-review/SKILL.md` (`python3 tools/build.py`).
- Cards cover a change review and seven audit levels: function, module, service, system, codebase, production, and incident (`ls cards/audit`).
- The site builds 11 static pages (`python3 tools/build.py`) for goodcodereview.com.
- You can install the checklist as a skill (`npx skills add n0nuser/goodcodereview`) or as a Claude Code plugin.
- Every card names at least one concern in its tags (correctness, security, performance, reliability, compatibility, testing, maintainability, observability, or process), so a review can be scoped to one concern. `tools/validate.py` enforces it.
- Performance cards at every review level (`rg -l '^tags:.*performance' cards | wc -l`).
- Community files: code of conduct, security policy, support guide, issue forms, and a pull request template.
