# AGENTS.md

## Review code with this repo

1. Read `skills/good-code-review/SKILL.md`.
2. Match the input (diff, file, package, service, repo, release, or incident) to a level with the routing table (a diff also takes the levels its changed lines touch).
3. To scope the review to some concerns (for example, performance only), keep only the cards whose `{...}` list names them.
4. Check each rule for that level. The full text is in `skills/good-code-review/references/<level>.md`.
5. Report each check as `PASS`, `FAIL`, or `N/A` with `file:line` evidence. A `FAIL` carries the card's severity: `block`, `should-fix`, or `discuss`.

To audit a whole repo, service, or release, follow `skills/good-code-review/references/audit.md` (the "Audit a repo, service, or release" section of `SKILL.md` points to it): it sets the scope, the read order, the rating of a missing control, and the report shape.

Without a checkout, read https://goodcodereview.com/llms.txt.

## Mandatory specs and size budgets

Four specs bind every change. Check them before you finish:

- `site/llms.txt`: https://llmstxt.org/ (an H1, a `>` summary, headingless sections, then H2 file lists of `- [name](url): notes`, secondary links under `## Optional`) and the Chrome Lighthouse audit https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt (the file must be served without a server error, follow the spec, and be a concise summary). `python3 tools/agent_ready_check.py` item 16 checks the shape.
- `skills/good-code-review/SKILL.md`: https://agentskills.io/specification (`name` matches the directory, `description` 1 to 1024 characters, `compatibility` up to 500, body under 500 lines and about 5,000 tokens, references one level deep). `test/test_skill.py` checks the limits. The official check is `uvx --from "git+https://github.com/agentskills/agentskills#subdirectory=skills-ref" skills-ref validate skills/good-code-review`; it fetches code, so ask the maintainer before you run it.
- `site/.well-known/ard.json`: the ARD publisher spec https://agenticresourcediscovery.org/spec/ (v0.91, re-read on 2026-11-02): an `entries` array, each entry with `identifier` (`urn:air:<publisher>:[<namespace>:]<name>`), `displayName`, `type`, and exactly one of `url` or `data`, 2 to 5 `representativeQueries`, `rel="ard"` in every page head, and an `Agentmap:` line in `robots.txt`. `python3 tools/agent_ready_check.py` item 43 checks it and names the version. When the spec changes version, re-read it and update the check.
- Every page an agent may need has a clean `.md` twin at the same URL.

Progressive disclosure keeps the first read small however many cards exist. Each layer has a budget that `python3 tools/build.py` enforces and `test/test_skill.py` checks:

| Layer | Holds | Budget |
|---|---|---|
| `llms.txt` | routing, a compact verdict format, and links to everything else | 12,000 characters |
| `SKILL.md` body | routing, verdict format, an audit pointer, gotchas | 16,000 characters (about 4,000 tokens) |
| `<level>-index.md` | one line per stable card: id, severity, concerns, context, rule | 12,000 characters; past it the build splits by `context` |
| `references/<level>.md`, `references/audit.md` | full card text and the audit procedure | 70,000 characters per file |

Rules:

- Never put card text, audit prose, or draft lists into `llms.txt` or `SKILL.md`. A new card adds one line to its level index and its text to the level file, nothing else.
- Put new audit advice in `references/audit.md` (built from `AUDIT_STEPS` in `tools/build.py`), not in `SKILL.md`.
- When a budget fails, split or move detail behind a link. Do not raise the number without the maintainer's approval.
- After you change the skill text, the description, or a card the evals plant, run `python3 tools/eval.py run --mode forced --runs 1` and `python3 tools/eval.py triggers --split train --runs 1`, and say what failed. `test/evals/README.md` explains the cases. They spend tokens, so CI does not run them.
- Eval runs: ask the maintainer first, naming the case, mode, number of runs, and model. Always pass `--save <dir>` (for example `--save /tmp/evals`) so a failure can be read without a second run, and `--model sonnet` unless told otherwise. Example: `python3 tools/eval.py run --mode forced --runs 1 --model sonnet --save /tmp/evals audit_repo`. One sample is not a verdict: a single substance failure needs the saved reply read before you call it a regression.

## Contribute a card

1. Copy `cards/_template.md` to `cards/change/` or `cards/audit/<level>/`. Set `status: draft` and a `lacks:` line that says why it is not stable yet. `docs/PROMOTION.md` lists the reasons and the bar for stable.
2. Meet the acceptance rules in `CONTRIBUTING.md`: a rule that can fail, a FAIL and a PASS example, a why and a counterpoint, a source, one level, and your own words.
3. Run `python3 tools/validate.py && python3 tools/build.py`.
4. Commit the regenerated `skills/` directory. CI fails a pull request if `git diff --exit-code skills/` is dirty, and a push to `main` regenerates and commits `skills/` as a bot (`.github/workflows/sync-skills.yml`). Never edit `skills/` by hand.
5. Send one card per pull request.
