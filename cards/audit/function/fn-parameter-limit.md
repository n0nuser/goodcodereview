---
id: fn-parameter-limit
level: function
tags: [maintainability, readability, api]
severity: should-fix
status: stable
lang: core
applies_when: A function or constructor signature takes more parameters than the project's limit allows, or the project has no limit yet.
tool_gate: ESLint max-params (default 3), Pylint too-many-arguments (R0913, max-args default 5) and too-many-positional-arguments (R0917, default 5), Checkstyle ParameterNumber (default 7), RuboCop Metrics/ParameterLists (default 5), PMD ExcessiveParameterList (minimum default 10).
note: the defaults range from 3 to 10, so the card asks for the project's limit; Checkstyle lets a project ignore an overridden method whose signature it does not control
borrowed_from:
  - https://eslint.org/docs/latest/rules/max-params
  - https://checkstyle.sourceforge.io/checks/sizes/parameternumber.html
  - https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html
  - https://pylint.readthedocs.io/en/stable/user_guide/messages/refactor/too-many-arguments.html
  - https://docs.rubocop.org/rubocop/latest/cops_metrics.html
  - https://pmd.github.io/pmd/pmd_rules_java_design.html
---

**Rule.** Set a parameter-count limit in the project's linter, and keep signatures within it.

**Why.** Every positional value is a fact the caller must remember and a slot that can take the wrong one, especially when several share a type. `create_user(name, email, street, city, zip, country, plan, trial_days)` cannot be read at the call site and is easy to call in the wrong order. A named record or a builder gives the values names and lets the compiler and the reader check them. Group only values that already travel together, and keep required fields required.

**FAIL**

```python
def create_user(name, email, street, city, zip, country, plan, trial_days):
    ...
```

**PASS**

```python
def create_user(contact: Contact, subscription: Subscription):
    ...

# or: User.builder().name(...).email(...).plan(...).build()
```

**Counterpoint.** "A parameter object just moves the fields into another class and can hide required ones." A record that groups values with one owner is not hiding them, and a builder that names each required value at the call site is clearer than eight slots. The failure is a bag object with optional fields that may be missing. Do not introduce one. A signature the author cannot change, such as an override of a third-party method, is exempt, because the parameter count is not the author's decision. Keyword-only parameters fix the call-site order problem but still count toward the limit, so group the values that travel together.
