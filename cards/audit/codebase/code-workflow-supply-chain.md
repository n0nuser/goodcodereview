---
id: code-workflow-supply-chain
level: codebase
tags: [security, process, supply-chain, ci]
severity: block
status: stable
lang: core
applies_when: Auditing CI workflow files and release pipelines.
tool_gate: OpenSSF Scorecard `Pinned-Dependencies` and `Dangerous-Workflow` checks; zizmor `unpinned-uses` audit.
note: GitHub, OpenSSF and StepSecurity back the pin; GitHub, OpenSSF (Scorecard `Dangerous-Workflow`) and GitLab (protected runners keep untrusted code off deployment keys) back the untrusted-code boundary; OWASP's CI/CD cheat sheet is a reference only
borrowed_from:
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
  - https://slsa.dev/spec/v1.0/levels
  - https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
  - https://docs.github.com/en/actions/reference/security/secure-use
  - https://www.stepsecurity.io/blog/pinning-github-actions-for-enhanced-security-a-complete-guide
  - https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html
  - https://docs.gitlab.com/ci/pipelines/
---

**Rule.** Pin every CI action to a full commit SHA, and keep code from an unreviewed change out of any job that holds secrets or can deploy.

**Why.** The pipeline holds secrets and publish rights, so a compromised action or injected input owns the artifact. A privileged trigger that checks out a fork runs the fork's code with the base repository's token and secrets. Give workflows least-privilege tokens, keep untrusted event data out of `run:` and out of `pull_request_target` checkouts, and attach build provenance to releases. Review a change to the workflow file like any other code, because it can grant the next job anything. [[code-dependency-pinning]] covers dependency pins, and [[code-dependency-licence-sbom]] covers the inventory.

**FAIL**

```yaml
on: pull_request_target
permissions: write-all
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4        # tag, can be moved to other code
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: ./build.sh                  # runs the PR author's code with the base repo's token
```

**PASS**

```yaml
on: pull_request
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<40-char-sha>   # v4.2.2
      - uses: some/action@<40-char-sha>        # v3.1.0
  deploy:
    if: github.ref == 'refs/heads/main'      # never runs for a fork or an unmerged change
    needs: build
    runs-on: ubuntu-latest
    environment: production                  # protected environment: required reviewers, scoped secrets
    steps:
      - run: ./deploy.sh
```

**Counterpoint.** "SHA pinning blocks automatic fixes and adds update churn." Let an update bot propose SHA bumps, so fixes still arrive as reviewed changes. Where the platform offers a lockfile for workflow dependencies, that lockfile is stronger than SHA pins and meets this check. A `pull_request_target` job can be safe when it never checks out or runs the fork's code, but splitting the privileged job from the untrusted one is easier to review than keeping them together.

