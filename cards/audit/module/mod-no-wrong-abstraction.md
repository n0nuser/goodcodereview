---
id: mod-no-wrong-abstraction
level: module
tags: [maintainability, design]
severity: should-fix
status: draft
lacks: orgs, Metz and Dodds back inlining; the re-split remedy has no third org, and the Counterpoint still cites an unsourced count
lang: core
applies_when: A shared helper or base class has gained flags or conditionals so different callers can bend it.
tool_gate: none
borrowed_from:
  - https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction
  - https://kentcdodds.com/blog/aha-programming
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
---

**Rule.** Inline an abstraction that has grown flags for its callers, then re-split it.

**Why.** Extract an abstraction when real call sites need it ([[mod-yagni]]). A wrong one is harder to remove than the duplication it replaced, because each new caller adds a branch until nobody can say what the code is for.

**FAIL**

```text
def render(doc, *, as_pdf=False, for_email=False, legacy=False, skip_header=False): ...
```

**PASS**

```text
render_pdf(doc), render_email(doc)   # small, similar, independent
```

**Counterpoint.** Sources disagree. Ousterhout lists repetition as a red flag (one fact in many places), and the AHA/Sandi Metz line prefers duplication to a wrong abstraction. They fit together: dedupe knowledge (a rule, a format, a constant), wait on shape, and extract only when the second real caller shows what is shared.