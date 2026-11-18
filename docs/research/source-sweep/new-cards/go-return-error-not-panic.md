---
id: go-return-error-not-panic
level: function
tags: [reliability, go]
severity: should-fix
status: draft
lacks: orgs, Uber and Google state it; a third independent organisation is missing
lang: go
applies_when: A Go function in a library or production path can fail on bad input, I/O, or another expected condition.
tool_gate: none
borrowed_from:
  - https://github.com/uber-go/guide/blob/master/style.md
  - https://go.dev/doc/effective_go
---

**Rule.** Return an `error` for an expected failure; do not `panic` in library or production code.

**Why.** A panic unwinds the whole goroutine and crashes the process unless a caller recovers it. The caller cannot choose to retry, fall back, or report the failure. An `error` value leaves that choice to the caller.

**FAIL**

```go
func LoadConfig(path string) Config {
	data, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		panic(err)
	}
	return cfg
}
```

**PASS**

```go
func LoadConfig(path string) (Config, error) {
	var cfg Config
	data, err := os.ReadFile(path)
	if err != nil {
		return cfg, fmt.Errorf("read config: %w", err)
	}
	if err := json.Unmarshal(data, &cfg); err != nil {
		return cfg, fmt.Errorf("parse config: %w", err)
	}
	return cfg, nil
}
```

**Counterpoint.** "`regexp.MustCompile` panics, and that is fine." It is fine at start-up, on a constant the programmer wrote, where the program cannot run without it. The rule covers failures that input or the environment can cause at run time.
