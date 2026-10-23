---
id: sys-ssrf
level: system
tags: [security, ssrf]
severity: block
status: draft
lang: core
applies_when: The server fetches a URL that a user or external data supplies.
tool_gate: Egress firewall or proxy allowlist.
borrowed_from:
  - https://owasp.org/Top10/2025/
---

**Rule.** Validate user-supplied URLs against an allowlist of hosts and block internal and metadata addresses, after DNS resolution.

**Why.** The server can reach networks the attacker cannot; an open fetch lets them read internal services. OWASP 2025 folds SSRF into A01 Broken Access Control.

**FAIL**

```text
requests.get(request.args["url"])
```

**PASS**

```text
host = resolve(url); require host in ALLOWED and not is_private(ip); no redirects
```

**Counterpoint.** "Blocklisting private ranges is enough." Redirects and DNS rebinding bypass checks done before the request; check the resolved address you actually connect to. The notes cite only the Top 10 index for SSRF, so detailed mitigations here are first-hand and the card is draft.
