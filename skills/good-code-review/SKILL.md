---
name: good-code-review
description: Review code against stable cards, from a diff up to an incident. Use when asked to review, audit, or check code.
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

Each check gets `PASS`, `FAIL`, or `N/A`, with `file:line` evidence.
A `FAIL` carries the card's severity: `block`, `should-fix`, or `discuss`.

The full text for each level is in `references/<level>.md`.

## Scope by concern

Each card lists its concerns in braces: `correctness`, `security`, `performance`, `reliability`, `compatibility`, `testing`, `maintainability`, `observability`, `process`.
To review only some concerns, such as a performance-only review, check only the cards that list them.

## change

- `chg-author-hygiene` [should-fix] {process}: Self-review the diff and write the description before requesting review.
- `chg-breaking-change-taxonomy` [block] {compatibility}: Treat any observable difference in signature, return shape, error type, ordering, timing, defaults, or side effects as breaking until a consumer check says otherwise.
- `chg-expand-contract` [block] {compatibility}: Evolve shared contracts in steps: add the new form beside the old (expand), migrate every consumer, then remove the old form (contract) in a later change.
- `chg-one-concern` [should-fix] {process}: Make each change do one logical thing; if the description needs "and" between unrelated outcomes, split it.
- `chg-perf-claim-evidence` [should-fix] {performance, testing}: Back a performance claim with measured before-and-after numbers.
- `chg-refactor-separate` [should-fix] {maintainability, process}: Put refactors, renames, and reformatting in their own commit or PR, apart from behaviour changes.
- `chg-review-signal` [discuss] {process}: Do not comment on what a tool enforces or on taste with no written rule; spend comments on a few high-conviction findings, and if there are many, talk to the author.
- `chg-size-ceiling` [discuss] {process}: Split a change past about 400 changed lines or about 20 files, or say in the description why not; aim for about 200.
- `chg-tests-ship-with-change` [block] {testing}: Ship new or changed behaviour in the same change as a test that fails if the behaviour breaks; a code-only change needs a stated reason.
- `chg-verify-before-claim` [block] {testing, process}: Back every "works" or "bug" claim with something run: a repro, a test or command output.

## function

- `fn-comments-explain-why` [should-fix] {maintainability}: Write comments that give a reason, a constraint, or a trade-off; rename before commenting, and never restate what the next line does.
- `fn-fetch-only-needed-data` [should-fix] {performance}: Filter, count, and aggregate in the query, and select only the columns the code uses.
- `fn-independent-work-concurrent` [should-fix] {performance, correctness}: Start independent I/O together and wait for all of it; run calls in sequence only when one needs the result of another.
- `fn-join-dont-concat-in-loop` [should-fix] {performance}: Build a string from a loop with a builder or a join, never with repeated `+=`.
- `fn-no-blocking-call-in-async-code` [block] {performance, correctness}: Never make a blocking I/O call or run long CPU work directly in async code; use the async API or hand the work to a thread or worker.
- `fn-regex-compiled-once` [should-fix] {performance}: Compile a regular expression once, at module or startup level, and reuse it.

## module

- `mod-pooled-clients-built-once` [should-fix] {performance}: Build pooled clients once at startup and reuse them.
- `mod-yagni` [should-fix] {maintainability, process}: Add an abstraction only when the logic is reused, non-trivial, or clutters the main flow; do not build for a need that does not exist yet.

## service

- `svc-api-conditional-writes` [should-fix] {correctness}: Return an `ETag` on reads and honour `If-Match` on writes, answering 412 when the entity tag is stale.
- `svc-api-deprecation-sunset` [should-fix] {compatibility}: Before removing an endpoint, mark it `deprecated` in the spec and send `Deprecation` and `Sunset` headers, with the `Sunset` date no earlier than the `Deprecation` date.
- `svc-api-error-code-stable` [should-fix] {compatibility}: Give each error a stable machine-readable code that callers branch on, and never make them parse the message text.
- `svc-api-versioning-policy` [should-fix] {compatibility}: Write down one versioning scheme for the API, and ship no breaking change inside a version it has published.
- `svc-idempotency-key` [block] {reliability, correctness}: Make every retryable write idempotent: the caller sends a unique key, and a retry with the same key never applies the write twice.
- `svc-list-endpoint-paginates` [should-fix] {performance}: Paginate every list endpoint, with a default page size and a server-side maximum.
- `svc-retry-policy` [block] {reliability}: Retry only transient errors, with capped attempts and jittered exponential backoff.

## system

- `sys-cache-bounds-invalidation` [should-fix] {performance}: Bound every cache by size and give its entries an expiry.
- `sys-fanout-leg-deadlines` [should-fix] {performance, reliability}: Give every leg of a fan-out its own deadline, and decide in code what happens when a leg misses it: a partial result, a hedged request, or an error.
- `sys-load-shedding-bounded-queues` [block] {reliability}: Bound every queue and reject excess work cheaply.
- `sys-lock-fencing` [block] {reliability, correctness}: Check a correctness lock on the resource side (fencing token or compare-and-set), never by lock possession alone.
- `sys-migration-expand-contract` [block] {reliability, compatibility}: Run data backfills in batches, in a migration separate from the schema change.
- `sys-n-plus-one-pooling` [should-fix] {performance}: Fetch related rows in one query or batch, never one query per row.
- `sys-secrets-and-errors` [block] {security, correctness}: Fail closed: a validation or auth error must deny, never continue, and an error response must not carry internals such as stack traces, SQL or tokens.

## codebase

- `code-ci-gates` [should-fix] {process}: Require review and passing build, tests, lint, and type checks on the default branch before merge, and leave nothing mechanical to reviewer vigilance.
- `code-dead-code` [should-fix] {maintainability}: Remove unreferenced functions, commented-out code, expired flags, and orphaned files; history keeps them.
- `code-dependency-pinning` [block] {security}: Commit a lockfile with hashes and install from it in CI.
- `code-perf-budget-in-ci` [should-fix] {performance, process}: Write the performance budget down as a CI check that fails the build when it is exceeded.

## production

- `prod-canary-staged-rollout` [block] {reliability}: Roll out in stages behind a canary, and abort by rule, not by judgment.
- `prod-latency-slo-percentile` [should-fix] {performance, observability}: Define latency SLOs and alerts on high percentiles, never on the mean.
- `prod-load-test-before-launch` [should-fix] {performance, reliability}: Load test before launch, past the expected peak, with pass and fail thresholds written down.
- `prod-profile-on-demand` [discuss] {performance, observability}: Make a CPU and memory profile of a production instance obtainable, through a continuous profiler or a private profile endpoint.
