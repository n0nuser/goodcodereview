---
id: py-imports
level: module
tags: [maintainability, python, imports]
severity: should-fix
status: draft
lang: python
applies_when: A Python module has imports.
tool_gate: ruff I, TID252, PLC0415
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Put imports at module top, absolute only.

**Why.** Local imports hide dependencies and cycles. Relative imports break when files move. Importing a private name couples you to something its owner may change without notice. Never import a `_`-prefixed name from another module, and use `__all__` only in a re-export `__init__.py`.

**FAIL**

```python
def handler():
    from .helpers import _parse
```

**PASS**

```python
from app.billing.parsing import parse
```

**Counterpoint.** "Import inside the function avoids a cycle." It hides the cycle instead of fixing it, and the design needs a third module or a dependency inversion. A lazy import for a heavy optional dependency is the one defensible exception; document it with a reason.
