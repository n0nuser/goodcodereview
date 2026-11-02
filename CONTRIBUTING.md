# Contributing

Send one card per pull request. Copy `cards/_template.md` into `cards/change/` or `cards/audit/<level>/`.

A card is accepted when it has:

- A rule that a reviewer can mark `FAIL` in code or config. A topic with nothing to fail goes in `glossary/`.
- A `FAIL` example and a `PASS` example.
- A why, and the best counterpoint with an answer.
- A source in `borrowed_from`, or a note of first-hand experience. A stable card needs three organisations, or one source by the creator ([ADR 0001](docs/adr/0001-creator-sources-satisfy-the-stable-floor.md)). Any other person's blog or talk is a reference and does not count as an organisation.
- Exactly one `level`.
- At least one concern in `tags`: `correctness`, `security`, `performance`, `reliability`, `compatibility`, `testing`, `maintainability`, `accessibility`, `usability`, `observability`, or `process`. Add topic tags such as `postgres` after it.
- Your own words. Distil sources; never paste their text.

New cards start as `status: draft`, with a `lacks:` line that says why the card is not stable yet. Only `stable` cards ship in `SKILL.md`. [docs/PROMOTION.md](docs/PROMOTION.md) gives the bar a draft must meet to become stable, and the reasons `lacks:` accepts.

A stable card or glossary entry must not name a draft card id. `tools/validate.py` fails if one does. When you promote a draft to stable, add back the links to it that stable cards and glossary entries dropped.

A card may carry `context: [ui]`, `[server]`, `[data]`, or `[cli]` (a list from that closed set) when it applies only to inputs that have that part. A reviewer marks the whole group `N/A` when the input has none. Leave it out when the rule fits any code.

A draft card has `severity: should-fix` or `discuss`, never `block`. Set the card's own severity when you promote it.

Run `python3 tools/validate.py` to lint the cards. Run `python3 tools/build.py` to build the site and the skill.

After a build, run `python3 tools/agent_ready_check.py` to check `site/` against the agent-readiness items in `docs/research/agent-readiness-gaps.md`. It reads files only and exits 1 on any failure. CI runs it after the build.

## Check your change

Set up once: `uv sync --locked` (Python dev tools from `uv.lock`) and `npm ci` (axe-core and jsdom). The build itself needs neither; it uses only the standard library. Then run what CI runs:

```
python3 tools/validate.py && python3 tools/build.py      # --dry-run prints what would change and writes nothing
uv run ruff check tools test && uv run mypy && uv run pytest -q
node --test test/worker.test.mjs
python3 tools/check_links.py                              # relative links and anchors in tracked Markdown
uv run python tools/sbom.py --check                       # sbom.cdx.json is current; every component has a licence
node test/a11y.mjs                                        # axe-core on index, function, and concerns pages of the built site
```

`node test/a11y.mjs [page.html ...]` checks other built pages. It runs in jsdom, which does no layout, so it skips the colour-contrast rule. When you change a dependency, run `uv run python tools/sbom.py` and commit the new `sbom.cdx.json`. [docs/python-pack-conformance.md](docs/python-pack-conformance.md) shows how the Python here meets the Python pack.

To propose or correct a card, use the [issue templates](.github/ISSUE_TEMPLATE). Before you open a pull request, read the [pull request template](.github/pull_request_template.md).
