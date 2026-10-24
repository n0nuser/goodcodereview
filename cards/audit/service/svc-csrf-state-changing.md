---
id: svc-csrf-state-changing
level: service
tags: [security, csrf, sessions]
severity: block
status: draft
lang: core
applies_when: The service authenticates browsers with cookies and changes state on requests.
tool_gate: Framework CSRF middleware enabled; test that a POST without the token returns 403.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
---

**Rule.** Require a CSRF token (or an equivalent header check) on every cookie-authenticated request that changes state, and never change state on GET.

**Why.** The browser attaches cookies to a cross-site request, so a hostile page can post as the user. `SameSite` helps but `Lax` still sends cookies on cross-site top-level GET, so it supports the token and does not replace it. Naive double-submit cookies fail when a sibling subdomain can set cookies.

**FAIL**

```text
@app.get("/account/delete")                    # state change on GET
@app.post("/transfer")                         # cookie auth, no token check
```

**PASS**

```text
@app.post("/transfer")
@csrf_protect                                  # token bound to the session
Set-Cookie: sid=...; SameSite=Lax; Secure; HttpOnly
```

**Counterpoint.** "Our API uses JSON, so browsers cannot forge it." A simple content type such as `text/plain` can carry a JSON body without a preflight. Reject it, or require a custom header such as `X-CSRF-Token`. Pure bearer-token APIs with no cookies are exempt.
