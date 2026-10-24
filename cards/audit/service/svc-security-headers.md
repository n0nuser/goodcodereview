---
id: svc-security-headers
level: service
tags: [security, http, headers]
severity: should-fix
status: draft
lang: core
applies_when: The service serves HTML pages or sets cookies for browsers.
tool_gate: Header check in CI against a staging URL; framework middleware that sets defaults.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
  - https://top10.owasp.org/2025/A04_2025-Cryptographic_Failures
  - https://infosec.mozilla.org/guidelines/web_security
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors
  - https://www.rfc-editor.org/rfc/rfc6797.html
---

**Rule.** Send `Strict-Transport-Security`, `X-Content-Type-Options: nosniff` and a CSP `frame-ancestors` (or `X-Frame-Options: DENY`) on every page response.

**Why.** Without HSTS a first plain-HTTP request can be downgraded. Without `nosniff` a browser may run an upload as script. Without a framing rule a hostile page can overlay yours (clickjacking). Each header is one line of config and fails visibly.

**FAIL**

```text
HTTP/1.1 200 OK
Content-Type: text/html
(no security headers)
```

**PASS**

```text
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
Content-Security-Policy: frame-ancestors 'none'
```

**Counterpoint.** "HSTS can lock users out if the certificate lapses." True, so ramp `max-age` up and check the preload rules before submitting. A lockout from an expired certificate is an outage you fix, while a downgrade is a breach.
