---
id: fn-flags-type-for-flag-sets
level: function
tags: [maintainability, correctness]
severity: should-fix
status: draft
lacks: orgs, Microsoft and the Rust API guidelines state it; a third independent organisation is missing
lang: core
applies_when: A type holds a set of independent options that can be combined, such as permissions or render options.
tool_gate: .NET analyzers CA1027 (mark flag enums with FlagsAttribute) and CA2217 (do not mark other enums with it).
borrowed_from:
  - https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/enum
  - https://rust-lang.github.io/api-guidelines/type-safety.html
---

**Rule.** Model a set of independent flags with the language's flags type (a `[Flags]` enum in C#, `bitflags` in Rust), and do not use a plain enum for it.

**Why.** A plain enum holds one value. Code that ORs its members together gets numbers that match no member, which print as a bare integer and fail an equality check. A flags type defines the combination, its printing, and the "no flags" value.

**FAIL**

```csharp
enum Access { Read = 1, Write = 2, Delete = 4 }

var rw = Access.Read | Access.Write;
Console.WriteLine(rw);   // prints 3
```

**PASS**

```csharp
[Flags]
enum Access { None = 0, Read = 1, Write = 2, Delete = 4 }

var rw = Access.Read | Access.Write;
Console.WriteLine(rw);   // prints Read, Write
```

**Counterpoint.** "A plain enum with a `List<Access>` is simpler." For two or three options it can be. Once callers combine and test flags, a list loses the one-value set operations and the compact storage a flags type gives.
