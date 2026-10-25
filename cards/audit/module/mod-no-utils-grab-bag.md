---
id: mod-no-utils-grab-bag
level: module
tags: [maintainability, architecture, naming]
severity: should-fix
status: draft
lacks: evidence, the only backer is a dev.to summary of Ousterhout; needs two orgs that say to name helpers after a concept
lang: core
applies_when: The diff adds or grows a module named `utils`, `helpers`, `common`, or `misc`.
tool_gate: none
borrowed_from:
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
---

**Rule.** Put a helper in the module that owns the concept, or in a new module named after the concept.

**Why.** A grab-bag has no owner and no cohesion. It becomes the dependency of everything and the place where unrelated code accretes.

**FAIL**

```text
utils.py: parse_date, send_email, price_with_tax, retry
```

**PASS**

```text
dates.py, notifications.py, pricing.py, retry.py
```

**Counterpoint.** "Tiny helpers do not deserve a file." Then inline them where they are used (YAGNI applies). When one is shared, naming its concept is the work that makes it findable.
