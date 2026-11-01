---
id: code-release-gated-on-ci
level: codebase
tags: [reliability, process, ci, release]
severity: should-fix
status: draft
lacks: evidence, GitHub and GitLab pages describe the feature; only Kubernetes states the practice (red jobs, no release); needs two more orgs that gate releases on CI
lang: core
applies_when: Auditing a workflow or pipeline that publishes a release when a tag is pushed.
tool_gate: Release job with `needs:` the test job, or a `workflow_run` trigger checked for `conclusion == 'success'`; a tag ruleset with required status checks.
note: code-ci-gates covers merge to the default branch, and this card covers the tag-to-publish path, which a merge gate does not cover
borrowed_from:
  - https://github.com/kubernetes/sig-release/blob/master/release-blocking-jobs.md
  - https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
  - https://docs.gitlab.com/ci/pipelines/
---

**Rule.** Make a release or publish job depend on the checks passing for the tagged commit, never on the tag alone.

**Why.** A tag can point at a commit that was never built or tested, or one whose checks are red. A workflow that fires on the tag then ships it. Branch protection does not help, because the tag does not go through a pull request.

**FAIL**

```yaml
on:
  push:
    tags: ["v*"]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<40-char-sha>
      - run: make publish
```

**PASS**

```yaml
on:
  push:
    tags: ["v*"]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<40-char-sha>
      - run: make test
  publish:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<40-char-sha>
      - run: make publish
```

**Counterpoint.** "CI already passed on the pull request, so rerunning tests on the tag wastes time." The pull request tested another commit if the base moved or the tag was cut elsewhere. Reuse the result by requiring the status check on the tagged commit, instead of dropping the gate.
