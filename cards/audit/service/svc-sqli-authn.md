---
id: svc-sqli-authn
level: service
tags: [security, injection]
severity: block
status: draft
note: sources thin: only the OWASP Top 10:2025 index was read; add detailed prevention source before stable
lang: core
applies_when: The code builds a query or command from request data, or exposes an endpoint.
tool_gate: SAST rule for string-built SQL; authn middleware as default-deny.
borrowed_from:
  - https://owasp.org/Top10/2025/
---

**Rule.** Pass untrusted data to queries as bound parameters, never by string concatenation.

**Why.** Concatenated input is injection (OWASP A05:2025). Related: endpoints should be authenticated and authorized by default, since opt-in checks eventually miss one (A01, A07).

**FAIL**

```text
db.execute("SELECT * FROM users WHERE id = " + req.id)
@route("/admin/export")           # no auth decorator
```

**PASS**

```text
db.execute("SELECT * FROM users WHERE id = %s", (req.id,))
router.default_deny(); @route("/admin/export") @require_role("admin")
```

**Counterpoint.** "An ORM makes this moot." Raw fragments and dynamic column or order-by names still bypass it.
