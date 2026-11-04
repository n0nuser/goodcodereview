---
id: chg-migration-add-column-rewrite
level: change
tags: [compatibility, database, migration, postgres]
severity: should-fix
status: stable
lang: core
applies_when: A migration adds a column to a large PostgreSQL table.
context: [data]
tool_gate: Migration linter that flags volatile defaults, stored generated columns and identity columns on ADD COLUMN.
borrowed_from:
  - https://www.postgresql.org/docs/current/sql-altertable.html
  - https://medium.com/paypal-tech/postgresql-at-scale-database-schema-changes-without-downtime-20d3749ed680
  - https://retool.com/blog/running-safe-database-migrations-using-postgres
---

**Rule.** Add the column nullable or with a constant default, then fill volatile, computed, or identity values in batches.

**Why.** A constant or NULL default is a metadata change. A volatile default, a stored generated column, or an identity column rewrites the whole table, and the default lock (ACCESS EXCLUSIVE) blocks every query on it for the duration.

**FAIL**

```sql
ALTER TABLE events ADD COLUMN token uuid DEFAULT gen_random_uuid();   -- volatile: rewrites 400M rows
```

**PASS**

```sql
ALTER TABLE events ADD COLUMN token uuid;                 -- no rewrite
-- backfill in batches, then SET DEFAULT for new rows only
```

**Counterpoint.** "The table is small." Then the rewrite is cheap and the one-step form is fine. State the row count in the description. [[sys-migration-lock-timeout]] covers locking and timeouts.
