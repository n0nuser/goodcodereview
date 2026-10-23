---
id: svc-api-compat-pagination
level: service
tags: [api, compatibility]
severity: should-fix
status: draft
lang: core
applies_when: A public or cross-team API response or request schema changes, or a list endpoint is added.
tool_gate: Schema diff check (e.g. OpenAPI breaking-change linter) in CI.
borrowed_from: []
---

**Rule.** Changes to an API must be backward compatible for existing callers (add, never rename, remove or retype), and list endpoints must be paginated with a cursor.

**Why.** Callers deploy on their own schedule; a removed field breaks them without warning. An unpaginated list grows until one request exhausts memory or the timeout.

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

**Counterpoint.** "Internal API, we control every caller." Then say how the change is released in lockstep; otherwise the rolling deploy itself runs two versions at once. No source in docs/research covers this card; it is first-hand reasoning and stays draft until sourced.
