---
id: mod-bounded-fan-out
level: module
tags: [maintainability, design, structure]
severity: discuss
status: stable
lang: core
applies_when: A change adds imports or type references to a class, file or function that already depends on many others.
tool_gate: Microsoft CA1506 (95 types, 40 members), Checkstyle ClassFanOutComplexity (20), eslint-plugin-import import/max-dependencies (10), PMD CouplingBetweenObjects (20) and ExcessiveImports (30).
note: a documented limit on how many other types or modules a unit depends on - Microsoft (CA1506), Checkstyle, eslint-plugin-import, PMD; the defaults differ by a factor of ten, so the Rule asks for a limit and does not name a number
borrowed_from:
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1506
  - https://checkstyle.sourceforge.io/checks/metrics/classfanoutcomplexity.html
  - https://github.com/import-js/eslint-plugin-import/blob/main/docs/rules/max-dependencies.md
  - https://pmd.github.io/pmd/pmd_rules_java_design.html
---

**Rule.** Set a limit on how many other types or modules one unit depends on, and split a unit that passes it.

**Why.** A unit that depends on many others breaks when any of them changes and is hard to test, because each dependency needs a stand-in. eslint-plugin-import says "a module with too many dependencies is a code smell, and usually indicates the module is doing too much". Microsoft's rule gives the same reason: high class coupling is "difficult to maintain".

**FAIL**

```text
order_service.py: 46 imports (payments, shipping, tax, email, pdf, audit, 40 more)
```

**PASS**

```text
order_service.py: 9 imports; tax, shipping and notification each sit behind one module
eslint: "import/max-dependencies": ["error", { "max": 10 }]
```

**Counterpoint.** "The entry point has to import everything to wire it up." It does, so allowlist the composition root and nothing else. Microsoft's own page says to suppress the rule when the type "is considered maintainable despite its large number of dependencies".
