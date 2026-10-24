---
id: py-no-cast
level: function
tags: [correctness, python, types]
severity: should-fix
status: draft
lang: python
applies_when: Code calls `typing.cast(...)`.
tool_gate: ruff TID251 (banned-api)
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Do not use `cast()`; parse the boundary into a typed model, or narrow with `isinstance`.

**Why.** `cast` is a promise to the type checker that nothing verifies at runtime. When the promise is wrong, the type checker's output is a lie that spreads.

**FAIL**

```python
data = cast(dict[str, int], json.loads(raw))
```

**PASS**

```python
class Payload(BaseModel):
    counts: dict[str, int]
data = Payload.model_validate_json(raw)
```

**Counterpoint.** "Sometimes the checker is wrong." Then fix the stub or narrow with `isinstance` or `assert`, which check at runtime. A justified `type: ignore[code]` with a reason is more honest than a cast, because it stays visible.
