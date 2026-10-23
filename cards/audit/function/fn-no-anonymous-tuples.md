---
id: fn-no-anonymous-tuples
level: function
tags: [readability, types]
severity: should-fix
status: draft
lang: core
applies_when: A function returns or passes a tuple whose positions mean different things.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Return a small named record, not a positional tuple, once the fields differ in meaning.

**Why.** `code, message = parse_error(e)` works until someone swaps the order. Nothing fails; the wrong value lands in the wrong place.

**FAIL**

```text
def parse_error(exc) -> tuple[str, str]: ...
code, message = parse_error(exc)
```

**PASS**

```text
@dataclass(frozen=True)
class ParsedError:
    code: str
    message: str
```

**Counterpoint.** "A pair is obviously (a, b)." Only when both elements are the same kind (`min`, `max` of one quantity, a coordinate). When two strings sit in different roles, the position is the only documentation, and it is wrong the day someone adds a third field.
