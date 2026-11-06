---
id: fn-no-caller-mutation
level: function
tags: [correctness, testing, state]
severity: should-fix
status: stable
lang: core
applies_when: A function writes to a parameter or to an object the caller still owns, such as a list, map, state object or shared configuration.
tool_gate: ESLint no-param-reassign with props true (the default props false misses param.field = value); Pylint dangerous-default-value (W0102) for a mutable default.
note: parameters and caller-owned objects only; module and class state belongs to mod-no-module-mutable-state, and a fresh local object may be mutated before it is returned
borrowed_from:
  - https://airbnb.io/javascript/#functions--mutate-params
  - https://react.dev/learn/updating-objects-in-state
  - https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects
  - https://eslint.org/docs/latest/rules/no-param-reassign
  - https://google.github.io/styleguide/pyguide.html#212-default-argument-values
  - https://kotlinlang.org/docs/coding-conventions.html
---

**Rule.** Do not mutate a parameter or an object the caller owns, unless the function is documented as mutating it.

**Why.** The caller still holds the old reference, so the change lands at a distance. A list passed to one function changes under the next loop, a shared default collects values across calls, and a mutated state object never triggers a re-render. Return a new value or a copy: the change shows at the call site and the old value stays safe to compare. A fresh local object is different. Nothing else references it yet, so build it in place and return it.

**FAIL**

```python
def apply_discount(order):
    order.total *= 0.9      # the caller's order changes too
    return order
```

**PASS**

```python
def apply_discount(order):
    return dataclasses.replace(order, total=order.total * 0.9)

def normalize(items):
    out = []                # local mutation is fine
    for item in items:
        out.append(item.strip())
    return out
```

**Counterpoint.** "Copying on every update is expensive, and an in-place reducer is simpler." Copy only the part you change and share the rest, which keeps the cost low for wide objects. An in-place API is honest when its name says it mutates and its caller owns the object, as with a builder or a buffer. The failure is a quiet change to something the caller still uses. A linter set to catch only reassignment will miss a field write, so turn on the property check too.
