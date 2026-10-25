---
id: sys-leader-two-leaders
level: system
tags: [reliability, leader-election, idempotency]
severity: should-fix
status: draft
lacks: orgs, AWS is the only backer; needs two more orgs
lang: core
applies_when: A job runs only on an elected leader or lease holder.
tool_gate: none
borrowed_from:
  - https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/
---

**Rule.** Make leader work safe if two leaders overlap: make it idempotent, check the lease before acting, and stop when renewal fails.

**Why.** Lease-based election cannot guarantee exactly one leader. Non-idempotent work during overlap duplicates side effects.

**FAIL**

```text
if am_leader: send_invoices()      # not idempotent, lease never rechecked
```

**PASS**

```text
for inv in pending: if lease.valid(): send_once(inv.id)   # keyed, idempotent
```

**See also.** [[sys-lock-fencing]], [[svc-idempotency-key]].

**Counterpoint.** AWS recommends first asking whether you need a leader at all (idempotent APIs or optimistic locking often suffice). Hardening the leader is the second choice, not the first.
