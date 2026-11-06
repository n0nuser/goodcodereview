---
id: py-test-hygiene
level: module
tags: [testing, reliability, python]
severity: discuss
status: stable
lang: python
applies_when: A Python unit test touches the network, the shared filesystem, the database or the real clock. A per-test temporary directory (pytest `tmp_path`) is not the shared filesystem.
tool_gate: pytest-socket (`--disable-socket`), plus a unit-test CI job with no database service and no network credentials
borrowed_from:
  - https://pablogonzalez.me/posts/python-code-review-guide/
  - https://abseil.io/resources/swe-book/html/ch11.html
  - https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices
  - https://docs.spring.io/spring-framework/reference/testing/unit.html
  - https://docs.gitlab.com/development/testing_guide/testing_levels/
  - https://docs.djangoproject.com/en/5.1/topics/testing/tools/
  - https://guides.rubyonrails.org/testing.html
  - https://laravel.com/docs/12.x/testing
note: Google (small tests cannot reach the network or disk), Microsoft (a unit test has no file system or database and controls DateTime.Now), Spring (stub repositories, no runtime infrastructure), GitLab (mock outgoing requests, fake timers), Django (SimpleTestCase blocks database queries), Rails (travel_to, system tests in a separate CI step), Laravel (Unit tests cannot reach the database; most tests should be feature tests)
---

**Rule.** Keep unit tests off external I/O (the network, the shared filesystem and the database) and off the real clock, and run tests that need them in a separate, slower tier.

**Why.** A test that reaches the network, the disk or the database is slow and fails for reasons outside the code: an offline CI runner, a schema change, a clock at midnight. Those dependencies belong in an integration tier, where the failure is about the integration. Google's small tests cannot reach the network or disk; Microsoft's unit tests have no file system or database and control the clock through a seam; Django's `SimpleTestCase` blocks database queries by default.

**FAIL**

```python
def test_invoice_total(db):
    db.execute("insert into line ...")
    assert invoice_total(1) == 12.0

def test_token_expires():
    assert issue_token(ttl=60).expires_at > datetime.now()
```

**PASS**

```python
def test_invoice_total(fake_repo, frozen_clock):
    assert invoice_total(fake_repo) == 12.0

# pytest --disable-socket; the integration tests run in their own CI job
```

**Counterpoint.** "Most tests should hit the real stack, and mocking every collaborator hides real failures." Many teams keep most tests at the feature level and prefer real dependencies where they can keep them. Both hold: the rule is about the network, disk, database and clock boundary, not about doubling every collaborator. A feature or system test that boots the app belongs in the slower tier, and a team can run that tier on every merge. The unit tier stays fast and deterministic.
