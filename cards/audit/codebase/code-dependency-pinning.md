---
id: code-dependency-pinning
level: codebase
tags: [supply-chain, dependencies]
severity: block
status: draft
lang: core
applies_when: Auditing how the repo resolves third-party packages.
tool_gate: Lockfile-required install in CI; dependency-update bot config present.
borrowed_from:
  - https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
---

**Rule.** Every deployable has a committed lockfile and CI installs from it; dependency updates arrive through reviewed changes, staged, not silently.

**Why.** Unpinned versions make builds non-reproducible and let a compromised release flow straight into production.

**FAIL**

```text
requirements.txt:  requests>=2   (no lockfile; CI runs pip install -U)
```

**PASS**

```text
requirements.lock with hashes; CI: pip install --require-hashes -r requirements.lock
Update bot opens PRs; changes are rolled out in stages.
```

**Counterpoint.** Pinning delays security patches. Answer: pin plus an update bot with a defined cadence beats floating versions; the lock makes the update visible and revertable.
