---
id: mod-layers-point-inward
level: module
tags: [architecture]
severity: block
status: draft
lang: core
applies_when: The codebase has separable transport, logic and outbound-boundary code.
tool_gate: import-linter or similar
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Name layers for what they do (surface, logic, boundary) and let dependencies point inward. A service never touches transport types; a surface never skips the service.

**Why.** Once transport types leak into logic, you cannot reuse or test the logic without the transport, and a change to the API shape ripples into the rules.

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

**Counterpoint.** "Three layers is ceremony for a CRUD app." For a ten-endpoint app, yes, fold them. The check applies once you have real logic; it asks only that dependencies not point outward, not that you build all three folders.
