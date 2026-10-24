---
id: fn-fetch-only-needed-data
level: function
tags: [performance, database]
severity: should-fix
status: draft
lang: core
applies_when: A function queries a database or an API and then filters, counts, or sums the result in application code.
tool_gate: none
borrowed_from:
  - https://learn.microsoft.com/en-us/azure/architecture/antipatterns/extraneous-fetching/
  - https://docs.djangoproject.com/en/stable/topics/db/optimization/
  - https://docs.djangoproject.com/en/stable/ref/models/querysets/
  - https://use-the-index-luke.com/sql/clustering/index-only-scan-covering-index
  - https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html
  - https://learn.microsoft.com/en-us/azure/architecture/antipatterns/busy-database/
---

**Rule.** Filter, count, and aggregate in the query, and select only the columns the code uses.

**Why.** Loading every row to count it, or every column to read one, moves data across the network and through memory for nothing. `SELECT *` also rules out an index-only scan.

**FAIL**

```python
total = sum(o.amount for o in Order.objects.all() if o.status == "paid")
n = len(Order.objects.filter(user=u))        # loads every row
```

**PASS**

```python
total = Order.objects.filter(status="paid").aggregate(Sum("amount"))["amount__sum"]
n = Order.objects.filter(user=u).count()
```

**Counterpoint.** "Pushing logic into the database makes it the bottleneck." Microsoft's busy-database guidance agrees for formatting and business rules. Filtering and aggregation are what the database is built for, and moving them out usually ships far more data than it saves.
