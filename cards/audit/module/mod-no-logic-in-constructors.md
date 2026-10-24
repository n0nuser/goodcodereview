---
id: mod-no-logic-in-constructors
level: module
tags: [correctness, testing, state]
severity: should-fix
status: draft
lang: core
applies_when: A constructor does work beyond assigning its arguments.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Assign only in constructors, and put I/O, parsing, and heavy computation in a named factory.

**Why.** A constructor with side effects makes every instantiation, including in tests, read a file or call an API. You need a real resource or a patch just to build the object.

**FAIL**

```text
class PriceList:
    def __init__(self, path):
        self._prices = json.loads(path.read_text())
```

**PASS**

```text
class PriceList:
    def __init__(self, prices): self._prices = prices
    @classmethod
    def from_file(cls, path): ...
```

**Counterpoint.** "A factory per class is ceremony." For a value object with no I/O, there is nothing to factor out. The rule targets constructors that read, call, or parse. With the factory, the test builds the object in one line.
