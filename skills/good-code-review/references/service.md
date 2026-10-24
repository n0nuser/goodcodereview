# service

## svc-api-conditional-writes

severity: should-fix  
applies_when: Two callers can update the same resource through PUT, PATCH or DELETE.

**Rule.** Return an `ETag` on reads and honour `If-Match` on writes, answering 412 when the entity tag is stale.

**Why.** A read-modify-write over HTTP is a race. The second writer overwrites the first without knowing it, and no error appears anywhere.

**FAIL**

```text
GET /docs/4  -> 200 {title: "A"}
PUT /docs/4  {title: "B"}   -> 200   # overwrites a change made after the GET
```

**PASS**

```text
GET /docs/4  -> 200  ETag: "v7"
PUT /docs/4  If-Match: "v7"  -> 200  ETag: "v8"
PUT /docs/4  If-Match: "v7"  -> 412 Precondition Failed
```

**Counterpoint.** "Last write wins is fine here." For a log or a counter it is; say so in the spec. For a document, a profile or a config that two people edit, it loses work. The card applies to shared resources that people edit.

## svc-api-deprecation-sunset

severity: should-fix  
applies_when: A service retires an endpoint, field, version or parameter that outside callers use.

**Rule.** Before removing an endpoint, mark it `deprecated` in the spec and send `Deprecation` and `Sunset` headers, with the `Sunset` date no earlier than the `Deprecation` date.

**Why.** Callers cannot read your roadmap. A removal with no signal in the responses is an outage for whoever has not read the changelog. Counting calls that carry the headers also tells you when removal is safe.

**FAIL**

```text
git: delete GET /v1/orders/{id}/summary
responses before removal: no header, spec not marked deprecated
```

**PASS**

```text
GET /v1/orders/9/summary -> 200
  Deprecation: @1767225600
  Sunset: Wed, 01 Jul 2026 00:00:00 GMT
  Link: <https://api.example.com/docs/summary-removal>; rel="deprecation"
spec: deprecated: true
```

**Counterpoint.** "Our only callers are internal." Then the call count with the header gives you the list of owners to ask, and removal is cheap. [[chg-expand-contract]] covers the order of steps; this card covers what the response tells the caller. Both headers describe one resource, so send them on each deprecated route, not only on the API root.

## svc-api-error-code-stable

severity: should-fix  
applies_when: Callers of an HTTP or RPC API branch on the kind of error.

**Rule.** Give each error a stable machine-readable code that callers branch on, and never make them parse the message text.

**Why.** Message text gets reworded, translated and fixed. A client that matches on "already exists" breaks on the first edit. A published code is a contract.

**FAIL**

```text
if "already exists" in response.json()["detail"]:   # client
    handle_conflict()
```

**PASS**

```text
if response.json()["type"] == "https://api.example.com/problems/order-exists":   # client
    handle_conflict()
# the server keeps that type value for as long as the API version lives
```

**Counterpoint.** "The HTTP status is enough." It is too coarse: two different 409 conflicts need different handling. Add a code only where callers act differently; do not mint one for every branch.

## svc-api-versioning-policy

severity: should-fix  
applies_when: A service offers an HTTP API to callers you do not deploy together with it.

**Rule.** Write down one versioning scheme for the API, and ship no breaking change inside a version it has published.

**Why.** Callers upgrade on their own schedule. With no stated scheme, each breaking change is a surprise, and each team invents its own v2.

**FAIL**

```text
GET /orders   # renamed total -> amount_total
no version marker anywhere; README says "we try not to break things"
```

**PASS**

```text
docs/api-versioning.md: dated api-version query parameter, previews last 6 months, 90 days' notice
GET /orders?api-version=2026-03-01 keeps returning "total"
the rename ships under api-version=2026-09-01
```

**Counterpoint.** "We will cross that bridge later." Later arrives with a customer on the old shape. The scheme can be minimal. A media type, a dated query parameter and a pinned header all work. Pick one and write it down. What counts as breaking is in [[chg-breaking-change-taxonomy]].

## svc-idempotency-key

severity: block  
applies_when: A non-idempotent operation (charge, create, send) can be retried by a client, a queue, or a saga.

**Rule.** Make every retryable write idempotent: the caller sends a unique key, and a retry with the same key never applies the write twice.

**Why.** A timeout does not say whether the first attempt ran. Retrying without a key charges twice or sends two emails. A common way to answer the retry is to store the first result and return it again.

**FAIL**

```text
POST /payments {amount: 10}          # retried on timeout
INSERT INTO payment(amount) VALUES (10)
```

**PASS**

```text
POST /payments  Idempotency-Key: k-123
INSERT ... ON CONFLICT (idem_key) DO UPDATE SET idem_key = EXCLUDED.idem_key RETURNING *
```

**See also.** [[sys-lock-fencing]] shares the goal but uses a different mechanism (stale lock holders).

**Counterpoint.** "Our retries are rare." Queues redeliver and sagas retry by design, so rare is not never. The cost is a unique key and a stored result. No standard fixes how long the server keeps a key. Pick a window and publish it.

## svc-retry-policy

severity: block  
applies_when: The code retries a failed call, or wraps a client that retries.

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
