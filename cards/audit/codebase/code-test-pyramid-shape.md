---
id: code-test-pyramid-shape
level: codebase
tags: [testing, process, ci]
severity: discuss
status: stable
lang: core
applies_when: Auditing a repo whose layout or CI report separates unit, integration and end-to-end tests, so a reviewer can count tests per tier. Without that split there is no count to fail, so mark the card N/A.
tool_gate: A CI report that prints the number of tests per tier next to the run time.
note: Google gives a very rough 80/15/5 mix, GitLab says most tests should be unit tests, Microsoft (Azure Well-Architected) says use the pyramid as a guide; none sets a hard ratio
borrowed_from:
  - https://abseil.io/resources/swe-book/html/ch11.html
  - https://docs.gitlab.com/development/testing_guide/testing_levels/
  - https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/testing
---

**Rule.** Keep most tests at the unit level, fewer at the integration level and fewest end-to-end.

**Why.** End-to-end tests are the slowest to run and the costliest to keep working, and a failure in one points at the whole system, not at a line. A suite that leans on them gives slow, flaky feedback. Unit tests run in milliseconds and locate the failure. The mix is a guide, not a quota.

**FAIL**

```text
CI report: unit 40, integration 120, end-to-end 310 (65% end-to-end).
Full run: 55 minutes.
```

**PASS**

```text
CI report: unit 1,450, integration 210, end-to-end 38 (about 85/12/2).
Full run: 11 minutes.
```

**Counterpoint.** "Our service is a thin layer over a database, and a UI-heavy app gets little from unit tests." Fair: such systems get more value from integration tests, and the right mix is not fixed. Raise a finding only when end-to-end tests clearly dominate and the run is slow, and raise it for discussion, not as a defect.
