---
id: sys-constraint-not-valid
level: system
tags: [compatibility, database, migration, postgres]
severity: block
status: draft
lacks: orgs, PostgreSQL docs are the only backer; needs two more orgs that add constraints in two steps
note: ADD CONSTRAINT ... USING INDEX route not independently verified; PostgreSQL is the example dialect
lang: core
applies_when: A migration adds a CHECK, FOREIGN KEY, or NOT NULL constraint to a large existing table.
tool_gate: Migration linter.
borrowed_from:
  - https://www.postgresql.org/docs/current/sql-altertable.html
---

**Rule.** Add the constraint `NOT VALID`, then run `VALIDATE CONSTRAINT` in a separate step, and never leave the VALIDATE out.

**Why.** The plain form scans the whole table while holding a strong lock. NOT VALID enforces new writes immediately and skips the scan. VALIDATE checks old rows with a lock that does not block writes. Skipping VALIDATE leaves old rows unverified.

**FAIL**

```sql
ALTER TABLE orders ADD CONSTRAINT amt_pos CHECK (amount > 0);
```

**PASS**

```sql
ALTER TABLE orders ADD CONSTRAINT amt_pos CHECK (amount > 0) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT amt_pos;   -- next migration
```

**Counterpoint.** "NOT VALID is lock-free." Not quite: the ADD still takes its lock briefly, so pair it with `lock_timeout`. Unique and primary keys do not accept NOT VALID. They need a concurrently built unique index first.
