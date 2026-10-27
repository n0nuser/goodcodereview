---
id: code-dead-code
level: codebase
tags: [maintainability, cleanup, deletion]
severity: should-fix
status: draft
lacks: orgs, only the Linux kernel and NVIDIA state "delete unused code"; commented-out code and orphaned files have no org; needs one more org per clause
lang: core
applies_when: Auditing for code, flags and files that nothing uses.
tool_gate: Dead-code detectors (vulture, knip, deadcode) plus unused-export lint in CI.
borrowed_from:
  - https://henrikwarne.com/2024/01/10/tidy-first/
  - https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to
  - https://blog.palantir.com/code-review-best-practices-19e02780015f
  - https://docs.kernel.org/process/coding-style.html
  - https://github.com/NVIDIA/Model-Optimizer/blob/main/CONTRIBUTING.md
  - https://www.jetbrains.com/help/inspectopedia/CommentedOutCode.html
  - https://www.uber.com/blog/piranha/
  - https://statsig.com/blog/feature-flag-code-cleanup
---

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
