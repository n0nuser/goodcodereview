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

**Rule.** A Python lock covers one process only: when more than one worker or process can run, make check-then-act an atomic DB statement or constraint.

**Why.** Core rule: [[fn-no-check-then-act-across-await]]. An `asyncio.Lock` does serialise tasks inside one event loop, but a second worker or host shares no lock, so the guard has to live where the state lives.

**FAIL**

```python
async with lock:                       # fine for one process, useless with two workers
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

**Counterpoint.** "asyncio is single-threaded, so a lock or no lock is enough." Within one process an `asyncio.Lock` is correct, and without it every await is a point where another task runs. The rule applies once deployment can run more than one worker, which is the normal case.