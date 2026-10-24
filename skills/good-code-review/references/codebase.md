# codebase

## code-ci-gates

severity: should-fix  
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
applies_when: Auditing how the repo resolves third-party packages.

**Rule.** Commit a lockfile with hashes and install from it in CI.

**Why.** Unpinned versions make builds non-reproducible and let a compromised release flow straight into production. Updates should arrive as reviewed, staged changes, not silently. [[code-workflow-supply-chain]] covers action pins and token scope.

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
