---
id: sys-append-only-stores-have-retention
level: system
tags: [reliability, performance, data, memory]
severity: should-fix
status: draft
lacks: evidence, each source is one product's retention setting for its own store; none states the practice for your own tables
lang: core
applies_when: The system keeps a table, file, index or in-memory map that gains an entry for each event, request or job and that no code removes entries from.
tool_gate: Retention settings in config (log rotation, index lifecycle policy, TTL or partition drop job); a check that every table named `*_events`, `*_log` or `*_history` has one.
note: Backed by Kubernetes (finished-job TTL and history limits), Prometheus (retention time and size), Docker (log max-size and max-file) and Elastic (lifecycle policies). other cards cover caches and personal data; this card covers any store that only grows
borrowed_from:
  - https://kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/
  - https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.docker.com/engine/logging/drivers/json-file/
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html
  - https://www.postgresql.org/docs/current/ddl-partitioning.html
---

**Rule.** Give every store that only grows (event, audit and history tables, log files, finished-job registries) a maximum age or count, and a job or setting that enforces it.

**Why.** Such a store grows with traffic, not with the feature. It fills the disk, slows scans and backups, or exhausts memory months after launch. and maps. Deleting old rows in bulk is slow; dropping a partition is cheap.

**FAIL**

```python
JOBS: dict[str, JobResult] = {}      # every finished job stays in memory until restart

def finish(job_id, result):
    JOBS[job_id] = result
```

```sql
CREATE TABLE audit_events (id bigserial, at timestamptz, payload jsonb);  -- nothing ever deletes rows
```

**PASS**

```python
class JobRegistry:
    def __init__(self):
        self._jobs = TTLCache(maxsize=5_000, ttl=3600)   # finished jobs expire after an hour

    def finish(self, job_id, result):
        self._jobs[job_id] = result
```

```sql
CREATE TABLE audit_events (id bigserial, at timestamptz NOT NULL, payload jsonb)
  PARTITION BY RANGE (at);               -- monthly partitions; a job detaches and drops those past 13 months
```

**Counterpoint.** "Audit data must never be deleted." Then the retention rule is the legal period plus a move to cheaper storage, not forever on the primary database. The card fails a store with no decision, not a long period you chose and wrote down.
