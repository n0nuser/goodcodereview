---
id: svc-server-read-timeouts
level: service
tags: [security, reliability, http]
severity: should-fix
status: draft
lacks: orgs, Cloudflare (Go) and Node.js only; needs one more org that sets server read and header timeouts for untrusted clients
lang: core
applies_when: The service runs its own HTTP server and untrusted clients or networks can reach it.
context: [server]
tool_gate: A slow-client test (send headers one byte at a time) that expects the connection closed; a lint that flags a server built without timeouts.
borrowed_from:
  - https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/
  - https://nodejs.org/api/http.html#class-httpagent
---

**Rule.** Set a header-read timeout and a request-read timeout on a server that faces untrusted clients.

**Why.** Without them, a client that sends one byte a minute holds a connection and a worker for as long as it likes. A few hundred such clients exhaust the server. A zero value means no limit, so a missing setting is the failure. Set the timeouts in the server itself, even when a proxy sits in front, because the server may be reached without it.

**FAIL**

```go
// No timeouts: a slow client can hold the connection open forever.
log.Fatal(http.ListenAndServe(":8080", mux))
```

**PASS**

```go
srv := &http.Server{
    Addr:              ":8080",
    Handler:           mux,
    ReadHeaderTimeout: 5 * time.Second,
    ReadTimeout:       30 * time.Second,
}
log.Fatal(srv.ListenAndServe())
```

**Counterpoint.** "Large uploads and slow mobile links need more time." Raise the limit for the route that needs it, or stream the body with its own deadline, and keep the short default elsewhere. A long limit is a choice. An unlimited one is a hole.
