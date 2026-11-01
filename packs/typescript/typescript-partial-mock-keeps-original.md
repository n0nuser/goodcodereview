---
id: typescript-partial-mock-keeps-original
level: function
tags: [testing, correctness, typescript]
severity: should-fix
status: draft
lacks: orgs, only the Vitest docs describe `importOriginal`; the instanceof failure is not documented by a second organisation
lang: typescript
applies_when: A `vi.mock` factory replaces a module that exports error classes, enums or constants the code under test also uses.
tool_gate: none
borrowed_from:
  - https://vitest.dev/guide/mocking/modules
---

**Rule.** A `vi.mock` factory spreads `await importOriginal()` and overrides only what the test needs; never swap an exported error class for a stub.

**Why.** Code under test does `err instanceof ApiError`. If the mock exports a different or empty class, the check is false and the error path is never exercised.

**FAIL**

```ts
vi.mock('./errors', () => ({ ApiError: class {} , fetchUser: vi.fn() }));
```

**PASS**

```ts
vi.mock('./errors', async (importOriginal) => ({
  ...(await importOriginal<typeof import('./errors')>()),
  fetchUser: vi.fn(),
}));
```

**Counterpoint.** "The real module has side effects on import." Then mock the effect's boundary; a factory that drops half the exports breaks other callers.
