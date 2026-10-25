---
id: svc-circuit-breaker-bulkhead
level: service
tags: [reliability, resilience, isolation]
severity: should-fix
status: draft
lacks: orgs, "per dependency" has Microsoft only; needs two more orgs that limit concurrency per downstream
lang: core
applies_when: A service calls several dependencies from shared pools, or retries a dependency that may be down.
tool_gate: none
borrowed_from:
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead
---

**Rule.** Give each critical dependency its own concurrency limit.

**Why.** One shared pool lets a slow dependency use every thread and starve healthy paths. Retrying a dead dependency only adds load, so also fail fast through a breaker with limited half-open probing where retries are demonstrably harmful.

**FAIL**

```text
pool = ThreadPool(50)               # used by billing, search, email alike
breaker = None                      # retries a dead host every request
```

**PASS**

```text
pools = {"billing": asyncio.Semaphore(10), "search": asyncio.Semaphore(20)}
# pseudocode: breaker logs and counts every state change; half-open allows 1 probe
```

**Counterpoint.** "More moving parts than a timeout." True. Start with the timeout and the per-dependency limit, and add the breaker where retries are demonstrably harmful. Retry and breaker have opposite aims, so do not present one as a substitute for the other.
