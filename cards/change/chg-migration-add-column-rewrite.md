---
id: chg-migration-add-column-rewrite
level: change
tags: [database, migrations, postgres]
severity: block
status: draft
lang: core
applies_when: A migration adds a column to a large PostgreSQL table.
tool_gate: Migration linter that flags volatile defaults, stored generated columns and identity columns on ADD COLUMN.
borrowed_from:
  - https://www.postgresql.org/docs/current/sql-altertable.html
---

**Rule.** Add the column nullable or with a constant default; fill volatile, computed or identity values in batches afterwards.

**Why.** A constant or NULL default is a metadata change. A volatile default, a stored generated column or an identity column rewrites the whole table, and the default lock (ACCESS EXCLUSIVE) blocks every query on it for the duration.

**FAIL**

```sql
ALTER TABLE events ADD COLUMN token uuid DEFAULT gen_random_uuid();   -- volatile: rewrites 400M rows
```

**PASS**

```sql
ALTER TABLE events ADD COLUMN token uuid;                 -- no rewrite
-- backfill in batches, then SET DEFAULT for new rows only
```

**Counterpoint.** "The table is small." Then the rewrite is cheap and the one-step form is fine; state the row count in the description. Locking and timeouts are in [[sys-migration-lock-timeout]].
