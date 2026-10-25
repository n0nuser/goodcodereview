---
id: py-test-hygiene
level: module
tags: [testing, python]
severity: discuss
status: draft
lacks: orgs, Shopify backs the Why only; Stripe test clocks are a product feature, so the Rule has no org
lang: python
applies_when: A Python test uses the current date or time, or reaches the network.
tool_gate: pytest-socket (`--disable-socket`)
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Freeze time and block network in tests.

**Why.** Tests that depend on the clock or the network flake, and fail in CI at midnight or offline.

**FAIL**

```python
def test_token_expires():
    token = issue_token(ttl=60)
    assert token.expires_at > datetime.now()
```

**PASS**

```python
from freezegun import freeze_time

@freeze_time("2026-01-01 12:00:00")
def test_token_expires():
    token = issue_token(ttl=60)
    assert token.expires_at == datetime(2026, 1, 1, 12, 1)
# run with: pytest --disable-socket
```

**Counterpoint.** "Real time catches real bugs." It catches flakes. Test time-dependent logic with a frozen clock, and cover real-network behaviour in a separate, opt-in suite.
