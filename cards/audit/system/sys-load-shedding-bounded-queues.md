---
id: sys-load-shedding-bounded-queues
level: system
tags: [overload, queues]
severity: block
status: draft
lang: core
applies_when: Work is buffered in a queue, channel or thread pool between components.
tool_gate: Lint for unbounded queue constructors.
borrowed_from:
  - https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/
  - https://aws.amazon.com/builders-library/fairness-in-multi-tenant-systems/
---

**Rule.** Bound every queue and reject excess work cheaply.

**Why.** An unbounded queue turns overload into minutes of latency; by the time old items are served, callers have given up. Also keep a way to sideline old or excess messages (see PASS).

**FAIL**

```text
q = Queue()                      # no maxsize
on overload: enqueue anyway; no age alarm, no spillover
```

**PASS**

```text
q = Queue(maxsize=1000); if full: return 503 fast
alarm on age of oldest item; spillover queue for old deltas
```

**Counterpoint.** "Dropping work loses data." A bounded queue only makes the loss explicit and early; for work that must not be lost, spill to durable storage rather than memory. AWS notes shedding itself must be cheap, and that deliberately slowing fast errors can stop a load balancer from steering more traffic at a shedding host.
