# API gateways

A reverse proxy for APIs. It handles auth, routing, quotas, and request shaping at one entry point.

**Why a reviewer cares.** Per-tenant quotas and 429 behaviour are often configured here. Check that they exist somewhere.

**Checks.** `svc-rate-limit-quota`
