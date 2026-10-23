---
id: py-class-earns-its-instance
level: module
tags: [python, classes]
severity: discuss
status: draft
lang: python
applies_when: A Python class has no state, only static methods, or a `Protocol` with one implementation.
tool_gate: ruff PLR6301 (partial)
borrowed_from:
  - https://go.dev/wiki/CodeReviewComments
---

**Rule.** A class needs real state, an injected collaborator or a substitutable abstraction. A `Protocol` needs two or more real implementations swapped at runtime; a test-only seam lives in the test suite.

**Why.** A static-only class is a module with extra typing. A one-implementation `Protocol` is a speculative interface ([[mod-yagni]]).

**FAIL**

```python
class DateUtils:
    @staticmethod
    def parse(s): ...
class Notifier(Protocol): ...   # one impl, ever
```

**PASS**

```python
dates.py:  def parse(s): ...
# use the concrete class until a second real impl exists
```

**Counterpoint.** "Protocols make testing easy." A fake of a concrete class in tests works with duck typing too. The Go review guide takes the same stance: declare interfaces where consumed, avoid speculative ones.
