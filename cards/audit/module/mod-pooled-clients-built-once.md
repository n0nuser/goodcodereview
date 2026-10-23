---
id: mod-pooled-clients-built-once
level: module
tags: [resources]
severity: should-fix
status: draft
lang: core
applies_when: Code creates a network or database client.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Build pooled clients once at startup and reuse them. Scope a short-lived client with a context manager.

**Why.** A client per call defeats connection pooling, leaks sockets, and pays a handshake every time.

**FAIL**

```text
def fetch(url):
    return HttpClient().get(url)    # new pool per call
```

**PASS**

```text
# startup: client = HttpClient(timeout=...); inject it; close at shutdown
```

**Counterpoint.** "A throwaway client is simpler." For a one-off script, yes (and scope it with `with`). For a server path it is a leak waiting to be counted.
