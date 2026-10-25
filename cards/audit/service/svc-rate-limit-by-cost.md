---
id: svc-rate-limit-by-cost
level: service
tags: [performance, reliability, overload, rate-limiting]
severity: should-fix
status: draft
note: Shopify (GraphQL query cost from static analysis, in points per second), GitHub (GraphQL API limits points per hour, not calls), Airbnb (key-value store charges request units from bytes read and latency, not raw requests per second); Uber tried a bytes-based quota and dropped it as imprecise, which is the Counterpoint
lang: core
applies_when: One API or store serves requests whose cost differs by orders of magnitude, such as GraphQL queries, scans next to point reads, or bulk endpoints.
tool_gate: none
borrowed_from:
  - https://shopify.engineering/rate-limiting-graphql-apis-calculating-query-complexity
  - https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api
  - https://airbnb.tech/infrastructure/from-static-rate-limiting-to-adaptive-traffic-management-in-airbnbs-key-value-store/
  - https://www.uber.com/es/en/blog/from-static-rate-limiting-to-intelligent-load-management/
---

**Rule.** When request costs differ by orders of magnitude, charge each request its estimated cost against the quota instead of counting it as one.

**Why.** A request count treats a one-row lookup and a 100,000-row scan the same, so a client within its quota can still overload the backend. Shopify computes a GraphQL query's cost by static analysis before it runs: one point per object, nothing for scalars, and a budget of 50 points per second up to 1,000. GitHub's GraphQL API also limits points, not calls. Airbnb's key-value store charges request units from the bytes read and the latency of each operation.

**FAIL**

```python
def handle(tenant, query):
    if not limiter.take(tenant, 1):          # a full scan costs the same as a point read
        raise TooManyRequests()
    return run(query)
```

**PASS**

```python
def handle(tenant, query):
    cost = estimate_cost(query)              # static: one point per object requested
    if not limiter.take(tenant, cost):
        raise TooManyRequests(retry_after=limiter.wait_for(tenant, cost))
    return run(query)
```

**Counterpoint.** "A cost model is guesswork." Uber tried a bytes-based quota for its storage and dropped it. A full table scan that returned one row looked cheap, and the shared counter in Redis added a network hop and a failure point. Base the cost on something you can measure, such as objects requested or bytes read, check it against real load, and keep a concurrency limit as a backstop. Where every request costs about the same, a request count is fine and the card is `N/A`. Which key carries the quota is [[svc-rate-limit-quota]]. This card covers the unit it counts in.
