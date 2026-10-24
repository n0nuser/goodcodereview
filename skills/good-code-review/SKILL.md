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
| incident | incident (no vetted cards yet) |

A level marked "no vetted cards yet" has no stable cards. Give no verdict for it. Say that there are no vetted cards for that level yet. You may list its draft cards as notes, never as `PASS` or `FAIL`.

## Verdict format

Report each check as `PASS`, `FAIL`, or `N/A` with `file:line` evidence.
A `FAIL` carries the card's severity.
Any `block` `FAIL` means request changes.
A `should-fix` or `discuss` `FAIL` goes in the review but does not block.

```
FAIL [block] chg-expand-contract - src/a.py:42 - renames the column and drops the old one in one migration
FAIL [should-fix] chg-one-concern - src/b.py:7 - a logging rewrite rides along with the bug fix
PASS chg-breaking-change-taxonomy - src/c.py:15 - no signature or return shape changes
N/A chg-perf-claim-evidence - the description makes no performance claim
```

Draft cards are never verdicts.

The full text for each level is in `references/<level>.md`.
Python pack (draft cards, not vetted): https://goodcodereview.com/pack-python.html
Glossary: https://goodcodereview.com/glossary.html
Draft cards (not vetted): https://goodcodereview.com/llms-drafts.txt

## Scope by concern

Each card lists its concerns in braces: `correctness`, `security`, `performance`, `reliability`, `compatibility`, `testing`, `maintainability`, `accessibility`, `usability`, `observability`, `process`.
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

- `fn-colour-not-sole-cue` [should-fix] {accessibility, usability}: Pair every colour that carries meaning with a second cue: text, an icon, a shape, or an underline.
- `fn-comments-explain-why` [should-fix] {maintainability}: Write comments that give a reason, a constraint, or a trade-off; rename before commenting, and never restate what the next line does.
- `fn-destructive-confirm-or-undo` [should-fix] {usability}: Make a destructive action reversible with undo, or ask the user to confirm it before it runs.
- `fn-dialog-focus-managed` [block] {accessibility, usability}: When a modal opens, move focus into it and keep Tab inside it. Make Escape close it.
- `fn-error-says-what-and-how` [should-fix] {usability, accessibility}: Show each validation error next to its field, in plain words that name what is wrong and how to fix it.
- `fn-fetch-only-needed-data` [should-fix] {performance}: Filter, count, and aggregate in the query, and select only the columns the code uses.
- `fn-focus-indicator-visible` [block] {accessibility, usability}: Keep a visible focus indicator on every focusable element. Never set `outline: none` without a replacement.
- `fn-form-control-has-label` [block] {accessibility, usability}: Tie every form control to a visible `<label>`, with `for` and a matching `id` or by wrapping it. A placeholder is not a label.
- `fn-heading-structure` [should-fix] {accessibility, usability}: Mark every heading with a real `<h1>` to `<h6>` element, not a styled `div`, `span`, or `p`.
- `fn-img-alt-text` [should-fix] {accessibility}: Give every `<img>` an `alt` attribute: text that serves the image's purpose, or `alt=""` when the image is decorative.
- `fn-independent-work-concurrent` [should-fix] {performance, correctness}: Start independent I/O together and wait for all of it; run calls in sequence only when one needs the result of another.
- `fn-join-dont-concat-in-loop` [should-fix] {performance}: Build a string from a loop with a builder or a join, never with repeated `+=`.
- `fn-keep-input-on-error` [should-fix] {usability}: After a failed validation or submit, show the form again with every value the user entered, correct or not.
- `fn-native-button-or-link` [block] {accessibility, usability}: Use `<button>` for an action and `<a href>` for navigation. Do not attach a click handler to a `div`, `span`, or `a` with no `href`.
- `fn-no-blocking-call-in-async-code` [block] {performance, correctness}: Never make a blocking I/O call or run long CPU work directly in async code; use the async API or hand the work to a thread or worker.
- `fn-no-positive-tabindex` [should-fix] {accessibility, usability}: Write the DOM in reading order and never set `tabindex` above 0.
- `fn-reduced-motion-respected` [should-fix] {accessibility, usability}: Switch off or replace large, repeating, or interaction-triggered motion when `prefers-reduced-motion: reduce` is set.
- `fn-regex-compiled-once` [should-fix] {performance}: Compile a regular expression once, at module or startup level, and reuse it.
- `fn-status-announced-live-region` [should-fix] {accessibility, usability}: Announce an async status message through a live region (`role="status"` or `role="alert"`) that is already in the markup before its text changes.

## module

- `mod-colour-tokens-meet-contrast` [should-fix] {accessibility, usability}: Make every text and background token pair meet 4.5:1 (3:1 for large text), and every border, icon, and focus colour meet 3:1 against its neighbour.
- `mod-pooled-clients-built-once` [should-fix] {performance}: Build pooled clients once at startup and reuse them.
- `mod-yagni` [should-fix] {maintainability, process}: Add an abstraction only when the logic is reused, non-trivial, or clutters the main flow; do not build for a need that does not exist yet.

## service

- `svc-api-conditional-writes` [should-fix] {correctness}: Return an `ETag` on reads and honour `If-Match` on writes, answering 412 when the entity tag is stale.
- `svc-api-deprecation-sunset` [should-fix] {compatibility}: Before removing an endpoint, mark it `deprecated` in the spec and send `Deprecation` and `Sunset` headers, with the `Sunset` date no earlier than the `Deprecation` date.
- `svc-api-error-code-stable` [should-fix] {compatibility}: Give each error a stable machine-readable code that callers branch on, and never make them parse the message text.
- `svc-api-versioning-policy` [should-fix] {compatibility}: Write down one versioning scheme for the API, and ship no breaking change inside a version it has published.
- `svc-idempotency-key` [block] {reliability, correctness}: Make every retryable write idempotent: the caller sends a unique key, and a retry with the same key never applies the write twice.
- `svc-list-endpoint-paginates` [should-fix] {performance}: Paginate every list endpoint, with a default page size and a server-side maximum.
- `svc-no-redundant-entry` [should-fix] {usability, accessibility}: Do not ask for information the user already gave in the same flow. Fill it in, or let the user pick it.
- `svc-reflow-and-zoom` [should-fix] {accessibility, usability}: Make the page usable at 320 CSS pixels wide and at 200% text zoom, with no sideways scrolling, no clipped content, and no blocked pinch-zoom.
- `svc-retry-policy` [block] {reliability}: Retry only transient errors, with capped attempts and jittered exponential backoff.
- `svc-slow-operation-shows-progress` [should-fix] {usability, accessibility}: Show that a slow action is under way, and show its progress when it runs long.

## system

- `sys-cache-bounds-invalidation` [should-fix] {performance}: Bound every cache by size and give its entries an expiry.
- `sys-consistent-ui-terms` [discuss] {usability, accessibility}: Use one label and one icon for the same action and the same concept across all screens.
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
