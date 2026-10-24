---
id: mod-layers-point-inward
level: module
tags: [architecture]
severity: should-fix
status: draft
lang: core
applies_when: The codebase has separable transport, logic, and outbound-boundary code.
tool_gate: import-linter or similar
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Make dependencies point inward: surface, then logic, then boundary.

**Why.** Once transport types leak into logic, you cannot reuse or test the logic without the transport, and a change to the API shape ripples into the rules. Name the layers for what they do (surface, logic, boundary).

**FAIL**

```text
service/orders.py:  def create(request: HttpRequest) -> HttpResponse
controller/orders.py: calls repository directly
```

**PASS**

```text
controller -> service -> repository      (imports only along this arrow)
service takes plain domain types
```

**Counterpoint.** "Three layers is ceremony for a CRUD app." For a ten-endpoint app, yes; fold them. The check applies once you have real logic. It asks only that dependencies not point outward, not that you build all three folders.
