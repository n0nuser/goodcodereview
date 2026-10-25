---
id: prod-alerts-symptoms-golden-signals
level: production
tags: [observability, monitoring, alerting]
severity: should-fix
status: stable
lang: core
applies_when: A service ships alerts or dashboards.
tool_gate: none
borrowed_from:
  - https://sre.google/sre-book/monitoring-distributed-systems/
  - https://prometheus.io/docs/practices/alerting/
  - https://grafana.com/docs/grafana/latest/alerting/guides/best-practices/
  - https://www.datadoghq.com/blog/monitoring-101-alerting/
---

**Rule.** Page on user-visible symptoms, such as error rate and latency, not on causes.

**Why.** Cause-based pages (CPU high) wake people without user impact. A mean hides the slow tail, and failed-request latency mixed with successes hides both. Require an error-rate alert to hold for a few minutes, so one blip does not page. Also cover latency, traffic, errors, and saturation, track latency as a distribution, and delete alerts that never fire.

**FAIL**

```text
alert: cpu > 80%  -> page
dashboard: avg latency only
```

**PASS**

```text
alert: error ratio > X, for 5m -> page
latency p50/p99 histogram, errors split from successes
```

**Counterpoint.** Cause alerts help diagnosis. Keep them as tickets or dashboard hints, not pages. The Honeycomb wide-event camp argues against pre-set metrics, while the SRE book favors simple metric-based paging, so this card does not ban events, only cause-paging.
