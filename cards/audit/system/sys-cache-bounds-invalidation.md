---
id: sys-cache-bounds-invalidation
level: system
tags: [caching, memory]
severity: should-fix
status: draft
lang: core
applies_when: The code adds an in-process or shared cache.
tool_gate: none
borrowed_from:
  - https://aws.amazon.com/builders-library/caching-challenges-and-strategies/
---

**Rule.** Bound every cache and version its values.

**Why.** Also give it a justified TTL, hit/miss and origin-request metrics, and an invalidation story. An unbounded cache is a memory leak with extra steps. An arbitrary TTL either serves stale data or does not help. Unversioned values break during a rolling deploy when old and new code read each other's entries.

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

**Counterpoint.** "Stale data is a business risk, not a review issue." It is one when the staleness window was never chosen; the rule asks for a decision, not a number. Soft TTL (refresh in background) and hard TTL (must refetch) is the pattern AWS describes for balancing both.
