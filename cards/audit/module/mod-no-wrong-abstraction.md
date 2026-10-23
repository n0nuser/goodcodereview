---
id: mod-no-wrong-abstraction
level: module
tags: [design]
severity: should-fix
status: draft
lang: core
applies_when: A shared helper or base class has gained flags or conditionals so different callers can bend it.
tool_gate: none
borrowed_from:
  - https://kentcdodds.com/blog/aha-programming
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
---

**Rule.** Duplicate until the pattern is proven. When an abstraction grows boolean switches for its callers, inline it and re-split.

**Why.** A wrong abstraction is harder to remove than the duplication it replaced. Each new caller adds a branch, until nobody can say what the code is for.

**FAIL**

```text
def render(doc, *, as_pdf=False, for_email=False, legacy=False, skip_header=False): ...
```

**PASS**

```text
render_pdf(doc), render_email(doc)   # small, similar, independent
```

**Counterpoint.** Sources disagree: Ousterhout lists repetition as a red flag (one fact in many places); AHA/Sandi Metz prefer duplication to a wrong abstraction. They fit together: dedupe knowledge (a rule, a format, a constant), wait on shape. At the second copy tolerate it; at the third, ask. The count is a weak heuristic, not a law.
