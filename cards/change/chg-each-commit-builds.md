---
id: chg-each-commit-builds
level: change
tags: [process, testing, maintainability]
severity: discuss
status: stable
lang: core
applies_when: A change is submitted as several commits that are kept, not squashed.
tool_gate: A CI job that checks out each commit and runs the build and tests (`git rebase --exec`, `git bisect run`).
note: The Linux kernel, Prometheus and Django state it. Rust's no-merge-commit rule is related but not the same
borrowed_from:
  - https://docs.kernel.org/process/submitting-patches.html
  - https://raw.githubusercontent.com/prometheus/prometheus/main/CONTRIBUTING.md
  - https://docs.djangoproject.com/en/dev/internals/contributing/committing-code/
---

**Rule.** Make each commit in a series build and pass the tests on its own.

**Why.** `git bisect` can land on any commit. A broken one in the middle of a series sends the person bisecting after a bug that the next commit already fixes.

**FAIL**

```text
commit 1: Rename Config.timeout to Config.deadline   (callers still use timeout; build fails)
commit 2: Update callers to deadline
```

**PASS**

```text
commit 1: Add Config.deadline, keep Config.timeout as an alias
commit 2: Move callers to deadline
commit 3: Remove Config.timeout
```

**Counterpoint.** "We squash on merge." Then the squashed commit is the unit and the rule is met by CI on the PR. The rule matters where the series is kept.
