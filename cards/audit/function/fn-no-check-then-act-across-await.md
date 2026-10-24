---
id: fn-no-check-then-act-across-await
level: function
tags: [correctness, concurrency]
severity: block
status: draft
lang: core
applies_when: Code reads shared state, yields (await, I/O, a lock release), then writes based on the earlier read.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Make check-and-write one atomic operation where the state lives, and never split it across a suspension point.

**Why.** Another task runs at every yield. Two withdrawals both read 100, both pass the check, and the balance goes negative.

**FAIL**

```text
balance = await repo.get_balance(acct)
if balance >= amount:
    await repo.set_balance(acct, balance - amount)
```

**PASS**

```text
# UPDATE accounts SET balance = balance - :amt WHERE id = :id AND balance >= :amt
if not await repo.debit_if_sufficient(acct, amount):
    raise InsufficientFunds(acct)
```

**Counterpoint.** "A lock fixes it." A process-local lock covers one process. With two workers or two hosts, you need a transaction, an atomic statement, an idempotency key, or optimistic concurrency. Name the other readers and writers of that state.
