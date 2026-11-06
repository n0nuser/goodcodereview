---
id: mod-no-import-cycles
level: module
tags: [maintainability, design, structure]
severity: should-fix
status: stable
lang: core
applies_when: A change adds an import, dependency or project reference between modules, packages or build targets.
tool_gate: eslint-plugin-import import/no-cycle, Pylint R0401 (cyclic-import), Nx @nx/enforce-module-boundaries, or ArchUnit slices().should().beFreeOfCycles().
note: the language or build tool rejects a cycle - Go (an import cycle is illegal), Bazel (targets form a directed acyclic graph), Cargo (the resolver does not allow cycles, except dev-dependencies); lint rules - eslint-plugin-import, Nx, Pylint, ArchUnit; scope to the package boundary, because Python and Rust allow cycles between modules
borrowed_from:
  - https://go.dev/ref/spec
  - https://bazel.build/concepts/dependencies
  - https://doc.rust-lang.org/cargo/reference/resolver.html
  - https://github.com/import-js/eslint-plugin-import/blob/main/docs/rules/no-cycle.md
  - https://nx.dev/docs/kb/resolve-circular-dependencies
  - https://www.archunit.org/userguide/html/000_Index.html
  - https://pylint.pycqa.org/en/stable/user_guide/messages/refactor/cyclic-import.html
---

**Rule.** Keep the dependency graph between modules or packages acyclic, and break a cycle by moving the shared part into a third module that both depend on.

**Why.** Two modules that import each other cannot be built, tested or understood alone, and a change in one can break the other. Go rejects the cycle at compile time, Bazel defines its dependency graph as acyclic, and Cargo tells authors to split a package so it "remains strictly acyclic". Where the language allows the cycle, it still ties the two modules into one.

**FAIL**

```text
billing/invoice.py   imports  customers/account.py
customers/account.py imports  billing/invoice.py     # cycle
```

**PASS**

```text
billing/invoice.py     imports  customers/account.py
customers/account.py   imports  nothing from billing/
(shared types live in customers/types.py, which both import)
```

**Counterpoint.** "Python lets you import inside the function, so the cycle works." That hides the cycle at run time and leaves the two modules coupled. Apply the rule at the package or module boundary, where the toolchain or a lint rule can check it, and allow a documented exception for generated code or a test-only dependency.
