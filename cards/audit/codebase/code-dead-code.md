---
id: code-dead-code
level: codebase
tags: [maintainability, cleanup, deletion]
severity: should-fix
status: stable
lang: core
applies_when: Auditing for code, flags and files that nothing uses.
tool_gate: An unused-code linter in CI (vulture, knip, or deadcode); allowlist each intentional exception with a reason.
note: Commented-out code (Lockheed Martin JSF, JetBrains) and orphaned files (no source) have fewer than three organisations, so they sit in the Why. Palantir's page loads and backs only the commented-out-code case in the Why. Version-control history as the reason to delete has two organisations (Google, JetBrains), so it stays in the Why. JetBrains and Statsig are vendors.
borrowed_from:
  - https://henrikwarne.com/2024/01/10/tidy-first/
  - https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to
  - https://blog.palantir.com/code-review-best-practices-19e02780015f
  - https://abseil.io/resources/swe-book/html/ch09.html
  - https://abseil.io/resources/swe-book/html/ch15.html
  - https://engineering.fb.com/2023/10/24/data-infrastructure/automating-dead-code-cleanup/
  - https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/recommendations/miscellaneous-msc/msc12-c
  - https://docs.kernel.org/process/coding-style.html
  - https://github.com/NVIDIA/Model-Optimizer/blob/main/CONTRIBUTING.md
  - https://learn.microsoft.com/en-us/devops/operate/progressive-experimentation-feature-flags
  - https://docs.gitlab.com/ee/development/feature_flags/
  - https://www.uber.com/blog/piranha/
  - https://statsig.com/blog/feature-flag-code-cleanup
  - https://www.jetbrains.com/help/inspectopedia/CommentedOutCode.html
  - https://www.stroustrup.com/JSF-AV-rules.pdf
---

**Rule.** Delete unreferenced functions and variables, and the branches of expired feature flags.

**Why.** Dead code costs reading time, misleads searches, and gets "fixed" and tested for no benefit. The same holds for the common cases of commented-out code and files nothing links to: delete them too and let version control remember.

**FAIL**

```text
def old_export(): ...      # no caller anywhere in the repo
if FLAGS["legacy_ui"]:     # flag permanently false since release 4
    render_legacy()
```

**PASS**

```text
Unused function and expired-flag branch deleted; version history shows where they went.
The unused-code linter reports 0 symbols, or each is allowlisted with a reason.
```

**Counterpoint.** Code may be called by reflection, plugins, or external users. Check with the detector's config and a grep of consumers. For public API, deprecate first (see `chg-expand-contract`).
