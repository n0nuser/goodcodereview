---
id: fn-distinct-types-for-ids
level: function
tags: [correctness, types]
severity: should-fix
status: draft
lang: core
applies_when: A function takes two or more arguments of one primitive type that mean different things (ids, amounts, units).
tool_gate: Type checker with a newtype or branded-type pattern.
note: one vendor's engineering guidance (opinion), from pstack principle-type-system-discipline
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-type-system-discipline/SKILL.md
---

**Rule.** Give arguments with different meanings distinct types, so a call that swaps them fails to type-check.

**Why.** Two `str` ids compile in either order. The swap passes review and fails in production, often as a "not found" that looks like missing data.

**FAIL**

```python
def refund(user_id: str, order_id: str) -> None: ...
refund(order.id, user.id)   # accepted
```

**PASS**

```python
UserId = NewType("UserId", str)
OrderId = NewType("OrderId", str)
def refund(user_id: UserId, order_id: OrderId) -> None: ...
```

**Counterpoint.** "Wrapper types add ceremony." A newtype costs one line and no runtime. Where the types differ only by argument position and the function has two arguments with obvious names, keyword-only parameters can be enough.
