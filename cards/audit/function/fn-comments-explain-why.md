---
id: fn-comments-explain-why
level: function
tags: [readability, docs]
severity: should-fix
status: draft
lang: core
applies_when: A comment sits next to code, or the code needs one to be understood.
tool_gate: none
borrowed_from:
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md
---

**Rule.** Write comments that give a reason, a constraint or a trade-off. Never restate what the next line does. Rename before commenting.

**Why.** A restating comment rots silently and adds nothing. A missing reason makes the next person delete the code that mattered.

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

**Counterpoint.** Sources disagree. Martin treats comments as a last resort after names; Ousterhout argues missing comments cost more than wrong ones (his multiplier is anecdotal). Both agree a stale comment is a defect and a *what* comment is waste. The test: does it add information the code cannot carry?
