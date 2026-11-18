---
id: svc-bound-inbound-concurrency
level: service
tags: [reliability, performance, overload]
severity: should-fix
status: stable
lang: core
applies_when: The service takes requests from callers it does not control.
context: [server]
tool_gate: none
borrowed_from:
  - https://aws.amazon.com/builders-library/dependency-isolation
  - https://docs.rs/tokio/latest/tokio/sync/struct.Semaphore.html
  - https://www.uber.com/es/en/blog/from-static-rate-limiting-to-intelligent-load-management/
  - https://github.com/Netflix/concurrency-limits
---

**Rule.** Cap how many requests a service handles at once with an explicit concurrency limit, and reject the excess. A timeout alone does not bound it.

**Why.** Concurrency is arrival rate times latency. When a dependency slows down, in-flight requests pile up even if every one has a timeout and a retry cap, and the service runs out of threads, memory or connections. A hard limit turns that into fast 503 responses. In-flight count is also a better overload signal than requests per second, because it rises when work gets slower. This card limits inbound requests. Per-dependency limits are in [[svc-circuit-breaker-bulkhead]], background tasks in [[svc-bounded-background-tasks]], and queues in [[sys-load-shedding-bounded-queues]].

**FAIL**

```python
import asyncio

from aiohttp import web

async def handle(request):
    async with asyncio.timeout(5):          # a timeout only; any number of requests can wait here
        return web.json_response(await backend.query(request))
```

**PASS**

```python
import asyncio

from aiohttp import web

limit = asyncio.Semaphore(100)

async def handle(request):
    if limit.locked():
        return web.Response(status=503, headers={"Retry-After": "1"})
    async with limit:
        async with asyncio.timeout(5):
            return web.json_response(await backend.query(request))
```

**Counterpoint.** "Autoscaling adds capacity when load rises." Scaling takes minutes and the pile-up takes seconds. The limit protects the service until new capacity arrives. Set it from a load test, not a guess, and revisit it when the service changes.
