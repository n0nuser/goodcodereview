---
id: py-await-check-then-act
level: function
tags: [python, concurrency]
severity: block
status: draft
lang: python
applies_when: An `async def` reads state, awaits, then writes based on that read.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Never split check and write across an `await`: another task runs at each one. Use an atomic statement, transaction, idempotency key or optimistic concurrency. A Python lock covers one process only. Core rule: [[fn-no-check-then-act-across-await]].

**Why.** Concurrent withdrawals both read 100 and both succeed.

**FAIL**

```python
bal = await repo.get_balance(id)
if bal >= amt:
    await repo.set_balance(id, bal - amt)
```

**PASS**

```python
if not await repo.debit_if_sufficient(id, amt):
    raise InsufficientFunds(id)
```

**Counterpoint.** "asyncio is single-threaded, so no race." True only between awaits; every await is a place where another task runs.
