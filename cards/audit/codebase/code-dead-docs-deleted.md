---
id: code-dead-docs-deleted
level: codebase
tags: [maintainability, docs]
severity: discuss
status: stable
note: Google (eng-practices), the Linux kernel and GitLab state it for docs of removed or never-shipped code. Whole-section retirement (MDN) and a deprecate-then-delete delay (Fuchsia) are partial
lang: core
applies_when: Auditing a repo whose docs, READMEs or design notes describe code that has since changed or gone.
tool_gate: A freshness check (last-reviewed date or owner per page) that fails or flags pages untouched past a threshold.
borrowed_from:
  - https://google.github.io/styleguide/docguide/best_practices
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://chromium.googlesource.com/chromium/src/+/main/docs/documentation_best_practices.md
  - https://docs.gitlab.com/development/documentation/workflow/
  - https://www.kernel.org/doc/html/latest/doc-guide/contributing.html
---

**Rule.** Delete the docs for code or features that were removed or never shipped, instead of leaving or hiding them.

**Why.** A wrong page is worse than none: readers trust it. A design doc left as a living doc after the code ships drifts the same way, so archive it as a decision record. Version control keeps the history, so deleting loses nothing. Docs known to be wrong go for the same reason.

**FAIL**

```text
docs/design-auth-v1.md   # describes a login flow removed two releases ago, no status line
```

**PASS**

```text
docs/adr/0004-auth.md    # status: superseded by 0009; the old design doc is deleted
```

**Counterpoint.** "Old docs may still help someone." Version control keeps them. The kernel guide allows an outdated-warning banner on a page you cannot fix yet. Mark a still-useful record `superseded` and link the replacement so nobody mistakes it for current.
