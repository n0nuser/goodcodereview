---
id: prod-alert-links-runbook
level: production
tags: [observability, alerting, process]
severity: should-fix
status: draft
lacks: orgs, "link a runbook" has Google and Grafana Labs; Prometheus links consoles only and shares an author with Google; needs one more org
lang: core
applies_when: A service ships alert rules that page a person.
tool_gate: A CI check that fails an alert rule with no runbook or dashboard annotation.
note: Google (each alert has a playbook entry), Grafana (annotations link dashboards and runbooks), Prometheus (alerts link to consoles). New Relic and Atlassian mention a runbook field in their own products, which is descriptive. Datadog, AWS and Azure pages had no matching sentence
borrowed_from:
  - https://sre.google/workbook/on-call/
  - https://prometheus.io/docs/practices/alerting/
  - https://grafana.com/docs/grafana/latest/alerting/guides/best-practices/
---

**Rule.** Link each paging alert to a runbook or dashboard that says what to check and do.

**Why.** A page at 3am reaches someone who may not know the service. Without a link they search for context while the outage runs. A runbook that nobody maintains misleads, so review the link when the alert changes.

**FAIL**

```yaml
groups:
  - name: api
    rules:
      - alert: HighErrorRatio
        expr: job:request_errors:ratio5m > 0.05
        for: 5m
        labels:
          severity: page
```

**PASS**

```yaml
groups:
  - name: api
    rules:
      - alert: HighErrorRatio
        expr: job:request_errors:ratio5m > 0.05
        for: 5m
        labels:
          severity: page
        annotations:
          runbook_url: https://wiki.example.com/runbooks/high-error-ratio
          dashboard: https://grafana.example.com/d/api-overview
```

**Counterpoint.** "Runbooks go stale, and a stale one is worse than none." Keep each one short, change it in the same change as the alert, and drill the mitigations it names ([[inc-rollback-path-tested]]). An alert whose action cannot be written down is a sign it should not page.
