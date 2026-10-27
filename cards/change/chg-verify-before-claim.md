---
id: chg-verify-before-claim
level: change
tags: [testing, process, verification, reviewer]
severity: block
status: stable
lang: core
applies_when: The author or reviewer asserts the change works or a finding is real.
tool_gate: none
note: Python, Google and GitLab back the run-something clause; GitLab asks for maintainer review only when tests pass and for an explanation when they fail. Anthropic (a vendor) also backs run-it-and-show-the-result, "Instead of saying the task is done, we ask it to show us the result", and is not counted
borrowed_from:
  - https://devguide.python.org/getting-started/pull-request-lifecycle/
  - https://secure.phabricator.com/book/phabflavor/article/writing_reviewable_code/
  - https://danluu.com/tests-v-reason/
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://x.com/addyosmani/status/2114604912520921136
  - https://docs.gitlab.com/development/code_review/
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

**Counterpoint.** Running everything is slow. Scale with risk: a rename needs no repro, but a race, a bug fix, or a UI change does. See it run, do not only read it.
