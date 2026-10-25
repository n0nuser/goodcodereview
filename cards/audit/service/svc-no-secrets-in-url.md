---
id: svc-no-secrets-in-url
level: service
tags: [security, secrets, http]
severity: should-fix
status: stable
lang: core
applies_when: A client or server puts an API key, session token, bearer token, password, or personal data into a URL.
tool_gate: none
note: ASVS 14.2.1; a log check that rejects query keys such as `token`, `key` or `password` in access logs is the nearest gate; sys-pii-minimise-retention and code-secret-scan cover other leak paths
borrowed_from:
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x23-V14-Data-Protection.md
  - https://www.rfc-editor.org/rfc/rfc6750.html
  - https://cwe.mitre.org/data/definitions/598.html
  - https://developer.mozilla.org/en-US/docs/Web/Security/Referer_header:_privacy_and_security_concerns
---

**Rule.** Send tokens, keys, passwords, and personal data in a header or the request body, never in the path or query string.

**Why.** A URL is copied to places nobody reviews: proxy and access logs, browser history, the `Referer` header sent to third-party scripts and images, and links pasted into chat. A token there stays readable long after the request ends. The `Authorization` header and a POST body skip all of those copies.

**FAIL**

```text
GET /api/orders?api_key=sk_live_abc123
GET /reset?email=ana@example.com&token=9f2c
```

**PASS**

```text
GET /api/orders
Authorization: Bearer sk_live_abc123

POST /reset
Content-Type: application/json

{"token": "9f2c"}
```

**Counterpoint.** "Email links have to carry the token in the URL." Make that token single-use and short-lived, have the landing page swap it for a session at once, and send `Referrer-Policy: no-referrer` on that page. A long-lived API key has no such excuse.
