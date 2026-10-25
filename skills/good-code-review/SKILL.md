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

An incident review also checks the stable cards of the level where the cause lived: `change` for a bad release or migration, `function`, `module`, `service`, or `system` for code and design, and `production` for rollout, alerting, and capacity. Quote the incident text as evidence in place of `file:line`. Those `FAIL` and `PASS` lines are real verdicts, and any `block` `FAIL` still means request changes.

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
- `chg-match-codebase-pattern` [should-fix] {correctness, maintainability}: Follow the established pattern nearby.
- `chg-one-concern` [should-fix] {process}: Make each change do one logical thing; if the description needs "and" between unrelated outcomes, split it.
- `chg-perf-claim-evidence` [should-fix] {performance, testing}: Back a performance claim with measured before-and-after numbers.
- `chg-refactor-has-behaviour-pin` [should-fix] {testing, maintainability}: Pin current behaviour with a characterization test, snapshot or equivalence check before the refactor moves any structure.
- `chg-refactor-separate` [should-fix] {maintainability, process}: Put refactors, renames, and reformatting in their own commit or PR, apart from behaviour changes.
- `chg-review-signal` [discuss] {process}: Do not comment on what a tool enforces or on taste with no written rule; spend comments on a few high-conviction findings, and if there are many, talk to the author.
- `chg-size-ceiling` [discuss] {process}: Split a change past about 400 changed lines or about 20 files, or say in the description why not; aim for about 200.
- `chg-tests-ship-with-change` [block] {testing}: Ship new or changed behaviour in the same change as a test that fails if the behaviour breaks; a code-only change needs a stated reason.
- `chg-verify-before-claim` [block] {testing, process}: Back every "works" or "bug" claim with something run: a repro, a test or command output.

## function

- `fn-aria-role-has-state-and-keys` [should-fix] {accessibility}: When a native element cannot do the job, give the custom widget the state attribute and the keys its role promises.
- `fn-colour-not-sole-cue` [should-fix] {accessibility, usability}: Pair every colour that carries meaning with a second cue: text, an icon, a shape, or an underline.
- `fn-comments-explain-why` [should-fix] {maintainability}: Write comments that give a reason, a constraint, or a trade-off; rename before commenting, and never restate what the next line does.
- `fn-confine-file-path` [block] {security}: Resolve the final path and check that it stays inside the intended base directory before using it.
- `fn-csprng-for-secrets` [block] {security}: Draw every security-relevant random value from the platform CSPRNG.
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
- `fn-jwt-verify-pinned` [block] {security}: Verify the signature against a fixed list of accepted algorithms, and check `iss` and `aud`, before reading any claim.
- `fn-keep-input-on-error` [should-fix] {usability}: After a failed validation or submit, show the form again with every value the user entered, correct or not.
- `fn-native-button-or-link` [block] {accessibility, usability}: Use `<button>` for an action and `<a href>` for navigation. Do not attach a click handler to a `div`, `span`, or `a` with no `href`.
- `fn-no-blocking-call-in-async-code` [block] {performance, correctness}: Never make a blocking I/O call or run long CPU work directly in async code; use the async API or hand the work to a thread or worker.
- `fn-no-mass-assignment` [block] {security}: Bind request data to a DTO or an explicit field allowlist, never straight onto the model.
- `fn-no-native-deserialise-untrusted` [block] {security}: Parse untrusted input with a data-only format, never with a native object deserialiser.
- `fn-no-positive-tabindex` [should-fix] {accessibility, usability}: Write the DOM in reading order and never set `tabindex` above 0.
- `fn-no-raw-html-sink` [block] {security}: Write untrusted text through an encoding sink (`textContent`, auto-escaped template), never through a raw HTML sink.
- `fn-no-shell-with-input` [block] {security}: Start processes with the program and each argument as separate list items, and never through a shell string.
- `fn-object-level-authz` [block] {security}: Check that the caller may act on the specific record before returning or changing it.
- `fn-password-slow-hash` [block] {security}: Hash passwords with Argon2id (or scrypt, bcrypt, PBKDF2) and a per-password salt from the library.
- `fn-reduced-motion-respected` [should-fix] {accessibility, usability}: Switch off or replace large, repeating, or interaction-triggered motion when `prefers-reduced-motion: reduce` is set.
- `fn-regex-compiled-once` [should-fix] {performance}: Compile a regular expression once, at module or startup level, and reuse it.
- `fn-rerun-safe-after-crash` [block] {reliability}: Make a state-changing operation give the same result on a second run and after a crash at any step, by deriving each step from current state and making leftovers recognisable as stale.
- `fn-response-fields-explicit` [should-fix] {security, compatibility}: Return a response type that lists each field, never the stored model or a generic dump of it.
- `fn-status-announced-live-region` [should-fix] {accessibility, usability}: Announce an async status message through a live region (`role="status"` or `role="alert"`) that is already in the markup before its text changes.
- `fn-target-size` [should-fix] {accessibility, usability}: Make each pointer target at least 24 by 24 CSS pixels, or space it so that a 24 px circle centred on it touches no other target and no other undersized target's circle.
- `fn-tls-verify-on` [block] {security}: Leave certificate and hostname verification on in every environment that ships.

## module

- `mod-colour-tokens-meet-contrast` [should-fix] {accessibility, usability}: Make every text and background token pair meet 4.5:1 (3:1 for large text), and every border, icon, and focus colour meet 3:1 against its neighbour.
- `mod-derive-dont-duplicate` [should-fix] {compatibility, maintainability}: Derive a type, list or enum from the schema or list that owns it, or add a build check that fails when the two disagree.
- `mod-pooled-clients-built-once` [should-fix] {performance}: Build pooled clients once at startup and reuse them.
- `mod-single-writer-per-state` [should-fix] {correctness}: Let only one writer change a piece of state at a time, through a single owner, a queue that serialises the writes, or compare-and-swap, never by convention.
- `mod-vetted-crypto-only` [block] {security}: Encrypt with an authenticated mode such as AES-GCM, and never reuse a nonce under one key.
- `mod-yagni` [should-fix] {maintainability, process}: Add an abstraction only when the logic is reused, non-trivial, or clutters the main flow; do not build for a need that does not exist yet.

## service

- `svc-api-conditional-writes` [should-fix] {correctness}: Return an `ETag` on reads and honour `If-Match` on writes, answering 412 when the entity tag is stale.
- `svc-api-deprecation-sunset` [should-fix] {compatibility}: Before removing an endpoint, mark it `deprecated` in the spec and send `Deprecation` and `Sunset` headers, with the `Sunset` date no earlier than the `Deprecation` date.
- `svc-api-error-code-stable` [should-fix] {compatibility}: Give each error a stable machine-readable code that callers branch on, and never make them parse the message text.
- `svc-api-versioning-policy` [should-fix] {compatibility}: Write down one versioning scheme for the API, and ship no breaking change inside a version it has published.
- `svc-auth-throttle-generic-errors` [block] {security}: Limit failed attempts per account, and return the same message and status code whether or not the account exists.
- `svc-authz-central-deny-default` [block] {security}: Route every request through one authorization layer that denies when no rule allows it.
- `svc-bound-client-controlled-sizes` [should-fix] {security}: Cap every client-controlled size and count on the server: body bytes, string length, array items, page size and batch size.
- `svc-bounded-background-tasks` [block] {reliability, correctness}: Cap how many background tasks run at once, and never spawn one per input with no limit.
- `svc-cors-allowlist` [should-fix] {security}: Allow cross-origin access only to a fixed list of named origins, and never echo the request `Origin` header back unchecked.
- `svc-csrf-state-changing` [block] {security}: Require a CSRF token (or an equivalent header check) on every cookie-authenticated request that changes state, and never change state on GET.
- `svc-idempotency-key` [block] {reliability, correctness}: Make every retryable write idempotent: the caller sends a unique key, and a retry with the same key never applies the write twice.
- `svc-list-endpoint-paginates` [should-fix] {performance}: Paginate every list endpoint, with a default page size and a server-side maximum.
- `svc-no-redundant-entry` [should-fix] {usability, accessibility}: Do not ask for information the user already gave in the same flow. Fill it in, or let the user pick it.
- `svc-rate-limit-quota` [should-fix] {security, reliability}: Enforce a per-tenant quota on shared APIs and queues.
- `svc-reflow-and-zoom` [should-fix] {accessibility, usability}: Make the page usable at 320 CSS pixels wide and at 200% text zoom, with no sideways scrolling, no clipped content, and no blocked pinch-zoom.
- `svc-retry-policy` [block] {reliability}: Retry only transient errors, with capped attempts and jittered exponential backoff.
- `svc-session-lifecycle` [block] {security}: Issue a new session ID at login, and set `Secure`, `HttpOnly` and `SameSite` on the session cookie.
- `svc-slow-operation-shows-progress` [should-fix] {usability, accessibility}: Show that a slow action is under way, and show its progress when it runs long.
- `svc-sqli-authn` [block] {security}: Pass untrusted data to queries as bound parameters, never by string concatenation or formatting.
- `svc-timeouts` [block] {performance, reliability}: Set an explicit timeout on every remote call.
- `svc-upload-validate-store` [block] {security}: Allowlist the file type, cap the size, and store each upload under a generated name where the server will not execute it.

## system

- `sys-agent-tool-least-privilege` [block] {security, process}: Give the agent only the narrow tools and the minimal credentials its task needs.
- `sys-cache-bounds-invalidation` [should-fix] {performance}: Bound every cache by size and give its entries an expiry.
- `sys-consistent-ui-terms` [discuss] {usability, accessibility}: Use one label and one icon for the same action and the same concept across all screens.
- `sys-fanout-leg-deadlines` [should-fix] {performance, reliability}: Give every leg of a fan-out its own deadline, and decide in code what happens when a leg misses it: a partial result, a hedged request, or an error.
- `sys-load-shedding-bounded-queues` [block] {reliability}: Bound every queue and reject excess work cheaply.
- `sys-lock-fencing` [block] {reliability, correctness}: Check a correctness lock on the resource side (fencing token or compare-and-set), never by lock possession alone.
- `sys-migration-expand-contract` [block] {reliability, compatibility}: Run data backfills in batches, in a migration separate from the schema change.
- `sys-n-plus-one-pooling` [should-fix] {performance}: Fetch related rows in one query or batch, never one query per row.
- `sys-pii-minimise-retention` [should-fix] {security}: Give every store of personal or sensitive data a retention period, and delete or anonymise the data when it ends.
- `sys-prompt-injection` [block] {security}: Validate model output deterministically before code acts on it.
- `sys-secrets-and-errors` [block] {security, correctness}: Fail closed: a validation or auth error must deny, never continue, and an error response must not carry internals such as stack traces, SQL or tokens.
- `sys-ssrf` [block] {security}: Fetch a user-supplied URL only when its host matches a server-side allowlist.

## codebase

- `code-adr` [discuss] {maintainability, process}: Keep a short written record for each significant design choice (datastore, framework, deviation from a pattern) that states the context, the decision, and its consequences.
- `code-build-hermetic` [should-fix] {process}: Build from declared inputs only, so that the same source revision gives the same artifact.
- `code-ci-gates` [should-fix] {process}: Require review and passing build, tests, lint, and type checks on the default branch before merge, and leave nothing mechanical to reviewer vigilance.
- `code-consistency-drift` [discuss] {correctness, maintainability}: For each recurring concern (errors, config, HTTP clients, logging), make one pattern the standard instead of leaving several as equal peers.
- `code-dead-code` [should-fix] {maintainability}: Remove unreferenced functions, commented-out code, expired flags, and orphaned files; history keeps them.
- `code-dependency-licence-sbom` [should-fix] {security}: Generate an SBOM, and scan dependencies for known vulnerabilities on every change or on a schedule.
- `code-dependency-pinning` [block] {security}: Commit a lockfile with hashes and install from it in CI.
- `code-perf-budget-in-ci` [should-fix] {performance, process}: Write the performance budget down as a CI check that fails the build when it is exceeded.
- `code-rule-has-enforcer` [should-fix] {maintainability}: Back each rule that a type, lint or CI check could enforce with that check, not with a line in an instruction file or a repeated review comment.
- `code-secret-scan` [block] {security, process}: Scan for committed credentials, and treat any hit as leaked: revoke and replace it first.
- `code-workflow-supply-chain` [block] {security, process}: Pin every CI action to a full commit SHA.

## production

- `prod-alerts-symptoms-golden-signals` [should-fix] {observability}: Page on user-visible symptoms, such as error rate and latency, not on causes.
- `prod-canary-staged-rollout` [block] {reliability}: Roll out in stages behind a canary, and abort by rule, not by judgment.
- `prod-kill-switch-fallback` [should-fix] {reliability}: Make a risky feature switchable off without a deploy, and exercise every fallback path in test or in production on a schedule.
- `prod-latency-slo-percentile` [should-fix] {performance, observability}: Define latency SLOs and alerts on high percentiles, never on the mean.
- `prod-load-test-before-launch` [should-fix] {performance, reliability}: Load test before launch, past the expected peak, with pass and fail thresholds written down.
- `prod-profile-on-demand` [discuss] {performance, observability}: Make a CPU and memory profile of a production instance obtainable, through a continuous profiler or a private profile endpoint.

## incident

- `inc-perf-fix-has-profile-evidence` [should-fix] {performance, testing}: Tie the performance fix to evidence that names the bottleneck: a profile, a trace, or a USE check.
- `inc-rollback-path-tested` [should-fix] {reliability}: Exercise each mitigation that a runbook names (rollback, failover, flag off) on a regular schedule.
