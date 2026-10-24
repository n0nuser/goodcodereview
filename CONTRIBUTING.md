# Contributing

Send one card per pull request. Copy `cards/_template.md` into `cards/change/` or `cards/audit/<level>/`.

A card is accepted when it has:

- A rule that a reviewer can mark `FAIL` in code or config. A topic with nothing to fail goes in `glossary/`.
- A `FAIL` example and a `PASS` example.
- A why, and the best counterpoint with an answer.
- A source in `borrowed_from`, or a note of first-hand experience.
- Exactly one `level`.
- At least one concern in `tags`: `correctness`, `security`, `performance`, `reliability`, `compatibility`, `testing`, `maintainability`, `accessibility`, `usability`, `observability`, or `process`. Add topic tags such as `postgres` after it.
- Your own words. Distil sources; never paste their text.

New cards start as `status: draft`. Only `stable` cards ship in `SKILL.md`.

Run `python3 tools/validate.py` to lint the cards. Run `python3 tools/build.py` to build the site and the skill.

After a build, run `python3 tools/agent_ready_check.py` to check `site/` against the agent-readiness items in `docs/research/agent-readiness-gaps.md`. It reads files only and exits 1 on any failure. CI does not run it.

To propose or correct a card, use the [issue templates](.github/ISSUE_TEMPLATE). Before you open a pull request, read the [pull request template](.github/pull_request_template.md).
