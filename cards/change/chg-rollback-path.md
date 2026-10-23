---
id: chg-rollback-path
level: change
tags: [release, rollback]
severity: block
status: draft
lang: core
applies_when: The change deploys schema, data, config or behaviour that is costly to undo.
tool_gate: Migration linter requiring a down step; deploy pipeline with automatic abort.
note: thin sourcing: canarying with auto rollback only; migration rollback practice unsourced
borrowed_from:
  - https://sre.google/workbook/canarying-releases/
  - https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to
---

**Rule.** State in the description how to undo the change.

**Why.** When a release goes wrong, the time to find the way back is before shipping. Irreversible steps (dropped data, sent messages) need an explicit decision. The author has checked that route is possible. See [[inc-rollback-path-tested]] for drilling it and [[prod-canary-staged-rollout]] for abort rules.

**FAIL**

```text
Migration drops column legacy_id and deletes backing rows.
Description: no rollback section. Code and migration deploy together.
```

**PASS**

```text
Rollback: revert PR; column kept for one release, dropped in a later PR.
Behaviour behind a flag; canary at 5% with an abort rule.
```

**Counterpoint.** "We can always roll forward." Fine for stateless code, but not after data is destroyed or a client has cached the new contract. The check is cheap for reversible changes (one line) and only bites on irreversible ones.
