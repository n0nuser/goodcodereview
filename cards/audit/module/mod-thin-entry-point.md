---
id: mod-thin-entry-point
level: module
tags: [maintainability, architecture]
severity: should-fix
status: draft
lacks: orgs, Python (PSF) and the Rust Book back it; needs a third org that keeps the entry module to wiring
lang: core
applies_when: The application has a main module, an entry point, or a bootstrap file.
tool_gate: none
borrowed_from:
  - https://docs.python.org/3/library/__main__.html
  - https://doc.rust-lang.org/book/ch12-03-improving-error-handling-and-modularity.html
note: Python says __main__ files stay short and import the functions they run, so the logic is testable and reusable. The Rust Book says to split the program into main.rs and lib.rs and move the logic to lib.rs. The Go module layout page does not say it
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
