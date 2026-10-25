# Coverage

Every source item maps to a card id (`cards/`, `packs/`), a glossary term (`glossary/`), or an explicit `dropped: <reason>`.
Nothing leaves without a row. Status is `draft` or `stable` for cards, `glossary`, `dropped`, or `gap` for a reserved id with no card yet.

| Source | Item | Maps to | Status |
|---|---|---|---|
| 111-list #1 | Rate Limiting | `svc-rate-limit-quota` | stable |
| 111-list #2 | Caching | `sys-cache-cold-start` | draft |
| 111-list #3 | Load Balancing | glossary/load-balancing | glossary |
| 111-list #4 | Reverse Proxies | glossary/reverse-proxies | glossary |
| 111-list #5 | API Gateways | glossary/api-gateways | glossary |
| 111-list #6 | CI/CD | `code-workflow-supply-chain` | stable |
| 111-list #7 | Docker | glossary/docker | glossary |
| 111-list #8 | Kubernetes | glossary/kubernetes | glossary |
| 111-list #9 | Service Discovery | glossary/service-discovery | glossary |
| 111-list #10 | Circuit Breakers | `svc-circuit-breaker-bulkhead` | draft |
| 111-list #11 | Timeouts | `svc-timeouts` | stable |
| 111-list #12 | Retries | `svc-retry-policy` | stable |
| 111-list #13 | Exponential Backoff | `svc-retry-policy` | stable |
| 111-list #14 | Idempotency | `svc-idempotency-key` | stable |
| 111-list #15 | Message Queues | `svc-dlq` | draft |
| 111-list #16 | Pub/Sub | glossary/pub-sub | glossary |
| 111-list #17 | Event-Driven Architecture | glossary/event-driven-architecture | glossary |
| 111-list #18 | Distributed Transactions | glossary/distributed-transactions | glossary |
| 111-list #19 | Saga Pattern | `svc-saga-steps` | draft |
| 111-list #20 | Dead Letter Queues | `svc-dlq` | draft |
| 111-list #21 | Cron Jobs | `sys-leader-two-leaders` | draft |
| 111-list #22 | WebSockets | glossary/websockets | glossary |
| 111-list #23 | Long Polling | glossary/long-polling | glossary |
| 111-list #24 | Server-Sent Events | glossary/server-sent-events | glossary |
| 111-list #25 | Database Indexing | `sys-index-concurrently` | draft |
| 111-list #26 | Query Optimization | glossary/query-optimization | glossary |
| 111-list #27 | N+1 Queries | `sys-n-plus-one-pooling` | stable |
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
| 111-list #38 | Distributed Locks | `sys-lock-fencing` | stable |
| 111-list #39 | Race Conditions | glossary/race-conditions | glossary |
| 111-list #40 | Deadlocks | glossary/deadlocks | glossary |
| 111-list #41 | Memory Leaks | `fn-resource-lifetime` | draft |
| 111-list #42 | Garbage Collection | glossary/garbage-collection | glossary |
| 111-list #43 | Thread Safety | glossary/thread-safety | glossary |
| 111-list #44 | Backpressure | `sys-load-shedding-bounded-queues` | stable |
| 111-list #45 | Autoscaling | glossary/autoscaling | glossary |
| 111-list #46 | Horizontal Scaling | glossary/horizontal-scaling | glossary |
| 111-list #47 | Vertical Scaling | glossary/vertical-scaling | glossary |
| 111-list #48 | CDN | glossary/cdn | glossary |
| 111-list #49 | Edge Caching | glossary/edge-caching | glossary |
| 111-list #50 | Cache Invalidation | `sys-cache-bounds-invalidation` | stable |
| 111-list #51 | Feature Flags | `prod-kill-switch-fallback` | stable |
| 111-list #51b | Feature Flags (telemetry) | `prod-wide-events-bounded-labels` | draft |
| 111-list #52 | Blue-Green Deployment | glossary/blue-green-deployment | glossary |
| 111-list #53 | Canary Releases | `prod-canary-staged-rollout` | stable |
| 111-list #54 | Rolling Deployments | `prod-canary-staged-rollout` | stable |
| 111-list #55 | Rollbacks | `prod-canary-staged-rollout` | stable |
| 111-list #56 | Health Checks | `sys-health-liveness-readiness` | draft |
| 111-list #57 | Liveness & Readiness Probes | glossary/liveness-readiness-probes | glossary |
| 111-list #58 | Monitoring | `prod-alerts-symptoms-golden-signals` | stable |
| 111-list #59 | Logging | `sys-secrets-and-errors` | stable |
| 111-list #60 | Distributed Tracing | glossary/distributed-tracing | glossary |
| 111-list #61 | Metrics | `prod-wide-events-bounded-labels` | draft |
| 111-list #62 | Alerts | `prod-alerts-symptoms-golden-signals` | stable |
| 111-list #63 | SLOs | glossary/slos | glossary |
| 111-list #64 | SLIs | glossary/slis | glossary |
| 111-list #65 | Error Budgets | glossary/error-budgets | glossary |
| 111-list #66 | Observability | `prod-wide-events-bounded-labels` | draft |
| 111-list #67 | Secrets Management | `code-secret-scan` | stable |
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
| 111-list #78 | SQL Injection | `svc-sqli-authn` | stable |
| 111-list #79 | XSS | `fn-no-raw-html-sink` | stable |
| 111-list #80 | SSRF | `sys-ssrf` | stable |
| 111-list #81 | Database Migrations | `sys-migration-lock-timeout` | draft |
| 111-list #81b | Database Migrations (constraints) | `sys-constraint-not-valid` | draft |
| 111-list #81c | Database Migrations (rewrite) | `chg-migration-add-column-rewrite` | draft |
| 111-list #81d | Database Migrations (backfill) | `sys-migration-expand-contract` | stable |
| 111-list #82 | Schema Versioning | `sys-migration-expand-contract` | stable |
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
| 111-list #102 | API Versioning | `chg-breaking-change-taxonomy` | stable |
| 111-list #103 | Semantic Versioning | glossary/semantic-versioning | glossary |
| 111-list #104 | Infrastructure as Code | glossary/infrastructure-as-code | glossary |
| 111-list #105 | Terraform | glossary/terraform | glossary |
| 111-list #106 | Helm Charts | glossary/helm-charts | glossary |
| 111-list #107 | Build Caching | `code-build-hermetic` | stable |
| 111-list #108 | Dependency Hell | `code-dependency-pinning` | stable |
| 111-list #109 | Production Incidents | glossary/production-incidents | glossary |
| 111-list #110 | On-Call | glossary/on-call | glossary |
| 111-list #111 | Postmortems | glossary/postmortems | glossary |
| 111-list #X1 | Concurrency (task reference) | `py-task-reference` | draft |
| 111-list #X2 | Concurrency (cancellation) | `py-cancellation` | draft |
| 111-list #X3 | Concurrency (timeout handler) | `py-cancellation` | draft |
| 111-list #X4 | Concurrency (bounded await) | `svc-timeouts` | stable |
| 111-list #X5 | Async vs Sync | `mod-prefer-sync-api` | draft |
| 111-list #X6 | Clean Code | glossary/clean-code | glossary |
| 111-list #X7 | YAGNI | `mod-yagni` | stable |
| 111-list #X8 | Grug | glossary/grug | glossary |
| 111-list #X9 | SOLID | glossary/solid | glossary |
| 111-list #X9b | SOLID (Liskov) | `mod-subtype-passes-parent-tests` | draft |
| 111-list #X10 | TDD | glossary/tdd | glossary |
| 111-list #X11 | DDD | glossary/ddd | glossary |
| 111-list #X13 | Pocock Standards axis | `chg-match-codebase-pattern` | stable |
| 111-list #X14 | Pocock Spec axis | `chg-matches-spec` | draft |
| pocock-smells | Mysterious Name | `mod-one-name-per-concept` | draft |
| pocock-smells | Duplicated Code | `chg-reuse-before-write` | draft |
| pocock-smells | Feature Envy | `mod-behaviour-lives-with-state` | draft |
| pocock-smells | Data Clumps | `fn-no-anonymous-tuples`, `fn-known-keys-get-a-type` | draft |
| pocock-smells | Primitive Obsession | `fn-no-stringly-typed-returns` | draft |
| pocock-smells | Repeated Switches | `mod-fowler-smells` | draft |
| pocock-smells | Shotgun Surgery | `mod-fowler-smells` | draft |
| pocock-smells | Divergent Change | `mod-cohesive-unit` | draft |
| pocock-smells | Speculative Generality | `mod-yagni` | stable |
| pocock-smells | Message Chains | `mod-fowler-smells` | draft |
| pocock-smells | Middle Man | `fn-no-pass-through-wrapper` | draft |
| pocock-smells | Refused Bequest | `mod-subtype-passes-parent-tests` | draft |
| pocock-smells | Smells are judgement calls; the repo's own standard overrides the baseline | `mod-fowler-smells` | draft |
| pocock-smells | Skip what tooling already enforces | `py-ruff-gate` | draft |
| pocock-smells | Axes reported separately, never reranked; worst finding per axis | dropped: output format of one skill | dropped |
| thermo-nuclear | P0 Ambition: restructure to delete whole layers (code judo) | dropped: reviewer posture, nothing to FAIL | dropped |
| thermo-nuclear | P1 File crosses 1000 lines | `code-file-lines-ceiling` | draft |
| thermo-nuclear | P2 Ad-hoc conditionals, one-off flags in unrelated flows | `chg-no-special-case-branches` | draft |
| thermo-nuclear | P3 Working code is not enough; prefer removing moving parts | dropped: reviewer posture, see chg-review-signal | dropped |
| thermo-nuclear | P4 Magic, thin wrappers, identity helpers | `fn-no-pass-through-wrapper` | draft |
| thermo-nuclear | P5 Needless optionality, any/unknown, casts, loose object shapes | `py-no-cast`, `fn-known-keys-get-a-type` | draft |
| thermo-nuclear | P6 Logic in the wrong layer; bespoke helper beside a canonical one | `mod-layers-point-inward`, `chg-reuse-before-write` | draft |
| thermo-nuclear | P7a Independent async work run sequentially | `fn-independent-work-concurrent` | stable |
| thermo-nuclear | P7b Related updates that can leave state half applied | `fn-atomic-related-updates` | draft |
| thermo-nuclear | Copy-pasted logic | `chg-reuse-before-write` | draft |
| thermo-nuclear | Temporary branching likely to stay | `chg-flag-owner-retirement` | draft |
| thermo-nuclear | Few high-conviction comments; direct tone; approval bar | `chg-review-signal`, `chg-review-comment-format` | draft |
| thermo-nuclear | Review: only report added or modified code | `chg-review-signal` | stable |
| thermo-nuclear | Review: trace side effects before claiming breakage; no unfinished research | `chg-verify-before-claim` | stable |
| thermo-nuclear | Review: developer-experience breaks (env vars, ports, secret sources, new scripts) | `chg-devex-breaking-config` | draft |
| thermo-nuclear | Review: feature-gate leaks | `chg-flag-owner-retirement` | draft |
| thermo-nuclear | Review: do not report an intended breakage | dropped: reviewer posture | dropped |
| thermo-nuclear | Review: do not over-report priority | `chg-review-signal` | stable |
| thermo-nuclear | Review: read bot comments only after own audit | `chg-agent-independent-review` | draft |
| thermo-nuclear | Thermos: two parallel passes then merge | dropped: workflow mechanics; fresh context is chg-agent-independent-review | dropped |
| research-gap | a change is too large to review (about 200-400 lines or 20+ fi | `chg-size-ceiling` | stable |
| research-gap | a change mixes refactor or formatting with behavior change. | `chg-refactor-separate` | stable |
| research-gap | legacy behavior changes with no test recording what it does to | `chg-chestertons-fence` | draft |
| research-gap | the description omits what the problem is, or lists only the c | `chg-author-hygiene` | stable |
| research-gap | code changes without tests and no reason is given. | `chg-tests-ship-with-change` | stable |
| research-gap | a rewrite names no defect that only a rewrite fixes. | `chg-chestertons-fence` | draft |
| research-gap | a module is a shallow wrapper or pass-through, or leaks one pi | `mod-deep-modules` | draft |
| research-gap | an abstraction is introduced from one or two uses, or grows fl | `mod-no-wrong-abstraction` | draft |
| research-gap | a comment restates the code or is stale. | `fn-comments-explain-why` | stable |
| research-gap | an except or catch swallows an error and continues, leaving a | `fn-propagate-dont-swallow` | draft |
| research-gap | release artifacts have no provenance. | `code-workflow-supply-chain` | stable |
| research-gap | model output or retrieved text is acted on without validation, | `sys-prompt-injection` | stable |
| research-gap | an AI-assisted PR lacks disclosure or an author able to explai | `code-ai-pr-disclosure` | draft |
| research-gap | Release tied to a reviewed revision | dropped: duplicate of code-build-hermetic | dropped |
| research-gap | Incident response/postmortems | `inc-postmortem-owned-actions`, `inc-rollback-path-tested` | draft |
| research-gap | a credential is committed to the repo. Sources added in second pass | `code-secret-scan` | stable |
| research-gap | Reviewer conduct | `chg-review-comment-format` | draft |
| change-codebase | Consistency with codebase unless pattern is bad; improve what you touch | `chg-match-codebase-pattern` | stable |
| change-codebase | Reuse: search for an existing helper first | `chg-reuse-before-write` | draft |
| change-codebase | Move logic to shared module with 2+ call sites; wrong-abstraction | `mod-yagni`, `mod-no-wrong-abstraction` | draft |
| change-codebase | Scope: one concern per change | `chg-one-concern` | stable |
| change-codebase | Size spread, SmartBear/Cisco single vendor study | `chg-size-ceiling` | stable |
| change-codebase | Refactors separate; moves not edited | `chg-refactor-separate` | stable |
| change-codebase | Tests ship with the change | `chg-tests-ship-with-change` | stable |
| change-codebase | New API ships with a usage | `chg-new-api-has-usage` | draft |
| change-codebase | Spec match, no unrequested changes | `chg-matches-spec` | draft |
| change-codebase | Author hygiene: description, self-review, CI green | `chg-author-hygiene` | stable |
| change-codebase | Expand/contract (gap: recipe unsourced) | `chg-expand-contract` | stable |
| change-codebase | Breaking-change taxonomy (Hyrum's law) | `chg-breaking-change-taxonomy` | stable |
| change-codebase | Rollback path (thin source) | `chg-rollback-path` | draft |
| change-codebase | Flag owner and retirement (thin source) | `chg-flag-owner-retirement` | draft |
| change-codebase | New attack surface named (thin source) | `chg-name-attack-surface` | draft |
| change-codebase | Severity labels, one comment per finding | `chg-review-comment-format` | draft |
| change-codebase | What not to flag; few high-conviction comments | `chg-review-signal` | stable |
| change-codebase | Verify before claim | `chg-verify-before-claim` | stable |
| change-codebase | No silenced diagnostics | `chg-no-silenced-diagnostics` | draft |
| change-codebase | Chesterton's fence | `chg-chestertons-fence` | draft |
| change-codebase | Agent code: hallucinated APIs, re-implemented helpers | `chg-agent-grounded-code` | draft |
| change-codebase | Agent code: mock-asserting tests | `chg-agent-mock-asserting-tests` | draft |
| change-codebase | Agent code: same-session self-review | `chg-agent-independent-review` | draft |
| change-codebase | File-size ceiling 1k lines (gap: heuristic) | `code-file-lines-ceiling` | draft |
| change-codebase | Dead code | `code-dead-code` | stable |
| change-codebase | Dependency pinning | `code-dependency-pinning` | stable |
| change-codebase | Licences, SBOM (licence part is a gap) | `code-dependency-licence-sbom` | stable |
| change-codebase | CI gates | `code-ci-gates` | stable |
| change-codebase | ADRs (gap: format unsourced) | `code-adr` | draft |
| change-codebase | Consistency drift | `code-consistency-drift` | stable |
| change-codebase | Supply chain: workflows, provenance | `code-workflow-supply-chain` | stable |
| core-python | How I review: Ledger: PASS/FAIL/N/A with evidence | `chg-review-comment-format` | draft |
| core-python | What the tools own: Linter owns what it can decide; add the gate | `py-ruff-gate` | draft |
| core-python | Architecture: Three layers named by what they do; dependencies point inward | `mod-layers-point-inward` | draft |
| core-python | Architecture: Entry module stays thin | `mod-thin-entry-point` | draft |
| core-python | Architecture: No helpers.py / utils.py | `mod-no-utils-grab-bag` | draft |
| core-python | Architecture: Large literals in their own module; one cohesive unit; single-module folder inlined | `mod-cohesive-unit` | draft |
| core-python | Architecture: `__init__.py` empty except at a public boundary | `py-init-py-empty` | draft |
| core-python | Architecture: I/O at the edges; import touches nothing | `mod-no-import-side-effects` | draft |
| core-python | Architecture: YAGNI | `mod-yagni` | stable |
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
| core-python | Naming and classes: Code explains itself; rename before commenting | `fn-comments-explain-why` | stable |
| core-python | Naming and classes: English everywhere | `fn-english-identifiers` | draft |
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
| core-python | Error handling: Retry only transient failures on idempotent operations | `svc-retry-policy` | stable |
| core-python | Error handling: Error responses don't leak internals | `sys-secrets-and-errors` | stable |
| core-python | Error handling: Log the branches that matter with a request ID | `svc-request-id-logging` | draft |
| core-python | Security: Validate every input; name new attack surface; secrets from settings | `mod-validate-at-boundary-once`, `chg-name-attack-surface`, `sys-secrets-and-errors` | draft |
| core-python | Docstrings and comments: Comments explain why | `fn-comments-explain-why` | stable |
| core-python | Docstrings and comments: Comments survive loss of context | `fn-comments-survive-context` | draft |
| core-python | Docstrings and comments: No forced docstrings, Google style | `py-docstrings-google` | draft |
| core-python | Docstrings and comments: No section banners | `mod-cohesive-unit` | draft |
| core-python | Docstrings and comments: Check every stated reason against the artifact | `fn-comments-explain-why` | stable |
| core-python | Docstrings and comments: Empty `__init__.py` means empty | `py-init-py-empty` | draft |
| core-python | Testing: `parametrize` for variations | `py-pytest-parametrize` | draft |
| core-python | Testing: No `test_init_*` or plain-model tests | `py-no-init-or-model-tests` | draft |
| core-python | Testing: Whole-object assertions; mock at the boundary; fake has real signature | `mod-mock-at-boundaries-only` | draft |
| core-python | Testing: No Arrange/Act/Assert comments; deterministic; layout mirrors source; fixtures; regression test first | `py-test-hygiene` | draft |
| core-python | Concurrency: No check-then-act across `await`; atomic operations | `fn-no-check-then-act-across-await`, `py-await-check-then-act` | draft |
| core-python | Concurrency: Shared state reasoned about for races | `fn-no-check-then-act-across-await` | draft |
| core-python | Resource lifecycle: Per-key caches bounded | `sys-cache-bounds-invalidation` | stable |
| core-python | Resource lifecycle: Pooled clients built once | `mod-pooled-clients-built-once`, `py-httpx-client-lifespan` | draft |
| core-python | Resource lifecycle: Timeouts on both legs | `svc-timeouts`, `py-httpx-client-lifespan` | draft |
| core-python | Resource lifecycle: Stream, don't materialise; bound background tasks | `svc-stream-dont-materialise`, `svc-bounded-background-tasks` | draft |
| core-python | Change discipline: Never silence a diagnostic | `py-no-silenced-diagnostics` | draft |
| core-python | Change discipline: No paths relative to the working directory | `py-paths-from-file` | draft |
| core-python | Change discipline: Verify before claiming; delete workarounds; stay in scope; Chesterton; measure | `chg-verify-before-claim`, `chg-matches-spec`, `chg-chestertons-fence` | draft |
| core-python | Writing the review: Severity labels, one comment per finding, design first | `chg-review-comment-format` | draft |
| core-python | Critical rules: Bookmark table | dropped: bookmark table, severity lives on cards | dropped |
| core-python | Additions beyond the guide: Deep modules | `mod-deep-modules` | draft |
| core-python | Additions beyond the guide: Wrong abstraction | `mod-no-wrong-abstraction` | draft |
| core-python | Additions beyond the guide: Fowler smells | `mod-fowler-smells` | draft |
| service-system | asyncio: discarded create_task, TaskGroup, shield | `py-task-reference` | draft |
| service-system | asyncio: swallowed CancelledError, TimeoutError inside timeout block | `py-cancellation` | draft |
| service-system | asyncio: await without timeout bound; Azure retry/timeouts | `svc-timeouts` | stable |
| service-system | Azure retry: backoff, attempts, non-transient, stacked layers; AWS correlated: jitter | `svc-retry-policy` | stable |
| service-system | Azure retry/saga: idempotency, unique saga id | `svc-idempotency-key` | stable |
| service-system | Azure circuit breaker and bulkhead | `svc-circuit-breaker-bulkhead` | draft |
| service-system | AWS queues: DLQ, visibility timeout, queue age | `svc-dlq` | draft |
| service-system | AWS fairness / shuffle sharding: per-tenant quota, 429 vs 503 | `svc-rate-limit-quota` | stable |
| service-system | AWS queues: bounded queue, sideline, cheap shedding | `sys-load-shedding-bounded-queues` | stable |
| service-system | Kleppmann / antirez: fencing, check-and-set, disagreement | `sys-lock-fencing` | stable |
| service-system | AWS leader election: two leaders, lease check | `sys-leader-two-leaders` | draft |
| service-system | AWS caching: TTL, size, metrics, versioned values | `sys-cache-bounds-invalidation` | stable |
| service-system | AWS caching: cold start, stampede, cache-off test | `sys-cache-cold-start` | draft |
| service-system | AWS health checks: liveness vs dependency, self-eviction | `sys-health-liveness-readiness` | draft |
| service-system | PG config + altertable: lock_timeout | `sys-migration-lock-timeout` | draft |
| service-system | PG altertable: NOT VALID / VALIDATE | `sys-constraint-not-valid` | draft |
| service-system | PG createindex: CONCURRENTLY, INVALID leftovers | `sys-index-concurrently` | draft |
| service-system | GitLab migration style + avoiding downtime | `sys-migration-expand-contract` | stable |
| service-system | OWASP A03:2025, Scorecard, SLSA | `code-dependency-pinning`, `code-workflow-supply-chain`, `code-dependency-licence-sbom` | stable |
| service-system | OWASP LLM01 | `sys-prompt-injection` | stable |
| service-system | OWASP A10:2025, ASVS V16 (error leaks, fail open, log data) | `sys-secrets-and-errors` | stable |
| service-system | OWASP A01 (SSRF folded in) | `sys-ssrf` | stable |
| service-system | OWASP A05 / A07 / A01 (index only) | `svc-sqli-authn` | stable |
| service-system | SRE monitoring | `prod-alerts-symptoms-golden-signals` | stable |
| service-system | Honeycomb wide events, cardinality, deploy markers | `prod-wide-events-bounded-labels` | draft |
| service-system | SRE canary + release engineering, AWS velocity control | `prod-canary-staged-rollout` | stable |
| service-system | AWS cache-off test, ASVS degradation path | `prod-kill-switch-fallback` | stable |
| service-system | Canary / health-check fail-open caution | `inc-rollback-path-tested` | stable |
| service-system | First-hand card, no research source | dropped: svc-api-compat-pagination merged away in stable pass 6; its Rule is `svc-api-versioning-policy` and its pagination half is `svc-list-endpoint-paginates` | dropped |
| service-system | First-hand card, no research source | `sys-n-plus-one-pooling` | stable |
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
| cursor-plugins | 1 Fix the fault, not where it surfaced; guards, retries, swallowed errors hide bugs | `chg-fix-root-cause-not-symptom` | draft |
| cursor-plugins | 2 Fails only after restart: suspect persisted state | dropped: investigation tip, nothing to FAIL | dropped |
| cursor-plugins | 3 Attack the premise after two failed fixes | dropped: author process, not visible in a diff | dropped |
| cursor-plugins | 4 Validate at the boundary; pure logic, thin shell | `mod-validate-at-boundary-once`, `mod-thin-entry-point` | draft |
| cursor-plugins | 5 No transport, storage or wire types in the public surface | `mod-no-wire-types-in-public-api` | draft |
| cursor-plugins | 6 Distinct types for semantic primitives (ids) | `fn-distinct-types-for-ids` | draft |
| cursor-plugins | 7 Derive types from the owning schema | `mod-derive-dont-duplicate` | stable |
| cursor-plugins | 8 External data untyped until parsed at the boundary | `mod-validate-at-boundary-once` | draft |
| cursor-plugins | 9 State machine or tagged union over synced booleans and growing chains | `fn-variants-as-tagged-union`, `chg-no-special-case-branches` | draft |
| cursor-plugins | 10 Organise by domain knowledge, not execution order | `mod-cohesive-unit` | draft |
| cursor-plugins | 11 Keep boring code; abstraction must remove branches or invalid states | `mod-no-wrong-abstraction` | draft |
| cursor-plugins | 12 Data shape first; DRY structure not lines; three similar lines beat early abstraction | `mod-yagni`, `mod-no-wrong-abstraction` | draft |
| cursor-plugins | 13 Scaffold first; small single-purpose commits | `chg-one-concern`, `code-ci-gates` | stable |
| cursor-plugins | 14 Reader load: layers to trace, state to hold; inline one-caller wrappers | `fn-no-pass-through-wrapper`, `mod-no-module-mutable-state`, `mod-deep-modules` | draft |
| cursor-plugins | 15 30-second reader-load test | glossary/reader-load | glossary |
| cursor-plugins | 16 One source of truth for a decision; smallest diff | `mod-central-config`, `chg-one-concern` | draft |
| cursor-plugins | 17 Subtract first; no speculative validators or stubs | `mod-yagni` | stable |
| cursor-plugins | 18 Operations converge on rerun and after a crash; stale markers recognisable | `fn-rerun-safe-after-crash`, `svc-idempotency-key` | stable |
| cursor-plugins | 19 Separate before serialising shared state; single writer; convention is not a lock | `mod-single-writer-per-state` | stable |
| cursor-plugins | 20 Migrate callers and delete the legacy API in one change (no outside consumers) | `chg-delete-legacy-after-migration` | draft |
| cursor-plugins | 21 Accept planned, scoped breakage between rewrite phases | dropped: planning posture; conflicts with per-commit green | dropped |
| cursor-plugins | 22 Verify the real thing, not a proxy; re-runnable script as artifact | `chg-verify-before-claim`, `chg-agent-independent-review` | draft |
| cursor-plugins | 23 Test must fail when behaviour breaks and survive an internals refactor | `chg-agent-mock-asserting-tests`, `mod-mock-at-boundaries-only`, `py-no-init-or-model-tests` | draft |
| cursor-plugins | 24 Independent test oracle; pair a negative assertion with a positive case | `fn-test-oracle-independent` | draft |
| cursor-plugins | 25 A performance number needs run count, spread and a named limiter | `chg-perf-claim-evidence` | stable |
| cursor-plugins | 26 Verify each unit before the next; failing test first | `chg-tests-ship-with-change` | stable |
| cursor-plugins | 26b Commit order tells the story | dropped: history shape is not visible in a diff | dropped |
| cursor-plugins | 27 Redesign instead of bolting on | dropped: posture; visible symptom is chg-no-special-case-branches | dropped |
| cursor-plugins | 28 Prefer the structural fix over a repeated instruction | `code-rule-has-enforcer` | stable |
| cursor-plugins | 29 Build the codemod or script so a reviewer can re-run it | dropped: author workflow, not failable from the diff | dropped |
| cursor-plugins | 30 Exhaust design space, experience first, guard context, never block on human | dropped: design-process posture, product taste, agent runtime | dropped |
| cursor-plugins | 31 Classify repeated corrections; fix at the highest level; lint message names the replacement | `code-rule-has-enforcer` | stable |
| cursor-plugins | 32 Fail only when a change adds more of a common pattern; exceptions carry reason, expiry, approver | `code-ci-gates`, `chg-no-silenced-diagnostics` | draft |
| cursor-plugins | 33 Comment exceptions: legal, forced by vendor or protocol, API contract, link; our surprises get a rename or type | `fn-comments-explain-why`, `fn-comments-survive-context` | draft |
| cursor-plugins | 34 Constraint and 'do not remove' comments become a type, lint or test; correctness suppressions go | `chg-no-silenced-diagnostics`, `code-rule-has-enforcer` | draft |
| cursor-plugins | 35 Blast radius beyond grep: JSON, DB column, wire format, flags, library source | `chg-breaking-change-taxonomy` | stable |
| cursor-plugins | 36 Prove the one fact the change is safe because of; mark unproven | `chg-verify-before-claim` | stable |
| cursor-plugins | 37 TDD bug fix: failing test first, confirm cause, never bend a test to a wrong implementation | `chg-tests-ship-with-change`, `chg-agent-mock-asserting-tests`, `chg-verify-before-claim` | draft |
| cursor-plugins | 38 TypeScript: tagged unions, exhaustive default, unknown over any, no as, honest type guards | `py-no-cast`, `fn-variants-as-tagged-union` | draft |
| cursor-plugins | 39 Object arguments over positional | `fn-bool-arg-at-callsite` | draft |
| cursor-plugins | 40 Do not mock what you can run; no console.log in shipped code | dropped: mock half is mod-mock-at-boundaries-only; logging is linter-owned | dropped |
| cursor-plugins | 41 Red flag: shallow module | `mod-deep-modules` | draft |
| cursor-plugins | 42 Red flag: information leakage | `mod-fowler-smells`, `mod-no-wire-types-in-public-api` | draft |
| cursor-plugins | 43 Red flag: temporal decomposition | `mod-cohesive-unit` | draft |
| cursor-plugins | 44 Red flag: pass-through method | `fn-no-pass-through-wrapper` | draft |
| cursor-plugins | 45 Red flag: split ownership of state | `mod-single-writer-per-state` | stable |
| cursor-plugins | 46 Red flag: two ways to do one task | `chg-delete-legacy-after-migration`, `code-consistency-drift` | draft |
| cursor-plugins | 47 Red flag: importable internals | `mod-internals-unreachable` | draft |
| cursor-plugins | 48 Red flag: hand-synced list | `mod-derive-dont-duplicate` | stable |
| cursor-plugins | 49 Signs the architecture is wrong: repeated workarounds, escape hatches, special-case branches | `chg-no-special-case-branches`, `mod-deep-modules` | draft |
| cursor-plugins | 50 Design twice; usage sketch first | dropped: design process, not visible in a diff | dropped |
| cursor-plugins | 51 Root cause vs symptom: masking guard, retry over broken contract, silencing cast | `chg-fix-root-cause-not-symptom` | draft |
| cursor-plugins | 52 A 'don't do X' comment should be a type, lint or runtime check | `code-rule-has-enforcer` | stable |
| cursor-plugins | 53 Legacy dual-paths with no external consumer | `chg-delete-legacy-after-migration` | draft |
| cursor-plugins | 54 Trace the call chain or input path before claiming a bug or security issue | `chg-verify-before-claim` | stable |
| cursor-plugins | 55 Reviewer judgement: nit inflation, unreachable hypotheticals, preference, independent agreement | `chg-review-signal`, `chg-agent-independent-review` | draft |
| cursor-plugins | 56 State intent first; findings bucketed by action and severity | `chg-matches-spec`, `chg-review-comment-format` | draft |
| cursor-plugins | 57 Bug fix: each line traces to runtime evidence; repro before fix | `chg-fix-root-cause-not-symptom`, `chg-verify-before-claim` | draft |
| cursor-plugins | 58 Refactor: pin behaviour with a characterization test before moving structure | `chg-refactor-has-behaviour-pin` | stable |
| cursor-plugins | 59 Refactor API reshape: migrate callers, delete old API, no shim | `chg-delete-legacy-after-migration` | draft |
| cursor-plugins | 59b Spot-check renames against strings and prose | dropped: manual step, not visible in a diff | dropped |
| cursor-plugins | 60 Refactor must lower reader load or be reverted | `chg-refactor-separate` | stable |
| cursor-plugins | 61 Perf fixes tie to a measurement; cheap options in order | glossary/performance-mantras | glossary |
| cursor-plugins | 62 Benchmark checklist: seven questions for a performance claim | `chg-perf-claim-evidence` | stable |
| cursor-plugins | 63 verify-this listed under pstack by mistake | dropped: duplicate of row 77 | dropped |
| cursor-plugins | 64 PR body as a one-minute briefing; narrow PRs; one primary perf number | `chg-author-hygiene`, `chg-size-ceiling` | stable |
| cursor-plugins | 65 A verdict covers one patch; recheck after rebase by patch id | `chg-approval-tied-to-patch` | draft |
| cursor-plugins | 66 Bot findings: fix, dismiss with reason, or ask; never dismiss data or security class | `chg-review-signal` | stable |
| cursor-plugins | 67 Append-only decision log and audit of the trail | dropped: agent audit trail; cross-model idea is chg-agent-independent-review | dropped |
| cursor-plugins | 68 Falsifiable definition of done; baseline before work; inconclusive is not a pass | `chg-verify-before-claim` | stable |
| cursor-plugins | 69 Prose rules (unslop, technical-writing) | dropped: prose style, already followed by this repo's writing rules | dropped |
| cursor-plugins | 70 No confirmed repro, no fix; symptom twice through real use; verify existing fix first | `chg-verify-before-claim` | stable |
| cursor-plugins | 70b Bot Slack and credential safety rules | dropped: bot-specific safety, not code review | dropped |
| cursor-plugins | 71 Trace history (blame, PR, ticket, postmortem) before judging defensive code | `chg-chestertons-fence` | draft |
| cursor-plugins | 72 Prompting and exploration helpers | dropped: not code review | dropped |
| cursor-plugins | 73 Deslop: extra comments, abnormal defensive try/catch, any casts, deep nesting | `chg-agent-grounded-code`, `chg-match-codebase-pattern`, `py-no-cast`, `mod-validate-at-boundary-once` | draft |
| cursor-plugins | 74 Reviewability: matching summary, core vs generated, no hidden behaviour change, split if too big | `chg-author-hygiene`, `chg-refactor-separate`, `chg-size-ceiling` | stable |
| cursor-plugins | 75 Compare tree hash after history rewrite | dropped: author workflow | dropped |
| cursor-plugins | 76 Review order correctness before style; severity groups; judge on all checks | `chg-review-signal`, `chg-review-comment-format`, `code-ci-gates` | draft |
| cursor-plugins | 77 Verify-this: falsifiable claim, same-condition baseline and treatment, one verdict | `chg-verify-before-claim`, `chg-perf-claim-evidence` | stable |
| cursor-plugins | 78 Fix CI one cause at a time; flaky retry once; unrelated fixes stay out | `chg-one-concern` | stable |
| cursor-plugins | 79 Task runners and agent mechanics (team-kit) | dropped: no review rule | dropped |
| cursor-plugins | 80 PR review canvas: core first, mechanical collapsed, callouts sparing | `chg-review-signal` | stable |
| cursor-plugins | 81 Root-cause gate and symptom-fix tells (guard, swallow, cast, retry, skip, weakened assertion, hard-code) | `chg-fix-root-cause-not-symptom` | draft |
| cursor-plugins | 82 Merge-ready definition: green review, ready, no conflicts, all checks, threads resolved | `chg-author-hygiene` | stable |
| cursor-plugins | 83 Review priority order; no factoring before second caller; understand before deleting | `chg-review-signal`, `mod-yagni`, `chg-chestertons-fence` | draft |
| cursor-plugins | 84 Keep real, in-diff, worthwhile findings; cap list; one ask each; no praise | `chg-review-signal`, `chg-review-comment-format` | draft |
| cursor-plugins | 85 Re-review context; PR text and CI logs are untrusted data | `chg-review-comment-format`, `sys-prompt-injection`, `code-workflow-supply-chain` | draft |
| cursor-plugins | 86 The Algorithm: question requirement, delete, optimise, accelerate, automate | `mod-yagni` | stable |
| cursor-plugins | 87 dyl-ready-pr loop and build-figma | dropped: platform workflow | dropped |
| cursor-plugins | 88 CLI: every input a flag; prompts only fallback; fail fast with example | `svc-cli-non-interactive` | draft |
| cursor-plugins | 89 CLI: --dry-run and confirmation bypass for destructive commands | `svc-cli-destructive-dry-run` | draft |
| cursor-plugins | 90 CLI: safe to rerun | `svc-idempotency-key`, `fn-rerun-safe-after-crash` | stable |
| cursor-plugins | 91 CLI help examples, consistent verbs, structured output | dropped: usability preference, one vendor's view | dropped |
| cursor-plugins | 92 Documented setup path runs on a clean checkout | `code-documented-setup-runs` | draft |
| cursor-plugins | 92a Scoped validation loop for a small change | `code-scoped-validation-loop` | draft |
| cursor-plugins | 92b Cold-start attempt, published scanner and blended score | dropped: scoring method and vendor CLI, not a rule | dropped |
| cursor-plugins | 93 Orchestrate, ralph-loop, continual-learning, advisor: agent machinery | dropped: agent runtime, no rule for code under review | dropped |

## Gaps

None. Every reserved id has a card.

## Security pass

Source: `docs/research/security-pass.md`. Row numbers are that file's.

| Source | Item | Maps to | Status |
|---|---|---|---|
| security-pass | 1-2, 4 Check the caller's right to the specific record | `fn-object-level-authz` | stable |
| security-pass | 1, 3-4 One authorization layer, deny by default | `svc-authz-central-deny-default` | stable |
| security-pass | 5-6 Bind requests to a DTO or allowlist | `fn-no-mass-assignment` | stable |
| security-pass | 5 Return listed fields, not the stored model | `fn-response-fields-explicit` | stable |
| security-pass | 7 Slow salted password hash | `fn-password-slow-hash` | stable |
| security-pass | 8 Session ID regeneration, cookie flags, server-side logout | `svc-session-lifecycle` | stable |
| security-pass | 9 Pinned JWT algorithm, `iss`, `aud`, `exp` | `fn-jwt-verify-pinned` | stable |
| security-pass | 10-11 Per-account throttle, uniform auth errors | `svc-auth-throttle-generic-errors` | stable |
| security-pass | 11, 29 Cap client-controlled sizes and counts | `svc-bound-client-controlled-sizes` | stable |
| security-pass | 12, 28 Encoding sinks, no raw HTML | `fn-no-raw-html-sink` | stable |
| security-pass | 13, 28 Argument arrays, no shell string | `fn-no-shell-with-input` | stable |
| security-pass | 14 Resolve and confine file paths | `fn-confine-file-path` | stable |
| security-pass | 15 No native deserialisation of untrusted input | `fn-no-native-deserialise-untrusted` | stable |
| security-pass | 16 Upload allowlist, size cap, generated name, outside web root | `svc-upload-validate-store` | stable |
| security-pass | 17 Server-side allowlist validation, regex limits | `mod-validate-at-boundary-once` | draft |
| security-pass | 18 CSRF token, no state change on GET | `svc-csrf-state-changing` | stable |
| security-pass | 19 CORS origin allowlist | `svc-cors-allowlist` | stable |
| security-pass | 20 HSTS, nosniff, frame-ancestors | `svc-security-headers` | draft |
| security-pass | 21 Subresource Integrity for vendor scripts | dropped: one narrow front-end row, left for a later pass | dropped |
| security-pass | 22 CSPRNG for tokens and keys | `fn-csprng-for-secrets` | stable |
| security-pass | 22-23 Vetted AEAD, no home-made crypto, no nonce reuse | `mod-vetted-crypto-only` | stable |
| security-pass | 23-24 TLS verification stays on | `fn-tls-verify-on` | stable |
| security-pass | 23 Minimise and expire sensitive data | `sys-pii-minimise-retention` | stable |
| security-pass | 25-26 Log security events, keep secrets out, encode untrusted values | `svc-security-event-logging` | draft |
| security-pass | 27 Narrow agent tools, user-scoped credentials | `sys-agent-tool-least-privilege` | stable |
| security-pass | 28 Treat model output as untrusted | `sys-prompt-injection` | stable |
| security-pass | 30 LLM supply chain: verify sources, sign, inventory | `code-dependency-licence-sbom` | stable |
| security-pass | 31 Invented package names from code models | `chg-agent-grounded-code` | draft |
| security-pass | §8 NIST SSDF practices | dropped: page named no practice numbers; read the PDF in a later pass | dropped |

- `chg-fix-root-cause-not-symptom`: FAIL if a fix adds a guard, retry, sleep, longer timeout, swallowed error, cast, skipped or weakened test, or a special case for the failing input, with no stated cause seen in evidence.
- `chg-perf-claim-evidence`: FAIL if a performance claim has no measured before-and-after numbers.
- `chg-delete-legacy-after-migration`: FAIL if a change adds a new API or path and leaves the old one alive when no consumer outside the repo needs it (sibling of `chg-expand-contract`).
- `chg-refactor-has-behaviour-pin`: FAIL if a refactor moves structure with no test, snapshot or equivalence check that pins current behaviour first.
- `chg-approval-tied-to-patch`: FAIL if an approval or verification verdict older than the last push that changed non-test content is treated as current.
- `fn-variants-as-tagged-union`: FAIL if state is a bag of optional fields or a set of booleans that must stay in sync, or a variant switch has no exhaustiveness check.
- `fn-distinct-types-for-ids`: FAIL if two arguments with different meanings share one primitive type and nothing stops them being swapped.
- `fn-test-oracle-independent`: FAIL if a test's expected value comes from the code under test, or a 'not called' assertion has no matching case where the call happens.
- `fn-rerun-safe-after-crash`: FAIL if an operation gives a different result on a second run or after a crash halfway, or leaves a marker the next run cannot judge as stale.
- `mod-single-writer-per-state`: FAIL if more than one writer can change the same state at once, with no single owner, serialising queue or compare-and-swap, or if only a convention guards it.
- `mod-internals-unreachable`: FAIL if a caller outside a module can import its internals and no check fails the build.
- `mod-derive-dont-duplicate`: FAIL if a type, list or enum duplicates a shape owned by a schema or another list, with no derivation and no build check for disagreement.
- `mod-no-wire-types-in-public-api`: FAIL if a public interface exposes transport, storage or framework types instead of domain types.
- `mod-cli-non-interactive`: FAIL if a CLI command needs a prompt or menu for any input that has no flag, or hangs on a missing flag instead of exiting with an example.
- `mod-cli-destructive-dry-run`: FAIL if a destructive CLI command has no preview flag or no non-interactive confirmation bypass.
- `code-rule-has-enforcer`: FAIL if a repeated review correction or an instruction file rule that a type, lint or CI check could enforce has no enforcer.
- `code-documented-setup-runs`: FAIL if a setup or run command in the README or contribution guide fails on a clean checkout.
- `code-scoped-validation-loop`: FAIL if the only documented way to check a small change is the full-repo run.

## API and contracts pass

From `docs/research/api-pass.md`.

| Source | Item | Maps to | Status |
|---|---|---|---|
| api-pass | RFC 9110 9.2: Safe and idempotent methods | `svc-api-safe-idempotent-methods` | draft |
| api-pass | RFC 9110 9.3, 10.2, 15.3: 201 with Location, 405 with Allow, most specific status | `svc-api-specific-status-codes` | draft |
| api-pass | RFC 9110 10.2.3, IETF ratelimit draft: Retry-After on 429 and 503; draft RateLimit fields not required | `svc-api-retry-after` | draft |
| api-pass | RFC 9110 13.1.1, Azure guidelines: ETag and If-Match on shared writes, 412 on stale | `svc-api-conditional-writes` | stable |
| api-pass | RFC 9111: Explicit Cache-Control, private for user data, Vary | `svc-api-cache-control` | draft |
| api-pass | RFC 9457, Zalando 176: Errors as application/problem+json, no internals | `svc-api-problem-json` | draft |
| api-pass | RFC 9457, AIP-193: Stable machine-readable error code | `svc-api-error-code-stable` | stable |
| api-pass | OpenAPI 3.1, Zalando 100-101: Spec is the source of truth and matches the service | `svc-api-spec-matches-impl` | draft |
| api-pass | OpenAPI 3.1, Zalando 101: Spec changes in the same diff as the route | `chg-api-spec-in-same-change` | draft |
| api-pass | OpenAPI 3.1, Zalando 151: Error responses and examples documented per operation | `svc-api-documented-errors` | draft |
| api-pass | RFC 9745, RFC 8594, Zalando 189: Deprecation and Sunset headers before removal | `svc-api-deprecation-sunset` | stable |
| api-pass | Zalando 113-116, Azure, Stripe: One documented versioning scheme, no breaks inside a version | `svc-api-versioning-policy` | stable |
| api-pass | Zalando 118, Azure: One naming convention per location | `svc-api-naming-consistent` | draft |
| api-pass | protobuf.dev (RPC vs storage messages): Response built from an explicit type, no internal fields | `fn-response-fields-explicit` | stable |
| api-pass | W3C Trace Context: Forward traceparent with a new parent id per hop | `svc-api-trace-context` | draft |
| api-pass | Pact docs: Consumer-derived contract tests across services | `svc-api-contract-tests` | draft |
| api-pass | protobuf.dev: Reserve deleted field numbers and names | `chg-proto-reserve-removed-fields` | draft |
| api-pass | protobuf.dev: No type, label or rename change on a field | `chg-proto-no-field-type-change` | draft |
| api-pass | protobuf.dev: Enum zero value is UNSPECIFIED | `mod-proto-enum-zero-unspecified` | draft |
| api-pass | AIP-193: Permission checked before existence (403 vs 404) | dropped: authorisation review, not a contract rule | dropped |
| api-pass | Zalando 233: X-Flow-ID header | dropped: superseded by traceparent | dropped |
| api-pass | IETF ratelimit draft: RateLimit and RateLimit-Policy header names | dropped: Internet-Draft, not a standard | dropped |
| api-pass | Azure guidelines: 202 with status monitor for long-running operations | dropped: one vendor's pattern | dropped |
| api-pass | protobuf.dev: No required fields | dropped: narrow, no card yet | dropped |
| api-pass | protobuf.dev: Do not rely on identical serialised bytes | dropped: narrow | dropped |

## Performance pass

From `docs/research/performance-pass.md`. Every card here except `sys-load-shedding-bounded-queues` carries the `performance` tag. The org count is the number of independent organisations behind the Rule.

| Source | Item | Maps to | Status |
|---|---|---|---|
| performance-pass | Attach the query plan for a new query on a growing table (3 orgs for EXPLAIN; attaching it is the card's practice) | `chg-new-query-has-plan` | draft |
| performance-pass | Build strings with a builder or join, not `+=` in a loop (3 orgs) | `fn-join-dont-concat-in-loop` | stable |
| performance-pass | Compile a regex once and reuse it (4 orgs) | `fn-regex-compiled-once` | stable |
| performance-pass | No blocking I/O or long CPU work on an event loop (4 orgs) | `fn-no-blocking-call-in-async-code` | stable |
| performance-pass | Filter, count, and aggregate in the query; select only used columns (4 orgs) | `fn-fetch-only-needed-data` | stable |
| performance-pass | Start independent I/O together (2 orgs plus an opinion source) | `fn-independent-work-concurrent` | stable |
| performance-pass | Build pooled clients once and reuse them (4 orgs) | `mod-pooled-clients-built-once` | stable |
| performance-pass | Paginate every list endpoint, with a default and a maximum (5 orgs; 4 for the maximum) | `svc-list-endpoint-paginates` | stable |
| performance-pass | Timeout on every remote call (3 orgs; deriving it from the caller's deadline has 2 and sits in Why) | `svc-timeouts` | stable |
| performance-pass | One query or batch for related rows, never one per row (4 orgs) | `sys-n-plus-one-pooling` | stable |
| performance-pass | Bound and expire every cache (3 orgs; invalidation 1) | `sys-cache-bounds-invalidation` | stable |
| performance-pass | A deadline and a miss policy on every fan-out leg (5 orgs) | `sys-fanout-leg-deadlines` | stable |
| performance-pass | Bounded queues and cheap rejection (5 orgs, corroboration only) | `sys-load-shedding-bounded-queues` | stable |
| performance-pass | A CI check fails the build on the performance budget (7 orgs) | `code-perf-budget-in-ci` | stable |
| performance-pass | Load test past peak on production-like infrastructure before launch (3 orgs) | `prod-load-test-before-launch` | stable |
| performance-pass | Latency SLOs and alerts on histogram percentiles, not the mean (3 firm orgs) | `prod-latency-slo-percentile` | stable |
| performance-pass | A production profile is obtainable without a redeploy (4 orgs) | `prod-profile-on-demand` | stable |
| performance-pass | A performance fix names its bottleneck with a profile or trace (4 orgs) | `inc-perf-fix-has-profile-evidence` | stable |
| performance-pass | A perf postmortem adds an automated regression guard (5 orgs) | `inc-perf-regression-guard` | draft |
| performance-pass | Benchmark for every hot-path change | dropped: a reviewer cannot tell a hot path without a profile; covered by `chg-perf-claim-evidence` and `code-perf-budget-in-ci` | dropped |
| performance-pass | Per-hop latency budget across a system | dropped: 2 orgs, and `svc-timeouts` already derives from the remaining deadline | dropped |
| performance-pass | Cap fan-out width | dropped: 1 org (Google) | dropped |
| performance-pass | Keep benchmarks runnable | dropped: the budget job runs them; Go, Rust, and JMH docs not read | dropped |

## Frontend pass

From `docs/research/frontend-pass.md`. Every card here carries the `accessibility` or `usability` concern and the `frontend` tag. The org count is the number of independent organisations behind the Rule. All cards are drafts.

| Source | Item | Maps to | Status |
|---|---|---|---|
| frontend-pass | Every image has an `alt`, empty when decorative (5 orgs) | `fn-img-alt-text` | stable |
| frontend-pass | Every form control has a visible, programmatic label (5 orgs) | `fn-form-control-has-label` | stable |
| frontend-pass | `button` for actions, `a href` for navigation (4 orgs) | `fn-native-button-or-link` | stable |
| frontend-pass | Visible, unobscured focus indicator (4 orgs) | `fn-focus-indicator-visible` | stable |
| frontend-pass | A modal moves focus in, traps it, closes on Escape, and returns focus (3 orgs; the return step has 1) | `fn-dialog-focus-managed` | stable |
| frontend-pass | No `tabindex` above 0; DOM in reading order (3 orgs) | `fn-no-positive-tabindex` | stable |
| frontend-pass | A custom widget gets its state and keys (3 orgs each; the name has 2 and sits in Why) | `fn-aria-role-has-state-and-keys` | stable |
| frontend-pass | Async status goes through a live region that already exists (3 orgs) | `fn-status-announced-live-region` | stable |
| frontend-pass | Real headings in outline order (3 orgs) | `fn-heading-structure` | stable |
| frontend-pass | A second cue beside colour (4 orgs) | `fn-colour-not-sole-cue` | stable |
| frontend-pass | Pointer targets 24 by 24 CSS px or spaced (3 orgs) | `fn-target-size` | stable |
| frontend-pass | Reduce or remove large motion under `prefers-reduced-motion` (5 orgs; WCAG level AAA) | `fn-reduced-motion-respected` | stable |
| frontend-pass | Error next to the field, naming the problem and the fix (5 orgs) | `fn-error-says-what-and-how` | stable |
| frontend-pass | Keep the entered values after a failed submit (3 orgs plus 1 related) | `fn-keep-input-on-error` | stable |
| frontend-pass | Undo or a named-outcome confirmation for destructive actions (4 orgs) | `fn-destructive-confirm-or-undo` | stable |
| frontend-pass | Colour tokens meet 4.5:1 for text and 3:1 for UI parts (5 orgs) | `mod-colour-tokens-meet-contrast` | stable |
| frontend-pass | Do not ask again for what the flow already has (3 orgs) | `svc-no-redundant-entry` | stable |
| frontend-pass | Feedback past 1 s, progress and cancel past 10 s (4 orgs) | `svc-slow-operation-shows-progress` | stable |
| frontend-pass | Reserve space for late content (1 firm org, 2 indirect) | `svc-async-content-reserves-space` | draft |
| frontend-pass | Usable at 320 CSS px and 200% text zoom; zoom not blocked (2 orgs) | `svc-reflow-and-zoom` | stable |
| frontend-pass | A unique `<title>` per page and client-side view (3 orgs) | `svc-page-title-per-route` | draft |
| frontend-pass | One label, icon, and place per action across screens (4 orgs) | `sys-consistent-ui-terms` | stable |
| frontend-pass | An automated accessibility check in the tests fails on a violation (3 orgs; tools find a minority) | `code-a11y-check-in-ci` | draft |
| frontend-pass | A UI change ships screenshots and a keyboard and zoom pass (3 orgs; screenshots unsourced) | `chg-ui-change-screenshots-and-keyboard-pass` | draft |
| frontend-pass | Audit with assistive technology before a public launch (3 orgs, one weak) | `prod-a11y-audit-before-launch` | draft |
| frontend-pass | Empty states say what is missing and offer a next action | dropped: 1 org (NN/g) | dropped |
| frontend-pass | Declare the page language with `lang` | dropped: 1 firm org plus the A11y Project checklist, small gain over `svc-page-title-per-route` | dropped |
| frontend-pass | A component requires an accessible name as a prop | dropped: the call site fails `fn-form-control-has-label` or `fn-native-button-or-link` | dropped |
| frontend-pass | Validate on blur versus on submit | dropped: GOV.UK and Baymard disagree | dropped |
| frontend-pass | Incident-level accessibility card | dropped: no source describes an accessibility incident review | dropped |
| frontend-pass | Material Design target and contrast guidance | dropped: the Material pages returned only a title | dropped |

## Alerting pass

Source: `docs/research/alerting-pass.md`. Row numbers are that file's.

| Source | Item | Maps to | Status |
|---|---|---|---|
| alerting-pass | 1-3 Page on user-visible symptoms such as error rate and latency; hold an error-rate alert for a few minutes | `prod-alerts-symptoms-golden-signals` | stable |
| alerting-pass | 4 Alert on workload health, not arbitrary values | dropped: never says symptoms or causes, so it adds no org to the Rule | dropped |

## Company sweep new cards

Source: `docs/research/new-cards-pass-1.md`, which verifies leads from the company sweeps.

| Source | Item | Maps to | Status |
|---|---|---|---|
| company-sweep | Run old and new side by side and diff outputs or snapshots before moving traffic (Netflix, Stripe, Airbnb, GitHub) | `prod-shadow-compare-before-cutover` | draft |
| company-sweep | Non-critical dependencies are best-effort and every fallback is counted (Netflix, Uber, Cabify) | `svc-best-effort-optional-deps` | draft |
| company-sweep | Cap blast radius with independent cells (Netflix, Slack, Airbnb, Cloudflare) | `sys-cells-limit-blast-radius` | draft |
| company-sweep | Flaky tests: report passes after retry, quarantine with an owner, verify the fix with many reruns (Dropbox, Shopify) | `code-flaky-test-quarantine` | draft |
| company-sweep | Rate-limit by cost, not request count (Shopify, GitHub, Airbnb) | `svc-rate-limit-by-cost` | draft |

## Security gaps pass 2

Source: `docs/research/security-gaps-pass-2.md`, which verifies sources for the gaps in sections 2 and 3 of `docs/research/security-gaps.md`.

| Source | Item | Maps to | Status |
|---|---|---|---|
| security-gaps | CWE-94 code injection through `eval`, `exec`, or templates (ASVS 1.3.2, 1.3.7) | `fn-no-eval-untrusted` | draft |
| security-gaps | Open redirects and URL scheme checks (ASVS 3.7.2, 1.2.2) | `fn-redirect-target-allowlist` | draft |
| security-gaps | Sensitive data in URLs and query strings (ASVS 14.2.1) | `svc-no-secrets-in-url` | draft |
| security-gaps | XML external entities and parser hardening (ASVS 1.5.1) | `fn-xml-no-external-entities` | draft |
| security-gaps | CWE-306 missing authentication for a critical function | `svc-authn-by-default` | draft |
| security-gaps | Content Security Policy beyond `frame-ancestors` (ASVS 3.4.3) | `svc-csp-strict-script-src` | draft |
| security-gaps | Prototype pollution (ASVS 15.3.6) | `fn-no-prototype-pollution` | draft |
| security-gaps | TLS version and cipher policy for servers (ASVS 12.1.1, 12.1.2) | `svc-tls-modern-only` | draft |
| security-gaps | Credential recovery, MFA enrolment, reset flows (ASVS 6.4) | dropped: no single Rule that can fail; `svc-auth-throttle-generic-errors` covers reset endpoints | dropped |
| security-gaps | CWE-787, 125, 120, 121, 122, 416 memory safety | dropped: needs a `packs/<lang>/` pack that does not exist | dropped |
