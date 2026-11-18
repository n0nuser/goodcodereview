---
id: chg-link-tracked-issue
level: change
tags: [process, maintainability]
severity: discuss
status: draft
lacks: orgs, "link each PR to its issue" has Apache and WordPress; needs a third org
lang: core
applies_when: The project tracks work in an issue tracker.
tool_gate: PR template with a required "Closes" line; a CI check for a linked issue.
borrowed_from:
  - https://flink.apache.org/how-to-contribute/code-style-and-quality-pull-requests/
  - https://raw.githubusercontent.com/WordPress/gutenberg/trunk/.github/PULL_REQUEST_TEMPLATE.md
---

**Rule.** Link each pull request to the issue it addresses, with a keyword such as `Closes` or `See`.

**Why.** The issue holds the problem statement, the discussion and the decision. Without the link a reviewer cannot check the change against the ask, and the issue stays open after the fix merges.

**FAIL**

```text
Title: Fix pagination on the orders page
Body: Fixes the off-by-one. Tests added.
(no issue reference; the bug report is still open)
```

**PASS**

```text
Title: Fix pagination on the orders page
Body: Fixes the off-by-one. Tests added.
Closes #412
```

**Counterpoint.** "Opening an issue for a one-line fix is overhead." Agreed: a typo fix or similar hotfix needs no issue. Anything that changes behaviour does, because the issue is where the reason lives.
