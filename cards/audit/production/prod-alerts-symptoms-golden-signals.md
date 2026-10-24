---
id: prod-alerts-symptoms-golden-signals
level: production
tags: [monitoring, alerting]
severity: should-fix
status: draft
lang: core
applies_when: A service ships alerts or dashboards.
tool_gate: none
borrowed_from:
  - https://sre.google/sre-book/monitoring-distributed-systems/
---

**Rule.** Page on user-visible symptoms, not causes.

**Why.** Cause-based pages (CPU high) wake people without user impact. A mean hides the slow tail, and failed-request latency mixed with successes hides both. Also cover latency, traffic, errors, and saturation, track latency as a distribution, and delete alerts that never fire.

**FAIL**

```text
alert: cpu > 80%  -> page
dashboard: avg latency only
```

**PASS**

```text
alert: error ratio > X over 5m -> page
latency p50/p99 histogram, errors split from successes
```

**Counterpoint.** Cause alerts help diagnosis. Keep them as tickets or dashboard hints, not pages. The Honeycomb wide-event camp argues against pre-set metrics, while the SRE book favors simple metric-based paging, so this card does not ban events, only cause-paging.
