---
id: py-error-hierarchy
level: module
tags: [correctness, python, errors]
severity: should-fix
status: draft
lacks: orgs, only the author's own Python review guide backs it; no independent org
lang: python
applies_when: A Python package raises its own exceptions.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Give each package one base exception, with the specific ones in an `errors` module.

**Why.** A base class gives callers one safe catch for the package. An inline `class X(Exception)` next to a raise scatters the hierarchy. Chain with `raise ... from err` ([[fn-propagate-dont-swallow]]).

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
