---
id: inc-postmortem-owned-actions
level: incident
tags: [reliability, process, incident, learning]
severity: should-fix
status: draft
lacks: orgs, an owner and due date on each action has no org; Dropbox and Shopify mention action items without naming either
note: no source yet; first-hand reasoning
lang: core
applies_when: A postmortem or incident review is written or audited.
tool_gate: Template that requires owner and due date per action.
borrowed_from: []
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
