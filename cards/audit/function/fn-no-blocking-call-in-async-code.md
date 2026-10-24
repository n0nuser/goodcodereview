---
id: fn-no-blocking-call-in-async-code
level: function
tags: [performance, correctness, concurrency, io]
severity: block
status: stable
lang: core
applies_when: Code runs on an event loop or an async runtime (asyncio, Node.js, Tokio, ASP.NET async handlers).
tool_gate: Linter rule for blocking calls in async functions (for example ruff ASYNC); asyncio debug mode flags slow callbacks.
borrowed_from:
  - https://docs.python.org/3/library/asyncio-dev.html
  - https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop
  - https://docs.rs/tokio/latest/tokio/
  - https://learn.microsoft.com/en-us/azure/architecture/antipatterns/synchronous-io/
---

**Rule.** Never make a blocking I/O call or run long CPU work directly in async code; use the async API or hand the work to a thread or worker.

**Why.** An event loop runs one callback at a time. A `time.sleep`, a synchronous HTTP call, or a big hash inside a handler stalls every other request on that loop, not just the slow one.

**FAIL**

```python
async def handler(req):
    data = requests.get(url).json()          # blocks the loop
    digest = hashlib.pbkdf2_hmac("sha256", pw, salt, 600_000)
```

**PASS**

```python
async def handler(req):
    data = (await client.get(url)).json()    # httpx.AsyncClient
    digest = await asyncio.to_thread(hashlib.pbkdf2_hmac, "sha256", pw, salt, 600_000)
```

**Counterpoint.** "This call is fast enough." A short read from a local SSD can be quicker synchronously. Measure it with asyncio debug mode or the runtime's equivalent. A call that crosses the network, or that waits on anything outside the process, is never in that class.
