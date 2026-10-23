---
id: fn-name-intermediate-conditions
level: function
tags: [readability]
severity: discuss
status: draft
lang: core
applies_when: An `if` or `while` joins three or more terms in one expression.
tool_gate: none
borrowed_from:
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
---

**Rule.** Name each compound condition: assign sub-conditions to booleans that say what they mean.

**Why.** Dense conditions force the reader to simulate them. A name states the intent and gives a place to put the next clause.

**FAIL**

```text
if u.active and not u.banned and (u.plan == "pro" or u.trial_days > 0) and not u.locked:
```

**PASS**

```text
can_login = u.active and not u.banned and not u.locked
has_access = u.plan == Plan.PRO or u.trial_days > 0
if can_login and has_access:
```

**Counterpoint.** "More variables, more state to track." These are immutable one-use names, and they replace a comment you would otherwise write. If the names turn out vague (`flag1`), the condition probably mixes two concepts; fix that instead.
