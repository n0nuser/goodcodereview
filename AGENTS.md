# AGENTS.md

## Review code with this repo

1. Read `skills/good-code-review/SKILL.md`.
2. Match the input (diff, file, package, service, repo, release, or incident) to a level with the routing table.
3. To scope the review to some concerns (for example, performance only), keep only the cards whose `{...}` list names them.
4. Check each rule for that level. The full text is in `skills/good-code-review/references/<level>.md`.
5. Report each check as `PASS`, `FAIL`, or `N/A` with `file:line` evidence. A `FAIL` carries the card's severity: `block`, `should-fix`, or `discuss`.

Without a checkout, read https://goodcodereview.com/llms.txt.

## llms.txt follows llmstxt.org

`site/llms.txt` follows https://llmstxt.org/ completely, and `python3 tools/build.py` writes it. Keep it that way:

- An H1 with the site name, then a `>` blockquote summary, then sections with no headings, then H2 sections.
- Every H2 section is a file list: `- [name](url): notes`. Each stable card is a link to its level file, `[id](https://goodcodereview.com/<level>.md#<id>): [severity] {concerns}: rule`.
- Secondary links go under the last section, `## Optional`.
- The file stays small enough to fit in context; the detail lives in the level files behind the links. The spec sets no size limit, and `tools/agent_ready_check.py` item 16 checks the shape.
- Every page that agents may need also has a clean `.md` twin at the same URL.

## Contribute a card

1. Copy `cards/_template.md` to `cards/change/` or `cards/audit/<level>/`. Set `status: draft` and a `lacks:` line that says why it is not stable yet. `docs/PROMOTION.md` lists the reasons and the bar for stable.
2. Meet the acceptance rules in `CONTRIBUTING.md`: a rule that can fail, a FAIL and a PASS example, a why and a counterpoint, a source, one level, and your own words.
3. Run `python3 tools/validate.py && python3 tools/build.py`.
4. Commit the regenerated `skills/` directory. CI fails if `git diff --exit-code skills/` is dirty. Never edit `skills/` by hand.
5. Send one card per pull request.
