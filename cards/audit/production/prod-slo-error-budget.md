---
id: prod-slo-error-budget
level: production
tags: [reliability, observability, slo]
severity: discuss
status: draft
lacks: orgs, gating releases on the error budget has no backing row
note: no source yet; first-hand reasoning
lang: core
applies_when: A service has users or dependents who rely on its availability.
tool_gate: none
borrowed_from: []
---

**Rule.** Define an SLO with an indicator and window, and use its remaining error budget to gate risky releases.

**Why.** Without a stated target, nobody can say whether reliability work or a freeze is warranted, and every incident is argued from feelings.

**FAIL**

```text
"we aim for high availability" ; no SLI, alerts at arbitrary thresholds
```

**PASS**

```text
SLO: 99.9% of requests succeed in 300ms over 30d ; budget burn alert; freeze at 0
```

**Counterpoint.** "SLOs are bureaucracy for small teams." A one-line target is enough. Skip it for internal tools with no users.
