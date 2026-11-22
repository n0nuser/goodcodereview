---
id: fn-doc-documents-errors
level: function
tags: [maintainability, docs, reliability]
severity: should-fix
status: stable
lang: core
applies_when: A public function can raise or throw, panic, or has a safety precondition the caller must meet.
tool_gate: Ruff `DOC501` (pydoclint rules) or the language's doc lint.
note: Rust, Google (Python) and Microsoft (.NET) state it. numpydoc makes Raises optional and Kotlin sets no expectation, so the Rule limits itself to exceptions a caller can cause or must handle
borrowed_from:
  - https://rust-lang.github.io/api-guidelines/documentation.html
  - https://google.github.io/styleguide/pyguide.html
  - https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/exception-throwing
---

**Rule.** Document in the doc comment each error a public function can raise, each condition that makes it panic, and each precondition a caller must meet to call it safely.

**Why.** A caller reads the doc, not the body. An undocumented exception reaches production as an unhandled one, and an undocumented precondition becomes a crash or a memory bug.

**FAIL**

```python
def port_for(name):
    """Return the port for a service name."""
    return PORTS[name]          # KeyError on an unknown name
```

**PASS**

```python
def port_for(name):
    """Return the port for a service name.

    Raises:
        KeyError: If the name is not in PORTS.
    """
    return PORTS[name]
```

**Counterpoint.** "Exceptions change and the list goes stale." That argues for a lint that checks it, and for listing only what callers can cause. Listing every exception from every callee is not what the rule asks.
