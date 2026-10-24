---
id: chg-no-special-case-branches
level: change
tags: [maintainability, design, complexity]
severity: should-fix
status: draft
lang: core
applies_when: The change adds a conditional, flag or nullable mode to code that serves more than one feature.
tool_gate: none
note: from one vendor's review skill (opinion, no data); keep as a judgement call
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/thermos/skills/thermo-nuclear-code-quality-review/SKILL.md
---

**Rule.** Put a new case behind its own function or type; do not add a one-off branch to a shared flow.

**Why.** Each special case in a shared path is a condition that every later reader and every other feature must reason about. The cases accumulate until nobody can say what the path does.

**FAIL**

```text
def checkout(cart, user):
    ...
    if user.org == "acme":            # added for one customer
        total = total * 0.9
```

**PASS**

```text
def checkout(cart, user, pricing=standard_pricing):
    total = pricing(cart, user)       # acme's rule lives in its own pricing function
```

**Counterpoint.** "It is one line; an abstraction is overkill." One is fine. The second and third special case are the signal. See [[mod-yagni]] for when not to extract yet. Temporary branches need an owner and a removal date ([[chg-flag-owner-retirement]]).
