---
id: fn-independent-work-concurrent
level: function
tags: [performance, correctness, concurrency]
severity: should-fix
status: stable
note: Start independent work together: Python, Mozilla, Go (errgroup). Sequence only when one call needs another's result: Mozilla, Microsoft (a vendor), Apple (a vendor); the cursor/plugins skill is opinion and supports it
lang: core
applies_when: A function awaits or calls several I/O operations that do not depend on each other.
tool_gate: none
borrowed_from:
  - https://pkg.go.dev/golang.org/x/sync/errgroup
  - https://github.com/cursor/plugins/blob/main/thermos/skills/thermo-nuclear-code-quality-review/SKILL.md
  - https://docs.python.org/3/library/asyncio-task.html
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all
  - https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/
  - https://developer.apple.com/videos/play/wwdc2025/268/
---

**Rule.** Start independent I/O together and wait for all of it; run calls in sequence only when one needs the result of another.

**Why.** Sequential awaits add their latencies. Three 200 ms calls take 600 ms in a row and 200 ms together.

**FAIL**

```python
user = await get_user(uid)
orders = await get_orders(uid)       # does not use `user`
prefs = await get_prefs(uid)
```

**PASS**

```python
user, orders, prefs = await asyncio.gather(
    get_user(uid), get_orders(uid), get_prefs(uid))
```

**Counterpoint.** "Parallel calls load the dependency harder and complicate errors." Cap fan-out with a semaphore or pool, and use a task group so one failure cancels the rest. A deliberate order, for rate limits or ordering, is a valid reason. Write it down.
