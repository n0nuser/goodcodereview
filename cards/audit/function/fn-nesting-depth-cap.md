---
id: fn-nesting-depth-cap
level: function
tags: [maintainability, readability]
severity: discuss
status: stable
lang: core
applies_when: Code nests conditions or loops several levels deep.
tool_gate: PMD AvoidDeeplyNestedIfStmts (problemDepth 3), Pylint too-many-nested-blocks (R1702, max-nested-blocks 5).
borrowed_from:
  - https://docs.pmd-code.org/latest/pmd_rules_java_design.html
  - https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html
  - https://flink.apache.org/how-to-contribute/code-style-and-quality-common/
---

**Rule.** Keep control-flow nesting shallow.

**Why.** Each level of nesting adds a condition the reader must keep in mind while reading the lines inside it. Deep code is harder to read and easier to break. Flatten it with early exits (see [[fn-early-return-no-else]]), and set a limit in the linter. The linters above stop at 3 levels of `if` or 5 nested blocks by default.

**FAIL**

```python
for user in users:
    if user.active:
        for order in user.orders:
            if order.paid:
                for line in order.lines:
                    if line.refundable:
                        refund(line)
```

**PASS**

```python
for user in users:
    if not user.active:
        continue
    for order in paid_orders(user):
        for line in order.lines:
            if line.refundable:
                refund(line)
```

**Counterpoint.** "Some data is nested, so the code must nest too." Walking a tree or a grid needs the loops. Move the inner body into a named function, or hide the walk in a generator, so each function stays flat.
