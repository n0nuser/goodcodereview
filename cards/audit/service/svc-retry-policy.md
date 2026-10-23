---
id: svc-retry-policy
level: service
tags: [resilience, retries]
severity: block
status: draft
note: retry budget is not defined in the sources
lang: core
applies_when: The code retries a failed call, or wraps a client that retries.
tool_gate: none
borrowed_from:
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/retry
  - https://aws.amazon.com/builders-library/minimizing-correlated-failures-in-distributed-systems/
---

**Rule.** Retry only transient errors, with capped attempts and jittered exponential backoff.

**Why.** Immediate, unbounded or synchronized retries turn a brief fault into a load spike on the struggling dependency. Retry at one layer only: three layers of three attempts is nine calls per user request. Make retried writes safe with [[svc-idempotency-key]].

**FAIL**

```text
while True:
    try: return client.call()
    except Exception: sleep(1)        # no cap, no jitter, retries 4xx too
```

**PASS**

```python
import random, time
for i in range(3):
    try:
        return client.call()
    except TransientError:
        time.sleep(random.uniform(0, min(CAP_S, BASE_S * 2**i)))
# retry at one layer only: the client's own retries are off
```

**Counterpoint.** "Retries make us more reliable." Only for transient faults and only within a budget; past that they hurt, which is why the Azure guidance also says to cancel on non-transient errors. A retry budget (retries capped as a share of traffic) is a further team convention, not required here.
