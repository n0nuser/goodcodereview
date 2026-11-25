---
id: fn-empty-collection-not-none
level: function
tags: [correctness, api, errors]
severity: should-fix
status: draft
lacks: orgs, Microsoft states it; PMD's rule page is a tool description; SEI CERT MET55-J would not load; needs two more orgs
lang: core
applies_when: A function returns a list, set or map.
tool_gate: type checker
borrowed_from:
  - https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/guidelines-for-collections
  - https://pmd.github.io/pmd/pmd_rules_java_errorprone.html
note: Microsoft: do not return null from methods returning collections; PMD ReturnEmptyCollectionRatherThanNull (soft); SEI CERT MET55-J fetch failed 2026-11-24
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
