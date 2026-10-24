---
id: mod-thin-entry-point
level: module
tags: [architecture]
severity: should-fix
status: draft
lang: core
applies_when: The application has a main module, an entry point, or a bootstrap file.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Keep the entry module to wiring (bootstrap, configuration, lifespan) and put no business logic in it.

**Why.** Logic in the entry module cannot be imported by tests or other entry points without starting the app.

**FAIL**

```text
main.py: defines routes, validates, computes prices, starts server
```

**PASS**

```text
main.py: build settings, wire dependencies, mount routers, start
```

**Counterpoint.** "It is only 20 lines." It will not stay 20. The rule gives the next feature an obvious home that is not main.
