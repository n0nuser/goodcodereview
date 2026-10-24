---
id: mod-subtype-passes-parent-tests
level: module
tags: [oop, design]
severity: should-fix
status: draft
lang: core
applies_when: The code adds a subclass or an implementation of an interface.
tool_gate: Run the parent's test suite against every subclass.
note: primary source (Liskov and Wing 1994) located but not read; secondary restatement used
borrowed_from:
  - https://www.hillelwayne.com/post/lsp/
---

**Rule.** A subtype must pass its parent's tests: accept every input the parent accepts, promise at least what it promises, keep its invariants.

**Why.** Callers hold the parent type. A subclass that rejects valid input or weakens a result breaks them, and the failure appears far from the subclass.

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

**Counterpoint.** "Inheritance is for sharing code." Then share it by composition. A subclass that ignores most of what it inherits ([[mod-fowler-smells]]) is a sign the hierarchy is wrong.
