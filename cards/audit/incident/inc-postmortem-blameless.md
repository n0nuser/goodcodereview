---
id: inc-postmortem-blameless
level: incident
tags: [process, incident, learning]
severity: should-fix
status: stable
lang: core
applies_when: A postmortem, incident review or postmortem template is written or audited.
tool_gate: none
note: Google, PagerDuty, Atlassian and Microsoft (Azure Well-Architected) each state it; Atlassian says the timeline may still name who made which change, so the Rule bans names as the cause, not names
borrowed_from:
  - https://sre.google/sre-book/postmortem-culture/
  - https://postmortems.pagerduty.com/culture/blameless/
  - https://www.atlassian.com/incident-management/postmortem/blameless
  - https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/incident-response
---

**Rule.** Write a postmortem so that it names causes in the system and the decisions around it, never a person or team as the one at fault.

**Why.** People who expect blame stay quiet about what they saw and soften the timeline, so the contributing factors never reach the review. A cause of "someone was careless" also gives no action that prevents the next failure, while a cause such as "the schema accepted an empty list" does. The timeline may still say who made which change; only the verdict of fault is out.

**FAIL**

```text
Root cause: Dana pushed a bad config without testing it.
Action: Dana to be more careful with config changes.
```

**PASS**

```text
Contributing causes: the config schema accepted an empty region list, and the
deploy pipeline had no validation step for region lists.
14:02 Dana's change (PR 4412) merged with an empty list after the usual review.
Action (owner: platform, due 2026-12-10, ISSUE-518): reject empty lists in the
schema and add a validation step to the pipeline.
```

**Counterpoint.** "Blameless means nobody is accountable." Each change stays in the timeline with its author, and each action has an owner. What the rule refuses is the finding that a person caused the outage, because that finding ends the inquiry at the person and leaves the system as it was. It says nothing about performance management, which is a separate process.
