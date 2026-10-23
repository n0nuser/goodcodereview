---
id: py-pydantic-validation
level: module
tags: [python, validation]
severity: should-fix
status: draft
lang: python
applies_when: A Python function validates request or config data by hand.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Use pydantic models and validators for validation. Fields are `snake_case`; for camelCase JSON use `alias_generator=to_camel` and `model_dump(by_alias=True)`. Core rule: [[mod-validate-at-boundary-once]].

**Why.** The model is the validation, the schema and the docs in one place.

**FAIL**

```python
if body.get("currency") not in {"EUR", "USD"}: raise ValueError
```

**PASS**

```python
class CreateOrder(BaseModel):
    items: list[LineItemIn] = Field(min_length=1)
    currency: Currency   # StrEnum
```

**Counterpoint.** "Validators hide logic." They put it next to the field it protects. Hand-rolled checks are where drift starts.
