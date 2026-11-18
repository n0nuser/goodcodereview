---
id: code-tests-order-independent
level: codebase
tags: [testing, reliability, ci]
severity: should-fix
status: draft
lacks: orgs, GitLab and Alloy back it; Kent Beck is a person and does not count; needs one more org that runs tests in random order or isolates state
lang: core
applies_when: Auditing a test suite for tests that pass alone and fail in a run, or the reverse.
tool_gate: Run the suite in random order in CI (`pytest-randomly`, RSpec `config.order = :random`, `go test -shuffle=on`).
borrowed_from:
  - https://testdesiderata.com/
  - https://docs.gitlab.com/development/testing_guide/best_practices/
  - https://alloy.ai/speeding-up-integration-tests-db
---

**Rule.** Make each test pass in any order, sharing no mutable state with other tests.

**Why.** A test that leans on rows, files or globals another test left behind passes until the order changes, then fails with no change to the code under test. Such failures look like flakes and take hours to trace.

**FAIL**

```python
cache = {}

def test_put():
    cache["a"] = 1
    assert cache["a"] == 1

def test_get():
    assert cache["a"] == 1   # passes only after test_put
```

**PASS**

```python
import pytest

@pytest.fixture
def cache():
    return {}

def test_put(cache):
    cache["a"] = 1
    assert cache["a"] == 1

def test_get(cache):
    cache["a"] = 1
    assert cache["a"] == 1
```

**Counterpoint.** "Random order makes failures hard to reproduce." Print the seed and rerun with it. A failure that appears only in some orders is the bug this finds, and a fixed order hides it until the day someone adds a test.
