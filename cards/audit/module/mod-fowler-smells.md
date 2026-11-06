---
id: mod-fowler-smells
level: module
tags: [maintainability, design, refactoring]
severity: discuss
status: stable
lang: core
applies_when: A reviewer sees long methods, feature envy, data clumps, primitive obsession, speculative generality, or divergent change.
tool_gate: none
borrowed_from:
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://google.github.io/eng-practices/review/reviewer/standard.html
  - https://docs.gitlab.com/development/code_review/
  - https://blog.palantir.com/code-review-best-practices-19e02780015f
note: name the issue and give a reason, not taste - Google ("Aspects of software design are almost never a pure style issue"), GitLab ("Be explicit", "Offer alternative implementations"), Palantir ("Suggestion: extract method to improve legibility", "Critique the code, not the author"); the smell catalog itself comes from Fowler and Beck (persons) through Ousterhout's red flags
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

**Counterpoint.** "Smells are subjective." Yes: they signal; they do not prove. That is why the comment names the smell, the line, and the refactoring. "This is messy" gives the author nothing to act on.