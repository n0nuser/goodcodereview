---
id: svc-timeouts
level: service
tags: [performance, reliability, resilience, io]
severity: block
status: stable
note: Rule backed by AWS, Google (gRPC), and Microsoft (ASP.NET Core gRPC); deriving the timeout from the caller's deadline has 2 orgs (Google, Microsoft) and sits in Why; no source prescribes timeout numbers
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

**Rule.** Set an explicit timeout on every remote call.

**Why.** A call without a bound holds a thread, a connection, and a caller indefinitely, so one slow dependency becomes an outage. Many clients, gRPC and `requests` among them, set no timeout by default. Where the caller has a deadline of its own, pass the remaining time down: a per-hop timeout that ignores it keeps working for a client that already gave up, and a retry loop shares that one deadline across its attempts.

**FAIL**

```python
resp = requests.get(url)                   # no timeout: can wait forever
reply = stub.GetUser(request)              # gRPC sets no deadline by default
```

**PASS**

```python
client = httpx.Client(timeout=httpx.Timeout(10.0, connect=2.0))   # set once on the client
resp = client.get(url)

def GetProfile(self, request, context):
    # bounded, and no longer than what the caller has left
    return stub.GetUser(request, timeout=min(2.0, context.time_remaining()))
```

**Counterpoint.** "Defaults are fine; the library will time out eventually." Many defaults are infinite, and an eventual timeout longer than the caller's own deadline is wasted work. Configure the client's timeout once at construction, connect and read separately, then shrink it per call to what the caller has left. Pick the numbers from measured latency, such as the downstream p99.9, not folklore.
