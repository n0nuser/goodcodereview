---
id: svc-timeouts
level: service
tags: [resilience, io]
severity: block
status: draft
lang: core
applies_when: The code calls anything over a network or process boundary.
tool_gate: none
borrowed_from:
  - https://docs.python.org/3/library/asyncio-task.html
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/retry
---

**Rule.** Give every remote call an explicit timeout, and pass the remaining deadline downstream instead of restarting a fresh timeout at each hop.

**Why.** A call without a bound holds a thread, connection and caller indefinitely; one slow dependency becomes an outage. A per-hop timeout that ignores the caller's budget keeps working for a client that already gave up.

**FAIL**

```text
resp = http.get(url)                 # library default: no timeout
def handle(req): return backend.call(x, timeout=30)   # ignores req.deadline
```

**PASS**

```text
resp = http.get(url, timeout=(0.5, 2.0))
def handle(req): return backend.call(x, timeout=min(2.0, req.deadline - now()))
```

**Counterpoint.** "Defaults are fine, the library will time out eventually." Many defaults are infinite, and an eventual timeout longer than the caller's own deadline is wasted work. The research notes give the mechanism (asyncio bounds, retry guidance) and the reviewable rule is ours; the sources do not prescribe numbers, so pick them from measured latency, not folklore.
