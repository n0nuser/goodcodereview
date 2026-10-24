---
id: sys-cache-bounds-invalidation
level: system
tags: [performance, caching, memory]
severity: should-fix
status: draft
note: bounds and expiry have 3 orgs (AWS, Redis, Caffeine); invalidation has one (IETF, HTTP only)
lang: core
applies_when: The code adds an in-process or shared cache.
tool_gate: none
borrowed_from:
  - https://builder.aws.com/content/3K9TeXp6strMiJ4vhakpRD7BQWO/caching-challenges-and-strategies
  - https://redis.io/docs/latest/develop/reference/eviction/
  - https://github.com/ben-manes/caffeine/wiki/Eviction
  - https://www.rfc-editor.org/rfc/rfc9111.html#name-invalidating-stored-response
---

**Rule.** Bound every cache and version its values.

**Why.** An unbounded cache is a memory leak with extra steps. An arbitrary TTL either serves stale data or does not help. Unversioned values break during a rolling deploy when old and new code read each other's entries. Also give the cache a justified TTL, hit/miss and origin-request metrics, and an invalidation story.

**FAIL**

```text
CACHE = {}                         # grows forever, no metrics
CACHE[k] = pickle(value)           # no version field
```

**PASS**

```text
cache = LRU(max=10_000, ttl=60)   # pseudocode; value = {"v": 2, "data": ...}
metrics: hits, misses, origin_calls
```

**Counterpoint.** "Stale data is a business risk, not a review issue." It is one when the staleness window was never chosen. The rule asks for a decision, not a number. AWS describes soft TTL (refresh in the background) and hard TTL (must refetch) as the pattern for balancing both.
