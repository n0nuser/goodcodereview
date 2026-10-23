---
id: svc-circuit-breaker-bulkhead
level: service
tags: [resilience, isolation]
severity: should-fix
status: draft
lang: core
applies_when: A service calls several dependencies from shared pools, or retries a dependency that may be down.
tool_gate: none
borrowed_from:
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead
---

**Rule.** Give each critical dependency its own concurrency limit, and fail fast through a breaker with limited half-open probing when it is down.

**Why.** One shared pool lets a slow dependency use every thread and starve healthy paths. Retrying a dead dependency only adds load.

**FAIL**

```text
pool = ThreadPool(50)               # used by billing, search, email alike
breaker = None                      # retries a dead host every request
```

**PASS**

```text
pools = {"billing": Sem(10), "search": Sem(20)}
breaker.state_change -> log + metric ; half_open allows 1 probe
```

**Counterpoint.** "More moving parts than a timeout." True; start with the timeout and the per-dependency limit, add the breaker where retries are demonstrably harmful. Retry and breaker have opposite aims, so do not present one as a substitute for the other.
