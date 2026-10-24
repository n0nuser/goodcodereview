---
id: chg-author-hygiene
level: change
tags: [author, process, ci]
severity: should-fix
status: stable
lang: core
applies_when: Every change submitted for review.
tool_gate: PR template with required sections; branch protection requiring green CI.
borrowed_from:
  - https://docs.kernel.org/process/submitting-patches.html
  - https://secure.phabricator.com/book/phabflavor/article/writing_reviewable_code/
  - https://blog.palantir.com/code-review-best-practices-19e02780015f
  - https://www.kubernetes.dev/docs/guide/pull-requests/
---

**Rule.** Self-review the diff and write the description before requesting review.

**Why.** Reviewer time spent on stray debug lines, red builds or a missing "why" is wasted and teaches reviewers to skim. The description gives the reason, the impact and how it was verified; CI is green, or a failing job is shown to fail on the base branch too.

**FAIL**

```text
Title: "fixes". Body empty. CI red on lint. Diff has a leftover print() and
a commented-out block.
```

**PASS**

```text
Body: why (bug link), what changed, test plan, risk. CI green.
Author left inline notes on the two non-obvious hunks.
```

**Counterpoint.** Templates breed boilerplate no one reads. Answer: the check is substance, not headings; a one-line change needs one line of reason. Performance claims need numbers.
