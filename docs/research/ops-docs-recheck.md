# Ops docs recheck (fetched 2026-10-23)

Method: each page was fetched as full HTML, tags stripped, then read via targeted extraction (key sections, prevention/consider lists, normative sentences). Quotes are paraphrased. Tags: CHECK = a reviewer can mark FAIL in code/config/diff; CONCEPT = background, not directly markable.

## Pages read (30 fetched; 28 substantively read)

| # | URL | Org / author | One line |
|---|-----|--------------|----------|
| 1 | https://docs.python.org/3/library/asyncio-task.html | Python docs | create_task, TaskGroup, timeout(), cancellation semantics |
| 2 | https://www.postgresql.org/docs/current/sql-altertable.html | PostgreSQL | Lock level per ALTER TABLE subform; NOT VALID / VALIDATE; rewrite rules |
| 3 | https://www.postgresql.org/docs/current/sql-createindex.html | PostgreSQL | CONCURRENTLY mechanics, INVALID leftovers, no transaction block |
| 4 | https://www.postgresql.org/docs/current/runtime-config-client.html | PostgreSQL | lock_timeout, idle_in_transaction_session_timeout, defaults |
| 5 | https://www.postgresql.org/docs/current/explicit-locking.html | PostgreSQL | Lock mode conflict table (skimmed) |
| 6 | https://docs.gitlab.com/development/migration_style_guide/ | GitLab | Migration rules: post-deploy, timeouts, disable_ddl_transaction!, batched background migrations |
| 7 | https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/ | GitLab | Multi-release drop/rename/type-change procedure (ignore_column, *_concurrently helpers) |
| 8 | https://antirez.com/news/101 | antirez (Salvatore Sanfilippo) | Rebuttal "Is Redlock safe?": argues tokens unnecessary, concedes monotonic clock |
| 9 | https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html | Martin Kleppmann | The analysis antirez answers: efficiency vs correctness locks, fencing tokens |
| 10 | https://www.honeycomb.io/blog/time-to-version-observability-signs-point-to-yes | Honeycomb (first-person Charity Majors voice; byline not in extracted text) | "Observability 2.0": one store of wide structured events, aggregate at read time |
| 11 | https://aws.amazon.com/builders-library/caching-challenges-and-strategies/ | AWS Builders' Library | Cache failure modes: cold start, coherence, fallback stampede, TTLs |
| 12 | https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/ | AWS (author line not extracted) | Bimodal queue behavior, sidelining, DLQ, visibility timeout |
| 13 | https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/ | AWS | Blast radius limiting by per-tenant virtual shards |
| 14 | https://aws.amazon.com/builders-library/implementing-health-checks/ | AWS | Liveness vs local vs dependency checks; fail-open |
| 15 | https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/ | AWS | Leader election tradeoffs, leases, two-leaders tolerance |
| 16 | https://aws.amazon.com/builders-library/minimizing-correlated-failures-in-distributed-systems/ | AWS | AZs, cells, velocity controls, jitter on shared limits |
| 17 | https://aws.amazon.com/builders-library/fairness-in-multi-tenant-systems/ | AWS | Per-tenant quotas, load shedding, 429 vs 503 |
| 18 | https://sre.google/sre-book/monitoring-distributed-systems/ | Google SRE book | Symptoms vs causes, four golden signals, simple paging rules |
| 19 | https://sre.google/sre-book/release-engineering/ | Google SRE book | Hermetic reproducible builds, review of every change, branch-and-cherry-pick |
| 20 | https://sre.google/workbook/canarying-releases/ | Google SRE workbook | Canary population/duration/metric selection, auto rollback |
| 21 | https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker | Microsoft Azure Architecture Center | Closed/open/half-open, exception handling, monitoring |
| 22 | https://learn.microsoft.com/en-us/azure/architecture/patterns/retry | Microsoft | Cancel vs retry-after-delay, idempotency, aggressive retry harm |
| 23 | https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead | Microsoft | Per-dependency pools and per-consumer partitions |
| 24 | https://learn.microsoft.com/en-us/azure/architecture/patterns/saga | Microsoft | Compensable / pivot / retryable steps, idempotence |
| 25 | https://owasp.org/Top10/2025/ and /0x00_2025-Introduction/ | OWASP | Top 10:2025 list (published, not draft) |
| 26 | https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/ and A10 (Mishandling_of_Exceptional_Conditions) | OWASP | Two new categories, prevention lists |
| 27 | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | OWASP GenAI Security Project | LLM01:2025 mitigation list |
| 28 | https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md | OWASP ASVS 5.0 | V16 logging and error handling requirements |
| 29 | https://slsa.dev/spec/v1.0/levels | SLSA | Build track L0-L3 (page notes v1.2 is current) |
| 30 | https://github.com/ossf/scorecard/blob/main/docs/checks.md | OpenSSF | Scorecard check definitions and risk ratings |

OWASP Top 10:2025 list as published: A01 Broken Access Control (SSRF folded in), A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions. New in 2025: A03 (expansion of 2021 A06 Vulnerable and Outdated Components) and A10.

## Checks by theme

### Async / concurrency (Python)
- CHECK: `asyncio.create_task(...)` result discarded (bare statement, no stored reference). Docs: the event loop keeps only weak references; an unreferenced task can be garbage-collected mid-execution. FAIL unless added to a set with `add_done_callback(set.discard)` or created through a TaskGroup. [asyncio-task]
- CHECK: fire-and-forget task that is never awaited and has no done-callback surfacing exceptions. Docs: failure leaves "Task exception was never retrieved" at GC. Prefer `asyncio.TaskGroup`. [asyncio-task]
- CHECK: `except asyncio.CancelledError` (or bare `except:` / `except BaseException`) that swallows cancellation without re-raise. Docs: TaskGroup and timeout() are built on cancellation and misbehave if it is swallowed; suppressing requires `uncancel()`. [asyncio-task]
- CHECK: `await` on network/IO call outside `asyncio.timeout()` / `wait_for` / client timeout. (Docs give the mechanism; "every remote await needs a bound" is the reviewable rule.) [asyncio-task]
- CHECK: `TimeoutError` handler placed inside the `async with asyncio.timeout()` block. Docs: the conversion from CancelledError happens at context exit, so it can only be caught outside. [asyncio-task]
- CONCEPT: a task passed to `asyncio.shield()` also needs a retained reference (docs repeat the warning there).

### Postgres migrations
- CHECK: `ALTER TABLE` on a hot table with no `SET lock_timeout` in the migration/session. Docs: default is 0 = wait forever, and most ALTER forms take ACCESS EXCLUSIVE. Docs also say not to set it globally in postgresql.conf, so it belongs per session/migration. [pg-config, pg-altertable]
- CHECK: `ADD CONSTRAINT ... CHECK/FOREIGN KEY` without `NOT VALID` on a large table. Docs: the plain form scans the whole table while holding the lock; NOT VALID skips the scan. Follow-up migration must `VALIDATE CONSTRAINT` (SHARE UPDATE EXCLUSIVE, does not block writes). Missing VALIDATE step = FAIL (constraint is left unverified for old rows). [pg-altertable]
- CHECK: `ALTER COLUMN SET NOT NULL` on a large table without a proven-valid CHECK first (docs: scan is skipped only if a valid CHECK proves no NULLs; current docs also allow NOT VALID not-null). [pg-altertable]
- CHECK: `ADD COLUMN` with a volatile default (e.g. `clock_timestamp()`), generated stored column, or identity column. Docs: full table + index rewrite. Non-volatile constant default is metadata-only. [pg-altertable]
- CHECK: `CREATE INDEX` (no CONCURRENTLY) on an existing large/busy table. [pg-createindex]
- CHECK: `CREATE INDEX CONCURRENTLY` inside a transaction block or a migration wrapper that opens one (error at runtime; GitLab: needs `disable_ddl_transaction!`). [pg-createindex, gitlab-style-guide]
- CHECK: no recovery path for a failed CONCURRENTLY build. Docs: failure leaves an INVALID index that is ignored by queries but still costs write overhead; drop and retry, or `REINDEX INDEX CONCURRENTLY`. Reviewer asks for `DROP INDEX IF EXISTS` before retry or an invalid-index monitor. [pg-createindex]
- CHECK: unique index built concurrently without considering that uniqueness is enforced from the second scan on, so other transactions can see violations even if the build later fails. [pg-createindex]
- CHECK: schema change and data backfill in one transaction/one deploy. GitLab: schema in regular or post-deploy migration, data in batches; post-deploy migrations capped at about 10 minutes, concurrent index ops 20 minutes; large data migrations go to batched background migrations that must not change schema. [gitlab-style-guide]
- CHECK: column drop/rename/type change shipped in one release. GitLab procedure: stop code using it (`ignore_column`), drop in post-deploy in a later release, rename via add-copy-cleanup helpers across milestones, keep `ignore_column` until the release after. [gitlab-avoiding-downtime]
- CONCEPT: lock mode conflict table (explicit-locking). Useful for explaining why one queued ACCESS EXCLUSIVE blocks all later readers; the queueing consequence is standard Postgres behavior but was not stated in a sentence I extracted, so treat as inference.
- CONCEPT: only FK, CHECK, not-null accept NOT VALID; unique/PK need a concurrently built unique index then `ADD CONSTRAINT ... USING INDEX` (the USING INDEX route is in the ALTER TABLE page, not independently verified here).

### Distributed locks / leaders
- CHECK: a lock with TTL guarding a write to an external store, with no fencing token or compare-and-set on the write. Kleppmann: correctness locks need a monotonically increasing token checked by the storage. antirez: a unique random token with check-and-set on the resource is an alternative. Either way, "lock held => safe to write" with no resource-side check is FAIL for correctness use. [kleppmann, antirez]
- CHECK: lock used for correctness but implemented as single Redis `SET NX PX` or Redlock with no fencing. Kleppmann says Redlock produces no monotonic token; antirez concedes Redlock should use monotonic time. [both]
- CHECK: code does not re-check remaining lock validity after acquisition and before the critical work (antirez's step 3-4: time-after-acquire minus start must leave validity). [antirez]
- CHECK: leader work not safe with two leaders (non-idempotent) when lease-based election is used. AWS: exactly-one leader cannot be guaranteed; design for overlap, use idempotence, check lease before acting, stop work when the lease cannot be renewed. [aws-leader]
- CONCEPT: efficiency lock vs correctness lock (Kleppmann). Reviewer should ask which one it is. AWS also says to first consider idempotent APIs / optimistic locking instead of leaders.

### Queues, caches, overload (AWS)
- CHECK: queue consumer with no DLQ / max receive count, or DLQ with no alarm on depth > 0. [aws-queues]
- CHECK: no age-of-oldest-message (or age-of-first-attempt) metric or alarm; only depth. [aws-queues]
- CHECK: processing longer than visibility timeout with no extension; also latency growth during overload crossing the timeout causing duplicate work. [aws-queues]
- CHECK: shared queue with no per-tenant rate limit / no concurrency cap per workload (semaphore or per-workload pool). [aws-queues, aws-fairness]
- CHECK: no way to sideline old or excess messages (spillover queue, drop old deltas) for a backlog. [aws-queues]
- CHECK: retries without jitter or with synchronized timers/TTLs across a fleet. AWS correlated failures: add jitter to retries, varied thresholds, varied limits (pool size, heap). [aws-correlated]
- CHECK: operator or deploy tool that acts on many hosts at once with no velocity control or feedback loop. [aws-correlated]
- CHECK: cache with fixed arbitrary TTL/size, no hit/miss/downstream-request metrics. [aws-caching]
- CHECK: cache miss path falls through to dependency with no rate cap or request coalescing (thundering herd, cold start after deploy). AWS tests with cache disabled. [aws-caching]
- CHECK: cached value format has no version field; new code cannot read old entries and old code cannot read new ones. [aws-caching]
- CHECK: cache client treats cache outage as fatal, or fallback to origin is unbounded. [aws-caching]
- CHECK: health check endpoint that tests shared dependency (DB) and is wired to the load balancer or auto-replacement. AWS: LB should use liveness + local checks only; dependency checks go to monitoring/alarms; fail-open behavior must be tested. [aws-health]
- CHECK: server auto-removes itself on dependency failure (fleet-wide self-eviction risk). [aws-health]
- CHECK: no per-tenant/per-key quota on a multi-tenant API; over-quota returns 503 (capacity) instead of 429 (quota). AWS notes older AWS services return 503 for historical reasons. [aws-fairness]
- CONCEPT: shuffle sharding (aws-shuffle): with 8 workers and 2-worker virtual shards there are 28 combinations; a tenant's bad requests hit only its shard. Reviewable form: tenant-to-shard assignment exists at all, versus every tenant on every worker.
- CONCEPT: load shedding should be cheap; AWS sometimes slows fast errors to match success latency so LBs do not route more traffic to a shedding host.

### Resilience patterns (Azure)
- CHECK: retry loop on non-idempotent operation without idempotency key. [azure-retry]
- CHECK: retry with fixed zero/short delay, unbounded attempts, or retry on non-transient errors (should cancel). Also retries stacked at multiple layers (stated as a consideration, multiplicative). [azure-retry]
- CHECK: remote call with retries but no circuit breaker or fast-fail path, or a breaker without half-open limited probing. [azure-circuit-breaker]
- CHECK: breaker with no metrics/log on state changes; breaker blocking concurrent calls with a coarse lock. [azure-circuit-breaker]
- CHECK: all dependencies share one connection/thread pool (no bulkhead); a slow dependency exhausts it. [azure-bulkhead]
- CHECK: saga step after the pivot that is not idempotent/retryable; compensating action that can fail with no handling; no unique saga/correlation id. [azure-saga]
- CONCEPT: breaker vs retry have opposite purposes (retry assumes eventual success, breaker prevents futile attempts). Saga data anomalies due to missing cross-service isolation.

### Observability / release
- CHECK: request handler emits many narrow log lines but no single wide event per request with high-cardinality fields (user/tenant id, build id, flag state, trace id). This is Honeycomb's position, a vendor opinion; see Disagreements. [honeycomb]
- CHECK: metric labeled with unbounded values (user id, request id). Honeycomb: metrics cannot hold high cardinality and cost scales by it. [honeycomb]
- CHECK: deploy/flag change not recorded as a field/marker on emitted telemetry, so before/after comparisons are impossible. [honeycomb]
- CHECK: alert pages on a cause (CPU high) rather than a symptom; alert rules not tied to a user-visible symptom; no four golden signals (latency, traffic, errors, saturation) on a service; latency tracked as a mean only (SRE book says use bucketed distributions); failed-request latency mixed with successful. [sre-monitoring]
- CHECK: alert or collected signal that nothing uses or that never fires (SRE: candidates for removal; rules not exercised for a quarter). [sre-monitoring]
- CHECK: build not hermetic or reproducible (depends on host-installed tools, floating versions); release not tied to a specific revision; no review of changes in a release. [sre-release]
- CHECK: rollout goes to 100% at once with no canary population, no automatic comparison of canary vs control on a small set of metrics (workbook suggests at most about a dozen, stack-ranked), no abort/rollback rule. Canary too short or too small to be representative. [sre-canary]
- CONCEPT: canary arithmetic: 20% errors on 5% of traffic is 1% overall error; ties canary size to SLO budget.

### Security / supply chain / LLM
- CHECK (OWASP A10:2025): `catch`/`except` that swallows errors and continues (fail open); partially completed multi-step operation with no rollback (debit/credit/log example); resources not released in the error path; no global/last-resort handler. [owasp-a10, asvs-v16]
- CHECK (ASVS 5.0 16.5.1): error responses returning stack traces, SQL, keys or tokens. [asvs]
- CHECK (ASVS 16.5.2-16.5.4): no degradation path when an external resource fails; no last-resort handler; fail-open on validation exceptions. [asvs]
- CHECK (ASVS 16.4.1, 16.2.5): log lines concatenating user input without encoding (log injection); sensitive data (credentials, payment details) logged. [asvs]
- CHECK (A03:2025): no lockfile / unpinned dependency versions; no SBOM or dependency-vulnerability scan in CI; packages not from official sources; updates auto-rolled to all systems at once (OWASP advises staged rollouts or canaries). [owasp-a03]
- CHECK (Scorecard Pinned-Dependencies): GitHub Actions referenced by tag/branch instead of full commit SHA. [scorecard]
- CHECK (Scorecard Token-Permissions): workflow with no top-level `permissions:` block or with broad write at top level (risk High). [scorecard]
- CHECK (Scorecard Dangerous-Workflow, risk Critical): `pull_request_target` or `workflow_run` workflow that checks out PR code; untrusted `${{ github.event... }}` interpolated into `run:` scripts; secrets/context logged. [scorecard]
- CHECK (Scorecard others): no dependency-update tool config, no SECURITY.md, binaries committed, release without signature, no branch protection/code review. [scorecard]
- CHECK (SLSA): release artifacts with no provenance. L1 = provenance exists; L2 = signed provenance from a hosted build platform; L3 = hardened build platform. [slsa]
- CHECK (OWASP LLM01:2025): model output or retrieved/external text executed or acted on without validation; tools/API tokens handed to the model instead of held in code; high-risk action (delete, send, pay) without human approval; no deterministic validation of expected output format; untrusted content not segregated/labelled in the prompt. OWASP states there may be no fool-proof prevention and that RAG/fine-tuning do not fully mitigate injection, so these reduce impact only. [llm01]
- CONCEPT: prompt injection vs jailbreaking distinction.

## Corrections to earlier claims

1. "Python event loop holds only weak references to tasks, keep a strong reference": CONFIRMED verbatim in the `asyncio.create_task` docs (Important note: save a reference, the loop keeps only weak references, a task may be garbage collected "at any time, even before it's done"). Additions: (a) the docs' recommended fix is a module/instance set plus `add_done_callback(background_tasks.discard)`; (b) that set approach still never retrieves exceptions, so docs recommend `TaskGroup` (strong refs, awaits, propagates as ExceptionGroup); (c) the same warning appears again on `asyncio.shield` ("tasks passed to this function"). The docs section on this was labelled as changed in 3.14 only for eager_start, not for this note.
2. Postgres:
   - `lock_timeout` default is 0, which disables it (confirmed). It applies per lock acquisition, to explicit and implicit locks, and docs advise against setting it in postgresql.conf because it affects all sessions. Also: with nonzero statement_timeout, lock_timeout >= statement_timeout is pointless.
   - NOT VALID then VALIDATE: confirmed, but scope is narrower/wider than often stated. Applies to foreign key, CHECK, and (in current docs) not-null constraints only. ADD FOREIGN KEY takes SHARE ROW EXCLUSIVE (on both tables), other ADD CONSTRAINT forms ACCESS EXCLUSIVE; VALIDATE CONSTRAINT takes SHARE UPDATE EXCLUSIVE. Constraint is enforced on new writes immediately after NOT VALID, which is the safe-to-ship property. NOT VALID is not instant-and-lock-free: the ADD still needs its lock briefly, so pair with lock_timeout (that pairing is my inference, consistent with GitLab's practice of setting lock timeouts).
   - CONCURRENTLY can leave invalid indexes: confirmed (deadlock or unique violation during scan). Docs: invalid index ignored for queries but still adds update overhead; shown as INVALID in `\d`; recover by DROP and retry or `REINDEX INDEX CONCURRENTLY`. Extra facts: needs two table scans and waits for older transactions, cannot run in a transaction block, only one concurrent build per table at a time.
3. AWS caching page: advises testing with cache disabled to confirm dependency protections work; earlier summaries that said only "use TTLs" miss the soft-TTL/hard-TTL pattern and the stampede rule.
4. OWASP Top 10: the current list is 2025 (not 2021). A10:2025 Mishandling of Exceptional Conditions and A03:2025 Software Supply Chain Failures are new/expanded; SSRF is no longer separate (rolled into A01). Any check text citing 2021 numbering (A06 Vulnerable Components, A10 SSRF) is stale.
5. SLSA: the page I fetched (v1.0 path) states v1.2 is current; v1.0+ has only a Build track (Source track dropped, older 1-4 numbering retired). L4 does not exist in this scheme.

## Disagreements

- antirez vs Kleppmann on Redlock. Kleppmann: Redlock is unsafe for correctness because it depends on timing assumptions and issues no fencing token. antirez: random unique token plus check-and-set is enough; process pauses after validity re-check affect all TTL locks equally; ordered tokens need a linearizable store. Agreed: Redlock implementations should use a monotonic clock; locks used only for efficiency can be loose. A reviewer should not assert Redlock "is safe" or "is broken" as settled; the defensible check is "correctness-critical write is guarded on the resource side."
- Honeycomb (vendor) says wide events are the single source of truth and metrics are a "bridge to our past." Google SRE book says to favor simple metrics-based paging rules and avoid magic; AWS Builders' Library also emphasizes metrics and alarms (queue age, hit rate). These are not strictly contradictory (alerts vs exploration), but Honeycomb's "no more metrics" stance is marketing-adjacent and should not be a FAIL criterion. Only the structural checks (wide event per request, bounded metric labels) are defensible without taking a side.
- AWS leader election page recommends avoiding leader election if idempotent APIs or optimistic locking suffice, while Kleppmann/antirez discuss making locks safe. Direction differs: avoid vs harden.
- AWS health-check page: fail-open is useful but AWS says it is skeptical of behavior it cannot fully test; do not mark "has fail-open LB" as PASS by itself.

## Not found / not done

- Honeycomb "There are no three pillars" post returned an empty page (JS rendered); no second Honeycomb page read. No separate Charity Majors "wide events" post read, so wide-event guidance rests on one page (the Observability 2.0 post). Author byline was not in the extracted text; attribution to Charity Majors is from the first-person voice and not confirmed from the page.
- OWASP LLM Top 10 index page returned little text; only LLM01 read in full. LLM10:2025 Unbounded Consumption appears in the index but was not read.
- OWASP ASVS: only V16 (5.0 branch, raw markdown) read, not V1-V15, and not the general ASVS landing page. 5.0 numbering differs from 4.0 (e.g. error handling was V7 in 4.0).
- GitHub gh-ost, Braintree, Stripe, Shopify zero-downtime posts: not fetched (GitLab used as the primary write-up). 
- Azure DLQ pattern: not fetched as a page (no dedicated Azure pattern page was read; DLQ guidance comes from the AWS queue backlog article).
- AWS queue backlog article author line and Postgres explicit-locking page details were skimmed only.
- Not independently checked: PG `ADD CONSTRAINT ... USING INDEX` for unique/PK promotion, and the lock-queueing consequence of ACCESS EXCLUSIVE waits (inference).
