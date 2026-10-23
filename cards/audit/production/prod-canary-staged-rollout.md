---
id: prod-canary-staged-rollout
level: production
tags: [deploys, release]
severity: block
status: draft
lang: core
applies_when: A change, config or dependency update is rolled out to production.
tool_gate: Deploy pipeline with canary stage and automatic abort.
borrowed_from:
  - https://sre.google/workbook/canarying-releases/
  - https://sre.google/sre-book/release-engineering/
  - https://aws.amazon.com/builders-library/minimizing-correlated-failures-in-distributed-systems/
---

**Rule.** Roll out to a small canary first, compare it automatically to a control on a few chosen metrics, and abort or roll back by rule, not by judgment at 3am.

**Why.** A 100% push exposes everyone to the bug. A canary must be large and long enough to be representative; 20% errors on 5% of traffic is only 1% overall, so tie the canary to your error budget.

**FAIL**

```text
deploy: all hosts at once, no comparison, rollback = "ask someone"
```

**PASS**

```text
5% canary 30m -> compare error rate, p99 -> auto-rollback if worse -> 25% -> 100%
```

**Counterpoint.** "Hotfixes can't wait." Then keep the canary short, not absent. Fleet tools should also have velocity limits; a hermetic, reproducible build tied to one revision is the precondition for rollback to mean anything.
