---
id: prod-kill-switch-fallback
level: production
tags: [resilience, flags]
severity: should-fix
status: draft
lang: core
applies_when: A new risky feature or a dependency fallback is added.
tool_gate: none
borrowed_from:
  - https://aws.amazon.com/builders-library/caching-challenges-and-strategies/
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md
---

**Rule.** A risky feature can be turned off without a deploy, and every fallback path is exercised in test or in production on a schedule.

**Why.** An untested fallback fails exactly when needed (AWS suggests testing with the cache disabled; ASVS expects a degradation path when an external resource fails).

**FAIL**

```text
if redis_down: use_backup()   # never run since written
new_checkout() # no flag, rollback needs a deploy
```

**PASS**

```text
flag.checkout_v2 (default off, runtime toggle) ; chaos test disables redis weekly
```

**Counterpoint.** "Flags add branches." True; delete them after rollout. The kill-switch part itself has no direct source in the notes, only the fallback part does.
