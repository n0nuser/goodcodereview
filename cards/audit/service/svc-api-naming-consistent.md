---
id: svc-api-naming-consistent
level: service
tags: [maintainability, api, naming]
severity: discuss
status: stable
note: Zalando and Microsoft disagree on the convention, so the card checks consistency, not the choice
lang: core
applies_when: A service defines JSON fields, query parameters, headers or path segments for an HTTP API.
context: [server]
tool_gate: Spec linter with a casing rule per location.
borrowed_from:
  - https://opensource.zalando.com/restful-api-guidelines/
  - https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md
  - https://google.aip.dev/140
  - https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md
  - https://github.com/island-is/handbook/blob/master/docs/api-design-guide/naming-conventions.md
  - https://github.com/microsoft/api-guidelines/blob/vNext/azure/ConsiderationsForServiceDesign.md
---

**Rule.** Use one casing convention per location (fields, query parameters, headers, paths) across the whole API, and state it in the API guide. Name collections and array fields as plural nouns.

**Why.** Mixed casing in one API makes callers look up each name. A client that guesses `orderId` after meeting `order_id` gets a silent null. The same goes for number: a field named `item` that holds a list reads as one value, so name collections and array fields in the plural.

**FAIL**

```text
GET /orders?pageSize=20 -> {"order_id": 1, "createdAt": "...", "Total-Cents": 500, "item": [...]}
```

**PASS**

```text
GET /orders?page_size=20 -> {"order_id": 1, "created_at": "...", "total_cents": 500, "items": [...]}
# snake_case everywhere, as docs/api-guide.md says
```

**Counterpoint.** "Pick the right convention." Published guides disagree: some ask for snake_case, others for camelCase in fields. Either passes. Do not change an existing API's casing to match a guide; that is a breaking change.
