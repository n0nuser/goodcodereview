---
id: mod-mock-at-boundaries-only
level: module
tags: [testing]
severity: should-fix
status: draft
lang: core
applies_when: A test uses mocks, patches or fakes.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Mock only at the process boundary (HTTP, DB, cloud, clock, I/O).

**Why.** Mocks of internals pin the implementation, so any refactor breaks tests that prove nothing. A fake looser than the real client passes tests that the real backend rejects. Keep internal objects real, make a fake accept only what the real client accepts, and assert whole outcomes. See [[chg-agent-mock-asserting-tests]] for tests that must fail when behaviour breaks.

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

**Counterpoint.** "Isolated unit tests need every collaborator mocked." That tests the wiring you wrote, not the behaviour. Prefer a stub when behaviour is simple, and mock only what crosses the process edge.
