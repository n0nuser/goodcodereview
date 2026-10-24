---
id: chg-one-concern
level: change
tags: [scope, size]
severity: should-fix
status: stable
lang: core
applies_when: Every change.
tool_gate: A CI check can label or warn on file count and diff size.
borrowed_from:
  - https://docs.kernel.org/process/submitting-patches.html
  - https://devguide.python.org/getting-started/pull-request-lifecycle/
  - https://secure.phabricator.com/book/phabflavor/article/writing_reviewable_code/
  - https://blog.palantir.com/code-review-best-practices-19e02780015f
---

**Rule.** Make each change do one logical thing; if the description needs "and" between unrelated outcomes, split it.

**Why.** Reviewers can only judge intent and risk of a single concern. Mixed changes hide the risky part, cannot be reverted alone, and break bisect.

**FAIL**

```text
PR "Add export button": new endpoint, renamed 40 files, bumped a dependency,
fixed an unrelated typo in the auth module.
```

**PASS**

```text
PR 1: dependency bump.  PR 2: rename (no logic change).  PR 3: export button.
```

**Counterpoint.** Splitting adds overhead, and stacked diffs need tooling and cost rebasing pain. The rule is one concern, not a line count: as small as possible, but no smaller. A single concern that is legitimately large (a generated migration) is fine if the description says so.
