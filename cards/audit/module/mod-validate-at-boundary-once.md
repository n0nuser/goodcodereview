---
id: mod-validate-at-boundary-once
level: module
tags: [correctness, maintainability, validation, design]
severity: should-fix
status: draft
lacks: failable, nobody backs "once"; without it the FAIL, hand-rolled checks in the handler, would pass
lang: core
applies_when: Input checks appear in more than one layer, or hand-rolled checks appear on a dict.
tool_gate: none
borrowed_from:
  - https://shopify.engineering/managing-pii-shopify-scale
  - https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf
  - https://www.uber.com/blog/scaling-verify-wallet/
  - https://blog.cloudflare.com/18-november-2025-outage/
note: from the author's own Python review guide; Shopify, Netflix, Uber and Cloudflare back validating at the boundary, but nobody backs 'once', and only Shopify uses a schema
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
