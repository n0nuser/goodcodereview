---
id: sys-load-shedding-bounded-queues
level: system
tags: [reliability, overload, queues]
severity: block
status: stable
lang: core
applies_when: Work is buffered in a queue, a channel, or a thread pool between components.
context: [server]
tool_gate: Lint for unbounded queue constructors.
note: Dropping requests that waited too long has AWS, Google SRE (CoDel and LIFO) and Uber (shedding stale work); Netflix says nothing about queue age
borrowed_from:
  - https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/
  - https://aws.amazon.com/builders-library/fairness-in-multi-tenant-systems/
  - https://sre.google/sre-book/addressing-cascading-failures/
  - https://sre.google/sre-book/handling-overload/
  - https://github.com/Netflix/concurrency-limits
  - https://www.uber.com/es/en/blog/from-static-rate-limiting-to-intelligent-load-management/
  - https://builder.aws.com/content/3Eun1EEyX6p2e3VYNyRLSJzLuMV/using-load-shedding-to-avoid-overload
---

**Rule.** Bound every queue, reject excess work cheaply, and drop queued requests whose caller has already given up.

**Why.** An unbounded queue turns overload into minutes of latency, and by the time old items are served, callers have given up. Also keep a way to sideline old or excess messages (see PASS). When something must go, shed the lowest-priority work first.

**FAIL**

```text
q = Queue()                      # no maxsize
on overload: enqueue anyway; no age alarm, no spillover
```

**PASS**

```text
q = Queue(maxsize=1000); if full: return 503 fast
alarm on age of oldest item; spillover queue for old deltas
drop a request that has waited past the caller's timeout
```

**Counterpoint.** "Dropping work loses data." A bounded queue only makes the loss explicit and early. For work that must not be lost, spill to durable storage rather than memory. Shedding itself must be cheap. Slowing fast errors on purpose can stop a load balancer from steering more traffic at a shedding host.
