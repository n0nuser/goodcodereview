---
id: fn-comments-stay-short
level: function
tags: [maintainability, docs]
severity: should-fix
status: draft
lacks: orgs, only Google (docguide, Go doc comments) backs moving long reasoning out of comments; needs two more organisations that state it as a practice
lang: core
applies_when: A comment block runs past a few lines, such as a long explanation above a config value or env var.
tool_gate: A comment-length lint with a baseline for existing blocks (Go `commentlen` or `maxcomments-lint`, ESLint `comment-length` for width).
borrowed_from:
  - https://google.github.io/styleguide/docguide/best_practices
  - https://go.dev/doc/comment
---

**Rule.** Keep a comment to a few lines. Put a longer explanation in the docs, a README or an ADR, and leave a one-line link in the comment.

**Why.** Long prose in code is not searched, linked or reviewed as documentation, and it goes stale next to the code it describes. A reader scanning the file skips it, so the one line that mattered gets skipped too.

**FAIL**

```text
# FEATURE_X_TIMEOUT
# (fifteen lines: what the setting does, who sets it,
#  why it was added, how it interacts with retries, history...)
FEATURE_X_TIMEOUT = env("FEATURE_X_TIMEOUT")
```

**PASS**

```text
# Seconds before a Feature X call is abandoned. See docs/config.md#feature-x-timeout.
FEATURE_X_TIMEOUT = env("FEATURE_X_TIMEOUT")
```

**Counterpoint.** "The reader is already at the code, so the explanation belongs there." A short comment keeps the pointer where the reader needs it, and the long text gets one place to be kept current. A genuinely tricky algorithm may need more than a few lines. Then the length is the signal to extract or rename the code first.
