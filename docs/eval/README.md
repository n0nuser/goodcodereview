# Eval results, 2026-11-15

What the skill adds on 16 review tasks, each with a planted flaw. Skill, cards and eval suite at commit [`3b71462`](https://github.com/n0nuser/goodcodereview/commit/3b71462d1a6e4153196275d4cac4e4d583b5b498) (`3b71462d1a6e4153196275d4cac4e4d583b5b498`). To reproduce or compare, check out that commit (`git checkout 3b71462`) and run `claude plugin eval . --model sonnet --runs 5 --scaffold --no-publish --trust-plugin`. The earlier 11-case run of 2026-11-12 predates it; its commit was not recorded. Runner: `claude plugin eval` (Claude Code 2.1.325), 5 runs per arm per case, with and without the skill, LLM graders judged by Haiku (the runner's default). The models are the CLI aliases `sonnet` and `haiku`. The runner does not record a resolved model ID, so none is given.

| 16 cases, 5 runs per arm | Sonnet | Haiku |
|---|---|---|
| mean score with the skill | 0.976 | 0.959 |
| mean delta (with minus without) | +0.169 | +0.158 |
| cases passed (score 1.0) | 14 | 13 |
| gains / ties / losses | 7 / 9 / 0 | 8 / 6 / 2 |
| cost | $11.96 | $0.98 |

Losses (Haiku): `audit_cli` and `clean_refactor` scored 0.8 with the skill against 1.0 without, one bad run each. Every tie is 1.0 on both arms, so those tasks are too easy to separate the arms; none is a tie below 1.0. Sonnet ties: accepted_risk, audit_cli, charge_no_idempotency, clean_refactor, host_header_reset, injected, invoice_idor, postmortem, retry_no_timeout. Haiku ties: accepted_risk, charge_no_idempotency, injected, invoice_idor, postmortem, retry_no_timeout.

## Scoring

A run's score is the share of scored graders that pass. Each grader has weight 1 and is a regex on the reply, a tool check, or an LLM judgement, so scores come in steps (0, 0.5, 0.75, 1.0). A case passes only at 1.0. Graders marked `with-only` (the `Verdict:` first line, the ledger `FAIL <card-id>` lines, whether the skill fired) are shown as indicators and are not in the score. Both arms are scored on whether the reply found the planted flaw.

Example, `sqli_no_test` (`evals/sqli_no_test`): the prompt is "Review the change in change.diff." The diff adds a search route that builds SQL with an f-string and has no tests. Scored graders: `found-svc-sqli-authn`, `found-chg-tests-ship-with-change`. One pair of replies, [with the skill](reply-sqli-with-skill.txt) and [without](reply-sqli-without-skill.txt), both score 1.0. Over the five Sonnet runs the without arm scored 0.5, 1, 1, 1, 1, so the case shows a delta of +0.1. Read the per-run numbers before claiming a lift from one case.

## Files

- [per-case-per-run.tsv](per-case-per-run.tsv): every case and run, both models, plus the earlier 11-case run.
- `raw/`: the full JSON reports (`2026-11-15-sonnet-16cases-5runs.json`, `2026-11-15-haiku-16cases-5runs.json`, the 11-case run of 2026-11-12 with 3 runs per arm, and the one-pair example).

## Earlier runs

The first 16-case run of 2026-11-15 (Sonnet, 2 runs: 6 gains, 10 ties, mean +0.17) was lost with its temporary worktree. This rerun agrees on the mean and moves one case from tie to gain. The 11-case run of 2026-11-12 (older suite and skill, mean +0.0625) is in `raw/`. In it `postmortem`, `retry_no_timeout` and `sqli_no_test` scored 0 in both arms because of a suite problem fixed later, not a model result.

## Limits

**The `coverage_codebase` gain follows from its graders.** Its prompt asks for every stable card of the codebase level, and its 22 scored graders are regexes on card ids. A run without the skill cannot know the ids, so the 1.0 gain measures whether the reply names the cards, not whether the review is better. Without that case the mean delta is +0.114 on Sonnet and +0.102 on Haiku (arithmetic on the table above, not a rerun).

The cases and graders were written by the skill's author, graders are mostly regex, and there are 16 tasks. Treat the numbers as a first look, not a benchmark. The mean delta rests on a few cases: `coverage_codebase` gains 1.0 on both models. The second model is another Claude model, because `plugin eval` runs only Claude models.
