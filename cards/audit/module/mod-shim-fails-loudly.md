---
id: mod-shim-fails-loudly
level: module
tags: [correctness, reliability, testing]
severity: should-fix
status: draft
lacks: evidence, the sources define how an unimplemented operation signals itself; none states a practice about shims or monkeypatches in production
lang: core
applies_when: The code replaces, wraps or stubs another library, symbol or service, such as a compatibility shim, a global monkeypatch or a stub with a default return.
tool_gate: Test that calls the shim with a symbol it does not implement and expects an exception; grep for `unittest.mock` and `monkeypatch` imports outside test directories.
note: Python, Rust, Oracle and Microsoft each define an exception or macro for an unimplemented or unsupported operation. None says "do not ship a success-returning shim"; that is the author's audit finding. A fourth source for the monkeypatch-in-production clause was not found
borrowed_from:
  - https://docs.python.org/3/library/exceptions.html#NotImplementedError
  - https://doc.rust-lang.org/std/macro.unimplemented.html
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/UnsupportedOperationException.html
  - https://learn.microsoft.com/en-us/dotnet/api/system.notsupportedexception
---

**Rule.** A shim or stub must raise for every operation it does not implement; it must not return a success value such as 0, `None` or an empty result for an unknown call.

**Why.** A fallback that answers every missing symbol with success turns a missing feature into silent wrong behaviour. A caller gets a zero, goes on, and the bug appears far from the shim. A mock or patch used by tests and left on a production path does the same for the whole process. Raising `NotImplementedError` or its equivalent puts the failure at the call that caused it.

**FAIL**

```python
# compat.py, imported by the app at startup
class _Lib:
    def __getattr__(self, name):
        return lambda *a, **k: 0        # every missing function "succeeds"

sys.modules["legacy_crypto"] = _Lib()
```

**PASS**

```python
class _Lib:
    def verify(self, data, sig): ...    # the one function the app uses

    def __getattr__(self, name):
        raise NotImplementedError(f"legacy_crypto.{name} is not shimmed")

sys.modules["legacy_crypto"] = _Lib()
```

**Counterpoint.** "A stub that returns defaults keeps the app up when a dependency is missing." Degrading on purpose is fine when the card's reader can see it: return a named fallback and log it. The card fails the catch-all that hides which call was never implemented.
