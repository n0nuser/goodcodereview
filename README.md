# Good Code Review

What to check when reviewing code, for people and for agents. Every check ends in `PASS`, `FAIL` or `N/A` with `file:line` evidence.

## 30 seconds

**Paste this to your agent:**

> Read https://goodcodereview.com/llms.txt and use it to review my code.

**Install as a skill** (Claude Code, Codex, Cursor and others that read `skills/<name>/SKILL.md`):

```
npx skills add n0nuser/goodcodereview
```

**Claude Code plugin:**

```
/plugin marketplace add n0nuser/goodcodereview
/plugin install goodcodereview@goodcodereview
```

**By hand:** open https://goodcodereview.com, pick a level, and tick through the checklist.

## Two front doors

- **Reviewing a change?** Start with `cards/change/`.
- **Auditing code that already exists?** Pick a level in `cards/audit/`: function, module, service, system, codebase, production, incident.

## Verdict format

Per check: `PASS`, `FAIL` or `N/A`, with `file:line` evidence. A `FAIL` carries the card's severity: `block`, `should-fix` or `discuss`.

## Contributing

One card per pull request. See [CONTRIBUTING.md](CONTRIBUTING.md). Agents: see [AGENTS.md](AGENTS.md).

More: [docs/COVERAGE.md](docs/COVERAGE.md) (source-to-card map), [docs/deploy.md](docs/deploy.md).

## Licence

Code (`tools/`, workflows): [MIT](LICENSE). Content (`cards/`, `packs/`, `glossary/`, `docs/`): [CC BY 4.0](LICENSE-CONTENT).

Created and maintained by [Pablo González](https://pablogonzalez.me).
