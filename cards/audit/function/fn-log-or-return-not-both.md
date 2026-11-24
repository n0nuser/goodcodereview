---
id: fn-log-or-return-not-both
level: function
tags: [observability, maintainability]
severity: should-fix
status: stable
lang: core
applies_when: A function handles an error by logging it and also returning or rethrowing it.
tool_gate: A linter for log-and-return (Go `errorlint` patterns, SonarQube `S2139`), or a review check.
note: Google (Go best practices), Uber (Go style guide) and Kubernetes (logging guide) state it
borrowed_from:
  - https://google.github.io/styleguide/go/best-practices
  - https://raw.githubusercontent.com/uber-go/guide/master/style.md
  - https://raw.githubusercontent.com/kubernetes/community/master/contributors/devel/sig-instrumentation/logging.md
---

**Rule.** Handle an error once: return it or log it, not both.

**Why.** Each caller up the stack repeats the same log line, so one failure fills the log with copies and hides the real order of events. The caller knows if the error is expected and can log it once, or retry.

**FAIL**

```go
if err != nil {
    log.Printf("could not save: %v", err)
    return err
}
```

**PASS**

```go
if err != nil {
    return fmt.Errorf("save order: %w", err)
}
```

**Counterpoint.** "I want the log at the point of failure." Add context with wrapping and log once at the boundary that decides the outcome. A top-level handler is where logging belongs.
