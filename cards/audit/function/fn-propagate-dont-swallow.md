---
id: fn-propagate-dont-swallow
level: function
tags: [correctness, errors]
severity: block
status: draft
lang: core
applies_when: A handler catches an error and either drops it or raises a different one.
tool_gate: ruff B904 (Python)
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Chain the original cause when you translate an exception.

**Why.** Dropping the cause removes the only trace of why the call failed. A translated error without the original traceback sends the on-call person to the wrong place. Never swallow an error silently.

**FAIL**

```text
try: gateway.charge(...)
except GatewayError:
    raise PaymentDeclined(order.id)   # cause lost
```

**PASS**

```text
try: gateway.charge(...)
except GatewayError as err:
    raise PaymentDeclined(order.id) from err
```

**Counterpoint.** "Chaining leaks internals to the caller." Chaining stays in logs and tracebacks. What the client sees is a separate mapping (see [[sys-secrets-and-errors]]).
