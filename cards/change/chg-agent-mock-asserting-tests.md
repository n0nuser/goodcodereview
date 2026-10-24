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
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-test-behavior-not-implementation/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/tdd/SKILL.md
---

**Rule.** Write tests that fail when the behaviour breaks, and reject tests that mostly assert on mocks, copy the implementation, or were edited to match new output without explanation.

**Why.** Generated tests tend to confirm what the code does, so they pass against a bug. A suite that cannot fail gives false confidence. Mock only at real boundaries; see [[mod-mock-at-boundaries-only]].

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

**Counterpoint.** Mocks isolate slow dependencies. Mock at real boundaries and still assert on observable outcomes. To check a test, break the code deliberately once: if the test stays green, it fails this card. Test messages should show the input, the actual value, and the expected value.
