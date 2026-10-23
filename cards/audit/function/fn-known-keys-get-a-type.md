---
id: fn-known-keys-get-a-type
level: function
tags: [types]
severity: should-fix
status: draft
lang: core
applies_when: A function takes or returns a dictionary whose keys are fixed and known.
tool_gate: mypy --strict (partial)
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Give a fixed key set a record type (model, dataclass or typed dict). Use a generic map only for open keys.

**Why.** A bag of keys hides the contract. A typo'd key is a runtime `KeyError` or, worse, a silently absent value.

**FAIL**

```text
def summary(o) -> dict[str, Any]:
    return {"id": o.id, "totl": o.total}
```

**PASS**

```text
@dataclass(frozen=True)
class Summary:
    id: int
    total: Decimal
```

**Counterpoint.** "A dict is easier to serialise and extend." Records serialise as well (`asdict`, model dump). Extension is exactly what the type should make deliberate.
