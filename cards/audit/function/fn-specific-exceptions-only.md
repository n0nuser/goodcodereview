---
id: fn-specific-exceptions-only
level: function
tags: [errors]
severity: block
status: draft
lang: core
applies_when: Code catches exceptions in business logic.
tool_gate: ruff BLE001 / E722 (Python)
borrowed_from:
  - https://go.dev/wiki/CodeReviewComments
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
---

**Rule.** Catch the specific exception you can handle. Never catch the base exception type in business code.

**Why.** A blanket catch treats a typo'd attribute the same as a network blip. Real bugs get swallowed, logged as a warning and retried. Python version: [[py-ruff-gate]].

**FAIL**

```text
try:
    charge(order)
except Exception:
    return None
```

**PASS**

```text
try:
    charge(order)
except CardDeclined as err:
    raise PaymentDeclined(order.id) from err
```

**Counterpoint.** "A worker loop must not die on one bad message." That is the one legitimate blanket catch, once, at the process boundary, with the traceback logged, playing the role a web framework's error middleware plays for routes. Everywhere else it stays specific.
