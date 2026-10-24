---
id: inc-perf-fix-has-profile-evidence
level: incident
tags: [performance, testing, verification]
severity: should-fix
status: draft
lang: core
applies_when: An incident or a slowdown is closed by a code or config change meant to make it faster.
tool_gate: none
note: 2 orgs (Google, Brendan Gregg) back evidence before the fix; Cloudflare's report is after-the-fact, so this card cannot be promoted yet
borrowed_from:
  - https://go.dev/blog/pprof
  - https://sre.google/sre-book/effective-troubleshooting/
  - https://www.brendangregg.com/usemethod.html
  - https://www.brendangregg.com/flamegraphs.html
---

**Rule.** Tie the performance fix to evidence that names the bottleneck (a profile, a trace, or a USE check), and show the same measurement after the fix.

**Why.** A guessed fix often speeds up code that was not slow, and the incident comes back. The profile that found the bottleneck is also the cheapest proof that the fix removed it.

**FAIL**

```text
postmortem: "latency spike; increased pod memory and added a cache"
no profile, no trace, no before-and-after numbers
```

**PASS**

```text
CPU profile: 61% in json.Marshal on /export (flame graph linked)
fix: stream the response; after: p99 1.9 s -> 240 ms, same load replay
```

**Counterpoint.** "In an outage we mitigate first." Yes. Rolling back or adding capacity needs no profile, and the SRE book says so. The rule covers the fix that closes the incident, which comes after the system is stable. See [[chg-perf-claim-evidence]] for the same rule on a change.
