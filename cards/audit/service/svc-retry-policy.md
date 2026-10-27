---
id: svc-retry-policy
level: service
tags: [reliability, resilience, retries]
severity: block
status: stable
note: Transient errors are backed by Microsoft, Google SRE and AWS (a vendor), though AWS frames retries as the tool for transient failures rather than forbidding permanent ones. Capped attempts are backed by Microsoft, Google SRE, AWS and GitHub (a vendor). Jittered exponential backoff is backed by Google SRE, AWS and Stripe (a vendor). Google SRE gives a retry budget (about 10% of requests); the card leaves the number to the team
lang: core
applies_when: The code retries a failed call, or wraps a client that retries.
tool_gate: none
borrowed_from:
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/retry
  - https://aws.amazon.com/builders-library/minimizing-correlated-failures-in-distributed-systems/
  - https://sre.google/sre-book/addressing-cascading-failures/
  - https://sre.google/sre-book/handling-overload/
  - https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
  - https://docs.stripe.com/rate-limits
  - https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api
---

**Rule.** Retry only transient errors, with capped attempts and jittered exponential backoff.

**Why.** Immediate, unbounded, or synchronized retries turn a brief fault into a load spike on the struggling dependency. Retry at one layer only: three layers of three attempts is nine calls per user request. Make retried writes safe with [[svc-idempotency-key]].

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
        if i == 2:
            raise
        time.sleep(random.uniform(0, min(CAP_S, BASE_S * 2**i)))
# retry at one layer only: the client's own retries are off
```

**Counterpoint.** "Retries make us more reliable." Only for transient faults and only within a budget. Past that they hurt, so a non-transient error should fail at once. A retry budget (retries capped as a share of traffic) helps further. This card leaves its size to the team.
