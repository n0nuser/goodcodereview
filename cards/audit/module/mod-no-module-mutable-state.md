---
id: mod-no-module-mutable-state
level: module
tags: [state, testing]
severity: block
status: draft
lang: core
applies_when: A module defines a variable that changes after load: a list, dict, counter, cache, client or singleton.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Keep no mutable state at module level and no singleton used to avoid dependency injection. A frozen, load-once constant (settings) is the exception.

**Why.** Hidden global state leaks between tests, between requests and between threads, and its order of mutation is unreadable.

**FAIL**

```text
_cache = {}
def get(k):
    _cache.setdefault(k, load(k))
```

**PASS**

```text
class Loader:
    def __init__(self, cache): self._cache = cache
```

**Counterpoint.** "A module global is the simplest cache." It is also unbounded and shared by everything. If you need one, bound it (LRU or TTL), inject it, and tie its lifetime to what it caches.
