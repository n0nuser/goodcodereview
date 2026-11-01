---
id: go-test-race-in-ci
level: codebase
tags: [correctness, reliability, testing, go]
severity: should-fix
status: draft
lacks: orgs, only the Go team states it; needs two more organisations
lang: go
applies_when: A Go module uses goroutines, channels or shared state and has CI.
tool_gate: go test -race
borrowed_from:
  - https://go.dev/doc/articles/race_detector
---

**Rule.** CI runs the test suite with `go test -race ./...`.

**Why.** Data races pass ordinary tests and fail in production, rarely and without a trace. The detector finds them only when the racing code runs under test, so the flag has to be on in the run that every change passes.

**FAIL**

```yaml
- run: go test ./...
```

**PASS**

```yaml
- run: go test -race ./...
```

**Counterpoint.** "The race detector slows tests and needs cgo." It costs several times the runtime and memory, so run it on every pull request if the suite is fast; otherwise at least on the main branch.
