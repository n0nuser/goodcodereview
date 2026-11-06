---
id: mod-behaviour-lives-with-state
level: module
tags: [maintainability, design, oop]
severity: discuss
status: stable
lang: core
applies_when: A function computes something only from one object's own fields.
tool_gate: none
note: Microsoft (entity methods own the invariants), PMD (DataClass, data-behaviour proximity) and DevIQ (anemic model) put the rule on the object; Microsoft and DevIQ also give the CRUD and functional exceptions
borrowed_from:
  - https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model
  - https://docs.pmd-code.org/latest/pmd_rules_java_design.html
  - https://deviq.com/domain-driven-design/anemic-model/
---

**Rule.** Put the invariants and calculations that read only one object's fields on that object.

**Why.** A rule about one object scattered across services makes every caller learn where the rule lives, and the object cannot enforce it. Microsoft says an entity's methods "take care of the invariants and rules of the entity instead of having those rules spread across the application layer". PMD calls a data holder whose behaviour lives elsewhere a sign of "poor data-behaviour proximity". DevIQ says model objects should "use encapsulation to manage their internal state and behavior".

**FAIL**

```text
def order_total(order): return sum(l.price * l.qty for l in order.lines)
```

**PASS**

```text
class Order:
    def total(self): return sum(l.price * l.qty for l in self.lines)
```

**Counterpoint.** "Records, data classes and dataclasses are made to carry data." They are, and a carrier with no rules has nothing to move. The rule is about the calculation, not the declaration, so `total()` on a record does not stop it being a record. Keep the type a pure carrier when it holds only data. A simple CRUD context can keep a data-only model, and a functional design keeps behaviour in functions over data. The rule is for an object model.
