---
id: sys-cache-cold-start
level: system
tags: [caching, overload]
severity: should-fix
status: draft
lang: core
applies_when: Cache misses fall through to a database or downstream service.
tool_gate: none
borrowed_from:
  - https://aws.amazon.com/builders-library/caching-challenges-and-strategies/
---

**Rule.** Cap and coalesce the cache-miss path so an empty cache cannot overwhelm the origin.

**Why.** The system must also survive with the cache down. After a deploy, restart or cache outage every request misses at once and the origin is overwhelmed (a stampede), which also stops the cache from refilling.

**FAIL**

```text
v = cache.get(k) or db.load(k)     # every miss hits db; cache error raises
```

**PASS**

```text
v = singleflight(k, db.load) with global origin limit
cache error -> fall back to origin within the limit
```

**Counterpoint.** "Overprovision the origin instead." That hides the dependency until the day the cache fails. AWS's advice is to test with the cache disabled and confirm the protections work.
