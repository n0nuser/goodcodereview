---
id: py-strenum-not-strings
level: function
tags: [python, types]
severity: should-fix
status: draft
lang: python
applies_when: Python code compares against or returns string literals for a fixed set of values.
tool_gate: ruff PLR2004 (partial)
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Use `StrEnum` (Python 3.11+) for fixed string sets and `HTTPStatus` for HTTP codes. Core rules: [[fn-no-magic-values]], [[fn-no-stringly-typed-returns]].

**Why.** `StrEnum` members are still strings (JSON-ready, comparable) but mistakes fail at the type checker.

**FAIL**

```python
def check(order) -> str:
    return "missing_items" if not order.lines else "ok"
if resp.status_code == 404: ...
```

**PASS**

```python
class OrderCheck(StrEnum):
    OK = "ok"
    MISSING_ITEMS = "missing_items"
if resp.status_code == HTTPStatus.NOT_FOUND: ...
```

**Counterpoint.** "Enum import is heavy for two values." It is one class and the type checker then protects every caller. In pydantic models, an enum field also rejects unknown values at parse.
