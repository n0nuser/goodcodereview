---
id: go-wrap-errors-with-w
level: function
tags: [correctness, reliability, go]
severity: should-fix
status: draft
lacks: orgs, Go team and Uber state it; a third independent organisation is missing
lang: go
applies_when: A Go function returns an error it received from a call.
tool_gate: errcheck, errorlint
borrowed_from:
  - https://go.dev/blog/go1.13-errors
  - https://github.com/uber-go/guide/blob/master/style.md
---

**Rule.** Check every returned `err`; when you add context, wrap with `fmt.Errorf("...: %w", err)` unless the cause must stay hidden.

**Why.** `%v` flattens the cause into text, so callers cannot use `errors.Is` or `errors.As`. An ignored `err` turns a failure into silent wrong output.

**FAIL**

```go
data, _ := os.ReadFile(path)
if err := json.Unmarshal(data, &cfg); err != nil {
	return fmt.Errorf("parse config: %v", err)
}
```

**PASS**

```go
data, err := os.ReadFile(path)
if err != nil {
	return fmt.Errorf("read config: %w", err)
}
if err := json.Unmarshal(data, &cfg); err != nil {
	return fmt.Errorf("parse config: %w", err)
}
```

**Counterpoint.** "`%w` makes the wrapped error part of my API." Right: callers may depend on it. Use `%v` at a package boundary when you do not want that, and say so.
