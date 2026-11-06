---
id: mod-law-of-demeter
level: module
tags: [maintainability, design, coupling]
severity: discuss
status: stable
lang: core
applies_when: A change adds a call chain that reaches through one object to use another, such as order.customer().address().city().
tool_gate: PMD LawOfDemeter (trustRadius, default 1), JetBrains inspection LawOfDemeter.
note: PMD, Google's Testing Blog (a heading only) and JetBrains state the rule. PMD's trustRadius (default 1) and JetBrains' LawOfDemeter inspection gate it with the same threshold: one call on an object another call returned; JetBrains notes the wrapper-method cost and calls the law a style guideline
borrowed_from:
  - https://pmd.github.io/pmd/pmd_rules_java_design.html#lawofdemeter
  - https://testing.googleblog.com/2008/08/by-miko-hevery-so-you-decided-to.html
  - https://www.jetbrains.com/help/inspectopedia/LawOfDemeter.html
---

**Rule.** Call methods on your direct collaborators, and do not call a method on an object that another call returned (a chain of two or more getters).

**Why.** A chain such as `order.customer().address().city()` ties the caller to the structure of three classes it does not own, so a change in any of them breaks it. PMD describes the rule as forbidding "fetching data from 'too far away'" to reduce coupling.

**FAIL**

```text
city = order.customer().address().city()
```

**PASS**

```text
city = order.shipping_city()      # Order owns how it finds the city
```

**Counterpoint.** "Fluent builders and stream pipelines chain by design." They return the same type or a value, so they do not expose structure. The rule targets getters that expose another object's parts. Every wrapper is code you now own. Pay that cost on the path that changes, and leave a stable library chain alone. The inspection ignores library calls by default. The law is a style guideline, which is why the severity is `discuss`. Use the project's tool setting as the threshold.
