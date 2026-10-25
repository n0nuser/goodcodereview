---
id: chg-delete-legacy-after-migration
level: change
tags: [compatibility, maintainability, migration, cleanup]
severity: should-fix
status: draft
lang: core
applies_when: The change adds a new API, path or config and every caller lives in this repo.
tool_gate: Dead-code and unused-export checks.
note: cursor/plugins and Stripe (one-PR Flow to TypeScript move) back the Rule; Uber's JUnit move ran old and new side by side, so it does not; applies only without outside consumers
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/architect/references/design-red-flags.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/references/rubric.md
  - https://stripe.dev/blog/migrating-to-typescript
---

**Rule.** When no consumer sits outside the repo, move every caller to the new API and delete the old one, and the tests that pinned its internals, in the same change.

**Why.** Two supported ways to do one task both keep gaining callers. The old path becomes the one nobody dares remove.

**FAIL**

```text
+ def fetch_user_v2(id): ...
  def fetch_user(id): ...        # kept "for now"; 14 callers still use it
```

**PASS**

```text
- def fetch_user(id): ...
+ def fetch_user(id): ...        # new behaviour; all 14 callers updated in this diff
```

**Counterpoint.** This rule applies only when no consumer sits outside the repo: a published library, a public API, a client on an older release, or data written by older code. For those, follow [[chg-expand-contract]] and remove the old form later. Check the consumer claim before you mark `FAIL`.
