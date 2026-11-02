# Go pack

Draft cards only; the stable Go cards are in the level files. A draft card is not vetted. Report a `FAIL` of one under Draft findings, at `should-fix` at most, never in the ledger or the verdict.

## go-govulncheck-in-ci

level: codebase  
severity: should-fix  
concerns: security  
applies_when: The repository is a Go module with a CI pipeline.  
lacks: orgs, only the Go team states it; needs two more organisations that run govulncheck in CI

Run `govulncheck ./...` in CI and fail the build on a reported vulnerability that your code calls.

## go-http-client-timeout

level: function  
severity: should-fix  
concerns: reliability, performance  
applies_when: A Go function makes an HTTP or other network call.  
context: server, cli  
lacks: orgs, Cloudflare and the Go docs (Google) state it; a third independent organisation is missing

Network calls carry a deadline: a `context.Context` passed to `NewRequestWithContext`, or an `http.Client` with `Timeout`, never `http.DefaultClient` without either.

## go-mod-readonly-verified

level: codebase  
severity: should-fix  
concerns: security, reliability  
applies_when: The repository is a Go module built in CI.  
lacks: orgs, only the Go team states it; needs two more organisations

Commit `go.sum`, build in CI with `-mod=readonly`, and run `go mod verify`.

## go-no-init-side-effects

level: function  
severity: discuss  
concerns: maintainability, correctness  
applies_when: A Go file defines `func init()`.  
lacks: orgs, only Uber states it; needs two more organisations

`init()` does no I/O, reads no environment and does not depend on other `init()` functions; do that work from `main()`.

## go-test-race-in-ci

level: codebase  
severity: should-fix  
concerns: correctness, reliability, testing  
applies_when: A Go module uses goroutines, channels or shared state and has CI.  
lacks: orgs, only the Go team states it; needs two more organisations

CI runs the test suite with `go test -race ./...`.

## go-vet-lint-gate

level: codebase  
severity: should-fix  
concerns: correctness, maintainability  
applies_when: The repository is a Go module with a CI pipeline.  
lacks: orgs, only Uber states it in a published guide; needs two more organisations

CI runs `go vet` and a linter set that includes staticcheck and errcheck, and a finding fails the build.

## go-wrap-errors-with-w

level: function  
severity: should-fix  
concerns: correctness, reliability  
applies_when: A Go function returns an error it received from a call.  
lacks: orgs, Go team and Uber state it; a third independent organisation is missing

Check every returned `err`; when you add context, wrap with `fmt.Errorf("...: %w", err)` unless the cause must stay hidden.
