# codebase

## code-ci-gates

severity: should-fix  
concerns: process  
applies_when: Auditing which checks must pass before a change merges.

**Rule.** Require review and passing build, tests, lint, and type checks on the default branch before merge, and leave nothing mechanical to reviewer vigilance.

**Why.** Any rule that depends on someone remembering will be skipped. Components where changes merge unreviewed or without discussion tend to ship more post-release defects.

**FAIL**

```text
Default branch: no protection. Force-push allowed. CI optional.
```

**PASS**

```text
Protected main: 1 approval + required checks (build, test, lint, types).
```

**Counterpoint.** Gates slow small teams, and flaky tests train people to override. Keep gates few and reliable, fix flakes instead of overriding them, and let the gates own the mechanical checks so review time goes to design.

## code-dead-code

severity: should-fix  
concerns: maintainability  
applies_when: Auditing for code, flags and files that nothing uses.

**Rule.** Remove unreferenced functions, commented-out code, expired flags, and orphaned files; history keeps them.

**Why.** Dead code costs reading time, misleads searches, and gets "fixed" and tested for no benefit.

**FAIL**

```text
# def old_export(): ...   (commented out since 2022)
if FLAGS["legacy_ui"]:     # flag permanently false since release 4
```

**PASS**

```text
Code deleted; git log -S shows where it went. Detector reports 0 unused symbols
or each is allowlisted with a reason.
```

**Counterpoint.** Code may be called by reflection, plugins, or external users. Check with the detector's config and a grep of consumers. For public API, deprecate first (see `chg-expand-contract`).

## code-dependency-pinning

severity: block  
concerns: security  
applies_when: Auditing how the repo resolves third-party packages.

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

## code-perf-budget-in-ci

severity: should-fix  
concerns: performance, process  
applies_when: The repo has a performance target (bundle size, page metrics, latency under load, or a benchmark) that matters to users.

**Rule.** Write the performance budget down as a CI check that fails the build when it is exceeded.

**Why.** Performance regresses a few percent at a time, and no reviewer sees a 3% slowdown in a diff. A budget that only warns becomes a log line nobody reads.

**FAIL**

```text
lighthouserc.json: "assertions": { "categories:performance": ["warn", { "minScore": 0.9 }] }
k6 script with no thresholds block
```

**PASS**

```text
size-limit: [{ "path": "dist/app.js", "limit": "180 kB" }]   # npm run size in CI
k6: thresholds: { http_req_duration: ["p(95)<300"] }        # non-zero exit fails the job
```

**Counterpoint.** "Benchmarks in CI are noisy and flake." They are when a gate trusts one run. Gate on a stable budget, compare repeated runs (benchstat wants 10 to 20), and keep the threshold above the noise. On a site with much room to improve, a tight budget only turns every build red, so set it at today's level and lower it later.

## code-secret-scan

severity: block  
concerns: security, process  
applies_when: Any repository, including its history, issues and pull requests.

**Rule.** Scan for committed credentials, and treat any hit as leaked: revoke and replace it first.

**Why.** A secret in history is readable by everyone with clone access, and forks and caches keep it after a rewrite. Rewriting history is slow and often unnecessary once the secret is dead.

**FAIL**

```text
git log -p | rg 'AKIA'      # a live cloud key in an old commit; "removed it in the next commit"
```

**PASS**

```text
scanner runs on every push and covers history
key revoked and reissued the same day; new value comes from the secret store
```

**Counterpoint.** "Scanners give false positives." Tune with an allowlist of reviewed, non-secret strings. A missed live key costs far more than a triaged alert. [sys-secrets-and-errors](system.md#sys-secrets-and-errors) covers where secrets live at runtime.
