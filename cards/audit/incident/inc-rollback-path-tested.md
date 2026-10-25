---
id: inc-rollback-path-tested
level: incident
tags: [reliability, incident, rollback]
severity: should-fix
status: stable
lang: core
applies_when: A runbook or incident response relies on rollback, failover, or a manual mitigation.
tool_gate: none
note: exercising runbook mitigations is backed by Dropbox (monthly failovers), Slack (a restore runbook failed until drilled; use rollback tooling often), Cloudflare (regular cut tests; a kill switch SOP failed on a rule type it had never met) and Shopify (repeated Game Days); naming who may trigger the mitigation has no source and sits in Why
borrowed_from:
  - https://sre.google/workbook/canarying-releases/
  - https://aws.amazon.com/builders-library/implementing-health-checks/
  - https://dropbox.tech/infrastructure/disaster-readiness-test-failover-blackhole-sjc
  - https://slack.engineering/break-stuff-on-purpose/
  - https://slack.engineering/deploy-safety/
  - https://blog.cloudflare.com/5-december-2025-outage/
  - https://blog.cloudflare.com/cloudflare-incident-on-november-14-2024-resulting-in-lost-logs/
  - https://shopify.engineering/four-steps-creating-effective-game-day-tests
---

**Rule.** Exercise each mitigation that a runbook names (rollback, failover, flag off) on a regular schedule.

**Why.** Rollbacks fail on schema changes or removed artifacts, backups stop running without anyone noticing, and untested failover paths rot. People who rarely use a rollback tool hesitate to use it in an incident. The runbook should also say who may trigger each mitigation, so nobody waits for permission during the outage.

**FAIL**

```text
Runbook: "roll back to previous version" (last attempted: never; migration not reversible)
```

**PASS**

```text
Runbook: rollback drilled monthly, last run 2026-10-01; schema is expand-only; on-call may trigger.
```

**See also.** [[prod-canary-staged-rollout]] for abort rules, and [[prod-kill-switch-fallback]] for fallbacks that run in code.

**Counterpoint.** "Drills are costly." Start with the mitigations an incident would need first, and drill again when a migration or release process changes. A drill is cheaper than finding out during an outage that the rollback is impossible.
