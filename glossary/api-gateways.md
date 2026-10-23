# API Gateways

A reverse proxy specialised for APIs: auth, routing, quotas and request shaping at one entry point.

**Why a reviewer cares.** Per-tenant quotas and 429 behaviour are often configured here; check they exist somewhere.

**Checks.** `svc-rate-limit-quota`
