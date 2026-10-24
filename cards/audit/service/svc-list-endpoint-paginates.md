---
id: svc-list-endpoint-paginates
level: service
tags: [performance, api]
severity: should-fix
status: draft
lang: core
applies_when: The service exposes an endpoint or RPC that returns a collection.
tool_gate: Contract test that calls the list with a huge page size and asserts the clamp or a 400.
note: 5 orgs back pagination and 4 state a server-side maximum (Zalando's maximum was not seen); a clamp or a 400 are both accepted
borrowed_from:
  - https://google.aip.dev/158
  - https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design
  - https://opensource.zalando.com/restful-api-guidelines/
  - https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api
  - https://docs.stripe.com/api/pagination
---

**Rule.** Paginate every list endpoint, with a default page size and a server-side maximum.

**Why.** A list that returns everything grows with the data until one request exhausts memory or the timeout. Adding pagination later breaks clients, so start with it. Without a maximum, a caller can ask for a page as big as the table. See [[svc-api-compat-pagination]] for compatibility and [[svc-bound-client-controlled-sizes]] for the security cap.

**FAIL**

```text
GET /orders          -> every order the user ever placed
GET /orders?limit=1000000   (server honours it)
```

**PASS**

```text
GET /orders?page_size=50&page_token=abc   (default 25, values above 100 clamped to 100)
response: { "items": [...], "next_page_token": "def" }
```

**Counterpoint.** "This list is always small." Say so with a bounded type or a documented limit, since data tends to outgrow its first estimate. Cursors cost more than offsets to build, but they stay stable while rows change.
