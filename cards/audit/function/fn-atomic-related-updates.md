---
id: fn-atomic-related-updates
level: function
tags: [correctness, consistency, errors]
severity: should-fix
status: draft
lacks: orgs, PostgreSQL, Django and Rails describe what a transaction is, not a rule to wrap related writes; needs orgs that tell reviewers to do so
lang: core
applies_when: One operation writes to two or more places that must agree (rows, tables, stores, files).
tool_gate: none
note: PostgreSQL, Django and Rails document the all-or-nothing mechanism (soft); the review rule itself comes from one vendor's review skill
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/thermos/skills/thermo-nuclear-code-quality-review/SKILL.md
  - https://www.postgresql.org/docs/current/tutorial-transactions.html
  - https://docs.djangoproject.com/en/5.1/topics/db/transactions/
  - https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html
---

**Rule.** Make related writes succeed or fail together.

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

**Counterpoint.** "The writes go to different systems; no transaction spans them." Then use one transaction per system and order the steps so a partial failure is harmless and retryable, or use an outbox or saga ([[svc-saga-steps]]). Do not leave it to chance. [[fn-no-check-then-act-across-await]] covers check-then-write races.
