# Coverage

Every source item maps to a check id (`cards/`), a glossary term (`glossary/`), or an explicit `dropped: <reason>`.
Nothing leaves without a row.

Source `111-list` rows come from `docs/coverage-111.md`; ids are reserved, no card exists yet.

| Source | Item | Maps to | Status |
|---|---|---|---|
| 111-list #1 | Rate Limiting | cards: `svc-rate-limit-quota` | reserved (draft) |
| 111-list #2 | Caching | cards: `svc-cache-miss-protection` | reserved (draft) |
| 111-list #3 | Load Balancing | glossary: `load-balancing` | glossary |
| 111-list #4 | Reverse Proxies | glossary: `reverse-proxies` | glossary |
| 111-list #5 | API Gateways | glossary: `api-gateways` | glossary |
| 111-list #6 | CI/CD | cards: `code-ci-workflow-hardening` | reserved (draft) |
| 111-list #7 | Docker | glossary: `docker` | glossary |
| 111-list #8 | Kubernetes | glossary: `kubernetes` | glossary |
| 111-list #9 | Service Discovery | glossary: `service-discovery` | glossary |
| 111-list #10 | Circuit Breakers | cards: `svc-circuit-breaker` | reserved (draft) |
| 111-list #11 | Timeouts | cards: `svc-timeouts` | reserved (draft) |
| 111-list #12 | Retries | cards: `svc-retry-policy` | reserved (draft) |
| 111-list #13 | Exponential Backoff | cards: `svc-retry-jitter` | reserved (draft) |
| 111-list #14 | Idempotency | cards: `svc-idempotency-key` | reserved (draft) |
| 111-list #15 | Message Queues | cards: `svc-queue-visibility-timeout` | reserved (draft) |
| 111-list #16 | Pub/Sub | glossary: `pub-sub` | glossary |
| 111-list #17 | Event-Driven Architecture | glossary: `event-driven-architecture` | glossary |
| 111-list #18 | Distributed Transactions | glossary: `distributed-transactions` | glossary |
| 111-list #19 | Saga Pattern | cards: `svc-saga-steps` | reserved (draft) |
| 111-list #20 | Dead Letter Queues | cards: `svc-queue-dlq` | reserved (draft) |
| 111-list #21 | Cron Jobs | cards: `svc-singleton-job-idempotent` | reserved (draft) |
| 111-list #22 | WebSockets | glossary: `websockets` | glossary |
| 111-list #23 | Long Polling | glossary: `long-polling` | glossary |
| 111-list #24 | Server-Sent Events | glossary: `server-sent-events` | glossary |
| 111-list #25 | Database Indexing | cards: `chg-migration-index-concurrently` | reserved (draft) |
| 111-list #26 | Query Optimization | glossary: `query-optimization` | glossary |
| 111-list #27 | N+1 Queries | cards: `fn-n-plus-one` | reserved (draft) |
| 111-list #28 | Connection Pooling | cards: `svc-bulkhead-pools` | reserved (draft) |
| 111-list #29 | Read Replicas | glossary: `read-replicas` | glossary |
| 111-list #30 | Sharding | glossary: `sharding` | glossary |
| 111-list #31 | Partitioning | glossary: `partitioning` | glossary |
| 111-list #32 | Replication | glossary: `replication` | glossary |
| 111-list #33 | Leader Election | cards: `svc-leader-two-leaders` | reserved (draft) |
| 111-list #34 | CAP Theorem | glossary: `cap-theorem` | glossary |
| 111-list #35 | Eventual Consistency | glossary: `eventual-consistency` | glossary |
| 111-list #36 | Optimistic Locking | glossary: `optimistic-locking` | glossary |
| 111-list #37 | Pessimistic Locking | glossary: `pessimistic-locking` | glossary |
| 111-list #38 | Distributed Locks | cards: `svc-lock-fencing` | reserved (draft) |
| 111-list #39 | Race Conditions | glossary: `race-conditions` | glossary |
| 111-list #40 | Deadlocks | glossary: `deadlocks` | glossary |
| 111-list #41 | Memory Leaks | cards: `fn-resource-lifetime` | reserved (draft) |
| 111-list #42 | Garbage Collection | glossary: `garbage-collection` | glossary |
| 111-list #43 | Thread Safety | glossary: `thread-safety` | glossary |
| 111-list #44 | Backpressure | cards: `svc-queue-backlog-controls` | reserved (draft) |
| 111-list #45 | Autoscaling | glossary: `autoscaling` | glossary |
| 111-list #46 | Horizontal Scaling | glossary: `horizontal-scaling` | glossary |
| 111-list #47 | Vertical Scaling | glossary: `vertical-scaling` | glossary |
| 111-list #48 | CDN | glossary: `cdn` | glossary |
| 111-list #49 | Edge Caching | glossary: `edge-caching` | glossary |
| 111-list #50 | Cache Invalidation | cards: `svc-cache-entry-version` | reserved (draft) |
| 111-list #51 | Feature Flags | cards: `chg-flag-off-switch` | reserved (draft) |
| 111-list #51b | Feature Flags (telemetry) | cards: `prod-change-markers` | reserved (draft) |
| 111-list #52 | Blue-Green Deployment | glossary: `blue-green-deployment` | glossary |
| 111-list #53 | Canary Releases | cards: `prod-canary-gate` | reserved (draft) |
| 111-list #54 | Rolling Deployments | cards: `prod-rollout-velocity` | reserved (draft) |
| 111-list #55 | Rollbacks | cards: `prod-rollback-rule` | reserved (draft) |
| 111-list #56 | Health Checks | cards: `svc-health-check-scope` | reserved (draft) |
| 111-list #57 | Liveness & Readiness Probes | glossary: `liveness-readiness-probes` | glossary |
| 111-list #58 | Monitoring | cards: `prod-golden-signals` | reserved (draft) |
| 111-list #59 | Logging | cards: `code-log-safety` | reserved (draft) |
| 111-list #60 | Distributed Tracing | glossary: `distributed-tracing` | glossary |
| 111-list #61 | Metrics | cards: `prod-metric-label-cardinality` | reserved (draft) |
| 111-list #62 | Alerts | cards: `prod-alert-symptom` | reserved (draft) |
| 111-list #63 | SLOs | glossary: `slos` | glossary |
| 111-list #64 | SLIs | glossary: `slis` | glossary |
| 111-list #65 | Error Budgets | glossary: `error-budgets` | glossary |
| 111-list #66 | Observability | cards: `prod-wide-event-fields` | reserved (draft) |
| 111-list #67 | Secrets Management | cards: `code-error-response-leak` | reserved (draft) |
| 111-list #68 | IAM | glossary: `iam` | glossary |
| 111-list #69 | OAuth | glossary: `oauth` | glossary |
| 111-list #70 | JWT Rotation | glossary: `jwt-rotation` | glossary |
| 111-list #71 | TLS | glossary: `tls` | glossary |
| 111-list #72 | Encryption at Rest | glossary: `encryption-at-rest` | glossary |
| 111-list #73 | Encryption in Transit | glossary: `encryption-in-transit` | glossary |
| 111-list #74 | WAF | glossary: `waf` | glossary |
| 111-list #75 | DDoS Protection | glossary: `ddos-protection` | glossary |
| 111-list #76 | CORS | glossary: `cors` | glossary |
| 111-list #77 | CSRF | glossary: `csrf` | glossary |
| 111-list #78 | SQL Injection | cards: `code-injection` | reserved (draft) |
| 111-list #79 | XSS | cards: `code-injection` | reserved (draft) |
| 111-list #80 | SSRF | cards: `code-ssrf` | reserved (draft) |
| 111-list #81 | Database Migrations | cards: `chg-migration-lock-timeout` | reserved (draft) |
| 111-list #81b | Database Migrations (constraints) | cards: `chg-migration-not-valid` | reserved (draft) |
| 111-list #81c | Database Migrations (rewrite) | cards: `chg-migration-add-column-rewrite` | reserved (draft) |
| 111-list #81d | Database Migrations (backfill) | cards: `chg-migration-schema-data-split` | reserved (draft) |
| 111-list #82 | Schema Versioning | cards: `chg-migration-expand-contract` | reserved (draft) |
| 111-list #83 | Disaster Recovery | glossary: `disaster-recovery` | glossary |
| 111-list #84 | Backups | glossary: `backups` | glossary |
| 111-list #85 | Failover | glossary: `failover` | glossary |
| 111-list #86 | Multi-Region Deployment | glossary: `multi-region-deployment` | glossary |
| 111-list #87 | Chaos Engineering | glossary: `chaos-engineering` | glossary |
| 111-list #88 | Cost Optimization | glossary: `cost-optimization` | glossary |
| 111-list #89 | Cold Starts | glossary: `cold-starts` | glossary |
| 111-list #90 | Serverless Limits | glossary: `serverless-limits` | glossary |
| 111-list #91 | Latency | glossary: `latency` | glossary |
| 111-list #92 | Throughput | glossary: `throughput` | glossary |
| 111-list #93 | P99 Latency | glossary: `p99-latency` | glossary |
| 111-list #94 | Tail Latency | glossary: `tail-latency` | glossary |
| 111-list #95 | Network Partitions | glossary: `network-partitions` | glossary |
| 111-list #96 | Clock Skew | glossary: `clock-skew` | glossary |
| 111-list #97 | DNS | glossary: `dns` | glossary |
| 111-list #98 | TCP vs UDP | glossary: `tcp-vs-udp` | glossary |
| 111-list #99 | HTTP/2 & HTTP/3 | glossary: `http2-http3` | glossary |
| 111-list #100 | gRPC | glossary: `grpc` | glossary |
| 111-list #101 | Webhooks | glossary: `webhooks` | glossary |
| 111-list #102 | API Versioning | cards: `chg-observable-behavior-change` | reserved (draft) |
| 111-list #103 | Semantic Versioning | glossary: `semantic-versioning` | glossary |
| 111-list #104 | Infrastructure as Code | glossary: `infrastructure-as-code` | glossary |
| 111-list #105 | Terraform | glossary: `terraform` | glossary |
| 111-list #106 | Helm Charts | glossary: `helm-charts` | glossary |
| 111-list #107 | Build Caching | cards: `code-build-hermetic` | reserved (draft) |
| 111-list #108 | Dependency Hell | cards: `code-deps-pinned` | reserved (draft) |
| 111-list #109 | Production Incidents | glossary: `production-incidents` | glossary |
| 111-list #110 | On-Call | glossary: `on-call` | glossary |
| 111-list #111 | Postmortems | glossary: `postmortems` | glossary |
| 111-list #X1 | Concurrency (task reference) | cards: `py-create-task-reference` | reserved (draft) |
| 111-list #X2 | Concurrency (cancellation) | cards: `py-cancelled-error-reraise` | reserved (draft) |
| 111-list #X3 | Concurrency (timeout handler) | cards: `py-timeout-handler-outside` | reserved (draft) |
| 111-list #X4 | Concurrency (bounded await) | cards: `py-remote-await-bounded` | reserved (draft) |
| 111-list #X5 | Async vs Sync | cards: `mod-prefer-sync-api` | reserved (draft) |
| 111-list #X6 | Clean Code | glossary: `clean-code` | glossary |
| 111-list #X7 | YAGNI | cards: `chg-speculative-extension-point` | reserved (draft) |
| 111-list #X8 | Grug | glossary: `grug` | glossary |
| 111-list #X9 | SOLID | glossary: `solid` | glossary |
| 111-list #X9b | SOLID (Liskov) | cards: `mod-subtype-passes-parent-tests` | reserved (draft) |
| 111-list #X10 | TDD | glossary: `tdd` | glossary |
| 111-list #X11 | DDD | glossary: `ddd` | glossary |
| 111-list #X12 | Fowler's 12 smells | glossary: `fowlers-smells` | glossary |
| 111-list #X13 | Pocock Standards axis | cards: `chg-standards-conform` | reserved (draft) |
| 111-list #X14 | Pocock Spec axis | cards: `chg-spec-match` | reserved (draft) |
| 111-list #X15 | Thermo-nuclear points | glossary: `thermo-nuclear` | glossary |
| research gap | chg-size-split (see coverage-111 Missing topics) | cards: `chg-size-split` | reserved |
| research gap | chg-refactor-separate (see coverage-111 Missing topics) | cards: `chg-refactor-separate` | reserved |
| research gap | chg-characterization-test (see coverage-111 Missing topics) | cards: `chg-characterization-test` | reserved |
| research gap | chg-problem-stated (see coverage-111 Missing topics) | cards: `chg-problem-stated` | reserved |
| research gap | chg-tests-with-code (see coverage-111 Missing topics) | cards: `chg-tests-with-code` | reserved |
| research gap | chg-no-rewrite-without-defect (see coverage-111 Missing topics) | cards: `chg-no-rewrite-without-defect` | reserved |
| research gap | mod-deep-module (see coverage-111 Missing topics) | cards: `mod-deep-module` | reserved |
| research gap | mod-abstraction-proven (see coverage-111 Missing topics) | cards: `mod-abstraction-proven` | reserved |
| research gap | fn-comment-adds-information (see coverage-111 Missing topics) | cards: `fn-comment-adds-information` | reserved |
| research gap | fn-error-swallow (see coverage-111 Missing topics) | cards: `fn-error-swallow` | reserved |
| research gap | code-supply-chain-provenance (see coverage-111 Missing topics) | cards: `code-supply-chain-provenance` | reserved |
| research gap | code-llm-output-untrusted (see coverage-111 Missing topics) | cards: `code-llm-output-untrusted` | reserved |
| research gap | code-ai-pr-disclosure (see coverage-111 Missing topics) | cards: `code-ai-pr-disclosure` | reserved |
| research gap | prod-hermetic-release-review (see coverage-111 Missing topics) | cards: `prod-hermetic-release-review` | reserved |
| research gap | inc-* (see coverage-111 Missing topics) | cards: `inc-*` | reserved |
| research gap | code-secret-scan (see coverage-111 Missing topics) | cards: `code-secret-scan` | reserved |
| research gap | Reviewer conduct | README process section | reserved |
