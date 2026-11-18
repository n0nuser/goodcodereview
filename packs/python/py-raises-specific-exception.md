---
id: py-raises-specific-exception
level: function
tags: [testing, python]
severity: should-fix
status: draft
lacks: orgs, bare-Exception clause has flake8-bugbear and pytest only; needs one more org
lang: python
applies_when: A test asserts that code raises an exception.
tool_gate: ruff B017 (assert-raises-exception), flake8-bugbear B017.
borrowed_from:
  - https://github.com/PyCQA/flake8-bugbear#readme
  - https://docs.pytest.org/en/stable/reference/reference.html
---

**Rule.** In a test, assert the specific exception type, never bare `Exception`.

**Why.** `Exception` is the base of almost every error, so `pytest.raises(Exception)` passes when a typo or a refactor raises something else, even when the code under test never runs. The test stays green and checks nothing.

**FAIL**

```python
import pytest

def test_rejects_negative():
    with pytest.raises(Exception):
        withdraw(account, -5)
```

**PASS**

```python
import pytest

def test_rejects_negative():
    with pytest.raises(ValueError, match="negative"):
        withdraw(account, -5)
```

**Counterpoint.** "The test should not care which error type." If the type is not part of the contract, the contract is too loose: name an error type for it. Use `Exception` only when any failure truly counts, and say so in a comment.
