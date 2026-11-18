---
id: cpp-no-c-style-cast
level: function
tags: [correctness, maintainability, cpp]
severity: should-fix
status: draft
lacks: orgs, LLVM and Google state it; a third independent organisation is missing
lang: cpp
applies_when: C++ code converts a value or pointer to another type.
tool_gate: clang-tidy `google-readability-casting` and `cppcoreguidelines-pro-type-cstyle-cast`; GCC and Clang `-Wold-style-cast`.
borrowed_from:
  - https://llvm.org/docs/CodingStandards.html
  - https://google.github.io/styleguide/cppguide.html
---

**Rule.** Use C++ casts (`static_cast`, `const_cast`, `reinterpret_cast`), never a C-style cast.

**Why.** A C-style cast picks whichever conversion compiles, including `reinterpret_cast` and a `const` strip, and it does not say which. A later type change can turn a safe cast into an unsafe one with no diagnostic. A named cast states the intent, fails to compile when the types stop fitting, and is easy to search for.

**FAIL**

```cpp
void use(const Base *b, double x) {
  Derived *d = (Derived *)b;   // drops const and downcasts
  int n = (int)x;
}
```

**PASS**

```cpp
void use(const Base *b, double x) {
  const auto *d = static_cast<const Derived *>(b);
  int n = static_cast<int>(x);
}
```

**Counterpoint.** "`static_cast<int>(x)` is noise next to `(int)x`." The noise is the point: each cast is a place a reviewer must check. For arithmetic types, `int{x}` is shorter and rejects a narrowing conversion.
