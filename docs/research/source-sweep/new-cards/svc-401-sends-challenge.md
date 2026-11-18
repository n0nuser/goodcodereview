---
id: svc-401-sends-challenge
level: service
tags: [compatibility, correctness, http]
severity: should-fix
status: draft
lacks: orgs, one org (IETF); the Siemens guideline restates RFC 9110, so it adds none; needs two more orgs that require the challenge
lang: core
applies_when: A service answers a request that lacks valid credentials for a protected resource.
context: [server]
tool_gate: Integration test that asserts a `WWW-Authenticate` header on every 401 response.
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc6750.html
---

**Rule.** Send a `WWW-Authenticate` challenge with every 401 response.

**Why.** A 401 says the request had no valid credentials. The challenge tells the client which scheme to use. Without it, generic HTTP clients and proxies cannot start an authentication flow, and the response breaks the HTTP contract.

**FAIL**

```text
GET /v1/orders
-> 401 Unauthorized
   Content-Type: application/json
   {"error": "unauthenticated"}
```

**PASS**

```text
GET /v1/orders
-> 401 Unauthorized
   WWW-Authenticate: Bearer realm="api"
   Content-Type: application/problem+json
```

**Counterpoint.** "Our clients already know the scheme, so the header is noise." The header costs one line, and any intermediary or new client reads it. If the scheme is a custom one, name it in the challenge. If a challenge would be wrong, the status is probably wrong: use 403 for an authenticated caller who lacks permission.
