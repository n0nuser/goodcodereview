---
id: chg-expand-contract
level: change
tags: [compatibility, migration]
severity: block
status: draft
lang: core
applies_when: The change renames, removes or reshapes a column, API field, message, config key or exported symbol that other code reads.
tool_gate: Schema or API diff tools (breaking-change detectors) in CI.
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

**Counterpoint.** Three steps are slow for internal, single-deploy code. Answer: when producer and consumers ship atomically from one repo and no old data lives on, a one-step change is fine; say so in the description. Sources give only the compatibility principle (optional params with defaults are safe, observable behaviour gets depended on); the expand/contract recipe itself has no source in the notes, so this card stays draft.
