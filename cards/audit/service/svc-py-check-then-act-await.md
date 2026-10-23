---
id: svc-py-check-then-act-await
level: service
tags: [asyncio, races]
severity: should-fix
status: draft
lang: python
applies_when: Async code reads shared state, awaits, then acts on the earlier read.
tool_gate: none
borrowed_from: []
---

**Rule.** Do not check a condition, `await`, then act as if the condition still holds; make check and act atomic (no await between) or guard with a lock or a database constraint.

**Why.** Every `await` is a point where other tasks run. The "single-threaded so no races" belief fails exactly here: two tasks both see the slot free and both take it.

**FAIL**

```python
if user_id not in sessions:
    sessions[user_id] = await create_session(user_id)   # two tasks both create
```

**PASS**

```python
async with locks[user_id]:
    if user_id not in sessions:
        sessions[user_id] = await create_session(user_id)
```

**Counterpoint.** "Rare in practice." It appears under load and is unreproducible in tests. This is standard event-loop semantics, but docs/research has no source naming this pattern, so the card is draft until one is added.
