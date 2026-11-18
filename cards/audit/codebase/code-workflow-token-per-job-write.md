---
id: code-workflow-token-per-job-write
level: codebase
tags: [security, ci, supply-chain]
severity: should-fix
status: stable
lang: core
applies_when: Auditing GitHub Actions workflow files.
tool_gate: OpenSSF Scorecard `Token-Permissions` check; zizmor `excessive-permissions` audit.
borrowed_from:
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
  - https://github.com/rust-lang/rustc-dev-guide/blob/master/.github/workflows/ci.yml
  - https://docs.github.com/en/actions/reference/security/secure-use
---

**Rule.** Set workflow token permissions to read-only or none at the top level and grant write only on the job that needs it.

**Why.** Every job in a workflow gets the workflow's token. A compromised step in a test job can then push code or edit releases if the token is wide. Write access held by one job shrinks what a bad step elsewhere can do. [[code-workflow-supply-chain]] covers pinning and untrusted triggers.

**FAIL**

```yaml
permissions: write-all
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: make test
  release:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: make release
```

**PASS**

```yaml
permissions: {}
jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - run: make test
  release:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - run: make release
```

**Counterpoint.** "Repeating permissions on every job is noise." Only the jobs that need more than the top level repeat anything, and a missing key fails closed. The noise is the point: each grant shows in review.
