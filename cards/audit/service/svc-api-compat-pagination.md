---
id: svc-api-compat-pagination
level: service
tags: [api, compatibility]
severity: should-fix
status: draft
note: no source yet; first-hand reasoning
lang: core
applies_when: A public or cross-team API response or request schema changes, or a list endpoint is added.
tool_gate: Schema diff check (e.g. OpenAPI breaking-change linter) in CI.
borrowed_from: []
---

**Rule.** Change an API only in backward-compatible ways: add fields, and never rename, remove, or retype them.

**Why.** Callers deploy on their own schedule, and a removed field breaks them without warning. Likewise, paginate every list endpoint with a cursor: an unpaginated list grows until one request exhausts memory or the timeout.

**FAIL**

```text
GET /orders -> [ ...all rows... ]
response: rename "total" to "amount_total" in place
```

**PASS**

```text
GET /orders?limit=100&cursor=abc -> {items, next_cursor}
response: add "amount_total", keep "total", mark it deprecated
```

**Counterpoint.** "Internal API, we control every caller." Then say how the change is released in lockstep. Otherwise the rolling deploy itself runs two versions at once.
