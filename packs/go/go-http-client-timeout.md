---
id: go-http-client-timeout
level: function
tags: [reliability, performance, go, io]
severity: should-fix
status: draft
lacks: orgs, Cloudflare and the Go docs (Google) state it; a third independent organisation is missing
lang: go
applies_when: A Go function makes an HTTP or other network call.
context: [server, cli]
tool_gate: noctx, bodyclose (golangci-lint)
borrowed_from:
  - https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/
  - https://pkg.go.dev/net/http
---

**Rule.** Network calls carry a deadline: a `context.Context` passed to `NewRequestWithContext`, or an `http.Client` with `Timeout`, never `http.DefaultClient` without either.

**Why.** A zero timeout means no timeout. One stalled peer hangs the goroutine, and with it the caller, until the process restarts.

**FAIL**

```go
resp, err := http.Get(url)
```

**PASS**

```go
var client = &http.Client{Timeout: 15 * time.Second}

req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
if err != nil {
	return err
}
resp, err := client.Do(req)
```

**Counterpoint.** "Streaming bodies outlive any fixed timeout." Then set per-phase timeouts on the transport and use the context for the total deadline; keep the deadline.
