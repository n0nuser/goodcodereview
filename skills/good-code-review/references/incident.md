# incident

## inc-perf-fix-has-profile-evidence

severity: should-fix  
concerns: performance, testing  
applies_when: An incident or a slowdown is closed by a code or config change meant to make it faster.

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
