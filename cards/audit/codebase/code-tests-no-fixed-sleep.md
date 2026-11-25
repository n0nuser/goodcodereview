---
id: code-tests-no-fixed-sleep
level: codebase
tags: [testing, reliability, ci]
severity: should-fix
status: stable
lang: core
applies_when: Auditing a test suite, or reviewing a diff that adds or changes a test that waits for something to happen.
tool_gate: Grep the test directories for sleep calls (`time.sleep`, `Thread.sleep`, `cy.wait(<number>)`) and fail CI on a new one.
note: Google (small tests may not sleep or do I/O), Microsoft (avoid sleeps in unit tests) and Cypress (no arbitrary waits) back the sleep clause. The I/O half has Google and Microsoft only, with GitLab descriptive, so it sits in the Why
borrowed_from:
  - https://abseil.io/resources/swe-book/html/ch11.html
  - https://microsoft.github.io/code-with-engineering-playbook/automated-testing/unit-testing/
  - https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices
  - https://docs.cypress.io/app/core-concepts/best-practices
---

**Rule.** Do not wait in a test on a fixed delay; wait for the condition you need, or inject a clock.

**Why.** A delay that is long enough on a fast machine is too short on a loaded CI runner, so the test turns flaky, and it adds its whole length to every run even when the thing it waits for finished at once. A sleep also often means the code reaches a dependency the test should have replaced. For the same reasons, small unit tests do no real network, database or file-system I/O.

**FAIL**

```python
import time
from concurrent.futures import ThreadPoolExecutor

def test_job_finishes():
    pool = ThreadPoolExecutor()
    future = pool.submit(run_job)
    time.sleep(5)
    assert future.done()
```

**PASS**

```python
from concurrent.futures import ThreadPoolExecutor

def test_job_finishes():
    with ThreadPoolExecutor() as pool:
        future = pool.submit(run_job)
        assert future.result(timeout=5) == "done"
```

**Counterpoint.** "Some systems give no signal to wait on, so polling with a sleep is the only way." Poll with a short interval and a deadline, and return as soon as the condition holds, so the delay is a ceiling and not a cost. End-to-end and integration tests legitimately use real I/O and polling; the rule bans the fixed wait, not the poll.
