---
id: chg-verify-before-claim
level: change
tags: [verification, reviewer]
severity: block
status: stable
lang: core
applies_when: The author or reviewer asserts the change works or a finding is real.
tool_gate: none
borrowed_from:
  - https://devguide.python.org/getting-started/pull-request-lifecycle/
  - https://secure.phabricator.com/book/phabflavor/article/writing_reviewable_code/
  - https://danluu.com/tests-v-reason/
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
---

**Rule.** Back every "works" or "bug" claim with something run: a repro, a test or command output.

**Why.** Reasoning that "looks correct" misses stateful and corner cases, and a reviewer's false finding wastes the author's time. For a bug fix, reproduce the bug first and rerun the repro after the change.

**FAIL**

```text
Author: "Fixed the race, trust me." Reviewer: "LGTM, reads fine."
Nobody ran the failing case.
```

**PASS**

```text
Author: "repro: script X failed 3/10 runs; after fix 0/200. Test added."
Reviewer checked out the branch and reran it.
```

**Counterpoint.** Running everything is slow. Scale with risk: a rename needs no repro; a race, a bug fix or a UI change does. See it run, do not only read it.
