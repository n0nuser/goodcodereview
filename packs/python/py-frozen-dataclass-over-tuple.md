---
id: py-frozen-dataclass-over-tuple
level: function
tags: [python, types]
severity: should-fix
status: draft
lang: python
applies_when: A Python function returns a tuple whose positions differ in meaning.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Return a `@dataclass(frozen=True)` (or `NamedTuple`). Core rule: [[fn-no-anonymous-tuples]].

**Why.** Unpacking `code, message = ...` with two str fields swaps silently.

**FAIL**

```python
def parse_error(exc) -> tuple[str, str]: ...
```

**PASS**

```python
@dataclass(frozen=True)
class ParsedError:
    code: str
    message: str
```

**Counterpoint.** "NamedTuple is lighter." Fine; both name the fields. Use the one your team already uses.
