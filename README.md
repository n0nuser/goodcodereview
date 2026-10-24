# Good Code Review

A checklist for reviewing code, for people and for agents. Every check ends in `PASS`, `FAIL`, or `N/A` with `file:line` evidence.

## Start a review

Paste this to your agent:

> Read https://goodcodereview.com/llms.txt and use it to review my code.

To install it as a skill (Claude Code, Codex, Cursor, and other tools that read `skills/<name>/SKILL.md`), run:

```
npx skills add n0nuser/goodcodereview
```

To install it as a Claude Code plugin, run:

```
/plugin marketplace add n0nuser/goodcodereview
/plugin install goodcodereview@goodcodereview
```

To review by hand, open https://goodcodereview.com, pick a level, and work through the checklist.

## Choose a starting point

- To review a change, start with `cards/change/`.
- To audit existing code, pick a level in `cards/audit/`: function, module, service, system, codebase, production, or incident.

## Verdict format

Each check gets `PASS`, `FAIL`, or `N/A`, with `file:line` evidence. A `FAIL` carries the card's severity: `block`, `should-fix`, or `discuss`.

## Contributing

Send one card per pull request. See [CONTRIBUTING.md](CONTRIBUTING.md). Agents: see [AGENTS.md](AGENTS.md).

See also [docs/COVERAGE.md](docs/COVERAGE.md), which maps sources to cards, and [docs/deploy.md](docs/deploy.md).

## Find what you need

- To report a wrong card, use the [card correction form](https://github.com/n0nuser/goodcodereview/issues/new?template=card-correction.yml).
- To propose a card, use the [card proposal form](https://github.com/n0nuser/goodcodereview/issues/new?template=card-proposal.yml), then follow [CONTRIBUTING.md](CONTRIBUTING.md).
- To report a security issue, follow [SECURITY.md](SECURITY.md).
- To get help, see [SUPPORT.md](SUPPORT.md).
- To see what changed, read [CHANGELOG.md](CHANGELOG.md). To cite this project, use [CITATION.cff](CITATION.cff).
- Everyone who takes part follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## Licence

Code (`tools/`, workflows) is under the [MIT licence](LICENSE). Content (`cards/`, `packs/`, `glossary/`, `docs/`) is under [CC BY 4.0](LICENSE-CONTENT).

Created and maintained by [Pablo González](https://pablogonzalez.me).
