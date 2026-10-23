---
id: inc-postmortem-owned-actions
level: incident
tags: [incident, learning]
severity: should-fix
status: draft
lang: core
applies_when: A postmortem or incident review is written or audited.
tool_gate: Template that requires owner and due date per action.
borrowed_from: []
---

**Rule.** Every postmortem action has one named owner, a due date and a tracker link, and addresses a cause, not just detection.

**Why.** Actions without owners are wishes; a list that only adds alerts leaves the failure mechanism in place.

**FAIL**

```text
Actions: improve monitoring; be more careful with deploys.
```

**PASS**

```text
A1 (owner: db-team, due 2026-11-15, ISSUE-412): add lock_timeout to migration template
```

**Counterpoint.** "Blameless means no names." Blameless is about cause, not ownership; an owner is a task assignee, not a culprit. No source in docs/research covers postmortems, so this is first-hand and draft.
