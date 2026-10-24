---
id: svc-saga-steps
level: service
tags: [reliability, correctness, distributed, consistency]
severity: block
status: draft
lang: core
applies_when: A business operation spans services, each with its own database, coordinated as a saga.
tool_gate: none
borrowed_from:
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/saga
---

**Rule.** Make steps after the pivot idempotent and retryable, and make every compensation idempotent with a failure path.

**Why.** After the pivot there is no undo, only retry until done. A compensation can itself fail, and unhandled it leaves the system inconsistent with nobody told.

**FAIL**

```text
step 4 (after pivot): charge_card(order)     # retried -> double charge
compensate: release_stock(order)             # throws; exception swallowed
```

**PASS**

```text
step 4: charge_card(order, idempotency_key=order.id)   # safe to retry
compensate: release_stock(order) retried; on exhaustion -> alert + manual queue
```

**Counterpoint.** "Use a distributed transaction." Often unavailable across services. A saga has no isolation, so also guard against reading half-done data (semantic locks, re-reading values before acting). [[svc-idempotency-key]] covers keys, and [[svc-dlq]] covers failed messages.
