---
id: sys-migration-expand-contract
level: system
tags: [database, migration, deploys]
severity: block
status: draft
lang: core
applies_when: A change drops, renames or retypes a column, or mixes schema change with a data backfill.
tool_gate: Migration linter for DROP/RENAME COLUMN.
borrowed_from:
  - https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/
  - https://docs.gitlab.com/development/migration_style_guide/
---

**Rule.** Run data backfills in batches, in a migration separate from the schema change.

**Why.** A large backfill in one transaction holds locks for its whole run. The principle of staging destructive changes across releases is [[chg-expand-contract]]; this card is the large-table procedure: stop using the column, drop it in a later release, and keep it ignored in code until the release after.

**FAIL**

```text
release N: RENAME COLUMN a TO b ; UPDATE big_table SET b = ... (one tx)
```

**PASS**

```text
N: add b, dual-write, ignore a in code ; N+1: batched backfill ; N+2: drop a
```

**Counterpoint.** "Three releases for a rename is heavy." It is, which is why the one-step exception lives in [[chg-expand-contract]] and applies here unchanged; this card covers only the batching and release steps for large tables.
