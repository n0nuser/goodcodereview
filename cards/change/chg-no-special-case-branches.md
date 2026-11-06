---
id: chg-no-special-case-branches
level: change
tags: [maintainability, design, complexity]
severity: should-fix
status: stable
lang: core
applies_when: The change adds a conditional, flag or nullable mode to code that serves more than one feature.
tool_gate: Microsoft CA1502 (cyclomatic complexity, default 25) or PMD CognitiveComplexity (default 15) on the shared function.
note: own function or type - Linux kernel (factor the conditional into a helper function), Effective Go (a type switch, a switch for an if-else chain), Shopify (move the branch onto the item); cap on branches - Microsoft CA1502, PMD CognitiveComplexity; Cursor review rubric is the origin
borrowed_from:
  - https://www.kernel.org/doc/html/latest/process/coding-style.html
  - https://go.dev/doc/effective_go
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1502
  - https://pmd.github.io/pmd/pmd_rules_java_design.html
  - https://shopify.engineering/other-driven-developments
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

**Counterpoint.** "It is one line; an abstraction is overkill." One is fine. The second and third special case are the signal. See [[mod-yagni]] for when not to extract yet..
