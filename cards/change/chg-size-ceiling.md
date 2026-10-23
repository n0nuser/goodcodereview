---
id: chg-size-ceiling
level: change
tags: [size, review-quality]
severity: discuss
status: draft
lang: core
applies_when: The diff exceeds roughly 400 changed lines or about 20 files and is not generated or a pure move.
tool_gate: Size labels or a diff-size warning in CI.
borrowed_from:
  - https://sback.it/publications/icse2018seip.pdf
  - https://www.microsoft.com/en-us/research/publication/characteristics-of-useful-code-reviews-an-empirical-study-at-microsoft/
  - https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/
  - https://newsletter.pragmaticengineer.com/p/stacked-diffs
---

**Rule.** Treat about 200 lines as the target and about 400 as the ceiling; above that, the author splits or explains in the description why not.

**Why.** Review usefulness falls as changes grow, so big diffs get skimmed and approved on trust.

**FAIL**

```text
1,800-line PR, 55 files, one approval after 10 minutes, no split plan.
```

**PASS**

```text
Stack of 6 changes of 150-300 lines, each builds and passes tests alone.
```

**Counterpoint.** The numbers are weakly sourced. The direction (smaller is better) holds across Google logs (median change 24 lines), Microsoft comment data (usefulness drops from about 20 files) and others. The 200-400 figure traces to a single vendor study (SmartBear's write-up of a Cisco study; the original report was not read), so call it a heuristic. Comment count rising with size is not defect yield.
