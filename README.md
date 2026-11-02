# Good Code Review

> A code review checklist for people and agents. Each stable rule cites at least three independent organisations, and every check ends in `PASS`, `FAIL`, or `N/A` with `file:line` evidence.

[![check](https://github.com/n0nuser/goodcodereview/actions/workflows/check.yml/badge.svg)](https://github.com/n0nuser/goodcodereview/actions/workflows/check.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-blue)](LICENSE-CONTENT)

This is what a review with it looks like (card ids are real, paths and lines are made up):

```text
Verdict: request changes - change, function - 2 block, 1 should-fix FAIL, 1 PASS, 14 N/A
FAIL [block] chg-expand-contract - src/a.py:42 - renames the column and drops the old one in one migration
FAIL [block] svc-sqli-authn - src/db.py:88 - proven: builds the WHERE clause with an f-string from request.args
FAIL [should-fix] chg-one-concern - src/b.py:7 - a logging rewrite rides along with the bug fix
PASS chg-breaking-change-taxonomy - src/c.py:15 - no signature or return shape changes
N/A: 14 cards, applies_when does not hold
```

Pick what you are reviewing (a diff, a function, a service, a whole codebase, a production setup, or an incident) and you get the checks for that level. Each check has a `FAIL` example and a `PASS` example, so a reviewer, human or agent, knows what each verdict means. Anyone can check the review afterwards, because every verdict names a card and a line.

There are 141 stable checks: 127 across the eight levels and 14 in the Python pack. The site prints the live count on its home page.

## How it differs

- A linter enforces rules about syntax. These cards cover what a reviewer decides: scope, compatibility, failure handling, rollout.
- An AI reviewer brings its own judgment. Here the agent reviews against a fixed rule set, and each stable card links the published sources behind it.
- A style guide says what to do. A card says what to check and when it fails.

## Where the rules come from

The rules are curated. Each stable check is backed by at least three independent organisations that have published the same practice (or, as a recorded exception, by the maintainer's own guide: [ADR 0001](docs/adr/0001-creator-sources-satisfy-the-stable-floor.md)), and the card links every source. They include Google, Microsoft, GitHub, AWS, Stripe, Cloudflare, Mozilla, OWASP, W3C, IETF, NIST, and GOV.UK. Those organisations did not write or endorse this project. Checks with less backing stay as drafts and never decide a verdict. [docs/COVERAGE.md](docs/COVERAGE.md) maps every source to its cards.

## Quick start

Paste this to your agent:

> Read https://goodcodereview.com/llms.txt and use it to review my code.

To install it as a skill (Claude Code, Codex, Cursor, and other tools that read `skills/<name>/SKILL.md`), run:

```
npx skills add n0nuser/goodcodereview
```

After you install the skill, name it in your request, such as `/good-code-review review this PR`. An agent that is not told may review without it.

To install it as a Claude Code plugin, run:

```
/plugin marketplace add n0nuser/goodcodereview
/plugin install goodcodereview@goodcodereview
```

To review by hand, open https://goodcodereview.com, pick a level, and work through the checklist.

## Choose a starting point

- To review a change, start with `cards/change/`.
- To audit existing code, pick a level in `cards/audit/`: function, module, service, system, codebase, production, or incident.

## Scope a review

Pick concerns, topics, and levels on the [Concerns page](https://goodcodereview.com/concerns). The picks live in the address, so you can share them and agents can fetch them:

```
https://goodcodereview.com/concerns?concern=security,performance&level=function
https://goodcodereview.com/concerns.md?concern=security,performance
https://goodcodereview.com/cards.json?topic=forms
```

`concern`, `topic`, and `level` take comma-separated values or repeat. A card matches when it has any value given for each filter. `group=concern|level|topic` groups the list.

`cards.json` is one bounded file with no pagination, each level has its own file, `cards/<level>.json`, each concern has `cards/concern-<concern>.json` and `concerns/<concern>.md`, and `cards-index.json` is a slim lookup table; [docs/cards-json.md](docs/cards-json.md) gives the size budget and how to fetch part of it. The shape carries a `schema_version`, and [docs/api-versioning.md](docs/api-versioning.md) is the versioning policy.

## Verdict format

Each check gets `PASS`, `FAIL`, or `N/A`, with `file:line` evidence. A `FAIL` carries the card's severity: `block`, `should-fix`, or `discuss`.

## Contributing

Send one card per pull request. See [CONTRIBUTING.md](CONTRIBUTING.md). Agents: see [AGENTS.md](AGENTS.md).

See also [docs/COVERAGE.md](docs/COVERAGE.md), which maps sources to cards, and [docs/deploy.md](docs/deploy.md).

## Find what you need

- To report a wrong card, use the [card correction form](https://github.com/n0nuser/goodcodereview/issues/new?template=card-correction.yml).
- To propose a card, use the [card proposal form](https://github.com/n0nuser/goodcodereview/issues/new?template=card-proposal.yml), then follow [CONTRIBUTING.md](CONTRIBUTING.md).
- To promote a draft card to stable, read [docs/PROMOTION.md](docs/PROMOTION.md) and use the [promote a draft form](https://github.com/n0nuser/goodcodereview/issues/new?template=promote-draft.yml). The [Drafts by what they lack](https://goodcodereview.com/drafts) page shows what each draft needs.
- To report a security issue, follow [SECURITY.md](SECURITY.md).
- To get help, see [SUPPORT.md](SUPPORT.md).
- To see what changed, read [CHANGELOG.md](CHANGELOG.md). To cite this project, use [CITATION.cff](CITATION.cff).
- Everyone who takes part follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## Licence

Code (`tools/`, workflows) is under the [MIT licence](LICENSE). Content (`cards/`, `packs/`, `glossary/`, `docs/`) is under [CC BY 4.0](LICENSE-CONTENT).

Created and maintained by [Pablo Jesús González Rubio](https://pablogonzalez.me).
