---
id: fn-early-return-no-else
level: function
tags: [maintainability, readability]
severity: discuss
status: stable
lang: core
applies_when: A function checks an error or edge case, then continues with the main path.
tool_gate: Pylint no-else-return (R1705), clang-tidy readability-else-after-return.
borrowed_from:
  - https://go.dev/doc/effective_go
  - https://flink.apache.org/how-to-contribute/code-style-and-quality-common/
  - https://llvm.org/docs/CodingStandards.html
---

**Rule.** Handle the error or edge case first and return early, so the main path is not nested.

**Why.** Nesting the main path inside `if ok:` pushes the real work to the right and puts the failure case far from its check. Exiting early keeps the success path in one straight line down the page, and each failure sits next to its test. An `else` after a `return` adds a level of indentation for nothing.

**FAIL**

```python
def charge(order):
    if order.items:
        if order.card:
            return gateway.charge(order.card, order.total)
        else:
            raise NoCard(order.id)
    else:
        raise EmptyOrder(order.id)
```

**PASS**

```python
def charge(order):
    if not order.items:
        raise EmptyOrder(order.id)
    if not order.card:
        raise NoCard(order.id)
    return gateway.charge(order.card, order.total)
```

**Counterpoint.** "A single exit point is easier to reason about." That holds when the function must release something on every path. Use `try`/`finally` or a context manager for that, and return early otherwise. Two symmetric branches of equal weight can stay as `if`/`else`.
