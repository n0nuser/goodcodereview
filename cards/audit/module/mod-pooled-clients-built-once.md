---
id: mod-pooled-clients-built-once
level: module
tags: [resources]
severity: should-fix
status: draft
lang: core
applies_when: Code creates a network or database client.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Build pooled clients once at startup and reuse them.

**Why.** A client per call defeats connection pooling, leaks sockets, and pays a handshake every time. Scope a short-lived client with a context manager.

**FAIL**

```text
def fetch(url):
    return HttpClient().get(url)    # new pool per call
```

**PASS**

```text
client = HttpClient(timeout=10)     # at startup, once
service = Service(client)           # inject it
# shutdown: client.close()
```

**Counterpoint.** "A throwaway client is simpler." For a one-off script, yes (scope it with `with`). On a server path it is a leak waiting to be counted.
