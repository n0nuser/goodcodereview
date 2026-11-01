---
id: mod-no-module-mutable-state
level: module
tags: [correctness, testing, state]
severity: should-fix
status: stable
lang: core
applies_when: A module defines a variable that changes after load: a list, dict, counter, cache, client or singleton.
tool_gate: none
borrowed_from:
  - https://google.github.io/styleguide/pyguide.html#25-mutable-global-state
  - https://github.com/uber-go/guide/blob/master/style.md#avoid-mutable-globals
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2211
note: Google Python guide 2.5, Uber Go guide, Microsoft CA2211; each says to avoid mutable global or static state and allow constants
---

**Rule.** Keep no mutable state at module level.

**Why.** Hidden global state leaks between tests, between requests, and between threads, and its order of mutation is unreadable. A frozen, load-once constant such as settings is the exception. A singleton used to dodge injection is not.

**FAIL**

```python
_cache = {}

def get(key):
    if key not in _cache:
        _cache[key] = load(key)
    return _cache[key]
```

**PASS**

```python
class Loader:
    def __init__(self, cache):
        self._cache = cache

    def get(self, key):
        if key not in self._cache:
            self._cache[key] = load(key)
        return self._cache[key]
```

**Counterpoint.** "A module global is the simplest cache." It is also unbounded and shared by everything. If you need one, bound it (LRU or TTL), inject it, and tie its lifetime to what it caches.
