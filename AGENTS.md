# AGENTS.md

## Review code with this repo

1. Read `skills/good-code-review/SKILL.md`.
2. Route the input (diff, file, package, service, repo, release, incident) to its level with the routing table.
3. Check each rule for that level; full text is in `skills/good-code-review/references/<level>.md`.
4. Report per check: `PASS`, `FAIL` or `N/A` with `file:line` evidence. A `FAIL` carries the card severity: `block`, `should-fix` or `discuss`.

Without a checkout, read https://goodcodereview.com/llms.txt.

## Contribute a card

1. Copy `cards/_template.md` to `cards/change/` or `cards/audit/<level>/`. Start with `status: draft`.
2. Meet the acceptance rules in `CONTRIBUTING.md` (failable rule, FAIL and PASS example, why and counterpoint, source, one level, own words).
3. Run `python3 tools/validate.py && python3 tools/build.py`.
4. `skills/` is generated: commit the regenerated output; CI fails if `git diff --exit-code skills/` is dirty. Never edit it by hand.
5. One card per pull request.
