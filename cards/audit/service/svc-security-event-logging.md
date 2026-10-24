---
id: svc-security-event-logging
level: service
tags: [security, logging]
severity: should-fix
status: draft
lang: core
applies_when: The service authenticates users, enforces access control or accepts untrusted input.
tool_gate: Test that a failed login and a 403 each produce a structured log line; log-redaction tests.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures
---

**Rule.** Log authentication failures, authorization denials and validation failures with who, what, when and a correlation ID, and never log secrets.

**Why.** Without these events, an attack in progress is invisible and an incident cannot be reconstructed. Passwords, tokens and session IDs in logs create a second leak. Untrusted values with CR or LF can forge log lines, so encode them or use structured output. [[svc-request-id-logging]] covers the ID.

**FAIL**

```text
except AuthError: return 401                             # nothing logged
log.info("login %s %s", username, password)
log.info("user said: " + comment)                       # raw CRLF
```

**PASS**

```text
except AuthError: log.warning("auth_failed", user=uid, ip=ip, req=req_id); return 401
log.info("comment", text=comment)                       # structured, newlines escaped
```

**Counterpoint.** "Logging every denial is noisy." Log them as one event type with a counter and alert on rate, not on each line. The sparse log is the one that misses the breach.
