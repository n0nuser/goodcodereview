---
id: fn-no-stringly-typed-returns
level: function
tags: [types, api]
severity: should-fix
status: draft
lang: core
applies_when: A function returns a status, kind or outcome, and callers branch on it.
tool_gate: type checker with exhaustive match
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Return an enum (or a tagged type), never a bare string the caller must compare.

**Why.** Callers compare against strings the compiler cannot check. A typo in the producer or the consumer compiles, runs, and takes the wrong branch.

**FAIL**

```text
def check(order) -> str:
    return "missing_items" if not order.lines else "ok"
```

**PASS**

```text
class OrderCheck(Enum):
    OK = "ok"
    MISSING_ITEMS = "missing_items"

def check(order) -> OrderCheck: ...
```

**Counterpoint.** "Strings serialise for free." The enum serialises too (by value), and the wire format is unchanged. You gain a closed set the type checker can exhaust.
