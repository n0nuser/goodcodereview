# Coverage

Every source item maps to a card id (`cards/`, `packs/`), a glossary term (`glossary/`), or an explicit `dropped: <reason>`.
Nothing leaves without a row. Status is `draft` or `stable` for cards, `glossary`, `dropped`, or `gap` for a reserved id with no card yet.

| Source | Item | Maps to | Status |
|---|---|---|---|
| 111-list #1 | Rate Limiting | `svc-rate-limit-quota` | draft |
| 111-list #2 | Caching | `sys-cache-cold-start` | draft |
| 111-list #3 | Load Balancing | glossary/load-balancing | glossary |
| 111-list #4 | Reverse Proxies | glossary/reverse-proxies | glossary |
| 111-list #5 | API Gateways | glossary/api-gateways | glossary |
| 111-list #6 | CI/CD | `code-workflow-supply-chain` | draft |
| 111-list #7 | Docker | glossary/docker | glossary |
| 111-list #8 | Kubernetes | glossary/kubernetes | glossary |
| 111-list #9 | Service Discovery | glossary/service-discovery | glossary |
| 111-list #10 | Circuit Breakers | `svc-circuit-breaker-bulkhead` | draft |
| 111-list #11 | Timeouts | `svc-timeouts` | draft |
| 111-list #12 | Retries | `svc-retry-policy` | draft |
| 111-list #13 | Exponential Backoff | `svc-retry-policy` | draft |
| 111-list #14 | Idempotency | `svc-idempotency-key` | draft |
| 111-list #15 | Message Queues | `svc-dlq` | draft |
| 111-list #16 | Pub/Sub | glossary/pub-sub | glossary |
| 111-list #17 | Event-Driven Architecture | glossary/event-driven-architecture | glossary |
| 111-list #18 | Distributed Transactions | glossary/distributed-transactions | glossary |
| 111-list #19 | Saga Pattern | `svc-saga-steps` | gap |
| 111-list #20 | Dead Letter Queues | `svc-dlq` | draft |
| 111-list #21 | Cron Jobs | `sys-leader-two-leaders` | draft |
| 111-list #22 | WebSockets | glossary/websockets | glossary |
| 111-list #23 | Long Polling | glossary/long-polling | glossary |
| 111-list #24 | Server-Sent Events | glossary/server-sent-events | glossary |
| 111-list #25 | Database Indexing | `sys-index-concurrently` | draft |
| 111-list #26 | Query Optimization | glossary/query-optimization | glossary |
| 111-list #27 | N+1 Queries | `sys-n-plus-one-pooling` | draft |
| 111-list #28 | Connection Pooling | `svc-circuit-breaker-bulkhead` | draft |
| 111-list #29 | Read Replicas | glossary/read-replicas | glossary |
| 111-list #30 | Sharding | glossary/sharding | glossary |
| 111-list #31 | Partitioning | glossary/partitioning | glossary |
| 111-list #32 | Replication | glossary/replication | glossary |
| 111-list #33 | Leader Election | `sys-leader-two-leaders` | draft |
| 111-list #34 | CAP Theorem | glossary/cap-theorem | glossary |
| 111-list #35 | Eventual Consistency | glossary/eventual-consistency | glossary |
| 111-list #36 | Optimistic Locking | glossary/optimistic-locking | glossary |
| 111-list #37 | Pessimistic Locking | glossary/pessimistic-locking | glossary |
| 111-list #38 | Distributed Locks | `sys-lock-fencing` | draft |
| 111-list #39 | Race Conditions | glossary/race-conditions | glossary |
| 111-list #40 | Deadlocks | glossary/deadlocks | glossary |
| 111-list #41 | Memory Leaks | `fn-resource-lifetime` | gap |
| 111-list #42 | Garbage Collection | glossary/garbage-collection | glossary |
| 111-list #43 | Thread Safety | glossary/thread-safety | glossary |
| 111-list #44 | Backpressure | `sys-load-shedding-bounded-queues` | draft |
| 111-list #45 | Autoscaling | glossary/autoscaling | glossary |
| 111-list #46 | Horizontal Scaling | glossary/horizontal-scaling | glossary |
| 111-list #47 | Vertical Scaling | glossary/vertical-scaling | glossary |
| 111-list #48 | CDN | glossary/cdn | glossary |
| 111-list #49 | Edge Caching | glossary/edge-caching | glossary |
| 111-list #50 | Cache Invalidation | `sys-cache-bounds-invalidation` | draft |
| 111-list #51 | Feature Flags | `prod-kill-switch-fallback` | draft |
| 111-list #51b | Feature Flags (telemetry) | `prod-wide-events-bounded-labels` | draft |
| 111-list #52 | Blue-Green Deployment | glossary/blue-green-deployment | glossary |
| 111-list #53 | Canary Releases | `prod-canary-staged-rollout` | draft |
| 111-list #54 | Rolling Deployments | `prod-canary-staged-rollout` | draft |
| 111-list #55 | Rollbacks | `prod-canary-staged-rollout` | draft |
| 111-list #56 | Health Checks | `sys-health-liveness-readiness` | draft |
| 111-list #57 | Liveness & Readiness Probes | glossary/liveness-readiness-probes | glossary |
| 111-list #58 | Monitoring | `prod-alerts-symptoms-golden-signals` | draft |
| 111-list #59 | Logging | `sys-secrets-and-errors` | draft |
| 111-list #60 | Distributed Tracing | glossary/distributed-tracing | glossary |
| 111-list #61 | Metrics | `prod-wide-events-bounded-labels` | draft |
| 111-list #62 | Alerts | `prod-alerts-symptoms-golden-signals` | draft |
| 111-list #63 | SLOs | glossary/slos | glossary |
| 111-list #64 | SLIs | glossary/slis | glossary |
| 111-list #65 | Error Budgets | glossary/error-budgets | glossary |
| 111-list #66 | Observability | `prod-wide-events-bounded-labels` | draft |
| 111-list #67 | Secrets Management | `sys-secrets-and-errors` | draft |
| 111-list #68 | IAM | glossary/iam | glossary |
| 111-list #69 | OAuth | glossary/oauth | glossary |
| 111-list #70 | JWT Rotation | glossary/jwt-rotation | glossary |
| 111-list #71 | TLS | glossary/tls | glossary |
| 111-list #72 | Encryption at Rest | glossary/encryption-at-rest | glossary |
| 111-list #73 | Encryption in Transit | glossary/encryption-in-transit | glossary |
| 111-list #74 | WAF | glossary/waf | glossary |
| 111-list #75 | DDoS Protection | glossary/ddos-protection | glossary |
| 111-list #76 | CORS | glossary/cors | glossary |
| 111-list #77 | CSRF | glossary/csrf | glossary |
| 111-list #78 | SQL Injection | `svc-sqli-authn` | draft |
| 111-list #79 | XSS | `svc-sqli-authn` | draft |
| 111-list #80 | SSRF | `sys-ssrf` | draft |
| 111-list #81 | Database Migrations | `sys-migration-lock-timeout` | draft |
| 111-list #81b | Database Migrations (constraints) | `sys-constraint-not-valid` | draft |
| 111-list #81c | Database Migrations (rewrite) | `chg-migration-add-column-rewrite` | gap |
| 111-list #81d | Database Migrations (backfill) | `sys-migration-expand-contract` | draft |
| 111-list #82 | Schema Versioning | `sys-migration-expand-contract` | draft |
| 111-list #83 | Disaster Recovery | glossary/disaster-recovery | glossary |
| 111-list #84 | Backups | glossary/backups | glossary |
| 111-list #85 | Failover | glossary/failover | glossary |
| 111-list #86 | Multi-Region Deployment | glossary/multi-region-deployment | glossary |
| 111-list #87 | Chaos Engineering | glossary/chaos-engineering | glossary |
| 111-list #88 | Cost Optimization | glossary/cost-optimization | glossary |
| 111-list #89 | Cold Starts | glossary/cold-starts | glossary |
| 111-list #90 | Serverless Limits | glossary/serverless-limits | glossary |
| 111-list #91 | Latency | glossary/latency | glossary |
| 111-list #92 | Throughput | glossary/throughput | glossary |
| 111-list #93 | P99 Latency | glossary/p99-latency | glossary |
| 111-list #94 | Tail Latency | glossary/tail-latency | glossary |
| 111-list #95 | Network Partitions | glossary/network-partitions | glossary |
| 111-list #96 | Clock Skew | glossary/clock-skew | glossary |
| 111-list #97 | DNS | glossary/dns | glossary |
| 111-list #98 | TCP vs UDP | glossary/tcp-vs-udp | glossary |
| 111-list #99 | HTTP/2 & HTTP/3 | glossary/http2-http3 | glossary |
| 111-list #100 | gRPC | glossary/grpc | glossary |
| 111-list #101 | Webhooks | glossary/webhooks | glossary |
| 111-list #102 | API Versioning | `chg-breaking-change-taxonomy` | draft |
| 111-list #103 | Semantic Versioning | glossary/semantic-versioning | glossary |
| 111-list #104 | Infrastructure as Code | glossary/infrastructure-as-code | glossary |
| 111-list #105 | Terraform | glossary/terraform | glossary |
| 111-list #106 | Helm Charts | glossary/helm-charts | glossary |
| 111-list #107 | Build Caching | `code-build-hermetic` | gap |
| 111-list #108 | Dependency Hell | `code-dependency-pinning` | draft |
| 111-list #109 | Production Incidents | glossary/production-incidents | glossary |
| 111-list #110 | On-Call | glossary/on-call | glossary |
| 111-list #111 | Postmortems | glossary/postmortems | glossary |
| 111-list #X1 | Concurrency (task reference) | `py-task-reference` | draft |
| 111-list #X2 | Concurrency (cancellation) | `py-cancellation` | draft |
| 111-list #X3 | Concurrency (timeout handler) | `py-cancellation` | draft |
| 111-list #X4 | Concurrency (bounded await) | `svc-timeouts` | draft |
| 111-list #X5 | Async vs Sync | `mod-prefer-sync-api` | gap |
| 111-list #X6 | Clean Code | glossary/clean-code | glossary |
| 111-list #X7 | YAGNI | `mod-yagni` | draft |
| 111-list #X8 | Grug | glossary/grug | glossary |
| 111-list #X9 | SOLID | glossary/solid | glossary |
| 111-list #X9b | SOLID (Liskov) | `mod-subtype-passes-parent-tests` | gap |
| 111-list #X10 | TDD | glossary/tdd | glossary |
| 111-list #X11 | DDD | glossary/ddd | glossary |
| 111-list #X12 | Fowler's 12 smells | glossary/fowlers-smells | glossary |
| 111-list #X13 | Pocock Standards axis | `chg-standards-conform` | gap |
| 111-list #X14 | Pocock Spec axis | `chg-matches-spec` | draft |
| 111-list #X15 | Thermo-nuclear points | glossary/thermo-nuclear | glossary |
| research-gap | a change is too large to review (about 200-400 lines or 20+ fi | `chg-size-ceiling` | draft |
| research-gap | a change mixes refactor or formatting with behavior change. | `chg-refactor-separate` | draft |
| research-gap | legacy behavior changes with no test recording what it does to | `chg-characterization-test` | gap |
| research-gap | the description omits what the problem is, or lists only the c | `chg-author-hygiene` | draft |
| research-gap | code changes without tests and no reason is given. | `chg-tests-ship-with-change` | draft |
| research-gap | a rewrite names no defect that only a rewrite fixes. | `chg-no-rewrite-without-defect` | gap |
| research-gap | a module is a shallow wrapper or pass-through, or leaks one pi | `mod-deep-modules` | draft |
| research-gap | an abstraction is introduced from one or two uses, or grows fl | `mod-no-wrong-abstraction` | draft |
| research-gap | a comment restates the code or is stale. | `fn-comments-explain-why` | draft |
| research-gap | an except or catch swallows an error and continues, leaving a | `fn-propagate-dont-swallow` | draft |
| research-gap | release artifacts have no provenance. | `code-workflow-supply-chain` | draft |
| research-gap | model output or retrieved text is acted on without validation, | `sys-prompt-injection` | draft |
| research-gap | an AI-assisted PR lacks disclosure or an author able to explai | `code-ai-pr-disclosure` | gap |
| research-gap | Release tied to a reviewed revision | dropped: duplicate of code-build-hermetic | dropped |
| research-gap | Incident response/postmortems | `inc-postmortem-owned-actions`, `inc-rollback-path-tested` | draft |
| research-gap | a credential is committed to the repo. Not backed by the notes | `code-secret-scan` | gap |
| research-gap | Reviewer conduct | `chg-review-comment-format` | draft |
| change-codebase | Consistency with codebase unless pattern is bad; improve what you touch | `chg-match-codebase-pattern` | draft |
| change-codebase | Reuse: search for an existing helper first | `chg-reuse-before-write` | draft |
| change-codebase | Move logic to shared module with 2+ call sites; wrong-abstraction | `chg-abstraction-needs-two-callers` | draft |
| change-codebase | Scope: one concern per change | `chg-one-concern` | draft |
| change-codebase | Size spread, SmartBear/Cisco single vendor study | `chg-size-ceiling` | draft |
| change-codebase | Refactors separate; moves not edited | `chg-refactor-separate` | draft |
| change-codebase | Tests ship with the change | `chg-tests-ship-with-change` | draft |
| change-codebase | New API ships with a usage | `chg-new-api-has-usage` | draft |
| change-codebase | Spec match, no unrequested changes | `chg-matches-spec` | draft |
| change-codebase | Author hygiene: description, self-review, CI green | `chg-author-hygiene` | draft |
| change-codebase | Expand/contract (gap: recipe unsourced) | `chg-expand-contract` | draft |
| change-codebase | Breaking-change taxonomy (Hyrum's law) | `chg-breaking-change-taxonomy` | draft |
| change-codebase | Rollback path (thin source) | `chg-rollback-path` | draft |
| change-codebase | Flag owner and retirement (thin source) | `chg-flag-owner-retirement` | draft |
| change-codebase | New attack surface named (thin source) | `chg-name-attack-surface` | draft |
| change-codebase | Severity labels, one comment per finding | `chg-review-comment-format` | draft |
| change-codebase | What not to flag; few high-conviction comments | `chg-review-signal` | draft |
| change-codebase | Verify before claim | `chg-verify-before-claim` | draft |
| change-codebase | No silenced diagnostics | `chg-no-silenced-diagnostics` | draft |
| change-codebase | Chesterton's fence | `chg-chestertons-fence` | draft |
| change-codebase | Agent code: hallucinated APIs, re-implemented helpers | `chg-agent-grounded-code` | draft |
| change-codebase | Agent code: mock-asserting tests | `chg-agent-mock-asserting-tests` | draft |
| change-codebase | Agent code: same-session self-review | `chg-agent-independent-review` | draft |
| change-codebase | File-size ceiling 1k lines (gap: heuristic) | `code-file-lines-ceiling` | draft |
| change-codebase | Dead code | `code-dead-code` | draft |
| change-codebase | Dependency pinning | `code-dependency-pinning` | draft |
| change-codebase | Licences, SBOM (licence part is a gap) | `code-dependency-licence-sbom` | draft |
| change-codebase | CI gates | `code-ci-gates` | draft |
| change-codebase | ADRs (gap: format unsourced) | `code-adr` | draft |
| change-codebase | Consistency drift | `code-consistency-drift` | draft |
| change-codebase | Supply chain: workflows, provenance | `code-workflow-supply-chain` | draft |
| core-python | How I review: Ledger: PASS/FAIL/N/A with evidence | dropped: out of scope (change-level cards) | dropped |
| core-python | What the tools own: Linter owns what it can decide; add the gate | `py-ruff-gate` | draft |
| core-python | Architecture: Three layers named by what they do; dependencies point inward | `mod-layers-point-inward` | draft |
| core-python | Architecture: Entry module stays thin | `mod-thin-entry-point` | draft |
| core-python | Architecture: No helpers.py / utils.py | `mod-no-utils-grab-bag` | draft |
| core-python | Architecture: Large literals in their own module; one cohesive unit; single-module folder inlined | `mod-cohesive-unit` | draft |
| core-python | Architecture: `__init__.py` empty except at a public boundary | `py-init-py-empty` | draft |
| core-python | Architecture: I/O at the edges; import touches nothing | `mod-no-import-side-effects` | draft |
| core-python | Architecture: YAGNI | `mod-yagni` | draft |
| core-python | Architecture: No pass-through wrappers | `fn-no-pass-through-wrapper` | draft |
| core-python | Architecture: Behaviour lives with the state it owns | `mod-behaviour-lives-with-state` | draft |
| core-python | Config and typing: Env config through pydantic-settings | `py-settings-pydantic-settings` | draft |
| core-python | Config and typing: Config values live in the settings module | `mod-central-config` | draft |
| core-python | Config and typing: No `cast()` | `py-no-cast` | draft |
| core-python | Config and typing: Fixed key set gets a type | `fn-known-keys-get-a-type` | draft |
| core-python | Config and typing: No stringly-typed returns | `fn-no-stringly-typed-returns`, `py-strenum-not-strings` | draft |
| core-python | Config and typing: `X \\| None`, builtin generics, strict typing | `py-modern-typing` | draft |
| core-python | Config and typing: `Field()` only when it adds something | `py-field-only-when-adds` | draft |
| core-python | Imports: Top of module, absolute, no `_` names, `__all__` only in re-export | `py-imports` | draft |
| core-python | State and `__init__`: No module-level mutable state | `mod-no-module-mutable-state` | draft |
| core-python | State and `__init__`: No logic in `__init__` | `mod-no-logic-in-constructors`, `py-init-assign-only` | draft |
| core-python | State and `__init__`: Inject boundary collaborators | `mod-inject-boundary-collaborators` | draft |
| core-python | Naming and classes: Semantics and consistency; one name per concept; glossary wins; no borrowed terms | `mod-one-name-per-concept` | draft |
| core-python | Naming and classes: Name intermediate conditions | `fn-name-intermediate-conditions` | draft |
| core-python | Naming and classes: Bool argument at call site | `fn-bool-arg-at-callsite` | draft |
| core-python | Naming and classes: Code explains itself; rename before commenting | `fn-comments-explain-why` | draft |
| core-python | Naming and classes: English everywhere | `fn-english-identifiers` | gap |
| core-python | Naming and classes: No codenames or ticket numbers in code | `fn-comments-survive-context` | draft |
| core-python | Naming and classes: A class earns its instance; Protocol needs two implementations | `py-class-earns-its-instance` | draft |
| core-python | Naming and classes: Field names over indexes; no getattr/setattr | `fn-no-getattr-for-known-names` | draft |
| core-python | Naming and classes: No anonymous tuples | `fn-no-anonymous-tuples`, `py-frozen-dataclass-over-tuple` | draft |
| core-python | Naming and classes: List-returning functions return `[]` | `fn-empty-collection-not-none` | draft |
| core-python | Naming and classes: No magic strings or numbers | `fn-no-magic-values`, `py-strenum-not-strings` | draft |
| core-python | Validation: Pydantic models, validate at the boundary once, snake_case with alias | `mod-validate-at-boundary-once`, `py-pydantic-validation` | draft |
| core-python | Error handling: Specific exceptions only | `fn-specific-exceptions-only` | draft |
| core-python | Error handling: Propagate, translate with `from` | `fn-propagate-dont-swallow` | draft |
| core-python | Error handling: Base exception per package, errors module | `py-error-hierarchy` | draft |
| core-python | Error handling: Retry only transient failures on idempotent operations | dropped: out of scope (service-level cards) | dropped |
| core-python | Error handling: Error responses don't leak internals | dropped: out of scope (service-level cards) | dropped |
| core-python | Error handling: Log the branches that matter with a request ID | dropped: out of scope (service-level cards) | dropped |
| core-python | Security: Validate every input; name new attack surface; secrets from settings | dropped: out of scope (service-level cards) | dropped |
| core-python | Docstrings and comments: Comments explain why | `fn-comments-explain-why` | draft |
| core-python | Docstrings and comments: Comments survive loss of context | `fn-comments-survive-context` | draft |
| core-python | Docstrings and comments: No forced docstrings, Google style | `py-docstrings-google` | draft |
| core-python | Docstrings and comments: No section banners | `mod-cohesive-unit` | draft |
| core-python | Docstrings and comments: Check every stated reason against the artifact | `fn-comments-explain-why` | draft |
| core-python | Docstrings and comments: Empty `__init__.py` means empty | `py-init-py-empty` | draft |
| core-python | Testing: `parametrize` for variations | `py-pytest-parametrize` | draft |
| core-python | Testing: No `test_init_*` or plain-model tests | `py-no-init-or-model-tests` | draft |
| core-python | Testing: Whole-object assertions; mock at the boundary; fake has real signature | `mod-mock-at-boundaries-only` | draft |
| core-python | Testing: No Arrange/Act/Assert comments; deterministic; layout mirrors source; fixtures; regression test first | `py-test-hygiene` | draft |
| core-python | Concurrency: No check-then-act across `await`; atomic operations | `fn-no-check-then-act-across-await`, `py-await-check-then-act` | draft |
| core-python | Concurrency: Shared state reasoned about for races | dropped: out of scope (change-level cards) | dropped |
| core-python | Resource lifecycle: Per-key caches bounded | `mod-bounded-caches` | draft |
| core-python | Resource lifecycle: Pooled clients built once | `mod-pooled-clients-built-once`, `py-httpx-client-lifespan` | draft |
| core-python | Resource lifecycle: Timeouts on both legs | `svc-timeouts`, `py-httpx-client-lifespan` | draft |
| core-python | Resource lifecycle: Stream, don't materialise; bound background tasks | `svc-stream-dont-materialise` | gap |
| core-python | Change discipline: Never silence a diagnostic | `py-no-silenced-diagnostics` | draft |
| core-python | Change discipline: No paths relative to the working directory | `py-paths-from-file` | draft |
| core-python | Change discipline: Verify before claiming; delete workarounds; stay in scope; Chesterton; measure | dropped: out of scope (change-level cards) | dropped |
| core-python | Writing the review: Severity labels, one comment per finding, design first | dropped: out of scope (change-level cards) | dropped |
| core-python | Critical rules: Bookmark table | dropped: bookmark table, severity lives on cards | dropped |
| core-python | Additions beyond the guide: Deep modules | `mod-deep-modules` | draft |
| core-python | Additions beyond the guide: Wrong abstraction | `mod-no-wrong-abstraction` | draft |
| core-python | Additions beyond the guide: Fowler smells | `mod-fowler-smells` | draft |
| service-system | asyncio: discarded create_task, TaskGroup, shield | `py-task-reference` | draft |
| service-system | asyncio: swallowed CancelledError, TimeoutError inside timeout block | `py-cancellation` | draft |
| service-system | asyncio: await without timeout bound; Azure retry/timeouts | `svc-timeouts` | draft |
| service-system | Azure retry: backoff, attempts, non-transient, stacked layers; AWS correlated: jitter | `svc-retry-policy` | draft |
| service-system | Azure retry/saga: idempotency, unique saga id | `svc-idempotency-key` | draft |
| service-system | Azure circuit breaker and bulkhead | `svc-circuit-breaker-bulkhead` | draft |
| service-system | AWS queues: DLQ, visibility timeout, queue age | `svc-dlq` | draft |
| service-system | AWS fairness / shuffle sharding: per-tenant quota, 429 vs 503 | `svc-rate-limit-quota` | draft |
| service-system | AWS queues: bounded queue, sideline, cheap shedding | `sys-load-shedding-bounded-queues` | draft |
| service-system | Kleppmann / antirez: fencing, check-and-set, disagreement | `sys-lock-fencing` | draft |
| service-system | AWS leader election: two leaders, lease check | `sys-leader-two-leaders` | draft |
| service-system | AWS caching: TTL, size, metrics, versioned values | `sys-cache-bounds-invalidation` | draft |
| service-system | AWS caching: cold start, stampede, cache-off test | `sys-cache-cold-start` | draft |
| service-system | AWS health checks: liveness vs dependency, self-eviction | `sys-health-liveness-readiness` | draft |
| service-system | PG config + altertable: lock_timeout | `sys-migration-lock-timeout` | draft |
| service-system | PG altertable: NOT VALID / VALIDATE | `sys-constraint-not-valid` | draft |
| service-system | PG createindex: CONCURRENTLY, INVALID leftovers | `sys-index-concurrently` | draft |
| service-system | GitLab migration style + avoiding downtime | `sys-migration-expand-contract` | draft |
| service-system | OWASP A03:2025, Scorecard, SLSA | `code-dependency-pinning`, `code-workflow-supply-chain`, `code-dependency-licence-sbom` | draft |
| service-system | OWASP LLM01 | `sys-prompt-injection` | draft |
| service-system | OWASP A10:2025, ASVS V16 (error leaks, fail open, log data) | `sys-secrets-and-errors` | draft |
| service-system | OWASP A01 (SSRF folded in) | `sys-ssrf` | draft |
| service-system | OWASP A05 / A07 / A01 (index only) | `svc-sqli-authn` | draft |
| service-system | SRE monitoring | `prod-alerts-symptoms-golden-signals` | draft |
| service-system | Honeycomb wide events, cardinality, deploy markers | `prod-wide-events-bounded-labels` | draft |
| service-system | SRE canary + release engineering, AWS velocity control | `prod-canary-staged-rollout` | draft |
| service-system | AWS cache-off test, ASVS degradation path | `prod-kill-switch-fallback` | draft |
| service-system | Canary / health-check fail-open caution | `inc-rollback-path-tested` | draft |
| service-system | First-hand card, no research source | `svc-api-compat-pagination` | draft |
| service-system | First-hand card, no research source | `sys-n-plus-one-pooling` | draft |
| service-system | First-hand card, no research source | `prod-slo-error-budget` | draft |
| service-system | First-hand card, no research source | `inc-postmortem-owned-actions` | draft |
| service-system | Glossary candidate: Shuffle sharding (tenant-to-shard assignment; reviewable only as "exists") | dropped: glossary candidate, no entry written | dropped |
| service-system | Glossary candidate: Efficiency vs correctness lock | dropped: glossary candidate, no entry written | dropped |
| service-system | Glossary candidate: Breaker vs retry purpose | dropped: glossary candidate, no entry written | dropped |
| service-system | Glossary candidate: Saga data anomalies; pivot/compensable/retryable steps | dropped: glossary candidate, no entry written | dropped |
| service-system | Glossary candidate: Canary arithmetic (error share vs traffic share) | dropped: glossary candidate, no entry written | dropped |
| service-system | Glossary candidate: Prompt injection vs jailbreaking | dropped: glossary candidate, no entry written | dropped |
| service-system | Glossary candidate: Retry budget (not defined in sources) | dropped: glossary candidate, no entry written | dropped |
| service-system | Glossary candidate: CSRF and CORS: no source read; add cards once a primary source is added | dropped: glossary candidate, no entry written | dropped |
| service-system | Glossary candidate: Lock mode conflict table; `ADD CONSTRAINT ... USING INDEX` (not verified) | dropped: glossary candidate, no entry written | dropped |
| service-system | Glossary candidate: Cheap load shedding and slowed fast errors | dropped: glossary candidate, no entry written | dropped |
| service-system | Glossary candidate: Unread: OWASP LLM10 Unbounded Consumption, ASVS V1-V15, Azure DLQ page | dropped: glossary candidate, no entry written | dropped |

## Gaps

Reserved ids with no card. Each line is the rule the card would check.

- `chg-characterization-test`: FAIL if legacy behavior changes with no test recording what it does today.
- `chg-migration-add-column-rewrite`: FAIL if ADD COLUMN with a volatile default, generated stored column or identity on a large table.
- `chg-no-rewrite-without-defect`: FAIL if a rewrite names no defect that only a rewrite fixes.
- `chg-standards-conform`: FAIL if the diff violates a documented repo standard and the comment cites it.
- `code-ai-pr-disclosure`: FAIL if an AI-assisted PR lacks disclosure or an author able to explain it.
- `code-build-hermetic`: FAIL if build depends on host tools or floating versions, or a release is not tied to one revision.
- `code-secret-scan`: FAIL if a credential is committed to the repo (unsourced).
- `fn-english-identifiers`: FAIL if identifiers or comments are not in English.
- `fn-resource-lifetime`: FAIL if a task, goroutine, thread or handle has no owner or stop path, or is not released on the error path.
- `mod-prefer-sync-api`: FAIL if a module exposes an async-only API where a synchronous one would let callers add concurrency.
- `mod-subtype-passes-parent-tests`: FAIL if a subclass breaks the parent's black-box tests (stricter inputs, weaker outputs, broken invariants).
- `svc-saga-steps`: FAIL if a step after the pivot is not idempotent and retryable, or a compensation can fail unhandled.
- `svc-stream-dont-materialise`: FAIL if a large result is materialised in memory, or background tasks are unbounded.
