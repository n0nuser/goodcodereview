---
id: py-field-only-when-adds
level: module
tags: [python, pydantic]
severity: discuss
status: draft
lang: python
applies_when: A pydantic model or settings class uses `Field()`.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Use `Field()` only when it adds something (a constraint, an alias, or API docs), and set plain defaults directly.

**Why.** `Field(default=5.0)` is noise that hides which fields are constrained.

**FAIL**

```python
request_timeout_s: float = Field(default=5.0)
```

**PASS**

```python
request_timeout_s: float = 5.0
max_batch_size: int = Field(default=500, gt=0, le=2_000)
```

**Counterpoint.** "Uniform `Field` everywhere is consistent." Consistency that hides the constraints is not worth the scan cost. Every `Field` should tell the reader something.
