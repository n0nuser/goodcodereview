---
id: mod-pooled-clients-built-once
level: module
tags: [performance, resources]
severity: should-fix
status: stable
lang: core
applies_when: Code creates a network or database client.
tool_gate: none
borrowed_from:
  - https://learn.microsoft.com/en-us/azure/architecture/antipatterns/improper-instantiation/
  - https://pkg.go.dev/net/http#Client
  - https://requests.readthedocs.io/en/latest/user/advanced/
  - https://nodejs.org/api/http.html#class-httpagent
---

**Rule.** Build pooled clients once at startup and reuse them.

**Why.** A client per call defeats connection pooling, leaks sockets, and pays a handshake every time. When a client must be short-lived, close it when the work ends.

**FAIL**

```csharp
async Task<string> Fetch(string url) {
    using var client = new HttpClient();     // new pool and socket per call
    return await client.GetStringAsync(url);
}
```

**PASS**

```csharp
static readonly HttpClient Client = new() { Timeout = TimeSpan.FromSeconds(10) };   // once

async Task<string> Fetch(string url) => await Client.GetStringAsync(url);
```

**Counterpoint.** "A throwaway client is simpler." For a one-off script, yes (scope it with `with`). On a server path it exhausts sockets under load.
