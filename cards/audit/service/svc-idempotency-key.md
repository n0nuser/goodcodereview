---
id: svc-idempotency-key
level: service
tags: [resilience, correctness]
severity: block
status: draft
lang: core
applies_when: A non-idempotent operation (charge, create, send) can be retried by a client, a queue or a saga.
tool_gate: none
borrowed_from:
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/retry
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/saga
---

**Rule.** Make every retryable write idempotent: the caller sends a key and the server stores and replays the first result.

**Why.** A timeout does not say whether the first attempt ran. Retrying without a key charges twice or sends two emails.

**FAIL**

```text
POST /payments {amount: 10}          # retried on timeout
INSERT INTO payment(amount) VALUES (10)
```

**PASS**

```text
POST /payments  Idempotency-Key: k-123
INSERT ... ON CONFLICT (idem_key) DO NOTHING   # then return the stored row
```

**Counterpoint.** "Our retries are rare." Queues redeliver and sagas retry by design, so rare is not never. The cost is a unique key and a stored result; the key's retention window is a design choice the sources do not fix.
