---
id: mod-bounded-caches
level: module
tags: [resources, state]
severity: block
status: draft
lang: core
applies_when: Code keeps a cache, map or queue keyed by request, session, user or similar.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Bound every per-key cache (LRU or TTL) and evict it when the owner ends. That includes dicts on injected objects and module globals.

**Why.** An unbounded per-session cache is a slow memory leak that appears only in production under real traffic.

**FAIL**

```text
sessions: dict[str, Context] = {}   # never evicted
```

**PASS**

```text
sessions = TTLCache(maxsize=10_000, ttl=3600)
```

**Counterpoint.** "Sessions end, so it is bounded in practice." Only if something deletes the entry on every exit path, including errors and crashes. A size or TTL bound makes the guarantee unconditional.
