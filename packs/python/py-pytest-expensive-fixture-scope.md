---
id: py-pytest-expensive-fixture-scope
level: module
tags: [testing, performance, python, fixtures]
severity: should-fix
status: stable
lang: python
applies_when: A pytest or unittest suite builds a database, a container, a client or a model in a fixture that many tests use.
tool_gate: pytest --durations=10 --durations-min=1.0 to find the fixture, and a CI job timeout to hold the line.
note: scope - pytest (module-scoped smtp_connection runs "as quick as a single one"; dynamic scope for slow setups like docker containers), Python (setUpClass for an expensive connection); cached database plus rollback and --reuse-db - pytest-django; the SQLAlchemy recipe for a rolled-back Session - SQLAlchemy
borrowed_from:
  - https://docs.pytest.org/en/stable/how-to/fixtures.html
  - https://docs.python.org/3/library/unittest.html
  - https://pytest-django.readthedocs.io/en/latest/database.html
  - https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
  - https://docs.djangoproject.com/en/5.1/topics/testing/tools/
  - https://github.com/zupo/awesome-pytest-speedup
---

**Rule.** Give an expensive pytest fixture `scope="session"` or `"module"` and isolate each test with a rollback, never a schema build or a seed load inside a function-scoped fixture.

**Why.** pytest destroys a function-scoped fixture after every test, and function scope is the default, so an expensive fixture pays its full cost for each test. A module or session scope pays it once. unittest has the same trade: `setUpClass` builds once per class, `setUp` once per test.

**FAIL**

```python
@pytest.fixture                       # scope defaults to "function"
def db():
    engine = create_engine(TEST_URL)
    Base.metadata.create_all(engine)  # ~25 s, repeated for every test
    seed_reference_data(engine)
    yield engine
    Base.metadata.drop_all(engine)
```

**PASS**

```python
@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_URL)
    Base.metadata.create_all(engine)  # ~25 s, once
    seed_reference_data(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db(engine):
    conn = engine.connect()
    tx = conn.begin()
    session = Session(bind=conn, join_transaction_mode="create_savepoint")
    yield session                     # milliseconds per test
    session.close()
    tx.rollback()
    conn.close()
```

In Django, `pytest-django` already does this: it builds the database once, runs each `db` test in a transaction that it rolls back, and `--reuse-db` skips the rebuild between runs.

**Counterpoint.** "A session fixture is shared, so one test can leak state into the next." That holds for mutable objects, which is why the PASS keeps the engine shared and gives each test its own rolled-back session. A fixture that cannot be reset stays at function scope. Python's own docs warn that shared fixtures break isolation and parallelism, so build the shared part read-only.
