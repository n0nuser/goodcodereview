---
id: sys-secrets-and-errors
level: system
tags: [security, secrets, errors]
severity: block
status: draft
note: ASVS V16 covers errors/logging only; the secrets-in-source side is first-hand. Fail-closed exception to [[fn-specific-exceptions-only]] lives here
lang: core
applies_when: The code handles credentials, logs data, or returns errors to clients.
tool_gate: Secret scanner in CI; log-redaction tests.
borrowed_from:
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md
  - https://owasp.org/Top10/2025/
---

**Rule.** Fail closed: a validation or auth error must deny, never continue.

**Why.** Also keep secrets out of source, logs and error responses. Stack traces, SQL and tokens in responses or logs leak; a catch-and-continue around a validation step grants access when the check crashes (OWASP A10:2025, ASVS V16).

**FAIL**

```text
return {"error": traceback.format_exc()}
try: check_token(t)
except Exception: pass            # continues as authorized
API_KEY = "sk_live_..."
```

**PASS**

```text
return {"error": "internal", "id": err_id}   # details to logs, redacted
try: check_token(t)
except Exception as err:
    log.warning("auth failed: %s", redact(err)); deny()
API_KEY = env["API_KEY"]
```

**Counterpoint.** "A broad `except Exception` breaks the specific-exceptions rule." At a security boundary, [[fn-specific-exceptions-only]] yields to fail-closed: catch broadly, log redacted, deny, and never use a bare `except:`. "We need detail to debug." Log it server-side with a correlation id.
