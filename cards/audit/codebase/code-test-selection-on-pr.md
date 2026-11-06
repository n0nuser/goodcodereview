---
id: code-test-selection-on-pr
level: codebase
tags: [testing, performance, process, ci]
severity: discuss
status: stable
lang: core
applies_when: A pull-request CI job runs a test suite that is slower than the team's feedback target for a pull request. Mark `N/A` when the full suite already fits the target.
tool_gate: A PR job that runs the affected-tests command (`nx affected -t test`, Azure Test Impact Analysis, Develocity Predictive Test Selection), plus a full-suite job off the PR path.
note: Meta, Microsoft, Shopify, Nx and Gradle (Develocity) select tests on the PR; Microsoft, Shopify and Gradle keep a full run before deploy or on a schedule (Meta's post does not say). Google's presubmit runs a team-chosen fast subset, not change-based selection
borrowed_from:
  - https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/
  - https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis?view=azure-devops
  - https://shopify.engineering/spark-joy-by-running-fewer-tests
  - https://abseil.io/resources/swe-book/html/ch23.html
  - https://nx.dev/ci/features/affected
  - https://docs.develocity.ai/current/using-develocity/predictive-test-selection/
---

**Rule.** When the full suite is slower than the pull-request feedback target, run only the tests the change affects on the pull request, and run the full suite before deploy or on a schedule.

**Why.** A full suite on every pull request makes the queue wait for tests the change cannot break. Meta runs a third of the affected tests and reports catching more than 99.9 percent of regressions. Shopify runs the tests related to the change. The full run still happens, outside the pull-request gate.

**FAIL**

```yaml
# the only test job
on: pull_request
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest          # 40-minute suite on every PR, no nightly or pre-deploy run
```

**PASS**

```yaml
# .github/workflows/pr.yml
on: pull_request
jobs:
  affected:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: nx affected -t test

# .github/workflows/nightly.yml
on:
  schedule: [{ cron: "0 3 * * *" }]
jobs:
  full:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest
```

**Counterpoint.** "Selection misses regressions." Shopify says a stale mapping let failing tests merge, about 0.06 percent of pull requests, and Microsoft falls back to all tests when it cannot classify a change. Keep the full run, fall back to all tests when the mapping cannot decide, and do not present the pull-request run as full coverage. The selected tests gate the merge, as [[code-ci-gates]] asks; the full run comes before deploy or on a schedule.
