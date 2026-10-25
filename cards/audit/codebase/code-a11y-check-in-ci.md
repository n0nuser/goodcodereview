---
id: code-a11y-check-in-ci
level: codebase
tags: [accessibility, testing, frontend, ci]
severity: should-fix
status: draft
lacks: held, kept draft by Pablo's call; no org backs failing the build on a violation
lang: core
applies_when: The repo builds a web UI and has an automated test suite.
tool_gate: This card is the gate: axe (through `@axe-core/playwright` or similar) against rendered pages in the test step; `eslint-plugin-jsx-a11y` in the lint step for JSX code.
note: Rule backed by USWDS (axe and pa11y on every change, failing merges blocked), Microsoft Playwright (the test verifies there are no violations), and Deque axe-core (axe calls in existing functional tests, example throws on violations); the JSX lint (jsx-eslint only) and merge blocking in CI (USWDS only) sit in Why; GDS found the best of 13 automated tools caught 40% of planted barriers
borrowed_from:
  - https://github.com/jsx-eslint/eslint-plugin-jsx-a11y
  - https://www.deque.com/axe/core-documentation/
  - https://alphagov.github.io/accessibility-tool-audit/
  - https://www.gov.uk/service-manual/helping-people-to-use-your-service/making-your-service-accessible-an-introduction
  - https://designsystem.digital.gov/documentation/accessibility/
  - https://www.gov.uk/service-manual/helping-people-to-use-your-service/testing-for-accessibility
  - https://playwright.dev/docs/accessibility-testing
  - https://github.com/dequelabs/axe-core
---

**Rule.** Run an automated accessibility check, such as axe on rendered pages, in the automated tests, and fail the test on a violation.

**Why.** A violation that nobody sees at review ships. A failing test catches the missing label or `alt` on the pull request that adds it, and run in CI on every change it blocks the merge. A JSX lint such as `jsx-a11y` catches some of the same problems earlier, in the editor. Either way it is a floor: tools find only part of the problems, so a person still tests with a keyboard.

**FAIL**

```js
// e2e: axe runs, but nothing fails on what it finds
const results = await new AxeBuilder({ page }).analyze();
console.log(results.violations.length);
```

**PASS**

```js
// e2e: fail on any axe violation
const results = await new AxeBuilder({ page }).analyze();
expect(results.violations).toEqual([]);
```

**Counterpoint.** "Tools only catch a minority, and we have a backlog, so a failing check would turn every build red." The check catches the cheap failures at no review cost, which frees the manual pass for what only a person can judge. For the backlog, exclude the known violations by name (`disableRules`, `exclude`, or a fingerprint of each known issue) and fail on anything new. Remove each exclusion once it is fixed.
