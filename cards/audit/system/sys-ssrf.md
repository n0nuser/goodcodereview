---
id: sys-ssrf
level: system
tags: [security, ssrf]
severity: block
status: draft
note: sources thin: only the OWASP Top 10:2025 index; mitigations are first-hand
lang: core
applies_when: The server fetches a URL that a user or external data supplies.
tool_gate: Egress firewall or proxy allowlist.
borrowed_from:
  - https://owasp.org/Top10/2025/
---

**Rule.** Fetch user-supplied URLs only after checking the resolved address against an allowlist.

**Why.** The server can reach networks that the attacker cannot, and an open fetch lets the attacker read internal services. Block internal and metadata addresses and disable redirects. OWASP 2025 folds SSRF into A01 Broken Access Control.

**FAIL**

```text
requests.get(request.args["url"])
```

**PASS**

```text
host = resolve(url); require host in ALLOWED and not is_private(ip); no redirects
```

**Counterpoint.** "Blocklisting private ranges is enough." Redirects and DNS rebinding bypass checks done before the request. Check the resolved address you actually connect to.
