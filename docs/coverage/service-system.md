# Coverage: service, system, production, incident

Source check (docs/research/ops-docs-recheck.md) -> card id. Cards with no source are marked `borrowed_from: []`, status draft.

## Source check -> card

| Source check | Card |
|---|---|
| asyncio: discarded create_task, TaskGroup, shield | py-task-reference |
| asyncio: swallowed CancelledError, TimeoutError inside timeout block | py-cancellation |
| asyncio: await without timeout bound; Azure retry/timeouts | svc-timeouts |
| Azure retry: backoff, attempts, non-transient, stacked layers; AWS correlated: jitter | svc-retry-policy |
| Azure retry/saga: idempotency, unique saga id | svc-idempotency-key |
| Azure circuit breaker and bulkhead | svc-circuit-breaker-bulkhead |
| AWS queues: DLQ, visibility timeout, queue age | svc-dlq |
| AWS fairness / shuffle sharding: per-tenant quota, 429 vs 503 | svc-rate-limit-quota |
| AWS queues: bounded queue, sideline, cheap shedding | sys-load-shedding-bounded-queues |
| Kleppmann / antirez: fencing, check-and-set, disagreement | sys-lock-fencing |
| AWS leader election: two leaders, lease check | sys-leader-two-leaders |
| AWS caching: TTL, size, metrics, versioned values | sys-cache-bounds-invalidation |
| AWS caching: cold start, stampede, cache-off test | sys-cache-cold-start |
| AWS health checks: liveness vs dependency, self-eviction | sys-health-liveness-readiness |
| PG config + altertable: lock_timeout | sys-migration-lock-timeout |
| PG altertable: NOT VALID / VALIDATE | sys-constraint-not-valid |
| PG createindex: CONCURRENTLY, INVALID leftovers | sys-index-concurrently |
| GitLab migration style + avoiding downtime | sys-migration-expand-contract |
| OWASP A03:2025, Scorecard, SLSA | dropped here; home is the code-* cards (code-dependency-pinning, code-workflow-supply-chain, code-dependency-licence-sbom) |
| OWASP LLM01 | sys-prompt-injection |
| OWASP A10:2025, ASVS V16 (error leaks, fail open, log data) | sys-secrets-and-errors |
| OWASP A01 (SSRF folded in) | sys-ssrf |
| OWASP A05 / A07 / A01 (index only) | svc-sqli-authn |
| SRE monitoring | prod-alerts-symptoms-golden-signals |
| Honeycomb wide events, cardinality, deploy markers | prod-wide-events-bounded-labels |
| SRE canary + release engineering, AWS velocity control | prod-canary-staged-rollout |
| AWS cache-off test, ASVS degradation path | prod-kill-switch-fallback (fallback half; kill switch unsourced) |
| Canary / health-check fail-open caution | inc-rollback-path-tested |

## Cards with no source in docs/research (first-hand, draft)

Check-then-act across await: dropped here; home is [[fn-no-check-then-act-across-await]].

svc-api-compat-pagination, sys-n-plus-one-pooling, prod-slo-error-budget, inc-postmortem-owned-actions. Also partly unsourced: svc-sqli-authn and sys-ssrf (OWASP index only), sys-secrets-and-errors (secret storage), prod-kill-switch-fallback (kill switch).

## Not covered by a card (no FAIL): glossary candidates

- Shuffle sharding (tenant-to-shard assignment; reviewable only as "exists")
- Efficiency vs correctness lock
- Breaker vs retry purpose
- Saga data anomalies; pivot/compensable/retryable steps
- Canary arithmetic (error share vs traffic share)
- Prompt injection vs jailbreaking
- Retry budget (not defined in sources)
- CSRF and CORS: no source read; add cards once a primary source is added
- Lock mode conflict table; `ADD CONSTRAINT ... USING INDEX` (not verified)
- Cheap load shedding and slowed fast errors
- Unread: OWASP LLM10 Unbounded Consumption, ASVS V1-V15, Azure DLQ page
