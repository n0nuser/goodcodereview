---
id: fn-no-stringly-typed-returns
level: function
tags: [correctness, compatibility, types, api]
severity: should-fix
status: draft
lacks: orgs, "closed type for a returned status" has Microsoft and Apple; Rust covers arguments and Kotlin is a feature page; needs one more org
lang: core
applies_when: A function returns a status, kind or outcome as a string, and callers branch on it.
tool_gate: partial: mypy with `--enable-error-code exhaustive-match` (or `assert_never`) flags a `match` that misses a case of an enum or Literal return type; a `-> str` return is not flagged
note: Microsoft (an enum for parameters, properties and return values) and Apple (replace a string constant with an enum or a raw-value struct) state the practice for strings; Rust's C-CUSTOM-TYPE covers arguments and booleans, and Kotlin's page describes sealed classes. A boolean flag belongs to fn-bool-arg-at-callsite and a switch over variants to fn-variants-as-tagged-union. Microsoft's open-set exception is the counterpoint
borrowed_from:
  - https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/enum
  - https://developer.apple.com/videos/play/wwdc2020/10680/
  - https://rust-lang.github.io/api-guidelines/type-safety.html
  - https://kotlinlang.org/docs/sealed-classes.html
---

**Rule.** Return a closed type (an enum, a tagged union or a sealed hierarchy) for a closed set of values, not a bare string. For a boolean flag, see [[fn-bool-arg-at-callsite]].

**Why.** The compiler cannot see the set. A typo or an unhandled case compiles and takes the wrong branch. Microsoft says to use an enum to strongly type "parameters, properties, and return values that represent sets of values". Kotlin's sealed hierarchy lets the compiler "check exhaustively that all possible cases are covered".

**FAIL**

```text
def check(order) -> str:
    return "missing_items" if not order.lines else "ok"
```

**PASS**

```text
class OrderCheck(Enum):
    OK = "ok"
    MISSING_ITEMS = "missing_items"

def check(order) -> OrderCheck: ...
```

**Counterpoint.** "The value crosses a wire and the set is open." Keep the string on the wire and convert at the boundary; the type is for the code, not the format. An open set stays a string. Where an enum is too heavy, another named type, such as a sealed hierarchy or a newtype, still gives the value a name.
