---
id: chg-size-ceiling
level: change
tags: [process, size, review-quality]
severity: discuss
status: stable
lang: core
applies_when: The diff exceeds roughly 400 changed lines or about 20 files and is not generated or a pure move.
tool_gate: Size labels or a diff-size warning in CI.
note: 200-400 LOC figure traces to one vendor study (SmartBear write-up of a Cisco study); original report not read
borrowed_from:
  - https://sback.it/publications/icse2018seip.pdf
  - https://www.microsoft.com/en-us/research/publication/characteristics-of-useful-code-reviews-an-empirical-study-at-microsoft/
  - https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/
  - https://newsletter.pragmaticengineer.com/p/stacked-diffs
---

**Rule.** Split a change past about 400 changed lines or about 20 files, or say in the description why not; aim for about 200.

**Why.** Review usefulness falls as changes grow, so big diffs get skimmed and approved on trust.

**FAIL**

```text
1,800-line PR, 55 files, one approval after 10 minutes, no split plan.
```

**PASS**

```text
Stack of 6 changes of 150-300 lines, each builds and passes tests alone.
```

**Counterpoint.** "Line counts are arbitrary." The exact numbers are rough, but the direction is not: larger changes get fewer useful comments per file and are approved on trust. Treat 400 as a prompt to split or explain, not a hard gate, and exclude generated code and pure moves.
