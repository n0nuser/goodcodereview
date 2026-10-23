---
id: py-frozen-dataclass-over-tuple
level: function
tags: [python, types]
severity: should-fix
status: draft
lang: python
applies_when: A Python function returns a tuple whose positions differ in meaning.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Return a `@dataclass(frozen=True, slots=True)` instead of a positional tuple.

**Why.** Core rule: [[fn-no-anonymous-tuples]]. In Python the frozen dataclass also gives hashing, immutability and a compact `slots` layout.

**FAIL**

```python
def parse_error(exc) -> tuple[str, str]: ...
```

**PASS**

```python
@dataclass(frozen=True, slots=True)
class ParsedError:
    code: str
    message: str
```

**Counterpoint.** "`NamedTuple` is lighter." Fine; both name the fields. Use the one your team already uses, but never a bare tuple.
