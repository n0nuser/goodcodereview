---
id: py-modern-typing
level: function
tags: [python, types]
severity: should-fix
status: draft
lang: python
applies_when: Annotations use `typing` aliases or the type gate is missing.
tool_gate: ruff UP; mypy --strict; pyright
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Write `X | None`, not `Optional`/`Union`; builtin `list`/`dict`/`tuple`, not `typing.List`. Gate new code with `mypy --strict` and pyright.

**Why.** A tool decides these, so a human comment is waste. The point is to make sure the gate exists.

**FAIL**

```python
from typing import Optional, List
def f(x: Optional[List[int]]): ...
```

**PASS**

```python
def f(x: list[int] | None) -> None: ...
```

**Counterpoint.** "Two type checkers is overkill." They disagree on edge cases; running both on new code catches different mistakes. Pick at least one as a hard gate.
