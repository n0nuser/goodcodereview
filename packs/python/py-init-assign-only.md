---
id: py-init-assign-only
level: module
tags: [maintainability, python, classes]
severity: should-fix
status: draft
lang: python
applies_when: A Python class defines `__init__` or `__post_init__`.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Keep `__init__` and `__post_init__` to assignments, and do I/O in a `@classmethod` factory.

**Why.** Core rule: [[mod-no-logic-in-constructors]]. A dataclass's `__post_init__` is a constructor too, so the same rule applies there.

**FAIL**

```python
@dataclass
class PriceList:
    path: Path
    def __post_init__(self):
        self.prices = json.loads(self.path.read_text())
```

**PASS**

```python
@dataclass
class PriceList:
    prices: dict[str, Decimal]

    @classmethod
    def from_file(cls, path: Path) -> "PriceList":
        raw = json.loads(path.read_text())
        return cls({sku: Decimal(p) for sku, p in raw.items()})
```

**Counterpoint.** "Dataclasses make `__post_init__` normal." It is normal for derived fields and cheap validation, but not for reading files or calling APIs.
