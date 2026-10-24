---
id: mod-validate-at-boundary-once
level: module
tags: [correctness, maintainability, validation, design]
severity: should-fix
status: draft
lang: core
applies_when: Input checks appear in more than one layer, or hand-rolled checks appear on a dict.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Validate at the boundary, once, with a schema or model, so that inner layers receive typed, already-valid data.

**Why.** The same check copied into three layers drifts until nobody knows which one is authoritative.

**FAIL**

```text
def create_order(body: dict):
    if not body.get("items"): raise ...
    if body.get("currency") not in {"EUR", "USD"}: raise ...
```

**PASS**

```text
class CreateOrder(Schema):
    items: list[Item]  # min 1
    currency: Currency # enum, unknown fails at parse
```

**Counterpoint.** "Defence in depth means validating everywhere." At trust boundaries, yes: every external input. Inside, repeated validation hides who owns the rule. Use types to carry "already valid" inward.
