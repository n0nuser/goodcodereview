# Coverage triage: 111-topic list

Each row is a CHECK (a reviewer can mark FAIL in code, config or diff) or a CONCEPT (glossary entry in `glossary/`). Sources are the notes in `docs/research/`. Rows 51b, 81b-d, 82 and X1-X15 are additions to the 111. Ids with no research source stay `status: draft`.

Counts: 52 CHECK rows (51 unique ids), 79 CONCEPT rows.

| # | Item | Type | Proposed check or glossary id | Level | Note |
|---|---|---|---|---|---|
| 1 | Rate Limiting | CHECK | `svc-rate-limit-quota` | service | FAIL if a multi-tenant API has no per-tenant quota, or returns 503 instead of 429 when a tenant is over quota. |
| 2 | Caching | CHECK | `svc-cache-miss-protection` | service | FAIL if a cache miss falls through to the dependency with no request coalescing or rate cap, or a cache outage is fatal to the caller. |
| 3 | Load Balancing | CONCEPT | `load-balancing` | - | Glossary only; the reviewable part is health-check scope. |
| 4 | Reverse Proxies | CONCEPT | `reverse-proxies` | - | No reviewable rule in the research. |
| 5 | API Gateways | CONCEPT | `api-gateways` | - | No reviewable rule in the research; rate limits go to svc-rate-limit-quota. |
| 6 | CI/CD | CHECK | `code-ci-workflow-hardening` | codebase | FAIL if a workflow pins actions by tag or branch, lacks a top-level permissions block, or runs PR code from a pull_request_target trigger. |
| 7 | Docker | CONCEPT | `docker` | - | Reviewable part is build reproducibility (code-build-hermetic). |
| 8 | Kubernetes | CONCEPT | `kubernetes` | - | Reviewable parts are probes and rollout (svc-health-check-scope, prod-rollout-velocity). |
| 9 | Service Discovery | CONCEPT | `service-discovery` | - | No reviewable rule in the research. |
| 10 | Circuit Breakers | CHECK | `svc-circuit-breaker` | service | FAIL if a remote call retries with no breaker or fast-fail path, or the breaker has no half-open probing or state-change metric. |
| 11 | Timeouts | CHECK | `svc-timeouts` | service | FAIL if a call over a network or process boundary has no explicit time bound. |
| 12 | Retries | CHECK | `svc-retry-policy` | service | FAIL if a retry loop is unbounded, has no delay, retries non-transient errors, or stacks with retries at another layer. |
| 13 | Exponential Backoff | CHECK | `svc-retry-jitter` | service | FAIL if retries or fleet-wide timers/TTLs run without jitter. |
| 14 | Idempotency | CHECK | `svc-idempotency-key` | service | FAIL if a retried or redelivered operation is non-idempotent and carries no idempotency key. |
| 15 | Message Queues | CHECK | `svc-queue-visibility-timeout` | service | FAIL if processing can outlast the visibility timeout with no extension, so overload causes duplicate work. |
| 16 | Pub/Sub | CONCEPT | `pub-sub` | - | Reviewable parts are idempotency and DLQ. |
| 17 | Event-Driven Architecture | CONCEPT | `event-driven-architecture` | - | Reviewable parts are idempotency, DLQ and saga steps. |
| 18 | Distributed Transactions | CONCEPT | `distributed-transactions` | - | Reviewable part is svc-saga-steps. |
| 19 | Saga Pattern | CHECK | `svc-saga-steps` | service | FAIL if a step after the pivot is not idempotent and retryable, a compensation can fail unhandled, or steps share no correlation id. |
| 20 | Dead Letter Queues | CHECK | `svc-queue-dlq` | service | FAIL if a consumer queue has no DLQ or max receive count, or the DLQ has no alarm on depth above zero. |
| 21 | Cron Jobs | CHECK | `svc-singleton-job-idempotent` | service | FAIL if a scheduled or leader-only job is not idempotent yet can run on two instances at once. Derived from the AWS leader-election page; no cron-specific source. |
| 22 | WebSockets | CONCEPT | `websockets` | - | No source in research. |
| 23 | Long Polling | CONCEPT | `long-polling` | - | No source in research. |
| 24 | Server-Sent Events | CONCEPT | `server-sent-events` | - | No source in research. |
| 25 | Database Indexing | CHECK | `chg-migration-index-concurrently` | change | FAIL if CREATE INDEX on a busy table omits CONCURRENTLY, runs inside a transaction block, or has no cleanup for a failed INVALID index. |
| 26 | Query Optimization | CONCEPT | `query-optimization` | - | No source in research. |
| 27 | N+1 Queries | CHECK | `fn-n-plus-one` | function | FAIL if a query runs once per item inside a loop over a prior result. No source in research: card stays draft. |
| 28 | Connection Pooling | CHECK | `svc-bulkhead-pools` | service | FAIL if all dependencies share one connection or thread pool so a slow one starves the rest. |
| 29 | Read Replicas | CONCEPT | `read-replicas` | - | No source in research. |
| 30 | Sharding | CONCEPT | `sharding` | - | Related: shuffle sharding is in the AWS isolation page. |
| 31 | Partitioning | CONCEPT | `partitioning` | - | No source in research. |
| 32 | Replication | CONCEPT | `replication` | - | No source in research. |
| 33 | Leader Election | CHECK | `svc-leader-two-leaders` | service | FAIL if lease-based leader work is unsafe with two leaders: not idempotent, no lease check before acting, no stop on failed renewal. |
| 34 | CAP Theorem | CONCEPT | `cap-theorem` | - | No source in research. |
| 35 | Eventual Consistency | CONCEPT | `eventual-consistency` | - | No source in research. |
| 36 | Optimistic Locking | CONCEPT | `optimistic-locking` | - | AWS leader page prefers it over leaders; check is svc-lock-fencing. |
| 37 | Pessimistic Locking | CONCEPT | `pessimistic-locking` | - | Related Postgres lock-mode material backs chg-migration-lock-timeout. |
| 38 | Distributed Locks | CHECK | `svc-lock-fencing` | service | FAIL if a TTL lock guards a correctness-critical write with no fencing token or compare-and-set on the resource side. Redlock dispute noted. |
| 39 | Race Conditions | CONCEPT | `race-conditions` | - | Reviewable parts: py-create-task-reference, svc-lock-fencing. |
| 40 | Deadlocks | CONCEPT | `deadlocks` | - | Reviewable part: chg-migration-lock-timeout. |
| 41 | Memory Leaks | CHECK | `fn-resource-lifetime` | function | FAIL if a task, goroutine, thread or handle has no owner or stop path, or is not released on the error path. |
| 42 | Garbage Collection | CONCEPT | `garbage-collection` | - | Reviewable part: py-create-task-reference (weak refs to tasks). |
| 43 | Thread Safety | CONCEPT | `thread-safety` | - | No dedicated source; see fn-resource-lifetime. |
| 44 | Backpressure | CHECK | `svc-queue-backlog-controls` | service | FAIL if a shared queue has no age-of-oldest alarm, no way to sideline old messages, or no per-tenant concurrency cap. |
| 45 | Autoscaling | CONCEPT | `autoscaling` | - | No source in research. |
| 46 | Horizontal Scaling | CONCEPT | `horizontal-scaling` | - | No source in research. |
| 47 | Vertical Scaling | CONCEPT | `vertical-scaling` | - | No source in research. |
| 48 | CDN | CONCEPT | `cdn` | - | No source in research. |
| 49 | Edge Caching | CONCEPT | `edge-caching` | - | Related: svc-cache-entry-version. |
| 50 | Cache Invalidation | CHECK | `svc-cache-entry-version` | service | FAIL if cached values carry no version field, so old and new code cannot read each other's entries. |
| 51 | Feature Flags | CHECK | `chg-flag-off-switch` | change | FAIL if a long-lived feature has no runtime switch to turn it off. |
| 51b | Feature Flags (telemetry) | CHECK | `prod-change-markers` | production | FAIL if a deploy or flag change is not recorded on telemetry, so before/after comparison is impossible. |
| 52 | Blue-Green Deployment | CONCEPT | `blue-green-deployment` | - | No source in research; see prod-canary-gate. |
| 53 | Canary Releases | CHECK | `prod-canary-gate` | production | FAIL if a rollout reaches 100% with no canary population, no canary-vs-control comparison on a few metrics, or a canary too small or short to be representative. |
| 54 | Rolling Deployments | CHECK | `prod-rollout-velocity` | production | FAIL if a deploy or ops tool acts on many hosts at once with no velocity limit or feedback loop. |
| 55 | Rollbacks | CHECK | `prod-rollback-rule` | production | FAIL if a rollout has no automatic abort or rollback criterion. |
| 56 | Health Checks | CHECK | `svc-health-check-scope` | service | FAIL if a load-balancer or auto-replace health check probes a shared dependency, or a host evicts itself on dependency failure. |
| 57 | Liveness & Readiness Probes | CONCEPT | `liveness-readiness-probes` | - | Reviewable part: svc-health-check-scope. |
| 58 | Monitoring | CHECK | `prod-golden-signals` | production | FAIL if a service lacks latency, traffic, errors and saturation signals, or tracks latency only as a mean. |
| 59 | Logging | CHECK | `code-log-safety` | codebase | FAIL if logs concatenate unencoded user input or contain credentials or payment data. |
| 60 | Distributed Tracing | CONCEPT | `distributed-tracing` | - | No source in research. |
| 61 | Metrics | CHECK | `prod-metric-label-cardinality` | production | FAIL if a metric label takes unbounded values such as user id or request id. |
| 62 | Alerts | CHECK | `prod-alert-symptom` | production | FAIL if a page fires on a cause (CPU high) with no user-visible symptom, or an alert never fires or is never used. |
| 63 | SLOs | CONCEPT | `slos` | - | No source in research beyond canary arithmetic. |
| 64 | SLIs | CONCEPT | `slis` | - | Related: prod-golden-signals. |
| 65 | Error Budgets | CONCEPT | `error-budgets` | - | Related: prod-canary-gate (canary arithmetic). |
| 66 | Observability | CHECK | `prod-wide-event-fields` | production | FAIL if a request emits only narrow log lines and no wide event with tenant, build, flag and trace fields. Vendor opinion: severity discuss. |
| 67 | Secrets Management | CHECK | `code-error-response-leak` | codebase | FAIL if an error response returns stack traces, SQL, keys or tokens. Hardcoded-secret scanning is unsourced; see Missing topics. |
| 68 | IAM | CONCEPT | `iam` | - | Related: code-ci-workflow-hardening (token permissions). |
| 69 | OAuth | CONCEPT | `oauth` | - | No source in research. |
| 70 | JWT Rotation | CONCEPT | `jwt-rotation` | - | No source in research. |
| 71 | TLS | CONCEPT | `tls` | - | No source in research. |
| 72 | Encryption at Rest | CONCEPT | `encryption-at-rest` | - | No source in research. |
| 73 | Encryption in Transit | CONCEPT | `encryption-in-transit` | - | No source in research. |
| 74 | WAF | CONCEPT | `waf` | - | No source in research. |
| 75 | DDoS Protection | CONCEPT | `ddos-protection` | - | Related: svc-rate-limit-quota. |
| 76 | CORS | CONCEPT | `cors` | - | No source in research. |
| 77 | CSRF | CONCEPT | `csrf` | - | No source in research. |
| 78 | SQL Injection | CHECK | `code-injection` | codebase | FAIL if untrusted input is concatenated into SQL, shell or query strings. Backed only at OWASP A05 category level. |
| 79 | XSS | CHECK | `code-injection` | codebase | Same card as 78: FAIL if untrusted input reaches HTML or script output unencoded. |
| 80 | SSRF | CHECK | `code-ssrf` | codebase | FAIL if a server fetches a user-supplied URL with no allow-list. Thin source (OWASP folded SSRF into A01): card stays draft. |
| 81 | Database Migrations | CHECK | `chg-migration-lock-timeout` | change | FAIL if ALTER TABLE on a hot table runs with no lock_timeout set for the migration session. |
| 81b | Database Migrations (constraints) | CHECK | `chg-migration-not-valid` | change | FAIL if a CHECK or FOREIGN KEY is added to a large table without NOT VALID, or the VALIDATE step is missing. |
| 81c | Database Migrations (rewrite) | CHECK | `chg-migration-add-column-rewrite` | change | FAIL if ADD COLUMN uses a volatile default, generated stored column or identity on a large table. |
| 81d | Database Migrations (backfill) | CHECK | `chg-migration-schema-data-split` | change | FAIL if schema change and data backfill share one transaction or deploy. |
| 82 | Schema Versioning | CHECK | `chg-migration-expand-contract` | change | FAIL if a column drop, rename or type change ships in a single release. |
| 83 | Disaster Recovery | CONCEPT | `disaster-recovery` | - | No source in research. |
| 84 | Backups | CONCEPT | `backups` | - | No source in research. |
| 85 | Failover | CONCEPT | `failover` | - | Related: svc-leader-two-leaders. |
| 86 | Multi-Region Deployment | CONCEPT | `multi-region-deployment` | - | Related: AWS correlated-failures page (cells, AZs), no card yet. |
| 87 | Chaos Engineering | CONCEPT | `chaos-engineering` | - | AWS caching page advises testing with the cache disabled; no card. |
| 88 | Cost Optimization | CONCEPT | `cost-optimization` | - | No source in research. |
| 89 | Cold Starts | CONCEPT | `cold-starts` | - | Related: svc-cache-miss-protection (cold cache after deploy). |
| 90 | Serverless Limits | CONCEPT | `serverless-limits` | - | No source in research. |
| 91 | Latency | CONCEPT | `latency` | - | Related: prod-golden-signals. |
| 92 | Throughput | CONCEPT | `throughput` | - | No source in research. |
| 93 | P99 Latency | CONCEPT | `p99-latency` | - | Related: prod-golden-signals (bucketed distributions). |
| 94 | Tail Latency | CONCEPT | `tail-latency` | - | Related: prod-golden-signals. |
| 95 | Network Partitions | CONCEPT | `network-partitions` | - | Related: svc-leader-two-leaders. |
| 96 | Clock Skew | CONCEPT | `clock-skew` | - | Related: svc-lock-fencing (monotonic clock concession). |
| 97 | DNS | CONCEPT | `dns` | - | No source in research. |
| 98 | TCP vs UDP | CONCEPT | `tcp-vs-udp` | - | No source in research. |
| 99 | HTTP/2 & HTTP/3 | CONCEPT | `http2-http3` | - | No source in research. |
| 100 | gRPC | CONCEPT | `grpc` | - | Reviewable part: svc-timeouts. |
| 101 | Webhooks | CONCEPT | `webhooks` | - | Reviewable parts: svc-idempotency-key, svc-retry-policy. |
| 102 | API Versioning | CHECK | `chg-observable-behavior-change` | change | FAIL if a change alters observable behavior (ordering, timing, error shape, defaults) with no staged rollout or consumer notice. |
| 103 | Semantic Versioning | CONCEPT | `semantic-versioning` | - | Related: chg-observable-behavior-change (Hyrum's law). |
| 104 | Infrastructure as Code | CONCEPT | `infrastructure-as-code` | - | No source in research. |
| 105 | Terraform | CONCEPT | `terraform` | - | No source in research. |
| 106 | Helm Charts | CONCEPT | `helm-charts` | - | No source in research. |
| 107 | Build Caching | CHECK | `code-build-hermetic` | codebase | FAIL if a build depends on host-installed tools or floating versions, or a release is not tied to one revision. |
| 108 | Dependency Hell | CHECK | `code-deps-pinned` | codebase | FAIL if there is no lockfile, dependencies are unpinned, or CI has no dependency-vulnerability scan. |
| 109 | Production Incidents | CONCEPT | `production-incidents` | - | No inc- card is sourced; see Missing topics. |
| 110 | On-Call | CONCEPT | `on-call` | - | Related: prod-alert-symptom. |
| 111 | Postmortems | CONCEPT | `postmortems` | - | No source in research. |
| X1 | Concurrency (task reference) | CHECK | `py-create-task-reference` | function | FAIL if asyncio.create_task() has its result discarded and the task is not in a TaskGroup or a set with a done-callback. Level function, prefix py-. |
| X2 | Concurrency (cancellation) | CHECK | `py-cancelled-error-reraise` | function | FAIL if CancelledError, a bare except or BaseException is swallowed without re-raise. Level function. |
| X3 | Concurrency (timeout handler) | CHECK | `py-timeout-handler-outside` | function | FAIL if the TimeoutError handler sits inside the asyncio.timeout() block. Level function. |
| X4 | Concurrency (bounded await) | CHECK | `py-remote-await-bounded` | function | FAIL if a network await runs outside asyncio.timeout(), wait_for or a client timeout. Level function. |
| X5 | Async vs Sync | CHECK | `mod-prefer-sync-api` | module | FAIL if a module exposes an async-only API where a synchronous one would let callers add concurrency themselves. |
| X6 | Clean Code | CONCEPT | `clean-code` | - | Disputed by Ousterhout on function length and comments. |
| X7 | YAGNI | CHECK | `chg-speculative-extension-point` | change | FAIL if the change adds an extension point, option or interface for a need no caller has today. |
| X8 | Grug | CONCEPT | `grug` | - | No source in research: glossary entry is a stub. |
| X9 | SOLID | CONCEPT | `solid` | - | Only Liskov is sourced; see mod-subtype-passes-parent-tests. |
| X9b | SOLID (Liskov) | CHECK | `mod-subtype-passes-parent-tests` | module | FAIL if a subclass breaks the parent's black-box tests: stricter inputs, weaker outputs or broken invariants. |
| X10 | TDD | CONCEPT | `tdd` | - | Dispute unresolved in research; see chg-characterization-test. |
| X11 | DDD | CONCEPT | `ddd` | - | No source in research: glossary entry is a stub. |
| X12 | Fowler's 12 smells | CONCEPT | `fowlers-smells` | - | The 12 are not listed in the task or research; confirm the list before splitting into rows. |
| X13 | Pocock Standards axis | CHECK | `chg-standards-conform` | change | FAIL if the diff violates a documented repo standard (style guide, lint config) and the comment cites it. |
| X14 | Pocock Spec axis | CHECK | `chg-spec-match` | change | FAIL if the diff adds behavior the linked issue did not ask for, or omits behavior it did. No URL source: card stays draft. |
| X15 | Thermo-nuclear points | CONCEPT | `thermo-nuclear` | - | The points were not supplied; add one row per point when the list arrives. |

## Missing topics

The 111 list has no row for these, yet the research supports them. Ids are reserved for later cards.

| Reserved id | Level | FAIL condition | Evidence in docs/research |
|---|---|---|---|
| `chg-size-split` | change | FAIL if a change is too large to review (about 200-400 lines or 20+ files) and not split. | review-culture-companies themes 'Complexity and scope', browser-pass Palantir |
| `chg-refactor-separate` | change | FAIL if a change mixes refactor or formatting with behavior change. | authors-principles-2 section 5; Beck, Palantir, Google all agree |
| `chg-characterization-test` | change | FAIL if legacy behavior changes with no test recording what it does today. | authors-principles-2 section 3 (Feathers) |
| `chg-problem-stated` | change | FAIL if the description omits what the problem is, or lists only the chosen design's costs. | authors-principles-2 section 5 (Hickey) |
| `chg-tests-with-code` | change | FAIL if code changes without tests and no reason is given. | review-culture-companies 'Tests' |
| `chg-no-rewrite-without-defect` | change | FAIL if a rewrite names no defect that only a rewrite fixes. | authors-principles-2 section 3 (Spolsky); disputed by Hickey-style rethinking |
| `mod-deep-module` | module | FAIL if a module is a shallow wrapper or pass-through, or leaks one piece of knowledge into several modules. | authors-principles-2 section 2, browser-pass Ousterhout flags |
| `mod-abstraction-proven` | module | FAIL if an abstraction is introduced from one or two uses, or grows flags so callers can bend it. | authors-principles-2 section 2 (AHA); DRY dispute in Disagreements |
| `fn-comment-adds-information` | function | FAIL if a comment restates the code or is stale. | authors-principles-2 section 6; Martin vs Ousterhout dispute |
| `fn-error-swallow` | function | FAIL if an except or catch swallows an error and continues, leaving a multi-step operation half done. | ops-docs-recheck OWASP A10:2025 and ASVS V16 |
| `code-supply-chain-provenance` | codebase | FAIL if release artifacts have no provenance. | ops-docs-recheck SLSA, Scorecard |
| `code-llm-output-untrusted` | codebase | FAIL if model output or retrieved text is acted on without validation, or tools hold broad tokens. | ops-docs-recheck OWASP LLM01:2025 |
| `code-ai-pr-disclosure` | codebase | FAIL if an AI-assisted PR lacks disclosure or an author able to explain it. | review-culture-companies 'Process hygiene' (Kubernetes only) |
| `prod-hermetic-release-review` | production | FAIL if a release is not tied to a reviewed revision. | ops-docs-recheck SRE release engineering; may merge into code-build-hermetic |
| `inc-*` | incident | None sourced: no research note covers incident response, postmortem content or on-call practice. Gather sources before reserving ids. | gap in docs/research |
| `code-secret-scan` | codebase | FAIL if a credential is committed to the repo. Not backed by the notes; Scorecard checks list not read in full. | gap in docs/research |
| `process-reviewer-conduct` | process | Reviewer conduct: label nits, ask rather than assert, do not approve with open questions. Process, not code: goes to a README section, not a card. | authors-principles-2 section 7, review-culture-companies 'Social and tone' |
