---
id: code-ci-gates
level: codebase
tags: [process, ci, quality-gates]
severity: should-fix
status: stable
lang: core
applies_when: Auditing which checks must pass before a change merges.
tool_gate: Branch protection with required status checks.
borrowed_from:
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
  - https://blog.palantir.com/code-review-best-practices-19e02780015f
  - https://www.kubernetes.dev/docs/guide/pull-requests/
  - https://rebels.cs.uwaterloo.ca/papers/msr2014_mcintosh.pdf
---

**Rule.** Require review and passing build, tests, lint, and type checks on the default branch before merge, and leave nothing mechanical to reviewer vigilance.

**Why.** Any rule that depends on someone remembering will be skipped. Components where changes merge unreviewed or without discussion tend to ship more post-release defects.

**FAIL**

```text
Default branch: no protection. Force-push allowed. CI optional.
```

**PASS**

```text
Protected main: 1 approval + required checks (build, test, lint, types).
```

**Counterpoint.** Gates slow small teams, and flaky tests train people to override. Keep gates few and reliable, fix flakes instead of overriding them, and let the gates own the mechanical checks so review time goes to design.
