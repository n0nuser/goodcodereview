---
id: sys-lock-fencing
level: system
tags: [locks, correctness, distributed]
severity: block
status: draft
lang: core
applies_when: A TTL lock or lease guards a write to an external store.
tool_gate: none
borrowed_from:
  - https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
  - https://antirez.com/news/101
  - https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/
---

**Rule.** If a lock protects correctness, the write must be checked on the resource side (fencing token or compare-and-set); holding the lock is not proof.

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

**Counterpoint.** Sources disagree. Kleppmann says Redlock gives no monotonic token and so is unsafe for correctness; antirez answers that a random unique token with check-and-set suffices and that ordered tokens need a linearizable store. Both agree locks used only for efficiency may be loose. So: state which kind of lock it is; for correctness, require a resource-side check, do not rule on Redlock itself.
