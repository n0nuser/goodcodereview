---
id: mod-fowler-smells
level: module
tags: [design, refactoring]
severity: discuss
status: draft
lang: core
applies_when: A reviewer sees long methods, feature envy, data clumps, primitive obsession, speculative generality or divergent change.
tool_gate: none
borrowed_from:
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
---

**Rule.** Name the smell, point to the line, and suggest the refactoring; do not file smells as taste.

**Why.** Smells are cheap to see and expensive to ignore, but a vague "this feels off" gives the author nothing to fix.

**FAIL**

```text
review: "This is messy."
```

**PASS**

```text
review: "should-fix: price_total reads only Order fields (feature envy). Move it to Order."
```

**Counterpoint.** "Smells are subjective." Yes: they signal, not prove. Sources here do not give Fowler's catalogue directly, so this card is DRAFT: it is mapped through Ousterhout's red flags (shallow module, pass-through, special-general mix). Add the Fowler/Beck primary source before marking stable.
