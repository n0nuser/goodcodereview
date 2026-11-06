---
id: py-xdist-worker-isolated-state
level: module
tags: [testing, reliability, python, parallelism]
severity: should-fix
status: stable
lang: python
applies_when: A pytest suite runs in parallel with pytest-xdist (`-n`) and its tests use a database or another shared resource.
tool_gate: none
note: session fixtures run once per worker - pytest-xdist; each xdist process gets its own database by default - pytest-django; PyPI's suite hit cross-test contamination after -n auto and fixed it with a database per worker (191 s to 63 s) - Trail of Bits
borrowed_from:
  - https://pytest-xdist.readthedocs.io/en/stable/how-to.html
  - https://pytest-django.readthedocs.io/en/latest/database.html
  - https://blog.trailofbits.com/2025/05/01/making-pypis-test-suite-81-faster/
---

**Rule.** Under pytest-xdist, give each worker its own database or other mutable resource, keyed by `worker_id`, and build an expensive shared one once with a lock file.

**Why.** Each xdist worker collects its own tests, so a `session` fixture runs once per worker and not once per run. Workers that share one mutable database corrupt each other's tests, and the failures look random. PyPI's suite found this the moment it moved to `-n auto`; per-worker databases fixed it, and execution time fell from 191 s to 63 s.

**FAIL**

```python
@pytest.fixture(scope="session")
def pg_db():
    create_database("tests")      # all workers create and use the same "tests" database
    yield "tests"
```

**PASS**

```python
@pytest.fixture(scope="session")
def pg_db(worker_id):             # "gw0", "gw1", ... or "master" without xdist
    name = f"tests-{worker_id}"
    create_database(name)
    yield name
    drop_database(name)
```

**Counterpoint.** "Building a database per worker multiplies the setup cost." It does, by the number of workers, which is still far less than the number of tests. When one build is too slow even per worker, build it once under a file lock, as the xdist documentation shows, and copy it for each worker with a database template.
