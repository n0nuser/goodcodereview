---
id: code-docs-link-dont-duplicate
level: codebase
tags: [maintainability, docs]
severity: discuss
status: stable
lang: core
applies_when: Auditing docs, READMEs or comments that restate a guide, spec or page that already exists elsewhere.
tool_gate: none
note: Google, GitLab and Mozilla (MDN) state it. Chromium and Go are Google. README-per-directory and minimum-viable-docs have only Google behind them
borrowed_from:
  - https://google.github.io/styleguide/docguide/best_practices
  - https://chromium.googlesource.com/chromium/src/+/main/docs/documentation_best_practices.md
  - https://docs.gitlab.com/development/documentation/styleguide/
  - https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Writing_style_guide
---

**Rule.** Link to the existing page or guide instead of rewriting or restating it.

**Why.** Each copy is one more page to keep current, and the copies drift apart. A link has a single owner who fixes it once.

**FAIL**

```text
README.md: a 40-line "How to use git rebase" section copied from the team wiki
```

**PASS**

```text
README.md: Rebase and branch rules are in [the contributing guide](docs/contributing.md#branches).
```

**Counterpoint.** "A link breaks and the reader has to leave the page." Run a link check (see `code-docs-refs-resolve`) and quote only the one line the reader needs here.
