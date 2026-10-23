---
id: chg-expand-contract
level: change
tags: [compatibility, migration]
severity: block
status: draft
lang: core
applies_when: The change renames, removes or reshapes a column, API field, message, config key or exported symbol that other code reads.
tool_gate: Schema or API diff tools (breaking-change detectors) in CI.
note: expand/contract recipe itself unsourced; compatibility principle from CPython devguide and Hyrum's law
borrowed_from:
  - https://www.hyrumslaw.com/
  - https://devguide.python.org/getting-started/pull-request-lifecycle/
---

**Rule.** Evolve shared contracts in steps: add the new form beside the old (expand), migrate every consumer, then remove the old form (contract) in a later change.

**Why.** Producers and consumers deploy at different times. A one-step rename breaks whichever side is still on the old version.

**FAIL**

```sql
ALTER TABLE users RENAME COLUMN name TO full_name;  -- app v1 still reads name
```

**PASS**

```sql
-- change 1: add full_name, dual-write, backfill
-- change 2: readers switch to full_name
-- change 3 (later): drop name
```

**Counterpoint.** Three steps are slow for internal code. Exception, stated once: when producer and consumers deploy atomically from one repo, or the table is small enough to alter in one safe step, a one-step change is fine; say so in the description. Batching and release steps for databases are in [[sys-migration-expand-contract]].
