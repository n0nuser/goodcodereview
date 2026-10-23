---
id: chg-agent-mock-asserting-tests
level: change
tags: [agents, testing]
severity: block
status: draft
lang: core
applies_when: Tests were generated or edited alongside the code under test, especially by an agent.
tool_gate: Mutation testing; fail the build if mutated code still passes.
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://go.dev/wiki/CodeReviewComments
  - https://michaelfeathers.silvrback.com/characterization-testing
---

**Rule.** A test must fail when the behaviour breaks; reject tests that mostly assert on mocks, copy the implementation, or were edited to match new output without explanation.

**Why.** Generated tests tend to confirm what the code does, passing against a bug. A suite that cannot fail gives false confidence.

**FAIL**

```python
repo = Mock(); repo.save.return_value = 1
assert svc.create(u) == 1          # asserts the mock's own answer
repo.save.assert_called_once()
```

**PASS**

```python
svc = Service(InMemoryRepo())
svc.create(u)
assert svc.get(u.id).email == u.email   # fails if create loses data
```

**Counterpoint.** Mocks isolate slow dependencies. Answer: mock at real boundaries and still assert on observable outcomes. Break the code deliberately once: if the test stays green, it fails this card. Test messages should show input, actual and expected.
