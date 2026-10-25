---
id: code-workflow-supply-chain
level: codebase
tags: [security, process, supply-chain, ci]
severity: block
status: stable
lang: core
applies_when: Auditing CI workflow files and release pipelines.
tool_gate: OpenSSF Scorecard `Pinned-Dependencies` check; zizmor `unpinned-uses` audit.
note: GitHub, OpenSSF and StepSecurity back the Rule; OWASP backs pinning in general
borrowed_from:
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
  - https://slsa.dev/spec/v1.0/levels
  - https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
  - https://docs.github.com/en/actions/reference/security/secure-use
  - https://www.stepsecurity.io/blog/pinning-github-actions-for-enhanced-security-a-complete-guide
---

**Rule.** Pin every CI action to a full commit SHA.

**Why.** The pipeline holds secrets and publish rights, so a compromised action or injected input owns the artifact. Also give workflows least-privilege tokens, keep untrusted event data out of `run:` and out of `pull_request_target` checkouts, and attach build provenance to releases. [[code-dependency-pinning]] covers dependency pins, and [[code-dependency-licence-sbom]] covers the inventory.

**FAIL**

```yaml
steps:
  - uses: actions/checkout@v4        # tag, can be moved to other code
  - uses: some/action@main           # branch, changes on every push
```

**PASS**

```yaml
permissions:
  contents: read
steps:
  - uses: actions/checkout@<40-char-sha>   # v4.2.2
  - uses: some/action@<40-char-sha>        # v3.1.0
```

**Counterpoint.** "SHA pinning blocks automatic fixes and adds update churn." Let an update bot propose SHA bumps, so fixes still arrive as reviewed changes. Where the platform offers a lockfile for workflow dependencies, that lockfile is stronger than SHA pins and meets this check.
