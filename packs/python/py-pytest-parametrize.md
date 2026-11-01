---
id: py-pytest-parametrize
level: function
tags: [testing, python]
severity: should-fix
status: stable
lang: python
applies_when: Tests differ only in inputs and expected values.
tool_gate: ruff PT006/PT007 (style only)
borrowed_from:
  - https://go.dev/wiki/TableDrivenTests
  - https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices
  - https://tech.gr.vodafone.com/post/junit-parameterized-tests
  - https://docs.pytest.org/en/stable/how-to/parametrize.html
note: Go (copy-paste a test, use a table), Microsoft (parameterized tests) and Vodafone (three tests that are one test with different inputs) state the practice; pytest documents the tool
---

**Rule.** Write tests that differ only in inputs and expected values as one `@pytest.mark.parametrize` test.

**Why.** Copy-pasted tests drift, and an empty parametrization silently runs nothing. Assert that a computed parameter list is not empty first.

**FAIL**

```python
def test_retry_502(): assert is_retryable(Response(502))
def test_retry_503(): assert is_retryable(Response(503))
```

**PASS**

```python
@pytest.mark.parametrize(("status", "retry"), [(502, True), (503, True), (400, False)])
def test_retries_gateway_errors(status, retry):
    assert is_retryable(httpx.Response(status)) is retry
```

**Counterpoint.** "Separate tests give clearer failures." Parametrize ids give one failure per case, with its inputs. For a computed list, `assert cases` before parametrising.
