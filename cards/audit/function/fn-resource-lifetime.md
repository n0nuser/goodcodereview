---
id: fn-resource-lifetime
level: function
tags: [correctness, concurrency, resources]
severity: block
status: draft
lacks: orgs, one blog post on structured concurrency backs it; needs two more orgs
lang: core
applies_when: Code starts a task, thread, goroutine, or subprocess, or opens a handle (file, socket, connection).
tool_gate: Leak detectors in tests (unclosed-resource warnings, goroutine leak checks).
borrowed_from:
  - https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/
---

**Rule.** Give every task and handle an owner that waits for it or closes it, on the error path too.

**Why.** A task started and forgotten outlives its caller. Its errors vanish, nobody cancels it, and its resources are never released, which shows up later as a leak or a stuck shutdown.

**FAIL**

```python
asyncio.create_task(send_metrics())     # nobody awaits it, nobody cancels it
f = open(path); data = f.read()         # leaked if read() raises
```

**PASS**

```python
async with asyncio.TaskGroup() as tg:   # children finish inside this scope
    tg.create_task(send_metrics())
with open(path) as f:
    data = f.read()
```

**Counterpoint.** "Some work is fire-and-forget by design." Then a long-lived owner (a supervisor or worker pool) holds it, logs its failures, and stops it at shutdown. [[py-task-reference]] covers Python task references.
