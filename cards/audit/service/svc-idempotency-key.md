---
id: svc-idempotency-key
level: service
tags: [resilience, correctness]
severity: block
status: stable
lang: core
applies_when: A non-idempotent operation (charge, create, send) can be retried by a client, a queue, or a saga.
tool_gate: none
borrowed_from:
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/retry
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/saga
  - https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/
  - https://docs.stripe.com/api/idempotent_requests
---

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
