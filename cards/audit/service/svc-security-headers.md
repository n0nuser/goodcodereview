---
id: svc-security-headers
level: service
tags: [security, http, headers]
severity: should-fix
status: stable
lang: core
applies_when: The service serves HTML pages or sets cookies for browsers over HTTPS.
tool_gate: Header check in CI against a staging URL; framework middleware that sets defaults.
note: the Rule covers HSTS only; nosniff and frame-ancestors each have two orgs (OWASP, Mozilla), so they sit in Why
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
  - https://top10.owasp.org/2025/A04_2025-Cryptographic_Failures
  - https://infosec.mozilla.org/guidelines/web_security
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors
  - https://www.rfc-editor.org/rfc/rfc6797.html
---

**Rule.** Send `Strict-Transport-Security` on every HTTPS response.

**Why.** Without HSTS, the first plain-HTTP request can be downgraded by anyone on the path, and a user can click through a certificate warning. With it, the browser rewrites `http` to `https` and refuses the click-through. Two more one-line headers belong next to it: `X-Content-Type-Options: nosniff`, so a browser does not run an upload as script, and CSP `frame-ancestors` (or `X-Frame-Options: DENY`), so a hostile page cannot frame yours for clickjacking.

**FAIL**

```text
HTTP/1.1 200 OK
Content-Type: text/html
(no Strict-Transport-Security)
```

**PASS**

```text
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
Content-Security-Policy: frame-ancestors 'none'
```

**Counterpoint.** "HSTS can lock users out if the certificate lapses." True, so ramp `max-age` up and check the preload rules before you submit the domain. A lockout from an expired certificate is an outage you fix, while a downgrade is a breach.
