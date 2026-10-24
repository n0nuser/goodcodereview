---
id: chg-perf-claim-evidence
level: change
tags: [performance, verification]
severity: should-fix
status: draft
lang: core
applies_when: The change or its description claims a speed, throughput, memory or cost improvement.
tool_gate: none
note: one vendor's engineering guidance (opinion), from benchmark-checklist/SKILL.md; the seven questions are condensed
borrowed_from:
  - https://github.com/cursor/plugins
---

**Rule.** Back a performance claim with the run count, the spread, the resource that limits further gain, and proof that errors were counted and the work ran inside the timed region.

**Why.** A single fast run can measure noise, a cached result, an error path that returns early, or a step that is a tenth of the total. A piece that is 10% of the run caps the gain near 11% however well it is tuned.

**FAIL**

```text
"Parse is 3x faster." (one run, no spread; 4% of requests now return 500 early)
```

**PASS**

```text
Median of 7 alternating runs: 412 ms -> 301 ms, range 398-421 vs 295-310.
0 errors in both. Parse is 35% of the request, so the cap is 1.5x; limiter: DB round trip.
```

**Counterpoint.** "A micro-optimisation needs no benchmark ceremony." A claim in prose does. If the description makes no performance claim, mark `N/A`.
