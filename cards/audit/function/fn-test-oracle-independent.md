---
id: fn-test-oracle-independent
level: function
tags: [correctness, testing, tests]
severity: should-fix
status: draft
lang: core
applies_when: A test asserts on a computed value or asserts that something was not called.
tool_gate: Mutation testing.
note: one vendor's engineering guidance (opinion), from pstack principle-test-behavior-not-implementation
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-test-behavior-not-implementation/SKILL.md
---

**Rule.** Take a test's expected value from the requirement, not from the code under test, and pair every "not called" assertion with a case where the call happens.

**Why.** An expected value computed by the code under test passes when the code is wrong. A "not called" assertion passes when the spy is wired to the wrong target, so it proves nothing until a case shows it can see the call.

**FAIL**

```python
assert total(items) == sum(i.price for i in items)   # re-implements the code
mailer.send.assert_not_called()                      # no case where it is called
```

**PASS**

```python
assert total([Item(price=300), Item(price=450)]) == 750
assert_not_called_when(free_plan); assert_called_when(paid_plan)
```

**Counterpoint.** "Recomputing keeps the test short." It also repeats the bug. Use a literal from the spec or a worked example. See [[chg-agent-mock-asserting-tests]] for tests that only check their own mocks.
