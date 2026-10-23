---
id: sys-supply-chain
level: system
tags: [security, supply-chain, ci]
severity: block
status: draft
lang: core
applies_when: The repo has dependencies, CI workflows or released artifacts.
tool_gate: OpenSSF Scorecard in CI; dependency scanner; lockfile check.
borrowed_from:
  - https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
  - https://slsa.dev/spec/v1.0/levels
---

**Rule.** Pin dependencies with a lockfile and Actions by commit SHA, give workflows least-privilege tokens, never check out PR code in privileged triggers, and publish provenance for releases.

**Why.** OWASP 2025 made supply chain failures its own category (A03). Scorecard rates dangerous workflows Critical and missing token permissions High.

**FAIL**

```text
uses: some/action@v3
on: pull_request_target  # then checks out the PR head
run: echo "${{ github.event.issue.title }}"
```

**PASS**

```text
uses: some/action@<full-commit-sha>
permissions: { contents: read }
build provenance attached (SLSA L1+, signed on a hosted builder for L2)
```

**Counterpoint.** "SHA pins are a maintenance burden." Use an update bot; the burden is the cost of knowing what runs. SLSA's current version is 1.2 per the page; the notes read the v1.0 levels (Build track L0-L3 only).
