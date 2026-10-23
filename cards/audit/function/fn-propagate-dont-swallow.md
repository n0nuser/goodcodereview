---
id: fn-propagate-dont-swallow
level: function
tags: [errors]
severity: block
status: draft
lang: core
applies_when: A handler catches an error and either drops it or raises a different one.
tool_gate: ruff B904 (Python)
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Translate with the cause attached; never swallow. A handler that returns a default must log or be justified.

**Why.** Dropping the cause removes the only trace of why it failed. A translated error without the original traceback sends the on-call person to the wrong place.

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

**Counterpoint.** "Chaining leaks internals to the caller." Chaining stays in logs and tracebacks; what the client sees is a separate mapping (see the error-response rule in the service cards).
