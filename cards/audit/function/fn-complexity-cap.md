---
id: fn-complexity-cap
level: function
tags: [maintainability, testing, complexity]
severity: discuss
status: stable
lang: core
applies_when: A function has many branches, or the project has no cyclomatic complexity limit yet.
tool_gate: PMD CyclomaticComplexity (reports 10 or more), RuboCop Metrics/CyclomaticComplexity (configured Max), Microsoft CA1502 (default 25).
borrowed_from:
  - https://pmd.github.io/pmd/pmd_rules_java_design.html
  - https://docs.pmd-code.org/latest/pmd_rules_java_design.html
  - https://docs.rubocop.org/rubocop/latest/cops_metrics.html
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1502
  - https://www.stroustrup.com/JSF-AV-rules.pdf
---

**Rule.** Set a cyclomatic complexity limit in the linter and keep every function under it.

**Why.** Each `if`, loop, `and` and `or` adds a path that a reader must follow and a test must cover. A function with 20 paths needs about 20 test cases, and nobody holds them all in mind at once. Set the limit in the linter so the count is not a matter of opinion. Common limits run from 10 to 25. Pick one and enforce it. Split a function that passes it into helpers that each do one job.

**FAIL**

```python
def shipping_cost(order):
    if order.country == "ES":
        if order.weight > 20:
            ...
        elif order.express:
            ...
    elif order.country in EU:
        if order.weight > 20 and order.express:
            ...
    # 12 more branches on tax, insurance and coupons
```

**PASS**

```python
def shipping_cost(order):
    base = base_rate(order.country, order.weight)
    return base + express_fee(order) + insurance(order)
# each helper stays under the limit and has its own tests
```

**Counterpoint.** "A flat `switch` over 30 cases is simple, and the split makes it worse." Agreed: one flat dispatch is easy to read, and a hard cap can force a bad split. Treat the limit as the point where a reviewer looks, and let a flat dispatch pass with a short note in the config or the code. Split by job, not to hit a number.
