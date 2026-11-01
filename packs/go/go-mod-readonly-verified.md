---
id: go-mod-readonly-verified
level: codebase
tags: [security, reliability, go, supply-chain]
severity: should-fix
status: draft
lacks: orgs, only the Go team states it; needs two more organisations
lang: go
applies_when: The repository is a Go module built in CI.
tool_gate: go mod verify, go mod tidy -diff
borrowed_from:
  - https://go.dev/ref/mod
  - https://go.dev/blog/supply-chain
---

**Rule.** Commit `go.sum`, build in CI with `-mod=readonly`, and run `go mod verify`.

**Why.** `go.sum` pins the hash of every dependency, so a re-uploaded version fails the build. A build that rewrites `go.mod` on its own hides drift. `go mod verify` catches a tampered module cache.

**FAIL**

```yaml
# go.sum is in .gitignore
- run: go mod tidy && go build -mod=mod ./...
```

**PASS**

```yaml
- run: go mod verify
- run: go build -mod=readonly ./...
- run: go mod tidy -diff
```

**Counterpoint.** "The default is already readonly since Go 1.16." True for `go build`; the explicit flag and the `go.sum` check keep a stray `GOFLAGS=-mod=mod` from changing that.
