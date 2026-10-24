---
id: svc-security-event-logging
level: service
tags: [security, observability, logging]
severity: should-fix
status: draft
lang: core
applies_when: The service authenticates users.
tool_gate: Test that a failed login produces one structured log line with the account and a timestamp.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures
  - https://learn.microsoft.com/en-us/azure/well-architected/security/monitor-threats
  - https://google.github.io/building-secure-and-reliable-systems/raw/ch15.html
  - https://www.ncsc.gov.uk/guidance/introduction-logging-security-purposes
---

**Rule.** Log every failed authentication with the account name and a timestamp.

**Why.** Without these events, password guessing in progress is invisible and an incident cannot be reconstructed. Log authorization denials and validation failures the same way, and add a correlation ID so one request can be followed across services. Never log passwords, tokens or session IDs, because the log then becomes a second leak. Untrusted values with CR or LF can forge log lines, so use structured output.

**FAIL**

```python
except AuthError:
    return 401                                   # nothing logged
```

**PASS**

```python
except AuthError:
    log.warning("auth_failed", account=username, ip=ip, at=utc_now(), req=req_id)
    return 401
```

**Counterpoint.** "Logging every failed login is noisy." Log them as one event type, count them, and alert on the rate, not on each line. Without the events, nobody sees the attack.
