---
id: prod-kill-switch-fallback
level: production
tags: [reliability, resilience, flags]
severity: should-fix
status: stable
note: switch off without a deploy - Cloudflare (kill switches through global config), GitHub (Flipper rollout and rollback), Slack (feature flags with instant rollback), Dropbox (rollback for experiments and gates); exercise the fallback - AWS (tests with the cache disabled), Cloudflare (regular cut tests; an untested fail-open path), Shopify (repeated Game Days in production), Dropbox (monthly datacenter failovers); on a schedule - Cloudflare, Shopify, Dropbox; Cloudflare's overload tests are a stated plan
lang: core
applies_when: A new risky feature or a dependency fallback is added.
tool_gate: none
borrowed_from:
  - https://aws.amazon.com/builders-library/caching-challenges-and-strategies/
  - https://blog.cloudflare.com/18-november-2025-outage/
  - https://blog.cloudflare.com/5-december-2025-outage/
  - https://blog.cloudflare.com/cloudflare-incident-on-november-14-2024-resulting-in-lost-logs/
  - https://github.blog/engineering/engineering-principles/how-we-improved-availability-through-iterative-simplification
  - https://slack.engineering/slack-ai-the-path-to-multi-cloud/
  - https://dropbox.tech/infrastructure/lessons-learned-in-incident-management
  - https://dropbox.tech/infrastructure/disaster-readiness-test-failover-blackhole-sjc
  - https://shopify.engineering/four-steps-creating-effective-game-day-tests
---

**Rule.** Make a risky feature switchable off without a deploy, and exercise every fallback path in test or in production on a schedule.

**Why.** A deploy is the slowest way to stop a feature that is hurting users. An untested fallback fails exactly when you need it: a fail-open path that never ran under load can overload the systems behind it, and a kill switch applied to a case it never met can raise its own error. Run the service with the dependency turned off, such as the cache disabled, and check that the safeguards hold.

**FAIL**

```python
if redis_down:
    return backup_lookup(key)   # never run since it was written
new_checkout(cart)              # no flag; turning it off needs a deploy
```

**PASS**

```python
if flags.enabled("checkout_v2"):   # runtime toggle, default off
    new_checkout(cart)
# chaos job, weekly: block Redis for 10 minutes and assert backup_lookup serves
```

**Counterpoint.** "Flags add branches." True for release flags, so delete each one after the rollout. A kill switch is meant to stay: keep it, give it an owner, and exercise it with the fallbacks, so it still works the day you need it. For runbook steps that a person runs, such as a rollback or a failover, see [[inc-rollback-path-tested]].
