---
id: go-vet-lint-gate
level: codebase
tags: [correctness, maintainability, go, tooling]
severity: should-fix
status: draft
lacks: orgs, only Uber states it in a published guide; needs two more organisations
lang: go
applies_when: The repository is a Go module with a CI pipeline.
tool_gate: go vet, staticcheck, errcheck via golangci-lint
borrowed_from:
  - https://github.com/uber-go/guide/blob/master/style.md
---

**Rule.** CI runs `go vet` and a linter set that includes staticcheck and errcheck, and a finding fails the build.

**Why.** These tools catch unchecked errors, misused `Printf` verbs and dead code before a reviewer sees them. If review comments repeat, the gate is missing. Lint the same way across the whole codebase; consistency matters more than the exact set.

**FAIL**

```yaml
- run: go build ./... && go test ./...
```

**PASS**

```yaml
- run: go vet ./...
- uses: golangci/golangci-lint-action@v6   # .golangci.yml enables errcheck, staticcheck
- run: go test ./...
```

**Counterpoint.** "A new linter floods an old codebase." Enable it with `new-from-rev` so only new code is held to it, then widen.
