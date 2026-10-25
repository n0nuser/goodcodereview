---
id: py-modern-typing
level: function
tags: [correctness, python, types]
severity: should-fix
status: draft
lacks: orgs, only the author's own Python review guide backs it; no independent org
lang: python
applies_when: Annotations use `typing` aliases, or the type gate is missing.
tool_gate: ruff UP; mypy --strict; pyright
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Write `X | None` and builtin generics, not `typing` aliases.

**Why.** A tool decides these, so a human comment is waste. Check that the gate exists, and gate new code with `mypy --strict` and pyright.

**FAIL**

```python
from typing import Optional, List
def f(x: Optional[List[int]]): ...
```

**PASS**

```python
def f(x: list[int] | None) -> None: ...
```

**Counterpoint.** "Two type checkers is overkill." They disagree on edge cases, so running both on new code catches different mistakes. Pick at least one as a hard gate.
