---
id: svc-cors-allowlist
level: service
tags: [security, cors, http]
severity: should-fix
status: draft
lang: core
applies_when: The service sends `Access-Control-Allow-Origin` or similar CORS headers.
tool_gate: Integration test that sends a hostile `Origin` and asserts it is not echoed.
note: the fetched OWASP page does not cover the null origin or `*` with credentials, so the card leaves them out
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
---

**Rule.** Allow cross-origin access only to a fixed list of named origins, and never echo the request `Origin` header back unchecked.

**Why.** Reflecting any Origin, or allowing `*` on an endpoint that returns private data, lets a hostile page read responses. CORS also does not stop CSRF, so it is no substitute for [[svc-csrf-state-changing]]. A subdomain regex that matches `evil-example.com` is the same bug.

**FAIL**

```text
resp.headers["Access-Control-Allow-Origin"] = request.headers["Origin"]
resp.headers["Access-Control-Allow-Credentials"] = "true"
```

**PASS**

```text
ALLOWED = {"https://app.example.com"}
if request.headers.get("Origin") in ALLOWED:
    resp.headers["Access-Control-Allow-Origin"] = request.headers["Origin"]
```

**Counterpoint.** "`*` is fine for a public API." It is, for endpoints that return only public data and take no credentials. Keep it off any endpoint behind a login.
