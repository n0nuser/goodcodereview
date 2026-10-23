---
id: py-init-py-empty
level: module
tags: [python, structure]
severity: should-fix
status: draft
lang: python
applies_when: The change adds or edits an `__init__.py`.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Keep `__init__.py` empty, except at a library's public boundary where it is a pure re-export (with `__all__`). No comments or docstrings in an empty one.

**Why.** Logic in `__init__.py` runs at import ([[mod-no-import-side-effects]]) and hides where things live.

**FAIL**

```python
# __init__.py
"""Utils."""
engine = create_engine(...)
```

**PASS**

```python
# __init__.py  (empty)
# or, at a library boundary:
from mylib.client import Client
__all__ = ["Client"]
```

**Counterpoint.** "A package docstring helps." Put it in the README or docs. An `__init__.py` that is empty says clearly that nothing is hidden here.
