---
id: sys-shuffle-shard
level: system
tags: [reliability, multitenancy, isolation]
severity: should-fix
status: draft
lacks: orgs, AWS and Airbnb back it; needs one more org that assigns tenants to shuffled worker subsets
lang: core
applies_when: Many tenants share a pool of workers or nodes, and one tenant's traffic or bug can take a worker down.
context: [server]
tool_gate: none
borrowed_from:
  - https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/
  - https://airbnb.tech/infrastructure/building-a-fault-tolerant-metrics-storage-system-at-airbnb/
---

**Rule.** Assign each tenant a shuffled subset of shared workers, so one tenant's fault reaches only a few other tenants.

**Why.** If every tenant can use every worker, one bad tenant can exhaust all of them. With a random subset per tenant, two tenants rarely share all their workers, so one bad tenant leaves most others a healthy worker.

**FAIL**

```python
def workers_for(tenant):
    return ALL_WORKERS              # every tenant on every worker
```

**PASS**

```python
import hashlib, random

def workers_for(tenant, k=4):
    rng = random.Random(hashlib.sha256(tenant.encode()).digest())
    return rng.sample(ALL_WORKERS, k)   # stable subset of k workers
```

**Counterpoint.** "Separate cells isolate better." They do, and they cost whole copies of the stack. Shuffle sharding runs on one shared pool and still leaves most tenants unaffected. Use cells for hard boundaries and this for the shared pool inside one.
