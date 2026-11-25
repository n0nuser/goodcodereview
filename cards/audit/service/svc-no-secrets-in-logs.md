---
id: svc-no-secrets-in-logs
level: service
tags: [security, logging, secrets]
severity: should-fix
status: stable
lang: core
applies_when: A service writes application or request logs.
context: [server]
tool_gate: A redacting log filter or formatter; secret scanning over the log output of the test suite.
note: OWASP (tokens, passwords, session ids, keys and connection strings are removed, masked, hashed or encrypted before logging), MITRE CWE-532 ("do not write secrets into the log files") and GitLab ("never log credentials under any circumstance"; log the credential's internal id). AWS Prescriptive Guidance repeats the OWASP list and is not counted
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://cwe.mitre.org/data/definitions/532.html
  - https://docs.gitlab.com/development/secure_coding_guidelines/
---

**Rule.** Do not log passwords, tokens, keys or session ids; log an internal id or a masked value instead.

**Why.** Logs are copied to more places and read by more people than the secret store, and they live longer. A credential in a log line stays valid for as long as the log does. Whole header maps, request bodies and config objects are the usual leak, because nobody wrote the secret into the call on purpose.

**FAIL**

```python
logger.info("request headers: %s", dict(request.headers))   # includes Authorization and Cookie
logger.debug("loaded config: %s", config)                   # includes db_password
```

**PASS**

```python
logger.info("request received", extra={"request_id": rid, "client_id": client.id})
logger.debug("loaded config", extra={"keys": sorted(config)})
```

**Counterpoint.** "Debugging needs the full request." Add a redaction layer that masks known secret fields before output, and keep verbose logs on a short retention ([[sys-pii-minimise-retention]]). Identifiers such as a credential's internal id stay loggable.
