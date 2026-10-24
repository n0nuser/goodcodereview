---
id: sys-n-plus-one-pooling
level: system
tags: [performance, database]
severity: should-fix
status: stable
note: N+1 half has 4 orgs (Django, Rails, SQLAlchemy, Microsoft); the bounded pool rests on 3 partial sources; the index clause has no source beyond topic level
lang: core
applies_when: Code loads related rows in a loop, or opens database connections per request.
tool_gate: Query-count assertion in tests; ORM N+1 detector.
borrowed_from:
  - https://docs.djangoproject.com/en/stable/ref/models/querysets/
  - https://guides.rubyonrails.org/active_record_querying.html
  - https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html
  - https://learn.microsoft.com/en-us/azure/architecture/antipatterns/chatty-io/
  - https://nodejs.org/api/http.html#class-httpagent
  - https://www.pgbouncer.org/features.html
  - https://www.postgresql.org/docs/current/runtime-config-connection.html
---

**Rule.** Fetch related rows in one query or batch, never one query per row.

**Why.** A query per row multiplies latency by result size. Also back filter and join columns with an index and use a bounded connection pool: an unindexed filter turns each query into a scan, and a connection per request exhausts the database under load.

**FAIL**

```python
for o in Order.objects.all():
    print(o.user.email)                              # one query per order
```

**PASS**

```python
for o in Order.objects.select_related("user"):
    print(o.user.email)                              # one query with a join
```

**Counterpoint.** "Measure first." Yes, for micro-optimizations, but a query inside a loop over unbounded input is a defect by shape.
