---
id: py-pydantic-validation
level: module
tags: [correctness, python, validation]
severity: should-fix
status: draft
lang: python
applies_when: A Python function validates request or config data by hand.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Validate request data with a pydantic model, not hand-written checks.

**Why.** Core rule: [[mod-validate-at-boundary-once]]. Fields stay `snake_case` in Python. For camelCase JSON, use an alias generator and dump by alias.

**FAIL**

```python
def create_order(body: dict):
    if body.get("currency") not in {"EUR", "USD"}:
        raise ValueError("bad currency")
```

**PASS**

```python
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

class CreateOrder(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    items: list[LineItemIn] = Field(min_length=1)
    currency: Currency          # StrEnum: unknown values fail at parse

body = CreateOrder.model_validate(payload)
body.model_dump(by_alias=True)
```

**Counterpoint.** "Validators hide logic." They put it next to the field it protects. Hand-rolled checks are where drift starts.
