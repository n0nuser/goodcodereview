---
id: fn-comments-explain-why
level: function
tags: [maintainability, readability, docs]
severity: should-fix
status: stable
lang: core
applies_when: A comment sits next to code, or the code needs one to be understood.
tool_gate: none
note: 3 orgs for the Rule (Google, Mozilla, Apache Flink; PEP 8 agrees). Only Google and the Linux kernel say to rewrite before commenting, so that point sits in the Why
borrowed_from:
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md
  - https://henrikwarne.com/2024/01/10/tidy-first/
  - https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/JavaScript
  - https://peps.python.org/pep-0008/
  - https://flink.apache.org/how-to-contribute/code-style-and-quality-common/
---

**Rule.** Write comments that give a reason, a constraint, or a trade-off, and never restate what the next line does.

**Why.** A restating comment rots silently and adds nothing. A missing reason makes the next person delete the code that mattered. Rename before commenting: clearer code needs fewer comments.

**FAIL**

```text
counter += 1  # increment the counter
retry = False  # see the PR, currently disabled
```

**PASS**

```text
# Business decision: activation and entitlement update in one transaction,
# so a user never has access without an active subscription.
# TODO: remove when billing emits entitlement events itself.
```

**Counterpoint.** "Good names make comments unnecessary." Names carry *what*. They cannot carry why a branch exists, a unit, or what callers may rely on, and a missing reason costs more than a slightly stale one. Rename first, then comment what the name cannot say. A stale comment is a defect either way. The test is whether the comment adds information that the code cannot carry.
