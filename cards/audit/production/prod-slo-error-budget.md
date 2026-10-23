---
id: prod-slo-error-budget
level: production
tags: [reliability, slo]
severity: discuss
status: draft
lang: core
applies_when: A service has users or dependents who rely on its availability.
tool_gate: none
borrowed_from: []
---

**Rule.** Define an SLO with an indicator and window, and use its remaining error budget to gate risky releases.

**Why.** Without a stated target nobody can say if reliability work or a freeze is warranted; every incident is argued from feelings.

**FAIL**

```text
"we aim for high availability" ; no SLI, alerts at arbitrary thresholds
```

**PASS**

```text
SLO: 99.9% of requests succeed in 300ms over 30d ; budget burn alert; freeze at 0
```

**Counterpoint.** "SLOs are bureaucracy for small teams." A one-line target is enough; skip it for internal tools with no users. docs/research has no SLO page (only a canary note that references a budget), so the card is draft and unsourced.
