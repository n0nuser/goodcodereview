---
id: prod-alert-actionable-context
level: production
tags: [observability, monitoring, alerting]
severity: should-fix
status: stable
lang: core
applies_when: A service ships alert rules that page a person.
tool_gate: A lint on alert rules that requires a description and a runbook annotation.
note: Google SRE (every page should be actionable), Microsoft (alerts actionable and with context, an alerting process that defines owners, actions and scope), AWS Well-Architected OPS08-BP04 (create actionable alerts) and Datadog (context clarifies ownership and impact). Owner and runbook link have fewer than three organisations and stay in the Why; Grafana, Prometheus and Google Cloud only describe a runbook annotation field
borrowed_from:
  - https://sre.google/sre-book/monitoring-distributed-systems/
  - https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/observability
  - https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_workload_observability_create_alerts.html
  - https://docs.datadoghq.com/monitors/guide/monitor_best_practices.md
---

**Rule.** Give every paging alert context a responder can act on: what it means and what to do next.

**Why.** A page that says only "metric X is high" makes the responder start from nothing at 3 a.m. The usual form is a one-line description, the owning team and a link to a runbook for the first checks and the mitigation. Written-down steps shorten recovery time, and an alert with an owner cannot be ignored by default. Alerts that need no immediate action belong in a ticket queue, not a page ([[prod-alerts-symptoms-golden-signals]]).

**FAIL**

```yaml
- alert: HighErrorRatio
  expr: job:http_errors:ratio5m > 0.05
  for: 5m
  labels: {severity: page}
```

**PASS**

```yaml
- alert: HighErrorRatio
  expr: job:http_errors:ratio5m > 0.05
  for: 5m
  labels: {severity: page, team: payments}
  annotations:
    summary: "More than 5% of checkout requests fail"
    runbook_url: https://wiki.example.com/runbooks/checkout-errors
```

**Counterpoint.** "Runbooks go stale and nobody reads them." A stale runbook is a fixable defect, and the card asks only that the alert say what it means and where to start. Ticket-only and informational alerts need no runbook, so the rule covers rules that page.
