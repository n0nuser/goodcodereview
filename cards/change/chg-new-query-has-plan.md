---
id: chg-new-query-has-plan
level: change
tags: [performance, database]
severity: should-fix
status: draft
lacks: failable, without "attach the plan" a change review has nothing to mark FAIL; attaching has GitLab only
lang: core
applies_when: The change adds or rewrites a SQL query against a table that grows with users or time.
tool_gate: none
note: PostgreSQL, MySQL, and SQLite docs describe the plan, not a review practice; "check the plan before it ships" has 2 orgs (AWS, GitLab); "attach it to the change" has 1 (GitLab); "production-sized data" has 2 (GitLab, PostgreSQL)
borrowed_from:
  - https://www.postgresql.org/docs/current/using-explain.html
  - https://dev.mysql.com/doc/refman/8.4/en/using-explain.html
  - https://www.sqlite.org/eqp.html
  - https://docs.gitlab.com/development/database_review/
  - https://aws.amazon.com/blogs/database/how-postgresql-processes-queries-and-how-to-analyze-them/
---

**Rule.** Attach the query plan for each new or rewritten query on a growing table, taken on production-sized data.

**Why.** A query that reads well can still scan every row. The plan shows a sequential scan or a missing index before the table grows into it, and the author is the person with the query and the data at hand.

**FAIL**

```text
+ SELECT * FROM orders WHERE customer_email = $1
  (description: "adds lookup by email"; no plan, no index)
```

**PASS**

```text
+ CREATE INDEX orders_customer_email_idx ON orders (customer_email);
  EXPLAIN ANALYZE on a 40M-row copy: Index Scan using orders_customer_email_idx, 0.08 ms
```

**Counterpoint.** "The planner changes its mind as data grows, so a plan today proves little." It proves more than no plan. A plan from a tiny dev table does mislead, because small tables scan by design, so take it on data close to production size and say where it came from.
