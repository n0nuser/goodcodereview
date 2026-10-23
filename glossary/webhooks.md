# Webhooks

HTTP callbacks sent when an event occurs.

**Why a reviewer cares.** Delivery repeats on failure, so receivers must be idempotent.

**Checks.** `svc-idempotency-key`, `svc-retry-policy`
