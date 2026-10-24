---
id: prod-kill-switch-fallback
level: production
tags: [resilience, flags]
severity: should-fix
status: draft
note: kill-switch half has no source; fallback half rests on the AWS caching article
lang: core
applies_when: A new risky feature or a dependency fallback is added.
tool_gate: none
borrowed_from:
  - https://aws.amazon.com/builders-library/caching-challenges-and-strategies/
---

**Rule.** Make a risky feature switchable off without a deploy, and exercise every fallback path in test or in production on a schedule.

**Why.** An untested fallback fails exactly when you need it (AWS suggests testing with the cache disabled).

**FAIL**

```text
if redis_down: use_backup()   # never run since written
new_checkout() # no flag, rollback needs a deploy
```

**PASS**

```text
flag.checkout_v2 (default off, runtime toggle) ; chaos test disables redis weekly
```

**Counterpoint.** "Flags add branches." True. Delete them after rollout.
