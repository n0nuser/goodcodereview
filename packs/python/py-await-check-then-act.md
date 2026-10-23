---
id: py-await-check-then-act
level: function
tags: [python, concurrency]
severity: block
status: draft
lang: python
applies_when: An `async def` reads state, awaits, then writes based on that read.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Do not rely on `asyncio.Lock` or the single-threaded event loop to make check-then-act safe.

**Why.** Core rule: [[fn-no-check-then-act-across-await]]. In Python the loop is single-threaded only between awaits, and an `asyncio.Lock` covers one process; the guard has to live where the state lives.

**FAIL**

```python
async with lock:                       # one process only
    bal = await repo.get_balance(acct)
    if bal >= amt:
        await repo.set_balance(acct, bal - amt)
```

**PASS**

```python
result = await session.execute(
    update(Account)
    .where(Account.id == acct, Account.balance >= amt)
    .values(balance=Account.balance - amt)
)
if result.rowcount == 0:
    raise InsufficientFunds(acct)
```

**Counterpoint.** "asyncio is single-threaded, so there is no race." True only between awaits; every await is a point where another task runs, and a second worker process shares no lock.
