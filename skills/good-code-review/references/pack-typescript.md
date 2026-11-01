# TypeScript pack

A draft card is not vetted. Report a `FAIL` of one under Draft findings, at `should-fix` at most, never in the ledger or the verdict.

## typescript-mock-at-the-boundary

level: function  
severity: should-fix  
concerns: testing, maintainability  
applies_when: A Vitest test calls `vi.mock` on a module of the project's own code.  
lacks: orgs, Vitest and Testing Library state it; Testing Library's own project counts once and a third is missing

Fake the system boundary (network, clock, storage), for example with Mock Service Worker; do not `vi.mock` your own modules when a boundary fake would do.

## typescript-no-floating-promises

level: function  
severity: should-fix  
concerns: correctness, reliability  
applies_when: TypeScript code calls an async function or creates a Promise.  
lacks: duplicate, the stable card fn-handle-rejected-promises covers unhandled rejections; merge or delete

Every Promise is awaited, returned, or given a `.catch`; enable `@typescript-eslint/no-floating-promises`.

## typescript-partial-mock-keeps-original

level: function  
severity: should-fix  
concerns: testing, correctness  
applies_when: A `vi.mock` factory replaces a module that exports error classes, enums or constants the code under test also uses.  
lacks: orgs, only the Vitest docs describe `importOriginal`; the instanceof failure is not documented by a second organisation

A `vi.mock` factory spreads `await importOriginal()` and overrides only what the test needs; never swap an exported error class for a stub.

## typescript-shared-test-setup

level: module  
severity: discuss  
concerns: testing, maintainability  
applies_when: Several Vitest test files repeat the same setup (i18n init, MSW server, DOM matchers).  
lacks: orgs, only the Vitest docs state it; needs two more organisations

Put setup that every test file repeats into one file listed in `setupFiles`, not into each test file.

## typescript-strict-mode

level: codebase  
severity: should-fix  
concerns: correctness, maintainability  
applies_when: The repository has a `tsconfig.json`.  
lacks: orgs, only Microsoft's tsconfig reference states it; needs two more organisations

`tsconfig.json` sets `"strict": true`; switch off a single strict flag only with a written reason.
