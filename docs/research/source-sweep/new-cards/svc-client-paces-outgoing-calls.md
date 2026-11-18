---
id: svc-client-paces-outgoing-calls
level: service
tags: [reliability, performance, api, rate-limits]
severity: should-fix
status: draft
lacks: unreviewed, sources listed but no stable pass has checked them against rules 1 to 10
lang: core
applies_when: The code makes many calls to an API that publishes a rate limit.
tool_gate: none
borrowed_from:
  - https://shopify.dev/docs/api/admin-rest/usage/rate-limits
  - https://docs.stripe.com/rate-limits
  - https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api
---

**Rule.** Pace outgoing calls to a rate-limited API on the client, at a fixed rate or with a token bucket, so the client is not throttled.

**Why.** A client that fires as fast as it can hits the limit, collects 429 responses, and spends its quota on calls that fail. Pacing to the published rate keeps the calls that count inside the budget. Retrying a 429 after backoff still has a place, as in [[svc-retry-policy]], but it is the second line.

**FAIL**

```python
for order in orders:
    client.post("/orders", json=order)   # thousands of calls in a tight loop; the API allows 2 per second
```

**PASS**

```python
import time

class Pacer:
    def __init__(self, per_second):
        self.gap = 1 / per_second
        self.next = 0.0

    def wait(self):
        now = time.monotonic()
        time.sleep(max(0.0, self.next - now))
        self.next = max(now, self.next) + self.gap

pacer = Pacer(2)
for order in orders:
    pacer.wait()
    client.post("/orders", json=order)
```

**Counterpoint.** "The server returns 429 and Retry-After, so we can just react." Reacting means the limit is hit every time, and on some APIs repeated hits cost extra or lock the client out. Pace first and keep the 429 handling for the bursts that still get through.
