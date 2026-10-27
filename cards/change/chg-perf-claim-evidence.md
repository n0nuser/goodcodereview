---
id: chg-perf-claim-evidence
level: change
tags: [performance, testing, verification]
severity: should-fix
status: stable
lang: core
applies_when: The change or its description claims a speed, throughput, memory or cost improvement.
tool_gate: none
note: the kernel, Phabricator and GitLab (measure again after deploy, report percentiles) back the Rule (numbers for an optimisation claim); the run count, spread and limiter in the Why come from benchmark-checklist/SKILL.md
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-explain-the-number/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/benchmark-checklist/SKILL.md
  - https://github.com/cursor/plugins/blob/main/cursor-team-kit/skills/verify-this/SKILL.md
  - https://docs.kernel.org/process/submitting-patches.html
  - https://docs.gitlab.com/development/performance/
  - https://secure.phabricator.com/book/phabflavor/article/writing_reviewable_code/
---

**Rule.** Back a performance claim with measured before-and-after numbers.

**Why.** A single fast run can measure noise, a cached result, an error path that returns early, or a step that is a tenth of the total. A piece that is 10% of the run caps the gain near 11% however well it is tuned. So a useful number comes with the run count, the spread, the resource that limits further gain, and a check that errors were counted and the work ran inside the timed region.

**FAIL**

```text
"Parse is much faster now." (no numbers; 4% of requests now return 500 early)
```

**PASS**

```text
Median of 7 alternating runs: 412 ms -> 301 ms, range 398-421 vs 295-310.
0 errors in both. Parse is 35% of the request, so the cap is 1.5x; limiter: DB round trip.
```

**Counterpoint.** "A micro-optimisation needs no benchmark ceremony." A claim in prose does. If the description makes no performance claim, mark `N/A`.
