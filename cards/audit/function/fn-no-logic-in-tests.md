---
id: fn-no-logic-in-tests
level: function
tags: [testing, maintainability]
severity: discuss
status: stable
lang: core
applies_when: A test body contains if, for, while or switch, or a table test branches on its case.
tool_gate: none; a review check for control flow inside test functions.
borrowed_from:
  - https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices
  - https://github.com/uber-go/guide/blob/master/style.md
  - https://testing.googleblog.com/2014/07/testing-on-toilet-dont-put-logic-in.html
---

**Rule.** Keep `if`, `for`, `while` and `switch` out of test bodies.

**Why.** A test with logic can be wrong itself, and nobody tests the tests. A loop that skips a case or an `if` that skips an assertion turns a failure into a pass. A table test that branches on its case means the cases do not share one expectation.

**FAIL**

```python
def test_discount():
    for qty, expected in [(1, 0), (10, 5), (100, 20)]:
        if qty < 5:
            assert discount(qty) == 0
        else:
            assert discount(qty) == expected
```

**PASS**

```python
@pytest.mark.parametrize("qty, expected", [(1, 0), (10, 5), (100, 20)])
def test_discount(qty, expected):
    assert discount(qty) == expected
```

**Counterpoint.** "A loop over many inputs is shorter." A parameterised test is just as short and reports each case separately. Cases that need different checks are different behaviours, so each gets its own test.
