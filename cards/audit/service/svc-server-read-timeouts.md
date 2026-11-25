---
id: svc-server-read-timeouts
level: service
tags: [security, reliability, http]
severity: should-fix
status: draft
lacks: orgs, request-read timeout has Cloudflare and Envoy firm; header-read timeout has no firm org; Node, Kestrel, nginx and Apache pages only describe options
lang: core
applies_when: The service runs its own HTTP server and untrusted clients or networks can reach it.
context: [server]
tool_gate: A slow-client test (send headers one byte at a time) that expects the connection closed; a lint that flags a server built without timeouts.
note: Cloudflare says the package-level Go server functions are unfit for public servers because timeouts stay off. Envoy lists request_timeout and stream_idle_timeout among the values to change for an edge proxy. The Node, Kestrel, nginx and Apache pages describe options and recommend nothing, so they are soft
borrowed_from:
  - https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/
  - https://nodejs.org/api/http.html#class-httpagent
  - https://www.envoyproxy.io/docs/envoy/latest/configuration/best_practices/edge
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel/options
  - https://nginx.org/en/docs/http/ngx_http_core_module.html
  - https://httpd.apache.org/docs/2.4/mod/mod_reqtimeout.html
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
