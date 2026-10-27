---
id: svc-bounded-background-tasks
level: service
tags: [reliability, correctness, concurrency, resilience, async]
severity: block
status: stable
lang: core
applies_when: The code starts a task, goroutine, or thread per item, request, or message.
tool_gate: none
note: Both clauses are backed by Google (the Go blog, flagged as a vendor), Cabify and AWS (a vendor). AWS states a semaphore and per-workload thread pools that limit concurrency, and its page names the same thread-pool exhaustion the Why describes. errgroup and asyncio supply the limiting tools
borrowed_from:
  - https://pkg.go.dev/golang.org/x/sync/errgroup
  - https://go.dev/blog/pipelines
  - https://docs.python.org/3/library/asyncio-sync.html
  - https://docs.rs/tokio/latest/tokio/sync/struct.Semaphore.html
  - https://tech.cabify.com/blog/engineering/shadow-routing-providers
  - https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/
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
async def worker(queue):
    while (msg := await queue.get()) is not None:
        await handle(msg)

queue = asyncio.Queue(maxsize=100)
async with asyncio.TaskGroup() as tg:
    for _ in range(32):                 # at most 32 handlers at once
        tg.create_task(worker(queue))
    for msg in batch:
        await queue.put(msg)
    for _ in range(32):
        await queue.put(None)           # one stop signal per worker
```

**Counterpoint.** "Tasks are cheap." Creating them is, but what each one holds (a socket, a buffer, a database connection) is not. A semaphore around each handler also caps concurrency, though it still creates one task object per input. This card covers work that a service starts for itself. [[sys-load-shedding-bounded-queues]] covers refusing incoming requests under load.
