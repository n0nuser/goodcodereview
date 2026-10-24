---
id: sys-cache-bounds-invalidation
level: system
tags: [performance, caching, memory]
severity: should-fix
status: stable
note: bounds and expiry have 3 orgs (AWS, Redis, Caffeine); invalidation has one (IETF, HTTP only) and value versioning none, so both sit in Why
lang: core
applies_when: The code adds an in-process or shared cache.
tool_gate: none
borrowed_from:
  - https://builder.aws.com/content/3K9TeXp6strMiJ4vhakpRD7BQWO/caching-challenges-and-strategies
  - https://redis.io/docs/latest/develop/reference/eviction/
  - https://github.com/ben-manes/caffeine/wiki/Eviction
  - https://www.rfc-editor.org/rfc/rfc9111.html#name-invalidating-stored-response
---

**Rule.** Bound every cache by size and give its entries an expiry.

**Why.** An unbounded cache is a memory leak that shows up only under production traffic. Redis has no memory limit by default on 64-bit builds. Choose the TTL from the staleness you can tolerate, because an arbitrary one either serves stale data or does not help. Also version the values, since old and new code read each other's entries during a rolling deploy, and give the cache hit, miss, and origin-request metrics and a way to invalidate.

**FAIL**

```text
CACHE = {}                         # grows forever, never expires
redis.conf: maxmemory 0            # unlimited, used as a cache
```

**PASS**

```text
cache = cachetools.TTLCache(maxsize=10_000, ttl=60)
redis.conf: maxmemory 2gb, maxmemory-policy allkeys-lru
```

**Counterpoint.** "Stale data is a business risk, not a review issue." It is one when the staleness window was never chosen. The rule asks for a decision, not a number. A soft TTL (refresh in the background) under a hard TTL (must refetch) balances freshness against load.
