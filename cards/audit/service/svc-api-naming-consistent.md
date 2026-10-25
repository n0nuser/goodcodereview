---
id: svc-api-naming-consistent
level: service
tags: [maintainability, api, naming]
severity: discuss
status: draft
lacks: orgs, Zalando and Microsoft back it, and they disagree on casing; needs a third org that asks for consistency
note: Zalando and Microsoft disagree on the convention, so the card checks consistency, not the choice
lang: core
applies_when: A service defines JSON fields, query parameters, headers or path segments for an HTTP API.
tool_gate: Spec linter with a casing rule per location.
borrowed_from:
  - https://opensource.zalando.com/restful-api-guidelines/
  - https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md
---

**Rule.** Use one casing convention per location (fields, query parameters, headers, paths) across the whole API, and state it in the API guide.

**Why.** Mixed casing in one API makes callers look up each name. A client that guesses `orderId` after meeting `order_id` gets a silent null.

**FAIL**

```text
GET /orders?pageSize=20 -> {"order_id": 1, "createdAt": "...", "Total-Cents": 500}
```

**PASS**

```text
GET /orders?page_size=20 -> {"order_id": 1, "created_at": "...", "total_cents": 500}
# snake_case everywhere, as docs/api-guide.md says
```

**Counterpoint.** "Pick the right convention." The sources disagree: Zalando asks for snake_case, Microsoft for camelCase in fields. Either passes. Do not change an existing API's casing to match a guide; that is a breaking change.
