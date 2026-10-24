---
id: fn-no-getattr-for-known-names
level: function
tags: [maintainability, types, readability]
severity: discuss
status: draft
lang: core
applies_when: Code reads or writes an attribute or field by a dynamic key when the name is known at write time.
tool_gate: ruff B009 / B010
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Use plain field access, and reserve dynamic access for genuinely dynamic names.

**Why.** Dynamic access defeats rename tools, type checking, and grep. A rename misses it, and it fails at runtime.

**FAIL**

```text
value = getattr(order, "total")
```

**PASS**

```text
value = order.total
```

**Counterpoint.** "I loop over field names." That is fine when the set of names is the data (a mapping from column names, a serializer). If the names are fixed, unroll the loop.
