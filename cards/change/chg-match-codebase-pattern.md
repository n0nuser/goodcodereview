---
id: chg-match-codebase-pattern
level: change
tags: [correctness, maintainability, consistency, style]
severity: should-fix
status: stable
note: Rule backed by Google (eng-practices standard), PEP 8, and the Microsoft engineering playbook; the Orosz post is inferred support only
lang: core
applies_when: The change adds code that solves a problem the codebase already solves somewhere.
tool_gate: Repeated style nits mean a missing linter or formatter rule; add the gate instead of commenting.
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/standard.html
  - https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/
  - https://peps.python.org/pep-0008/
  - https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/
---

**Rule.** Follow the established pattern nearby.

**Why.** A silent second way to do the same thing doubles what every later reader must learn. Equally, copying a bad pattern forever freezes it in place.

**FAIL**

```text
Repo uses Result-returning repository classes everywhere.
New PR adds a module that raises raw DB exceptions and builds SQL inline,
description: "cleaner this way". No ticket, no mention of the old pattern.
```

**PASS**

```text
New module uses the repository pattern like its neighbours.
PR notes: "pattern X leaks DB errors, see TICKET-123 proposing a standard".
Code the PR touches anyway is improved in passing.
```

**Counterpoint.** "Consistency preserves bugs." Consistency is a tie-breaker, not a reason to copy something that breaks a rule or hurts code health, so a reviewer must not demand matching code that makes things worse. When the nearby pattern is bad, keep to the local style in this change, file a ticket, and propose the new standard in its own change, improving what you touch. A second pattern slipped into a feature change without a word is the failure.
