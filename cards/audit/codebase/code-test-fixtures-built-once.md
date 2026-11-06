---
id: code-test-fixtures-built-once
level: codebase
tags: [testing, performance, ci, fixtures]
severity: should-fix
status: stable
lang: core
applies_when: Auditing a test suite in which many tests share an expensive setup (a database schema and seed data, a container, a loaded application context).
tool_gate: A CI job timeout plus a slowest-tests report in the build log (pytest or Django --durations, Gradle build scan).
note: build once - Django (setUpTestData), Spring (context cache), Laravel (RefreshDatabase skips the migration), Microsoft (create and seed "exactly once"), Alloy.ai (migrate once per suite), GitLab (let_it_be); reset by rollback - Django, Rails, Spring, Laravel, Ecto, SQLAlchemy, Microsoft, Alloy.ai, GitLab; truncate for tests that must commit - Django, Microsoft
borrowed_from:
  - https://docs.djangoproject.com/en/5.1/topics/testing/tools/
  - https://guides.rubyonrails.org/testing.html
  - https://docs.spring.io/spring-framework/reference/testing/testcontext-framework/ctx-management/caching.html
  - https://docs.spring.io/spring-framework/reference/testing/testcontext-framework/tx.html
  - https://laravel.com/docs/12.x/database-testing
  - https://hexdocs.pm/ecto_sql/Ecto.Adapters.SQL.Sandbox.html
  - https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
  - https://learn.microsoft.com/en-us/ef/core/testing/testing-with-the-database
  - https://alloy.ai/speeding-up-integration-tests-db
  - https://docs.gitlab.com/development/testing_guide/best_practices/
---

**Rule.** Build an expensive fixture once per test run, and reset state between tests with a rollback or a truncate, never a rebuild.

**Why.** A fixture that takes 20 seconds costs 20 seconds times the number of tests that rebuild it, and adding tests adds that cost again. One team measured about 10 seconds to drop, recreate and migrate a database per test and a 14-minute suite for 78 integration tests; wrapping each test in a rolled-back transaction cut it to 8 minutes. A slow suite then gets skipped locally, and changes arrive in larger, riskier batches.

**FAIL**

```text
before each test:
    create database; run all migrations; load seed data     # 20-30 s
after each test:
    drop database
```

**PASS**

```text
once per run (session, test binary, or global setup):
    create database; run all migrations; load seed data
before each test:  begin a transaction (or savepoint)
after each test:   roll it back
tests that must commit: their own database, cleaned with DELETE or TRUNCATE after each test, run serially
```

**Counterpoint.** "A shared fixture breaks test isolation and blocks parallel runs." It does when the shared part is mutable or when tests commit. Keep the shared part read-only, undo each test's writes by rollback, give each parallel worker its own database, and give the few tests that must commit a separate database. A database kept between runs goes stale after a schema change, so rebuild it when the migrations change.
