---
id: svc-dlq
level: service
tags: [queues, resilience]
severity: should-fix
status: draft
lang: core
applies_when: The code consumes from a queue or stream.
tool_gate: Queue config check for maxReceiveCount and an alarm on DLQ depth.
borrowed_from:
  - https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/
---

**Rule.** Every consumer queue has a dead-letter queue with a max receive count, an alarm when it is non-empty, and a visibility timeout longer than worst-case processing (or an extension).

**Why.** A poison message otherwise loops forever, hides real backlog, and processing that outlives the visibility timeout creates duplicate work.

**FAIL**

```text
queue: orders        # no redrive policy, only alarm is depth
handler runs 90s, visibility_timeout=30s
```

**PASS**

```text
queue: orders  redrive -> orders-dlq (maxReceiveCount=5)
alarm: orders-dlq depth > 0 ; alarm: age of oldest message
```

**Counterpoint.** "A DLQ just hides failures." Only if nobody watches it; the alarm and a replay path are part of the rule.
