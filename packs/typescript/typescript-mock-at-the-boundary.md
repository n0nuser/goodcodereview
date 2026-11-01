---
id: typescript-mock-at-the-boundary
level: function
tags: [testing, maintainability, typescript]
severity: should-fix
status: draft
lacks: orgs, Vitest and Testing Library state it; Testing Library's own project counts once and a third is missing
lang: typescript
applies_when: A Vitest test calls `vi.mock` on a module of the project's own code.
tool_gate: none
borrowed_from:
  - https://vitest.dev/guide/mocking/requests
  - https://testing-library.com/docs/guiding-principles/
---

**Rule.** Fake the system boundary (network, clock, storage), for example with Mock Service Worker; do not `vi.mock` your own modules when a boundary fake would do.

**Why.** A mocked internal module makes the test check the mock. The test then passes while the real wiring is broken, and fails on a harmless refactor.

**FAIL**

```ts
vi.mock('./api/client', () => ({ getUser: vi.fn().mockResolvedValue({ name: 'Ada' }) }));
```

**PASS**

```ts
import { http, HttpResponse } from 'msw';
server.use(http.get('/api/user', () => HttpResponse.json({ name: 'Ada' })));
```

**Counterpoint.** "Some internal seams are slow or nondeterministic." Mock those at their edge (the clock, the random source), not the module that uses them.
