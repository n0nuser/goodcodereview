# AGENTS.md

## Review code with this repo

1. Read `skills/good-code-review/SKILL.md`.
2. Match the input (diff, file, package, service, repo, release, or incident) to a level with the routing table.
3. Check each rule for that level. The full text is in `skills/good-code-review/references/<level>.md`.
4. Report each check as `PASS`, `FAIL`, or `N/A` with `file:line` evidence. A `FAIL` carries the card's severity: `block`, `should-fix`, or `discuss`.

Without a checkout, read https://goodcodereview.com/llms.txt.

## Contribute a card

1. Copy `cards/_template.md` to `cards/change/` or `cards/audit/<level>/`. Set `status: draft`.
2. Meet the acceptance rules in `CONTRIBUTING.md`: a rule that can fail, a FAIL and a PASS example, a why and a counterpoint, a source, one level, and your own words.
3. Run `python3 tools/validate.py && python3 tools/build.py`.
4. Commit the regenerated `skills/` directory. CI fails if `git diff --exit-code skills/` is dirty. Never edit `skills/` by hand.
5. Send one card per pull request.
