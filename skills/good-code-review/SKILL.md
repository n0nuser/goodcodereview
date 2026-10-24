---
name: good-code-review
description: Review code against stable cards, from a diff up to an incident. Use when asked to review, audit or check code.
---

# Good Code Review

## Routing

| Input | Entry point |
|---|---|
| diff / PR | change |
| file / function | function |
| package / path | module |
| service | service |
| cross-service design doc | system |
| repo | codebase |
| release / launch | production |
| incident | incident |

## Verdict format

Per check: `PASS`, `FAIL` or `N/A`, with `file:line` evidence.
A `FAIL` carries the card severity: block, should-fix or discuss.

Full text per level: `references/<level>.md`.

## change

- `chg-author-hygiene` [should-fix]: Self-review the diff and write the description before requesting review.
- `chg-breaking-change-taxonomy` [block]: Classify the change against what callers can see: signature, return shape, error type, ordering, timing, defaults, side effects. Any observable difference is breaking until a consumer check says otherwise.
- `chg-expand-contract` [block]: Evolve shared contracts in steps: add the new form beside the old (expand), migrate every consumer, then remove the old form (contract) in a later change.
- `chg-one-concern` [should-fix]: A change does one logical thing; if the description needs "and" between unrelated outcomes, split it.
- `chg-refactor-separate` [should-fix]: Put refactors, renames and reformatting in their own commit or PR, apart from behaviour changes.
- `chg-review-signal` [discuss]: Do not comment on what a tool enforces or on taste with no written rule; spend comments on a few high-conviction findings, and if there are many, talk to the author.
- `chg-size-ceiling` [discuss]: Past about 400 changed lines or about 20 files, split the change or say in the description why not; aim for about 200.
- `chg-tests-ship-with-change` [block]: New or changed behaviour arrives in the same change as a test that fails if the behaviour breaks; a code-only change needs a stated reason.
- `chg-verify-before-claim` [block]: Back every "works" or "bug" claim with something run: a repro, a test or command output.

## function

- `fn-comments-explain-why` [should-fix]: Write comments that give a reason, a constraint or a trade-off. Never restate what the next line does. Rename before commenting.

## module

- `mod-yagni` [should-fix]: Add an abstraction only when the logic is reused, non-trivial, or clutters the main flow. Do not build for a need that does not exist yet.

## system

- `sys-lock-fencing` [block]: Check a correctness lock on the resource side (fencing token or compare-and-set), never by lock possession alone.

## codebase

- `code-ci-gates` [should-fix]: The default branch requires review and passing build, tests, lint and type checks before merge; nothing mechanical is left to reviewer vigilance.
- `code-dead-code` [should-fix]: Remove unreferenced functions, commented-out code, expired flags and orphaned files; history keeps them.
- `code-dependency-pinning` [block]: Commit a lockfile with hashes and install from it in CI.

## production

- `prod-canary-staged-rollout` [block]: Roll out in stages behind a canary, and abort by rule, not by judgment.
