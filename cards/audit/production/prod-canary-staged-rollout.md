---
id: prod-canary-staged-rollout
level: production
tags: [reliability, deploys, release]
severity: block
status: stable
lang: core
applies_when: A change, config or dependency update is rolled out to production.
tool_gate: Deploy pipeline with canary stage and automatic abort.
borrowed_from:
  - https://sre.google/workbook/canarying-releases/
  - https://sre.google/sre-book/release-engineering/
  - https://aws.amazon.com/builders-library/minimizing-correlated-failures-in-distributed-systems/
  - https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
---

**Rule.** Roll out in stages behind a canary, and abort by rule, not by judgment.

**Why.** A 100% push exposes everyone to the bug. A canary must be large and long enough to be representative. Errors of 20% on 5% of traffic are only 1% overall, so tie the canary to your error budget.

**FAIL**

```text
deploy: all hosts at once, no comparison, rollback = "ask someone"
```

**PASS**

```text
# compare the canary to a control on a few chosen metrics
5% canary 30m -> compare error rate, p99 -> auto-rollback if worse -> 25% -> 100%
```

**See also.** [[inc-rollback-path-tested]] (drill the rollback).

**Counterpoint.** "Hotfixes can't wait." Then keep the canary short, not absent. Fleet tools should also have velocity limits. A hermetic, reproducible build tied to one revision ([[code-build-hermetic]]) is the precondition for rollback to mean anything.
