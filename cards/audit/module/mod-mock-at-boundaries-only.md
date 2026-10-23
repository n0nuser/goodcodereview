---
id: mod-mock-at-boundaries-only
level: module
tags: [testing]
severity: should-fix
status: draft
lang: core
applies_when: A test uses mocks, patches or fakes.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Mock only at the boundary (HTTP, DB, cloud, clock, I/O). Internal objects are real. A fake accepts only what the real thing accepts. Assert outcomes as whole objects.

**Why.** Mocks of internals pin the implementation, so any refactor breaks tests that prove nothing. A fake looser than the real client passes tests the real backend rejects.

**FAIL**

```text
mailer.send.assert_called_once()        # proves a call, not what was sent
class FakeStore:  def get(self, **_): ...   # accepts anything
```

**PASS**

```text
assert outbox.sent == [Email(to="ana@example.com", template="welcome")]
class FakeStore:  def get(self, key: str): ...   # real signature
```

**Counterpoint.** "Isolated unit tests need every collaborator mocked." That tests the wiring you wrote, not the behaviour. Prefer a stub when behaviour is simple; mock only what crosses the process edge.
