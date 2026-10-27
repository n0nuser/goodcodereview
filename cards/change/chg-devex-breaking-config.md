---
id: chg-devex-breaking-config
level: change
tags: [compatibility, process, config]
severity: should-fix
status: draft
lacks: orgs, one vendor's review skill (cursor/plugins) backs it; needs two more orgs
lang: core
applies_when: The change renames an environment variable, remaps a port, moves a secret source, or adds a step needed to run or build the project.
tool_gate: Startup check that fails fast on missing or unknown config keys.
note: from one vendor's review skill (opinion); the rule is the narrow, checkable part
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/thermos/skills/thermo-nuclear-review/SKILL.md
---

**Rule.** Flag a change that renames or removes an environment variable, moves a secret, or remaps a port as breaking for developers and operators, and update every place that documents or sets it.

**Why.** A renamed variable or moved secret fails on the next machine that pulls, often with a vague error far from the cause. The diff looks harmless because nothing in the code breaks. A short migration note with the old name, the new name, and what to do saves each person from finding that out alone.

**FAIL**

```text
- DATABASE_URL=...
+ DB_DSN=...            # no note, no fallback, .env.example untouched
```

**PASS**

```text
+ DB_DSN=...            # reads DATABASE_URL with a deprecation warning for one release
+ PR text flags the break: "DATABASE_URL renamed to DB_DSN; update .env and CI secrets"
+ .env.example updated
```

**Counterpoint.** "It is an internal repo; people will ask." Each person who asks costs more than the note, and CI and deploy environments cannot ask. For published configuration, [[chg-breaking-change-taxonomy]] has the wider rules.
