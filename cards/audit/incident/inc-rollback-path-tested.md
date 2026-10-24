---
id: inc-rollback-path-tested
level: incident
tags: [incident, rollback]
severity: should-fix
status: draft
lang: core
applies_when: A runbook or incident response relies on rollback, failover, or a manual mitigation.
tool_gate: none
borrowed_from:
  - https://sre.google/workbook/canarying-releases/
  - https://aws.amazon.com/builders-library/implementing-health-checks/
---

**Rule.** Run the mitigation named in a runbook (rollback, failover, flag off) recently, and state in the runbook who may trigger it.

**Why.** Rollbacks fail on schema changes or removed artifacts, and untested failover paths rot. Canary guidance assumes an abort rule that actually works, and AWS is cautious about fail-open behavior it cannot test.

**FAIL**

```text
Runbook: "roll back to previous version" (last attempted: never; migration not reversible)
```

**PASS**

```text
Runbook: rollback drill 2026-10-01, schema is expand-only, on-call may trigger.
```

**See also.** [[chg-rollback-path]], [[prod-canary-staged-rollout]].

**Counterpoint.** "Drills are costly." Do one when a migration or release process changes. It is cheaper than discovering during an outage that rollback is impossible.
