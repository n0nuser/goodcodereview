---
id: mod-deep-modules
level: module
tags: [maintainability, design]
severity: discuss
status: stable
lang: core
applies_when: A new class or module is introduced, or an existing interface grows.
tool_gate: none
borrowed_from:
  - https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/abstractions-abstract-types-and-interfaces
  - https://rust-lang.github.io/api-guidelines/future-proofing.html
  - https://go.dev/wiki/CodeReviewComments
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md
note: a small interface, nothing more than callers need - Microsoft Framework Design Guidelines ("no more and no fewer" members), Rust API Guidelines (hide the representation, "promise less to the client"), Go review comments (do not define an interface before it is used); the "interface as complex as the implementation" test is Ousterhout alone and sits in the Why
---

**Rule.** Prefer a small interface that hides its implementation, and add a member only when callers need it.

**Why.** An interface with too many members is hard to learn and hard to implement, and a public detail is a commitment you cannot change later. A shallow module, whose interface is nearly as complex as its implementation, charges the reader the cost of learning it and returns nothing. The complexity moves; it does not shrink.

**FAIL**

```text
class Reader:
    def open(self); def read_line(self); def set_encoding(self, e); def close(self)
    # caller must sequence all four; same work in a function would be one call
```

**PASS**

```text
def read_lines(path, encoding="utf-8") -> list[str]: ...
```

**Counterpoint.** Ousterhout and Martin disagree. Martin favours many very small functions, and Ousterhout says that yields shallow, entangled pieces. Evidence is thin on both sides. Ask the local question: does the split help a reader here?