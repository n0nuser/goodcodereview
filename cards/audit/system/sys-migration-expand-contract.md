---
id: sys-migration-expand-contract
level: system
tags: [database, migration, deploys]
severity: block
status: stable
lang: core
applies_when: A change drops, renames, or retypes a column, or mixes schema change with a data backfill.
tool_gate: Migration linter for DROP/RENAME COLUMN.
borrowed_from:
  - https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/
  - https://docs.gitlab.com/development/migration_style_guide/
  - https://stripe.com/blog/online-migrations
  - https://github.com/ankane/strong_migrations
---

**Rule.** Run data backfills in batches, in a migration separate from the schema change.

**Why.** A large backfill in one transaction holds locks for its whole run, and a failure halfway rolls all of it back. Batches with a pause between them keep each lock short and let the backfill resume. [[chg-expand-contract]] covers the order of releases around it.

**FAIL**

```text
release N: RENAME COLUMN a TO b ; UPDATE big_table SET b = ... (one tx)
```

**PASS**

```text
N: add b, dual-write, ignore a in code ; N+1: batched backfill ; N+2: drop a
```

**Counterpoint.** "One `UPDATE` is simpler than a batched job." On a small table it is, and this card does not apply there. Once the update holds a lock long enough to block live traffic, batch it.
