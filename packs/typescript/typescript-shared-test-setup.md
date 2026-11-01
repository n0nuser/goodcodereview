---
id: typescript-shared-test-setup
level: module
tags: [testing, maintainability, typescript]
severity: discuss
status: draft
lacks: orgs, only the Vitest docs state it; needs two more organisations
lang: typescript
applies_when: Several Vitest test files repeat the same setup (i18n init, MSW server, DOM matchers).
tool_gate: none
borrowed_from:
  - https://vitest.dev/config/setupfiles
---

**Rule.** Put setup that every test file repeats into one file listed in `setupFiles`, not into each test file.

**Why.** Copies drift: one file inits i18n with other resources and a test passes alone but fails in the suite. One file is one place to change.

**FAIL**

```ts
// a.test.tsx, b.test.tsx, c.test.tsx each start with:
import i18n from 'i18next';
i18n.init({ lng: 'en', resources });
```

**PASS**

```ts
// vitest.config.ts
export default defineConfig({ test: { setupFiles: ['./test/setup.ts'] } });
// test/setup.ts runs i18n.init once per test file
```

**Counterpoint.** "A global setup hides what a test needs." Keep the shared file to things every test needs; per-test data stays in the test.
