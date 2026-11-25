# incident

## inc-perf-fix-has-profile-evidence

severity: should-fix  
concerns: performance, testing  
applies_when: An incident or a slowdown is closed by a code or config change meant to make it faster.  
Backed by: Google (unjudged), GitLab (unjudged), Microsoft (unjudged). Backing: unjudged. People cited: Brendan Gregg (unjudged).

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

## inc-postmortem-blameless

severity: should-fix  
concerns: process  
applies_when: A postmortem, incident review or postmortem template is written or audited.  
Backed by: Google (unjudged), PagerDuty (unjudged), Atlassian (unjudged), Microsoft (unjudged). Backing: unjudged.

**Rule.** Write a postmortem so that it names causes in the system and the decisions around it, never a person or team as the one at fault.

**Why.** People who expect blame stay quiet about what they saw and soften the timeline, so the contributing factors never reach the review. A cause of "someone was careless" also gives no action that prevents the next failure, while a cause such as "the schema accepted an empty list" does. The timeline may still say who made which change; only the verdict of fault is out.

**FAIL**

```text
Root cause: Dana pushed a bad config without testing it.
Action: Dana to be more careful with config changes.
```

**PASS**

```text
Contributing causes: the config schema accepted an empty region list, and the
deploy pipeline had no validation step for region lists.
14:02 Dana's change (PR 4412) merged with an empty list after the usual review.
Action (owner: platform, due 2026-12-10, ISSUE-518): reject empty lists in the
schema and add a validation step to the pipeline.
```

**Counterpoint.** "Blameless means nobody is accountable." Each change stays in the timeline with its author, and each action has an owner. What the rule refuses is the finding that a person caused the outage, because that finding ends the inquiry at the person and leaves the system as it was. It says nothing about performance management, which is a separate process.

## inc-rollback-path-tested

severity: should-fix  
concerns: reliability  
applies_when: A runbook or incident response relies on rollback, failover, or a manual mitigation.  
Backed by: Google (unjudged), AWS (unjudged), Dropbox (unjudged), Slack (unjudged), Cloudflare (unjudged), Shopify (unjudged). Backing: unjudged.

**Rule.** Exercise each mitigation that a runbook names (rollback, failover, flag off) on a regular schedule.

**Why.** Rollbacks fail on schema changes or removed artifacts, backups stop running without anyone noticing, and untested failover paths rot. After a drill finds a gap and you fix it, run the drill again to confirm the fix. People who rarely use a rollback tool hesitate to use it in an incident. The runbook should also say who may trigger each mitigation, so nobody waits for permission during the outage.

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

## inc-single-incident-commander

severity: discuss  
concerns: process, reliability  
applies_when: The repo or wiki holds an incident policy or runbook that covers major incidents. A repo with no such document has nothing to fail, so mark the card N/A.  
Backed by: Google (unjudged), PagerDuty (unjudged), AWS (unjudged). Backing: unjudged.

**Rule.** Name one incident commander for each major incident, who holds the overall state of the response and oversees the other roles.

**Why.** Without one person holding the whole picture, responders duplicate each other, change the system in parallel and wait for someone else to decide. The commander does not need to be the most senior or the most technical person present; the role is to keep the state and assign the work.

**FAIL**

```text
Incident policy: when a major incident starts, the on-call engineers and the
manager join the channel and work it out together.
```

**PASS**

```text
Incident policy: the first responder declares a major incident and acts as
incident commander until they hand over by name. The commander assigns
operations and communications leads and keeps the incident log.
```

**Counterpoint.** "A role hierarchy is overhead for a small team or a small incident." Scope it to major incidents, and let one person hold several roles on a small team. The rule only asks that someone is named commander, so the question "who decides" has an answer before the page goes out.
