---
id: fn-regex-compiled-once
level: function
tags: [performance]
severity: should-fix
status: stable
lang: core
applies_when: Code builds a regular expression or similar compiled matcher inside a loop or a function that runs per request.
tool_gate: Linter rule for a regex constructor in a loop, where the language has one.
note: 4 orgs back it; only the Rust docs state the loop rule outright, and Python and .NET cache recent patterns, so a few module-level calls are not a failure
borrowed_from:
  - https://docs.rs/regex/latest/regex/
  - https://pkg.go.dev/regexp
  - https://docs.python.org/3/library/re.html
  - https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-regex
---

**Rule.** Compile a regular expression once, at module or startup level, and reuse it.

**Why.** Compiling costs far more than matching and throws away reusable allocations. Inside a loop or a per-request function, the cost repeats on every call.

**FAIL**

```go
func valid(s string) bool {
	return regexp.MustCompile(`^[a-z]+$`).MatchString(s)   // compiled per call
}
```

**PASS**

```go
var lower = regexp.MustCompile(`^[a-z]+$`)

func valid(s string) bool { return lower.MatchString(s) }
```

**Counterpoint.** "The library caches patterns." Python and .NET keep recently used patterns, so a few static calls are fine. A pattern built from input or an unbounded set of patterns defeats the cache.
