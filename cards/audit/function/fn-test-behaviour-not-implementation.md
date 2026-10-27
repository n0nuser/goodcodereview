---
id: fn-test-behaviour-not-implementation
level: function
tags: [testing, maintainability, tests]
severity: should-fix
status: stable
lang: core
applies_when: A test exercises a function, class, or module with callers.
tool_gate: Refactor the code without changing what it does and run the tests; mutation testing shows whether they still catch real faults.
note: Google (Software Engineering at Google, ch. 12), Microsoft Learn (.NET unit-testing best practices), Spotify engineering. Spotify keeps tests of internals for isolated, complex logic; the Rust book calls testing private functions a debate.
borrowed_from:
  - https://abseil.io/resources/swe-book/html/ch12.html
  - https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices
  - https://engineering.atspotify.com/2018/01/11/testing-of-microservices
---

**Rule.** Assert what a caller can observe through the public interface, so a change that keeps behaviour does not break the test.

**Why.** A test tied to private calls, call order, or internal state fails when the code is restructured though nothing a caller sees changed. People then edit tests to match the code, and the suite stops protecting behaviour. It also pins whatever shape the code has today, including shapes that should change.

**FAIL**

```python
def test_checkout():
    cart = Cart()
    cart.add(Item("pen", 300))
    cart._recalculate_totals = Mock()          # private call
    cart.checkout()
    cart._recalculate_totals.assert_called_once()
```

**PASS**

```python
def test_checkout_charges_the_sum_of_item_prices():
    cart = Cart()
    cart.add(Item("pen", 300))
    cart.add(Item("book", 450))
    assert cart.checkout().total == 750
```

**Counterpoint.** "Some internals are complex enough to test on their own." Then give that logic its own unit with a public interface and test it through that. Testing a private function directly is a debated choice, so say why in the test.
