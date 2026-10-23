---
id: svc-sqli-authn
level: service
tags: [security, injection]
severity: block
status: draft
lang: core
applies_when: The code builds a query or command from request data, or exposes an endpoint.
tool_gate: SAST rule for string-built SQL; authn middleware as default-deny.
borrowed_from:
  - https://owasp.org/Top10/2025/
---

**Rule.** Pass untrusted data to queries and commands as bound parameters, and require authentication and authorization on every endpoint by default.

**Why.** Concatenated input is injection (OWASP A05:2025); endpoints that must opt in to checks eventually miss one (A01 broken access control, A07 authentication failures).

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

**Counterpoint.** "An ORM makes this moot." Raw fragments and dynamic column or order-by names still bypass it. Note: the research read only the OWASP Top 10 list pages for these categories, not detailed prevention text, so this card stays draft until a primary source is added.
