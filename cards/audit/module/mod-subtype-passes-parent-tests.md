---
id: mod-subtype-passes-parent-tests
level: module
tags: [maintainability, oop, design]
severity: should-fix
status: draft
lang: core
applies_when: The code adds a subclass or an implementation of an interface.
tool_gate: Run the parent's test suite against every subclass; mypy flags incompatible overrides.
note: Liskov and Wing read for the abstract and the subtype definition; running the parent's tests is a practical proxy for their specification rules
borrowed_from:
  - https://www.cs.columbia.edu/~wing/publications/LiskovWing94.pdf
  - https://www.eiffel.org/doc/solutions/Design_by_Contract_and_Assertions
  - https://mypy.readthedocs.io/en/stable/common_issues.html
  - https://www.hillelwayne.com/post/lsp/
---

**Rule.** Make a subtype pass its parent's tests: accept every input the parent accepts, promise at least what it promises, and keep its invariants.

**Why.** Callers hold the parent type. A subtype may weaken preconditions and strengthen postconditions, never the reverse, and must keep the parent's invariants. The parent's black-box tests are the cheapest way to check that. A subclass that rejects valid input or weakens a result breaks them, and the failure appears far from the subclass.

**FAIL**

```python
class ReadOnlyFile(File):
    def write(self, data):
        raise NotImplementedError      # parent accepts any bytes
```

**PASS**

```python
class ReadOnlyFile(Readable): ...      # separate type; File(Readable, Writable)
# or: the parent's black-box tests run unchanged against ReadOnlyFile
```

**Counterpoint.** "Inheritance is for sharing code." Then share it by composition. A subclass that ignores most of what it inherits ([[mod-fowler-smells]]) is a sign that the hierarchy is wrong.
