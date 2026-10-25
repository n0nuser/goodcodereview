---
id: sys-index-concurrently
level: system
tags: [compatibility, database, migration, postgres]
severity: block
status: draft
lacks: orgs, PostgreSQL and GitLab back it; needs a third org
lang: core
applies_when: A migration creates an index on an existing large or busy table.
tool_gate: Migration linter.
borrowed_from:
  - https://www.postgresql.org/docs/current/sql-createindex.html
  - https://docs.gitlab.com/development/migration_style_guide/
---

**Rule.** Create indexes with `CONCURRENTLY`, outside a transaction block, and handle a failed build that leaves an INVALID index.

**Why.** A plain build blocks writes for its whole duration. A concurrent build fails inside a transaction. A concurrent build that fails leaves an invalid index that queries ignore but writes still pay for.

**FAIL**

```sql
CREATE INDEX idx_orders_user ON orders (user_id);
```

**PASS**

```sql
-- migration with the DDL transaction disabled
DROP INDEX CONCURRENTLY IF EXISTS idx_orders_user;
CREATE INDEX CONCURRENTLY idx_orders_user ON orders (user_id);
```

**Counterpoint.** "CONCURRENTLY is slower." It does two scans, waits for older transactions, and runs only one concurrent build per table at a time. That is the price of not blocking writes. For a unique index, others can see violations before a failed build is cleaned up.
