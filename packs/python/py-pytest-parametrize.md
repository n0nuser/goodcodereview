---
id: py-pytest-parametrize
level: function
tags: [python, testing]
severity: should-fix
status: draft
lang: python
applies_when: Tests differ only in inputs and expected values.
tool_gate: ruff PT006/PT007 (style only)
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Use `@pytest.mark.parametrize` for test variations.

**Why.** Copy-pasted tests drift, and an empty parametrization silently runs nothing. Assert a computed parameter list is not empty first.

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

**Counterpoint.** "Separate tests give clearer failures." Parametrize ids give one failure per case with its inputs. For a computed list, `assert cases` before parametrising.
