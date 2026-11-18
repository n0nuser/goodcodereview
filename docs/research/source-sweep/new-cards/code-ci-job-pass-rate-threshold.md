---
id: code-ci-job-pass-rate-threshold
level: codebase
tags: [reliability, process, ci]
severity: discuss
status: draft
lacks: orgs, GitLab states a target and Kubernetes a gate; needs one more org that sets a numeric pass rate for the pipeline or a blocking job
lang: core
applies_when: Auditing how a team keeps its main-branch pipeline and blocking CI jobs trustworthy.
tool_gate: A scheduled job that reads pass rate from CI history and opens an issue or pages the owner below the threshold.
borrowed_from:
  - https://about.gitlab.com/blog/gitlab-top-devops-tooling-metrics-and-targets/
  - https://github.com/kubernetes/sig-release/blob/master/release-blocking-jobs.md
---

**Rule.** Set a numeric pass-rate threshold for the pipeline or each blocking job, and act when it falls below it.

**Why.** A blocking job that fails one run in three teaches people to rerun and merge. With no number, nobody can say when the job has gone bad, so nobody owns the fix. [[code-flaky-test-quarantine]] covers the single flaky test.

**FAIL**

```text
CI dashboard: main pipeline green 61% of runs this week.
No target, no owner. "Just rerun it."
```

**PASS**

```text
Policy: main pipeline passes at least 95% of runs; each blocking job at least 75% per week.
Below the line: the owning team is paged, and the job leaves the merge gate until it recovers.
This week: 97%.
```

**Counterpoint.** "A threshold lets a 5% failure rate stand." It does, on purpose: the number is a floor that triggers action, not a goal. Raise it as the pipeline improves, and treat each failure below the floor as a bug to fix.
