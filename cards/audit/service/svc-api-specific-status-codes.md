---
id: svc-api-specific-status-codes
level: service
tags: [compatibility, api, http]
severity: should-fix
status: draft
lacks: orgs, IETF and Zalando back it; needs a third org
note: RFC 9110 sections 9.3.4, 10.2.1 and 15.3.2; section 15.5.6 on 405 was not read
lang: core
applies_when: A service returns HTTP responses that callers or intermediaries interpret by status code.
tool_gate: Integration tests asserting status and headers per operation; a spec linter for 201 and 405 responses.
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc9110.html
  - https://opensource.zalando.com/restful-api-guidelines/
---

**Rule.** Return the most specific status code that fits: 201 with `Location` for a create, 405 with `Allow` for a wrong method, and a 4xx or 5xx for any failure.

**Why.** Clients, proxies and monitors act on the status line. A 200 with an error in the body hides failures from retries, caches and error-rate alerts. A create that returns 200 without `Location` forces the caller to guess the new URL.

**FAIL**

```text
POST /orders -> 200 {"error": "out of stock"}
PATCH /orders (route is read-only) -> 404, no Allow header
```

**PASS**

```text
POST /orders -> 201  Location: /orders/9031
POST /orders (out of stock) -> 409 application/problem+json
PATCH /orders (not supported) -> 405  Allow: GET, POST
```

**Counterpoint.** "A 200 with a status field is easier for our clients." It breaks every generic tool that reads the status line, including your own dashboards. Choosing between two fitting codes is a style call; the card fails only a code that says the wrong thing.
