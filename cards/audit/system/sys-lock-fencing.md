---
id: sys-lock-fencing
level: system
tags: [reliability, correctness, locks, distributed]
severity: block
status: stable
lang: core
applies_when: A TTL lock or lease guards a write to an external store.
tool_gate: none
note: Apache Hadoop and Hazelcast state the rule; Hazelcast is a vendor and its page draws on Chubby and Kleppmann. Microsoft and AWS, both vendors, state the compare-and-set arm only. The Google Chubby link serves the abstract and does not count. The AWS Builders Library leader-election page backs the Why only; it names the hazard and never says to check at the resource
borrowed_from:
  - https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
  - https://antirez.com/news/101
  - https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/
  - https://research.google/pubs/the-chubby-lock-service-for-loosely-coupled-distributed-systems/
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html
  - https://docs.hazelcast.com/hazelcast/5.7/data-structures/fencedlock
  - https://learn.microsoft.com/en-us/azure/storage/blobs/concurrency-manage
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html
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


**Counterpoint.** "Our lock library is safe, so holding the lock is enough." Whether a given algorithm such as Redlock is safe is disputed, but that a paused holder can still write is not. Locks used only for efficiency (avoiding duplicate work) may be loose. For correctness, state that it is a correctness lock and make the store reject stale writers, with a monotonically increasing token or a unique token checked by compare-and-set, whatever the lock implementation.

**See also.** [[svc-idempotency-key]].
