---
id: sys-n-plus-one-pooling
level: system
tags: [database, performance]
severity: should-fix
status: draft
lang: core
applies_when: Code loads related rows in a loop, or opens database connections per request.
tool_gate: Query-count assertion in tests; ORM N+1 detector.
borrowed_from: []
---

**Rule.** Fetch related data in one query or batch, back every filter and join column with an index, and use a bounded connection pool.

**Why.** A query per row multiplies latency by result size; an unindexed filter turns each query into a scan; a connection per request exhausts the database under load.

**FAIL**

```text
for o in orders: o.user = db.get_user(o.user_id)    # N+1
db = connect()  # per request
```

**PASS**

```text
users = db.get_users(ids=[o.user_id for o in orders])
pool = Pool(max=20)
```

**Counterpoint.** "Measure first." Yes, for micro-optimizations; but a query inside a loop over unbounded input is a defect by shape. docs/research has no source for this card (the notes name only a bulkhead pool pattern), so it stays draft until one is added.
