---
id: code-test-suite-time-budget
level: codebase
tags: [testing, performance, ci, process]
severity: should-fix
status: draft
lacks: orgs, "fail the build on a suite or per-test budget" has thoughtbot and SciPy; needs one more org
lang: core
applies_when: Auditing how a codebase keeps its own test suite fast.
tool_gate: A CI step that reads the test report's timings and fails over the budget (thoughtbot test_budget audit), plus a job timeout.
note: thoughtbot (suite budget 10% above today's total, per-type budget at the 99th percentile, allowlist entries expire, the audit fails), Shopify (the time budget is an upper bound and CI runs tests up to it), SciPy (pytest-fail-slow fails a test over 5 s), GitLab (a 45-minute MR pipeline target, not a failing gate)
borrowed_from:
  - https://thoughtbot.com/blog/introducing-test-budget
  - https://shopify.engineering/test-budget-time-constrained-ci-feedback
  - https://scipy.github.io/devdocs/dev/contributor/continuous_integration.html
  - https://about.gitlab.com/blog/gitlab-top-devops-tooling-metrics-and-targets/
---

**Rule.** Record the suite's total time and its slowest tests on every CI run, and fail the build when the total or a single test passes a written budget.

**Why.** A suite slows a few seconds per pull request, and no reviewer sees that in a diff. The team finds out when the run takes 20 minutes and nobody remembers which change did it. A budget that only warns is read once and then ignored.

**FAIL**

```text
CI: run all tests            # duration shown in the log, no limit, no per-test report
```

**PASS**

```text
CI: run all tests, write per-test timings
CI: fail if total > 10 min, or any single test > 5 s unless it is on an allowlist with a reason and an expiry date
```

**Counterpoint.** "A time budget is noisy and fails builds on a slow runner." Set it 10% above today's measured total so it starts green, and tighten it as the suite improves. A hard stop on one test is still worth having, because the fix for a slow test is to profile it, and not to raise its timeout.
