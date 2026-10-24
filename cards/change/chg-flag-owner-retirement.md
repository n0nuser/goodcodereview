---
id: chg-flag-owner-retirement
level: change
tags: [reliability, feature-flags, release]
severity: should-fix
status: draft
lang: core
applies_when: The change adds a feature flag, kill switch or config toggle.
tool_gate: Flag registry linter that requires owner and expiry fields.
note: one practitioner essay (switch off a long-lived branch); retirement discipline is an extension
borrowed_from:
  - https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to
---

**Rule.** Give every new flag an owner, a default, and a removal condition or date, and ticket the removal.

**Why.** A flag without an owner becomes a permanent fork of behaviour that nobody dares delete and that multiplies test paths.

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

**Counterpoint.** Some flags are permanent (kill switches, entitlements). Label them as permanent, with an owner. The check is that the intent is explicit.
