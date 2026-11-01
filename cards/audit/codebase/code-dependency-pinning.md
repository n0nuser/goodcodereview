---
id: code-dependency-pinning
level: codebase
tags: [security, supply-chain, dependencies]
severity: block
status: stable
lang: core
applies_when: Auditing how the repo resolves third-party packages.
tool_gate: Lockfile-required install in CI; dependency-update bot config present.
note: Install must fail on a stale lock, not re-resolve (npm ci errors when the lock and package.json disagree; pip --require-hashes rejects unhashed requirements). The Go and uv/poetry equivalents are the same rule applied to their tools; the sources name npm and pip only
borrowed_from:
  - https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
  - https://sre.google/sre-book/release-engineering/
  - https://pip.pypa.io/en/stable/topics/secure-installs/
  - https://docs.npmjs.com/cli/v10/commands/npm-ci
---

**Rule.** Commit a lockfile with hashes and install from it in CI.

**Why.** Unpinned versions make builds non-reproducible and let a compromised release flow straight into production. Updates should arrive as reviewed, staged changes, not silently. [[code-workflow-supply-chain]] covers CI action pins.

**FAIL**

```text
requirements.txt:  requests>=2   (no lockfile; CI runs pip install -U)
```

**FAIL** (other ecosystems)

```text
CI: npm install            (rewrites package-lock.json, ignores drift)
CI: go build -mod=mod ./...   (go.sum changes silently)
CI: uv sync               (re-resolves and rewrites uv.lock when it is stale)
CI: poetry install        (no poetry.lock committed, so it resolves and creates one)
```

**PASS**

```text
requirements.lock with hashes; CI: pip install --require-hashes -r requirements.lock
Update bot opens PRs; changes are rolled out in stages.
```

```text
CI: npm ci                       (integrity hashes in package-lock.json; fails on drift)
CI: go mod verify && go build -mod=readonly ./...   (go.sum committed)
CI: uv sync --locked      (fails if uv.lock is stale)
CI: poetry install        (poetry.lock committed; fails if it is stale)
```

**Counterpoint.** Pinning delays security patches. A pin plus an update bot with a defined cadence beats floating versions, because the lock makes the update visible and revertable.
