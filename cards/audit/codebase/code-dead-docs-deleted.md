---
id: code-dead-docs-deleted
level: codebase
tags: [maintainability, docs]
severity: discuss
status: draft
lacks: orgs, Google and GitLab back deleting wrong docs; needs a third org (Chromium counts as Google)
lang: core
applies_when: Auditing a repo whose docs, READMEs or design notes describe code that has since changed or gone.
tool_gate: A freshness check (last-reviewed date or owner per page) that fails or flags pages untouched past a threshold.
borrowed_from:
  - https://google.github.io/styleguide/docguide/best_practices
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://chromium.googlesource.com/chromium/src/+/main/docs/documentation_best_practices.md
  - https://docs.gitlab.com/development/documentation/workflow/
---

**Rule.** Delete docs known to be wrong or obsolete instead of leaving them in place or hiding them.

**Why.** A wrong page is worse than none: readers trust it. A design doc left as a living doc after the code ships drifts the same way, so archive it as a decision record. Version control keeps the history, so deleting loses nothing.

**FAIL**

```text
docs/design-auth-v1.md   # describes a login flow removed two releases ago, no status line
```

**PASS**

```text
docs/adr/0004-auth.md    # status: superseded by 0009; the old design doc is deleted
```

**Counterpoint.** "Old docs may still help someone." Version control keeps them. Mark a still-useful record `superseded` and link the replacement so nobody mistakes it for current.
