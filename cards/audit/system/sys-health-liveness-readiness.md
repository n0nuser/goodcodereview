---
id: sys-health-liveness-readiness
level: system
tags: [health, availability]
severity: block
status: draft
lang: core
applies_when: A service exposes a health endpoint used by a load balancer, orchestrator or auto-replacement.
tool_gate: none
borrowed_from:
  - https://aws.amazon.com/builders-library/implementing-health-checks/
---

**Rule.** Wire the load balancer and restarter to liveness and local checks only; dependency checks feed alarms, and a host must not evict itself because a shared dependency failed.

**Why.** If the database blips, every host fails its check, all are removed at once, and a partial outage becomes total.

**FAIL**

```text
GET /health -> SELECT 1 on primary db     # drives LB removal and restart
```

**PASS**

```text
/live: process responds ; /ready: local init done, no shared-dependency call
dependency status -> metric + alarm only
```

**Counterpoint.** Readiness that reflects a dependency feels more honest. AWS accepts fail-open designs but is wary of behavior it cannot fully test, so a fail-open health policy counts as PASS only if you have actually tested it.
