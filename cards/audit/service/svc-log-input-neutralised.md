---
id: svc-log-input-neutralised
level: service
tags: [security, logging]
severity: should-fix
status: stable
lang: core
applies_when: A service writes plain-text (unstructured) log lines that include a value from a request, header, form or other external input.
context: [server]
tool_gate: A formatter that escapes CR and LF in every record; a test that logs a value containing a newline and asserts a single line.
note: OWASP (sanitise all event data for CR, LF and delimiters), MITRE CWE-117 (log message built from external input without neutralising special elements) and GitLab (external input not captured in logs without validation). The Python logging cookbook shows a newline-escaping formatter and is descriptive only. Structured logs ([[svc-logs-structured]]) escape newlines by construction
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://cwe.mitre.org/data/definitions/117.html
  - https://docs.gitlab.com/development/secure_coding_guidelines/
---

**Rule.** In plain-text logs, escape or strip CR, LF and delimiter characters in external input before logging it.

**Why.** A value that contains a newline lets the sender write a line of their own into the log, such as a fake "login succeeded" entry, and so hide or forge events. Anyone reading or parsing the log cannot tell the forged line from a real one.

**FAIL**

```python
logging.info(f"login failed for {username}")   # username = "bob\nINFO login succeeded for admin"
```

**PASS**

```python
logging.info("login failed for %r", username)   # %r escapes the newline: 'bob\nINFO login ...'
```

**Counterpoint.** "We already log JSON." Then the encoder escapes the newline and this check passes by construction; the card only applies to plain-text formats. Escaping in the formatter for every record is better than at each call site, so a missed call cannot reopen the hole.
