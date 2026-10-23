---
id: py-init-assign-only
level: module
tags: [python, classes]
severity: block
status: draft
lang: python
applies_when: A Python class defines `__init__`.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** `__init__` only assigns attributes. Put I/O, parsing and heavy computation in a `@classmethod` factory. Core rule: [[mod-no-logic-in-constructors]].

**Why.** Tests must build real files or patch `open` just to create the object.

**FAIL**

```python
def __init__(self, path):
    self._prices = json.loads(path.read_text())
```

**PASS**

```python
def __init__(self, prices): self._prices = prices
@classmethod
def from_file(cls, path): ...
```

**Counterpoint.** "Dataclasses already do this." Right: use a `dataclass` and the problem mostly disappears, apart from `__post_init__`, which has the same rule.
