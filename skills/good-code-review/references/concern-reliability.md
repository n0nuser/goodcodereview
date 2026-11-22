# reliability cards

Every stable card that lists the `reliability` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-rollback-path` [should-fix] {reliability} change.md:L727+27: State in the description how to undo the change.

## function

- `fn-bounded-read-fails-at-cap` [should-fix] {correctness, reliability, security} function.md:L60+36: When a size cap is reached, return an error; never hand back the first N bytes as if they were the whole input.
- `fn-doc-documents-errors` [should-fix] {maintainability, reliability} function.md:L464+33: Document in the doc comment each error a public function can raise, each condition that makes it panic, and each precondition a caller must meet to call it safely.
- `fn-guard-uri-decoding` [should-fix] {reliability, correctness} <ui,server> function.md:L715+32: Wrap `decodeURIComponent` on user input in a `try`/`catch`, or parse with `URLSearchParams`, so that a malformed `%` sequence cannot throw.
- `fn-handle-rejected-promises` [should-fix] {reliability, correctness} function.md:L748+35: Handle the rejection of every promise you start: `await` it inside `try`/`catch`, end the chain with `.catch()`, or return it to a caller that does.
- `fn-rerun-safe-after-crash` [should-fix] {reliability} function.md:L1877+30: Make a state-changing operation give the same result on a second run and after a crash at any step, by deriving each step from current state and making leftovers recognisable as stale.

## module

- `py-test-hygiene` [discuss] {testing, reliability} module.md:L911+33: Keep unit tests off external I/O (the network, the shared filesystem and the database) and off the real clock, and run tests that need them in a separate, slower tier.
- `py-xdist-worker-isolated-state` [should-fix] {testing, reliability} module.md:L945+32: Under pytest-xdist, give each worker its own database or other mutable resource, keyed by `worker_id`, and build an expensive shared one once with a lock file.

## service

- `svc-api-retry-after` [should-fix] {reliability} <server> service.md:L324+30: Send `Retry-After` on every 429 and 503, and set it no earlier than the time capacity returns.
- `svc-best-effort-optional-deps` [should-fix] {reliability, observability} service.md:L566+34: Give each call to a non-critical dependency a short budget and a default, so its failure degrades the result instead of failing the critical path, and count every fallback.
- `svc-bound-inbound-concurrency` [should-fix] {reliability, performance} <server> service.md:L631+42: Cap how many requests a service handles at once with an explicit concurrency limit, and reject the excess. A timeout alone does not bound it.
- `svc-bounded-background-tasks` [block] {reliability, correctness} service.md:L674+36: Cap how many background tasks run at once, and never spawn one per input with no limit.
- `svc-circuit-breaker-bulkhead` [should-fix] {reliability} service.md:L749+26: Give each critical dependency its own concurrency limit.
- `svc-cli-destructive-dry-run` [should-fix] {reliability, maintainability} <cli> service.md:L776+52: Give a destructive command a preview flag that changes nothing and a flag that skips the confirmation prompt.
- `svc-client-paces-outgoing-calls` [should-fix] {reliability, performance} service.md:L904+40: Pace outgoing calls to a rate-limited API on the client, at a fixed rate or with a token bucket, so the client is not throttled.
- `svc-dlq` [should-fix] {reliability} <server> service.md:L1063+54: Give every consumer queue a dead-letter queue and keep a way to replay it after the fix. On an ordered queue, key the group or session to the unit that must stay ordered, so a poison message holds only its own unit.
- `svc-idempotency-key` [block] {reliability, correctness} <server> service.md:L1221+29: Make every retryable write idempotent: the caller sends a unique key, and a retry with the same key never applies the write twice.
- `svc-invalid-input-is-4xx` [should-fix] {correctness, reliability} <server> service.md:L1251+48: Check each caller-supplied value against its allowed domain (range, allowed set, an id that must exist, an encoding the code can handle) at the boundary, and answer a failed check with a 4xx, never a 5xx.
- `svc-rate-limit-quota` [should-fix] {security, reliability} <server> service.md:L1498+27: Enforce a per-tenant quota on shared APIs and queues.
- `svc-retry-policy` [block] {reliability} service.md:L1607+34: Retry only transient errors, with capped attempts and jittered exponential backoff.
- `svc-saga-steps` [should-fix] {reliability, correctness} <server> service.md:L1642+27: Make steps after the pivot idempotent and retryable, and make every compensation idempotent with a failure path.
- `svc-timeouts` [block] {performance, reliability} service.md:L1888+30: Set an explicit timeout on every remote call.
- `svc-update-rollback-on-failure` [should-fix] {reliability} service.md:L2017+43: When an update fails, restore the previous version instead of leaving a missing or half-written one.
- `py-cancellation` [should-fix] {reliability, correctness} service.md:L2162+32: Re-raise `CancelledError` (do not catch it via bare `except` or `BaseException`), and catch `TimeoutError` outside the `asyncio.timeout()` block.

## system

- `sys-cells-limit-blast-radius` [discuss] {reliability} system.md:L57+32: Split shared infrastructure into independent cells, each with its own control plane and storage, and route each tenant or request to one cell, so one failure stops only that cell.
- `sys-fanout-leg-deadlines` [should-fix] {performance, reliability} system.md:L120+28: Give every leg of a fan-out its own deadline, and decide in code what happens when a leg misses it: a partial result, a hedged request, or an error.
- `sys-health-liveness-readiness` [should-fix] {reliability} system.md:L149+25: Wire load balancers and restarters to liveness and local checks only, never to shared-dependency checks.
- `sys-load-shedding-bounded-queues` [block] {reliability} <server> system.md:L204+29: Bound every queue, reject excess work cheaply, and drop queued requests whose caller has already given up.
- `sys-lock-fencing` [block] {reliability, correctness} system.md:L234+29: Check a correctness lock on the resource side (fencing token or compare-and-set), never by lock possession alone.
- `sys-migration-expand-contract` [block] {reliability, compatibility} <data> system.md:L264+26: Run data backfills in batches, in a migration separate from the schema change.

## codebase

- `code-release-gated-on-ci` [should-fix] {reliability, process} codebase.md:L419+47: Make a release or publish job depend on the checks passing for the tagged commit, never on the tag alone.

## production

- `prod-canary-staged-rollout` [block] {reliability} production.md:L61+28: Roll out in stages behind a canary, and abort by rule, not by judgment.
- `prod-kill-switch-fallback` [should-fix] {reliability} production.md:L90+28: Make a risky feature switchable off without a deploy, and exercise every fallback path in test or in production on a schedule.
- `prod-load-test-before-launch` [should-fix] {performance, reliability} production.md:L147+27: Load test before launch, past the expected peak, with pass and fail thresholds written down.
- `prod-shadow-compare-before-cutover` [should-fix] {correctness, reliability} <data> production.md:L202+36: Before you move traffic to a new system, run it beside the old one on live or captured production traffic, diff the results, and cut over only when every mismatch is fixed or explained.
- `prod-slo-error-budget` [discuss] {reliability, observability} production.md:L239+24: Define an SLO with an indicator and window, and use its remaining error budget to gate risky releases.

## incident

- `inc-rollback-path-tested` [should-fix] {reliability} incident.md:L30+26: Exercise each mitigation that a runbook names (rollback, failover, flag off) on a regular schedule.
