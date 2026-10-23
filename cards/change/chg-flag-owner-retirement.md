---
id: chg-flag-owner-retirement
level: change
tags: [feature-flags, release]
severity: should-fix
status: draft
lang: core
applies_when: The change adds a feature flag, kill switch or config toggle.
tool_gate: Flag registry linter that requires owner and expiry fields.
borrowed_from:
  - https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to
---

**Rule.** A new flag names an owner, a default, and a removal condition or date; the removal is ticketed.

**Why.** Flags without owners become permanent forks of behaviour that nobody dares delete and that multiply test paths.

**FAIL**

```python
if flags.get("new_checkout"):   # who owns it? when does it go?
    ...
```

**PASS**

```python
# flag: new_checkout  owner: payments  default: off
# remove when 100% for 2 weeks  ticket: PAY-88
if flags.get("new_checkout"): ...
```

**Counterpoint.** Some flags are permanent (kill switches, entitlements). Answer: label them as such with an owner; the check is that the intent is explicit. The source here is one practitioner essay (flag to switch a long-lived branch off); retirement discipline is our extension.
