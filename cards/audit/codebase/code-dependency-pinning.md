---
id: code-dependency-pinning
level: codebase
tags: [security, supply-chain, dependencies]
severity: block
status: stable
lang: core
applies_when: Auditing how the repo resolves third-party packages.
tool_gate: Lockfile-required install in CI; dependency-update bot config present.
borrowed_from:
  - https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
  - https://sre.google/sre-book/release-engineering/
---

**Rule.** Commit a lockfile with hashes and install from it in CI.

**Why.** Unpinned versions make builds non-reproducible and let a compromised release flow straight into production. Updates should arrive as reviewed, staged changes, not silently.

**FAIL**

```text
requirements.txt:  requests>=2   (no lockfile; CI runs pip install -U)
```

**PASS**

```text
requirements.lock with hashes; CI: pip install --require-hashes -r requirements.lock
Update bot opens PRs; changes are rolled out in stages.
```

**Counterpoint.** Pinning delays security patches. A pin plus an update bot with a defined cadence beats floating versions, because the lock makes the update visible and revertable.
