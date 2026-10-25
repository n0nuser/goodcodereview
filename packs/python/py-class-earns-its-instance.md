---
id: py-class-earns-its-instance
level: module
tags: [maintainability, python, classes]
severity: discuss
status: draft
lacks: orgs, the Go wiki and the author's own guide back it; needs a third independent org
lang: python
applies_when: A Python class has no state, only static methods, or a `Protocol` with one implementation.
tool_gate: ruff PLR6301 (partial)
borrowed_from:
  - https://go.dev/wiki/CodeReviewComments
---

**Rule.** Give a class real state or a collaborator; otherwise write a module function.

**Why.** A static-only class is a module with extra typing. A `Protocol` with one implementation is a speculative interface. A `Protocol` needs two or more real implementations swapped at runtime; see [[mod-yagni]].

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

**Counterpoint.** "Protocols make testing easy." A fake of a concrete class in tests works with duck typing too. The Go review guide takes the same stance: declare interfaces where consumed, and avoid speculative ones.
