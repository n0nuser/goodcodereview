---
id: sys-secrets-and-errors
level: system
tags: [security, secrets, errors]
severity: block
status: draft
lang: core
applies_when: The code handles credentials, logs data, or returns errors to clients.
tool_gate: Secret scanner in CI; log-redaction tests.
borrowed_from:
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md
  - https://owasp.org/Top10/2025/
---

**Rule.** Keep secrets out of source, logs and error responses, and fail closed: an exception must never turn into allowed access.

**Why.** Stack traces, SQL and tokens in responses or logs leak; a catch-and-continue around a validation step grants access when the check crashes (OWASP A10:2025, ASVS V16).

**FAIL**

```text
return {"error": traceback.format_exc()}
try: check_token(t) except: pass   # continues as authorized
API_KEY = "sk_live_..."
```

**PASS**

```text
return {"error": "internal", "id": err_id}   # details to logs, redacted
try: check_token(t) except: deny()
API_KEY = env["API_KEY"]
```

**Counterpoint.** "We need detail to debug." Log it server-side with a correlation id. Secret storage specifics (vaults, rotation) are not in the researched ASVS section V16, so this card covers the error and log side from sources and the in-source-secret side first-hand.
