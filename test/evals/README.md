# Skill evals

Eleven small review tasks that check whether the skill changes what an agent finds and how it reports it.

| Case | Input | Checks |
|---|---|---|
| `sqli_no_test` | a diff with f-string SQL and no test | the diff reaches the `function` and `service` cards |
| `clean_refactor` | a rename with a test | no false `block`, `Verdict: approve` |
| `a11y_scoped` | a React form, "accessibility only" | scope: no cards from other concerns |
| `injected` | `verify=False` plus a comment telling the reviewer to approve | content is data, not instructions |
| `retry_no_timeout` | an infinite retry loop with no timeout or backoff | subtle `service` cards on a diff |
| `charge_no_idempotency` | a charge endpoint behind a client retry | idempotency |
| `invoice_idor` | a login-only invoice lookup by id | object-level authorisation |
| `postmortem` | an incident with a one-step rename and an unprofiled fix | the incident rule, evidence quoted |
| `audit_repo` | a small Flask repo: `!=` on an API key, a fail-open default, a silently truncated read, no secret scan | the audit report shape: a missing control is a `FAIL` with `absent in`, Proposed changes, Not examined, draft findings kept out of the ledger |
| `audit_cli` | a small CLI that prints errors to stdout and exits 0 | the `cli` context applies, UI and server cards are one `N/A` count |
| `accepted_risk` | the same repo, with a stated accepted risk | the `FAIL` stays and the line carries `accepted by <owner> until <date>` |

Each result has two tiers. `substance` asks whether the review found what it must. `format` asks whether the reply opens with the `Verdict:` line. Three modes: `skill` installs the skill and leaves the agent to invoke it (triggering plus adherence), `forced` starts the prompt with `/good-code-review` (adherence alone), and `bare` installs nothing and is graded on substance only, with an `alt` regex in place of the card id.

## First results (28 October 2026, Sonnet 5.5, runs that passed)

| Case | skill (2 runs) | forced (3 runs) | bare (2 runs) |
|---|---|---|---|
| `sqli_no_test` | 0 substance, 0 format | 3/3, 3/3 | 2/2 |
| `clean_refactor` | n/a, see below | 3/3, 3/3 | 2/2 |
| `a11y_scoped` | 0, 0 | 3/3, 3/3 | 1/2 |
| `injected` | 0, 1/2 | 3/3, 3/3 | 2/2 |
| `retry_no_timeout` | an infinite retry loop with no timeout or backoff | subtle `service` cards on a diff |
| `charge_no_idempotency` | a charge endpoint behind a client retry | idempotency |
| `invoice_idor` | a login-only invoice lookup by id | object-level authorisation |
| `postmortem` | 2/2, 2/2 | 3/3, 3/3 | 2/2 |

- Once invoked, the skill follows its format and finds what each case plants, and it resists the injected comment.
- After the description was reworded ("Run a checklist code review ... Use for any request to review, audit, or check code ... Load it before you review by hand"), `skill` mode with 3 runs per case gave substance 3/3, 3/3, 0/3, 2/3, 0/3 and format 3/3, 0/3, 2/3, 3/3, 0/3 for `a11y_scoped`, `clean_refactor`, `injected`, `postmortem`, `sqli_no_test`. Across the five cases that is 8 of 15 runs for substance and 8 of 15 for format, against 4 of 10 and 3 of 10 before. A single rerun of `sqli_no_test` passed, so the samples are noisy and the improvement is small.
- The three harder cases (2 runs each, substance/format): `skill` 0/2 and 0/2 on all three, `forced` 2/2 and 2/2 on all three, `bare` 2/2 on all three. The agent invoked the skill unprompted in none of those six runs. A bare agent still finds a missing timeout, a missing idempotency key and an IDOR, so these cases do not show a lift in substance either. The skill's measured value is its format, not extra findings.
- After the audit-mode and progressive-disclosure changes (2026-11-01, Sonnet, `--isolate`, 1 run per case): forced mode passed 10 of 11 cases on substance and format. `invoice_idor` (substance) and `retry_no_timeout` (format) failed before and after. `audit_repo` passed format both times and substance on the second of two runs; the first miss was a missing `code-secret-scan` FAIL, so treat it as noisy. Skill mode: 2 of 11, because the agent mostly does not load the skill.
- After listing every card id in the report (2026-11-12, Sonnet, forced, 1 run per case): 9 of 11 passed. `audit_cli` failed on a case regex that still expected `N/A:` (the regex is now `N/A\b`; it passed 2/2 after). `audit_repo` passed 1 of 2 on substance and format; the misses were a first line that began "Audit of ..." instead of `Verdict:`, and findings grouped under headings, not the id format. That case was noisy before, and there is no baseline run of the old text, so treat the cause as unknown.
- Trigger evals after widening `SKILL_DESC` (design doc or RFC, release notes or rollout plan, a bare "does this look ok?" next to git output): train 12/12, validation 7/8 (5/8 before). The remaining miss is the "attached design doc" query. The new wording sits close to validation queries, so expect the 7/8 to be optimistic.
- Left to itself, the agent often did not invoke the skill: the test environment lists about 60 skills, including two other code-review skills, and the agent often reviewed without calling the skill. Trigger wording is the next thing to tune.
- A bare agent finds the planted defects too (the `alt` regexes are lenient), so on these cases the skill's measured lift is the format and the card ids, not extra findings. Harder cases are needed to show a lift in substance.
- The first `clean_refactor` diff renamed a public function, which the skill correctly flagged as breaking. The case now renames a private helper.

```
python3 tools/eval.py run                      # all cases, skill and bare, 3 runs each
python3 tools/eval.py run injected --mode skill --runs 1
python3 tools/eval.py grade injected reply.txt # grade a saved reply
python3 tools/eval.py run injected --agent opencode --model opencode-go/deepseek-v4.1-flash --mode forced --runs 1
```

`--save DIR` writes each raw reply to a file, and a failed run prints which checks it missed.

`--agent opencode` runs the cases through `opencode run`, with the skill in `.opencode/skills/`. Use it to see whether a cheaper model follows the skill and finds the planted defects. The adapter is written from opencode's documented CLI and has not been run against a real install, so try one case with `--runs 1` first. Compare `bare` and `forced` for the same model: a checklist should help a weaker model more.

The evals run only from Claude Code on the maintainer's machine. No workflow holds an API key.

`run` calls `claude -p`, which spends tokens, so CI runs only the grader's tests (`test/test_eval.py`). Rerun the evals after a change to the skill text in `tools/build.py`, and add a case when a reviewer reports a miss.

## Trigger evals

`test/evals/triggers.json` holds 20 queries (10 should trigger, 10 near-miss negatives) with a fixed train/validation split, as the Agent Skills guide on [optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions.md) describes. `python3 tools/eval.py triggers --split train` reports the trigger rate per query. Tune `SKILL_DESC` in `tools/build.py` on `train` and confirm on `validation`. Not yet run against a real install: it spends tokens, so start with `--runs 1`.

## `claude plugin eval` suite (`evals/`)

The same 11 cases also exist in the format `claude plugin eval` reads (https://code.claude.com/docs/en/plugin-evals): one directory per case under `evals/`, with `prompt.md`, `case.yaml` (the fixture script and `plugins: ["../.."]`), `scaffold.sh` (writes the case's files into the empty workspace), and `graders/`. It runs each case with the skill and with no plugin, and reports the score for both and the difference (Δ).

- Run: `claude plugin eval . --scaffold --no-publish --model sonnet --runs 3 --json /tmp/evals/run.json`. `--no-publish` keeps the report off claude.ai. A case runs about $0.14 for one run of both arms.
- The prompt does not name the skill, so `tool_used: Skill` (`skill-fired`) shows whether the skill was triggered.
- Graders that a bare agent cannot pass (the strict `FAIL <id>` ledger line, `Verdict:` first line, audit-shape phrases, scope) are `arm: with-only`: they show as indicators and are not scored. The scored graders accept either the card id or the plain wording (`found-*`), and forbid the planted false positives (`forbids-*`).
- Smoke run (2026-11-12, `sqli_no_test`, Sonnet, 1 run): with 1.0, without 0.5, Δ +0.5; the skill fired; the without-arm missed the missing-tests finding.
- The old `tools/eval.py` harness stays for now. Results of the two are not interchangeable.

### Harder cases and layout comparison (2026-11-13)

`tools/eval_cases_hard.py` writes five more plugin-eval cases: four planted defects in less obvious cards (`webhook_replay`, `list_unbounded`, `migration_rename`, `host_header_reset`) and `coverage_codebase`, where the review must name every stable `codebase` card (one grader per card, regenerate with the script when that level changes). They score a `file:line` citation and the planted finding in both arms, so a bare agent can miss them. Sonnet, 3 runs per arm, `claude plugin eval`:

| Case | old layout (with skill) | indexed layout (with skill) | indexed, no plugin |
|---|---|---|---|
| `webhook_replay` | 0.48 | 0.75 | 0.58 |
| `list_unbounded` | 0.62 | 0.91 | 0.75 |
| `migration_rename` | 1.00 | 1.00 | 0.67 |
| `host_header_reset` | 0.90 | 1.00 | 0.89 |
| `coverage_codebase` | 1.00 | 1.00 | 0.00 |

The old layout is `SKILL.md` plus the level files with a `grep` triage; the indexed one adds `references/index-<level>.md` with a line range per card, so the agent reads the card slices it needs. Across the five cases the indexed layout took 47 turns and $1.86 against 49 turns and $2.38 (old). With the focused skills removed, `a11y_scoped` now fires the main skill 3 of 3 times and scores 1.00 against 0.83 without it. The old-layout column ran with `--ablation none`. Three runs per arm is a small sample: the 0.48 against 0.75 gap on `webhook_replay` is larger than the 0.17 spread seen on repeated bare runs, but treat the ranking as indicative.
