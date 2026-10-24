---
id: code-workflow-supply-chain
level: codebase
tags: [security, process, supply-chain, ci]
severity: block
status: draft
lang: core
applies_when: Auditing CI workflow files and release pipelines.
tool_gate: OpenSSF Scorecard run in CI; workflow linters.
note: SLSA page fetched was the v1.0 path, which says a newer version is current
borrowed_from:
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
  - https://slsa.dev/spec/v1.0/levels
  - https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
  - https://docs.github.com/en/actions/reference/security/secure-use
---

**Rule.** Pin every CI action to a full commit SHA.

**Why.** The pipeline holds secrets and publish rights, so a compromised action or injected input owns the artifact. Also give workflows least-privilege tokens, keep untrusted event data out of `run:` and out of `pull_request_target` checkouts, and attach build provenance to releases. [[code-dependency-pinning]] covers dependency pins, and [[code-dependency-licence-sbom]] covers the inventory.

**FAIL**

```yaml
on: pull_request_target
steps:
  - uses: some/action@v3            # tag, not SHA
  - run: echo "${{ github.event.pull_request.title }}"
  - uses: actions/checkout@v4
    with: { ref: ${{ github.event.pull_request.head.sha }} }
```

**PASS**

```yaml
permissions: { contents: read }
steps:
  - uses: some/action@<40-char-sha>
  - run: echo "$TITLE"
    env: { TITLE: ${{ github.event.pull_request.title }} }
```

**Counterpoint.** "SHA pinning blocks automatic fixes and adds update churn." Let an update bot propose SHA bumps, so fixes still arrive as reviewed changes. Where the platform offers a lockfile for workflow dependencies, that lockfile is stronger than SHA pins and meets this check.
