---
id: svc-rate-limit-quota
level: service
tags: [security, reliability, multi-tenant, overload]
severity: should-fix
status: stable
lang: core
applies_when: A shared API or queue serves several tenants or callers.
context: [server]
tool_gate: none
note: the per-tenant cap rests on AWS (quotas at a per-tenant or per-workload granularity), Google (a quota for each customer) and Microsoft (quota enforcement so a single tenant cannot overwhelm the system); GitHub, Shopify, AWS and Microsoft document the principal key and the window
borrowed_from:
  - https://aws.amazon.com/builders-library/fairness-in-multi-tenant-systems/
  - https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/
  - https://sre.google/sre-book/handling-overload/
  - https://learn.microsoft.com/en-us/azure/architecture/antipatterns/noisy-neighbor/noisy-neighbor
  - https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-228-upd1.pdf
  - https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api
  - https://shopify.dev/docs/apps/build/apis/graphql-admin/rate-limits
  - https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html
  - https://learn.microsoft.com/en-us/azure/api-management/rate-limit-policy
---

**Rule.** Enforce a per-tenant quota on shared APIs and queues.

**Why.** Without a quota, one noisy tenant consumes shared capacity for everyone. Key the count to the identity that owns the quota, such as the tenant, account or API key, and state the window and when capacity returns. Also add a per-tenant concurrency cap, and return 429 for over-quota but 503 for the service's own lack of capacity, so clients do not retry quota errors as capacity problems.

**FAIL**

```text
every tenant shares one worker pool and one request budget
no per-tenant limit: one tenant's batch job starves the rest
```

**PASS**

```text
limiter.check(tenant_id) -> 429 + Retry-After
per-tenant semaphore on workers
```

**Counterpoint.** "One global rate limit is simpler." A global limit protects the service, but one tenant can use all of it, and then every other tenant gets errors. A per-tenant limit costs one key per tenant in the limiter. Some older services return 503 for quota errors, so the status code is a convention. What matters is that a client can tell a quota error from a capacity error. Shuffle sharding (per-tenant worker subsets) isolates tenants further, and this card does not require it.
