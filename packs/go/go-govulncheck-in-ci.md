---
id: go-govulncheck-in-ci
level: codebase
tags: [security, go, supply-chain]
severity: should-fix
status: draft
lacks: orgs, only the Go team states it; needs two more organisations that run govulncheck in CI
lang: go
applies_when: The repository is a Go module with a CI pipeline.
tool_gate: govulncheck
borrowed_from:
  - https://go.dev/blog/govulncheck
---

**Rule.** Run `govulncheck ./...` in CI and fail the build on a reported vulnerability that your code calls.

**Why.** Dependencies pick up known vulnerabilities after you pin them. A scan that only runs on a laptop finds them when someone remembers. govulncheck reports only vulnerabilities in functions your code reaches, so a failing run is worth acting on.

**FAIL**

```yaml
jobs:
  test:
    steps:
      - uses: actions/checkout@v4
      - run: go test ./...
```

**PASS**

```yaml
jobs:
  test:
    steps:
      - uses: actions/checkout@v4
      - run: go test ./...
      - run: go run golang.org/x/vuln/cmd/govulncheck@latest ./...
```

**Counterpoint.** "A new advisory breaks an unrelated pull request." That is the signal; the scan needs a fix or a recorded exception. A scheduled run on the main branch keeps the check alive between pull requests.
