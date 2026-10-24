---
id: svc-api-retry-after
level: service
tags: [api, http, resilience]
severity: should-fix
status: draft
note: the draft rate-limit header fields are not required here; RFC 6585 on 429 was not fetched
lang: core
applies_when: A service answers 429 or 503 to HTTP callers.
tool_gate: Integration test that forces a 429 and a 503 and asserts a `Retry-After` header.
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc9110.html
  - https://opensource.zalando.com/restful-api-guidelines/
  - https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/
---

**Rule.** Send `Retry-After` on every 429 and 503, and set it no earlier than the time capacity returns.

**Why.** Without it, every client invents its own backoff, and a hundred of them retry in the same second. The header lets the server pace its own recovery.

**FAIL**

```text
HTTP/1.1 429 Too Many Requests

{"error": "slow down"}
```

**PASS**

```text
HTTP/1.1 429 Too Many Requests
Retry-After: 30
Content-Type: application/problem+json
```

**Counterpoint.** "Clients should use exponential backoff anyway." They should, and [[svc-retry-policy]] says so. A server hint narrows the guess; it does not replace the client's cap. The IETF `RateLimit` header fields are still an Internet-Draft, so the card requires only `Retry-After`, which is in the HTTP standard. The quota itself is [[svc-rate-limit-quota]].
