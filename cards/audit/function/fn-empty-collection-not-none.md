---
id: fn-empty-collection-not-none
level: function
tags: [api, errors]
severity: should-fix
status: draft
lang: core
applies_when: A function returns a list, set or map.
tool_gate: type checker
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Return an empty collection for "nothing found"; return `None` only when absent differs from empty.

**Why.** Every caller must remember the `None` check, and the one who forgets crashes on iteration, in production, on the rare empty case.

**FAIL**

```text
def find_orders(user) -> list[Order] | None:
    return rows or None
```

**PASS**

```text
def find_orders(user) -> list[Order]:
    return rows
```

**Counterpoint.** "None tells me the query failed." Then raise, or return a distinct result type. Using `None` for both "failed" and "empty" is the bug.
