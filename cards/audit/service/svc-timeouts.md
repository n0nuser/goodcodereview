---
id: svc-timeouts
level: service
tags: [performance, reliability, resilience, io]
severity: block
status: draft
note: timeout numbers are not prescribed by any source; only Google (gRPC, SRE) and AWS state that the deadline passes down the chain
lang: core
applies_when: The code calls anything over a network or process boundary.
tool_gate: none
borrowed_from:
  - https://docs.python.org/3/library/asyncio-task.html
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/retry
  - https://grpc.io/docs/guides/deadlines/
  - https://sre.google/sre-book/addressing-cascading-failures/
  - https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter
  - https://learn.microsoft.com/en-us/aspnet/core/grpc/deadlines-cancellation
---

**Rule.** Set an explicit timeout on every remote call, and derive it from the caller's remaining deadline.

**Why.** A call without a bound holds a thread, a connection, and a caller indefinitely, so one slow dependency becomes an outage. A per-hop timeout that ignores the caller's budget keeps working for a client that already gave up.

**FAIL**

```text
resp = requests.get(url)             # no timeout argument: waits forever
def handle(req): return backend.call(x, timeout=30)   # ignores req.deadline
retry(backend.call, attempts=3, timeout=2.0)           # 6 s of tries inside a 1 s caller deadline
```

**PASS**

```text
client = httpx.Client(timeout=httpx.Timeout(10.0, connect=2.0))   # per-call bound, set once on the client
resp = client.get(url)
def handle(req): return backend.call(x, timeout=min(2.0, req.deadline - now()))
```

**Counterpoint.** "Defaults are fine; the library will time out eventually." Many defaults are infinite, and an eventual timeout longer than the caller's own deadline is wasted work. Configure the client's timeout once at construction (connect and read separately), then shrink it per call to the caller's remaining deadline. Pick numbers from measured latency, not folklore. For Python specifics, see [[py-cancellation]] (catching `TimeoutError` outside `asyncio.timeout()`).
