---
id: chg-expand-contract
level: change
tags: [compatibility, migration]
severity: block
status: stable
lang: core
applies_when: The change renames, removes or reshapes a column, API field, message, config key or exported symbol that other code reads.
tool_gate: Schema or API diff tools (breaking-change detectors) in CI.
note: 3 orgs (GitLab, Stripe, Kubernetes). Kubernetes states the add-both-versions-then-remove rule for API versions, not expand-contract by name. Config keys and exported symbols have no source
borrowed_from:
  - https://www.hyrumslaw.com/
  - https://devguide.python.org/getting-started/pull-request-lifecycle/
  - https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/
  - https://stripe.com/blog/online-migrations
  - https://kubernetes.io/docs/reference/using-api/deprecation-policy/
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

**Counterpoint.** Three steps are slow for internal code. Exception: when producer and consumers deploy atomically from one repo, or the table is small enough to alter in one safe step, a one-step change is fine. Say so in the description. [[sys-migration-expand-contract]] covers batching the backfill.
