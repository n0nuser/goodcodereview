---
id: py-task-reference
level: service
tags: [asyncio, concurrency]
severity: block
status: draft
lang: python
applies_when: Python code calls asyncio.create_task or ensure_future.
tool_gate: Ruff RUF006 (asyncio-dangling-task).
borrowed_from:
  - https://docs.python.org/3/library/asyncio-task.html
---

**Rule.** Never discard the result of `create_task`; keep a reference and surface its exceptions, preferably through a `TaskGroup`.

**Why.** The event loop holds only weak references, so an unreferenced task can be garbage-collected mid-run. A task that nobody awaits also loses its exception ("never retrieved").

**FAIL**

```python
asyncio.create_task(send_email(user))   # fire and forget
```

**PASS**

```python
async with asyncio.TaskGroup() as tg:
    tg.create_task(send_email(user))
# or: t = create_task(...); bg.add(t); t.add_done_callback(bg.discard)
```

**See also.** [[py-cancellation]]; for retried background work, [[svc-idempotency-key]].

**Counterpoint.** "The set-and-discard recipe from the docs is enough." It keeps the task alive but still never retrieves the exception, and the docs point to TaskGroup for that. The same reference rule applies to tasks passed to `asyncio.shield`.
