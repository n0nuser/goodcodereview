---
id: py-error-hierarchy
level: module
tags: [python, errors]
severity: should-fix
status: draft
lang: python
applies_when: A Python package raises its own exceptions.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Define a base exception per package and its specific errors in a dedicated `errors` module. Chain with `raise ... from err`. Core rules: [[fn-specific-exceptions-only]], [[fn-propagate-dont-swallow]].

**Why.** A base class gives callers one safe catch for the package. Inline `class X(Exception)` next to a raise scatters the hierarchy.

**FAIL**

```python
raise Exception("declined")
```

**PASS**

```python
# billing/errors.py
class BillingError(Exception): ...
class PaymentDeclined(BillingError): ...
```

**Counterpoint.** "Built-in exceptions are enough." For ValueError-like cases, yes. For domain failures, callers need names to catch and a base to catch them all.
