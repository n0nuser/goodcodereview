# incident

## inc-perf-fix-has-profile-evidence

severity: should-fix  
concerns: performance, testing  
applies_when: An incident or a slowdown is closed by a code or config change meant to make it faster.  
Backed by: Google, GitLab, Microsoft. People cited: Brendan Gregg.

**Rule.** Tie the performance fix to evidence that names the bottleneck: a profile, a trace, or a USE check.

**Why.** A guessed fix often speeds up code that was not slow, and the incident comes back. The profile that found the bottleneck is also the cheapest proof that the fix removed it, so take the same measurement again after the fix, under the same load ([chg-perf-claim-evidence](change.md#chg-perf-claim-evidence)).

**FAIL**

```text
postmortem: "latency spike; increased pod memory and added a cache"
no profile, no trace, nothing that names where the time went
```

**PASS**

```text
CPU profile: 61% in json.Marshal on /export (flame graph linked)
fix: stream the response; after: p99 1.9 s -> 240 ms, same load replay
```

**Counterpoint.** "In an outage we mitigate first." Yes. Rolling back or adding capacity to stop the bleeding needs no profile. The rule covers the fix that closes the incident, which comes after the system is stable. Capacity kept as that fix, with no profile behind it, hides a code problem rather than removing it.

## inc-rollback-path-tested

severity: should-fix  
concerns: reliability  
applies_when: A runbook or incident response relies on rollback, failover, or a manual mitigation.  
Backed by: Google, AWS, Dropbox, Slack, Cloudflare, Shopify.

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

**See also.** [prod-canary-staged-rollout](production.md#prod-canary-staged-rollout) for abort rules, and [prod-kill-switch-fallback](production.md#prod-kill-switch-fallback) for fallbacks that run in code.

**Counterpoint.** "Drills are costly." Start with the mitigations an incident would need first, and drill again when a migration or release process changes. A drill is cheaper than finding out during an outage that the rollback is impossible.
