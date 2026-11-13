# Good Code Review

> A code review checklist for people and agents. Each stable rule cites at least three independent organisations, and every check ends in `PASS`, `FAIL`, or `N/A` with `file:line` evidence.

[![check](https://github.com/n0nuser/goodcodereview/actions/workflows/check.yml/badge.svg)](https://github.com/n0nuser/goodcodereview/actions/workflows/check.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-blue)](LICENSE-CONTENT)

Good Code Review is a set of Markdown files. An AI coding agent loads them as a "skill" (a folder of instructions it reads when you ask), or you work through them by hand. You ask for a review of your code and get back a list of verdicts, each naming a rule and a line.

![A terminal recording: an agent reviews a real pull request and prints FAIL and PASS lines with file and line evidence](docs/demo/demo.gif)

That is a real run on a pull request of mine (how it was made: [docs/demo](docs/demo/README.md)). A shorter sample, with made-up paths and lines:

```text
Verdict: request changes - change, function - 2 block, 1 should-fix FAIL, 1 PASS, 3 N/A
FAIL [block] chg-expand-contract - src/a.py:42 - renames the column and drops the old one in one migration
FAIL [block] svc-sqli-authn - src/db.py:88 - proven: builds the WHERE clause with an f-string from request.args
FAIL [should-fix] chg-one-concern - src/b.py:7 - a logging rewrite rides along with the bug fix
PASS chg-breaking-change-taxonomy - src/c.py:15 - no signature or return shape changes
N/A (applies_when does not hold): chg-chestertons-fence, chg-matches-spec, chg-reuse-before-write
```

Pick what you are reviewing (a diff, a function, a service, a whole codebase, a production setup, or an incident) and you get the checks for that level. Each check has a `FAIL` example and a `PASS` example, so a reviewer, human or agent, knows what each verdict means. Anyone can check the review afterwards, because every verdict names a card and a line.

There are 202 stable checks: 188 across the eight levels and 14 in the language packs. The site prints the live count on its home page.

## How it differs

- A linter enforces rules about syntax. These cards cover what a reviewer decides: scope, compatibility, failure handling, rollout.
- An AI reviewer brings its own judgment. Here the agent reviews against a fixed rule set, and each stable card links the published sources behind it.
- A style guide says what to do. A card says what to check and when it fails.

## Where the rules come from

Each stable check is backed by at least three independent organisations that have published the same practice. The exception is a check whose source is the maintainer's own guide, which the repository records ([ADR 0001](docs/adr/0001-creator-sources-satisfy-the-stable-floor.md)). The card links every source. The organisations include Google, Microsoft, GitHub, AWS, Stripe, Cloudflare, Mozilla, OWASP, W3C, IETF, NIST, and GOV.UK. Those organisations did not write or endorse this project. Checks with less backing stay as drafts and never decide a verdict. [docs/COVERAGE.md](docs/COVERAGE.md) maps every source to its cards.

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

## For tools and agents

Everything is static files, served without a server, an account, or a key:

- [`cards.json`](https://goodcodereview.com/cards.json) with [`cards.schema.json`](https://goodcodereview.com/cards.schema.json): every stable card. [`cards-index.json`](https://goodcodereview.com/cards-index.json) is the slim lookup table. Each level and concern also has its own file (see [docs/cards-json.md](docs/cards-json.md)).
- [`llms.txt`](https://goodcodereview.com/llms.txt): the routing table and verdict format, for an agent's first read.
- [`agent.json`](https://goodcodereview.com/agent.json), [`.well-known/ard.json`](https://goodcodereview.com/.well-known/ard.json), and [`.well-known/agent-skills/index.json`](https://goodcodereview.com/.well-known/agent-skills/index.json): discovery files.
- WebMCP: pages register read-only tools (`start_review`, `list_levels`, `list_cards`) in browsers that support it.
- A command line in [`cli/`](cli/README.md). It is not on PyPI yet, so `uvx goodcodereview` does not work today; run it from a checkout.

The only stability promise is the one in [docs/api-versioning.md](docs/api-versioning.md).

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

`cards.json` is one file with no pagination. Each level has its own file, `cards/<level>.json`, and each concern has `cards/concern-<concern>.json` and `concerns/<concern>.md`. `cards-index.json` is a slim lookup table. [docs/cards-json.md](docs/cards-json.md) says how to fetch part of it. The shape carries a `schema_version`, and [docs/api-versioning.md](docs/api-versioning.md) is the versioning policy.

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
