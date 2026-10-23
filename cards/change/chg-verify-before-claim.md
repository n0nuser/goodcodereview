---
id: chg-verify-before-claim
level: change
tags: [verification, reviewer]
severity: block
status: draft
lang: core
applies_when: The author or reviewer asserts the change works or a finding is real.
tool_gate: none
borrowed_from:
  - https://devguide.python.org/getting-started/pull-request-lifecycle/
  - https://secure.phabricator.com/book/phabflavor/article/writing_reviewable_code/
  - https://danluu.com/tests-v-reason/
---

**Rule.** A claim of "works" or "bug" cites something run: a failing repro, a passing test, a command output. For fixes, reproduce the bug first and rerun the repro after applying the change.

**Why.** Reasoning that "looks correct" misses stateful and corner cases, and a reviewer's false finding wastes the author's time.

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

**Counterpoint.** Running everything is slow. Answer: scale with risk; a rename needs no repro. For UI changes the sources say to see it running, not only read it. Luu's case rests on examples, not studies.
