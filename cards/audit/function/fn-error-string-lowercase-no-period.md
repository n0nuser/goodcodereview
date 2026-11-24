---
id: fn-error-string-lowercase-no-period
level: function
tags: [maintainability, usability]
severity: discuss
status: stable
lang: core
applies_when: Code builds an error or diagnostic string that callers wrap, print after other text, or show next to other tool output.
tool_gate: Go `staticcheck` `ST1005`, `revive` `error-strings`, Rust `clippy` has no rule; a regex check otherwise.
note: Google (Go review comments and style decisions), Rust (rustc-dev-guide and API guidelines) and LLVM state it. It is for developer-facing and wrapped strings; user-facing UI text follows sentence case with a period
borrowed_from:
  - https://go.dev/wiki/CodeReviewComments
  - https://raw.githubusercontent.com/rust-lang/rustc-dev-guide/master/src/diagnostics.md
  - https://llvm.org/docs/CodingStandards.html
---

**Rule.** Start an error string in lowercase and end it without punctuation when it is wrapped or printed after other context.

**Why.** Wrapped errors join into one line ("open config: read file: permission denied"). A capital or a full stop in the middle reads as a typo and breaks the chain.

**FAIL**

```go
return fmt.Errorf("Failed to read config.")
```

**PASS**

```go
return fmt.Errorf("read config: %w", err)
```

**Counterpoint.** "Messages shown to users should be proper sentences." They should, at the UI layer. Keep the wrapped error lowercase and format the user text where it is shown.
