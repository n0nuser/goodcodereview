---
id: inc-postmortem-owned-actions
level: incident
tags: [reliability, process, incident, learning]
severity: should-fix
status: draft
lacks: orgs, Atlassian is the only firm backer; the Google SRE workbook shows an owner column in an example table only; needs two more orgs
note: Atlassian asks who will take each action and by when, and says every postmortem action must be tracked in Jira. The Google workbook sample has owner and tracking-bug columns but states no rule, so it is soft
lang: core
applies_when: A postmortem or incident review is written or audited.
tool_gate: Template that requires owner and due date per action.
borrowed_from:
  - https://www.atlassian.com/incident-management/handbook/postmortems
  - https://sre.google/workbook/postmortem-culture/
---

**Rule.** Give every postmortem action one named owner, a due date, and a tracker link.

**Why.** Actions without owners are wishes. A list that only adds alerts leaves the failure mechanism in place, so actions should also address a cause, not just detection.

**FAIL**

```text
Actions: improve monitoring; be more careful with deploys.
```

**PASS**

```text
A1 (owner: db-team, due 2026-11-15, ISSUE-412): add lock_timeout to migration template
```

**Counterpoint.** "Blameless means no names." Blameless is about cause, not ownership. An owner is a task assignee, not a culprit.
