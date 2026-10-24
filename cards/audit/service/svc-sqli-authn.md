---
id: svc-sqli-authn
level: service
tags: [security, injection, sql]
severity: block
status: stable
note: the id says authn but the card covers SQL injection only; rename it in a change that also fixes docs/COVERAGE.md and the research notes
lang: core
applies_when: The code builds a SQL query that includes request data or other untrusted input.
tool_gate: Bandit B608 (`hardcoded_sql_expressions`), CodeQL `py/sql-injection`.
borrowed_from:
  - https://owasp.org/Top10/2025/
  - https://docs.python.org/3/library/sqlite3.html
  - https://codeql.github.com/codeql-query-help/python/py-sql-injection/
  - https://portswigger.net/web-security/sql-injection
  - https://go.dev/doc/database/sql-injection
---

**Rule.** Pass untrusted data to queries as bound parameters, never by string concatenation or formatting.

**Why.** Concatenated input becomes SQL, so a value of `1 OR 1=1` reads every row and a quote ends the string early. A bound parameter travels apart from the query text, and the database never parses it as SQL.

**FAIL**

```python
db.execute("SELECT * FROM users WHERE id = " + req.id)
db.execute(f"SELECT * FROM users WHERE name = '{name}'")
```

**PASS**

```python
db.execute("SELECT * FROM users WHERE id = %s", (req.id,))
db.execute("SELECT * FROM users WHERE name = %s", (name,))
```

**Counterpoint.** "An ORM makes this moot." Raw fragments still bypass it, and so do table, column and `ORDER BY` names, which cannot be bound. Map those to a fixed allowlist in code.
