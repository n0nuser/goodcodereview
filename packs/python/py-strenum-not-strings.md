---
id: py-strenum-not-strings
level: function
tags: [correctness, python, types]
severity: should-fix
status: draft
lacks: orgs, only the author's own Python review guide backs it; no independent org
lang: python
applies_when: Python code compares against string or number literals for a fixed set of values.
tool_gate: ruff PLR2004 (partial)
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Use `StrEnum` for fixed string sets and `HTTPStatus` for HTTP codes.

**Why.** Core rules: [[fn-no-magic-values]], [[fn-no-stringly-typed-returns]]. `StrEnum` members are still `str` (JSON-ready, comparable), and a pydantic field typed with one rejects unknown values at parse time.

**FAIL**

```python
if resp.status_code == 404 or mode == "fast": ...
```

**PASS**

```python
class Mode(StrEnum):
    FAST = "fast"

if resp.status_code == HTTPStatus.NOT_FOUND or mode == Mode.FAST: ...
```

**Counterpoint.** "An enum is heavy for two values." It is one class, and it makes the type checker guard every caller. `StrEnum` needs Python 3.11 or later; on older versions, use `class Mode(str, Enum)`.
