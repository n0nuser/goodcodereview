---
id: py-class-earns-its-instance
level: module
tags: [maintainability, python, classes]
severity: discuss
status: stable
lang: python
applies_when: A Python class has no state, only static methods, or a `Protocol` with one implementation.
tool_gate: ruff PLR6301 (partial), Pylint R0903 (min-public-methods=2, dataclasses exempt; it counts public methods, not state, so a static-only class with two methods passes)
note: Go review guide and the creator's Python guide back the rule; Refactoring.Guru and Pylint add the class half. Pylint's threshold is 2 and it exempts dataclasses, so treat it as a prompt, not a hard gate
borrowed_from:
  - https://go.dev/wiki/CodeReviewComments
  - https://pablogonzalez.me/posts/python-code-review-guide/
  - https://refactoring.guru/smells/lazy-class
  - https://pylint.readthedocs.io/en/latest/user_guide/messages/refactor/too-few-public-methods.html
---

**Rule.** Give a class real state or a collaborator; otherwise write a module function.

**Why.** A static-only class is a module with extra typing. A `Protocol` with one implementation is a speculative interface. A `Protocol` needs two or more real implementations swapped at runtime; see [[mod-yagni]]. Every class costs time to understand and maintain, so one that does too little should become a function. A class kept to mark future work is the same speculation: delete it, or name the plan and its owner. Pylint flags a class with too few public methods and shows a dataclass plus a function, or a larger API, as the fixes.

**FAIL**

```python
class DateUtils:
    @staticmethod
    def parse(s): ...
class TaxCalc:
    def total(self, order): return order.total   # no state, one method
class Notifier(Protocol): ...   # one impl, ever
```

**PASS**

```text
dates.py:  def parse(s): ...
tax.py:    def total(order): ...
# use the concrete class until a second real impl exists
```

**Counterpoint.** "Protocols make testing easy." A fake of a concrete class in tests works with duck typing too. Declare an interface where it is consumed, and avoid speculative ones.
