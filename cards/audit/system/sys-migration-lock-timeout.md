---
id: sys-migration-lock-timeout
level: system
tags: [compatibility, database, migration, postgres]
severity: block
status: draft
note: lock-queue consequence is inference, not stated in the Postgres page read
lang: core
applies_when: A migration runs ALTER TABLE on a busy PostgreSQL table.
tool_gate: Migration linter (e.g. flag ALTER without lock_timeout).
borrowed_from:
  - https://www.postgresql.org/docs/current/runtime-config-client.html
  - https://www.postgresql.org/docs/current/sql-altertable.html
  - https://docs.gitlab.com/development/migration_style_guide/
---

**Rule.** Set `lock_timeout` for the migration session and retry on timeout.

**Why.** The default is 0, meaning wait forever, and most ALTER forms need the strongest lock. A migration stuck waiting can make later queries on that table wait behind it (inferred from how lock queues work).

**FAIL**

```sql
ALTER TABLE orders ADD COLUMN note text;   -- no lock_timeout
```

**PASS**

```sql
SET lock_timeout = '5s';
ALTER TABLE orders ADD COLUMN note text;   -- retry on timeout
```

**Counterpoint.** "Set it globally." The Postgres docs advise against setting it in postgresql.conf because it affects every session, so scope it to the migration. Also, with a non-zero `statement_timeout`, a larger `lock_timeout` has no effect.
