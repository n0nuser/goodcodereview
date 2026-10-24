---
id: sys-lock-fencing
level: system
tags: [locks, correctness, distributed]
severity: block
status: stable
lang: core
applies_when: A TTL lock or lease guards a write to an external store.
tool_gate: none
borrowed_from:
  - https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
  - https://antirez.com/news/101
  - https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/
---

**Rule.** Check a correctness lock on the resource side (fencing token or compare-and-set), never by lock possession alone.

**Why.** A holder can pause past its TTL, lose the lock and still write. Only the store can reject the stale writer.

**FAIL**

```text
if redis.set(key, id, nx=True, px=10000):
    db.update(row)                 # pause here => two writers
```

**PASS**

```text
token = lock.acquire()             # monotonically increasing
db.update(row, where fence < token, set fence = token)
```

**See also.** [[sys-leader-two-leaders]], [[svc-idempotency-key]].

**Counterpoint.** "Our lock library is safe, so holding the lock is enough." Whether a given algorithm such as Redlock is safe is disputed, but that a paused holder can still write is not. Locks used only for efficiency (avoiding duplicate work) may be loose. For correctness, state that it is a correctness lock and make the store reject stale writers, with a monotonically increasing token or a unique token checked by compare-and-set, whatever the lock implementation.
