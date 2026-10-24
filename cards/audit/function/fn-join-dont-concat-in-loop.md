---
id: fn-join-dont-concat-in-loop
level: function
tags: [performance, strings]
severity: should-fix
status: draft
lang: core
applies_when: A function builds a string from pieces in a loop whose length depends on input.
tool_gate: Linter rule for string concatenation in a loop (for example ruff PERF or a .NET analyzer).
borrowed_from:
  - https://docs.python.org/3/faq/programming.html
  - https://pkg.go.dev/strings#Builder
  - https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/strings/common-tasks/concatenate
---

**Rule.** Build a string from a loop with a builder or a join, never with repeated `+=`.

**Why.** Strings are immutable in Python, Go, Java, and .NET, so each `+=` copies everything built so far. Over n pieces the total cost grows with the square of the output length.

**FAIL**

```python
out = ""
for row in rows:
    out += f"{row.id},{row.name}\n"
```

**PASS**

```python
out = "".join(f"{row.id},{row.name}\n" for row in rows)
```

**Counterpoint.** "CPython optimises `+=` in place." Sometimes, and only in CPython, and the language FAQ still says to join. A small fixed number of pieces is fine with `+` or an f-string, which read better. The rule covers loops over input-sized data.
