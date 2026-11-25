---
id: inc-single-incident-commander
level: incident
tags: [process, incident, reliability]
severity: discuss
status: stable
lang: core
applies_when: The repo or wiki holds an incident policy or runbook that covers major incidents. A repo with no such document has nothing to fail, so mark the card N/A.
tool_gate: none
note: Google, PagerDuty and AWS name the commander role; Atlassian's handbook describes its own process and is not counted. Google and PagerDuty scope the role to major incidents
borrowed_from:
  - https://sre.google/sre-book/managing-incidents/
  - https://response.pagerduty.com/before/different_roles/
  - https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_event_response_push_notify.html
---

**Rule.** Name one incident commander for each major incident, who holds the overall state of the response and oversees the other roles.

**Why.** Without one person holding the whole picture, responders duplicate each other, change the system in parallel and wait for someone else to decide. The commander does not need to be the most senior or the most technical person present; the role is to keep the state and assign the work.

**FAIL**

```text
Incident policy: when a major incident starts, the on-call engineers and the
manager join the channel and work it out together.
```

**PASS**

```text
Incident policy: the first responder declares a major incident and acts as
incident commander until they hand over by name. The commander assigns
operations and communications leads and keeps the incident log.
```

**Counterpoint.** "A role hierarchy is overhead for a small team or a small incident." Scope it to major incidents, and let one person hold several roles on a small team. The rule only asks that someone is named commander, so the question "who decides" has an answer before the page goes out.
