---
id: fn-propagate-dont-swallow
level: function
tags: [correctness, errors]
severity: should-fix
status: draft
lacks: orgs, chaining has Microsoft; Python and Oracle describe the mechanism; Google Go and SEI CERT back no-swallow, which is in the Why; needs two more orgs
lang: core
applies_when: A handler catches an error and either drops it or raises a different one.
tool_gate: ruff B904 (Python)
borrowed_from:
  - https://go.dev/wiki/CodeReviewComments
  - https://wiki.sei.cmu.edu/confluence/display/java/ERR00-J.+Do+not+suppress+or+ignore+checked+exceptions
  - https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions
  - https://docs.python.org/3/tutorial/errors.html
  - https://docs.oracle.com/javase/tutorial/essential/exceptions/chained.html
note: Microsoft: throw a new exception with the original as inner exception; Google Go: do not discard errors with _; SEI CERT ERR00-J: do not suppress checked exceptions; Python and Oracle describe chaining (soft)
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
