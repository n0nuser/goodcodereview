---
id: sys-secrets-and-errors
level: system
tags: [security, correctness, secrets, errors]
severity: block
status: stable
note: Fail closed is backed by OWASP, MITRE (CWE-636 and CWE-209) and Microsoft, whose page states it only for certificate-validation errors. RFC 9457 backs the no-internals half. Secrets in source rest on 12factor and OWASP only, so they stay in the Why
lang: core
applies_when: The code handles credentials, logs data, or returns errors to clients.
tool_gate: Secret scanner in CI; log-redaction tests.
borrowed_from:
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md
  - https://owasp.org/Top10/2025/
  - https://cwe.mitre.org/data/definitions/636.html
  - https://cwe.mitre.org/data/definitions/209.html
  - https://12factor.net/config
  - https://web.mit.edu/Saltzer/www/publications/protection/Basic.html
  - https://www.rfc-editor.org/rfc/rfc9457.html
  - https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/security
---

**Rule.** Fail closed: a validation or auth error must deny, never continue, and an error response must not carry internals such as stack traces, SQL or tokens.

**Why.** A catch-and-continue around a validation step grants access when the check crashes. Stack traces and SQL in a response show an attacker how the system is built, and a token there can be reused. Keep secrets out of source and logs too: read them from the environment or a secrets manager.

**FAIL**

```text
return {"error": traceback.format_exc()}
try: check_token(t)
except Exception: pass            # continues as authorized
```

**PASS**

```text
return {"error": "internal", "id": err_id}   # details to logs, redacted
try: check_token(t)
except Exception as err:
    log.warning("auth failed: %s", redact(err)); deny()
```

**Counterpoint.** "A broad `except Exception` breaks the specific-exceptions rule." At a security boundary, fail-closed wins: catch broadly, log redacted, deny, and never use a bare `except:`. "We need detail to debug." Log it server-side with a correlation id.
