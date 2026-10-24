---
id: mod-yagni
level: module
tags: [maintainability, process, design, scope]
severity: should-fix
status: stable
lang: core
applies_when: The change adds an abstraction, parameter, hook or option.
tool_gate: none
borrowed_from:
  - https://kentcdodds.com/blog/aha-programming
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://henrikwarne.com/2024/01/10/tidy-first/
---

**Rule.** Add an abstraction only when the logic is reused, non-trivial, or clutters the main flow; do not build for a need that does not exist yet.

**Why.** Speculative flexibility costs reading time every day and is usually the wrong shape when the need arrives. Reviewers cannot verify a use that does not exist.

**FAIL**

```text
class NotifierFactory: ...   # one product, one caller
def send(msg, retries=3, backoff=None, hook=None): ...   # nobody passes these
```

**PASS**

```text
def send_welcome_email(user): ...
```

**Counterpoint.** "But we will surely need it." Then add it when you do, in a change that has the real second caller to shape it. Optimising for easy change means simple code, not built-in flexibility. Trivial single-use logic stays inline. The cost of waiting is low, and the cost of the wrong guess is not.
