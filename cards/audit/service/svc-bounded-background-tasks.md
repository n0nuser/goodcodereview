---
id: svc-bounded-background-tasks
level: service
tags: [reliability, correctness, concurrency, resilience, async]
severity: block
status: draft
lang: core
applies_when: The code starts a task, goroutine, or thread per item, request, or message.
tool_gate: none
note: the docs give the limiting tools; pairing a semaphore with every spawn site is our inference from them
borrowed_from:
  - https://pkg.go.dev/golang.org/x/sync/errgroup
  - https://go.dev/blog/pipelines
  - https://docs.python.org/3/library/asyncio-sync.html
  - https://docs.rs/tokio/latest/tokio/sync/struct.Semaphore.html
---

**Rule.** Cap how many background tasks run at once, and never spawn one per input with no limit.

**Why.** Input size is not under your control. One task per item works for ten items and exhausts memory, connections, or the downstream service at ten thousand, and the failure lands on everything else in the process. Go's `errgroup.SetLimit`, asyncio's `Semaphore` and Tokio's `Semaphore` exist for exactly this.

**FAIL**

```python
for msg in batch:                       # batch size comes from the queue
    asyncio.create_task(handle(msg))    # 50k messages -> 50k concurrent handlers
```

**PASS**

```python
limit = asyncio.Semaphore(32)

async def bounded(msg):
    async with limit:
        await handle(msg)

async with asyncio.TaskGroup() as tg:
    for msg in batch:
        tg.create_task(bounded(msg))
```

**Counterpoint.** "Tasks are cheap." Creating them is, but what each one holds (a socket, a buffer, a database connection) is not. A worker pool or bounded channel works as well as a semaphore. This card covers work that a service starts for itself. [[sys-load-shedding-bounded-queues]] covers refusing incoming requests under load, and [[fn-resource-lifetime]] covers task lifetime.
