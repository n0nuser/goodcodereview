---
id: sys-migration-expand-contract
level: system
tags: [database, migrations, deploys]
severity: block
status: draft
lang: core
applies_when: A change drops, renames or retypes a column, or mixes schema change with a data backfill.
tool_gate: Migration linter for DROP/RENAME COLUMN.
borrowed_from:
  - https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/
  - https://docs.gitlab.com/development/migration_style_guide/
---

**Rule.** Ship destructive schema changes over several releases (stop using, then drop), and run data backfills in batches, separate from the schema change.

**Why.** During a rolling deploy old code still runs against the new schema. A dropped or renamed column breaks it, and a large backfill in one transaction holds locks for its whole run.

**FAIL**

```text
release N: RENAME COLUMN a TO b ; UPDATE big_table SET b = ... (one tx)
```

**PASS**

```text
N: add b, dual-write, ignore a in code ; N+1: batched backfill ; N+2: drop a
```

**Counterpoint.** "Three releases for a rename is heavy." It is, and for tables small enough that a lock is harmless a single step is fine; GitLab's procedure targets zero-downtime on large tables, and the card applies only there.
