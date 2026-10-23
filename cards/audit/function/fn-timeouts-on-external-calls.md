---
id: fn-timeouts-on-external-calls
level: function
tags: [resilience, io]
severity: block
status: draft
lang: core
applies_when: The code calls anything across a network or process boundary.
tool_gate: none (partial: linters per client)
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Set an explicit timeout on every external call, on both connect and read.

**Why.** A call without a timeout can hang forever and hold a worker, a connection and a lock with it. "No timeout" is an infinite timeout.

**FAIL**

```text
http.get(url)
http.get(url, timeout=None)
```

**PASS**

```text
http.get(url, timeout=Timeout(10, connect=2))
```

**Counterpoint.** "The library default is fine." Many defaults are infinite or surprising. A default you did not read is a default you did not choose. State it once in the client's construction so it cannot be forgotten per call.
