---
id: svc-api-problem-json
level: service
tags: [compatibility, api, errors]
severity: should-fix
status: draft
lang: core
applies_when: A service returns errors from an HTTP API to other services or to clients.
tool_gate: Middleware that builds every error body from one problem-details type; a test that fails on an error response without the media type.
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc9457.html
  - https://opensource.zalando.com/restful-api-guidelines/
---

**Rule.** Return errors as `application/problem+json` with a `status` that equals the HTTP status, and leave stack traces and internal detail out.

**Why.** Callers then parse every error one way. A body that differs per endpoint, or a `status` that disagrees with the real code, makes generic client and proxy handling unreliable. A stack trace in `detail` hands an attacker the implementation.

**FAIL**

```text
HTTP/1.1 500
Content-Type: text/html

<pre>NullPointerException at OrderRepo.java:88 ...</pre>
```

**PASS**

```text
HTTP/1.1 404
Content-Type: application/problem+json

{"type": "https://api.example.com/problems/order-not-found",
 "title": "Order not found", "status": 404,
 "detail": "No order with id 7731 for this account."}
```

**Counterpoint.** "We already have our own error envelope." That is fine inside one team's API, if it is one envelope and documented. The card asks for one shape everywhere; problem details is the one with a registered media type and existing client support. See [[sys-secrets-and-errors]] for what must stay out of any error.
