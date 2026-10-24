---
id: fn-atomic-related-updates
level: function
tags: [consistency, errors]
severity: block
status: draft
lang: core
applies_when: One operation writes to two or more places that must agree (rows, tables, stores, files).
tool_gate: none
note: from one vendor's review skill (opinion); the all-or-nothing principle is standard
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/thermos/skills/thermo-nuclear-code-quality-review/SKILL.md
---

**Rule.** Make related writes succeed or fail together: one transaction, or an ordered sequence with a defined undo.

**Why.** If step two fails after step one, the system holds a half-applied change that no later code expects, such as an order without its items.

**FAIL**

```text
db.insert(order)
db.insert_many(items)          # raises: the order exists with no items
```

**PASS**

```text
with db.transaction():
    db.insert(order)
    db.insert_many(items)
```

**Counterpoint.** "The writes go to different systems; no transaction spans them." Then order the steps so a partial failure is harmless and retryable, or use an outbox or saga ([[svc-saga-steps]]). Do not leave it to chance. [[fn-no-check-then-act-across-await]] covers check-then-write races.
