---
id: py-init-py-empty
level: module
tags: [maintainability, python, structure]
severity: should-fix
status: draft
lacks: orgs, only the author's own Python review guide backs it; no independent org
lang: python
applies_when: The change adds or edits an `__init__.py`.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Keep `__init__.py` empty unless it re-exports the public API.

**Why.** Logic in `__init__.py` runs at import ([[mod-no-import-side-effects]]) and hides where things live. A re-export file may use `__all__`. An empty one has no comment or docstring.

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

**Counterpoint.** "A package docstring helps." Put it in the README or docs. An empty `__init__.py` says clearly that nothing is hidden here.
