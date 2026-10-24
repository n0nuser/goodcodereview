# module

## mod-pooled-clients-built-once

severity: should-fix  
concerns: performance  
applies_when: Code creates a network or database client.

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

## mod-yagni

severity: should-fix  
concerns: maintainability, process  
applies_when: The change adds an abstraction, parameter, hook or option.

**Rule.** Add an abstraction only when the logic is reused, non-trivial, or clutters the main flow; do not build for a need that does not exist yet.

**Why.** Speculative flexibility costs reading time every day and is usually the wrong shape when the need arrives. Reviewers cannot verify a use that does not exist.

**FAIL**

```text
class NotifierFactory: ...   # one product, one caller
def send(msg, retries=3, backoff=None, hook=None): ...   # nobody passes these
```

**PASS**

```text
def send_welcome_email(user): ...
```

**Counterpoint.** "But we will surely need it." Then add it when you do, in a change that has the real second caller to shape it. Optimising for easy change means simple code, not built-in flexibility. Trivial single-use logic stays inline. The cost of waiting is low, and the cost of the wrong guess is not.
