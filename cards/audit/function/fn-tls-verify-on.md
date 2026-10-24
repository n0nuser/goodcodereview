---
id: fn-tls-verify-on
level: function
tags: [security, tls, network]
severity: block
status: draft
lang: core
applies_when: Code makes an outbound HTTPS, database or message-broker connection.
tool_gate: SAST rules for `verify=False`, `rejectUnauthorized: false`, `InsecureSkipVerify`.
note: the TLS cheat sheet does not forbid disabling verification outright; the rule rests on the Top 10 A04 checklist item to validate certificates
borrowed_from:
  - https://top10.owasp.org/2025/A04_2025-Cryptographic_Failures
  - https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html
  - https://www.rfc-editor.org/rfc/rfc9525.html
  - https://pkg.go.dev/crypto/tls#Config
  - https://codeql.github.com/codeql-query-help/python/py-request-without-cert-validation/
  - https://docs.python.org/3/library/ssl.html
---

**Rule.** Leave certificate and hostname verification on in every environment that ships.

**Why.** With verification off, any on-path attacker presents a certificate and reads or changes the traffic. The flag is usually added to silence a dev-box error and then ships. Fix the trust store or pin a private CA instead.

**FAIL**

```python
requests.get(url, verify=False)
https.request({ rejectUnauthorized: false })
```

**PASS**

```python
requests.get(url, verify="/etc/ssl/company-ca.pem")   # private CA added, check stays on
```

**Counterpoint.** "It is an internal network." Internal links get sniffed after one compromised host. A private CA gives you the same convenience with the check intact.
