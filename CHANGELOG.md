# Changelog

All notable changes to this project are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.2.0] - 2026-11-28

The first release under [Semantic Versioning](docs/versioning.md). Every change in detail: [docs/changelog/0.2.0.md](docs/changelog/0.2.0.md).

### Added

- Frozen releases at `/v/<version>/` with `cards.json`, its schema, and a badge. One version number covers the cards, the site, and the skill.
- 309 stable cards, up from 114 in 0.1.0.
- Guides, including a secure code review checklist and one on reviewing with AI agents. An FAQ and an audit procedure.
- A share image for each page, and a ping to IndexNow search engines after each deploy.

### Changed (breaking)

- `schema_version` of `cards.json` went from 4 to 5, and the skill's file layout changed. Large levels are split into parts.

### Fixed

- The secret-scan card and empirical mode no longer let an agent send values to a live service.
- The eval comparison says that the whole-codebase gain comes from how that task is graded.
