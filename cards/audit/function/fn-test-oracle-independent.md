---
id: fn-test-oracle-independent
level: function
tags: [correctness, testing, tests]
severity: should-fix
status: draft
lacks: orgs, Google states "from the requirement"; Microsoft backs "no logic in tests"; one source is person-authored
lang: core
applies_when: A test asserts on a computed value.
tool_gate: Mutation testing.
note: Google, Microsoft and Cursor each say to write the expected value out in the test, not compute it with logic that can share the bug
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-test-behavior-not-implementation/SKILL.md
  - https://abseil.io/resources/swe-book/html/ch12.html
  - https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices
---

**Rule.** Take a test's expected value from the requirement, not from the code under test.

**Why.** An expected value computed by the code under test passes when the code is wrong. Likewise, a "not called" assertion passes when the spy is wired to the wrong target, so pair it with a case where the call happens.

**FAIL**

```python
assert total(items) == sum(i.price for i in items)   # re-implements the code
```

**PASS**

```python
assert total([Item(price=300), Item(price=450)]) == 750
```

**Counterpoint.** "Recomputing keeps the test short." It also repeats the bug. Use a literal from the spec or a worked example.
