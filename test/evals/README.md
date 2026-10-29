# Skill evals

Eight small review tasks that check whether the skill changes what an agent finds and how it reports it.

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

The `eval` workflow (Actions, Run workflow) runs the same command with the repository secret `ANTHROPIC_API_KEY`; it never runs on its own. It is untested until someone starts it once.

`run` calls `claude -p`, which spends tokens, so CI runs only the grader's tests (`test/test_eval.py`). Rerun the evals after a change to the skill text in `tools/build.py`, and add a case when a reviewer reports a miss.

## Trigger evals

`test/evals/triggers.json` holds 20 queries (10 should trigger, 10 near-miss negatives) with a fixed train/validation split, as the Agent Skills guide on [optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions.md) describes. `python3 tools/eval.py triggers --split train` reports the trigger rate per query. Tune `SKILL_DESC` in `tools/build.py` on `train` and confirm on `validation`. Not yet run against a real install: it spends tokens, so start with `--runs 1`.
