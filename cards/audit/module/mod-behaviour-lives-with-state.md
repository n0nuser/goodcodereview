---
id: mod-behaviour-lives-with-state
level: module
tags: [design, oop]
severity: discuss
status: draft
lang: core
applies_when: A service function computes something only from one object's own fields.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Put invariants and calculations over one object on that object. Move logic to a service only when it spans objects or needs an injected collaborator.

**Why.** An anemic model scatters rules about an object across services. Every caller needs to know where the rule lives.

**FAIL**

```text
def order_total(order): return sum(l.price * l.qty for l in order.lines)
```

**PASS**

```text
class Order:
    @property
    def total(self): return sum(l.price * l.qty for l in self.lines)
```

**Counterpoint.** "Data classes should stay dumb." That is a style choice, not a free pass. If the calculation needs I/O or other aggregates, a service is right. The rule only targets functions that read nothing but one object.
