---
id: sys-leader-two-leaders
level: system
tags: [reliability, leader-election, idempotency]
severity: should-fix
status: draft
lacks: orgs, AWS and Microsoft state it firm; Kubernetes client-go only states that its election does not fence; needs a third org that says to guard leader work
lang: core
applies_when: A job runs only on an elected leader or lease holder.
tool_gate: none
note: Microsoft says to stop leader work when ownership is lost, reject stale-leader writes at the resource, and make replayed operations idempotent. The Kubernetes client-go page states the limit of its election, not a rule, so it is soft
borrowed_from:
  - https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/leader-election
  - https://pkg.go.dev/k8s.io/client-go/tools/leaderelection
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
