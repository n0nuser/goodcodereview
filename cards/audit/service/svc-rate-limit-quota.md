---
id: svc-rate-limit-quota
level: service
tags: [security, reliability, multi-tenant, overload]
severity: should-fix
status: draft
lang: core
applies_when: A shared API or queue serves several tenants or callers.
tool_gate: none
borrowed_from:
  - https://aws.amazon.com/builders-library/fairness-in-multi-tenant-systems/
  - https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/
---

**Rule.** Enforce a per-tenant quota on shared APIs and queues.

**Why.** Without a quota, one noisy tenant consumes shared capacity for everyone. Also add a per-tenant concurrency cap, and return 429 for over-quota but 503 for the service's own lack of capacity, so clients do not retry quota errors as capacity problems.

**FAIL**

```text
every tenant shares one worker pool, no limit
if over_limit: return 503
```

**PASS**

```text
limiter.check(tenant_id) -> 429 + Retry-After
per-tenant semaphore on workers
```

**See also.** [[svc-api-retry-after]] covers the `Retry-After` header the 429 must carry.

**Counterpoint.** AWS notes that some of its older services use 503 for quota errors for historical reasons, so 429 is a convention, not law. The substance is per-tenant limits and distinguishable errors. Shuffle sharding (per-tenant worker subsets) is a stronger isolation option that this card does not require.
