---
id: sys-cache-hit-rate-watched
level: system
tags: [observability, performance, reliability, caching]
severity: should-fix
status: draft
lacks: orgs, both clauses have AWS and Google; Microsoft lists a Cache Hits metric but gives no advice to alert on it; needs one more org that says to alert
lang: core
applies_when: The change adds a cache, or resizes one, in front of a database or downstream service.
context: [server]
tool_gate: none
borrowed_from:
  - https://aws.amazon.com/builders-library/caching-challenges-and-strategies/
  - https://cloud.google.com/memorystore/docs/redis/memory-management-best-practices
  - https://www.atlassian.com/blog/atlassian-engineering/unlocking-reliability-with-splunk-smartstore
  - https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-how-to-monitor
---

**Rule.** Emit a cache hit-rate or memory-use metric and alert on it, so an undersized cache is noticed before it hurts the origin.

**Why.** A cache that is too small evicts hot entries. The hit rate falls and the origin takes the load, and nothing fails until the origin does. A metric and an alert turn that into a ticket instead of an outage.

**FAIL**

```python
cache = Redis(host="cache")  # maxmemory 2gb set in redis.conf; no hit-rate metric, no memory alert

def get_user(uid):
    return cache.get(uid) or db.load(uid)
```

**PASS**

```python
def get_user(uid):
    v = cache.get(uid)
    metrics.incr("user_cache.hit" if v else "user_cache.miss")
    return v or db.load(uid)

# alert: memory usage ratio > 80% for 10 minutes
# alert: hit rate < 0.8 for 10 minutes
```

**Counterpoint.** "The origin's own alerts will catch it." They fire after users see slow pages. The cache metric fires while the origin is still healthy, and it names the cause.
