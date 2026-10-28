# Postmortem: orders page timeouts, 2026-09-14

## Cause
At 09:02 the deploy ran one migration that renamed `orders.cust_id` to `orders.customer_id` and dropped the old column. Pods still on the previous release kept reading `cust_id` and returned 500s for 11 minutes until the rollout finished.

## Fix
The orders list was also slow before the deploy. We added an in-process cache around the list query and p99 now looks better. We did not profile it.

## Actions
- Add a cache TTL (owner: team).
