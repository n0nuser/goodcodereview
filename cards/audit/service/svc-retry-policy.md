---
id: svc-retry-policy
level: service
tags: [resilience, retries]
severity: block
status: draft
lang: core
applies_when: The code retries a failed call, or wraps a client that retries.
tool_gate: none
borrowed_from:
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/retry
  - https://aws.amazon.com/builders-library/minimizing-correlated-failures-in-distributed-systems/
---

**Rule.** Retry only transient errors, with capped attempts, exponential backoff plus jitter, and at one layer of the call stack only.

**Why.** Immediate, unbounded or synchronized retries turn a brief fault into a load spike on the struggling dependency. Retries at several layers multiply: three layers of three attempts is nine calls per user request.

**FAIL**

```text
while True:
    try: return client.call()
    except Exception: sleep(1)        # no cap, no jitter, retries 4xx too
```

**PASS**

```text
for i in range(3):
    try: return client.call()
    except Transient: sleep(random(0, min(cap, base * 2**i)))
# the SDK's own retries are disabled, or this loop is removed
```

**Counterpoint.** "Retries make us more reliable." Only for transient faults and only within a budget; past that they hurt, which is why the Azure guidance also says to cancel on non-transient errors. The notes do not define a retry budget (a cap on retries as a share of traffic); if you require one, say it is a team convention.
