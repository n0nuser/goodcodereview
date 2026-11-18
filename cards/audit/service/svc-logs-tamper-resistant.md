---
id: svc-logs-tamper-resistant
level: service
tags: [security, observability, logging]
severity: should-fix
status: draft
lacks: orgs, tamper resistance has Google and OWASP only; needs a third org that ships logs to a store the host cannot alter
lang: core
applies_when: The service writes security-relevant logs or an audit trail.
context: [server]
tool_gate: Config check that the log shipper targets a remote collector, and that the host's credentials there are append-only.
borrowed_from:
  - https://google.github.io/building-secure-and-reliable-systems/raw/ch15.html
  - https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures
---

**Rule.** Ship logs and audit trails to a store that the logged host cannot alter or delete.

**Why.** An attacker who gets a foothold on a host edits or erases the local logs first. If the only copy sits on that host, the evidence goes with it. A remote store with append-only access for the host keeps the record, and the attacker then has to compromise a second system. What to log is covered by [[svc-security-event-logging]].

**FAIL**

```python
import logging

audit = logging.getLogger("audit")
audit.addHandler(logging.FileHandler("/var/log/app/audit.log"))   # the app user can edit or delete this file
```

**PASS**

```python
import logging
from logging.handlers import SysLogHandler

audit = logging.getLogger("audit")
audit.addHandler(SysLogHandler(address=("logs.internal", 514)))   # collector grants this host append-only access
```

**Counterpoint.** "Central logging costs money, and local files are enough for debugging." Keep local files for debugging. Send only the audit and security events to the remote store, which is a small share of the volume.
