---
id: mod-no-repeated-switches
level: module
tags: [maintainability, design, complexity]
severity: discuss
status: draft
lacks: orgs, "repeated condition to polymorphism" has Refactoring.Guru and Google; needs one more org (the Shopify post does not mention switches)
lang: core
applies_when: The same switch or if-chain on one type, status or kind appears in more than one place.
tool_gate: none
note: smell "Switch Statements" (Fowler and Beck, through Refactoring.Guru); Google's testable-code post states the same replacement; the "second and third copy" threshold is this card's own reading; no fetched source backs the one-lookup-table alternative. An exhaustive switch over a closed type is [[fn-variants-as-tagged-union]]
borrowed_from:
  - https://refactoring.guru/smells/switch-statements
  - https://testing.googleblog.com/2008/08/by-miko-hevery-so-you-decided-to.html
---

**Rule.** When the same switch or if-chain on one type appears in more than one place, replace the copies with polymorphism, unless each copy is an exhaustive switch over a closed type that fails the build when a case is missing.

**Why.** Each copy is a place to forget when a new case arrives. Refactoring.Guru says: "When a new condition is added, you have to find all the switch code and modify it." The copies drift, and when the compiler does not check each switch, the missed one fails at run time.

**FAIL**

```text
def price(item):   if item.kind == "book": ...  elif item.kind == "dvd": ...
def ship(item):    if item.kind == "book": ...  elif item.kind == "dvd": ...
def label(item):   if item.kind == "book": ...  elif item.kind == "dvd": ...
```

**PASS**

```text
class Book(Item):  price(), ship(), label()
class Dvd(Item):   price(), ship(), label()      # a new kind is one new class
```

**Counterpoint.** "A switch is simpler than a class hierarchy." For one switch with short branches it is, and Refactoring.Guru says to leave it. The signal is the second and third copy of the same switch. A factory that picks a class from a string is a switch you can keep. So is a switch over a closed type that the compiler checks for every case, as [[fn-variants-as-tagged-union]] asks.
