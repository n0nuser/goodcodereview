---
id: py-cancellation
level: service
tags: [reliability, correctness, asyncio, cancellation]
severity: block
status: draft
lacks: orgs, the asyncio docs are the only backer; needs a second independent source on cancellation
lang: python
applies_when: Async code catches exceptions around awaits or uses asyncio.timeout.
tool_gate: Ruff BLE001 / S110 for broad swallow; lint for CancelledError needs custom rule.
borrowed_from:
  - https://docs.python.org/3/library/asyncio-task.html
---

**Rule.** Re-raise `CancelledError` (do not catch it via bare `except` or `BaseException`), and catch `TimeoutError` outside the `asyncio.timeout()` block.

**Why.** TaskGroup and timeouts are built on cancellation, so swallowing it makes shutdown hang and timeouts silently not fire. The conversion to `TimeoutError` happens at context exit, so a handler inside the block never sees it.

**FAIL**

```python
async with asyncio.timeout(5):
    try: await fetch()
    except TimeoutError: ...        # never reached
    except BaseException: pass      # eats cancellation
```

**PASS**

```python
try:
    async with asyncio.timeout(5):
        await fetch()
except TimeoutError:
    handle_timeout()
```

**Counterpoint.** "Cleanup code must run even on cancel." Clean up in `finally`, then re-raise, and never suppress. `uncancel()` is task bookkeeping, not permission to swallow.
