---
id: code-ci-gates
level: codebase
tags: [ci, quality-gates]
severity: should-fix
status: draft
lang: core
applies_when: Auditing which checks must pass before a change merges.
tool_gate: Branch protection with required status checks.
borrowed_from:
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
  - https://blog.palantir.com/code-review-best-practices-19e02780015f
  - https://www.kubernetes.dev/docs/guide/pull-requests/
  - https://rebels.cs.uwaterloo.ca/papers/msr2014_mcintosh.pdf
---

**Rule.** The default branch requires review and passing build, tests, lint and type checks before merge; nothing mechanical is left to reviewer vigilance.

**Why.** Any rule that depends on someone remembering will be skipped. Observational data also links low review coverage and participation to more post-release defects.

**FAIL**

```text
Default branch: no protection. Force-push allowed. CI optional.
```

**PASS**

```text
Protected main: 1 approval + required checks (build, test, lint, types).
```

**Counterpoint.** Gates slow small teams and flaky tests train people to override. Answer: keep gates few and reliable, and fix flakes. The McIntosh result is association from three projects (models explain 19-44% of variance), not proof that review causes fewer defects.
