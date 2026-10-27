---
id: inc-review-asks-which-check
level: incident
tags: [reliability, process, incident, learning]
severity: should-fix
status: draft
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs whose incident review asks which check or layer should have caught the fault
lang: core
applies_when: An incident review or postmortem is written or audited.
tool_gate: Postmortem template with a required "which check should have caught this" field.
note: Anthropic only (a vendor, in a post about its own Claude Code team); incident reviews "involve looking back to see what layer should have caught the problem"
borrowed_from:
  - https://x.com/addyosmani/status/2114604912520921136
---

**Rule.** Every incident review names the check that should have caught the fault (a test, CI gate, review, canary or alert) and says what it would take to catch the next one there.

**Why.** An incident that ends at "the author made a mistake" leaves the gaps in place. Asking which layer should have caught it turns one failure into a fix for the whole class.

**FAIL**

```text
Root cause: a null check was missed in the payment handler.
Action: remind the team to check for nulls.
```

**PASS**

```text
Root cause: a null check was missed in the payment handler.
Should have been caught by: unit tests (no case for a missing field) and the type checker (field typed as optional).
Action: add the missing-field test; turn on strict null checks for payments/.
```

**Counterpoint.** "Some faults no check could catch." Then the review says so and moves to detection and rollback: which alert or revert path would have limited the harm. The question still gets asked each time.
