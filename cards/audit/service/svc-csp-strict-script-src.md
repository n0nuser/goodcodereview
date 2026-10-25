---
id: svc-csp-strict-script-src
level: service
tags: [security, http, headers, xss]
severity: should-fix
status: draft
lacks: evidence, OWASP, Mozilla and Google are listed, but no stable pass has read them; the nonce or hash form is stricter than the ASVS minimum
lang: core
applies_when: The service serves HTML pages to browsers.
tool_gate: Google CSP Evaluator on the policy; a CI header check against a staging URL.
note: follows OWASP, MDN and web.dev, which are stricter than the ASVS 3.4.3 minimum (that minimum still allows a host allowlist); svc-security-headers covers frame-ancestors; fn-no-raw-html-sink is the first defence against XSS and CSP is the second
borrowed_from:
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x12-V3-Web-Frontend-Security.md
  - https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
  - https://web.dev/articles/strict-csp
---

**Rule.** Send a `Content-Security-Policy` whose `script-src` uses a per-response nonce or script hashes, with `object-src 'none'` and `base-uri 'none'`.

**Why.** When an XSS bug slips through, CSP decides whether the injected script runs. A host allowlist such as `script-src 'self' cdn.example` usually has a bypass, because some allowed host serves JSONP or an old library. A nonce or hash only lets through scripts the server marked. `'strict-dynamic'` lets those scripts load their own children. Browsers that support nonces ignore an `'unsafe-inline'` fallback placed next to one, so that fallback is safe. `'unsafe-inline'` on its own turns the policy off for inline script.

**FAIL**

```text
Content-Security-Policy: script-src 'self' 'unsafe-inline' https://cdn.example.com
```

**PASS**

```text
Content-Security-Policy: script-src 'nonce-r4nd0m' 'strict-dynamic'; object-src 'none'; base-uri 'none'
<script nonce="r4nd0m" src="/app.js"></script>
```

**Counterpoint.** "A strict CSP breaks inline handlers and third-party tags." It does at first, so roll it out with `Content-Security-Policy-Report-Only`, move `onclick=` attributes into script files, and switch to enforce when the reports go quiet. A policy that never leaves report-only protects nothing, so give that step a date.
