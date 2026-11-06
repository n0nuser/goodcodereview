---
id: mod-temporary-field
level: module
tags: [maintainability, design, state]
severity: discuss
status: draft
lacks: unreviewed, sources and examples are in place; no stable pass has checked rules 1 to 10
lang: core
applies_when: A private field is assigned and read inside one method, or every read of it follows an assignment.
tool_gate: JetBrains FieldCanBeLocal, Sonar S1450, PMD SingularField (all private fields only).
note: JetBrains, SonarSource and PMD flag a private field that is always assigned before it is read; PMD warns that threading can produce false positives. Refactoring.Guru's Temporary Field is a different smell (fields set only in some circumstances, fixed with Extract Class), so it backs the name and not the trigger
borrowed_from:
  - https://refactoring.guru/smells/temporary-field
  - https://www.jetbrains.com/help/inspectopedia/FieldCanBeLocal.html
  - https://raw.githubusercontent.com/SonarSource/sonar-dotnet/master/analyzers/rspec/cs/S1450.html
  - https://docs.pmd-code.org/latest/pmd_rules_java_design.html
---

**Rule.** Make a field a local variable or a parameter when every method that uses it assigns it before reading it.

**Why.** The field looks like object state, so a reader expects it to survive between calls. It does not. It is one method's scratch space, so a reader looks for state the object never keeps. JetBrains, Sonar and PMD flag a private field whose every read follows an assignment, because a local variable says the same thing without the extra state.

**FAIL**

```python
class Invoice:
    def total(self, lines):
        self._subtotal = sum(l.price for l in lines)   # scratch on the object
        return self._subtotal * 1.2
```

**PASS**

```python
class Invoice:
    def total(self, lines):
        subtotal = sum(l.price for l in lines)
        return subtotal * 1.2
```

**Counterpoint.** "The field carries state between calls." Then a read can happen before the next assignment, and the rule does not fire. The trigger is every read following an assignment in the same method. Caches, ORM models and serialisation models set attributes outside `__init__` on purpose, and their reads are not preceded by a fresh assignment, so they stay. In concurrent code a second thread can read between the assignment and the read, which is why PMD calls its rule threading-unaware; suppress it where another thread reads the field on purpose.
